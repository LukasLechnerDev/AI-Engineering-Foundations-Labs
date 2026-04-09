# 2 - Development Setup - r2r

### Summary
- Enable the student to perform the first LLM call on their system as fast as possible
  - What are Jupyter Notebooks
  - How to install UV and initialise the project

## Jupyter Notebooks

As you can see in the Visual Studio Code explorer, every module has its own dedicated folder that contains code snippets and full projects that are related to the module. Let's open up the folder of the current module `1-introduction` and take a look at the Jupyter notebook `0-development-setup.ipynb`

The file extension IPYNB stands for i Python notebook. If you are a ML Engineer or Data Scientist, you are probably very familiar with Jupyter notebooks. If you are a Software Engineer, maybe a Frontend, Backend or Mobile Engineer, you might see such a notebook for the first time, so let me briefly explain what these notebooks are all about. 

A jupyter notebook usually consists of multiple cells, so this here is a cell… and this is a cell, and every cell consists of either markdown or code. These first cells - “Development setup”, “Visual Studio Extensions” are all markdown files. We can add new cells by clicking on these +Code or +Markdown Buttons. With the “Generate” button, we can use AI to help us with the definition of new cells. 

If we scroll down a little bit, you can see that this here is a first simple  *code* cell. We will execute it later to check if our development environment is correctly set up. This code cell is python code. 

## Python
The programming language we will use in this course is Python. As you will see later in the course, when we analyse some job postings for AI Engineers, you will see that Python is the number 1 programming language for AI Engineers, and every AI Engineer has to have a good knowledge of it. This course, however, doesn’t teach the basics of Python, as there are plenty of other good resources for learning it. Python is really easy to read and understand so if you already have knowledge in another programming language like JavaScript or Java or C#, it should be no problem to understand the code in this course. 

## VS Code Extensions

There are 2 VS Code extensions that we need to install: 
The first one is the Python extension to get proper Python language support. You can install the extension by clicking on extensions on the left sidebar, search for “Python”, and install the extension from microsoft. As you see, I have already installed this extension, so I can only uninstall it, but for you it should show install and thats the button that you should click. 

The second Extension that we need is the support for Jupyter Notebooks. Therefore, let's search for “Jupyter” and, here again install the plugin from microsoft. 

- Python Extension - ms-python
- Jupyter ms-toolsai

### UV Setup

See notebook


## Ruff ? 
auto-formatting on save

---
Python setup is not requried because we use UV
## Python Setup - NOT required when using UV

Now that we have cloned the repo, we can go into the `1-introduction` folder and open up the Jupyter Notebook called `0-developer-setup.ipynb`. 

Let's make sure that Python is properly installed on your machine. This can be done by opening up a new terminal and executing `python3 --version` on Mac and Linux - or `python` without the `3` on Windows. Make sure you get a version that starts with `3.x`. I am using a Mac, and Python was already preinstalled on my machine. 

Terminal commands can also be executed directly in a notebook by starting the command with an exclamation mark. So if I execute this line here, you can see that Python is installed on my machine.

If you don’t have Python installed, please check out the official Python guide on how to install it. You can find the link in the Notebook. 
> Open Python Guide

In the Guide, you can find the installation instructions for Unix-based Systems, Windows, and Mac. 
> Highlight different sections

# Python Installation

First we need to make sure if Python is properly installed: 

This can be done by opening up a terminal, and executing: On mac and linux: `python3 --version` and on windows `python --version`

You can also try to run this version directly in this notebook by executing the  (you can use `!` to run terminal commands)

If that doesn't work, then Python is not yet installed on your machine. Please follow the official Python guides to install it: 
- https://docs.python.org/3/using/index.html
