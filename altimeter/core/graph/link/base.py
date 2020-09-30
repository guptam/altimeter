from typing import Any, Dict, List

from rdflib import BNode, Namespace, Graph

from altimeter.core.graph.node_cache import NodeCache
from altimeter.core.alti_base_model import BaseAltiModel


class Link(BaseAltiModel):
    """A Link represents the predicate-object portion of a triple.
    Links in general have a field_type which describes the nature of the relationship.

    Args:
        pred: predicate portion of the triple this Link represents
        obj: object portion of the triple this Link represents.
    """

    pred: str
    obj: Any
    field_type: str

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
