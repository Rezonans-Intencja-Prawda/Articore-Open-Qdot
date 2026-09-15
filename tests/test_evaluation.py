"""
Testy modułu Evaluator.

Realizują zasady z Tablica.txt:
- Każda zmiana musi mieć powód i wynik testu
- Zmiana produkcyjna musi być odwracalna
- Nie nagradzać pewności samej w sobie
- Detekcja regresji
"""

import pytest
from core import ObservationRecord, ContradictionStatus, Evaluator, Provenance


class TestEvaluator:
    """Testy ewaluatora."""

    def test_correct_result_can_promote(self):
        """Poprawny wynik z wysoką pewnością — można promować."""
        record = ObservationRecord(
            task="Optymalizacja poprawna",
            expected=8,
            observed=8,
            confidence=0.9,
        )
        result = Evaluator.evaluate(record)
        assert result.correctness is True
        assert result.can_promote is True
        assert result.regression_detected is False

    def test_regression_detected(self):
        """Wykrycie regresji — wynik różny, wysoka pewność."""
        record = ObservationRecord(
            task="Optymalizacja błędna",
            expected=8,
            observed=6,
            confidence=0.85,
        )
        result = Evaluator.evaluate(record)
        assert result.correctness is False
        assert result.regression_detected is True
        assert result.can_promote is False

    def test_contradiction_blocks_promotion(self):
        """Sprzeczność blokuje promocję."""
        record = ObservationRecord(
            task="Sprzeczne dane",
            expected="prawda",
            observed="falsz",
            confidence=0.9,
        )
        result = Evaluator.evaluate(record)
        assert result.contradiction_status == ContradictionStatus.CONTRADICTORY.value
        assert result.can_promote is False
        assert "rollback" in result.recommendation.lower()

    def test_insufficient_data_blocks_promotion(self):
        """Niewystarczające dane blokują promocję."""
        record = ObservationRecord(
            task="Brak danych",
            expected="X",
            observed="Y",
            confidence=0.1,
        )
        result = Evaluator.evaluate(record)
        assert result.can_promote is False
        assert "wystarczając" in result.recommendation.lower()

    def test_unknown_state_blocks_promotion(self):
        """Stan UNKNOWN blokuje promocję."""
        record = ObservationRecord(
            task="Niepewne",
            expected=100,
            observed=99,
            confidence=0.25,
        )
        result = Evaluator.evaluate(record)
        assert result.can_promote is False

    def test_errors_block_promotion(self):
        """Błędy blokują promocję nawet przy zgodnym wyniku."""
        record = ObservationRecord(
            task="Z błędami",
            expected="ok",
            observed="ok",
            confidence=0.9,
            errors=["warning_deprecated"],
        )
        result = Evaluator.evaluate(record)
        assert result.can_promote is False

    def test_low_confidence_correct_blocks_promotion(self):
        """Poprawny wynik, ale niska pewność — brak promocji."""
        record = ObservationRecord(
            task="Niska pewność",
            expected="ok",
            observed="ok",
            confidence=0.4,
        )
        result = Evaluator.evaluate(record)
        assert result.correctness is True
        assert result.can_promote is False

    def test_improvement_hypothesis_generated(self):
        """Przy rozbieżności generowana jest hipoteza poprawy."""
        record = ObservationRecord(
            task="Test hipotezy",
            expected=10,
            observed=7,
            confidence=0.5,
        )
        result = Evaluator.evaluate(record)
        assert result.metrics_summary["improvement_hypothesis"] is not None
        assert "Rozbieżność" in result.metrics_summary["improvement_hypothesis"]

    def test_no_improvement_hypothesis_when_correct(self):
        """Brak hipotezy poprawy przy poprawnym wyniku."""
        record = ObservationRecord(
            task="Poprawny",
            expected="ok",
            observed="ok",
            confidence=0.9,
        )
        result = Evaluator.evaluate(record)
        assert result.metrics_summary["improvement_hypothesis"] is None

    def test_evaluation_result_to_dict(self):
        """Wynik ewaluacji zawiera wszystkie pola."""
        record = ObservationRecord(
            task="Test dict",
            expected=1,
            observed=1,
            confidence=0.85,
        )
        result = Evaluator.evaluate(record)
        d = result.to_dict()
        required_keys = {
            "observation_id", "correctness", "confidence",
            "confidence_level", "contradiction_status",
            "epistemic_summary", "recommendation",
            "can_promote", "regression_detected", "metrics_summary",
        }
        assert required_keys.issubset(d.keys())

    def test_epistemic_summary_in_result(self):
        """Wynik ewaluacji zawiera podsumowanie epistemiczne."""
        record = ObservationRecord(
            task="Epistemic test",
            expected="A",
            observed="A",
            confidence=0.95,
        )
        result = Evaluator.evaluate(record)
        assert len(result.epistemic_summary) > 0
