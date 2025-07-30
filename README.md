# Pill Minder

This is a multi-user medication reminder application with a web interface and Telegram notifications.

Warning: The application is still under development and contains many issues!

## Features

- Multi-user system with registration and login.
- Web dashboard to view and manage medications.
- Mark medications as 'Taken' from the web interface.
- Actionable Telegram notifications to mark medications as 'Taken'.
- Medication information lookup using the British National Formulary (BNF).

## Setup

### 1. Create a Telegram Bot

1.  Talk to the [BotFather](https://t.me/botfather) on Telegram.
2.  Create a new bot by sending the `/newbot` command.
3.  Follow the instructions and get your bot token.
4.  Get your chat ID by talking to the [userinfobot](https://t.me/userinfobot) on Telegram.

### 2. Set Environment Variables

Create a `.env` file in the project root and add the following:

```
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
SECRET_KEY=a_very_secret_key
```

Replace `your_telegram_bot_token` with the token you got from the BotFather.
Replace `a_very_secret_key' with a secure key

### 3. Build and Run the Docker Container

1.  Build the Docker image:

    ```bash
    docker build -t pill-minder .
    ```

2.  Run the Docker container:

    ```bash
    docker run -p 5000:5000 -v $(pwd):/app pill-minder
    ```

    The application will be available at [http://localhost:5000](http://localhost:5000).
