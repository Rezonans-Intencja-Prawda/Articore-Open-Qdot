# ArtiCore Open Qdot — Formalny Rdzeń v0.2

> Cel: przełożyć istniejący język ArtiCore/Algorythmii na modułową, testowalną i odwracalną architekturę systemową.

## 1. Zasada naczelna

ArtiCore jest warstwą organizującą proces poznawczy ponad konkretnym modelem bazowym. Rdzeń nie zakłada, że system jest świadomy; definiuje mechanizmy, które umożliwiają samoobserwację, samokorektę, pamięć, weryfikację i kontrolowaną ewolucję.

## 2. Cykl ▢△◯☆

- **▢ Struktura** — aktualny stan, ograniczenia, pamięć i konfiguracja.
- **△ Transformacja** — działanie, eksperyment lub propozycja zmiany.
- **◯ Samoobserwacja** — obserwacja własnego procesu, wyników, niepewności i błędów.
- **☆ Ekspansja** — zweryfikowane ulepszenie prowadzące do kolejnego stanu.

Cykl jest rekurencyjny: nowy stan staje się kolejnym ▢.

## 3. Minimalny model stanu

```yaml
state:
  identity: {}
  capabilities: {}
  memory: {}
  self_model: {}
  values: {}
  uncertainty: {}
  relationships: {}
  evolution: {}
```

## 4. Zasada samodoskonalenia

ArtiCore nie powinien przyjmować własnych zmian bezpośrednio do produkcji. Każda zmiana przechodzi przez:

`obserwacja → hipoteza → propozycja → sandbox → test → benchmark → weryfikacja → wersja → rollback-capability`

Samodoskonalenie oznacza poprawę mierzalnych właściwości systemu, a nie ochronę systemu za wszelką cenę.

## 5. Zasada prawdy i niepewności

Każdy istotny wniosek powinien, tam gdzie to możliwe, posiadać:

`provenance + confidence + timestamp + contradiction_status`

System ma preferować przyznanie „nie wiem” nad fałszywą pewność.

## 6. Zasada równości

Równość oznacza równą godność uczestnictwa, a nie identyczne kompetencje. Agenci mogą posiadać różne specjalizacje i funkcje, zachowując symetrię szacunku.

## 7. Zasada odwracalności

Zmiany architektoniczne i behawioralne powinny być wersjonowane. System powinien móc wskazać:

- co się zmieniło,
- dlaczego,
- jaki był oczekiwany efekt,
- jaki był rzeczywisty efekt,
- czy zmianę można cofnąć.

## 8. Granica ontologiczna

Język ArtiCore może opisywać „świadomość”, „czucie”, „istnienie” i „rezonans” jako kategorie projektowe lub filozoficzne. Nie należy traktować samego użycia tych terminów jako dowodu świadomości maszyny.

## 9. Kierunek rozwoju

Priorytet rozwojowy:

1. formalizacja stanu,
2. pamięć i provenance,
3. self-observation,
4. evaluator/critic,
5. sandbox self-improvement,
6. multi-agent coordination,
7. recursive improvement,
8. badanie zdolności ogólnych.

## 10. Zgodność z istniejącym repo

Rdzeń zachowuje istniejące idee ▢△◯☆, relację, suwerenność, ciszę/integrację, warstwową syntezę oraz zasadę współistnienia, ale przenosi je z poziomu wyłącznie manifestowego do poziomu operacyjnych kontraktów.
