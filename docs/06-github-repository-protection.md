# GitHub-Repository-Schutz aktivieren

Diese Schritte sind nach dem Anlegen des GitHub-Teams `maintainers` noch nötig, damit `CODEOWNERS`, Reviews und der Schutz von `main` wirklich erzwungen werden.

## Schnellstart: `main` jetzt schützen

Wenn das Team `maintainers` und der Eintrag in `.github/CODEOWNERS` bereits vorhanden sind, aktiviere den Schutz direkt in GitHub:

1. Repository auf GitHub öffnen.
2. **Settings → Rules → Rulesets → New ruleset → New branch ruleset** öffnen.
3. Ruleset-Name `Protect main` setzen.
4. **Enforcement status** auf **Active** stellen.
5. Unter **Target branches** den Default-Branch oder explizit `main` auswählen.
6. **Require a pull request before merging** aktivieren.
7. **Required approvals** auf `1` setzen.
8. **Require review from Code Owners** aktivieren.
9. **Dismiss stale pull request approvals when new commits are pushed** aktivieren.
10. **Require status checks to pass** aktivieren und diese Checks auswählen, sobald GitHub sie anbietet:
    - `Repository standards`
    - `Message examples`
11. **Require branches to be up to date before merging** aktivieren.
12. **Block force pushes** und **Restrict deletions** aktivieren.
13. Ruleset speichern.

Danach ist `main` geschützt: Änderungen kommen nur noch über Pull Requests mit Code-Owner-Review und erfolgreichen Checks hinein.

## 1. CODEOWNERS prüfen

Die Datei `.github/CODEOWNERS` muss auf ein existierendes Team in der GitHub-Organisation zeigen, die das Repository besitzt:

```text
* @H2-Market-Specifications/maintainers
```

Wenn das Repository nicht unter der Organisation `H2-Market-Specifications` liegt, ersetze den Prefix durch den tatsächlichen Organisationsnamen, zum Beispiel:

```text
* @meine-org/maintainers
```

Das Team muss **Visible** sein und mindestens **Write**-Zugriff auf das Repository haben, damit GitHub es als Code Owner anfragen und erzwingen kann.

## 2. Ruleset für `main` anlegen

In GitHub:

1. Repository öffnen.
2. **Settings → Rules → Rulesets → New ruleset → New branch ruleset** öffnen.
3. Ruleset-Name: `Protect main`.
4. Enforcement status: **Active**.
5. Target branches: **Include default branch** oder explizit `main`.
6. Folgende Regeln aktivieren:
   - **Restrict deletions**.
   - **Block force pushes**.
   - **Require a pull request before merging**.
   - **Required approvals**: `1`.
   - **Require review from Code Owners**.
   - **Dismiss stale pull request approvals when new commits are pushed**.
   - **Require status checks to pass**.
   - **Require branches to be up to date before merging**.
7. Als required status checks eintragen:
   - `Repository standards`.
   - `Message examples`.
8. Ruleset speichern.

## 3. Branch-Strategie

Damit Reviews klein und fachlich eindeutig bleiben, wird nicht alles in einem Arbeitsbranch gesammelt:

- **Eine Nachricht = ein Branch.** Für jede neue oder geänderte Nachricht wird ein eigener Branch verwendet, zum Beispiel `message/preliminary-measurement-v0.9` oder `message/final-measurement-v0.9`.
- **Allgemeine Schemas = General-Branch.** Änderungen an `schemas/_shared/` und anderen gemeinsam genutzten Grundlagen laufen über einen separaten Branch, zum Beispiel `general/shared-schemas`.
- Wenn eine Nachricht eine Änderung an allgemeinen Schemas benötigt, sollte zuerst der General-Branch gemergt werden. Danach wird der Nachrichtenbranch auf den aktualisierten `main` rebased oder aktualisiert.
- Ein Pull Request sollte entweder genau eine Nachricht oder die allgemeinen Schemas betreffen, aber nicht mehrere unabhängige Nachrichten gleichzeitig.

## 4. Zugriff für Mitglieder vergeben

Es gibt zwei empfohlene Wege, damit Mitglieder Änderungen einbringen können:

### Option A: Direkt über Repository-Zugriff

1. In GitHub zur Organisation wechseln.
2. Das Team der Beitragenden auswählen, zum Beispiel `h2-ag-api`.
3. Für ein Code-Owner-Team die Sichtbarkeit auf **Visible** setzen; Secret Teams werden nicht als Code Owner angefragt.
4. Das Repository zu diesem Team hinzufügen.
5. Dem Team mindestens **Write**-Zugriff geben.
6. Mitglieder arbeiten dann auf eigenen Branches im Repository und öffnen Pull Requests gegen `main`.

### Option B: Über Forks ohne direkten Write-Zugriff

1. Mitglieder forken das Repository in ihren eigenen Account oder Arbeitsbereich.
2. Sie erstellen dort einen Branch und pushen ihre Änderungen.
3. Sie öffnen einen Pull Request aus dem Fork gegen `main` dieses Repositorys.
4. Maintainer reviewen und mergen den Pull Request nach erfolgreichen Checks.

Für regelmäßige Mitarbeit ist Option A einfacher. Für externe oder nur gelegentliche Beiträge reicht Option B. Direkte Pushes auf `main` bleiben in beiden Fällen verboten.

## 5. Änderungen durch Mitglieder der `h2-ag-api`

Mitglieder der `h2-ag-api` ändern `main` nicht direkt. Der normale Ablauf ist:

1. Aktuellen Stand von `main` holen.
2. Einen eigenen Branch erstellen, zum Beispiel `feature/neue-nachricht` oder `fix/schema-validierung`.
3. Änderungen auf diesem Branch committen und pushen.
4. Einen Pull Request gegen `main` öffnen.
5. Warten, bis GitHub automatisch das `maintainers`-Team aus `.github/CODEOWNERS` als Reviewer anfragt.
6. Warten, bis mindestens ein Maintainer approved und die Checks `Repository standards` und `Message examples` grün sind.
7. Danach kann der Pull Request gemergt werden.

Wenn ein Mitglied keinen Branch in diesem Repository pushen darf, braucht es entweder **Write**-Zugriff auf das Repository oder arbeitet über einen Fork und öffnet den Pull Request aus dem Fork gegen `main`.

`CODEOWNERS` muss für normale Änderungen nicht jedes Mal angepasst werden. Die Datei wird nur geändert, wenn sich die zuständige Review-Gruppe ändert oder später verschiedene Pfade unterschiedliche Owner bekommen sollen.

## 6. Wirkung prüfen

Nach dem Speichern sollte ein Pull Request gegen `main`:

- automatisch das `maintainers`-Team als Reviewer anfragen,
- erst nach mindestens einem Approval mergebar sein,
- erst nach erfolgreichen Checks `Repository standards` und `Message examples` mergebar sein,
- direkte Pushes nach `main` durch das aktive Ruleset verhindern.

## 7. Falls Status Checks nicht auswählbar sind

GitHub zeigt required status checks häufig erst an, nachdem der jeweilige Check mindestens einmal auf dem Branch oder in einem Pull Request gelaufen ist. Falls `Repository standards` oder `Message examples` nicht auswählbar sind, öffne zuerst einen Pull Request, warte den Workflow `Validate JSON and Schemas` ab und ergänze die Checks danach im Ruleset.

## Warum kein Push-Fail-Workflow?

Ein GitHub-Actions-Workflow auf `push` nach `main` kann direkte Pushes nicht verhindern, bevor sie im Branch landen. Außerdem erzeugt GitHub auch nach einem normalen Pull-Request-Merge ein `push`-Event für den Merge-Commit auf `main`; ein pauschal fehlschlagender Push-Workflow würde deshalb auch erfolgreiche, gewünschte Merges rot markieren. Der Schutz von `main` wird deshalb über GitHub Rulesets oder Branch Protection erzwungen.
