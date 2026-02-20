#!/usr/bin/env python3
"""Debug Qdrant client connection"""
import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv("/data/workspace/cognee-config/.env")

async def debug_qdrant():
    from qdrant_client import AsyncQdrantClient
    import httpx
    
    url = os.getenv("VECTOR_DB_URL")
    api_key = os.getenv("VECTOR_DB_KEY")
    
    print(f"🔗 URL: {url}")
    print(f"🔑 API Key: {api_key[:10]}...{api_key[-5:] if api_key else 'None'}")
    
    try:
        # Create client with gRPC disabled
        print("\n--- Creating client (prefer_grpc=False) ---")
        client = AsyncQdrantClient(url=url, api_key=api_key, prefer_grpc=False)
        
        print(f"Client type: {type(client)}")
        print(f"Client _client type: {type(client._client)}")
        
        # Try to access the HTTP client directly
        http_client = client._client
        print(f"HTTP client: {http_client}")
        
        # Try a simple health check
        print("\n--- Testing get_collections ---")
        collections = await client.get_collections()
        print(f"✅ Success! Collections: {[c.name for c in collections.collections]}")
        
        await client.close()
    except Exception as e:
        print(f"❌ Failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(debug_qdrant())
