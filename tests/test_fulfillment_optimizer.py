import sys
import unittest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.fulfillment_optimizer import assign_orders


class FulfillmentOptimizerTests(unittest.TestCase):
    def test_assigns_to_fastest_sla_safe_node(self):
        result = assign_orders(
            [{"order_id": "o-1", "units": 4, "sla_hours": 6, "zone": "west"}],
            [
                {"node_id": "sd-1", "available_units": 10, "zone": "west", "average_pick_pack_hours": 1.5, "distance_hours_by_zone": {"west": 2}},
                {"node_id": "az-1", "available_units": 10, "zone": "southwest", "average_pick_pack_hours": 1.0, "distance_hours_by_zone": {"west": 4}},
            ],
        )

        self.assertEqual(result[0]["status"], "assigned")
        self.assertEqual(result[0]["node_id"], "sd-1")

    def test_respects_capacity_across_orders(self):
        result = assign_orders(
            [
                {"order_id": "o-1", "units": 6, "sla_hours": 6, "zone": "west"},
                {"order_id": "o-2", "units": 6, "sla_hours": 6, "zone": "west"},
            ],
            [{"node_id": "sd-1", "available_units": 10, "zone": "west", "average_pick_pack_hours": 1, "distance_hours_by_zone": {"west": 2}}],
        )

        self.assertEqual(result[0]["status"], "assigned")
        self.assertEqual(result[1]["status"], "unassigned")


if __name__ == "__main__":
    unittest.main()

