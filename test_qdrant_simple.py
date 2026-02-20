#!/usr/bin/env python3
"""Test simple Qdrant connection"""
import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv("/data/workspace/cognee-config/.env")

async def test_qdrant():
    from qdrant_client import AsyncQdrantClient
    
    url = os.getenv("VECTOR_DB_URL")
    api_key = os.getenv("VECTOR_DB_KEY")
    
    print(f"🔗 Connecting to Qdrant at: {url}")
    print(f"🔑 API Key present: {bool(api_key)}")
    
    try:
        client = AsyncQdrantClient(url=url, api_key=api_key)
        
        # Test connection by listing collections
        collections = await client.get_collections()
        print(f"✅ Qdrant connection successful!")
        print(f"📦 Collections: {[c.name for c in collections.collections]}")
        
        # Try to create a test collection
        test_collection = "test_cognee_collection"
        
        from qdrant_client import models
        
        if not await client.collection_exists(test_collection):
            await client.create_collection(
                collection_name=test_collection,
                vectors_config={
                    "text": models.VectorParams(
                        size=1536,
                        distance=models.Distance.COSINE,
                    )
                }
            )
            print(f"✅ Created test collection: {test_collection}")
        else:
            print(f"ℹ️ Collection already exists: {test_collection}")
        
        await client.close()
        print("✅ Qdrant test completed successfully!")
        
    except Exception as e:
        print(f"❌ Qdrant connection failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_qdrant())
