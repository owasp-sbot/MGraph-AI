from typing                                         import Dict
from xml.dom                                        import minidom
from xml.etree                                      import ElementTree
from xml.etree.ElementTree                          import Element, SubElement
from mgraph_ai.mgraph.actions.MGraph__Data          import MGraph__Data
from mgraph_ai.mgraph.domain.Domain__MGraph__Graph  import Domain__MGraph__Graph
from osbot_utils.type_safe.Type_Safe                import Type_Safe

class MGraph__Export(Type_Safe):
    graph: Domain__MGraph__Graph

    def data(self):                                                                        # Access to graph data
        return MGraph__Data(graph=self.graph)

    def to__mgraph_json(self):                                                            # Export full graph data
        return self.graph.model.data.json()

    def to__json(self):                                                                   # Export minimal topology
        nodes = {}
        edges = {}
        with self.data() as _:
            for domain_node in _.nodes():
                node = domain_node.node_id
                nodes[node] = {}
            for domain_edge in _.edges():
                edge = domain_edge.edge_id
                edges[edge] = {'from_node_id': domain_edge.from_node_id(),
                             'to_node_id'   : domain_edge.to_node_id  ()}
        return dict(nodes=nodes, edges=edges)

    def to__xml(self) -> str:                                                               # Export as XML
        root  = Element('graph')                                                            # Create root element and main containers
        nodes = SubElement(root, 'nodes')
        edges = SubElement(root, 'edges')

        with self.data() as _:                                                              # Add all nodes
            for node in _.nodes():
                SubElement(nodes, 'node', {'id': str(node.node_id)})

        with self.data() as _:                                                              # Add all edges
            for edge in _.edges():
                edge_elem       = SubElement(edges, 'edge', {'id': str(edge.edge_id)})
                from_elem       = SubElement(edge_elem, 'from')
                from_elem.text  = str(edge.from_node_id())
                to_elem         = SubElement(edge_elem, 'to')
                to_elem.text    = str(edge.to_node_id())
        return self.format_xml(root, indent='  ')

    def to__dot(self) -> str:                                                            # Export as DOT graph
        lines = ['digraph {']

        with self.data() as _:
            # First output all nodes
            for node in _.nodes():
                lines.append(f'  "{node.node_id}"')

            # Then output all edges
            for edge in _.edges():
                lines.append(f'  "{edge.from_node_id()}" -> "{edge.to_node_id()}" [id="{edge.edge_id}"]')

        lines.append('}')
        return '\n'.join(lines)

    def to__graphml(self) -> str:  # Export as GraphML
        graphml_ns = "http://graphml.graphdrawing.org/xmlns"  # Define namespace

        # Create root element with namespace attribute
        root = Element('graphml', {
            'xmlns': graphml_ns  # Add namespace as attribute
        })

        graph = SubElement(root, 'graph', {
            'id': 'G',
            'edgedefault': 'directed'
        })

        with self.data() as _:  # Add all nodes
            for node in _.nodes():
                SubElement(graph, 'node', {'id': str(node.node_id)})

        with self.data() as _:  # Add all edges
            for edge in _.edges():
                SubElement(graph, 'edge', {
                    'id': str(edge.edge_id),
                    'source': str(edge.from_node_id()),
                    'target': str(edge.to_node_id())
                })

        return self.format_xml(root, indent='  ')

    def to__turtle(self) -> str:                                                         # Export as RDF/Turtle
        lines = ['@prefix mg: <http://mgraph.org/> .']
        lines.append('')

        with self.data() as _:
            # Declare nodes
            for node in _.nodes():
                lines.append(f'mg:{node.node_id} a mg:Node .')

            lines.append('')
            # Declare edges
            for edge in _.edges():
                lines.append(f'mg:{edge.edge_id} mg:from mg:{edge.from_node_id()} ;')
                lines.append(f'            mg:to   mg:{edge.to_node_id()} .')
                lines.append('')

        return '\n'.join(lines)

    def to__ntriples(self) -> str:                                                      # Export as N-Triples
        lines = []
        with self.data() as _:
            # Declare nodes
            for node in _.nodes():
                lines.append(f'<urn:{node.node_id}> <urn:exists> "true" .')

            # Declare edges
            for edge in _.edges():
                lines.append(f'<urn:{edge.edge_id}> <urn:from> <urn:{edge.from_node_id()}> .')
                lines.append(f'<urn:{edge.edge_id}> <urn:to> <urn:{edge.to_node_id()}> .')

        return '\n'.join(lines)

    def to__gexf(self) -> str:                                              # Export as GEXF
        gexf_ns = "http://www.gexf.net/1.2draft"                            # Define namespace


        root = Element('gexf', {'xmlns'  : gexf_ns,
                                'version': '1.2'  })                        # Create root element with namespace attribute and version

        graph = SubElement(root, 'graph', { 'defaultedgetype': 'directed' })

        nodes_elem = SubElement(graph, 'nodes')                             # Create nodes container and add all nodes
        with self.data() as _:                                              # Add all nodes
            for node in _.nodes():
                SubElement(nodes_elem, 'node', {'id': str(node.node_id)})

        edges_elem = SubElement(graph, 'edges')                             # Create edges container and add all edges
        with self.data() as _:                                              # Add all edges
            for edge in _.edges():
                SubElement(edges_elem, 'edge', {'id'    : str(edge.edge_id       ),
                                                'source': str(edge.from_node_id()),
                                                'target': str(edge.to_node_id  ()) })

        return self.format_xml(root, indent='  ')

    def to__tgf(self) -> str:                                                           # Export as TGF
        lines = []

        # First output all nodes
        with self.data() as _:
            for node in _.nodes():
                lines.append(str(node.node_id))

        # Separator between nodes and edges
        lines.append('#')

        # Then output all edges
        with self.data() as _:
            for edge in _.edges():
                lines.append(f'{edge.from_node_id()} {edge.to_node_id()} {edge.edge_id}')

        return '\n'.join(lines)

    def to__cypher(self) -> str:                                                        # Export as Neo4j Cypher
        lines = ['CREATE']
        node_refs = {}

        with self.data() as _:
            # Create node references
            for i, node in enumerate(_.nodes()):
                node_refs[node.node_id] = f'n{i}'
                if i == 0:
                    lines.append(f'  ({node_refs[node.node_id]}:Node {{id: \'{node.node_id}\'}})')
                else:
                    lines.append(f', ({node_refs[node.node_id]}:Node {{id: \'{node.node_id}\'}})')

            # Create edges
            for i, edge in enumerate(_.edges()):
                from_ref = node_refs[edge.from_node_id()]
                to_ref = node_refs[edge.to_node_id()]
                lines.append(f', ({from_ref})-[r{i}:CONNECTS {{id: \'{edge.edge_id}\'}}]->({to_ref})')

        return '\n'.join(lines)

    def to__csv(self) -> Dict[str, str]:                                                # Export as CSV
        nodes_csv = ['node_id']
        edges_csv = ['edge_id,from_node_id,to_node_id']

        with self.data() as _:
            for node in _.nodes():
                nodes_csv.append(str(node.node_id))

            for edge in _.edges():
                edges_csv.append(f'{edge.edge_id},{edge.from_node_id()},{edge.to_node_id()}')

        return {
            'nodes.csv': '\n'.join(nodes_csv),
            'edges.csv': '\n'.join(edges_csv)
        }



    def format_xml(self, root: ElementTree,indent: str = '  ') -> str:  # Format an XML ElementTree with consistent indentation.
        xml_str       = ElementTree.tostring(root, encoding='UTF-8')                                # Convert to string with UTF-8 encoding
        dom           = minidom.parseString(xml_str)                                                # Parse and format using minidom
        formatted_xml = dom.toprettyxml(indent=indent, encoding='UTF-8').decode('UTF-8')
        return '\n'.join(line for line in formatted_xml.splitlines() if line.strip())               # Remove extra blank lines while preserving intended whitespace