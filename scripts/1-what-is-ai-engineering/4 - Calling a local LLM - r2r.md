# 4 - Calling a local LLM - r2r

### Summary
- use local LLM to save costs
- ollama installation
- calling ollama model

There is an academind course on that topic

## Introduction

In the previous video, we interacted with a powerful model hosted by OpenAI. 
In order to be able to do this, we had to buy some credits. 
In this lecture, we are now going to take a look at how we can use large language models for free, by installing ollama and pulling and running an oss model locally on our machine.

## Ollama installation
![](4%20-%20Calling%20a%20local%20LLM%20-%20r2r/image.png)<!-- {"width":398} -->
To install ollama, we need to head over to ollama.com and then simply copy-paste this command here into a terminal and execute it. The other option is to click on “download Ollama” here, and then depending on your operating system you can simply download an installer and install it as you would install any other software. 

Ollama comes with a graphical UI, but we will just use the terminal interface in this lecture. 

Once installation is done, you can check if everything works as expected by running `ollama` in your terminal. Then you should see the options to - run a model, launch Claude Code - and so on. 
![](4%20-%20Calling%20a%20local%20LLM%20-%20r2r/image%202.png)<!-- {"width":343} -->

You can escape this again with Esc. 


## Model download

==🟡TODO: Improve this once I have more knowledge about parameter sizes, oss models etc.== 

> Info from academind video (link below): Take the parameter amount in billion, double that and then you have the gigabyte amount that you need to run locally to have an estimate about how much memory you need. 1b => 2GB of memory, preferably GPU memory

> Frontier models are of course more capable, but local models can still be useful for some tasks like summarizing or creating text

Okay, so now that ollama is running, we can now download our first open source model and run it locally. To see which models are available for Ollama, simply go to the ollama website and click on “Models”.
Here, you can see some models that are currently popular, like …
An important model property to take into consideration is the parameters size. 
In general, its true that the more parameter a model has, the more powerful it is. However, a greater amount of parameters also means that the machine we need to run the model on needs to be very powerful. 
The most powerful models on the planet, like the ones from Anthropic, OpenAI and Google run on hardware with the most powerful GPUs in the world. These models have XYZ parameters. 

Locally, we can’t run these newest frontier models - they aren’t opensource anyway - So we have to pick a model with a smaller number of parameters.

As a recommendation, we can use the Gemma model from Google - the one with 4Billion parameters. So let's download this model with `ollama pull gemma3:4b`.

This takes a little bit, but once it is pulled we can start interacting with the new model by just executing `ollama`, and then select `Run a model (gemma3:4b)`.

Then it takes a little bit for the model to start up, and then we can talk to it like with chatGPT, and can ask for “Who are you?” for instance, and the local model response with: …

So nice, we have installed our first local oss model and now we have the option to use a model that runs on our computer - for free!

## Using local ollama model with openAI Python SDK

A great thing about ollama is that it is OpenAI compatible. This means that the ollama endpoints are defined exactly like the one’s from OpenAI and so we can also use the OpenAI python sdk to communicate with our locally running ollama models.

So here we have almost the same code as in the last video when we talked to gpt-5.4-nano that was hosted on the OpenAI servers, the only difference is that when we initialize the client, we do it with a different base-url `localhost:11434/v1` - so the localhost with ollama’s default port `11434` and the `v1` that stands for version 1 of the api. 

We also have to specify an `api_key` to a random value, like `ollama` here. Otherwise, we are getting an error when here at client initialization. 

And that’s all we have to do! As a prompt, I have again defined `Who are you?` and when we now run this cell, we get a similar answer as before: “Hi there! ….”

And that’s all for this video! We now have a working setup that allows us to write python code and utilize a locally running model. 

If you like you can play around with ollama - maybe download some different models and try out different prompts!

See you in the next lecture!

## Sources: 
https://pro.academind.com/courses/ai-agents-workflows-the-practical-guide/lectures/62110808

