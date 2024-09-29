# MS Teams Chat Bot with OpenAI Integration

This is a Python-based chat bot application that integrates with the OpenAI API to simulate conversations similar to ChatGPT. The bot is built using `aiohttp` for handling requests and leverages the OpenAI API for generating responses. Additionally, it integrates with the **Microsoft Bot Framework**, supports **OAuth2** authentication, and implements **WaterfallDialogs** for managing complex conversations.

## Features
- **Asynchronous OpenAI API Integration**: Uses OpenAI's GPT-3.5-Turbo model to generate conversational responses asynchronously.
- **Bot Framework Integration**: The bot leverages the **Microsoft Bot Framework** to manage incoming requests and respond to user messages.
- **OAuth2 Authentication**: Securely handles user authentication using **OAuth2** through the **Bot Framework**.
- **Waterfall Dialog Implementation**: Manages complex, multi-step conversations using the **WaterfallDialog** pattern, guiding users through a sequence of prompts and responses.
- **Conversation History Management**: Keeps track of the conversation history using user and assistant roles, ensuring contextual responses from OpenAI.
- **Dockerized for Easy Deployment**: The entire application is containerized, allowing for easy setup and deployment using Docker.

## Prerequisites
Before running the application, ensure you have the following installed:
- **Docker** (For running the app in containers)
- **Docker Compose**
- **Poetry** (For managing Python dependencies)

