#!/usr/bin/env python3
"""Test MiniMax API endpoint"""
import asyncio
import os
from dotenv import load_dotenv

load_dotenv("/data/workspace/cognee-config/.env")

async def test_endpoints():
    import httpx
    
    api_key = os.getenv('LLM_API_KEY')
    model = os.getenv('LLM_MODEL')
    
    endpoints = [
        "https://api.minimax.io/v1/chat/completions",
        "https://api.minimax.io/anthropic/v1/chat/completions",
        "https://api.minimax.io/anthropic/v1/messages",
        "https://api.minimax.io/v1/messages",
    ]
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": "Hola"}],
        "max_tokens": 10
    }
    
    print("🔍 Probando endpoints de MiniMax...")
    print("=" * 60)
    
    for endpoint in endpoints:
        try:
            print(f"\n📝 Probando: {endpoint}")
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    endpoint,
                    headers=headers,
                    json=payload,
                    timeout=30.0
                )
                print(f"   Status: {response.status_code}")
                print(f"   Respuesta: {response.text[:150]}")
                if response.status_code == 200:
                    print(f"   ✅ ¡Endpoint válido!")
        except Exception as e:
            print(f"   ❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_endpoints())
