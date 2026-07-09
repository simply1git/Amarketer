---
title: Top 5 Proven KB Design Patterns for LLM Agents
type: research-findings
status: complete
ai_usage: >
  Each pattern has a TL;DR, evidence from a named production system, and
  implementation steps. Read TL;DRs first; expand only the pattern you need.
related: [02-prompting-methods.md, 03-metadata-schema.md, 04-red-flags.md, 05-amarketer-applications.md]
---

# Top 5 Proven KB Design Patterns for LLM Agents

Ordered by leverage. All are deployed in named production systems.

---

## Pattern 1 — Progressive disclosure (three-tier loading)

**TL;DR:** Never load a KB entry's full content by default. Always-loaded tier = name + one-line trigger description; tier 2 = full entry body, loaded when relevant; tier 3 = referenced detail files/scripts, loaded on demand.

**Production evidence:** Anthropic Agent Skills (Claude Code, Claude API). At startup only YAML frontmatter (`name`, `description`) of every skill is in the system prompt. When a task matches, the agent reads the full `SKILL.md`; that file references deeper files (`reference.md`, `forms.md`, executable scripts) loaded only if needed. Anthropic states this makes bundled context "effectively unbounded." Their PDF skill is the canonical example: lean core file + two reference files + a deterministic Python script for form extraction.

**How to implement in a KB:**
1. Every KB entry is a directory or file with frontmatter: `name` (kebab-case slug) + `description` (one line stating **when to use it**, not just what it is — this line does the routing).
2. Build an always-in-context index file listing only name + description of every entry (cap it; Claude Code's MEMORY.md analog has a 200-line hard limit — see [04-red-flags.md](04-red-flags.md)).
3. Body ≤ ~500 lines; when it grows, split rarely-co-used content into referenced sub-files ("keeping the paths separate reduces token usage when contexts are mutually exclusive").
4. Bundle deterministic operations as scripts, and state explicitly whether the agent should *execute* them or *read them as reference*.
5. Iterate on `description` wording by observing when the agent triggers the entry wrongly or misses it — Anthropic's stated tuning loop.

---

## Pattern 2 — Contextual retrieval (situated chunks + hybrid lexical/semantic search)

**TL;DR:** Before embedding a chunk, prepend a 50–100 token LLM-generated context explaining where it sits in its source document; index both embeddings and BM25; rerank.

**Production evidence:** Anthropic engineering blog + Claude Cookbook, deployed via Amazon Bedrock Knowledge Bases. Numbers: contextual embeddings alone cut top-20 retrieval failure 35% (5.7%→3.7%); + contextual BM25: 49% (→2.9%); + Cohere reranking: 67% (→1.9%). One-time cost ≈ $1.02 per million document tokens using Claude Haiku with prompt caching (whole document cached, per-chunk calls cheap).

**Exact context-generation prompt used:**
```
<document>
{{WHOLE_DOCUMENT}}
</document>
Here is the chunk we want to situate within the whole document
<chunk>
{{CHUNK_CONTENT}}
</chunk>
Please give a short succinct context to situate this chunk within the overall
document for the purposes of improving search retrieval of the chunk. Answer
only with the succinct context and nothing else.
```

**How to implement in a KB:**
1. First check size: **KB ≤ 200K tokens → no RAG at all**; put the whole corpus in the prompt with caching.
2. Chunk without overlap (systematic studies show overlap adds cost, no quality); keep chunks under ~2.5K tokens (quality "context cliff" beyond that); sentence/section-boundary chunking is the cost-effective default.
3. Run the prompt above per chunk (cheap model + prompt caching); store `context + chunk` as the embedded text.
4. Index in both a vector store (Voyage/Gemini embeddings tested best) and BM25; merge results.
5. Retrieve ~150 candidates → rerank → pass **top-20** to the model (top-20 beat top-10 and top-5 in Anthropic's evals).

---

## Pattern 3 — Agentic search over plain files (just-in-time retrieval)

**TL;DR:** For corpora with meaningful structure and names, skip the vector index. Store knowledge as plain, well-named files and let the agent iteratively grep/glob/read — the KB's *file layout and naming* is the retrieval system.

**Production evidence:** Claude Code — Anthropic built a vector-RAG pipeline, benchmarked agentic search (grep/glob/read with iterative refinement) against it, and per creator Boris Cherny it "outperformed everything. By a lot"; the RAG pipeline was deleted. Cursor and Devin converged on the same plan→glob/grep→read→refine loop. Anthropic's context-engineering guidance generalizes it: agents keep *lightweight identifiers* (paths, links, queries) in context and load data just-in-time, hybridizing with some upfront retrieval when data is stable.

**Why it wins where it wins:** exact-match precision (no fuzzy false positives on identifiers like SKUs, program names, error codes), zero index staleness, no ingestion pipeline, and iterative refinement — one-shot RAG can't adapt its query after seeing bad results.

**How to implement in a KB:**
1. Store entries as Markdown/JSON files in a semantic directory tree (`programs/`, `tactics/`, `channels/`); names are greppable identifiers (`amazon-associates-commission-rates.md`).
2. Put exact identifiers (program names, network names, metric names) verbatim in file bodies so grep hits them.
3. Give the agent grep/glob/read tools plus a top-level map file (the Pattern-1 index) as the entry point.
4. Keep files small and single-topic so a read costs little; cross-link with relative links the agent can follow.
5. Reserve embeddings for genuinely fuzzy semantic queries; hybrid is fine, but don't build the index first.

---

## Pattern 4 — Summary-first hierarchical retrieval with structured metadata filters (+ graphs for relational questions)

**TL;DR:** Represent each document as a concise summary + structured metadata dictionary at the top level; route queries by summary/metadata first, drill into chunks second. Add a knowledge graph only when questions are inherently relational.

**Production evidence:** LlamaIndex structured hierarchical retrieval (production pattern: per-document metadata dict with extracted summary stored as vector-DB filters; auto-retrieval infers both semantic query and metadata filters). AutoMergingRetriever: when most retrieved child chunks share a parent, return the parent instead. Graph variant: LinkedIn customer support GraphRAG — parsed tickets into a knowledge graph, cut median resolution time **28.6%** (≈40h→15h), +77.6% MRR over baseline; Microsoft GraphRAG reported **26–97% fewer tokens** than alternatives on global-question tasks.

**How to implement in a KB:**
1. At ingestion, extract per document: 1–3 sentence summary + typed metadata (see [03-metadata-schema.md](03-metadata-schema.md)).
2. Store metadata as vector-DB filter fields; retrieval = LLM infers filters from the query (auto-retrieval), then semantic search within the filtered set.
3. Parent/child chunking: retrieve small chunks for precision, auto-merge to parent for context.
4. Metadata must flow end-to-end: filter on it at retrieval, print it in the prompt, use it for access control.
5. Build a graph layer only for relational queries ("which tactics work for programs like X?"); entity-relation extraction at ingestion, graph traversal at query time.

---

## Pattern 5 — Self-improving knowledge loop via file-based memory

**TL;DR:** The proven self-improvement mechanism in production is *not* fine-tuning — it's the agent writing validated learnings back into its own KB as files, plus context compaction to survive long horizons.

**Production evidence:** Anthropic memory tool (`memory_20250818`, GA on the Messages API): agent reads/writes a client-side directory of memory files across sessions; combined with context editing, internal benchmark on a 100-turn web-search task showed **84% token savings and +39% performance**. Claude Code: CLAUDE.md / MEMORY.md injected each session. Letta (MemGPT lineage): agent manages its own memory tiers via tool calls — core in-context blocks + archival store + explicit forgetting. Anthropic's skill-authoring guidance closes the loop: "ask Claude to capture its successful approaches and common mistakes into reusable context and code."

**How to implement in a KB:**
1. Give the agent write access to a dedicated `learned/` area of the KB, same entry format as curated content but `status: unverified`.
2. After each task, agent appends outcome notes (structured note-taking): what worked, what failed, with metrics.
3. A promotion step (scheduled agent or human review) merges duplicates, resolves contradictions with curated entries, and flips `status` to `verified` — never let unreviewed self-writes silently override curated facts.
4. Use compaction for long sessions: summarize the trajectory preserving decisions and discard raw tool output ("maximize recall first, then precision" — Anthropic).
5. Enforce an index-size budget with an explicit forgetting/archival policy (Letta's tiered pattern: small always-in-context core + retrievable archive).

---

## Cross-cutting: fine-tuning datasets

Deliberately thin here because production teams overwhelmingly solve knowledge problems with retrieval/context, not fine-tuning — fine-tuning is used for *behavior/format*, not facts (facts baked into weights go stale and can't be attributed). Where teams do fine-tune (e.g., HF ecosystem practice), the dataset pattern mirrors KB design: instruction/response pairs generated *from* the KB with provenance kept in a metadata column, so the KB remains the source of truth. Recommendation for Amarketer: KB-first; revisit fine-tuning only for output-format consistency.
