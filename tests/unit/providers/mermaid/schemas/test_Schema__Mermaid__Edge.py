from unittest                                                            import TestCase
from osbot_utils.helpers.Random_Guid                                     import Random_Guid
from osbot_utils.helpers.Safe_Id                                         import Safe_Id
from mgraph_ai.mgraph.schemas.Schema__MGraph__Attribute                  import Schema__MGraph__Attribute
from mgraph_ai.providers.mermaid.schemas.Schema__Mermaid__Node           import Schema__Mermaid__Node
from mgraph_ai.providers.mermaid.schemas.Schema__Mermaid__Edge           import Schema__Mermaid__Edge
from mgraph_ai.providers.mermaid.schemas.Schema__Mermaid__Edge__Config   import Schema__Mermaid__Edge__Config


class test_Schema__Mermaid__Edge(TestCase):

    def setUp(self):                                                                # Initialize test data
        self.edge_config = Schema__Mermaid__Edge__Config(
            edge_id        = Random_Guid()         ,
            from_node_type = Schema__Mermaid__Node ,
            to_node_type   = Schema__Mermaid__Node
        )

        self.attribute = Schema__MGraph__Attribute(
            attribute_id    = Random_Guid()       ,
            attribute_name  = Safe_Id('test')     ,
            attribute_value = "test_value"        ,
            attribute_type  = str
        )

        self.attributes = {self.attribute.attribute_id: self.attribute}

        self.edge = Schema__Mermaid__Edge(
            attributes   = self.attributes          ,
            edge_config  = self.edge_config         ,
            edge_type    = Schema__Mermaid__Edge    ,
            from_node_id = Random_Guid()            ,
            to_node_id   = Random_Guid()            ,
            label        = "Test Edge"
        )

    def test_init(self):                                                            # Tests basic initialization and type checking
        assert type(self.edge)             is Schema__Mermaid__Edge
        assert self.edge.edge_config       == self.edge_config
        assert self.edge.label             == "Test Edge"
        assert len(self.edge.attributes)   == 1

    def test_type_safety_validation(self):                                          # Tests type safety validations
        with self.assertRaises(ValueError) as context:
            Schema__Mermaid__Edge(
                attributes   = self.attributes       ,
                edge_config  = self.edge_config      ,
                edge_type    = Schema__Mermaid__Edge ,
                from_node_id = Random_Guid()         ,
                to_node_id   = Random_Guid()         ,
                label        = 123                   # Invalid type for label
            )
        assert "Invalid type for attribute 'label'" in str(context.exception)

    def test_json_serialization(self):                                              # Tests JSON serialization and deserialization
        json_data = self.edge.json()

        # Verify JSON structure
        assert 'label'        in json_data
        assert 'edge_config'  in json_data
        assert 'attributes'   in json_data
        assert 'from_node_id' in json_data
        assert 'to_node_id'   in json_data

        # Test deserialization
        restored = Schema__Mermaid__Edge.from_json(json_data)
        assert restored.label       == self.edge.label
        assert restored.edge_type   == self.edge.edge_type
        assert restored.edge_config.edge_id == self.edge.edge_config.edge_id