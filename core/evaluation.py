"""
ArtiCore Open Qdot — Moduł Oceny v0.3

Evaluator: porównuje expected vs observed, generuje rekomendację,
oblicza metryki jakości i decyduje czy zmiana może być promowana.

Zasady:
- Nie nagradzać pewności samej w sobie — pewność musi być powiązana z jakością dowodów.
- Każda zmiana musi posiadać powód i wynik testu.
- Zmiana produkcyjna musi być odwracalna, gdy technicznie możliwe.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .observation import ObservationRecord, ContradictionStatus, ConfidenceLevel


@dataclass
class EvaluationResult:
    """Wynik oceny rekordu obserwacji."""

    observation_id: str
    correctness: bool
    confidence: float
    confidence_level: str
    contradiction_status: str
    epistemic_summary: str
    recommendation: str
    can_promote: bool = False
    regression_detected: bool = False
    metrics_summary: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "observation_id": self.observation_id,
            "correctness": self.correctness,
            "confidence": self.confidence,
            "confidence_level": self.confidence_level,
            "contradiction_status": self.contradiction_status,
            "epistemic_summary": self.epistemic_summary,
            "recommendation": self.recommendation,
            "can_promote": self.can_promote,
            "regression_detected": self.regression_detected,
            "metrics_summary": self.metrics_summary,
        }


class Evaluator:
    """
    Ocena jakości działania systemu.

    Odpowiada na cztery pytania (z 22_SELF_OBSERVATION_AND_IMPROVEMENT.md):
    1. Czy wynik był poprawny?
    2. Czy sposób działania był efektywny?
    3. Czy wystąpiły błędy lub ryzyka?
    4. Czy istnieje wiarygodna hipoteza poprawy?
    """

    # Progi decyzyjne — jawne, mierzalne, wersjonowane
    PROMOTE_CONFIDENCE_THRESHOLD = 0.7
    REGRESSION_CONFIDENCE_THRESHOLD = 0.6

    @staticmethod
    def evaluate(record: ObservationRecord) -> EvaluationResult:
        correctness = record.expected == record.observed
        has_errors = len(record.errors) > 0

        # Detekcja regresji: wynik różny od oczekiwanego przy wysokiej pewności
        regression_detected = (
            not correctness
            and record.confidence >= Evaluator.REGRESSION_CONFIDENCE_THRESHOLD
        )

        # Czy zmiana może być promowana?
        can_promote = (
            correctness
            and not has_errors
            and record.confidence >= Evaluator.PROMOTE_CONFIDENCE_THRESHOLD
            and record.contradiction_status == ContradictionStatus.CLEAR
        )

        # Rekomendacja
        if record.contradiction_status == ContradictionStatus.CONTRADICTORY:
            recommendation = "Wykryto sprzeczność. Wykonaj rollback. Nie promuj zmiany."
        elif record.contradiction_status == ContradictionStatus.INSUFFICIENT:
            recommendation = "Niewystarczające dane. Zbierz więcej dowodów przed decyzją."
        elif record.contradiction_status == ContradictionStatus.UNKNOWN:
            recommendation = "Poziom niepewności zbyt wysoki. Nie podejmuj decyzji."
        elif correctness and not has_errors:
            recommendation = "Wynik zgodny. Można rozważyć promocję po testach regresyjnych."
        elif regression_detected:
            recommendation = "Wykryto regresję. Zmień hipotezę lub odrzuć zmianę."
        else:
            recommendation = "Wyniki różnią się, ale pewność jest umiarkowana. Zbadaj szczegóły."

        # Hipoteza poprawy
        improvement_hypothesis = None
        if not correctness and record.confidence >= 0.3:
            improvement_hypothesis = (
                f"Rozbieżność między expected ({record.expected}) a observed ({record.observed}). "
                "Zaproponuj zmianę i przetestuj w sandboxie."
            )

        metrics_summary = {
            "correctness": correctness,
            "has_errors": has_errors,
            "error_count": len(record.errors),
            "regression_detected": regression_detected,
            "can_promote": can_promote,
            "improvement_hypothesis": improvement_hypothesis,
        }

        return EvaluationResult(
            observation_id=record.observation_id,
            correctness=correctness,
            confidence=record.confidence,
            confidence_level=record.confidence_level.value,
            contradiction_status=record.contradiction_status.value,
            epistemic_summary=record.epistemic_summary(),
            recommendation=recommendation,
            can_promote=can_promote,
            regression_detected=regression_detected,
            metrics_summary=metrics_summary,
        )
