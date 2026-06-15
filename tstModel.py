
from model.model import Model

myModel = Model()
myModel.buildGraph(5)
nNodes , sEdges = myModel.getGraphDetailes()
print(f"num nodi: {nNodes} , num archi: {sEdges}")
