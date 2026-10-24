# SESSION JOURNAL (append-only; newest at the bottom; never edit old entries)

### 2026-10-16 · Day 1 · Onboarding (planned: Day 1)
- Covered: Onboarding, learner constraints (B.Tech 3rd yr AIML, 2 hrs/day max, parallel DSA, targeting intern/WFH AI role), technical diagnostic (Python, API/JSON, Git).
- Did myself (hint level max): L1 (independently coded test files and pushed branch `feature/day-1` to GitHub).
- Gate: Diagnostic passed.
- Mistakes / misconceptions: In Python max task, extracted just the value `92` rather than the dictionary item `{'id': 2, 'score': 92}`; introduced `key=lambda` idiom. In Git, noted that `mentor/` should not be ignored if tracking progress.
- Interview Q practiced + how I did: Diagnostic tasks executed with working code.
- Next: Unit 1.1: What an LLM Does.

### 2026-10-17 · Day 1 · Unit 1.1 (planned: Day 1)
- Covered: What an LLM Does, next-token prediction, sampling vs greedy decoding, token probability distributions.
- Did myself (hint level max): L2 (wrote API script, resolved .env path, fixed 401 auth header and 402 token quota errors).
- Gate: score 3.75/5 · needs-review · confidence not stated by learner across questions.
- Mistakes / misconceptions: Confused internal transformer output logits/softmax with vector similarity search; suggested prompt fallback instead of tool/function calling for stateful backend actions.
- Interview Q practiced + how I did: Answered company policy hallucination question with high-level RAG/prompting concepts; critiqued and upgraded to senior articulation.
- Next: Retest Unit 1.1 weak spots, then proceed to Unit 1.2 (Tokens, Context and Latency).

### 2026-10-18 · Day 2 · Unit 1.1 Review (planned: Day 2)
- Covered: Clarified transformer LM head architecture: final hidden state projection via matrix multiplication into vocabulary logits, followed by Softmax probability distribution (contrasted with vector database search).
- Did myself (hint level max): L1 (Identified need for architectural depth and mental model reset).
- Gate: Unit 1.1 retest deferred · status remains needs-review.
- Mistakes / misconceptions: Clarified confusion around decoding step vs vector search.
- Interview Q practiced + how I did: None (short session focused on architectural mental model).
- Next: Complete 3-question warm-up (logits/softmax check, tool-calling distinction), then start Unit 1.2 (Tokens, Context and Latency).

### 2026-10-24 · Day 6 · Module 1 Checkpoint & Mastery (planned: Day 6)
- Covered: Micro-LLM simulation engine & interactive visualizer, BPE tokenization & non-English fragmentation benchmarking, hardware latency profiling (TTFT vs ITL, Prefill vs Decode, Prompt Caching), sampling dynamics (temperature vs Top-P), and execution boundaries (Tool Calling vs raw generation).
- Did myself (hint level max): L1 (independently coded matrix multiplication and softmax, tested token benchmarking, analyzed visualizer).
- Gate: Module 1 Checkpoint quiz: scored 4.85/5 · MASTERED · strong confidence and crisp answers.
- Mistakes / misconceptions: Prior confusion on Softmax/logits vs cosine similarity and tool calling boundaries completely resolved with evidence.
- Interview Q practiced + how I did: Defended 2M context window stuffing vs RAG on TTFT latency and cost grounds; articulated Tool Calling boundary for backend state mutation.
- Next: Fetch Module 2 syllabus (Building with LLM APIs) and begin Unit 2.1 (API Client Architecture, Pydantic schemas, and error retries).


