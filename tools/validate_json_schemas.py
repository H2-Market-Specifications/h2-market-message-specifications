#!/usr/bin/env python3
"""Validate JSON files, JSON Schemas, schema refs and examples.

Designed for repositories that contain market-message specifications such as:
- schemas/**/*.json
- examples/**/*.json
- message test files validated through validation/validation-manifest.yml

The check intentionally does not fetch remote schemas. All schemas and referenced
schemas must be present in the repository or be addressable through a local $id.
"""

import argparse
from pathlib import Path
import json
import sys

from validation.core import CheckResult, LoadedJson, DuplicateKeyError, load_json_file, iter_json_files, rel
from validation.schema import is_schema_file, build_schema_stores, validate_schema_self, check_ref_targets, validate_schema_declared_instances
from validation.manifest import load_manifest, validate_manifest_examples, validate_catalog_references, validate_catalog_manifest_coverage


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".", help="Repository root")
    parser.add_argument("--manifest", default="validation/validation-manifest.yml", help="YAML validation manifest")
    parser.add_argument(
        "--require-manifest",
        action="store_true",
        help="Fail if no explicit manifest validations are configured",
    )
    parser.add_argument(
        "--standards-only",
        action="store_true",
        help="Run repository-wide JSON/schema/ref/$schema standards checks without manifest example validation.",
    )
    parser.add_argument(
        "--examples-only",
        action="store_true",
        help="Run manifest-based positive/negative example validation without repository-wide standards checks.",
    )
    args = parser.parse_args()

    if args.standards_only and args.examples_only:
        parser.error("--standards-only and --examples-only are mutually exclusive")

    root = Path(args.root).resolve()
    manifest_path = (root / args.manifest).resolve()
    result = CheckResult(errors=[], warnings=[])

    # Step 1: load every JSON file in the repository once, up front, so the
    # later steps can just look it up instead of re-reading from disk.
    loaded_json: list[LoadedJson] = []
    json_files = iter_json_files(root)

    for path in json_files:
        try:
            loaded_json.append(LoadedJson(path=path, data=load_json_file(path)))
        except DuplicateKeyError as exc:
            result.error(f"{rel(path, root)}: invalid JSON: {exc}")
        except json.JSONDecodeError as exc:
            result.error(f"{rel(path, root)}: invalid JSON syntax at line {exc.lineno}, column {exc.colno}: {exc.msg}")
        except Exception as exc:
            result.error(f"{rel(path, root)}: cannot read JSON: {exc}")

    # Step 2: figure out which of the loaded files are schemas, and build
    # the lookup stores needed to resolve $ref / $schema / catalog refs.
    schemas = [loaded for loaded in loaded_json if is_schema_file(loaded.path, loaded.data, root)]

    if not schemas:
        result.warn("No JSON Schema files detected. Expected *.schema.json or JSON files under schemas/.")

    store, uri_to_schema_path, path_to_schema = build_schema_stores(root, schemas)
    loaded_by_path = {loaded.path.resolve(): loaded for loaded in loaded_json}

    # Step 3: repository-wide "standards" checks (schema validity, ref
    # resolution, $schema-declared instances, catalog wiring) — skipped
    # when only manifest example validation was requested.
    if not args.examples_only:
        for schema in schemas:
            validate_schema_self(root, schema, result)
            check_ref_targets(root, schema, store, uri_to_schema_path, path_to_schema, result)

        validate_schema_declared_instances(root, loaded_json, schemas, store, uri_to_schema_path, result)
        validate_catalog_references(root, loaded_by_path, store, uri_to_schema_path, result)

    # Step 4: manifest-driven positive/negative example validation —
    # skipped when only the standards checks above were requested.
    if not args.standards_only:
        validate_manifest_examples(root, manifest_path, store, uri_to_schema_path, loaded_by_path, result)

    # Step 5 (optional, --require-manifest): additionally enforce that the
    # manifest actually declares validations, and that every catalog
    # message/example is covered by one of them.
    if args.require_manifest and not args.standards_only:
        try:
            manifest = load_manifest(manifest_path)
            if not manifest.get("validations"):
                result.error(f"{rel(manifest_path, root)}: no explicit validations configured")
            validate_catalog_manifest_coverage(root, manifest_path, loaded_by_path, store, uri_to_schema_path, result)
        except Exception:
            # Already reported above.
            pass

    print("JSON files checked:", len(json_files))
    print("JSON Schemas checked:", len(schemas))

    if result.warnings:
        print("\nWarnings:")
        for warning in result.warnings:
            print(f"::warning::{warning}")

    if result.errors:
        print("\nErrors:")
        for error in result.errors:
            print(f"::error::{error}")
        return 1

    print("\nValidation successful.")
    return 0


if __name__ == "__main__":
    sys.exit(main())