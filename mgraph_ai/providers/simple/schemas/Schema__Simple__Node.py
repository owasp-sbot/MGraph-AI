from mgraph_ai.mgraph.schemas.Schema__MGraph__Node                 import Schema__MGraph__Node
from mgraph_ai.providers.simple.schemas.Schema__Simple__Node__Data import Schema__Simple__Node__Data


class Schema__Simple__Node(Schema__MGraph__Node):
    node_data: Schema__Simple__Node__Data