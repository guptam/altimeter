from typing import Any, Dict, List

from rdflib import BNode, Namespace, Graph

from altimeter.core.alti_base_model import BaseAltiModel
from altimeter.core.graph.exceptions import LinkParseException
from altimeter.core.graph.node_cache import NodeCache

from altimeter.core.graph.link import links as Links


class Link(BaseAltiModel):
    """A Link represents the predicate-object portion of a triple.
    Links in general have a link_type which describes the nature of the relationship.

    Args:
        pred: predicate portion of the triple this Link represents
        obj: object portion of the triple this Link represents.
    """

    pred: str
    obj: Any
    link_type: str

    def to_rdf(
        self, subj: BNode, namespace: Namespace, graph: Graph, node_cache: NodeCache
    ) -> None:
        """Graph this link on a BNode in a Graph using a given Namespace to create the full
        predicate.

        Args:
             subj: subject portion of triple - graph this link's pred, obj against it.
             namespace: RDF namespace to use for this triple's predicate
             graph: RDF graph
             node_cache: NodeCache to use to find cached nodes.
        """
        raise NotImplementedError()

    def to_lpg(self, parent: Dict, vertices: List[Dict], edges: List[Dict], prefix: str) -> None:
        """Graph this link on a BNode in a Graph using a given Namespace to create the full
        predicate.

        Args:
             parent: a dictionary og the parent
             vertices: a list of dictionaries of the vertices for a labeled property graph
             edges: a list of dictionaries of the edges for a labeled property graph
             prefix: a prefix to add to the attribute name
        """
        raise NotImplementedError()

    @classmethod
    def parse_obj(cls, data: Dict[str, Any]) -> "Link":
        if cls != Link:
            return super().parse_obj(data)
        link_type = data.get("link_type")
        if link_type is None:
            raise LinkParseException(f"key 'type' not found in {data}")
        pred = data.get("pred")
        if pred is None:
            raise LinkParseException(f"key 'pred' not found in {data}")
        obj = data.get("obj")
        if link_type == "transient_resource_link":
            return Links.TransientResourceLinkLink.parse_obj(data)
        if obj is None:
            raise LinkParseException(f"key 'obj' not found in {data}")
        if link_type == "simple":
            return Links.SimpleLink.parse_obj(data)
        if link_type == "multi":
            return Links.MultiLink.parse_obj(data)
        if link_type == "resource_link":
            return Links.ResourceLinkLink.parse_obj(data)
        if link_type == "tag":
            return Links.TagLink.parse_obj(data)
        raise LinkParseException(f"Unknown field type '{link_type}")
