
from __future__ import annotations

import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from sales_processor import process_sales_data


class SalesProcessorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.temp_path = Path(self.temp_dir.name)

    def _write_input(self, payload: list[dict]) -> Path:
        input_path = self.temp_path / "input.json"
        with input_path.open("w", encoding="utf-8") as handle:
            json.dump(payload, handle)
        return input_path

    def test_process_sales_data_end_to_end(self) -> None:
        payload = [
            {
                "id": 1,
                "product": "Apple",
                "category": "Fruit",
                "price": "1.2",
                "quantity": 10,
                "timestamp": "2023-05-01T10:00:00Z",
            },
            {
                "id": 2,
                "product": "Orange",
                "category": "Fruit",
                "price": None,
                "quantity": 5,
                "timestamp": "2023-05-01T11:00:00Z",
            },
            {
                "id": 3,
                "product": "Laptop",
                "category": "Electronics",
                "price": "999.99",
                "quantity": "2",
                "timestamp": "2023-06-15T09:30:00Z",
            },
            {
                "id": 4,
                "product": "Chair",
                "category": "Furniture",
                "price": 50,
                "quantity": "bad",
                "timestamp": "2023-05-20T14:00:00Z",
            },
            {
                "id": 5,
                "product": "Book",
                "category": "Books",
                "price": 15.5,
                "quantity": 3,
                "timestamp": "not-a-date",
            },
            {
                "id": 6,
                "product": "Apple",
                "category": "Fruit",
                "price": 1.25,
                "quantity": 4,
                "timestamp": "2023-06-02T12:00:00Z",
            },
        ]

        input_path = self._write_input(payload)
        results = process_sales_data(input_path, self.temp_path)

        cleaned = results["cleaned"]
        self.assertEqual(len(cleaned), 5, "Records with invalid timestamps should be dropped")

        apple_entries = [row for row in cleaned if row["product"] == "Apple"]
        self.assertEqual(apple_entries[0]["total_value"], 12.0)
        self.assertEqual(apple_entries[1]["total_value"], 5.0)

        orange_entry = next(row for row in cleaned if row["product"] == "Orange")
        self.assertEqual(orange_entry["price"], 0.0)
        self.assertEqual(orange_entry["total_value"], 0.0)

        chair_entry = next(row for row in cleaned if row["product"] == "Chair")
        self.assertEqual(chair_entry["quantity"], 0)
        self.assertEqual(chair_entry["total_value"], 0.0)

        category_summary = results["category_summary"]
        category_totals = {row["category"]: row["total_sales"] for row in category_summary}
        self.assertAlmostEqual(category_totals["Fruit"], 17.0)
        self.assertAlmostEqual(category_totals["Electronics"], 1999.98)

        top_products = results["top_products"]
        self.assertLessEqual(len(top_products), 5)
        self.assertEqual(top_products[0]["product"], "Laptop")

        monthly_summary = results["monthly_summary"]
        monthly_totals = {row["month"]: row["total_sales"] for row in monthly_summary}
        self.assertAlmostEqual(monthly_totals["2023-05"], 12.0)
        self.assertAlmostEqual(monthly_totals["2023-06"], 2004.98)

        # Validate that files were emitted
        for filename in (
            "cleaned_sales.json",
            "category_sales.json",
            "top_products.json",
            "monthly_sales.json",
        ):
            self.assertTrue((self.temp_path / filename).exists(), f"{filename} should exist")

    def test_non_list_input_is_rejected(self) -> None:
        payload = {"foo": "bar"}
        input_path = self._write_input(payload)  # type: ignore[arg-type]

        with self.assertRaises(ValueError):
            process_sales_data(input_path, self.temp_path)


if __name__ == "__main__":
    unittest.main()
