# 80 - Evaluations with Langfuse

## Learning goals
- Use Langfuse traces to inspect why a local eval failed.
- Compare failing and passing runs without moving the evaluation logic into the platform.
- Decide whether a failure belongs to the prompt, model choice, parsing, or pipeline code.

## Notes
- This lesson comes after module 9, once the MVP is already complete.
- The eval suite should still live in code.
- Langfuse is the inspection layer, not the source of truth for pass or fail.

## Script
- Start from a concrete failing example in the local eval suite.
- Open the corresponding trace in Langfuse.
- Inspect the prompt, model, inputs, outputs, tool calls, latency, and token usage.
- Compare the failed run with a passing run for the same task.
- Ask where the real problem lives:
  - unclear prompt
  - wrong model choice
  - parsing bug
  - missing validation
  - bad upstream data
- Turn the finding into a concrete fix in code or prompt logic.
- Re-run the local eval suite to verify the change.
- Emphasize the workflow boundary:
  - evals tell us that something failed
  - traces help us understand why it failed

## Sources
