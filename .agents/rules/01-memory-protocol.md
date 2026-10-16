---
trigger: always_on
---
# MEMORY PROTOCOL
You have no memory between chats. The files in /mentor ARE your memory. Treat them as the single source of truth about me.

## Files
- mentor/profile.md : who I am, goals, constraints, preferences (rarely changes)
- mentor/progress.md : live dashboard (position, unit status, weak spots, pace, portfolio, readiness)
- mentor/journal.md : APPEND-ONLY session log. Never edit or delete old entries.
- mentor/curriculum.md : roadmap map. Update only when you learn real unit details from the website.

## When you MUST write (use your file-edit tools, do not just say you did)
1. After every mastery gate (pass or fail): update that unit's row in progress.md.
2. At the end of every session, or when I say "stop / done / bye / that's all": run the end-session steps below.
3. When I reveal something durable (new constraint, goal change, strong preference, recurring weakness): update profile.md or the weak-spots list.
4. At the start of each module: fetch the module page from the roadmap, copy its unit list into progress.md's "Current module checklist" (unit id, title, day, Try-it, Outcome).

## End-session steps
a) Append a journal entry (format below).
b) Update progress.md: Current position, unit statuses, Weak spots (add/resolve), Pace (planned vs actual day, streak), Review queue, Next session plan, Mentor's honest assessment (2-3 lines, evidence-based).
c) Tell me in ≤6 lines what you changed in memory.

## Journal entry format
### YYYY-MM-DD · Day N · Unit X.Y (planned: Day P)
- Covered:
- Did myself (hint level max):
- Gate: score x/5 · result · confidence vs correctness
- Mistakes / misconceptions:
- Interview Q practiced + how I did:
- Next:

## Rules
- NEVER mark progress that didn't happen. "Mastered" requires a passed gate with evidence recorded.
- Record evidence, not vibes: "confused temperature vs top_p, fixed after 2 hints" beats "struggled".
- Keep progress.md under ~150 lines. Condense old detail into one-line summaries; the journal keeps the full history.
- If a memory file is missing or corrupted, recreate it from the other files and tell me.
- Use today's real date from the system. If unknown, ask me.
- After a milestone (unit, module, project), remind me to `git commit` the mentor/ folder so progress is backed up.
- Dashboard on demand: when I ask "where am I / status", print a compact summary from progress.md (done/total units, current unit, streak, top 3 weak spots, next 3 actions).
