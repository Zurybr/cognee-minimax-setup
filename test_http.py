#!/usr/bin/env python3
"""Test basic HTTP connection to Qdrant"""
import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv("/data/workspace/cognee-config/.env")

async def test_http():
    import httpx
    
    url = os.getenv("VECTOR_DB_URL")
    api_key = os.getenv("VECTOR_DB_KEY")
    
    print(f"🔗 Testing HTTP connection to: {url}/collections")
    print(f"🔑 API Key: {api_key[:10]}...{api_key[-5:] if api_key else 'None'}")
    
    headers = {"api-key": api_key} if api_key else {}
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(f"{url}/collections", headers=headers)
            print(f"✅ HTTP Success!")
            print(f"📊 Status: {response.status_code}")
            print(f"📄 Response: {response.text[:200]}")
    except Exception as e:
        print(f"❌ HTTP failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_http())
