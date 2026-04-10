# 20 - Prompt Management and Versioning

## Teaching goal
- Students should understand why managing prompts as versioned artifacts — rather than hardcoded strings — makes AI systems easier to iterate on, debug, and maintain.

## What to cover
- The problem with hardcoding prompts directly in source code
  - Every prompt change requires a code change, a review, and a deployment
  - It is hard to track which prompt version produced which output
  - Rolling back a bad prompt means rolling back code
- What prompt management gives you
  - A central place to store, name, and version prompts
  - The ability to compare outputs across prompt versions in your traces
  - A history of every change so you can audit or revert quickly
- How Langfuse handles prompt management
  - Creating and naming a prompt in the Langfuse UI
  - Publishing a new version
  - Pulling a prompt by name and version in code using the Langfuse SDK
  - Linking a prompt version to a trace so every run is tied to the exact prompt that produced it
  - the temperature can also be configured remotely
  - Mention A/B testing for prompt versions

## Key point to emphasize
- With a prompt management tool, you can update and deploy a prompt **without touching your source code or redeploying your application**.
- This is a meaningful operational advantage: non-engineers (product managers, domain experts) can iterate on prompts directly, and changes can go live immediately.

## Benefits and drawbacks of external prompt management

### Benefits
- Prompts can be updated and go live without a code change or redeployment
- Full version history makes it easy to audit changes and roll back a bad prompt
- Non-engineers can own and iterate on prompts directly
- Every trace is linked to the exact prompt version that produced it, which makes debugging much easier

### Drawbacks
- Prompts live outside the codebase, so they are not reviewed in pull requests and changes are harder to catch before they go live
- The system gains an external runtime dependency — if the prompt management service is down, fetching prompts can fail
- It is easier to lose track of which prompts are still in use and which are stale
- Local development and testing gets more complex - we  require a connection to the external service, or a fallback strategy

## Keep out of this lecture
- A/B testing prompts in production (save for a later lesson if needed) => but mention it!
- Custom prompt templating engines

## Sources: 
- https://app.datalumina.academy/c/genai-accelerator/sections/578161/lessons/2306561