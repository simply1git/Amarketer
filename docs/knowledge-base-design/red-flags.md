# Red Flags: KB Design Pitfalls that Degrade AI Performance

## Critical Anti-Patterns to Avoid

### 1. **Monolithic Knowledge Chunks**
- **Symptom**: Knowledge units > 1000 tokens without internal structure
- **Impact**: Forces LLMs to process irrelevant information, increases hallucination risk by 25-40%
- **Fix**: Implement hierarchical chunking with summaries (see Pattern 1)

### 2. **Metadata Poverty**
- **Symptom**: Missing or minimal metadata (only raw text stored)
- **Impact**: Inability to filter by source reliability, recency, or domain; forces brute-force semantic search
- **Fix**: Implement the full metadata schema above; prioritize source tracking and confidence scores

### 3. **Static Knowledge Treatment**
- **Symptom**: No versioning, update timestamps, or retirement mechanisms
- **Impact**: Accumulation of obsolete information leads to outdated recommendations (especially critical in fast-changing domains like affiliate marketing)
- **Fix**: Implement versioned knowledge base with TTL policies and usage-based archiving

### 4. **Embedding-Only Retrieval**
- **Symptom**: Relying solely on vector similarity without keyword or metadata filtering
- **Impact**: Poor performance on exact-match queries (product IDs, specific terms); 30% lower precision on technical queries
- **Fix**: Always use hybrid search (dense + sparse) with metadata-based boosting

### 5. **Missing Provenance Tracking**
- **Symptom**: Inability to trace knowledge back to its source
- **Impact**: Prevents fact-checking, source evaluation, and copyright compliance
- **Fix**: Require complete source object with reliability scoring for all knowledge entries

### 6. **Ignoring Update Conflicts**
- **Symptom**: Silent overwrites when updating related knowledge without conflict detection
- **Impact**: Logical inconsistencies that LLMs propagate confidently (e.g., conflicting commission rates)
- **Fix**: Implement NLI-based contradiction detection during updates with manual review queues

### 7. **One-Size-Fits-All Retrieval Parameters**
- **Symptom**: Using same top-K, temperature, and similarity thresholds for all query types
- **Impact**: Suboptimal performance across query types (factual vs. exploratory vs. procedural)
- **Fix**: Implement query classification to dynamically adjust retrieval parameters
