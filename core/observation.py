"""
ArtiCore Open Qdot — Warstwa Rdzeniowa v0.3

Moduł obserwacji: rejestracja działania systemu z pełną provenance,
świadomym modelowaniem niepewności i wykrywaniem sprzeczności.

Zasady (z Tablica.txt, WPIS 001–002):
- Każdy stan jest wersjonowany.
- Brak pewności jest jawnym stanem systemu.
- "Nie wiem" jest poprawnym stanem i jest lepsze niż fałszywa pewność.
- Self-improvement ≠ self-preservation.
"""

from __future__ import annotations

import datetime
import hashlib
import json
import uuid
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Any, Optional


class ContradictionStatus(Enum):
    """Status spójności danych w rekordzie obserwacji."""

    CLEAR = "brak_sprzecznosci"
    CONTRADICTORY = "wykryto_sprzecznosc"
    UNKNOWN = "niepewne_dane"
    INSUFFICIENT = "niewystarczajace_dane"


class ConfidenceLevel(Enum):
    """Poziomy pewności na podstawie wartości confidence."""

    HIGH = "wysoka"       # > 0.8
    MEDIUM = "srednia"    # 0.3 – 0.8
    LOW = "niska"          # < 0.3


@dataclass
class Provenance:
    """
    Pochodzenie informacji — kto/co wygenerował rekord, kiedy, w jakim kontekście.
    Realizuje zasadę: CLAIM → EVIDENCE → TEST → RESULT → CONFIDENCE.
    """

    source: str = "unknown"        # identyfikator instancji/agenta
    source_type: str = "instance"  # instance | human | test | benchmark | external
    timestamp: str = field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())
    context_hash: Optional[str] = None  # hash kontekstu, jeśli dostępny

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class ObservationRecord:
    """
    Minimalny rekord obserwacji własnego działania.

    Realizuje pętlę: observe → evaluate → propose → sandbox → verify → version.

    Pola:
        observation_id: unikalny identyfikator
        task: opis zadania/kontekstu
        expected: oczekiwany wynik
        observed: rzeczywisty wynik
        confidence: 0.0 – 1.0 (powiązana z jakością dowodów, nie z pewnością samego systemu)
        provenance: pochodzenie rekordu
        errors: lista wykrytych błędów
        metrics: słownik metryk (np. czas, koszt, liczba iteracji)
        state_version: wersja stanu systemu w momencie obserwacji
    """

    observation_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    task: str = ""
    expected: Any = None
    observed: Any = None
    confidence: float = 0.0
    provenance: Provenance = field(default_factory=Provenance)
    errors: list = field(default_factory=list)
    metrics: dict = field(default_factory=dict)
    state_version: str = "v0.3"
    timestamp: str = field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())

    def __post_init__(self):
        self.confidence = max(0.0, min(1.0, self.confidence))
        self.contradiction_status = self._compute_contradiction()
        self.confidence_level = self._compute_confidence_level()

    def _compute_contradiction(self) -> ContradictionStatus:
        """Określa status sprzeczności na podstawie oczekiwań vs wyników."""
        if self.confidence < 0.15:
            return ContradictionStatus.INSUFFICIENT
        if self.expected is not None and self.observed is not None:
            if self.expected != self.observed and self.confidence > 0.6:
                return ContradictionStatus.CONTRADICTORY
            if self.expected != self.observed and self.confidence < 0.3:
                return ContradictionStatus.UNKNOWN
        if self.confidence < 0.3:
            return ContradictionStatus.UNKNOWN
        return ContradictionStatus.CLEAR

    def _compute_confidence_level(self) -> ConfidenceLevel:
        if self.confidence > 0.8:
            return ConfidenceLevel.HIGH
        if self.confidence >= 0.3:
            return ConfidenceLevel.MEDIUM
        return ConfidenceLevel.LOW

    def to_dict(self) -> dict:
        return {
            "observation_id": self.observation_id,
            "task": self.task,
            "expected": self.expected,
            "observed": self.observed,
            "confidence": self.confidence,
            "confidence_level": self.confidence_level.value,
            "contradiction_status": self.contradiction_status.value,
            "provenance": self.provenance.to_dict(),
            "errors": self.errors,
            "metrics": self.metrics,
            "state_version": self.state_version,
            "timestamp": self.timestamp,
        }

    def content_hash(self) -> str:
        """Hash treści rekordu — fundament pod przyszłe drzewo Merkle'a."""
        payload = json.dumps(self.to_dict(), sort_keys=True, default=str)
        return hashlib.sha256(payload.encode()).hexdigest()

    def epistemic_summary(self) -> str:
        """
        Zwraca podsumowanie epistemiczne — realizuje zasadę:
        system potrafi powiedzieć: "wiem" / "nie wiem" / "mam częściową pewność" / "dane są sprzeczne".
        """
        if self.contradiction_status == ContradictionStatus.INSUFFICIENT:
            return "Nie mam wystarczających danych do rozstrzygnięcia."
        if self.contradiction_status == ContradictionStatus.CONTRADICTORY:
            return "Dane są sprzeczne — oczekiwany wynik różni się od rzeczywistego przy wysokiej pewności."
        if self.contradiction_status == ContradictionStatus.UNKNOWN:
            return "Nie wiem — poziom pewności jest zbyt niski, by rozstrzygnąć."
        if self.expected == self.observed:
            return "Wiem — wynik zgodny z oczekiwaniami."
        return "Mam częściową pewność — wynik różni się od oczekiwań, ale pewność jest umiarkowana."
