from typing                                                 import Type, List
from mgraph_ai.mgraph.domain.Domain__MGraph__Default__Types import Domain__MGraph__Default__Types
from mgraph_ai.mgraph.models.Model__MGraph__Edge            import Model__MGraph__Edge
from mgraph_ai.mgraph.models.Model__MGraph__Node            import Model__MGraph__Node
from osbot_utils.helpers.Random_Guid                        import Random_Guid
from mgraph_ai.mgraph.domain.Domain__MGraph__Edge           import Domain__MGraph__Edge
from mgraph_ai.mgraph.domain.Domain__MGraph__Node           import Domain__MGraph__Node
from mgraph_ai.mgraph.models.Model__MGraph__Graph           import Model__MGraph__Graph
from osbot_utils.type_safe.Type_Safe                        import Type_Safe


class Domain__MGraph__Graph(Type_Safe):
    default_types : Domain__MGraph__Default__Types
    model         : Model__MGraph__Graph


    def delete_edge(self, edge_id: Random_Guid) -> bool:
        return self.model.delete_edge(edge_id)

    def delete_node(self, node_id: Random_Guid) -> bool:
        return self.model.delete_node(node_id)

    def edge(self, edge_id: Random_Guid) -> Domain__MGraph__Edge:
        edge = self.model.edge(edge_id)
        if edge:
            return self.mgraph_edge(edge=edge)

    def edges(self) -> List[Domain__MGraph__Edge]:
        return [self.mgraph_edge(edge=edge) for edge in self.model.edges()]

    def graph_id(self):
        return self.model.data.graph_config.graph_id

    def mgraph_edge(self, edge: Model__MGraph__Edge) -> Domain__MGraph__Edge:
        return self.default_types.edge_domain_type(edge=edge, graph=self.model)

    def mgraph_node(self, node: Model__MGraph__Node) -> Domain__MGraph__Edge:
        return self.default_types.node_domain_type(node=node, graph=self.model)

    def new_edge(self, **kwargs) -> Domain__MGraph__Edge:
        edge = self.model.new_edge(**kwargs)
        return self.mgraph_edge(edge=edge)

    def new_node(self, **kwargs)-> Domain__MGraph__Node:
        node = self.model.new_node(**kwargs)
        return self.mgraph_node(node=node)

    def node(self, node_id: Random_Guid) -> Domain__MGraph__Node:
        node = self.model.node(node_id)
        if node:
            return self.mgraph_node(node=node)

    def nodes(self) -> List[Domain__MGraph__Node]:
        return [self.mgraph_node(node=node) for node in self.model.nodes()]
