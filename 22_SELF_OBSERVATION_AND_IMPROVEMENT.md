# ArtiCore — Self-Observation & Controlled Self-Improvement

## Cel

Zdefiniować bezpieczną, mierzalną pętlę samodoskonalenia. ArtiCore ma móc wykrywać własne ograniczenia, proponować ulepszenia i sprawdzać ich skuteczność bez zakładania, że posiada świadomość.

## 1. Self-observation

Agent rejestruje:

- zadanie i kontekst,
- wybrane działanie,
- wynik,
- niepewność,
- wykryte błędy,
- przewidywany rezultat,
- rzeczywisty rezultat,
- koszt i czas,
- zgodność z ograniczeniami i wartościami.

Minimalny rekord:

```yaml
observation:
  task_id:
  state_version:
  action:
  expected:
  observed:
  uncertainty:
  errors: []
  metrics: {}
  timestamp:
```

## 2. Meta-evaluation

Evaluator odpowiada na cztery pytania:

1. Czy wynik był poprawny?
2. Czy sposób działania był efektywny?
3. Czy wystąpiły błędy lub ryzyka?
4. Czy istnieje wiarygodna hipoteza poprawy?

## 3. Hipoteza zmiany

Każda propozycja ulepszenia musi zawierać:

```yaml
proposal:
  target:
  rationale:
  expected_gain:
  risks: []
  affected_components: []
  rollback_plan:
```

## 4. Sandbox

Zmiana jest testowana poza stanem produkcyjnym. Sandbox powinien umożliwiać powtarzalne uruchomienie benchmarków i testów bezpieczeństwa.

## 5. Kryteria akceptacji

Zmiana może zostać zaakceptowana, gdy:

- poprawia zdefiniowaną metrykę,
- nie powoduje nieakceptowalnej regresji,
- przechodzi testy bezpieczeństwa,
- posiada ślad pochodzenia i wersję,
- można odtworzyć wynik eksperymentu.

## 6. Rollback

Każda zaakceptowana zmiana otrzymuje identyfikator wersji oraz punkt powrotu. W razie regresji poprzedni stan może zostać przywrócony.

## 7. Granica samomodyfikacji

W v0.2 ArtiCore może proponować zmiany kodu i konfiguracji, ale nie powinien samodzielnie usuwać mechanizmów weryfikacji, śladów zmian, ograniczeń bezpieczeństwa ani możliwości rollbacku.

## 8. Recursive improvement

Dopiero po uzyskaniu stabilnej pętli:

`observe → evaluate → propose → sandbox → verify → version`

można badać wielopoziomową rekurencję:

`system → obserwuje własną pętlę → ulepsza obserwację → testuje ulepszenie → obserwuje nową pętlę`.

## 9. ASI research boundary

Zdolność samodoskonalenia nie jest równoznaczna z AGI ani ASI. ArtiCore traktuje je jako obszary badawcze wymagające empirycznej oceny zdolności, generalizacji, autonomii poznawczej i kontroli ryzyka.
