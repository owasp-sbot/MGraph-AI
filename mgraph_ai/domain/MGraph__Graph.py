from mgraph_ai.domain.MGraph__Edge import MGraph__Edge
from mgraph_ai.domain.MGraph__Node import MGraph__Node
from mgraph_ai.models.Model__MGraph__Graph  import Model__MGraph__Graph
from mgraph_ai.schemas.Schema__MGraph__Node import Schema__MGraph__Node
from osbot_utils.type_safe.Type_Safe        import Type_Safe


class MGraph__Graph(Type_Safe):
    graph: Model__MGraph__Graph

    def add_node(self, **kwargs):
        node = self.model.add_node(**kwargs)
        return MGraph__Node(node=node, graph=self)

    def node(self, node_id):
        node_model = self.nodes().get(node_id)
        return MGraph__Node(node=node_model, graph=self)

    def nodes(self):
        return [self.node(node_id) for node_id in self.model.nodes.keys()]

    def edge(self, edge_id):
        edge_model = self.graph.nodes().get(edge_id)
        return MGraph__Edge(edge=edge_model, graph=self)

    def edges(self):
        return [self.edge(edge_id) for edge_id in self.model.edges.keys()]

    def new_node(self):
        node =  Schema__MGraph__Node
        return self.add_node(node=node)