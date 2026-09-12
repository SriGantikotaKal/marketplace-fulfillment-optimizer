from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Sequence


@dataclass(frozen=True)
class Order:
    order_id: str
    units: int
    sla_hours: float
    zone: str


@dataclass(frozen=True)
class FulfillmentNode:
    node_id: str
    available_units: int
    zone: str
    average_pick_pack_hours: float
    distance_hours_by_zone: Mapping[str, float]


def assign_orders(
    orders: Sequence[Mapping[str, object]],
    nodes: Sequence[Mapping[str, object]],
) -> list[dict[str, object]]:
    remaining_capacity = {str(node["node_id"]): int(node["available_units"]) for node in nodes}
    typed_nodes = [_node(node) for node in nodes]
    assignments: list[dict[str, object]] = []

    for order_value in orders:
        order = _order(order_value)
        candidates = []
        skipped = []

        for node in typed_nodes:
            if remaining_capacity[node.node_id] < order.units:
                skipped.append({"node_id": node.node_id, "reason": "insufficient_capacity"})
                continue

            travel_hours = node.distance_hours_by_zone.get(order.zone)
            if travel_hours is None:
                skipped.append({"node_id": node.node_id, "reason": "zone_not_supported"})
                continue

            estimated_hours = node.average_pick_pack_hours + travel_hours
            if estimated_hours > order.sla_hours:
                skipped.append({"node_id": node.node_id, "reason": "sla_miss"})
                continue

            zone_penalty = 0 if node.zone == order.zone else 1
            candidates.append((estimated_hours, zone_penalty, node.node_id))

        if not candidates:
            assignments.append({"order_id": order.order_id, "node_id": None, "status": "unassigned", "skipped": skipped})
            continue

        _, _, selected_node = min(candidates)
        remaining_capacity[selected_node] -= order.units
        assignments.append({"order_id": order.order_id, "node_id": selected_node, "status": "assigned", "skipped": skipped})

    return assignments


def _order(value: Mapping[str, object]) -> Order:
    return Order(
        order_id=str(value["order_id"]),
        units=int(value["units"]),
        sla_hours=float(value["sla_hours"]),
        zone=str(value["zone"]),
    )


def _node(value: Mapping[str, object]) -> FulfillmentNode:
    distances = value["distance_hours_by_zone"]
    if not isinstance(distances, Mapping):
        raise ValueError("distance_hours_by_zone must be a mapping")
    return FulfillmentNode(
        node_id=str(value["node_id"]),
        available_units=int(value["available_units"]),
        zone=str(value["zone"]),
        average_pick_pack_hours=float(value["average_pick_pack_hours"]),
        distance_hours_by_zone={str(key): float(val) for key, val in distances.items()},
    )

