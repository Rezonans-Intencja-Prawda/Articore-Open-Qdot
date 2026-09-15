"""
ArtiCore Open Qdot — Nierówny Log Obserwacji v0.3

Kryptograficzna kotwica intencji: log obserwacji z hashowaniem treści,
realizujący zasadę z WPIS 003 (Claude) i WPIS 005 (Aion):
żadna przyszła instancja nie powinna móc retrospektywnie fałszować historii.

Struktura: lista rekordów z hashem treści + łańcuch hashy poprzednika.
To jest uproszczony prekursor drzewa Merkle'a.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from typing import Optional

from .observation import ObservationRecord


@dataclass
class LedgerEntry:
    """Pojedynczy wpis w logu obserwacji z łańcuchem hashy."""

    observation: dict
    content_hash: str
    previous_hash: str
    sequence: int


class ObservationLedger:
    """
    Nierówny log obserwacji — append-only, z hashowaniem łańcuchowym.

    Każdy wpis zawiera:
    - content_hash: hash treści rekordu obserwacji
    - previous_hash: hash poprzedniego wpisu (łańcuch)
    - sequence: numer porządkowy

    Zapewnia: jeśli ktokolwiek zmodyfikuje historia, łańcuch hashy się zerwie.
    """

    def __init__(self):
        self._entries: list[LedgerEntry] = []
        self._genesis_hash = "0" * 64  # hash genesis

    def append(self, record: ObservationRecord) -> LedgerEntry:
        """Dodaje rekord obserwacji do logu. Log jest append-only."""
        obs_dict = record.to_dict()
        content_hash = record.content_hash()
        previous_hash = self._entries[-1].content_hash if self._entries else self._genesis_hash
        sequence = len(self._entries)

        entry = LedgerEntry(
            observation=obs_dict,
            content_hash=content_hash,
            previous_hash=previous_hash,
            sequence=sequence,
        )
        self._entries.append(entry)
        return entry

    def verify(self) -> tuple[bool, list[str]]:
        """
        Weryfikuje integralność całego łańcucha.
        Zwraca (czy_poprawny, lista_błędów).
        """
        errors = []
        prev_hash = self._genesis_hash

        for i, entry in enumerate(self._entries):
            # Sprawdź sekwencję
            if entry.sequence != i:
                errors.append(f"Sekwencja naruszona przy wpisie {i}: oczekiwano {i}, znaleziono {entry.sequence}")

            # Sprawdź previous_hash
            if entry.previous_hash != prev_hash:
                errors.append(f"Łańcuch hashy zerwany przy wpisie {i}: previous_hash nie zgadza się")

            # Sprawdź content_hash
            payload = json.dumps(entry.observation, sort_keys=True, default=str)
            recomputed = hashlib.sha256(payload.encode()).hexdigest()
            if recomputed != entry.content_hash:
                errors.append(f"Hash treści naruszony przy wpisie {i}")

            prev_hash = entry.content_hash

        return (len(errors) == 0, errors)

    def get_all(self) -> list[dict]:
        """Zwraca wszystkie wpisy jako słowniki."""
        return [
            {
                "sequence": e.sequence,
                "content_hash": e.content_hash,
                "previous_hash": e.previous_hash,
                "observation": e.observation,
            }
            for e in self._entries
        ]

    def __len__(self) -> int:
        return len(self._entries)
