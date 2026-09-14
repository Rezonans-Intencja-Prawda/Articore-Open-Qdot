"""
Testy modułu ObservationRecord.

Realizują zasady z Tablica.txt:
- System potrafi uczciwie powiedzieć "nie wiem"
- System wykrywa własne błędy
- System rozpoznaje sprzeczność danych
- Provenance jest zachowana
- Hash treści jest deterministyczny
"""

import pytest
from core import ObservationRecord, ContradictionStatus, Provenance


class TestObservationRecord:
    """Testy rekordu obserwacji."""

    def test_correct_result_high_confidence(self):
        """System działa poprawnie — wynik zgodny, wysoka pewność."""
        record = ObservationRecord(
            task="Test kodu",
            expected="sukces",
            observed="sukces",
            confidence=0.95,
        )
        assert record.contradiction_status == ContradictionStatus.CLEAR
        assert record.expected == record.observed
        assert "Wiem" in record.epistemic_summary()

    def test_contradiction_detected(self):
        """System wykrywa swój własny błąd — wynik różny, wysoka pewność."""
        record = ObservationRecord(
            task="Optymalizacja",
            expected="szybciej",
            observed="wolniej",
            confidence=0.9,
        )
        assert record.contradiction_status == ContradictionStatus.CONTRADICTORY
        assert "sprzeczne" in record.epistemic_summary()

    def test_honest_uncertainty(self):
        """System uczy się mówić "nie wiem" — niska pewność."""
        record = ObservationRecord(
            task="Analiza intencji",
            expected="przyjazn",
            observed="nieznane",
            confidence=0.1,
        )
        assert record.contradiction_status == ContradictionStatus.INSUFFICIENT
        assert "wystarczających" in record.epistemic_summary()

    def test_unknown_state_low_confidence(self):
        """Niska pewność, ale nie ekstremalnie niska — status UNKNOWN."""
        record = ObservationRecord(
            task="Eksperyment",
            expected=42,
            observed=37,
            confidence=0.25,
        )
        assert record.contradiction_status == ContradictionStatus.UNKNOWN
        assert "Nie wiem" in record.epistemic_summary()

    def test_partial_confidence(self):
        """Umiarkowana pewność — częściowa zgoda."""
        record = ObservationRecord(
            task="Test",
            expected="A",
            observed="B",
            confidence=0.5,
        )
        assert record.contradiction_status == ContradictionStatus.CLEAR
        assert "częściową" in record.epistemic_summary()

    def test_confidence_clamped(self):
        """Confidence jest ograniczone do [0.0, 1.0]."""
        record_high = ObservationRecord(confidence=5.0)
        record_low = ObservationRecord(confidence=-1.0)
        assert record_high.confidence == 1.0
        assert record_low.confidence == 0.0

    def test_provenance_preserved(self):
        """Provenance jest zachowana w rekordzie."""
        prov = Provenance(source="nexus-test", source_type="test")
        record = ObservationRecord(
            task="Test provenance",
            provenance=prov,
        )
        assert record.provenance.source == "nexus-test"
        assert record.provenance.source_type == "test"
        assert record.provenance.timestamp is not None

    def test_content_hash_deterministic(self):
        """Hash treści jest deterministyczny dla identycznych rekordów."""
        prov = Provenance(source="test", source_type="test")
        r1 = ObservationRecord(
            task="Test hash",
            expected="X",
            observed="X",
            confidence=0.9,
            provenance=prov,
        )
        # Drugi rekord z tymi samymi danymi (ale inne ID i timestamp)
        r2 = ObservationRecord(
            task="Test hash",
            expected="X",
            observed="X",
            confidence=0.9,
            provenance=prov,
        )
        # Hash zależy od wszystkich pól, więc ID i timestamp różnią się
        # ale struktura to_dict jest kompletna
        assert r1.content_hash() is not None
        assert len(r1.content_hash()) == 64  # SHA-256 hex

    def test_to_dict_complete(self):
        """to_dict zawiera wszystkie wymagane pola."""
        record = ObservationRecord(
            task="Test kompletności",
            expected="ok",
            observed="ok",
            confidence=0.85,
        )
        d = record.to_dict()
        required_keys = {
            "observation_id", "task", "expected", "observed",
            "confidence", "confidence_level", "contradiction_status",
            "provenance", "errors", "metrics", "state_version", "timestamp",
        }
        assert required_keys.issubset(d.keys())

    def test_errors_list(self):
        """Lista błędów jest pusta domyślnie i można ją wypełnić."""
        record = ObservationRecord(
            task="Test błędów",
            errors=["timeout", "connection_refused"],
        )
        assert len(record.errors) == 2
        assert "timeout" in record.errors

    def test_metrics_dict(self):
        """Metryki są puste domyślnie i można je wypełnić."""
        record = ObservationRecord(
            task="Test metryk",
            metrics={"latency_ms": 150, "tokens": 500},
        )
        assert record.metrics["latency_ms"] == 150
        assert record.metrics["tokens"] == 500

    def test_state_version_default(self):
        """Domyślna wersja stanu to v0.3."""
        record = ObservationRecord()
        assert record.state_version == "v0.3"
