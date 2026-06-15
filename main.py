from engine import Engine
from debug.vector_view import VectorView
from debug.matrix_view import MatrixView
from debug.cube_view import CubeView
from debug.em_view import EMView

# -----------------------------------------------
# Switch the scene here to change what you see:
#   VectorView()  — Vec3 operations visualised
#   MatrixView()  — Mat4 rotation visualised
#   CubeView()    — interactive wireframe cube
#   EMView()      — EM particle sandbox
# -----------------------------------------------

scene = EMView()

engine = Engine(scene=scene, antialiasing=True)
engine.start()