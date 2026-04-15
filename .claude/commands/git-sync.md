<!--
  artifact_name: git-sync.md
  version: v1
  status: Draft
  purpose: Claude Code slash command that performs a full git sync cycle in one shot:
           save all open files → stage all changes → auto-generate a context-driven
           commit message from the diff → push to upstream. Eliminates manual git
           ceremony during active development sessions.
  date: 2026-02-19
  author: Generated for Iqbal Yusuf / KSE
  usage: /git-sync
         No parameters required. Run from any directory inside a git repository.
         Claude Code will execute all steps sequentially and confirm with the last
         3 commits on success.
  prerequisites:
    - Must be inside a git repository (git init or cloned)
    - Remote origin must be configured for push to succeed
    - SSH key or credential helper must be set up for remote auth
  guardrails:
    - Warns before staging if sensitive or unintended files are detected
    - Exits gracefully if working tree is clean (nothing to commit)
    - Will auto-set upstream if not configured (git push --set-upstream origin <branch>)
-->

# Git Sync — Save, Stage, Commit, Push

Save all unsaved files in the editor, stage everything, generate a descriptive commit message based on the actual diff, and push to the current upstream branch — all in one shot.

## Steps

1. **Save all open files** — use the editor API or tell the user to ensure all buffers are saved before proceeding.

2. **Stage all changes**:
   ```bash
   git add -A
   ```

3. **Inspect the diff to craft a commit message**:
   ```bash
   git diff --cached --stat
   git diff --cached
   ```
   From the diff output, generate a commit message that follows this structure:
   - **Subject line** (≤72 chars): imperative mood, specific — e.g. `Add resume ranking module with vocabulary normalization`
   - **Body** (optional, if changes are non-trivial): bullet list of what changed and why, wrapped at 72 chars
   
   Do NOT use generic messages like "Update files" or "Fix stuff".

4. **Commit with the generated message**:
   ```bash
   git commit -m "<generated subject>" -m "<generated body if applicable>"
   ```

5. **Push to upstream**:
   ```bash
   git push
   ```
   If no upstream is set, run:
   ```bash
   git push --set-upstream origin $(git branch --show-current)
   ```

6. **Confirm** by outputting the result of:
   ```bash
   git log --oneline -3
   ```

## Notes

- If `git add -A` would stage unintended files (e.g. secrets, build artifacts), warn the user and list what will be staged before committing.
- If the working tree is clean (nothing to commit), report that and exit gracefully.
- Commit message language: English, present/imperative tense.