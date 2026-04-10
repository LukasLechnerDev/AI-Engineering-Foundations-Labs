# 20 - Prompt Management and Versioning

## Learning goals
- Understand why versioned prompt management is useful once the project has a working pipeline.
- See the operational tradeoffs of storing prompts outside the codebase.
- Learn how Langfuse connects prompt versions to traces.

## Notes
- This lesson still belongs in the observability module because students have already experienced prompt iteration in code.
- It should be taught as an optional operational convenience, not as the only way to work with prompts.
- The main teaching value is the tradeoff, not the UI workflow alone.

## Script
- Explain the problem with hardcoding prompts directly in source code:
  - Every prompt change requires a code change, a review, and a deployment.
  - It is hard to track which prompt version produced which output.
  - Rolling back a bad prompt means rolling back code.
- Explain what prompt management gives you:
  - A central place to store, name, and version prompts.
  - The ability to compare outputs across prompt versions in your traces.
  - A history of every change so you can audit or revert quickly.
- Show how Langfuse handles prompt management:
  - Creating and naming a prompt in the Langfuse UI
  - Publishing a new version
  - Pulling a prompt by name and version in code using the Langfuse SDK
  - Linking a prompt version to a trace so every run is tied to the exact prompt that produced it
  - Configuring temperature remotely
  - Mentioning A/B testing for prompt versions as a later extension
- Emphasize the core point:
  - With a prompt management tool, you can update and deploy a prompt without touching your source code or redeploying your application.
  - This is a meaningful operational advantage because non-engineers can iterate on prompts directly and changes can go live immediately.
- Cover the benefits and drawbacks of external prompt management:
  - Benefits: no code deploy for prompt changes, version history, easier rollback, better traceability
  - Drawbacks: weaker code review, extra runtime dependency, harder local development, stale prompt risk
- Keep out:
  - full A/B testing workflows in production
  - custom prompt templating engines

## Sources
- https://app.datalumina.academy/c/genai-accelerator/sections/578161/lessons/2306561
