# 40 - What is an AI Engineer? - r2r

## Summary
- Definition from the AIE book
- Not someone who uses Agentic Engineering to write software
- latent space blogpost + diagram
- easy to build demos and prototypes, hard to operate them reliably at scale
  - What are the challenges?

## Link Sources
- https://www.latent.space/p/ai-engineer

## Sources
- AIE Book
- [What We’ve Learned From A Year of Building with LLMs](https://applied-llms.org/)
- https://www.latent.space/p/ai-engineer

## Introduction

This course is designed to help developers transition into an AI engineering role.

But what exactly is an AI engineer?

There is, of course, no central authority that defines job roles. Instead, roles emerge from the market and are shaped by what companies need and what practitioners actually do in the real world.

The definition of an AI engineer—and of AI engineering more broadly—is still evolving and not yet stable. In this video, however, I want to discuss definitions from some credible sources.


## Definition from the Book AI Engineering

The book *AI Engineering* by Chip Huyen is one of the most influential resources shaping how people think about AI engineering. In this course, I will often refer to it, since, in my opinion, it is one of the best foundational books on this topic.

In the book, Chip describes an AI Engineer like this: (page 12)

> “AI Engineering refers to the process of building applications on top of foundation models.”

So, on top of AI models that are provided by OpenAI or Anthropic. 

How did she initially come up with the term “AI Engineering”? Well, she just surveyed 20 people developing applications on top of foundation models about what term they would use to describe what they are doing, and most preferred the term “AI Engineering”. 

### AI Engineering vs ML Engineering
She also writes about the difference between ML engineering (so machine learning engineering) and AI engineering: 

> “[…] traditional ML engineering involves developing ML models, AI engineering leverages existing ones. 


> An AI Engineer is not someone who has deep knowledge about Machine Learning and Mathematics, and does not build models from scratch. 

>Instead, an AI Engineer builds applications on top of foundational models. AI engineering is less about Machine Learning and more about Engineering, and closer to the actual product.


## Definition from Latent Space blogpost
Another popular resource on AI Engineering is the blog post on the Latent Space platform titled “The Rise of the AI Engineer”. 
![](40%20-%20What%20is%20an%20AI%20Engineer%20-%20r2r/image%203.png)<!-- {"width":730} -->
It shows a popular diagram in which, in the center, we have a dotted line that should represent an API of an AI or machine learning model. // API level boundary

![](40%20-%20What%20is%20an%20AI%20Engineer%20-%20r2r/image%202.png)
On the left side of the API, we have Job Roles like ML Researchers, ML Engineers and Data Scients who’s job is to build models from scratch and build APIs so that Job Role on the left of the API boundary, like 

![](40%20-%20What%20is%20an%20AI%20Engineer%20-%20r2r/image%204.png)

the AI Engineer and the Fullstack Engineer can use this API and build production-ready products on top of it. 

![](40%20-%20What%20is%20an%20AI%20Engineer%20-%20r2r/image%205.png)


AI Engineers are more product-focused. 
The API line is permeable, though.  
Depending on the amount of ML knowledge you have, you will sometimes cross the API line as a AI Engineer, for instance if you do model fine-tuning you could even train your own ML model for certain use cases. 

## Just a fancy name?

Okay, so we learned that an AI Engineer is someone, who builds app on top of foundation models…. When I first heard this definition, I was a bit skeptical and thought - well, this is just a fancy name for a Software Developer who knows how to talk to the OpenAI API. 

As you have seen in a recent lesson, it is really easy to talk to an LLM and we have already performed a call to an LLM of OpenAI, which only took a couple of minutes to do. So does this activty really deserve it’s own Role - the “AI Engineer”?

Well, while it is really easy to build MVPs, prototypes or demos, the real challenges arise when such an ai-based application should be released to production. 

Andrew Karpathy, a veteran in the field of AI and machine learning, once said this: 
https://x.com/eugeneyan/status/1672692174704766976
![](40%20-%20What%20is%20an%20AI%20Engineer%20-%20r2r/image.png)

He said this specifically in the context of building AI agents, however, I think this holds true in general for all ai-based applications: They are easy to build and run nicely in a controlled setting, however operating them reliably at scale is much more difficult. 

## Challenges of deploying AI-based apps to production

But there is a huge difference between a **prototype, demo, or MVP** and a **production-ready AI-based application**.

| Prototype / Demo / MVP                                       | production-ready ai-based application                        |
|--------------------------------------------------------------|--------------------------------------------------------------|
| Monitoring + Evaluations<br>- Not required                   | Monitoring + Evaluations<br>- How can we make sure our app is running without errors in production?<br>- non-deterministic |
| Cost: <br>- Just use the latest frontier model from OpenAI or Anthropic<br>- Context Size doesn’t matter | Cost: <br>- What’s the cheapest model we can use that “gets the job done”<br>- Context needs to be optimized to save costs<br>- Prompt Caching |
| Latency: <br>- It’s fine if responses are slow               | Latency: <br>- are users happy with the speed of the responses? |
| Input: <br>- Happy Path<br>- Clean Input                     | Input: <br>- Messy<br>- unexpected                           |
| Deployment<br>- Not Required                                 | Deployment<br>- How and where should we deploy our app?<br>- How should our CI/CD pipeline look like? |
| Inference Service to use<br>- doesn’t matter                 | Inference Service to use<br>- model provider? hyper-scaler? Own infrastructure? |
| Robustness: <br>- Error Handling not implemented             | Robustness: <br>- What’s should the system do on errors? Problems with LLM responses when they are in an incorrect format?<br>- Validations, Guardrails, Retries, Fallbacks |
| Safety / Security<br>- Ignored                               | Safety / Security<br>- Users may try to manipulate the model, extract sensitive information, or force the system into unwanted behavior. |
### Monitoring and Evaluations

In a prototype, monitoring and evaluation sets are not important. A prototype should only prove that something is possible. You use it, maybe with a few examples, and if the outputs look good enough, you move on. That is totally fine for a prototype. 

However, after shipping an ai-based app to production, we always need to know if our application is actually working as expected. 
We need to think about how we can set up dashboards to see information like the current latency of our feature the error rate, and in case of a high error rate we want to have an infrastructure that sends alerts so that we can check our system. 

Collect logs and an easy way to inspect the logs. 

Monitoring is especially challenging with AI systems, because their outputs are often **non-deterministic**. The same input may produce slightly different outputs. And even if the output looks "good", that does not automatically mean it is correct, useful, or safe.

One concept that helps us identify if an ai-based application is behaving incorrectly is the concept of Evaluations, or evals in short. Evals are a big topic in this course, as I think it’s the one skill that an AI Engineer needs to master. 

track latency?

### Cost

In a prototype, cost usually does not matter much. 

Model Selection
There, it’s totally fine to just use the most powerful frontier model by OpenAI, Anthropic or another lab. 
For production apps however, costs become a concerns and calls to these frontier models can become quite expensive, so we have to ask the question “What’s the cheapest model we can use that still gets the job done?”. 

How can we answer this question? Well, by defining a set of evaluations or evals, and execute those agains cheaper and cheaper models until we find the cheapest one that still fulfills our evaluations. 

Context Size
Having a lot of context in the prompt that we send to an LLM can be very expensive. In prototypes, we usually don’t pay much attation regarding keeping context small - we load a lot of information into it so that we get the bets results possible. 
In production, though, we need to keep the context size, and therefor the costs, in control. We need to optimize what ends up in our context. 

Prompt Caching
Also prompt caching needs to be considered!

### Latency

Latency is another area where prototypes and production systems differ a lot.
In a prototype, slow responses are often acceptable.
If the answer takes five or even ten seconds, nobody really cares. You are just testing whether a feature works at all.

But in production, users care a lot.
Once real people are using your application, response speed becomes part of the product experience. If the system feels slow, users are less likely to use it much. 

And that means AI Engineers have to think about things like model choice, streaming, context size, parallelization, infrastructure, and architectural trade-offs.

### Input Quality

In prototype demos, you usually only see the happy path, so input that is very clean and represents the main use cases of the product for which the system performs nicely. 

But production is messy.
Real users do not behave like the person who built the demo. They write unclear prompts, provide incomplete information, make mistakes, ask unexpected questions, and interact with the system in ways you did not anticipate.

That means AI Engineers need to make sure that production systems are able to handle messy, unpredictable input. 

### Deployment

Protoypes are usually running locally or a deployed on a machine reachable just within the company network. 

Once an app goes live, it needs to be accessibly by a much larger group of users. 
Now you need to decide where the application should run, how it is deployed, how environments are managed, how secrets are handled, and how changes are rolled out safely.

You also need to think about CI/CD, how to test prompt and model changes, and how can we roll back if something goes wrong. 

Furthermore, when you are going to release a new ai-powered feature to your application, you maybe don’t want to release it to all users immediately, but only to a small percentage of users - maybe 10% and collect their feedback to see if the new feature is actually usefull for them. Setting up such a A/B testing infrastructure is also often one of the AI Engineers responsibilities.

### Inference Service

What is an Inference Service? Inference simply means “running a model”, so actually processing the input prompt and working on the result. 

There are different providers that you can use as a Inference Service. In the previous lecture in which we performed our first call to an LLM, we used the OpenAI API as an inference service, so the model provider directly. Of course, you can also use the other model labs, like Anthropic or Google, but there are also other alternatives. 
You could, for instance, use a cloud hyperscaler like AWS, Azure or GCP. These hyperscalers also host some foundational models. 
Also, while much more complex, you can also host a model yourself. 

For prototypes, you mostly just choose the inference service that is the most easy to plug into your app. You don’t think about it too much, as costs and latency usually doesn’t matter that much. 

But in production, the decision about which inference service you should use becomes much more important.
Now you have to think about trade-offs:
- Should we use a model provider directly?
- Should we use a cloud hyperscaler?
- Should we host models ourselves?
- What about pricing, latency, reliability, rate limits, compliance, and vendor lock-in?

Depending on your use case, the right answer can look very different. 

### Robustness

Usually, you have to search very long for error handling code in prototypes. 
Handling error paths gracefully are not in scope of prototypes most of the time. 

If an error happens, maybe you just reload the page. If the output is malformed, you manually try again. If the model behaves strangely, you ignore it for now.

But in production, robustness becomes essential.
Now you have to define what the system should do when things go wrong.

- What happens if the model returns output in the wrong format?
- What happens if the request times out?
- What happens if the provider is temporarily unavailable? 
- What happens if the answer is clearly broken or low quality?

This is where concepts like validation, guardrails, retries, fallbacks, and error handling come in.
Because in production, failures  are guaranteed to happen.
An AI Engineer needs to design systems that handle them well.

### Safety and Security

And finally, there is safety and security.
In a prototype, these topics are often ignored because the first goal is simply to see whether the idea works.

In production though, safety and security become really important. 

Real users may try to manipulate the system. They may intentionally or unintentionally trigger harmful behavior. They may try to extract sensitive information, bypass rules, or exploit weaknesses in your prompt or workflow.

That means production systems need protections that are implemented by AI Engineers.

## Wrap Up

Let’s wrap up this important lecture!

Its mainly an engineering role, not a research / scientific role. 

Now you know what an AI Engineer is and know all about the difference of building a quick prototype and shipping a reliable ai-based application to production. 

In this course, I try to equip you with all the necessary AI engineering skills to ship reliable ai-based applications to production, so that you get a job as an AI engineer fast!

==🟢Nice AI generated image that shows AI Engineering and powerful cool builders==

Alright! Now you know everything about AI Engineering! 💪

AI Engineers are builders who want to leverage foundation models to build cool production products that solve real-world problems on top of them.



## Random
- an AI Engineer is a Software Engineer who knows how to productionize AI
