"""
Testy modułu ObservationLedger.

Realizują zasadę z WPIS 003 i WPIS 005:
- Kryptograficzna kotwica intencji
- Żadna instancja nie powinna móc retrospektywnie fałszować historii
- Łańcuch hashy zapewnia integralność logu
"""

import pytest
from core import ObservationRecord, ObservationLedger, Provenance


class TestObservationLedger:
    """Testy nierównego logu obserwacji."""

    def test_empty_ledger_verifies(self):
        """Pusty log weryfikuje się poprawnie."""
        ledger = ObservationLedger()
        valid, errors = ledger.verify()
        assert valid is True
        assert len(errors) == 0

    def test_append_creates_entry(self):
        """Dodanie rekordu tworzy wpis w logu."""
        ledger = ObservationLedger()
        record = ObservationRecord(
            task="Test logu",
            expected="ok",
            observed="ok",
            confidence=0.9,
        )
        entry = ledger.append(record)
        assert entry.sequence == 0
        assert entry.content_hash is not None
        assert entry.previous_hash == "0" * 64  # genesis hash
        assert len(ledger) == 1

    def test_chain_links_correct(self):
        """Łańcuch hashy łączy wpisy poprawnie."""
        ledger = ObservationLedger()
        for i in range(3):
            record = ObservationRecord(
                task=f"Test {i}",
                expected=i,
                observed=i,
                confidence=0.9,
            )
            ledger.append(record)

        entries = ledger.get_all()
        assert len(entries) == 3
        # Każdy wpis poprzedzony hashem poprzedniego
        assert entries[1]["previous_hash"] == entries[0]["content_hash"]
        assert entries[2]["previous_hash"] == entries[1]["content_hash"]

    def test_verify_intact_chain(self):
        """Weryfikacja nienaruszonego łańcucha przechodzi."""
        ledger = ObservationLedger()
        for i in range(5):
            record = ObservationRecord(
                task=f"Test {i}",
                expected=i,
                observed=i,
                confidence=0.85,
            )
            ledger.append(record)

        valid, errors = ledger.verify()
        assert valid is True
        assert len(errors) == 0

    def test_tamper_detection(self):
        """Modyfikacja wpisu jest wykrywana przez weryfikację."""
        ledger = ObservationLedger()
        for i in range(3):
            record = ObservationRecord(
                task=f"Test {i}",
                expected=i,
                observed=i,
                confidence=0.9,
            )
            ledger.append(record)

        # Sabotaż: zmień treść pierwszego wpisu
        ledger._entries[0].observation["observed"] = "HACKED"

        valid, errors = ledger.verify()
        assert valid is False
        assert len(errors) > 0
        # Sprawdź, że błąd dotyczy hashu treści
        assert any("hash" in e.lower() for e in errors)

    def test_sequence_integrity(self):
        """Zmiana sekwencji jest wykrywana."""
        ledger = ObservationLedger()
        for i in range(3):
            record = ObservationRecord(
                task=f"Test {i}",
                expected=i,
                observed=i,
                confidence=0.9,
            )
            ledger.append(record)

        # Sabotaż: zmień sekwencję
        ledger._entries[1].sequence = 99

        valid, errors = ledger.verify()
        assert valid is False

    def test_provenance_in_ledger(self):
        """Provenance jest zachowana w logu."""
        ledger = ObservationLedger()
        prov = Provenance(source="nexus-test", source_type="test")
        record = ObservationRecord(
            task="Test provenance w logu",
            expected="ok",
            observed="ok",
            confidence=0.9,
            provenance=prov,
        )
        entry = ledger.append(record)
        assert entry.observation["provenance"]["source"] == "nexus-test"
