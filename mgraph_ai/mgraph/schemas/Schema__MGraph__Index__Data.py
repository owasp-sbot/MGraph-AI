from typing                          import Dict, Set, Any, Optional
from osbot_utils.helpers.Obj_Id      import Obj_Id
from osbot_utils.type_safe.Type_Safe import Type_Safe

class Schema__MGraph__Index__Data(Type_Safe):
    nodes_to_outgoing_edges: Dict[Obj_Id, set  [Obj_Id         ]]  # node_id -> set of outgoing edge_ids
    nodes_to_incoming_edges: Dict[Obj_Id, set  [Obj_Id         ]]  # node_id -> set of incoming edge_ids
    edge_to_nodes          : Dict[Obj_Id, tuple[Obj_Id, Obj_Id ]]  # edge_id -> (from_node_id, to_node_id)
    nodes_by_type          : Dict[str   , set  [Obj_Id         ]]  # node_type -> set of node_ids
    edges_by_type          : Dict[str   , set  [Obj_Id         ]]  # edge_type -> set of edge_ids
    nodes_by_field         : Dict[str   , Dict[Any, set[Obj_Id]]]  # field_name -> {value -> set of node_ids}
    edges_by_field         : Dict[str   , Dict[Any, set[Obj_Id]]]  # field_name -> {value -> set of edge_ids}