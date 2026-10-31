# 🚀 100 Days of AI Engineering - Progress Tracker

**Course Roadmap:** [100 Days of AI Engineering (Vercel)](https://ai-engineer-roadmap-2026.vercel.app/100-days/building-with-llm-apis/)  
**Current Module:** Module 2: Building with LLM APIs  
**Current Subtopic:** Unit 2.8: Rate Limiting, Concurrency & Batching (Day 16)

---

## 🗺️ What's Left in "Building with LLM APIs"
- [x] Day 7-8: Client Configuration & Basic Calls
- [x] Day 9-10: Multi-Turn Conversations & Memory
- [x] Day 11-12: Streaming Responses (SSE)
- [x] Day 13-14: Structured Outputs & Tool Calling
- [x] **Day 15: Handling Failures (COMPLETED ✅)**
- [ ] **Day 16: Rate Limiting & Concurrency / Batching (CURRENT 🟡)**
- [ ] Day 17: Cost & Latency Optimization / Caching

---

## 📊 Unit Progress History

### Unit 2.7: Handling Failures (Day 15)
```
[████████████████████] 100% Completed
```

| Sub-concept | Status | Key Concept Covered |
| :--- | :---: | :--- |
| **1. Failure Taxonomy** | ✅ Done | Transport (429, 5xx) vs Semantic (broken JSON, hallucinations) |
| **2. Retry vs. Fail-Fast** | ✅ Done | Backoff with jitter on 429/503; Immediate abort on 401/400 |
| **3. Timeouts & Guardrails** | ✅ Done | Strict request deadlines (`timeout=8.0`) to avoid hung threads |
| **4. Multi-Provider Fallbacks** | ✅ Done | `.with_fallbacks([backup_model])` (OpenAI ➡️ Anthropic) |
| **5. Output Auto-Repair** | ✅ Done | `OutputFixingParser` & LangChain's internal `NAIVE_FIX_PROMPT` |
| **6. The End-to-End Master Challenge** | ✅ Done | Architectural design & reasoning for all 5 failure modes |
| **7. Final Hands-On Coding Lab** | ✅ Done | Production failure pipeline from scratch |

---

### Unit 2.8: Rate Limiting, Concurrency & Batching (Day 16)
```
[░░░░░░░░░░░░░░░░░░░░] 0% Completed
```

| Sub-concept | Status | Key Concept Covered |
| :--- | :---: | :--- |
| **1. The Two Bottlenecks: RPM vs TPM** | 🟡 **IN PROGRESS** | Request counts vs token budget per minute |
| **2. Client-Side Rate Limiter Algorithms** | ⚪ Not Started | Token Bucket & Leaky Bucket implementations |
| **3. Controlled Concurrency (Semaphores)** | ⚪ Not Started | `asyncio.Semaphore` to throttle inflight workers |
| **4. The OpenAI / Anthropic Batch API** | ⚪ Not Started | Asynchronous 50% discount batch endpoints |
| **5. Scenario Challenge: Thundering Herd** | ⚪ Not Started | Multi-worker queue design & backpressure |
| **6. Final Hands-On Coding Lab** | ⚪ Not Started | Custom Token-Bucket Rate Limiter + Async worker pool |

---
*Last Updated: 2026-10-30*
