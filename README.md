<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./assets/header-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="./assets/header-light.svg">
  <img alt="Soham Shah. I build LLM apps, and then I measure them." src="./assets/header-light.svg" width="100%">
</picture>

[LinkedIn](https://www.linkedin.com/in/soham-shah842/) &nbsp;·&nbsp; [sshah270@asu.edu](mailto:sshah270@asu.edu) &nbsp;·&nbsp; [Try LiveDocs](https://live-docs-ten-neon.vercel.app)

### About

I finished my MS in Computer Science at Arizona State University in May 2026 (GPA 3.84). Most of what I build is LLM software, and I care a lot about proving it works: retrieval evals, held-out test sets, ablations and significance tests.

I've also shipped ML to production, running FastAPI inference services on AWS EKS with Docker and CI/CD, and I co-authored a Springer paper on reinforcement learning for algorithmic trading.

### Projects

<p>
  <a href="https://github.com/soham842op/LiveDocs"><picture><source media="(prefers-color-scheme: dark)" srcset="./assets/projects/livedocs-dark.svg"><img alt="LiveDocs: realtime collaborative editor with a Gemini copilot that answers with citations. 97.1% hit@1 on a 40-question retrieval benchmark." src="./assets/projects/livedocs-light.svg" width="49%"></picture></a>
  <a href="https://github.com/soham842op/DevLens"><picture><source media="(prefers-color-scheme: dark)" srcset="./assets/projects/devlens-dark.svg"><img alt="DevLens: CLI that indexes repos and git history and writes reports with a local Llama 3. Error-handling precision up from 31% to 96%." src="./assets/projects/devlens-light.svg" width="49%"></picture></a>
</p>
<p>
  <a href="https://github.com/rajmahato111/music_recommendation_system"><picture><source media="(prefers-color-scheme: dark)" srcset="./assets/projects/music-recommender-dark.svg"><img alt="Hybrid Music Recommender: Item2Vec and audio embeddings over 170K Spotify tracks with FAISS retrieval. NDCG@10 +22% over collaborative-only." src="./assets/projects/music-recommender-light.svg" width="49%"></picture></a>
  <a href="https://github.com/soham842op/DataWhisperer"><picture><source media="(prefers-color-scheme: dark)" srcset="./assets/projects/datawhisperer-dark.svg"><img alt="DataWhisperer: offline Text-to-SQL agent using a local CodeLlama model on GPU." src="./assets/projects/datawhisperer-light.svg" width="49%"></picture></a>
</p>

### Open source

I contribute to [Don't Be Michael](https://github.com/agentvivekkumar/dontbemichael), a multi-agent desktop app built on Claude Code (590+ stars, MIT).

- [#601](https://github.com/agentvivekkumar/dontbemichael/pull/601) (merged): the "max turns per run" safety limit for agents was silently ignored in interactive terminals. I fixed it and added 13 unit tests.
- [#645](https://github.com/agentvivekkumar/dontbemichael/pull/645) (in review): shows those stops in the app's safety dashboard.

### Publication

[Reinforcement learning for algorithmic trading](https://link.springer.com/chapter/10.1007/978-981-96-2179-8_31), Springer. We compared Actor-Critic, Policy Gradient, Q-Learning and Double Dueling Q-Learning on Larsen & Toubro stock data. Policy Gradient came out ahead with a 43.95% ROI.

### Toolkit

| | |
|:--|:--|
| ML and data | <img alt="Python, scikit-learn, TensorFlow" src="https://skillicons.dev/icons?i=py,sklearn,tensorflow" height="36"> |
| LLMs and retrieval | Gemini API, Ollama (Llama 3), RAG, pgvector, FAISS, MCP |
| Backend and MLOps | <img alt="FastAPI, Node.js, PostgreSQL, SQLite, Docker, Kubernetes, AWS, GitHub Actions" src="https://skillicons.dev/icons?i=fastapi,nodejs,postgres,sqlite,docker,kubernetes,aws,githubactions" height="36"> |
| Frontend | <img alt="TypeScript, React, Next.js, Electron, Vercel" src="https://skillicons.dev/icons?i=ts,react,nextjs,electron,vercel" height="36"> |

<sub>Thanks for reading. If something here overlaps with what you're working on, I'd like to hear about it.</sub>
