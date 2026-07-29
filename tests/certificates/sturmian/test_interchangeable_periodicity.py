import json
from pathlib import Path

from einstein.repository import repository_root


ROOT = repository_root(Path(__file__))
RESULT = ROOT / "data/sturmian-source/ahi-interchangeable-periodicity.json"


def test_translation_periodicity_census_is_complete_at_forced_indices():
    data = json.loads(RESULT.read_text())
    assert [item["forced_translation_index"] for item in data["results"]] == [51, 49]
    # Number of rank-two sublattices of index n is sigma_1(n).
    assert [item["hnf_count_tested"] for item in data["results"]] == [72, 57]


def test_any_translation_certificate_has_full_quotient_residue_counts():
    data = json.loads(RESULT.read_text())
    for result in data["results"]:
        index = result["forced_translation_index"]
        assert result["translation_fundamental_domain_count"] == len(
            result["translation_fundamental_domains"]
        )
        for certificate in result["translation_fundamental_domains"]:
            assert certificate["hnf"]["determinant"] == index
            assert certificate["up_residue_count"] == index
            assert certificate["down_residue_count"] == index
