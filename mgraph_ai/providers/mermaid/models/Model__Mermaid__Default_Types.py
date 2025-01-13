from typing                                                  import Type
from mgraph_ai.mgraph.models.Model__MGraph__Default__Types   import Model__MGraph__Default__Types
from mgraph_ai.providers.mermaid.models.Model__Mermaid__Edge import Model__Mermaid__Edge
from mgraph_ai.providers.mermaid.models.Model__Mermaid__Node import Model__Mermaid__Node


class Model__Mermaid__Default_Types(Model__MGraph__Default__Types):
    node_model_type: Type[Model__Mermaid__Node]
    edge_model_type: Type[Model__Mermaid__Edge]