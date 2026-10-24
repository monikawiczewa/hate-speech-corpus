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

class RegressionTests(unittest.TestCase):
    def fixture(self, root, indexed=True):
        source = root / 'clean'
        source.mkdir()
        for i in range(1, 11):
            with (source/f'Dataset_{i}.txt').open('w',newline='',encoding='utf-8') as f:
                w=csv.writer(f)
                header=['','sentence','intent'] if indexed else ['sentence','intent']
                w.writerow(header)
                for j in range(20):
                    row=[f'  Quoted, text\n{i}-{j}  ', 'A' if j<17 else 'B']
                    w.writerow([j]+row if indexed else row)
                w.writerow(header)
                for j,row in enumerate([['ＳＡＭＥ text','A'],['same   TEXT','B'],['','A']]):
                    w.writerow([100+j]+row if indexed else row)
        return source

    def test_indexed_conflicts_determinism_and_heldout_integrity(self):
        from scripts.verify_split import verify
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); source=self.fixture(root)
            a=run(source,root/'a'); b=run(source,root/'b')
            self.assertEqual(a,b)
            self.assertEqual(a['skipped_header_rows'],20)
            self.assertEqual(a['skipped_empty_rows'],10)
            self.assertEqual(a['groups_with_conflicting_labels'],1)
            self.assertEqual(a['input_records'],220)
            self.assertEqual(verify(source,root/'a')['independent_verification'],'passed')
            for p in ('train','val','test'):
                self.assertEqual((root/'a'/f'{p}.csv').read_bytes(),(root/'b'/f'{p}.csv').read_bytes())
            with self.assertRaises(FileExistsError): run(source,root/'a')

    def test_two_column_still_supported(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); source=self.fixture(root,indexed=False)
            self.assertEqual(run(source,root/'out')['input_records'],220)

    def test_malformed_and_invalid_encoding_fail_closed(self):
        for bad in (b',sentence,intent\n0,one,A,extra\n',b',sentence,intent\n0,\xff,A\n',b',sentence,intent\nno-index,text,A\n'):
            with self.subTest(bad=bad), tempfile.TemporaryDirectory() as tmp:
                root=Path(tmp); source=self.fixture(root)
                (source/'Dataset_1.txt').write_bytes(bad)
                with self.assertRaises((ValueError,UnicodeError)):
                    run(source,root/'out')
                self.assertFalse((root/'out').exists())

    def test_independent_verifier_detects_changed_holdout(self):
        from scripts.verify_split import verify
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); source=self.fixture(root); run(source,root/'out')
            with (root/'out'/'val.csv').open('a') as f: f.write('invented,A,1\n')
            with self.assertRaises(AssertionError): verify(source,root/'out')

    def test_overlap_guard_detects_unicode_duplicates(self):
        from scripts.safe_split import assert_no_overlap
        with self.assertRaises(AssertionError):
            assert_no_overlap({'train':[('ＳＡＭＥ','A',1)],'val':[(' same ','B',2)],'test':[]})


if __name__ == "__main__":
    unittest.main()
