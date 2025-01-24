from typing                                               import Type, Set, Any
from mgraph_ai.mgraph.domain.Domain__MGraph__Graph        import Domain__MGraph__Graph
from mgraph_ai.mgraph.schemas.Schema__MGraph__Node        import Schema__MGraph__Node
from mgraph_ai.mgraph.schemas.Schema__MGraph__Edge        import Schema__MGraph__Edge
from mgraph_ai.mgraph.schemas.Schema__MGraph__Index__Data import Schema__MGraph__Index__Data
from osbot_utils.helpers.Obj_Id                           import Obj_Id
from osbot_utils.type_safe.Type_Safe                      import Type_Safe
from osbot_utils.utils.Json                               import json_file_create, json_load_file

# note we don't have a top level Domain__MGraph__Graph because that is
#       a) not needed
#       b) would add complexity to this class
#       c) could imply that the index was up-to-date with the graph
#          todo: look into the detection and handling of the scenario where the a graph is not in sync from a loaded graph

class MGraph__Index(Type_Safe):
    index_data : Schema__MGraph__Index__Data

    def add_node(self, node: Schema__MGraph__Node) -> None:                         # Add a node to the index
        node_id   = node.node_id
        node_type = node.node_type.__name__

        if node_id not in self.index_data.nodes_to_outgoing_edges:                  # Initialize sets if needed
            self.index_data.nodes_to_outgoing_edges[node_id] = set()
        if node_id not in self.index_data.nodes_to_incoming_edges:
            self.index_data.nodes_to_incoming_edges[node_id] = set()


        if node_type not in self.index_data.nodes_by_type:                          # Add to type index
            self.index_data.nodes_by_type[node_type] = set()
        self.index_data.nodes_by_type[node_type].add(node_id)

        self.index_node_data(node)                                            # Index attributes

    def add_edge(self, edge: Schema__MGraph__Edge) -> None:                     # Add an edge to the index
        edge_id      = edge.edge_config.edge_id
        from_node_id = edge.from_node_id
        to_node_id   = edge.to_node_id
        edge_type    = edge.edge_type.__name__


        self.index_data.nodes_to_outgoing_edges[from_node_id].add(edge_id)      # Add to node relationship indexes
        self.index_data.nodes_to_incoming_edges[to_node_id].add(edge_id)
        self.index_data.edge_to_nodes[edge_id] = (from_node_id, to_node_id)


        if edge_type not in self.index_data.edges_by_type:                      # Add to type index
            self.index_data.edges_by_type[edge_type] = set()
        self.index_data.edges_by_type[edge_type].add(edge_id)

        self.index_edge_data(edge)                                        # Index edge attributes

    def remove_node(self, node: Schema__MGraph__Node) -> None:  # Remove a node and all its references from the index"""
        node_id = node.node_id

        # Get associated edges before removing node references
        outgoing_edges = self.index_data.nodes_to_outgoing_edges.pop(node_id, set())
        incoming_edges = self.index_data.nodes_to_incoming_edges.pop(node_id, set())

        # Remove from type index
        node_type = node.node_type.__name__
        if node_type in self.index_data.nodes_by_type:
            self.index_data.nodes_by_type[node_type].discard(node_id)
            if not self.index_data.nodes_by_type[node_type]:
                del self.index_data.nodes_by_type[node_type]

        self.remove_node_data(node)                                   # Remove from attribute indexes

    def remove_edge(self, edge: Schema__MGraph__Edge) -> None:          # Remove an edge and all its references from the index
        edge_id = edge.edge_config.edge_id

        if edge_id in self.index_data.edge_to_nodes:
            from_node_id, to_node_id = self.index_data.edge_to_nodes.pop(edge_id)
            self.index_data.nodes_to_outgoing_edges[from_node_id].discard(edge_id)
            self.index_data.nodes_to_incoming_edges[to_node_id].discard(edge_id)

        # Remove from type index
        edge_type = edge.edge_type.__name__
        if edge_type in self.index_data.edges_by_type:
            self.index_data.edges_by_type[edge_type].discard(edge_id)
            if not self.index_data.edges_by_type[edge_type]:
                del self.index_data.edges_by_type[edge_type]

        self.remove_edge_data(edge)

    def index_node_data(self, node: Schema__MGraph__Node) -> None:
        """Index all fields from node_data"""
        if node.node_data:
            for field_name, field_value in node.node_data.__dict__.items():
                if field_name.startswith('_'):
                    continue
                if field_name not in self.index_data.nodes_by_field:
                    self.index_data.nodes_by_field[field_name] = {}
                if field_value not in self.index_data.nodes_by_field[field_name]:
                    self.index_data.nodes_by_field[field_name][field_value] = set()
                self.index_data.nodes_by_field[field_name][field_value].add(node.node_id)

    def remove_node_data(self, node: Schema__MGraph__Node) -> None:
        """Remove indexed node_data fields"""
        if node.node_data:
            for field_name, field_value in node.node_data.__dict__.items():
                if field_name.startswith('_'):
                    continue
                if field_name in self.index_data.nodes_by_field:
                    if field_value in self.index_data.nodes_by_field[field_name]:
                        self.index_data.nodes_by_field[field_name][field_value].discard(node.node_id)

    def index_edge_data(self, edge: Schema__MGraph__Edge) -> None:
        """Index all fields from edge_data"""
        if edge.edge_data:
            for field_name, field_value in edge.edge_data.__dict__.items():
                if field_name.startswith('_'):
                    continue
                if field_name not in self.index_data.edges_by_field:
                    self.index_data.edges_by_field[field_name] = {}
                if field_value not in self.index_data.edges_by_field[field_name]:
                    self.index_data.edges_by_field[field_name][field_value] = set()
                self.index_data.edges_by_field[field_name][field_value].add(edge.edge_config.edge_id)

    def remove_edge_data(self, edge: Schema__MGraph__Edge) -> None:
        """Remove indexed edge_data fields"""
        if edge.edge_data:
            for field_name, field_value in edge.edge_data.__dict__.items():
                if field_name.startswith('_'):
                    continue
                if field_name in self.index_data.edges_by_field:
                    if field_value in self.index_data.edges_by_field[field_name]:
                        self.index_data.edges_by_field[field_name][field_value].discard(edge.edge_config.edge_id)

    def load_index_from_graph(self, graph : Domain__MGraph__Graph) -> None:                                             # Create index from existing graph
        for node_id, node in graph.model.data.nodes.items():                                                            # Add all nodes to index
            self.add_node(node)

        for edge_id, edge in graph.model.data.edges.items():                                           # Add all edges to index
            self.add_edge(edge)


    def save_to_file(self, target_file: str) -> None:                                               # Save index to file
        index_data = self.index_data.json()                                                              # get json (serialised) representation of the index object
        return json_file_create(index_data, target_file)                                            # save it to the target file

    @classmethod
    def from_graph(cls, graph: Domain__MGraph__Graph) -> 'MGraph__Index':                           # Create index from graph
        with cls() as _:
            _.load_index_from_graph(graph)                                                             # Build initial index
            return _

    @classmethod
    def from_file(cls, source_file: str) -> 'MGraph__Index':                                           # Load index from file
        with cls() as _:
            index_data   = json_load_file(source_file)
            _.index_data = Schema__MGraph__Index__Data.from_json(index_data)
            return _


    def get_node_outgoing_edges(self, node: Schema__MGraph__Node) -> Set[Obj_Id]:           # Get all outgoing edges for a node
        return self.index_data.nodes_to_outgoing_edges.get(node.node_id, set())

    def get_node_incoming_edges(self, node: Schema__MGraph__Node) -> Set[Obj_Id]:           # Get all incoming edges for a node
        return self.index_data.nodes_to_incoming_edges.get(node.node_id, set())

    def get_nodes_by_type(self, node_type: Type[Schema__MGraph__Node]) -> Set[Obj_Id]:      # Get all nodes of a specific type
        return self.index_data.nodes_by_type.get(node_type.__name__, set())

    def get_edges_by_type(self, edge_type: Type[Schema__MGraph__Edge]) -> Set[Obj_Id]:      # Get all edges of a specific type
        return self.index_data.edges_by_type.get(edge_type.__name__, set())

    def get_nodes_by_field(self, field_name: str, field_value: Any) -> Set[Obj_Id]:         # Get all nodes with a specific field value
        return self.index_data.nodes_by_field.get(field_name, {}).get(field_value, set())

    def get_edges_by_field(self, field_name: str, field_value: Any) -> Set[Obj_Id]:         # Get all edges with a specific field value
        return self.index_data.edges_by_field.get(field_name, {}).get(field_value, set())


    def edge_to_nodes           (self): return self.index_data.edge_to_nodes
    def edges_by_field          (self): return self.index_data.edges_by_field
    def edges_by_type           (self): return self.index_data.edges_by_type
    def nodes_by_field          (self): return self.index_data.nodes_by_field
    def nodes_by_type           (self): return self.index_data.nodes_by_type
    def nodes_to_incoming_edges (self): return self.index_data.nodes_to_incoming_edges
    def nodes_to_outgoing_edges (self): return self.index_data.nodes_to_outgoing_edges