from typing                                       import Type
from mgraph_ai.mgraph.domain.Domain__MGraph__Edge import Domain__MGraph__Edge
from mgraph_ai.mgraph.domain.Domain__MGraph__Node import Domain__MGraph__Node
from osbot_utils.type_safe.Type_Safe              import Type_Safe

class Domain__MGraph__Default__Types(Type_Safe):
    node_domain_type : Type[Domain__MGraph__Node]
    edge_domain_type : Type[Domain__MGraph__Edge]