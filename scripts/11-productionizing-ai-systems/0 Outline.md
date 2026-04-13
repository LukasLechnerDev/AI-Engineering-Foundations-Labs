# Outline

## Learning goals
- Understand how to harden the project after the MVP already works end to end.
- Learn the core production engineering concerns that matter after prompting, evals, and basic observability.
- Understand why choosing an inference service is a production engineering decision.
- See how reliability work differs from prompt iteration and local evals.

## Notes
- This module now sits immediately after the MVP completion module.
- Basic Langfuse observability was already introduced earlier in the MVP path.
- Teach production engineering first: reliability, validation, fallbacks, logging, and routing.
- Keep the course OpenAI-first for the MVP, but explain that real systems often have more than one inference-service option.
- If Langfuse shows up in this module, it should be as a later extension for working with eval failures, not as basic observability.

## Script
1. From prototype to product
2. Choosing an inference service
3. Model choice and routing
4. Cost and latency tradeoffs
5. Handling rate limits and retries
6. Defensive parsing and output validation
7. Fallbacks and graceful degradation
8. Logging, failures, and operational debugging
9. Optional extension: Evaluations with Langfuse

## Sources
