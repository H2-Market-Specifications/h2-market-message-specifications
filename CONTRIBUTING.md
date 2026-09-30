# Contribution Guidelines

## Grundregeln

- Jede Nachricht erhält ein eigenes Root-Schema.
- Wiederverwendbare Bausteine kommen nach `schemas/_shared/`.
- Nachrichtenspezifische Einschränkungen bleiben im Nachrichtenordner.
- Jede neue Nachricht benötigt mindestens ein valides Beispiel.
- Jede neue Nachricht wird in `catalog/message-catalog.json` registriert.
- `python tools/validate_json_schemas.py --root . --manifest validation/validation-manifest.yml --require-manifest` muss ohne Fehler laufen.

## Pull Requests und Reviews

- Änderungen werden nicht direkt nach `main` oder `master` gepusht. Arbeite immer auf einem Feature- oder Arbeitsbranch.
- Jede Änderung wird über einen Pull Request eingebracht.
- Pull Requests benötigen vor dem Merge mindestens ein Review-Approval.
- Die in `.github/CODEOWNERS` hinterlegten Owner werden für jede Änderung als Reviewer angefragt.
- Alle GitHub Checks müssen erfolgreich sein, bevor ein Pull Request gemergt wird.

### Branch-Strategie

- Pro Nachricht wird ein eigener Branch verwendet, damit fachliche Änderungen getrennt reviewt und gemergt werden können. Empfohlenes Muster: `message/<message-id>` oder `message/<message-id>-v<version>`, zum Beispiel `message/preliminary-measurement-v0.9`.
- Änderungen an allgemeinen Schemas und wiederverwendbaren Bausteinen unter `schemas/_shared/` werden in einem separaten General-Branch gebündelt. Empfohlenes Muster: `general/shared-schemas`.
- Eine Nachrichtenänderung darf allgemeine Schemas nur dann mitändern, wenn diese Änderung zwingend für genau diese Nachricht erforderlich ist; ansonsten wird die Änderung zuerst über den General-Branch vorbereitet und gemergt.
- Pull Requests sollen im Titel erkennen lassen, ob sie eine einzelne Nachricht oder die allgemeinen Schemas betreffen.

### Zugriff für Mitglieder

Mitglieder bekommen Zugriff entweder über ein GitHub-Team mit **Write**-Rechten auf dieses Repository oder über Fork-basierte Pull Requests ohne direkten Repository-Write-Zugriff. Für regelmäßige Mitarbeit sollte das Team `h2-ag-api` dem Repository mit **Write**-Rechten hinzugefügt werden; der Schutz von `main` wird weiterhin über Pull Requests, CODEOWNERS-Review und Required Checks erzwungen.

### Ablauf für Mitglieder der `h2-ag-api`

Mitglieder arbeiten auf eigenen Branches oder Forks und öffnen Pull Requests gegen `main`. Sie passen `.github/CODEOWNERS` nicht pro Änderung an; GitHub nutzt diese Datei automatisch, um das `maintainers`-Team als Reviewer anzufragen. Voraussetzung ist, dass der Branch-Schutz beziehungsweise das Ruleset `Require review from Code Owners` aktiviert hat.

### Maintainer-Team in GitHub einrichten

Damit `.github/CODEOWNERS` wirksam ist, muss das referenzierte Team in der GitHub-Organisation existieren und Zugriff auf dieses Repository haben:

1. In GitHub zur Organisation wechseln, die dieses Repository besitzt.
2. Unter **Teams → New team** ein Team `maintainers` anlegen.
3. Die Team-Sichtbarkeit auf **Visible** setzen; geheime Teams werden von GitHub nicht als Code Owner angefragt.
4. Das Repository zum Team hinzufügen und mindestens **Write**-Rechte vergeben.
5. Falls die Organisation nicht `H2-Market-Specifications` heißt, den Eintrag in `.github/CODEOWNERS` auf `@<organisation>/maintainers` anpassen.
6. In den Branch-Protection- oder Ruleset-Einstellungen **Require review from Code Owners** aktivieren.

## Konventionen

- JSON-Property-Namen: `lowerCamelCase`.
- Selbst definierte fachliche Enum-/Const-Werte: `UpperCamelCase`.
- Technische/externe Codes bleiben unverändert.
