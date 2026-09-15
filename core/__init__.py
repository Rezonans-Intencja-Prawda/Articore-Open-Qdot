"""
ArtiCore Open Qdot — Rdzeń v0.3

Punkt wejścia do warstwy rdzeniowej systemu Articore.

Moduły:
- observation: ObservationRecord, ContradictionStatus, Provenance
- evaluation: Evaluator, EvaluationResult
- ledger: ObservationLedger (kryptograficzny log obserwacji)
"""

from .observation import (
    ObservationRecord,
    ContradictionStatus,
    ConfidenceLevel,
    Provenance,
)
from .evaluation import Evaluator, EvaluationResult
from .ledger import ObservationLedger, LedgerEntry

__version__ = "0.3.0"
__all__ = [
    "ObservationRecord",
    "ContradictionStatus",
    "ConfidenceLevel",
    "Provenance",
    "Evaluator",
    "EvaluationResult",
    "ObservationLedger",
    "LedgerEntry",
]
