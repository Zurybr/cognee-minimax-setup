#!/usr/bin/env python3
"""Test Qdrant connection with different configurations"""
import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv("/data/workspace/cognee-config/.env")

async def test_qdrant():
    from qdrant_client import AsyncQdrantClient
    import httpx
    
    url = os.getenv("VECTOR_DB_URL")
    api_key = os.getenv("VECTOR_DB_KEY")
    
    print(f"🔗 Testing Qdrant connection to: {url}")
    print(f"🔑 API Key: {api_key[:10]}...{api_key[-5:] if api_key else 'None'}")
    
    # Try with explicit headers
    headers = {"api-key": api_key} if api_key else None
    print(f"📋 Headers: {headers}")
    
    try:
        # Method 1: Using api_key parameter (standard way)
        print("\n--- Method 1: Standard api_key parameter ---")
        client1 = AsyncQdrantClient(url=url, api_key=api_key)
        collections1 = await client1.get_collections()
        print(f"✅ Method 1 success! Collections: {[c.name for c in collections1.collections]}")
        await client1.close()
    except Exception as e:
        print(f"❌ Method 1 failed: {e}")
    
    try:
        # Method 2: Using headers parameter
        print("\n--- Method 2: Using headers ---")
        client2 = AsyncQdrantClient(url=url, headers=headers)
        collections2 = await client2.get_collections()
        print(f"✅ Method 2 success! Collections: {[c.name for c in collections2.collections]}")
        await client2.close()
    except Exception as e:
        print(f"❌ Method 2 failed: {e}")
    
    try:
        # Method 3: Using httpx client with custom transport
        print("\n--- Method 3: Custom httpx client ---")
        custom_headers = {"api-key": api_key} if api_key else {}
        http_client = httpx.AsyncClient(headers=custom_headers, timeout=30.0)
        client3 = AsyncQdrantClient(url=url, prefer_grpc=False)
        # Manually set the http client
        # This won't work directly but let's see
        collections3 = await client3.get_collections()
        print(f"✅ Method 3 success! Collections: {[c.name for c in collections3.collections]}")
        await client3.close()
    except Exception as e:
        print(f"❌ Method 3 failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_qdrant())
