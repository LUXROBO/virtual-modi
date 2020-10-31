
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
            pass

        @staticmethod
        def init_topology_graph(modules):
            topology_graph = [
                [modules[0] for _ in range(2 * len(modules))]
                for _ in range(2 * len(modules))
            ]
            return topology_graph

        @staticmethod
        def fill_topology_graph(topology_graph):
            # Start from network module, iterate recursively in DFS manner
            return topology_graph

        @staticmethod
        def trim_topology_graph(topology_graph):
            return topology_graph

        #
        # Helper functions are defined below
        #
        def f(self):
            pass

    def __init__(self, modules):
        self.modules = modules

    def construct_topology_graph(self):
        return self.TopologyGraph(self.modules)

    def print_topology_graph(self):
        topology_graph = self.construct_topology_graph()
        print(topology_graph)
