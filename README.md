# Cognee + MiniMax + Qdrant + Memgraph Setup

Complete guide for setting up Cognee with MiniMax LLM, Qdrant vector database, and Memgraph graph database.

## Overview

This setup provides a complete knowledge graph system with:
- **Cognee**: Knowledge graph engine for AI agents
- **MiniMax**: Cost-effective LLM (via Anthropic-compatible API)
- **Qdrant**: Vector search engine
- **Memgraph**: Graph database for knowledge relationships

## Architecture

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Cognee    │────▶│  MiniMax    │     │   Qdrant    │
│   (Core)    │     │    (LLM)    │     │  (Vectors)  │
└──────┬──────┘     └─────────────┘     └─────────────┘
       │
       ▼
┌─────────────┐
│  Memgraph   │
│   (Graph)   │
└─────────────┘
```

## Prerequisites

- Python 3.11+
- Virtual environment
- API keys for MiniMax and OpenAI (for embeddings)
- Qdrant instance (self-hosted or cloud)
- Memgraph instance

## Installation

### 1. Create Virtual Environment

```bash
python3 -m venv venv-cognee
source venv-cognee/bin/activate  # Linux/Mac
# or
venv-cognee\Scripts\activate  # Windows
```

### 2. Install Dependencies

```bash
pip install cognee
pip install cognee-community-vector-adapter-qdrant
pip install cognee-community-graph-adapter-memgraph
pip install python-dotenv anthropic
```

### 3. Environment Configuration

Create `.env` file:

```env
# ============================================
# LLM Configuration - MiniMax via Anthropic API
# ============================================
LLM_PROVIDER=anthropic
LLM_MODEL=MiniMax-M2.5
LLM_API_KEY=your_minimax_api_key
LLM_ENDPOINT=https://api.minimax.io/anthropic

# ============================================
# Embeddings Configuration (OpenAI)
# ============================================
EMBEDDING_PROVIDER=openai
EMBEDDING_MODEL=text-embedding-3-small
EMBEDDING_API_KEY=your_openai_api_key
EMBEDDING_DIMENSIONS=1536

# ============================================
# Vector Store - Qdrant
# ============================================
VECTOR_DB_PROVIDER=qdrant
VECTOR_DB_URL=https://your-qdrant-instance.com
VECTOR_DB_KEY=your_qdrant_api_key

# ============================================
# Graph Store - Memgraph
# ============================================
GRAPH_DATABASE_PROVIDER=memgraph
GRAPH_DATABASE_URL=bolt://your-memgraph-ip:7687
GRAPH_DATABASE_USERNAME=your_username
GRAPH_DATABASE_PASSWORD=your_password

# ============================================
# Other Configurations
# ============================================
ENABLE_BACKEND_ACCESS_CONTROL=false
ENVIRONMENT=development
```

## Configuration Details

### MiniMax Setup

MiniMax provides an Anthropic-compatible API endpoint:

- **Base URL**: `https://api.minimax.io/anthropic`
- **Models**: `MiniMax-M2.5`, `MiniMax-M2.1`, `MiniMax-M2`
- **Cost**: ~$0.30/M tokens (much cheaper than OpenAI)

### Qdrant Setup

Qdrant runs via HTTPS on port 443 (not 6333):

```env
VECTOR_DB_URL=https://qdrant.e6labs.lat
```

**Important**: The Qdrant adapter was modified to use port 443 for HTTPS connections instead of the default 6333.

### Memgraph Setup

Standard Bolt connection:

```env
GRAPH_DATABASE_URL=bolt://31.97.214.150:7687
```

## Usage

### Basic Test Script

```python
#!/usr/bin/env python3
import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv(".env")

# Import adapters
import cognee_community_vector_adapter_qdrant.register
from cognee_community_graph_adapter_memgraph import register as register_memgraph
register_memgraph()

# Import Cognee
import cognee
from cognee.api.v1.cognify import cognify
from cognee.api.v1.search import search
from cognee.api.v1.add import add

async def test_cognee():
    # Add data
    await add("Your text here", "dataset_name")
    
    # Create knowledge graph
    await cognify("dataset_name")
    
    # Search
    results = await search("Your query", "dataset_name")
    print(results)

if __name__ == "__main__":
    asyncio.run(test_cognee())
```

## Code Modifications

### 1. Qdrant Adapter Fix

**File**: `cognee_community_vector_adapter_qdrant/qdrant_adapter.py`

Modified `get_qdrant_client()` to detect HTTPS and use port 443:

```python
def get_qdrant_client(self) -> AsyncQdrantClient:
    if self.url is not None:
        import urllib.parse
        parsed = urllib.parse.urlparse(self.url)
        if parsed.port is None:
            port = 443 if parsed.scheme == "https" else 80
        else:
            port = parsed.port
        # Added timeout parameter
        return AsyncQdrantClient(
            url=self.url, 
            api_key=self.api_key, 
            port=port,
            timeout=60.0
        )
```

### 2. Anthropic Adapter Fix

**File**: `cognee/infrastructure/llm/structured_output_framework/litellm_instructor/llm/anthropic/adapter.py`

Modified to support custom endpoints (for MiniMax):

```python
def __init__(
    self, api_key: str, model: str, max_completion_tokens: int, 
    instructor_mode: str = None, endpoint: str = None
):
    # ... 
    if endpoint:
        self.aclient = instructor.patch(
            create=anthropic.AsyncAnthropic(
                api_key=self.api_key, base_url=endpoint
            ).messages.create,
            mode=instructor.Mode(self.instructor_mode),
        )
```

### 3. LLM Client Factory Fix

**File**: `cognee/infrastructure/llm/structured_output_framework/litellm_instructor/llm/get_llm_client.py`

Modified CUSTOM provider to pass endpoint:

```python
return GenericAPIAdapter(
    llm_config.llm_api_key,
    llm_config.llm_model,
    max_completion_tokens,
    "Custom",
    endpoint=llm_config.llm_endpoint,  # Added
    # ...
)
```

## Troubleshooting

### Issue: Qdrant Connection Timeout

**Solution**: Increased timeout from default to 60s:
```python
return AsyncQdrantClient(..., timeout=60.0)
```

### Issue: MiniMax Not Recognized

**Solution**: Use Anthropic provider with MiniMax endpoint:
```env
LLM_PROVIDER=anthropic
LLM_ENDPOINT=https://api.minimax.io/anthropic
```

### Issue: Port 6333 Blocked

**Solution**: Use HTTPS on port 443:
```env
VECTOR_DB_URL=https://qdrant.e6labs.lat  # Not :6333
```

## Costs Comparison

| Provider | Input Cost | Output Cost | Notes |
|----------|------------|-------------|-------|
| OpenAI GPT-4o-mini | $0.15/M | $0.60/M | Default |
| MiniMax M2.5 | $0.30/M | $1.20/M | Cheaper than GPT-4 |
| OpenAI Embeddings | $0.02/M | - | For vectors |

## Files

- `.env` - Environment configuration
- `test_connection.py` - Test script
- `README.md` - This file

## Credits

Setup created for Brandom's AI infrastructure using:
- Cognee v0.5.2
- MiniMax API
- Qdrant Vector DB
- Memgraph Graph DB
