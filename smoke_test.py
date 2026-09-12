import sys
import os
sys.path.append(os.path.abspath("src"))
try:
    from ez_antigravity.entities import GravEntity
    from ez_antigravity.nbody_engine import NBodyEngine
    print("\n🦆 Initializing N-Body Engine demo... Quack!")
    engine = NBodyEngine()
    entity = GravEntity(name="Alpha", mass=100.0, position=(0.0, 0.0, 0.0), velocity=(0.0, 0.0, 0.0))
    engine.add_entity(entity)
    print(f"✅ Successfully added entity: {entity.name}")
except Exception as e:
    print(f"❌ Smoke Test Failed: {e}")
    sys.exit(1)