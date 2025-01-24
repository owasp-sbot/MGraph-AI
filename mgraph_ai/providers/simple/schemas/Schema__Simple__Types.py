from typing                                                        import Type
from mgraph_ai.mgraph.schemas.Schema__MGraph__Edge                 import Schema__MGraph__Edge
from mgraph_ai.mgraph.schemas.Schema__MGraph__Edge__Config         import Schema__MGraph__Edge__Config
from mgraph_ai.mgraph.schemas.Schema__MGraph__Graph__Data          import Schema__MGraph__Graph__Data
from mgraph_ai.mgraph.schemas.Schema__MGraph__Types                import Schema__MGraph__Types
from mgraph_ai.providers.simple.schemas.Schema__Simple__Node       import Schema__Simple__Node
from mgraph_ai.providers.simple.schemas.Schema__Simple__Node__Data import Schema__Simple__Node__Data


class Schema__Simple__Types(Schema__MGraph__Types):
    node_type        : Type[Schema__Simple__Node        ]           # only change from Schema__MGraph__Types
    node_data_type   : Type[Schema__Simple__Node__Data  ]
    edge_type        : Type[Schema__MGraph__Edge        ]
    edge_config_type : Type[Schema__MGraph__Edge__Config]
    graph_data_type  : Type[Schema__MGraph__Graph__Data ]