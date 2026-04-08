# 70 - Costs


## Sources

- Daves Q&A Week1
- Q12: What are the best practices for managing costs of AI solutions?
  **A12:** Consider your whole application and the big problem you're trying to solve, then break that up into various subproblems, making them smaller and smaller. You'll find that for some problems you may not even need AI or an LLM at all. Once you do hit a wall where you need an LLM, if you make the problem small enough, you can use a very cheap model like GPT-4o-mini or even an open source model with a specialized, optimized short prompt that focuses on solving a particular problem. That API call becomes almost free, leaving the heavier models only for really big problems that need that kind of power. The other part is properly managing input and output tokens. Optimize your RAG system, make your chunks smaller, reduce the total chunks you make available, and consider splitting up problems to use cheaper models.
  
#courses/ai-engineer-fundamentals/3-interacting-with-foundation-models