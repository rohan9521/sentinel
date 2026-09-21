from __future__ import annotations

from sentinel.data.synthetic import SyntheticCaseGenerator


def test_split_cases_time_based_has_no_leakage() -> None:
    generator = SyntheticCaseGenerator(seed=7)
    cases = generator.generate_cases(200)

    train, val, test = generator.split_cases_time_based(cases)

    train_ids = {case.case_id for case in train}
    val_ids = {case.case_id for case in val}
    test_ids = {case.case_id for case in test}

    assert train_ids.isdisjoint(val_ids)
    assert train_ids.isdisjoint(test_ids)
    assert val_ids.isdisjoint(test_ids)
    assert max(case.transaction.timestamp for case in train) <= min(case.transaction.timestamp for case in val)
    assert max(case.transaction.timestamp for case in val) <= min(case.transaction.timestamp for case in test)


def test_synthetic_data_is_seeded_and_reproducible() -> None:
    generator_a = SyntheticCaseGenerator(seed=123)
    generator_b = SyntheticCaseGenerator(seed=123)

    cases_a = generator_a.generate_cases(25)
    cases_b = generator_b.generate_cases(25)

    assert [case.case_id for case in cases_a] == [case.case_id for case in cases_b]
    assert [case.transaction.amount for case in cases_a] == [case.transaction.amount for case in cases_b]
