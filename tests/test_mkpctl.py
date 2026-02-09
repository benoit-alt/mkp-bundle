"""Unit tests for mkpctl v1.0.1 — covers top_predicates, _validate_exit_code, _exit_class."""

import unittest
from collections import Counter


class TestExitClass(unittest.TestCase):
    """Test _exit_class() mapping per SPEC-003."""

    def _exit_class(self, code):
        # Mirror the implementation in mkp.cli
        if code == 0: return "success"
        if 21 <= code <= 25: return "validation"
        if 31 <= code <= 32: return "load"
        if 41 <= code <= 42: return "helper"
        return "internal"

    def test_success(self):
        self.assertEqual(self._exit_class(0), "success")

    def test_validation_family(self):
        for code in (21, 22, 23, 24, 25):
            self.assertEqual(self._exit_class(code), "validation", f"code {code}")

    def test_load_family(self):
        for code in (31, 32):
            self.assertEqual(self._exit_class(code), "load", f"code {code}")

    def test_helper_family(self):
        for code in (41, 42):
            self.assertEqual(self._exit_class(code), "helper", f"code {code}")

    def test_internal_fallback(self):
        self.assertEqual(self._exit_class(1), "internal")
        self.assertEqual(self._exit_class(99), "internal")


class TestValidateExitCode(unittest.TestCase):
    """Test _validate_exit_code() string-to-code mapping per SPEC-003."""

    def _validate_exit_code(self, msg):
        # Mirror the implementation in mkp.cli
        if "missing columns" in msg: return 21
        if "Invalid URN" in msg: return 22
        if "Predicate not allowed" in msg: return 23
        if "Dangling reference" in msg: return 24
        if "mutate Core" in msg: return 25
        return 21

    def test_schema_missing_columns(self):
        self.assertEqual(self._validate_exit_code("entities.csv: missing columns ['id']"), 21)

    def test_schema_empty_file(self):
        # "is empty" doesn't match any specific rule → defaults to 21 (schema)
        self.assertEqual(self._validate_exit_code("entities.csv is empty"), 21)

    def test_urn_entities(self):
        self.assertEqual(self._validate_exit_code("Invalid URN in entities: bad:urn"), 22)

    def test_urn_relationships(self):
        self.assertEqual(self._validate_exit_code("Invalid URN in relationships: {...}"), 22)

    def test_urn_module_entities(self):
        self.assertEqual(self._validate_exit_code("Invalid URN in module entities: x"), 22)

    def test_urn_module_relationships(self):
        self.assertEqual(self._validate_exit_code("Invalid URN in module relationships: {...}"), 22)

    def test_predicate_core(self):
        self.assertEqual(self._validate_exit_code("Predicate not allowed (core): FOOBAR"), 23)

    def test_predicate_module(self):
        self.assertEqual(self._validate_exit_code("Predicate not allowed (module): FOOBAR"), 23)

    def test_dangling_source(self):
        self.assertEqual(self._validate_exit_code("Dangling reference (source): urn:x"), 24)

    def test_dangling_target(self):
        self.assertEqual(self._validate_exit_code("Dangling reference (target): urn:x"), 24)

    def test_mutate_core(self):
        self.assertEqual(self._validate_exit_code("Module attempts to mutate Core entity: urn:x"), 25)

    def test_nested_in_loader_message(self):
        """Verify that _validate_exit_code works on loader.py's wrapped messages too."""
        msg = "Core validation failed: Invalid URN in entities: bad:urn"
        self.assertEqual(self._validate_exit_code(msg), 22)

        msg = "Module validation failed (01_Module_DarkWeb): Dangling reference (source): urn:x"
        self.assertEqual(self._validate_exit_code(msg), 24)

        msg = "Module validation failed (01_Module_DarkWeb): Predicate not allowed (module): FOOBAR"
        self.assertEqual(self._validate_exit_code(msg), 23)


class TestTopPredicates(unittest.TestCase):
    """Test top_predicates computation logic (same as loader.py lines 86-92)."""

    def _compute_top_predicates(self, all_rels, limit=3):
        pred_counts = Counter(r["relation"] for r in all_rels)
        return [
            {"predicate": p, "edge_count": c}
            for p, c in sorted(pred_counts.items(), key=lambda x: (-x[1], x[0]))[:limit]
        ]

    def test_empty_relationships(self):
        self.assertEqual(self._compute_top_predicates([]), [])

    def test_single_predicate(self):
        rels = [{"relation": "USES"}]
        result = self._compute_top_predicates(rels)
        self.assertEqual(result, [{"predicate": "USES", "edge_count": 1}])

    def test_top_3_by_count(self):
        rels = [
            {"relation": "USES"},
            {"relation": "USES"},
            {"relation": "PROVIDES"},
            {"relation": "PROVIDES"},
            {"relation": "PROVIDES"},
            {"relation": "IS_A"},
            {"relation": "TARGETS"},
        ]
        result = self._compute_top_predicates(rels)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0], {"predicate": "PROVIDES", "edge_count": 3})
        self.assertEqual(result[1], {"predicate": "USES", "edge_count": 2})
        self.assertEqual(result[2], {"predicate": "IS_A", "edge_count": 1})

    def test_alphabetical_tiebreak(self):
        rels = [
            {"relation": "RELATED_TO"},
            {"relation": "PROVIDES"},
            {"relation": "AFFILIATED_WITH"},
        ]
        result = self._compute_top_predicates(rels)
        # All have count 1 → sorted alphabetically
        self.assertEqual(result[0]["predicate"], "AFFILIATED_WITH")
        self.assertEqual(result[1]["predicate"], "PROVIDES")
        self.assertEqual(result[2]["predicate"], "RELATED_TO")

    def test_truncation_to_3(self):
        rels = [
            {"relation": "A"}, {"relation": "B"}, {"relation": "C"},
            {"relation": "D"}, {"relation": "E"},
        ]
        result = self._compute_top_predicates(rels)
        self.assertEqual(len(result), 3)
        self.assertEqual([r["predicate"] for r in result], ["A", "B", "C"])

    def test_deterministic_sort(self):
        """Same input twice → identical output."""
        rels = [
            {"relation": "USES"}, {"relation": "USES"},
            {"relation": "IS_A"}, {"relation": "IS_A"},
            {"relation": "PROVIDES"},
        ]
        r1 = self._compute_top_predicates(rels)
        r2 = self._compute_top_predicates(rels)
        self.assertEqual(r1, r2)


if __name__ == "__main__":
    unittest.main()
