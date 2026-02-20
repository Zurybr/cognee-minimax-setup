#!/usr/bin/env python3
"""
Test script for Cognee + MiniMax + Qdrant + Memgraph setup
"""
import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

async def test_connection():
    print("🚀 Iniciando prueba de Cognee")
    print("=" * 50)
    
    # Display configuration
    print(f"📍 Qdrant: {os.getenv('VECTOR_DB_URL')}")
    print(f"📍 Memgraph: {os.getenv('GRAPH_DATABASE_URL')}")
    print(f"📍 LLM Provider: {os.getenv('LLM_PROVIDER')}")
    print(f"📍 LLM Model: {os.getenv('LLM_MODEL')}")
    print()
    
    # Import adapters
    import cognee_community_vector_adapter_qdrant.register
    from cognee_community_graph_adapter_memgraph import register as register_memgraph
    register_memgraph()
    
    print("✅ Adaptador Qdrant registrado")
    print("✅ Adaptador Memgraph registrado")
    print()
    
    # Import Cognee
    import cognee
    from cognee.api.v1.cognify import cognify
    from cognee.api.v1.search import search
    from cognee.api.v1.add import add
    
    print("🔧 Vector DB Provider:", os.getenv('VECTOR_DB_PROVIDER'))
    print("🔧 Graph DB Provider:", os.getenv('GRAPH_DATABASE_PROVIDER'))
    print()
    
    print("=" * 50)
    print("🧪 PROBANDO CONEXIONES")
    print("=" * 50)
    
    try:
        # Test 1: Add data
        print("\n1️⃣ Agregando datos de prueba...")
        await add("Cognee es un motor de conocimiento para agentes de IA. Conecta a Memgraph para grafos de conocimiento. Conecta a Qdrant para búsqueda vectorial.", "test_dataset")
        print("✅ Datos agregados correctamente")
        
        # Test 2: Cognify
        print("\n2️⃣ Creando knowledge graph (cognify)...")
        await cognify("test_dataset")
        print("✅ Knowledge graph creado")
        
        # Test 3: Search
        print("\n3️⃣ Buscando información...")
        results = await search("¿Qué es Cognee?", "test_dataset")
        print(f"✅ Búsqueda exitosa. Resultados: {len(results)}")
        for i, result in enumerate(results[:3], 1):
            print(f"   {i}. {result}")
        
        print("\n" + "=" * 50)
        print("🎉 TODAS LAS PRUEBAS PASARON")
        print("=" * 50)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_connection())
