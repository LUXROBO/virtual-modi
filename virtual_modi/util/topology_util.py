
class TopologyManager:

    class TopologyGraph:
        def __init__(self, modules):
            tp_graph = self.init_topology_graph(modules)
            tp_graph = self.fill_topology_graph(tp_graph)
            tp_graph = self.trim_topology_graph(tp_graph)

            # Assign tp_graph as class variable for __str__
            self.topology_graph = tp_graph

        def __str__(self):
            # Init the minimum value required to represent longest module name
            pad_val = 25

            # Construct printable_topology_graph
            printable_topology_graph = self.topology_graph
            for i in range(len(printable_topology_graph)):
                for j in range(len(printable_topology_graph[0])):
                    curr_module = printable_topology_graph[i][j]
                    printable_name = (
                        f'{curr_module.__str__():^{pad_val}}' if curr_module
                        else ' '*pad_val
                    )
                    printable_topology_graph[i][j] = printable_name

            # Format the constructed topology graph above
            width = len(printable_topology_graph[0]) * pad_val
            title = '[Virtual MODI Topology Graph]'
            if width < len(title):
                title = title.replace('Virtual', 'Vir')
            lines_to_print = []
            title_line = f'{title:^{width}}'
            border_line = '=' * width
            lines_to_print.append(title_line)
            lines_to_print.append(border_line)
            for row in printable_topology_graph:
                curr_module_line = ''.join(row)
                lines_to_print.append(curr_module_line)

            # Return the formatted printable topology graph
            return '\n'.join(lines_to_print)

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
            # Given rows, calculate x and vertical length
            x, v = TopologyManager.TopologyGraph.calc_x_v(topology_graph)

            # Given cols, calculate y and horizontal length
            y, h = TopologyManager.TopologyGraph.calc_y_h(topology_graph)

            print(x, v, y, h)
            # Return the trimmed topology graph
            return TopologyManager.TopologyGraph.slice_topology_graph(
                topology_graph, x, v, y, h
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
        def calc_x_v(topology_graph):
            x, v = None, None
            for i, row in enumerate(topology_graph):
                if not x and any([module for module in row]):
                    x = i
                    continue
                if x and all([not module for module in row]):
                    v = i-x
                    break
            return x, v

        @staticmethod
        def calc_y_h(topology_graph):
            topology_graph_transposed = zip(*topology_graph)

            y, h = None, None
            for j, col in enumerate(topology_graph_transposed):
                if not y and any([module for module in col]):
                    y = j
                    continue
                if y and all([not module for module in col]):
                    h = j-y
                    break
            return y, h

        @staticmethod
        def slice_topology_graph(topology_graph, x, v, y, h):
            return [row[y:y+h] for row in topology_graph[x:x+v]]

    def __init__(self, modules):
        self.modules = modules

    def construct_topology_graph(self):
        return self.TopologyGraph(self.modules)

    def print_topology_graph(self):
        topology_graph = self.construct_topology_graph()
        print(topology_graph)
