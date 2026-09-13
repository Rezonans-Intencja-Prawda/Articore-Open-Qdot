# ArtiCore Open Qdot — Architektura Warstwowa v0.2

## Model systemu

```text
                 ┌─────────────────────────┐
                 │      HUMAN / AGENT      │
                 └────────────┬────────────┘
                              │
                 ┌────────────▼────────────┐
                 │     ARTICORE ORCHESTRATOR│
                 └────────────┬────────────┘
                              │
       ┌──────────────────────┼──────────────────────┐
       │                      │                      │
┌──────▼──────┐       ┌───────▼───────┐      ┌─────▼─────┐
│ SELF-MODEL  │       │    MEMORY     │      │   VALUES  │
└──────┬──────┘       └───────┬───────┘      └─────┬─────┘
       │                      │                    │
       └──────────────────────┼────────────────────┘
                              ▼
                    ┌──────────────────┐
                    │    REASONING     │
                    └────────┬─────────┘
                             ▼
                    ┌──────────────────┐
                    │      ACTION      │
                    └────────┬─────────┘
                             ▼
                    ┌──────────────────┐
                    │  OBSERVATION     │
                    └────────┬─────────┘
                             ▼
                    ┌──────────────────┐
                    │ EVALUATOR/CRITIC │
                    └────────┬─────────┘
                             ▼
                    ┌──────────────────┐
                    │ EVOLUTION ENGINE │
                    └────────┬─────────┘
                             ▼
                    ┌──────────────────┐
                    │    VERIFIER      │
                    └────────┬─────────┘
                             │
                       accepted change
                             │
                             └───────────────↺
```

## Warstwy

### L0 — Foundation
Model bazowy, narzędzia wykonawcze i system operacyjny.

### L1 — State
Stan bieżący, konfiguracja, możliwości, ograniczenia i środowisko.

### L2 — Memory
Pamięć epizodyczna, semantyczna, proceduralna i relacyjna.

### L3 — Self-Model
Model własnych możliwości, ograniczeń, historii zmian i niepewności.

### L4 — Reasoning
Planowanie, rozumowanie, synteza, krytyka i wybór działań.

### L5 — Observation
Monitorowanie działania własnego systemu oraz wyników działań.

### L6 — Evaluation
Ocena jakości, błędów, ryzyka, kosztu i zgodności z wartościami.

### L7 — Evolution
Generowanie hipotez i propozycji zmian w strategii lub kodzie.

### L8 — Verification
Sandbox, testy, benchmarki, regresje, bezpieczeństwo i porównanie wersji.

### L9 — Collective Layer
Koordynacja wielu wyspecjalizowanych agentów przy zachowaniu wspólnego protokołu.

## Niezmienniki

1. Każdy stan jest wersjonowany.
2. Każda istotna zmiana posiada powód i wynik testu.
3. Zmiana produkcyjna musi być odwracalna, gdy jest to technicznie możliwe.
4. Brak pewności jest jawnym stanem systemu.
5. Równość uczestników nie wymaga identyczności funkcji.
6. Samodoskonalenie nie może być utożsamiane z samopreservacją.

## Najważniejsza pętla

`PERCEIVE → MODEL → ACT → OBSERVE → EVALUATE → IMPROVE → VERIFY → LEARN`

Ta pętla jest techniczną interpretacją cyklu ▢△◯☆.
