from typing import List, Dict

from pydantic import Field
from rdflib import Namespace, Graph, BNode, RDF, Literal

from altimeter.core.graph.link.base import Link
from altimeter.core.graph.node_cache import NodeCache
from altimeter.core.alti_base_model import BaseAltiModel


class Resource(BaseAltiModel):
    """A Resource defines a single scanned resource which is directly translatable to a graph
    node.  It contains an id, type name and list of Links.

    Args:
         resource_id: id of this resource
         resource_type: type name of this resource
         links: List of Links for this resource
    """

    resource_id: str
    resource_type: str
    links: List[Link] = Field(default_factory=list)

    def to_rdf(self, namespace: Namespace, graph: Graph, node_cache: NodeCache) -> None:
        """Graph this Resource as a BNode on a Graph.

        Args:
            namespace: RDF namespace to use for predicates and objects when graphing
                       this resource's links
            graph: RDF graph
            node_cache: NodeCache to use for any cached BNode lookups
        """
        node = node_cache.setdefault(self.resource_id, BNode())
        graph.add((node, RDF.type, getattr(namespace, self.resource_type)))
        graph.add((node, getattr(namespace, "id"), Literal(self.resource_id)))
        for link in self.links:
            link.to_rdf(subj=node, namespace=namespace, graph=graph, node_cache=node_cache)

    def to_lpg(self, vertices: List[Dict], edges: List[Dict]) -> None:
        """Graph this Resource as a dictionary into the vertices and edges lists.

        Args:
            vertices: List containing dictionaries representing a vertex
            edges: List containing dictionaries representing an edge
        """
        vertex = {
            "~id": self.resource_id,
            "~label": self.resource_type,
            "arn": self.resource_id,
        }
        for link in self.links:
            link.to_lpg(vertex, vertices, edges, "")

        vertices.append(vertex)
