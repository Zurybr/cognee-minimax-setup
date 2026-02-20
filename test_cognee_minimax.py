#!/usr/bin/env python3
"""Test Cognee with MiniMax"""
import asyncio
import os
from dotenv import load_dotenv

load_dotenv("/data/workspace/cognee-config/.env")

async def test_cognee_minimax():
    print("🧪 Probando Cognee + MiniMax")
    print("=" * 50)
    print(f"🔧 LLM Provider: {os.getenv('LLM_PROVIDER')}")
    print(f"🔧 LLM Model: {os.getenv('LLM_MODEL')}")
    print(f"🔧 LLM Endpoint: {os.getenv('LLM_ENDPOINT')}")
    print()
    
    try:
        # Import adapters
        import cognee_community_vector_adapter_qdrant.register
        from cognee_community_graph_adapter_memgraph import register as register_memgraph
        register_memgraph()
        
        import cognee
        from cognee.api.v1.cognify import cognify
        from cognee.api.v1.search import search
        from cognee.api.v1.add import add
        
        # Clean previous test data
        print("🧹 Limpiando datos anteriores...")
        await cognee.prune.prune_data()
        
        # Test add
        print("📝 Agregando documento de prueba...")
        await add("MiniMax es un proveedor de modelos de lenguaje de China. Es muy económico comparado con OpenAI.", "test_minimax")
        
        # Test cognify
        print("🧠 Creando knowledge graph...")
        await cognify("test_minimax")
        
        # Test search
        print("🔍 Buscando información...")
        results = await search("¿Qué es MiniMax?", "test_minimax")
        
        print("\n✅ ¡Cognee + MiniMax funcionando correctamente!")
        print(f"📊 Resultados: {len(results)}")
        for i, result in enumerate(results[:3], 1):
            print(f"   {i}. {result}")
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_cognee_minimax())
