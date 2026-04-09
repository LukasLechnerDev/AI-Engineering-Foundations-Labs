# 30 - Cost and latency tradeoffs

## Goal
- Show students how to move from a working prototype to a system that is affordable and fast enough to use in practice.

## What to cover
- not every subproblem needs the same model
- when a smaller, faster model is enough
- when a stronger model is worth the cost
- token costs as part of total system design
- latency as a product problem, not just a technical metric
- breaking one big task into smaller targeted calls
- reducing unnecessary context and output length
- designing multi-step pipelines that stay useful without becoming too expensive

## Sources
- Dave's Q&A Week 1
- Q12: What are the best practices for managing costs of AI solutions?
  - Break the application into smaller subproblems.
  - Use cheaper models when the subproblem allows it.
  - Optimize input and output token usage.
  - Reserve stronger models for the parts that truly need them.
