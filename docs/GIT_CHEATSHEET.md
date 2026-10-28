# Git & GitHub cheat sheet for researchers

Think of Git as a **lab notebook for your files**. Each *commit* is a dated, signed entry you can return to. GitHub is the online copy, so your thesis survives a stolen laptop.

## The everyday loop

```bash
git pull                         # 1. get the latest version (start of each session)
# ... work on your files ...
git status                       # 2. what changed?
git add notebooks/analysis.ipynb # 3. choose what to save (or `git add .` for everything)
git commit -m "Add regression of yield on fertiliser"   # 4. save a snapshot with a message
git push                         # 5. upload to GitHub
```

In VS Code you can do all of this from the **Source Control** panel (**Ctrl + Shift + G**): type a message, click **Commit**, then **Sync Changes**.

## Good commit messages
| ❌ Unhelpful | ✅ Helpful |
|---|---|
| `update` | `Remove duplicate survey rows and fix LGA spellings` |
| `final final v3` | `Add Table 2: regression coefficients with 95% CI` |
| `changes` | `Fix bug: ages above 90 were not set to missing` |

Commit **small and often**, at least at the end of every working session.

## Looking back

```bash
git log --oneline                # list of snapshots
git diff                         # what changed since the last commit
git restore <file>               # throw away uncommitted changes to a file ⚠️
git checkout <commit-id> -- <file>   # bring back an old version of one file
```

## Branches: try an idea without breaking your main work

```bash
git switch -c try-random-forest  # create and move to a new branch
# ... experiment, commit ...
git switch main                  # back to the safe version
git merge try-random-forest      # keep the experiment if it worked
```

## What NOT to put on GitHub
- Confidential, personal or ethically restricted data. Add the file to `.gitignore` **before** committing
- Passwords and API keys
- Huge files (> 50 MB). Store them elsewhere and describe how to get them in the README

Accidentally committed something sensitive? **Tell your facilitator or supervisor straight away.** Deleting it in a new commit does not remove it from the history.

## Get a DOI for your code (for your thesis or paper)
1. Log in to https://zenodo.org with GitHub
2. Account → **GitHub** → switch your repository **on**
3. On GitHub: **Releases → Draft a new release** → tag `v1.0` → **Publish**
4. Zenodo creates a citable DOI. Add the badge to your README
