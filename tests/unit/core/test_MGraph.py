from unittest                           import TestCase
from osbot_utils.utils.Objects          import __
from osbot_utils.testing.Stdout         import Stdout
from osbot_utils.utils.Misc             import random_text
from mgraph_ai.core.MGraph              import MGraph


class test_MGraph(TestCase):

    def setUp(self):
        self.mgraph = MGraph()

    def test___init__(self):
        expected_args = ['config', 'edges', 'key', 'nodes']
        with self.mgraph as _:
            assert _.__attr_names__() == expected_args
            assert _.edges            == []
            assert _.nodes            == []
            assert _.key.startswith('mgraph_')

    def test_add_node(self):
        key   = random_text()
        label = random_text()
        with self.mgraph as _:
            new_node = _.add_node(key=key, label=label)
            assert _.nodes               == [new_node]
            assert new_node.label        == label

            assert new_node.obj()        == __(node_id    = new_node.node_id,
                                               attributes = __()            ,
                                               key        = key             ,
                                               label      = label           )

    def test_add_edge(self):
        with self.mgraph as _:
            from_node  = _.add_node()
            to_node    = _.add_node()
            new_edge   = _.add_edge(from_node=from_node, to_node=to_node)
            assert _.edges               == [new_edge]
            assert new_edge.from_node    == from_node
            assert new_edge.to_node      == to_node
            assert new_edge.__locals__() == {'attributes': {}, 'from_node': from_node, 'to_node': to_node}

            with Stdout() as stdout:
                _.print()
            assert stdout.value() == ('\n'
                                      '\n'
                                      '┌───────────────────────────────────────────┐\n'
                                      '│ key               │ edges                 │\n'
                                      '├───────────────────────────────────────────┤\n'
                                     f"│ {from_node.node_id} │ ['{to_node.node_id}'] │\n"
                                     f'│ {to_node  .node_id  } │ []                │\n'
                                      '└───────────────────────────────────────────┘\n')
