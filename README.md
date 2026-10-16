# AI Mentor for Antigravity (100 Days of AI Engineering)

## Setup (5 minutes)
1. Unzip this folder somewhere permanent, e.g. ~/ai-mentor.
2. In Antigravity: File -> Open Folder -> select `ai-mentor` (the folder itself, not its parent).
3. Open the Customizations panel (the "..." menu in the agent panel) -> Rules. Confirm `00-mentor-persona` and `01-memory-protocol` show as **Always On**. If a rule shows another mode, switch it to Always On.
4. Open Workflows and confirm the slash commands appear: /start-session, /end-session, /where-am-i, /module-checkpoint, /weekly-review, /mock-interview.
5. In a new agent chat, type `/start-session`. The first run does onboarding (profile + prerequisite check).
6. `git init` in this folder and commit after each session. This is your backup of progress.

## Daily loop
/start-session -> study with your mentor -> /end-session

## Notes
- The files in `mentor/` are the memory. Chats don't remember anything by themselves, so always finish with /end-session.
- Keep each rule file under 12,000 characters (Antigravity's limit).
- Put your code in subfolders (e.g. `day-01/`, `projects/`), not inside `mentor/`.
- Older Antigravity versions used `.agent/` instead of `.agents/`. If your rules/workflows don't show up, rename the folder to `.agent`.
# AI-Engineering-Accelerated
