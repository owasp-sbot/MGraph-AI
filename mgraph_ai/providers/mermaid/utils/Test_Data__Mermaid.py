from mgraph_ai.providers.mermaid.domain.Domain__Mermaid__Graph           import Domain__Mermaid__Graph
from osbot_utils.helpers.Safe_Id                                         import Safe_Id
from osbot_utils.helpers.Random_Guid                                     import Random_Guid
from mgraph_ai.providers.mermaid.schemas.Schema__Mermaid__Node           import Schema__Mermaid__Node
from mgraph_ai.providers.mermaid.schemas.Schema__Mermaid__Node__Data     import Schema__Mermaid__Node__Data
from mgraph_ai.providers.mermaid.models.Model__Mermaid__Graph            import Model__Mermaid__Graph
from mgraph_ai.providers.mermaid.schemas.Schema__Mermaid__Graph          import Schema__Mermaid__Graph
from mgraph_ai.providers.mermaid.schemas.Schema__Mermaid__Default__Types import Schema__Mermaid__Default__Types
from mgraph_ai.providers.mermaid.schemas.Schema__Mermaid__Graph__Config  import Schema__Mermaid__Graph__Config

# todo: refactor this out, and use Mermaid__Random_Graph instead
class Test_Data_Mermaid:
    @staticmethod
    def create_test_graph(num_nodes=3):
        default_types = Schema__Mermaid__Default__Types()
        graph_config  = Schema__Mermaid__Graph__Config(graph_id=Random_Guid())
        graph_data    = Schema__Mermaid__Graph        (default_types = default_types         ,
                                                       edges        = {}                     ,
                                                       nodes        = {}                     ,
                                                       graph_config = graph_config           ,
                                                       graph_type   = Schema__Mermaid__Graph ,
                                                       mermaid_code = []                     )
        graph_model  = Model__Mermaid__Graph          (data         = graph_data             )
        graph        = Domain__Mermaid__Graph                 (model        = graph_model)

        # Add test nodes
        node_keys = [Safe_Id(f'key_{i}') for i in range(num_nodes)]
        nodes     = []

        for key in node_keys:
            node_data = Schema__Mermaid__Node__Data()
            node      = Schema__Mermaid__Node      (node_data = node_data          ,
                                                    node_type   = Schema__Mermaid__Node,
                                                    key         = key                  ,
                                                    label       = f"Label {key}"       )
            nodes.append(graph_model.add_node(node))

        return {
                'graph'       : graph,
                'graph_model' : graph_model,
                'graph_data'  : graph_data,
                'graph_config': graph_config,
                'nodes'       : nodes,
                'node_keys'   : node_keys
        }

    @staticmethod
    def create_empty_graph():
        default_types = Schema__Mermaid__Default__Types()
        graph_config  = Schema__Mermaid__Graph__Config(graph_id=Random_Guid())
        graph_data    = Schema__Mermaid__Graph        (default_types = default_types       ,
                                                       edges        = {}                    ,
                                                       nodes        = {}                    ,
                                                       graph_config = graph_config          ,
                                                       graph_type   = Schema__Mermaid__Graph,
                                                       mermaid_code = []                    )
        graph_model = Model__Mermaid__Graph(data  = graph_data )
        graph       = Domain__Mermaid__Graph       (model = graph_model)

        return {'graph'       : graph        ,
                'graph_model' : graph_model  ,
                'graph_data'  : graph_data   ,
                'graph_config': graph_config }