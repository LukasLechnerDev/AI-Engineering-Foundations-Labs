# 3- Your first LLM call - r2r

## Summary
- define API key
- First call to OpenAI API

## Intro

Okay so now that we have a working development setup, it's time for our first interaction with an LLM. In this video we now will make a call to the Open AI API for the very first time. 

I have already opened up the file `1-first-llm-call.ipynb`

## Generate OpenAI token

To communicate with the Open AI API, we need an API key.
I will now show you how to create and use an Open AI API key. 

The OpenAI API key needs to be stored in the .env file. The project already contains a .env.example file and this file can be used as a template for the actual .env file. 

Let's open up the terminal and use `cp dotenv.example.env` to just copy the example file as a new .env file. 

In the dotenv file you can see that this is the place where we need to paste our API key later. It's really important that this API key is not leaked so this API key should not be stored in the repository. 

The .gitignore file of this project already defines that the dotenv file should not be tracked by git but in your own projects you have to be really careful not to commit your keys and push them to GitHub for instance. 

Operating a LLM costs a lot of money for OpenAI, and whenever we perform a call to the OpenAI API, we need to pay for some of the costs. That’s why for this course we need to spend some money in order to buy credits so that we can perform requests to the OpenAI endpoints. 

If you don’t want to spend any extra money, or if there are any other reasons why buying credits is not an option for you, then this is not a problem. In the next lecture I will show you how to install a small model on your machine that you can use for free. But of course, these small local models are not as powerful as the big foundation models that are hosted by OpenAI or Anthropic. 

If you are willing to spend some money on credits - and I highly recommend that you at least spend the minimum amount of $5, then you need to head over to [OpenAI Platform](https://platform.openai.com/api-keys) . I assume you are a ChatGPT user and already have an OpenAI account, but if not, you first need to create one. 

In the OpenAI Platform, you now need to click on “Create new secret key” on the top right. Then you can give it a name, like “Key for AI Engineering Foundamentals Course”, and click “create secret key”. 

Then, a new key is generated, and you have the option to copy that key into your clipbard, and then paste it into the `.env` file. 


### Import dependencies

Let's switch back to the notebook. 
So now that we have defined the api key, the next thing is to import some dependencies by executing this first cell here.

Whenever we execute a cell in a new Jupyter notebook, we first have to select the kernel we need. As in the previous lecture we need to select the virtual environment of our project, the one that is highlighted with a star here in Visual Studio Code. 

If you can't see this option, then this probably means that you didn't execute `uv sync`. If that is the case, just open up the terminal and do a `uv sync`. After doing this, you should now have a `.venv` folder and you should be able to select this virtual enviroment as the kernel for this notebook. 

So this first cell here imports os - which is a standard library python module that comes with python itself. 

The other two dependencies, “dotenv” and “openai” are third party packages that do not come bundled with python. Usually we have to use `pip install` first to add those dependencies, but since we are using `uv`, and in the last lecture we have run `uv sync` these dependencies are already installed in our virtual environment. 

To verify that, we take a look into our virtual environment - so the `.venv` folder in the root folder, and open up the `lib` folder, you can see that this virtual environment already contains `dotenv` and `openai`.

When we use uv, then all dependencies of our virtual environment are defined in `pyproject.toml` file in the root folder.

When we open up this file, we can see that the OpenAI and dotenv dependencies are defined with their respective version numbers.

## Checking API Key
The next code cell in the notebook stores the open-ai-api-key from the `.env` file as an environment variable and makes sure that we have correctly set the API key in our `.env` file. The `load_dotenv()` function will define all variables from the .env file as environment variables. The `override equals true` parameter defines that if an environment variable with the same name as the one in the `.env` file already exists, it is overritten. 
The exact name of the environment variable is defined in the OpenAI docs: [Developer quickstart](https://developers.openai.com/api/docs/quickstart). As you can read here that if an environment variable with that name exists, then the open-ai sdk will automatically read the key from there. 


In the next codeline, we can then read the OpenAI API Key from the environment variables and store it in the `api_key` variable. 

Afterwards, int the if-else condition, we check the content of the `api_key` variable. If it is empty, “No APIkey defined …” is printed out. 
If there is an `api_key` but it doesn’t start with `sk-proj-`, then it is printed out that the API key is in the wrong format. 
If the Api Key is in the right format - then everything is fine. 
When I execute this cell… 
… then `API key was defined with the correct format!` is printed out, and this should also be printed out for you. If you get a different message printed out, then there is some problem with your API key, so please make sure that you have correctly defined in you `env` file!
Maybe rewatch this lecture from the beginning to check where you have made a mistake.

## Define Prompt
Okay, so now that our API key setup is fine, we can define our first prompt, which we will later send to an LLM. 

But first we are going to initialize a new client with the python OpenAI sdk by defining `client = OpenAI()` 

In the next line, we define the prompt. 
The prompt I have defined here is “This is my first programmatic interaction with an LLM, I’m so excited”. You can leave the prompt as is, or adjust it to whatever you want to send to the LLM. 

## First LLM interaction

Next, we already perform the call by using the Responses api. So we call `client.responses.create`, define the model and the prompt as input!

Of course, we will dive deeper into the OpenAI Api in module 3 and I will show you all of the important options you need to know as an AI Engineer there, for now, I just want to show how easy and quick it is to talk to an LLM.

Last but not least we simply print out the output_text field of the response. 

So let's run this cell, and, as you can see, it takes a couple of seconds, and then… Boom - we have our first response from OpenAI telling us …


So this should demonstrate how easy it is to get started with the python sdk. Within minues, we have set up everything we need and are ready to interact with the most powerful models in the world. 
