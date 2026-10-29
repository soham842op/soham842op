<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./assets/banner-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="./assets/banner-light.svg">
  <img alt="Soham Shah - AI/ML Engineer building LLM apps, RAG systems and MLOps pipelines" src="./assets/banner-light.svg" width="100%">
</picture>

<p align="center">
  <a href="https://www.linkedin.com/in/soham-shah842/"><img alt="LinkedIn" src="https://img.shields.io/badge/LinkedIn-soham--shah842-4f46e5?style=flat-square&logo=linkedin&logoColor=white"></a>
  <a href="mailto:sshah270@asu.edu"><img alt="Email" src="https://img.shields.io/badge/Email-sshah270%40asu.edu-4f46e5?style=flat-square&logo=gmail&logoColor=white"></a>
  <a href="https://live-docs-ten-neon.vercel.app"><img alt="LiveDocs live demo" src="https://img.shields.io/badge/Live_Demo-LiveDocs-4f46e5?style=flat-square&logo=vercel&logoColor=white"></a>
</p>

<p align="center"><b>Open to AI/ML Engineer, Data Scientist and Software Engineer roles in the US</b></p>

## About

- MS in Computer Science, Arizona State University (May 2026, GPA 3.84)
- I build LLM apps and then measure them: retrieval evals, held-out test sets, ablations and significance tests
- Shipped ML to production before: FastAPI inference services on AWS EKS with Docker and CI/CD
- Co-author of a Springer paper on reinforcement learning for algorithmic trading

## Featured projects

| Project | What it does |
|:--|:--|
| **LiveDocs**<br>[Demo](https://live-docs-ten-neon.vercel.app) · [Code](https://github.com/soham842op/LiveDocs) | Realtime collaborative editor (Yjs CRDTs) with a Gemini copilot: cited RAG Q&A over pgvector, inconsistency detection and structured suggestions. **97.1% hit@1, 100% hit@5** on a 40-question retrieval benchmark. <br><sub>Next.js · FastAPI · Postgres + pgvector · AWS S3</sub> |
| **DevLens**<br>[Code](https://github.com/soham842op/DevLens) | Privacy-first CLI that indexes local repos and git history into SQLite and writes reports with a local Llama 3 model, so no code leaves the machine. Ground-truth eval harness raised error-handling precision from **31% to 96%**. <br><sub>TypeScript · Node.js · SQLite · Ollama · Vitest · GitHub Actions</sub> |
| **Hybrid Music Recommender**<br>[Code](https://github.com/rajmahato111/music_recommendation_system) | Item2Vec plus audio-feature embeddings over 170K Spotify tracks with FAISS retrieval. **NDCG@10 +22%** over collaborative-only (95% CI 13-33%, Wilcoxon p < 0.00001). Group project. <br><sub>Python · Gensim · FAISS · LightGBM</sub> |
| **DataWhisperer**<br>[Code](https://github.com/soham842op/DataWhisperer) | Offline Text-to-SQL agent: ask questions in plain English, get SQL and answers from a local CodeLlama model on GPU. <br><sub>Python · LangChain · llama-cpp · Streamlit</sub> |

## Open source

**[Don't Be Michael](https://github.com/agentvivekkumar/dontbemichael)** - a multi-agent desktop app built on Claude Code (590+ stars, MIT)

- [PR #601](https://github.com/agentvivekkumar/dontbemichael/pull/601) ![merged](https://img.shields.io/badge/merged-6f42c1?style=flat-square) - fixed the "max turns per run" safety limit for AI agents, which was silently ignored in interactive terminals; added 13 unit tests
- [PR #645](https://github.com/agentvivekkumar/dontbemichael/pull/645) ![in review](https://img.shields.io/badge/in_review-6b7280?style=flat-square) - surfaced those stops in the app's safety dashboard

## Publication

**Springer chapter on reinforcement learning for algorithmic trading** · [Read the paper](https://link.springer.com/chapter/10.1007/978-981-96-2179-8_31)<br>
Compared Actor-Critic, Policy Gradient, Q-Learning and Double Dueling Q-Learning on Larsen & Toubro stock data; Policy Gradient led with a 43.95% ROI.

## Tech stack

**ML and data**<br>
<img alt="Python, scikit-learn, TensorFlow" src="https://skillicons.dev/icons?i=py,sklearn,tensorflow">

**LLMs and retrieval:** Gemini API · Ollama (Llama 3) · RAG · pgvector · FAISS · MCP

**Backend and MLOps**<br>
<img alt="FastAPI, Node.js, PostgreSQL, SQLite, Docker, Kubernetes, AWS, GitHub Actions" src="https://skillicons.dev/icons?i=fastapi,nodejs,postgres,sqlite,docker,kubernetes,aws,githubactions">

**Frontend**<br>
<img alt="TypeScript, React, Next.js, Electron, Vercel" src="https://skillicons.dev/icons?i=ts,react,nextjs,electron,vercel">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./assets/footer-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="./assets/footer-light.svg">
  <img alt="" src="./assets/footer-light.svg" width="100%">
</picture>
