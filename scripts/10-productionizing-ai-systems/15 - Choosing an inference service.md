# 15 - Choosing an inference service

## Learning goals
- Understand the main ways a production system can access foundation models.
- Compare direct model providers, hyperscalers, and inference platforms at a high level.
- Understand why this course still uses OpenAI directly for the MVP.

## Notes
- Keep this lecture practical and short.
- This is not a vendor survey.
- The goal is to show that inference-service choice becomes important once the product moves beyond the MVP.

## Script
- Explain that in this course we use OpenAI directly because it is the simplest way to get the MVP working.
- Then explain that in production, teams often have more than one way to get inference from a model.
- The main options are:
  - model providers directly, like OpenAI, Anthropic, or Google
  - hyperscalers in the middle, like Azure OpenAI, AWS Bedrock, or Vertex AI
  - inference platforms and aggregators, like OpenRouter and similar services
- Briefly mention that self-hosting exists too, but it is a more advanced path with more operational complexity.
- Explain the decision factors:
  - ease of use
  - model access
  - pricing
  - latency
  - reliability
  - rate limits
  - compliance and enterprise constraints
  - vendor lock-in
- Close with the rule of thumb:
  - for a course project or fast MVP, choose the simplest reliable setup
  - for production, choosing the inference service becomes an engineering decision

## Sources
