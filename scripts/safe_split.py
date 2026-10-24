#!/usr/bin/env python3
"""Leakage-safe, deterministic replacement for the historical preprocessing split.

Input: clean/Dataset_1.txt ... Dataset_10.txt (CSV with sentence,intent).
Outputs go to a NEW directory; historical files are never overwritten.
"""
import argparse
import csv
import hashlib
import json
import random
import re
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path


def key_for(text):
    """Conservative normalized-text grouping, not semantic near-duplicate detection."""
    return " ".join(unicodedata.normalize("NFKC", text).casefold().split())


def load_records(folder):
    records = []
    skipped_headers = 0
    skipped_empty = 0
    for i in range(1, 11):
        path = folder / f"Dataset_{i}.txt"
        if not path.is_file():
            raise FileNotFoundError(path)
        with path.open(encoding="utf-8-sig", newline="", errors="replace") as stream:
            for line_no, row in enumerate(csv.reader(stream), 1):
                if len(row) != 2:
                    raise ValueError(f"{path}:{line_no}: expected 2 CSV fields, got {len(row)}")
                sentence, intent = (value.strip() for value in row)
                if sentence.casefold() == "sentence" and intent.casefold() == "intent":
                    skipped_headers += 1
                    continue
                if not sentence or not intent or not key_for(sentence):
                    skipped_empty += 1
                    continue
                records.append((sentence, intent, i))
    return records, skipped_headers, skipped_empty


def group_split(records, seed):
    groups = defaultdict(list)
    for record in records:
        groups[key_for(record[0])].append(record)
    # Groups with conflicting labels are kept together, not silently relabelled.
    # Allocate groups to the currently most underfilled split, weighted by size.
    rng = random.Random(seed)
    keys = list(groups)
    rng.shuffle(keys)
    keys.sort(key=lambda k: len(groups[k]), reverse=True)
    targets = {"train": 0.6 * len(records), "val": 0.2 * len(records), "test": 0.2 * len(records)}
    parts = {name: [] for name in targets}
    for k in keys:
        chosen = max(targets, key=lambda name: (targets[name] - len(parts[name])) / targets[name])
        parts[chosen].extend(groups[k])
    assert_no_overlap(parts)
    return parts, groups


def assert_no_overlap(parts):
    keys = {name: {key_for(r[0]) for r in rows} for name, rows in parts.items()}
    for a, b in (("train", "val"), ("train", "test"), ("val", "test")):
        overlap = keys[a] & keys[b]
        if overlap:
            raise AssertionError(f"Leakage between {a} and {b}: {len(overlap)} normalized-text groups")


def oversample_train(rows, seed):
    by_label = defaultdict(list)
    for row in rows:
        by_label[row[1]].append(row)
    if not by_label:
        raise ValueError("Empty training split")
    target = max(map(len, by_label.values()))
    rng = random.Random(seed)
    balanced = list(rows)
    for label, members in sorted(by_label.items()):
        balanced.extend(rng.choice(members) for _ in range(target - len(members)))
    rng.shuffle(balanced)
    return balanced


def save_csv(path, rows):
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(["sentence", "intent", "source_dataset"])
        writer.writerows(rows)


def run(input_dir, output_dir, seed=42):
    if output_dir.exists() and any(output_dir.iterdir()):
        raise FileExistsError(f"Refusing to overwrite nonempty output directory: {output_dir}")
    records, headers, empty = load_records(input_dir)
    if not records:
        raise ValueError("No valid records")
    parts, groups = group_split(records, seed)
    before = {name: len(rows) for name, rows in parts.items()}
    # The held-out sets stay untouched; only train is oversampled.
    balanced_train = oversample_train(parts["train"], seed)
    output_dir.mkdir(parents=True, exist_ok=True)
    save_csv(output_dir / "train.csv", balanced_train)
    save_csv(output_dir / "val.csv", parts["val"])
    save_csv(output_dir / "test.csv", parts["test"])
    conflicting = sum(len({r[1] for r in rows}) > 1 for rows in groups.values())
    report = {
        "seed": seed,
        "input_records": len(records),
        "skipped_header_rows": headers,
        "skipped_empty_rows": empty,
        "unique_normalized_text_groups": len(groups),
        "groups_with_conflicting_labels": conflicting,
        "before_oversampling": before,
        "after_oversampling": {"train": len(balanced_train), "val": len(parts["val"]), "test": len(parts["test"])},
        "class_counts": {name: dict(sorted(Counter(r[1] for r in rows).items()))
                         for name, rows in (("train", balanced_train), ("val", parts["val"]), ("test", parts["test"]))},
        "normalized_text_overlap_between_splits": 0,
        "warning": "Exact normalized-text grouping only; semantic near-duplicates, source-level leakage and upstream rights not verified."
    }
    (output_dir / "audit.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=Path("clean"))
    parser.add_argument("--output", type=Path, default=Path("split_data_corrected"))
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()
    print(json.dumps(run(args.input, args.output, args.seed), indent=2))


if __name__ == "__main__":
    main()
