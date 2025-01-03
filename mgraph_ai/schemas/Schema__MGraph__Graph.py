from typing import Dict

from mgraph_ai.schemas.Schema__MGraph__Edge import Schema__MGraph__Edge
from mgraph_ai.schemas.Schema__MGraph__Node import Schema__MGraph__Node
from osbot_utils.type_safe.Type_Safe     import Type_Safe
from osbot_utils.helpers.Random_Guid        import Random_Guid


class Schema__MGraph__Graph(Type_Safe):
    edges     : Dict[Random_Guid, Schema__MGraph__Edge]
    graph_id  : Random_Guid
    graph_type: type
    nodes     : Dict[Random_Guid, Schema__MGraph__Node]