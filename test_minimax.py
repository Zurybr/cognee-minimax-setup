#!/usr/bin/env python3
"""Test MiniMax configuration with Cognee"""
import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv("/data/workspace/cognee-config/.env")

async def test_minimax():
    print("🧪 Probando configuración MiniMax")
    print("=" * 50)
    
    print(f"🔧 LLM Provider: {os.getenv('LLM_PROVIDER')}")
    print(f"🔧 LLM Model: {os.getenv('LLM_MODEL')}")
    print(f"🔧 LLM Endpoint: {os.getenv('LLM_ENDPOINT')}")
    print(f"🔧 API Key: {os.getenv('LLM_API_KEY')[:20]}..." if os.getenv('LLM_API_KEY') else "❌ No API key")
    print()
    
    # Test direct LLM call
    try:
        print("📝 Test 1: Llamada directa a MiniMax...")
        import httpx
        
        headers = {
            "Authorization": f"Bearer {os.getenv('LLM_API_KEY')}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": os.getenv('LLM_MODEL'),
            "messages": [{"role": "user", "content": "Hola, responde con una sola palabra: ¿funciona?"}],
            "max_tokens": 10
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{os.getenv('LLM_ENDPOINT')}/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=30.0
            )
            print(f"✅ Respuesta HTTP: {response.status_code}")
            print(f"📄 Respuesta: {response.text[:200]}")
    except Exception as e:
        print(f"❌ Error en llamada directa: {e}")
    
    print()
    print("🧠 Test 2: Probando Cognee con MiniMax...")
    
    try:
        # Import adapters
        import cognee_community_vector_adapter_qdrant
        import cognee_community_graph_adapter_memgraph
        
        cognee_community_vector_adapter_qdrant.register()
        cognee_community_graph_adapter_memgraph.register()
        
        import cognee
        from cognee.api.v1.cognify import cognify
        from cognee.api.v1.search import search
        from cognee.api.v1.add import add
        
        # Test add + cognify
        await add("MiniMax es un proveedor de LLM chino muy económico.", "test_minimax")
        await cognify("test_minimax")
        
        # Test search
        results = await search("¿Qué es MiniMax?", "test_minimax")
        
        print("✅ Cognee + MiniMax funcionando correctamente!")
        print(f"📊 Resultados de búsqueda: {len(results)}")
        for i, result in enumerate(results[:3], 1):
            print(f"   {i}. {result}")
            
    except Exception as e:
        print(f"❌ Error con Cognee: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_minimax())
