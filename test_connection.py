#!/usr/bin/env python3
"""
Script de prueba para Cognee con Qdrant + Memgraph
Configuración para Brandom - e6labs
"""

import os
import asyncio
import sys

# Cargar variables de entorno PRIMERO
from dotenv import load_dotenv
load_dotenv('/data/workspace/cognee-config/.env')

# Verificar que las variables están cargadas
print("🚀 Iniciando prueba de Cognee")
print(f"📍 Qdrant: {os.getenv('VECTOR_DB_URL')}")
print(f"📍 Memgraph: {os.getenv('GRAPH_DATABASE_URL')}")
print(f"📍 LLM Provider: {os.getenv('LLM_PROVIDER')}")

# Importar cognee primero (para que sus infraestructuras estén disponibles)
import cognee
from cognee import config

# ============================================
# REGISTRAR ADAPTADORES (después de cognee)
# ============================================

# Registrar Qdrant
try:
    import cognee_community_vector_adapter_qdrant.register
    print("✅ Adaptador Qdrant registrado")
except Exception as e:
    print(f"❌ Error registrando Qdrant: {e}")
    import traceback
    traceback.print_exc()

# Registrar Memgraph
try:
    from cognee_community_graph_adapter_memgraph import register as register_memgraph
    register_memgraph()
    print("✅ Adaptador Memgraph registrado")
except Exception as e:
    print(f"❌ Error registrando Memgraph: {e}")
    import traceback
    traceback.print_exc()

print(f"\n🔧 Vector DB Provider: {os.getenv('VECTOR_DB_PROVIDER')}")
print(f"🔧 Graph DB Provider: {os.getenv('GRAPH_DATABASE_PROVIDER')}")

async def test_connection():
    """Probar conexión a Qdrant y Memgraph"""
    
    print("\n" + "="*50)
    print("🧪 PROBANDO CONEXIONES")
    print("="*50)
    
    # Test 1: Agregar datos
    print("\n1️⃣ Agregando datos de prueba...")
    try:
        await cognee.add("Cognee es un motor de conocimiento para agentes de IA.")
        await cognee.add("Conecta a Qdrant para búsqueda vectorial.")
        await cognee.add("Conecta a Memgraph para grafos de conocimiento.")
        print("✅ Datos agregados correctamente")
    except Exception as e:
        print(f"❌ Error agregando datos: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Test 2: Cognify (crear grafo)
    print("\n2️⃣ Creando knowledge graph (cognify)...")
    try:
        await cognee.cognify()
        print("✅ Knowledge graph creado")
    except Exception as e:
        print(f"❌ Error en cognify: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Test 3: Buscar
    print("\n3️⃣ Buscando información...")
    try:
        results = await cognee.search("¿Qué es Cognee?")
        print(f"✅ Búsqueda exitosa. Resultados: {len(results)}")
        for i, result in enumerate(results, 1):
            print(f"   {i}. {result}")
    except Exception as e:
        print(f"❌ Error en búsqueda: {e}")
        import traceback
        traceback.print_exc()
        return
    
    print("\n" + "="*50)
    print("🎉 TODAS LAS PRUEBAS PASARON")
    print("="*50)

if __name__ == "__main__":
    asyncio.run(test_connection())
