from ..models.grid import Grid
from ..models.frontier import StackFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node


class DepthFirstSearch:
    @staticmethod
    def search(grid: Grid) -> Solution:
        """Find path between two points in a grid using Depth First Search

        Args:
            grid (Grid): Grid of points

        Returns:
            Solution: Solution found
        """
        
        # Initialize root node
        root = Node("", state=grid.initial, cost=0, parent=None, action=None)

        # Initialize expanded with the empty dictionary
        expanded = dict()

        # El nodo raíz, ¿tiene estado objetivo?
        if grid.objective_test(root.state):
            return Solution(root, expanded)

        # Initialize frontier with the root node
        frontier = StackFrontier()
        frontier.add(root)

        # Bucle principal:
        while True:

            # Si la frontera queda vacía, no hay solución:
            if frontier.is_empty():
                return NoSolution(expanded)
            
            # Tomamos el último nodo agregado:
            node = frontier.remove()

            # Evaluar si el estado se encuentra en expandidos:
            if node.state in expanded:
                continue

            # Agrego el resultado a expandidos:
            expanded[node.state] = True

            for action in grid.actions(node.state):

                # Resultado que da aplicar cada acción al nodo:
                result = grid.result(node.state, action)

	            # Si este resultado NO está en expandidos (es decir, debemos explorarlo):
                if result not in expanded:

               	    # Creo un nuevo nodo (hijo) con el resultado:
                    new_node = Node('', result, node.cost + grid.individual_cost(node.state, action), node,action) 

		            # Verifico si este nuevo nodo hijo llegó al objetivo:
                    if grid.objective_test(new_node.state):
                        return Solution(new_node, expanded)
                
                    # En caso de que no lo sea, lo agrego a la frontera:
                    frontier.add(new_node)

        return NoSolution(expanded)