# 80 - Tool Calling

The LLM is not calling the function you provide, it only tells us which function it wants to use with which parameters. We have to call the tools ourselves.

The model returns finish-reason = tool_calls when it wants to use a tool. 

Before jumping directly into the code, give the student a simplified explanations: We make a call to the LLM and provide the tools we are offering - The LLM doesn’t respond with a final answer, but with finish-reason = tool call, We have to check the response, and make the tool call if its in the finish reason - we make another request to the LLM with the result of the tool call. 

> Can -I define in the OpenAI API that the API itself uses tools like web-search?

Retrieval is a special kind of tool calling - so that the LLM gets more information

https://www.anthropic.com/engineering/building-effective-agents => Bottom shows how to prompt engineer your tools
	
#courses/ai-engineer-fundamentals/3-interacting-with-foundation-models