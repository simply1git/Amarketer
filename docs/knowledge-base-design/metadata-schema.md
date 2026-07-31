# Metadata Schema Recommendations

## Core Metadata Schema (JSON Schema)
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["id", "content", "created_at", "updated_at", "source"],
  "properties": {
    "id": {
      "type": "string",
      "format": "uuid",
      "description": "Unique identifier for the knowledge unit"
    },
    "content": {
      "type": "string",
      "description": "The actual knowledge content (text, code, structured data)"
    },
    "summary": {
      "type": "string",
      "maxLength": 100,
      "description": "Concise summary for quick relevance assessment (<50 tokens)"
    },
    "created_at": {
      "type": "string",
      "format": "date-time",
      "description": "Timestamp when knowledge was first added"
    },
    "updated_at": {
      "type": "string",
      "format": "date-time",
      "description": "Timestamp of last modification"
    },
    "version": {
      "type": "string",
      "pattern": "^\d+\.\d+\.\d+$",
      "description": "Semantic version of this knowledge unit"
    },
    "source": {
      "type": "object",
      "required": ["type", "id", "reliability"],
      "properties": {
        "type": {
          "enum": ["internal_doc", "external_api", "user_feedback", "web_scrape", "code_repo", "agent_interaction"],
          "description": "Origin of the knowledge"
        },
        "id": {
          "type": "string",
          "description": "Source identifier (URL, doc ID, etc.)"
        },
        "reliability": {
          "type": "number",
          "minimum": 0,
          "maximum": 1,
          "description": "Trustworthiness score (0.0 = untrusted, 1.0 = fully trusted)"
        },
        "accessed_at": {
          "type": "string",
          "format": "date-time"
        }
      }
    },
    "entities": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "name": { "type": "string" },
          "type": { "enum": ["PERSON", "ORGANIZATION", "PRODUCT", "CAMPAIGN", "DATE", "METRIC", "URL"] },
          "confidence": { "type": "number", "minimum": 0, "maximum": 1 }
        }
      },
      "description": "Named entities extracted from content"
    },
    "topics": {
      "type": "array",
      "items": {
        "type": "string",
        "pattern": "^[a-z][a-z0-9_]*(\.[a-z][a-z0-9_]*)*$"
      },
      "description": "Hierarchical topic tags (e.g., 'marketing.affiliate.tracking.parameters')"
    },
    "confidence_score": {
      "type": "number",
      "minimum": 0,
      "maximum": 1,
      "description": "Model-derived confidence in factual accuracy"
    },
    "language": {
      "type": "string",
      "enum": ["en", "es", "fr", "de", "ja", "zh"],
      "default": "en"
    },
    "tags": {
      "type": "array",
      "items": { "type": "string" },
      "description": "Free-form tags for flexible categorization"
    },
    "relationships": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "target_id": { "type": "string", "format": "uuid" },
          "type": {
            "enum": ["supports", "contradicts", "updates", "references", "prerequisite_for"]
          },
          "strength": { "type": "number", "minimum": 0, "maximum": 1 }
        }
      },
      "description": "Relationships to other knowledge units"
    },
    "usage_stats": {
      "type": "object",
      "properties": {
        "access_count": { "type": "integer", "minimum": 0 },
        "success_rate": { "type": "number", "minimum": 0, "maximum": 1 },
        "last_accessed": { "type": "string", "format": "date-time" }
      },
      "description": "Telemetry on how this knowledge is used in practice"
    }
  }
}
```

## AI-Specific Field Explanations

- **summary**: Enables rapid relevance filtering without loading full content, reducing token usage by 40-60%
- **entities**: Allows entity-based routing and Fact-checking against knowledge graphs
- **topics**: Facilitates domain-specific retrieval boosting and prevents cross-contamination
- **confidence_score**: Triggers uncertainty-based behaviors (additional verification, human handoff)
- **source.reliability**: Weights evidence during conflict resolution (more trusted sources override less trusted)
- **usage_stats**: Powers popularity-based ranking and identifies obsolete knowledge for archiving
- **relationships**: Enables reasoning over knowledge graphs and contradiction detection
- **version**: Supports rollback and A/B testing of knowledge updates
