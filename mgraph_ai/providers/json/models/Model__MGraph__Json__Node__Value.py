from typing                                                             import Any
from mgraph_ai.providers.json.models.Model__MGraph__Json__Node          import Model__MGraph__Json__Node
from mgraph_ai.providers.json.schemas.Schema__MGraph__Json__Node__Value import Schema__MGraph__Json__Node__Value
from osbot_utils.type_safe.methods.type_safe_property                   import set_as_property

class Model__MGraph__Json__Node__Value(Model__MGraph__Json__Node):                         # Model class for JSON value nodes
    data: Schema__MGraph__Json__Node__Value

    value_type = set_as_property('data.node_data', 'value_type')

    def is_primitive(self) -> bool:                                                         # Check if the value is a primitive type
        return self.value_type in (str, int, float, bool, type(None))

    @property
    def value(self) -> Any:
        return self.data.node_data.value

    @value.setter
    def value(self, new_value: Any) -> None:
        self.data.node_data.value      = new_value
        self.data.node_data.value_type = type(new_value)