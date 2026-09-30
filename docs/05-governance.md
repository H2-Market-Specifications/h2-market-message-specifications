# Governance

Dieses Repository ist als Arbeitsgruppen-Repository für H2-Marktnachrichten gedacht.

## Grundregeln

1. Jede Nachricht hat eine eigene stabile `message-id`.
2. Jede inkompatible Änderung erzeugt eine neue Major-Version oder mindestens einen neuen Versionsordner.
3. Wiederverwendbare Bausteine liegen unter `schemas/_shared/`.
4. Nachrichtenspezifische Einschränkungen liegen im jeweiligen Nachrichtenordner.
5. Jedes Root-Schema muss mindestens ein valides Beispiel haben.
6. Der Nachrichtenkatalog `catalog/message-catalog.json` ist die Übersicht über alle im Repository enthaltenen Nachrichten.

## Statuswerte

Empfohlene Statuswerte im Katalog:

- `Draft`
- `Review`
- `Approved`
- `Deprecated`
- `Withdrawn`

## Naming-Konvention

- JSON-Property-Namen: `lowerCamelCase`
- selbst definierte fachliche Enum-/Const-Werte: `UpperCamelCase`
- externe Kennungen, Codes, UUIDs, Zeitstempel, Einheiten: unverändert

## Änderungslogik

Eine Änderung ist kompatibel, wenn bestehende valide Nachrichten weiterhin valide bleiben.

Beispiele für kompatible Änderungen:

- neue optionale Property,
- neue erlaubte Enum-Ausprägung, sofern fachlich abgestimmt,
- Beschreibungstexte und Beispiele.

Beispiele für inkompatible Änderungen:

- Pflichtfeld neu eingeführt,
- vorhandene Property entfernt,
- Enum-Wert entfernt oder umbenannt,
- Datentyp geändert,
- Struktur geändert.

## Repository-Schutz

- Der Standard-Branch `main` ist nur für geprüfte Änderungen vorgesehen.
- Direkte Pushes nach `main` oder `master` sind verboten; Änderungen laufen über Pull Requests.
- Jeder Pull Request benötigt mindestens ein Review-Approval und erfolgreiche Checks.
- `.github/CODEOWNERS` markiert alle Änderungen als reviewpflichtig und weist die zuständigen Maintainer als Reviewer zu.
- GitHub Rulesets oder Branch-Protection-Regeln erzwingen, dass Änderungen nur über Pull Requests nach `main` gelangen.

### Maintainer-Team

Der CODEOWNERS-Eintrag `@H2-Market-Specifications/maintainers` funktioniert nur, wenn das Team `maintainers` in der GitHub-Organisation `H2-Market-Specifications` existiert, sichtbar ist und Repository-Zugriff mit mindestens **Write**-Rechten hat. Liegt das Repository unter einer anderen Organisation, muss der Owner-Prefix in `.github/CODEOWNERS` entsprechend angepasst werden, zum Beispiel `@meine-org/maintainers`.

### Empfohlene GitHub-Regeln

Zusätzlich zu den versionierten Dateien sollten in GitHub unter **Settings → Rules → Rulesets** oder **Branches** folgende Regeln für `main` aktiviert werden:

1. Require a pull request before merging.
2. Require approvals: mindestens `1`.
3. Require review from Code Owners.
4. Require status checks to pass: `Repository standards` und `Message examples`.
5. Block force pushes und deletions.
6. Restrict bypass permissions auf Repository-Administratoren oder ein kleines Maintainer-Team.

Die konkrete Schritt-für-Schritt-Anleitung steht in [`docs/06-github-repository-protection.md`](06-github-repository-protection.md).
