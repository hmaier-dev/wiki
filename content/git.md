---
categories:
- cli
- Linux
- ci/cd
title: git
---

## TL;DR 

-   *Ich möchte alles rückgängig machen was ich bisher gemacht habe*:
    -   `reset --hard`
-   *Ich habe ungewollte Commits in meinem Branch*:
    -   `rebase -i <commit-hash>^`
        - Das *Circumflex* macht den `rebase --interactive` inklusiv. Es gibt den Parent des Commits an, und nimmt den angegebenen Commit daher in den `rebase -i` mit hinein.
-   *Ich muss nachträglich Änderungen zu einem Commit hinzufügen*:
    -   `commit --fixup <commit>` und `rebase -i --autosquash`
-   *Ich möchte Änderungen aus dem Hauptbranch (z.B. production) in
    meinem branch übernehmen*:
    -   `git pull && git rebase production`
-   *Wie kann ich ein Commit zu mehreren umwandeln*:
    -   `rebase -i && edit <jeweiligen-commit> && add -p`
-   *Wie erstelle ich einen neuen Branch?*:
    -   `checkout <main/prod> && switch -c <new-branch>`
-   *Ich ein `rebase -i` auf meinen kompletten Branch machen*:
    -   `git rebase -i HEAD~$( git rev-list --count --no-merges <main>..)`
    -   Bezieht den allerste Commit mit ein: `git rebase -i --root`
-   *Wie übernehme ich einzelne Commits in meinen Branch*:
    -   `git switch <mein-branch> && git cherry-pick <commit-hash>`
-   *Wie sehe ich alle Änderungen in einer Datei auf Zeit?*:
    -   `git log -p production.. -- <file>`
-   Wie kann ich den letzten Commit, von meiner derzeitigen Position,
    auseinander-basteln?
    -   `git reset HEAD~`
        -   Kann man mit nem `rebase -i` kombinieren, da dabei der
            `HEAD` ja durch die Commits wandert. Einfach im Editor mit
            `edit` am gewünschten Commit anhalten und dann `reset`en.
-   Wie kann ich ein gelöschtes File wiederherstellen.
    -   `git checkout <commit-hash>^ -- <filename>`
    -   `git add <filename>`
-   This feature helps Git remember how you resolved conflicts
    previously, so if the same conflict arises again, Git can
    automatically apply the same resolution.
    -   `git config --global rerere.enabled true`
- Wie kriege ich mein lokales Repo auf den Stand des Remote-Repos?
    - Falls `origin` `main` ist: `git rebase origin/main`
- Welches ist Remote-Repo?
    - `git branch -a` um alle Branches zu sehen.
    - Um nur die Remote-Branches zu sehen ein `git branch -r`
- Wie arbeite ich mit meinem Remote-Branch lokal?
    - Zuerst, alle Remote-Branches anzeigen lasse: `git branch -r`
    - Dann, neuen lokalen Branch auf Remote-Branch als Startpunkt zeigen lassen: `git checkout -b <branch> origin/<branch>`

## rebase

Mit einem `rebase <main>` bringt man den Branch auf die Höhe des
Hauptbranches.

Falls man eine Branch versaut hat und dieser schon als Merge-Request im
Gitlab steht, kann man die ganze Sache mit nem `rebase -i` bereinigen.

Dazu nehme man den letzten Commit in dem Branch bevor, die Sauerei
angefangen hat und geben starte damit den rebase:
`git rebase -i <commit>`.

Man wird nun in ein Editor geworfen in dem man Commits ändern oder auch
entfernen kann. Nach dem Schließen des Editors kann man dem versauten
Zustand mit nem `git pull` wiederherstellen oder mit nem
`git push origin <versaubeutelter-branch> --force` den Merge-Request
aktualisieren.

Was bei einem `rebase` wichtig zu beachten ist, dass sich die Commit-IDs
ändern. Zwei unterschiedliche Commits mit den
**gleichen Änderungen** gehören somit dann nicht
mehr zusammen.

## reset

Falls man schon getätigte Commits wieder rückgängig machen möchte, kann
man dies mit `git reset --hard <commit>` machen. Der angegebene Commit
ist dabei der, auf welchen man zurück möchte. Möchte man diesen
inklusive löschen, gibt man einfach den Commit mit Circumflex
(`<commit>^`) an.

Allerdings ist dieses Kommando mit Vorsicht zu genießen, den alle
neueren Commit werden gelöscht.

## reflog

Vorherige Stände des Branch anziegn.

## merge

Habe ich einen Hauptbranch (z.B. `main`) und möchte eine Nebenbranch (z.B. `wichtiges-feature1`)
mergen, bietet es sich an `wichtiges-feature1` zu allererst mit einem rebase auf den Stand des
Hauptbranches zu bringen. 

- `git checkout wichtiges-feature1`
- `git rebase main`

Wenn alle potenziellen Konflikte bereinigt sind, kann ich mergen.
Dazu gehe ich in den Hautpbranch und merge dort.

- `git checkout main`
- `git merge wichtiges-feature1`

Danach kann ich den Nebenbranch löschen.

- `git branch -d wichtiges-feature1`

Beim mergen ist zu beachten, dass beide Branches lokal vorhanden sind.

## add \--patch 

Falls ich in einem File Änderungen gemacht habe, die verschiedenen
Commits zugehörig sind, kann ich dies mit einem `--patch` bzw. `-p`
machen. Git teilt das File dann in Blöcke ein, die es für sinnig
befindet. Das heißt nicht, dass die Einteilung immer sinnig ist.
Allerdings kann man diese auch nachbearbeiten.

``` bash
# Alle Optionen beim git add -p
Diesen Patch-Block der Staging-Area hinzufügen [y,n,q,a,d,j,J,g,/,e,?]?
```

## commit \--fixup <commit> 

Falls man im Nachhinein einem Commit Änderungen hinzufügen möchte und
die Commit-ID parat hat, kann man dies mit eine `--fixup` machen. Danach
ist ein `rebase -i --autosquash <base-branch>` nötig. Dabei werden dem
`<commit>` die darunterliegenden Commits mit `squash` hinzugefügt.

## commits spliten 

Diese manpage ist ziemlich hilfreich dabei:
<https://manpages.debian.org/bookworm/git-man/git-rebase.1.en.html#SPLITTING_COMMITS>.

Während des `rebase` kann mit `add -p` verschiedene Code-Stücke in
einzelne Commits übernehmen.

## update-refs

``` bash
update-ref refs/heads/<your-branch>
```

## Einzelne Commits für MR fertig machen

### Variante 1 (cherry-pick) 

Da ein MR einfach nur ein Branch ist, erstellt man einen seperaten
Branch in den man per `cherry-pick` die gewünschten Commits kopiert. Die
gepickten Commits werden *kopiert* und nicht verschoben (sie existieren
nun auf beiden Branches). Hier ist ein möglicher Ablauf mit
`cherry-pick`:

``` bash
# Beim Checkout neuen Branch anlegen
git checkout -b <neuer-branch> origin/production
git cherry-pick <commit-hash1>
git cherry-pick <commit-hash2>
git push -u origin
```

Beim `cherry-pick` kann es durchaus zu Merge-Konflikten kommen.
Bespielweise wenn man verschiedene Commits von Änderungen an einen File
pickt, die von einander abhängen.

Man könnte natürlich auch den gesamten Branch kopieren und mit einem
`rebase -i` alle Commits entfernen die nicht passend sind.

``` bash
# Nimmt derzeitigen Branch als base
git checkout -b <neuer-branch>

# Nimmt production als base-branch
git checkout -B <neuer-branch> production
```

### Variante 2 (update-refs)
Ab der Version 2.38, kann man in einem
interactive rebase den Command `update-ref refs/heads/<anderer-branch>`
angeben. Damit kann man entweder auf einen bestehenden Branch verweisen
oder einen neuen Branch anlegen. Diese ist dann als Referenz zum
`base`-Branch. Man zweigt also Commits in seperate Branches ab, kann man
aber bei nem rebase vom `base`-Branch dessen Änderungen übernehmen.

## MR/PR löschen 

Da ein Merge-/Pull-Request im Grunde nichts anderes als ein Branch ist,
kann man ihn wie folgt löschen:

``` bash
# Lösche den Remote-Branch (ersetze origin durch den Namen deines Remotes)
git push origin --delete <dein-branch>

# Wechsle zu einem anderen Branch, um sicherzustellen, dass der zu löschende Branch nicht aktiv ist
git checkout <anderer-branch>

# Lösche den lokalen Branch
git branch -d <dein-branch>
```

## Submodule Repositorys 

Bei manchen Repositorys werden anderer Repos mit eingebunden. Ab und an
kann man ein solche Nachricht krigen:

``` bash
Auf Branch main
Ihr Branch ist auf demselben Stand wie 'origin/main'.

Änderungen, die nicht zum Commit vorgemerkt sind:
  (benutzen Sie "git add <Datei>...", um die Änderungen zum Commit vorzumerken)
  (benutzen Sie "git restore <Datei>...", um die Änderungen im Arbeitsverzeichnis zu verwerfen)
        geändert:       file.mod/pkg/myfile (neue Commits)

Unversionierte Dateien:
  (benutzen Sie "git add <Datei>...", um die Änderungen zum Commit vorzumerken)
```

Mit dem `(neue Commits)` wird darauf hingewiesen, das eingebettete Repo
einmal mit `git submodule update` auf den neusten Stand zu bringen.

## \--bare
Mit einem bare-Repository kann man einen selbstgewählten `--work-tree` benutzen.
Man kann beispielweise dafür sein `$HOME` nehmen, um damit Configs, Dotfiles, etc. zu 
verwalten. Dafür benutzt man dann diesen alias.
```bash
/usr/bin/git --git-dir=$HOME/repos/dotfiles/ --work-tree=$HOME
```
Die Einrichtung dieses Setups zum Verwalten von Dotfiles läuft wie folgt.
```bash
git config --global init.defaultBranch main
mkdir -p $HOME/repos
git clone --bare https://github.com/hmaier-dev/dotfiles.git $HOME/repos/dotfiles
# oder
# git clone --bare git@github.com:hmaier-dev/dotfiles.git $HOME/repos/dotfiles
git --git-dir=$HOME/repos/dotfiles/ --work-tree=$HOME config --local status.showUntrackedFiles no
git --git-dir=$HOME/repos/dotfiles/ --work-tree=$HOME checkout main
git --git-dir=$HOME/repos/dotfiles/ --work-tree=$HOME push --set-upstream origin main
```
Vorher sollte `$HOME` am besten komplett blank sein (also auch ohne `.bashrc` etc.),
damit es nicht zu Merge-Konflikten kommt.

## config
Diese Variable kann gesetzt werden, wenn git-diff immer sein eigenes vim nimmt.
```bash
git config --global core.editor nvim
```

## Plattformen

- Github
- Gitlab
- https://forgejo.org/

