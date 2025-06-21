# API Documentation

## Overview

The AI Knowledge Graph Engine provides a comprehensive REST API for accessing and querying the world's largest open catalog of AI capabilities. Our API is designed for researchers, developers, and organizations requiring programmatic access to AI model and tool metadata.

## Base URL

- **Production**: `https://api.ai-knowledge.dev`
- **Development**: `http://localhost:8000`

## Authentication

### API Keys (Production)
```bash
curl -H "Authorization: Bearer YOUR_API_KEY" \
  "https://api.ai-knowledge.dev/v1/search?q=transformer"
```

### Rate Limiting
- **Free Tier**: 1,000 requests/hour
- **Research Tier**: 10,000 requests/hour
- **Enterprise Tier**: Unlimited

## Core Endpoints

### Search AI Capabilities

Search across all indexed AI models, tools, and agents.

```http
GET /api/v1/search
```

**Parameters:**
- `q` (string, required): Search query
- `limit` (integer, optional): Results per page (max 100, default 20)
- `offset` (integer, optional): Pagination offset (default 0)
- `platform` (string, optional): Filter by platform (github, huggingface, arxiv, etc.)
- `category` (string, optional): Filter by category (nlp, computer-vision, etc.)
- `min_stars` (integer, optional): Minimum star count
- `language` (string, optional): Programming language filter
- `license` (string, optional): License type filter

**Example:**
```bash
curl "https://api.ai-knowledge.dev/v1/search?q=transformer&platform=huggingface&min_stars=100&limit=50"
```

**Response:**
```json
{
  "results": [
    {
      "id": "hf_model_12345",
      "name": "bert-base-uncased",
      "description": "BERT base model (uncased) for natural language understanding",
      "platform": "huggingface",
      "category": "nlp",
      "subcategory": "text-classification",
      "url": "https://huggingface.co/bert-base-uncased",
      "stars": 5420,
      "downloads": 2847291,
      "license": "apache-2.0",
      "created_at": "2019-10-17T14:30:00Z",
      "updated_at": "2024-12-15T09:22:31Z",
      "tags": ["transformer", "bert", "nlp", "pytorch"],
      "metrics": {
        "model_size": "110M",
        "inference_time": "12ms",
        "accuracy": 0.847
      }
    }
  ],
  "total": 1247,
  "limit": 50,
  "offset": 0,
  "query_time_ms": 23
}
```

### Get Model Details

Retrieve comprehensive information about a specific AI model or tool.

```http
GET /api/v1/models/{model_id}
```

**Example:**
```bash
curl "https://api.ai-knowledge.dev/v1/models/hf_model_12345"
```

**Response:**
```json
{
  "id": "hf_model_12345",
  "name": "bert-base-uncased",
  "description": "BERT base model (uncased) for natural language understanding tasks",
  "platform": "huggingface",
  "category": "nlp",
  "subcategory": "text-classification",
  "url": "https://huggingface.co/bert-base-uncased",
  "repository_url": "https://github.com/huggingface/transformers",
  "paper_url": "https://arxiv.org/abs/1810.04805",
  "stars": 5420,
  "downloads": 2847291,
  "license": "apache-2.0",
  "created_at": "2019-10-17T14:30:00Z",
  "updated_at": "2024-12-15T09:22:31Z",
  "tags": ["transformer", "bert", "nlp", "pytorch", "tensorflow"],
  "frameworks": ["pytorch", "tensorflow", "jax"],
  "languages": ["python"],
  "metrics": {
    "model_size": "110M",
    "parameters": 110000000,
    "inference_time": "12ms",
    "memory_usage": "440MB",
    "accuracy": 0.847,
    "f1_score": 0.832
  },
  "related_models": [
    {
      "id": "hf_model_12346",
      "name": "bert-large-uncased",
      "similarity": 0.95
    }
  ],
  "usage_examples": [
    {
      "language": "python",
      "code": "from transformers import BertTokenizer, BertModel\\ntokenizer = BertTokenizer.from_pretrained('bert-base-uncased')\\nmodel = BertModel.from_pretrained('bert-base-uncased')"
    }
  ]
}
```

### Browse Categories

Get AI capabilities organized by categories and subcategories.

```http
GET /api/v1/categories
```

**Response:**
```json
{
  "categories": {
    "nlp": {
      "name": "Natural Language Processing",
      "count": 45230,
      "subcategories": {
        "text-classification": 12450,
        "text-generation": 8930,
        "translation": 5420,
        "summarization": 3210
      }
    },
    "computer-vision": {
      "name": "Computer Vision",
      "count": 38940,
      "subcategories": {
        "image-classification": 15230,
        "object-detection": 9840,
        "image-generation": 7650,
        "semantic-segmentation": 4220
      }
    }
  }
}
```

### Analytics and Trends

Access aggregated analytics and trend data.

```http
GET /api/v1/analytics/trends
```

**Parameters:**
- `timeframe` (string, optional): Time period (7d, 30d, 90d, 1y) (default: 30d)
- `category` (string, optional): Category filter
- `metric` (string, optional): Trend metric (stars, downloads, models_created)

**Example:**
```bash
curl "https://api.ai-knowledge.dev/v1/analytics/trends?timeframe=30d&category=nlp&metric=models_created"
```

**Response:**
```json
{
  "timeframe": "30d",
  "category": "nlp",
  "metric": "models_created",
  "data_points": [
    {
      "date": "2024-12-01",
      "value": 234,
      "cumulative": 45234
    },
    {
      "date": "2024-12-02",
      "value": 189,
      "cumulative": 45423
    }
  ],
  "summary": {
    "total_change": 1847,
    "percentage_change": 4.2,
    "average_daily": 61.6
  }
}
```

### Platform Statistics

Get platform-specific statistics and metadata.

```http
GET /api/v1/platforms
```

**Response:**
```json
{
  "platforms": [
    {
      "name": "huggingface",
      "display_name": "Hugging Face",
      "total_models": 156789,
      "categories": ["nlp", "computer-vision", "audio"],
      "last_updated": "2024-12-21T10:30:00Z",
      "update_frequency": "hourly",
      "api_coverage": 0.98
    },
    {
      "name": "github",
      "display_name": "GitHub",
      "total_repositories": 487291,
      "categories": ["all"],
      "last_updated": "2024-12-21T10:15:00Z",
      "update_frequency": "real-time",
      "api_coverage": 0.85
    }
  ]
}
```

## Advanced Features

### Semantic Search

Use natural language queries for semantic similarity search.

```http
POST /api/v1/search/semantic
```

**Request Body:**
```json
{
  "query": "I need a model for analyzing sentiment in social media posts",
  "limit": 10,
  "min_relevance": 0.7
}
```

### Batch Operations

Process multiple queries in a single request.

```http
POST /api/v1/batch
```

**Request Body:**
```json
{
  "queries": [
    {
      "id": "query_1",
      "endpoint": "/v1/search",
      "params": {"q": "transformer", "limit": 5}
    },
    {
      "id": "query_2",
      "endpoint": "/v1/models/hf_model_12345"
    }
  ]
}
```

### Export Data

Export search results in various formats.

```http
GET /api/v1/export
```

**Parameters:**
- `format` (string, required): Output format (csv, json, xlsx)
- `query` (string, optional): Search query for filtering
- `category` (string, optional): Category filter
- `fields` (string, optional): Comma-separated list of fields to include

**Example:**
```bash
curl "https://api.ai-knowledge.dev/v1/export?format=csv&category=nlp&fields=name,description,stars,url" -o nlp_models.csv
```

## Error Handling

### HTTP Status Codes

- `200 OK`: Request successful
- `400 Bad Request`: Invalid request parameters
- `401 Unauthorized`: Invalid or missing API key
- `403 Forbidden`: Rate limit exceeded
- `404 Not Found`: Resource not found
- `429 Too Many Requests`: Rate limit exceeded
- `500 Internal Server Error`: Server error

### Error Response Format

```json
{
  "error": {
    "code": "INVALID_PARAMETER",
    "message": "The 'limit' parameter must be between 1 and 100",
    "details": {
      "parameter": "limit",
      "provided_value": 150,
      "valid_range": [1, 100]
    },
    "request_id": "req_abc123def456"
  }
}
```

## SDKs and Libraries

### Python SDK

```bash
pip install ai-knowledge-client
```

```python
from ai_knowledge import Client

client = Client(api_key="your_api_key")

# Search for models
results = client.search("transformer", platform="huggingface", limit=10)

# Get model details
model = client.get_model("hf_model_12345")

# Get analytics
trends = client.get_trends(timeframe="30d", category="nlp")
```

### JavaScript SDK

```bash
npm install @ai-knowledge/client
```

```javascript
import { AIKnowledgeClient } from '@ai-knowledge/client';

const client = new AIKnowledgeClient({ apiKey: 'your_api_key' });

// Search for models
const results = await client.search('transformer', {
  platform: 'huggingface',
  limit: 10
});

// Get model details
const model = await client.getModel('hf_model_12345');
```

## Webhooks

Subscribe to real-time updates when new models are added or existing models are updated.

```http
POST /api/v1/webhooks
```

**Request Body:**
```json
{
  "url": "https://your-api.com/webhooks/ai-knowledge",
  "events": ["model.created", "model.updated"],
  "filters": {
    "categories": ["nlp", "computer-vision"],
    "min_stars": 100
  }
}
```

## GraphQL API (Beta)

Access data using GraphQL for more flexible queries.

```http
POST /api/graphql
```

**Example Query:**
```graphql
query GetTransformerModels {
  models(
    query: "transformer"
    platform: HUGGINGFACE
    limit: 10
  ) {
    edges {
      node {
        id
        name
        description
        stars
        downloads
        metrics {
          modelSize
          accuracy
        }
        relatedModels(limit: 3) {
          name
          similarity
        }
      }
    }
    pageInfo {
      hasNextPage
      endCursor
    }
  }
}
```

## Support

- **API Status**: [status.ai-knowledge.dev](https://status.ai-knowledge.dev)
- **Documentation**: [docs.ai-knowledge.dev](https://docs.ai-knowledge.dev)
- **Support**: api-support@ai-knowledge.dev
- **Rate Limit Increases**: enterprise@ai-knowledge.dev

---

*Last Updated: December 21, 2024*
