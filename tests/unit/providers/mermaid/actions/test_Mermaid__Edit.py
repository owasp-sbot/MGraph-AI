from unittest                                                           import TestCase
from mgraph_ai.providers.mermaid.domain.Mermaid__Edge                   import Mermaid__Edge
from mgraph_ai.providers.mermaid.schemas.Schema__Mermaid__Diagram__Type import Schema__Mermaid__Diagram__Type
from mgraph_ai.providers.mermaid.schemas.Schema__Mermaid__Node__Config  import Schema__Mermaid__Node__Config
from osbot_utils.helpers.Safe_Id                                        import Safe_Id
from osbot_utils.utils.Objects                                          import __, obj
from mgraph_ai.providers.mermaid.domain.Mermaid__Node                   import Mermaid__Node
from osbot_utils.utils.Misc                                             import is_guid
from mgraph_ai.mgraph.actions.MGraph__Edit                              import MGraph__Edit
from mgraph_ai.providers.mermaid.actions.Mermaid__Edit                  import Mermaid__Edit
from mgraph_ai.providers.mermaid.domain.Mermaid__Graph                  import Mermaid__Graph


class test__Mermaid__Edit(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.mermaid__edit = Mermaid__Edit()

    def test__init__(self):
        with self.mermaid__edit as _:
            assert type(_)                      is Mermaid__Edit
            assert isinstance(_, MGraph__Edit)  is True
            assert type(_.graph)                is Mermaid__Graph

    def test_add_directive(self):
        with self.mermaid__edit as _:
            _.set_diagram_type(Schema__Mermaid__Diagram__Type.flowchart)
            _.add_directive   ('init: {"flowchart": {"htmlLabels": false}} ')
            _.add_node        (key='markdown', label='This **is** _Markdown_').markdown()

            assert _.code() ==  ('%%{init: {"flowchart": {"htmlLabels": false}} }%%\n'
                                 'flowchart LR\n'
                                 '    markdown["`This **is** _Markdown_`"]\n')

    def test_add_edge(self):
        with self.mermaid__edit as _:
            from_node_key    = 'from_key'
            to_node_key      =  'to_key'
            edge             = _.add_edge(from_node_key=from_node_key, to_node_key=to_node_key, label='an_label', attributes={'answer': '42'})
            edge_id          =  edge.edge_id()
            edge_attributes  = edge.attributes()
            attribute_id     = edge_attributes[0].attribute.data.attribute_id
            nodes__by_key    = _.data().nodes__by_key()
            from_node        = nodes__by_key.get(from_node_key)
            to_node          = nodes__by_key.get(to_node_key  )

            assert is_guid(edge_id     ) is True
            assert is_guid(attribute_id) is True
            assert type(from_node)       == Mermaid__Node
            assert type(from_node)       == Mermaid__Node
            assert type(edge     )       == Mermaid__Edge

            assert from_node.node_key() == from_node_key
            assert to_node  .node_key() == to_node_key
            assert edge_attributes[0].attribute.obj() == __(data=__(attribute_id    = attribute_id,
                                                                    attribute_name  = 'answer',
                                                                    attribute_value = '42',
                                                                    attribute_type  = 'builtins.str'))
            from osbot_utils.utils.Dev import pprint
            attributes = obj({attribute_id: edge_attributes[0].attribute.data.json()})
            assert edge.edge.obj() == __(data         =__(label        = '',
                                                          edge_config  = __(from_node_type = 'mgraph_ai.providers.mermaid.schemas.Schema__Mermaid__Node.Schema__Mermaid__Node',
                                                                            to_node_type   = 'mgraph_ai.providers.mermaid.schemas.Schema__Mermaid__Node.Schema__Mermaid__Node',
                                                                            edge_id        = edge_id                                                                          ),
                                                          edge_type    = 'mgraph_ai.providers.mermaid.schemas.Schema__Mermaid__Edge.Schema__Mermaid__Edge',
                                                          attributes   = attributes                                     ,
                                                          from_node_id = from_node.node_id()                            ,
                                                          to_node_id   = to_node.node_id()                             ))

    def test_add_node(self):
        with self.mermaid__edit as _:
            node        = _.add_node()
            node_id     = node.node_id()
            node_key    = node.node_key()
            node_config = node.node_config()
            assert is_guid(node_id)  is True
            assert type(node)        is Mermaid__Node
            assert type(node_key)    is Safe_Id
            assert type(node_config) is Schema__Mermaid__Node__Config
            assert node.obj()        == __(node=__(data=__(key         = node_key            ,
                                                           label       = node_key    ,
                                                           node_config =__(node_shape      = 'default',
                                                                          show_label       = True,
                                                                          wrap_with_quotes = True,
                                                                          markdown         = False,
                                                                          value_type       = None,
                                                                          node_id          = node_id),
                                                           node_type   = 'mgraph_ai.providers.mermaid.schemas.Schema__Mermaid__Node.Schema__Mermaid__Node',
                                                           attributes  =__() ,
                                                           value       =None )),
                                           graph = _.graph.model.obj())

        node_2 = _.add_node(key='an-key', value='an-value', label = 'an-label')
        assert node_2.node.data.obj() == __(key         = 'an-key'                   ,
                                            label       = 'an-label'                 ,
                                            node_config = node_2.node_config().obj() ,
                                            node_type   = 'mgraph_ai.providers.mermaid.schemas.Schema__Mermaid__Node.Schema__Mermaid__Node',
                                            attributes  = __()                       ,
                                            value       = 'an-value'                 )