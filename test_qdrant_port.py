#!/usr/bin/env python3
"""Test Qdrant with explicit port 443"""
import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv("/data/workspace/cognee-config/.env")

async def test_qdrant():
    from qdrant_client import AsyncQdrantClient
    
    url = os.getenv("VECTOR_DB_URL")
    api_key = os.getenv("VECTOR_DB_KEY")
    
    print(f"🔗 URL: {url}")
    print(f"🔑 API Key: {api_key[:10]}...{api_key[-5:] if api_key else 'None'}")
    
    try:
        # Explicitly set port=443 for HTTPS
        print("\n--- Testing with port=443 ---")
        client = AsyncQdrantClient(url=url, api_key=api_key, port=443, prefer_grpc=False)
        collections = await client.get_collections()
        print(f"✅ Success! Collections: {[c.name for c in collections.collections]}")
        await client.close()
    except Exception as e:
        print(f"❌ Failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_qdrant())
