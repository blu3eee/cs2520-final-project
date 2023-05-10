# Programming in Python - Discord Bot Project

## Table of Contents

- [Introduction](#introduction)
- [Problem Statement](#problem-statement)
- [Design Ideas](#design-ideas)
- [Key Python Features](#key-python-features)
- [Conclusion](#conclusion)

## Introduction

This project is part of the Programming in Python class, focused on creating a Discord bot using Python and the Nextcord library. The primary goal is to create a functional and useful bot that can be easily deployed on Discord servers.

## Problem Statement

With the growing popularity of Discord as a communication platform, server administrators are looking for ways to enhance user experience and manage their communities more effectively. Many servers require bots that can perform various tasks, such as moderating content, managing roles, and providing utility functions for users.

The problem this project aims to solve is to create a customizable and extensible Discord bot that can be deployed on any server to provide useful features and improve server management.

## Design Ideas

To solve this problem, the following design ideas were implemented:

1. Use the Nextcord library to interact with the Discord API and build the bot's functionality.
2. Create a modular design using Cogs to allow for easy addition and removal of features.
3. Store necessary data in JSON files for easy data management and persistence.
4. Use a command prefix and aliases to allow users to interact with the bot easily.
5. Implement error handling and logging to ensure the bot runs smoothly and issues can be identified and resolved.

## Key Python Features

The following Python features were utilized in solving the problem:

1. Object-oriented programming (OOP) - Used to create classes and methods for the bot's functionality and Cogs.
2. JSON module - Used to read and write data to JSON files for data storage and persistence.
3. Regular expressions (re module) - Used for matching and parsing command arguments.
4. List comprehensions and generators - Used for efficient data manipulation and processing.
5. Asyncio and coroutines - Used for asynchronous programming and non-blocking operations with the Discord API.

## How to Run

To run the Discord bot, follow these steps:

### Setting up the Discord bot

1. Create a new Discord bot on the [Discord Developer Portal](https://discord.com/developers/applications). Follow the steps to set up your bot and obtain its token.

2. Add the bot to your Discord server using the generated invite link.

### Installing python & libraries

1. Make sure you have Python 3.8 or higher installed on your system. You can check your Python version by running `python --version` or `python3 --version` in your terminal or command prompt.

2. Install the all the necessary library using pip:

```
pip install -r requirements.txt
```


### Running the bot

1. Clone or download the repository to your local machine.

2. In the root directory of the project, create a `.env` file and add your bot token:

```
# in .env file
BOT_TOKEN=your-bot-token-goes-here

```

Replace `your-bot-token-goes-here` with the actual token you obtained from the Discord Developer Portal.

3. In the terminal or command prompt, navigate to the project directory and run the following command:

```
python main.py
```

Alternatively, you can use `python3 main.py` if your system uses Python 3 as `python3`.

4. The bot should now be online and ready to use in your Discord server. Interact with the bot using the configured command prefix and available commands.

Note: To stop the bot, press `Ctrl + C` in the terminal or command prompt where it is running.

## Conclusion

This project successfully created a Discord bot using Python and the Nextcord library, providing a modular and extensible solution for server administrators. By implementing the design ideas and using key Python features, the bot offers an easy-to-use interface for users and improved server management capabilities.
