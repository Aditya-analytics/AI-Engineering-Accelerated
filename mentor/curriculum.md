# Curriculum Map: 100 Days of AI Engineering (CampusX, accelerated)
Source of truth: https://ai-engineer-roadmap-2026.vercel.app/100-days/
Pre-reqs: basic Python, calling an API + reading JSON, Git. (Otherwise Level 0: https://ai-engineer-roadmap-2026.vercel.app/level/0/)

| # | Module | Days | Units | URL |
|---|--------|------|-------|-----|
| 1 | LLM Fundamentals | 1-6 | 6 | https://ai-engineer-roadmap-2026.vercel.app/100-days/llm-fundamentals/ |
| 2 | Building with LLM APIs | 7-17 | 9 | https://ai-engineer-roadmap-2026.vercel.app/100-days/building-with-llm-apis/ |
| 3 | Prompt Engineering | 18-24 | 8 | https://ai-engineer-roadmap-2026.vercel.app/100-days/prompt-engineering/ |
| 4 | RAG | 25-56 | 26 | https://ai-engineer-roadmap-2026.vercel.app/100-days/rag/ |
| 5 | Agents | 57-83 | 22 | https://ai-engineer-roadmap-2026.vercel.app/100-days/agents/ |
| 6 | Shipping to Production | 84-100 | 15 | https://ai-engineer-roadmap-2026.vercel.app/100-days/shipping-to-production/ |

After Day 100: Projects (12, build 2-3) https://ai-engineer-roadmap-2026.vercel.app/100-days/projects/ · Interview Prep (100 Qs) https://ai-engineer-roadmap-2026.vercel.app/100-days/interview-prep/
Going deeper later: full roadmap Levels 11 (platforms/self-hosting), 12 (multimodal/voice), 13 (fine-tuning), 4+5 (advanced RAG, multi-agent).

Rule: at the start of Modules 2-6, fetch the module URL and use the page's units, Try-its and Outcomes. If the fetch fails, ask me to paste the page. Then record the unit list below.

## Module 1 · LLM Fundamentals (Days 1-6)
Goal: explain why an LLM gives fluent wrong answers, estimate cost and latency, choose a model from measurements.
- 1.1 (Day 1) What an LLM Does: next-token prediction, what it is not (not a DB/search engine), text->tokens->numbers->layers->likelihoods, parameter counts, why chat models behave as they do. Try: send same prompt 5x, note variation. Outcome: explain in 2 sentences how an LLM answers and why it can be confidently wrong.
- 1.2 (Day 2) Tokens, Context and Latency: tokens not words, why Hindi/code/numbers cost more, input vs output tokens, time-to-first-token vs speed, what fills the context window, context is not memory, bigger windows aren't better. Try: count tokens for English, Hindi, code, numbers; estimate cost at 10,000 sends. Outcome: estimate cost + latency, decide more vs better context.
- 1.3 (Day 3) Beyond Text: images/audio/PDFs: images cost tokens, digital vs scanned PDFs, audio transcribe-first vs native, strengths/slips, image vs extracted text. Try: same chart as image vs extracted text, compare answers + tokens. Outcome: choose when to send images/audio/docs, predict cost + failure points.
- 1.4 (Day 4) Controlling Output: temperature, length limits/stop points, match randomness to task, reasoning models, when reasoning is wasted, trade-offs. Try: extraction vs creative at low/high temp; 3 hard problems on fast vs reasoning model. Outcome: choose settings and model type by task.
- 1.5 (Day 5) Where LLMs Fail: strengths, failure modes, why they make things up, ask "how reliably?". Try: 10 questions (knowable, unknowable, false premise, missing info); record answer + confidence. Outcome: predict which tasks need safeguards (docs, checks, human review).
- 1.6 (Day 6) Choosing a Model: closed vs open, no single best, knowledge cutoffs, pin versions, leaderboards shortlist/your examples decide, five things to compare, selection process. Outcome: choose a model from your own example results.
- Skipped on purpose (optional, full roadmap): attention/transformer internals (L1), MoE, training details, advanced sampling, cloud platforms/licenses, named benchmarks.

## Modules 2-6
Unit lists are filled in here when each module starts (mentor fetches the page, then appends the units below).
