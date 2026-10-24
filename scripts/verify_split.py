"""Independently inspect serialized CSVs; emit aggregate-only verification."""
import argparse
import csv
import hashlib
import json
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path


def normalized(text):
    return ' '.join(unicodedata.normalize('NFKC', text).casefold().split())


def verify(source, output):
    originals = Counter()
    groups = defaultdict(set)
    raw = headers = empty = 0
    for i in range(1, 11):
        with (source / f'Dataset_{i}.txt').open(encoding='utf-8-sig', newline='') as f:
            for row in csv.reader(f, strict=True):
                raw += 1
                if [x.strip().lower() for x in row[-2:]] == ['sentence', 'intent']:
                    headers += 1
                    continue
                if len(row) not in (2, 3):
                    raise AssertionError('Malformed input row')
                text, label = row[-2:]
                if not normalized(text) or not label.strip():
                    empty += 1
                    continue
                originals[(text, label, str(i))] += 1
                groups[normalized(text)].add(label)
    parts = {}
    for name in ('train', 'val', 'test'):
        with (output / f'{name}.csv').open(encoding='utf-8', newline='') as f:
            reader = csv.DictReader(f)
            assert reader.fieldnames == ['sentence', 'intent', 'source_dataset']
            parts[name] = Counter((r['sentence'], r['intent'], r['source_dataset']) for r in reader)
    keys = {p: {normalized(r[0]) for r in rows} for p, rows in parts.items()}
    pairs = {f'{a}-{b}': len(keys[a] & keys[b]) for a,b in
             (('train','val'),('train','test'),('val','test'))}
    assert not any(pairs.values()), pairs
    assert set().union(*keys.values()) == set(groups)
    # No missing/altered/extra held-out rows; train may only repeat its originals.
    for p, rows in parts.items():
        expected = Counter({r:n for r,n in originals.items() if normalized(r[0]) in keys[p]})
        if p == 'train':
            assert rows.keys() == expected.keys()
            assert all(rows[r] >= n for r,n in expected.items())
        else:
            assert rows == expected, f'{p}: held-out records changed'
    report = json.loads((output / 'audit.json').read_text())
    assert report['input_records'] == sum(originals.values())
    assert report['ingestion']['raw_csv_records'] == raw
    assert report['skipped_header_rows'] == headers
    assert report['skipped_empty_rows'] == empty
    for p, rows in parts.items():
        before = sum(n for r,n in originals.items() if normalized(r[0]) in keys[p])
        counts = Counter()
        for r,n in rows.items(): counts[r[1]] += n
        assert report['before_oversampling'][p] == before
        assert report['after_oversampling'][p] == sum(rows.values())
        assert report['class_counts'][p] == dict(counts)
    assert len(set(report['class_counts']['train'].values())) == 1
    assert report['groups_with_conflicting_labels'] == sum(len(v)>1 for v in groups.values())
    # Limited lexical diagnostic: collapse punctuation and whitespace, without
    # calling this exhaustive near-duplicate or semantic detection.
    loose = {p: {''.join(c for c in k if c.isalnum()) for k in ks} - {''} for p,ks in keys.items()}
    result = {'independent_verification': 'passed', 'raw_csv_records': raw,
              'pairwise_normalized_overlap': pairs,
              'held_out_record_multisets_unchanged': True,
              'conflicting_label_groups_kept_together': True,
              'training_only_replication': True,
              'punctuation_insensitive_overlap': {f'{a}-{b}':len(loose[a]&loose[b]) for a,b in
                  (('train','val'),('train','test'),('val','test'))},
              'source_ids_in_splits': {p:sorted({r[2] for r in rows},key=int) for p,rows in parts.items()},
              'output_sha256': {p:hashlib.sha256((output/f'{p}.csv').read_bytes()).hexdigest() for p in parts}}
    (output/'verification.json').write_text(json.dumps(result,indent=2)+'\n')
    return result

if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--input',type=Path,default=Path('clean'))
    parser.add_argument('--output',type=Path,default=Path('split_data_corrected'))
    a=parser.parse_args()
    print(json.dumps(verify(a.input,a.output),indent=2))
