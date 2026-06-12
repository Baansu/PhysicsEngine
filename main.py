from engine import Engine
from debug.vector_view import VectorView
from debug.matrix_view import MatrixView
from debug.cube_view import CubeView

# -----------------------------------------------
# Switch the scene here to change what you see:
#   VectorView()  — Vec3 operations visualised
#   MatrixView()  — Mat4 rotation visualised
#   CubeView()    — wireframe cube, full 3D pipeline
# -----------------------------------------------

scene = CubeView()

engine = Engine(scene=scene, antialiasing=False)
engine.start()