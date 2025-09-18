# Lumina — AI Assistant Project Brief

## Vision

Build **Lumina** — a JARVIS-like AI assistant whose primary language is **Hindi**. It should understand Hindi (speech & text), respond in Hindi (text + TTS), connect to the internet for live info, and be resilient to API rate limits by rotating between multiple providers.

---

## Core Goals

* **Hindi-first**: Hindi STT, NLU, response generation, and Hindi TTS.
* **Multi-provider orchestration**: OpenRouter, Gemini, Groq (rotate across multiple API keys).
* **RAG (Retrieval-Augmented Generation)**: web search + vector DB.
* **Real-time voice**: microphone capture → STT → LLM → TTS → playback.
* **Robust rate-limit handling**: round-robin, circuit breaker, backoff.
* **Colorful logger**: states like Listening, Thinking, Generating, Searching, Speaking.
* **Research-driven**: follow official docs for APIs & integrations.

---

## Architecture Overview

1. **Input Layer**: mic or text.
2. **STT**: Whisper / Vosk / Coqui for Hindi speech recognition.
3. **Controller / Orchestrator**: manage provider selection, RAG, rate-limit handling.
4. **RAG Subsystem**: retriever (DuckDuckGo, Serp API, Tavily) + vector DB (Chroma/FAISS).
5. **LLM Generation**: OpenRouter / Gemini / Groq with API rotation.
6. **TTS**: StreamElements (Hindi) or LiveKit streaming.
7. **Output**: TTS playback + logs.
8. **Logger**: colorful state tracker (Thinking, Searching, Speaking).

---

## Integrations

* **TTS**: [StreamElements](https://api.streamelements.com/kappa/v2/speech)
* **Voice AI**: [LiveKit](https://docs.livekit.io/agents/start/voice-ai/)
* **LLMs**: OpenRouter, Gemini, Groq
* **Search APIs**: DuckDuckGo, Serp API, Tavily, LiveKit-search
* **Vector DB**: Chroma, FAISS, or Milvus

---

## Rate-limit Strategy

* Maintain pool of API keys per provider.
* Use **round-robin** load distribution.
* Circuit breaker to skip failing keys.
* Retry with exponential backoff + jitter.
* Centralized error reporting & telemetry.

---

## RAG Pipeline

1. Detect Hindi query.
2. Retrieve from vector DB.
3. If needed, fetch fresh results from DuckDuckGo / Serp / Tavily.
4. Embed + store documents.
5. Construct prompt in Hindi with context.
6. Send to LLM.
7. Generate concise Hindi response with citations.

---

## Logging System

Use `rich` for colored terminal logs:

* **Thinking** → Yellow
* **Generating** → Magenta
* **Searching** → Cyan
* **Speaking** → Green
* **Error/Idle** → White

---

## MVP Scope

* CLI prototype:

  * Mic input → Whisper STT (Hindi)
  * LLM query (one provider)
  * TTS via StreamElements (Hindi)
  * Colorful state logger
* Provider pool (2 API keys, fallback)
* Simple RAG with DuckDuckGo + Chroma
* Config-driven API key storage

---

## Roadmap

1. **Research & design** (docs, providers) — 2–4 days
2. **Prototype loop** (STT → LLM → TTS) — 1 week
3. **Provider resilience** (multi-API failover) — 3 days
4. **RAG integration** (search + vector DB) — 1 week
5. **LiveKit / web UI integration** — 1–2 weeks
6. **Polish & testing** — 1 week

---

## Research Checklist

* StreamElements API limits & voices.
* LiveKit voice-ai & search.
* OpenRouter, Groq, Gemini docs.
* Serp API & Tavily API quotas.
* Embedding libraries (sentence-transformers).
* Vector DB: Chroma / FAISS / Milvus.
* Whisper / Vosk / Coqui for Hindi STT.

---

## Tech Stack

* Python 3.10+
* Networking: `httpx` / `requests`
* Async: `asyncio`, `anyio`
* STT: Whisper / Vosk / Coqui
* TTS: StreamElements, LiveKit
* LLM Orchestration: custom wrapper / LangChain
* Vector DB: Chroma / FAISS
* Logging/UI: `rich`
* Packaging: Docker, Poetry / Pipenv

---

## Security

* Store API keys securely (env vars, secrets manager).
* Respect provider TOS.
* User privacy: add opt-in and retention policies.
* Sanitize all web-scraped content.

---
