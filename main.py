from engine import Engine
from debug.vector_view import VectorView
from debug.matrix_view import MatrixView

# -----------------------------------------------
# Switch the scene here to change what you see:
#   VectorView()  — Vec3 operations visualised
#   MatrixView()  — Mat4 rotation visualised
# -----------------------------------------------

scene = MatrixView()

engine = Engine(scene=scene, antialiasing=True)
engine.start()