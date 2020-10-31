
class TopologyManager:

    class TopologyGraph:
        def __init__(self, modules):
            tp_graph = self.init_topology_graph(modules)
            tp_graph = self.fill_topology_graph(tp_graph)
            tp_graph = self.trim_topology_graph(tp_graph)

            # Assign tp_graph as class variable for __str__
            self.topology_graph = tp_graph

        def __str__(self):
            # Print topology graph
            print(self.topology_graph)
            return ''

        @staticmethod
        def init_topology_graph(modules):
            radius = len(modules) - 1
            diameter = 2 * radius + 1
            topology_graph = [
                [None for _ in range(diameter)] for _ in range(diameter)
            ]
            network_module = modules[0]
            if network_module.type != 'network':
                raise ValueError('Cannot retrieve network module from modules')
            # Init topology graph with centering the network module as a root
            topology_graph[radius][radius] = network_module
            return topology_graph

        @staticmethod
        def fill_topology_graph(topology_graph):
            radius = len(topology_graph) // 2
            row, col = radius, radius
            network_module = topology_graph[row][col]

            # With DFS, visit all modules recursively and update the graph
            visited_modules = []
            modules_to_visit = [(network_module, row, col)]
            while modules_to_visit:
                module_to_visit, r, c = modules_to_visit.pop()
                if module_to_visit in visited_modules:
                    continue
                for direction, neighbor in module_to_visit.topology.items():
                    if not neighbor:
                        continue
                    next_r, next_c = \
                        TopologyManager.TopologyGraph.calc_next_coordinates(
                            r, c, direction
                        )
                    topology_graph[next_r][next_c] = neighbor
                    modules_to_visit.append((neighbor, next_r, next_c))
                visited_modules.append(module_to_visit)
            return topology_graph

        @staticmethod
        def trim_topology_graph(topology_graph):
            # Given rows, calculate x and width
            x, w = TopologyManager.TopologyGraph.calc_x_w(topology_graph)

            # Given cols, calculate y and height
            y, h = TopologyManager.TopologyGraph.calc_y_h(topology_graph)

            # Return the trimmed topology graph
            return TopologyManager.TopologyGraph.slice_topology_graph(
                topology_graph, x, w, y, h
            )

        #
        # Helper functions are defined below
        #
        @staticmethod
        def calc_next_coordinates(row, col, direction):
            x, y = {
                'r': (+0, +1),
                't': (-1, +0),
                'l': (+0, -1),
                'b': (+1, +0),
            }.get(direction)
            return row+x, col+y

        @staticmethod
        def calc_x_w(topology_graph):
            x = None
            for i, row in enumerate(topology_graph):
                if not x and any([module for module in row]):
                    x = i
                    break
            w = None
            for i, row in enumerate(topology_graph[::-1]):
                if not w and any([module for module in row]):
                    w = x - i
                    break
            return x, w

        @staticmethod
        def calc_y_h(topology_graph):
            topology_graph_transposed = zip(*topology_graph)

            y = None
            for j, col in enumerate(topology_graph_transposed):
                if not y and any([module for module in col]):
                    y = j
                    break
            h = None
            for j, col in enumerate(list(topology_graph_transposed)[::-1]):
                if not h and any([module for module in col]):
                    h = y - j
                    break
            return y, h

        @staticmethod
        def slice_topology_graph(topology_graph, x, w, y, h):
            return [row[y:y+h+1] for row in topology_graph[x:x+w+1]]

    def __init__(self, modules):
        self.modules = modules

    def construct_topology_graph(self):
        return self.TopologyGraph(self.modules)

    def print_topology_graph(self):
        topology_graph = self.construct_topology_graph()
        print(topology_graph)
