import csv
import tempfile
import unittest
from pathlib import Path
from scripts.safe_split import run, key_for


class SplitTests(unittest.TestCase):
    def test_header_and_cross_split_duplicates(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "clean"
            source.mkdir()
            for i in range(1, 11):
                with (source / f"Dataset_{i}.txt").open("w", newline="", encoding="utf-8") as f:
                    writer = csv.writer(f)
                    writer.writerow(["sentence", "intent"])
                    for j in range(15):
                        writer.writerow([f"Text {j} shared across sources" if j < 5 else f"Unique text {i} {j}", "A" if j % 2 else "B"])
            out = root / "out"
            report = run(source, out)
            self.assertEqual(report["skipped_header_rows"], 10)
            self.assertEqual(report["normalized_text_overlap_between_splits"], 0)
            parts = {}
            for part in ("train", "val", "test"):
                with (out / f"{part}.csv").open(newline="", encoding="utf-8") as f:
                    parts[part] = list(csv.DictReader(f))
            keys = {p: {key_for(r["sentence"]) for r in rows} for p, rows in parts.items()}
            self.assertFalse(keys["train"] & keys["val"])
            self.assertFalse(keys["train"] & keys["test"])
            self.assertFalse(keys["val"] & keys["test"])
            self.assertEqual(len(parts["val"]), report["before_oversampling"]["val"])
            self.assertEqual(len(parts["test"]), report["before_oversampling"]["test"])


if __name__ == "__main__":
    unittest.main()
