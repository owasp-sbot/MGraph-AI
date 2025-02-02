from typing                                         import Type
from mgraph_db.mgraph.actions.MGraph__Export        import MGraph__Export
from mgraph_db.mgraph.actions.MGraph__Screenshot    import MGraph__Screenshot
from mgraph_db.mgraph.domain.Domain__MGraph__Graph  import Domain__MGraph__Graph
from mgraph_db.mgraph.actions.MGraph__Data          import MGraph__Data
from mgraph_db.mgraph.actions.MGraph__Edit          import MGraph__Edit
from mgraph_db.mgraph.actions.MGraph__Storage       import MGraph__Storage
from mgraph_db.mgraph.actions.MGraph__Index         import MGraph__Index
from mgraph_db.query.MGraph__Query                  import MGraph__Query
from osbot_utils.type_safe.Type_Safe                import Type_Safe

class MGraph(Type_Safe):                                                                                        # Main MGraph class that users will interact with
    graph           : Domain__MGraph__Graph                                                                                       # Reference to the underlying graph model
    query_class     : Type[MGraph__Query     ]
    edit_class      : Type[MGraph__Edit      ]
    screenshot_class: Type[MGraph__Screenshot]

    def data(self) -> MGraph__Data:
        return MGraph__Data(graph=self.graph)

    def edit(self) -> MGraph__Edit:
        return self.edit_class(graph=self.graph)

    def export(self) -> MGraph__Export:
        return MGraph__Export(graph=self.graph)

    def index(self) -> MGraph__Index:
        return MGraph__Index.from_graph(self.graph)

    def query(self) -> MGraph__Query:
        mgraph_data  = self.data()
        mgraph_index = self.index()
        mgraph_query = self.query_class(mgraph_data=mgraph_data, mgraph_index=mgraph_index).setup()
        return mgraph_query

    def storage(self) -> MGraph__Storage:
        return MGraph__Storage(graph=self.graph)

    def screenshot(self, **kwargs):                                                                                     # Access screenshot operations
        return self.screenshot_class(**kwargs, graph=self.graph)






