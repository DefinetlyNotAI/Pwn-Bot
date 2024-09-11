# AutoPCAP Project

## Table of Contents
- [Introduction](#-introduction)
  - [Overview](#-overview)
  - [Purpose](#-purpose)
- [Installation](#-installation)
  - [Prerequisites](#-prerequisites)
    - [For Pwngotchi](#-for-pwngotchi)
    - [For Discord Bot](#-for-discord-bot)
  - [Steps for Installation](#-steps-to-install)
    - [Pwngotchi Configuration](#-pwngotchi-side)
    - [Discord Bot Configuration](#-discord-bot-side)
- [Configuration](#-configuration)
  - [Pwngotchi Configuration](#-pwngotchi-configuration)
  - [Discord Bot Configuration](#-discord-bot-configuration)
- [Usage](#-usage)
  - [Pwngotchi Usage](#-pwngotchi-usage)
  - [Discord Bot Usage](#-discord-bot-usage)
- [Bot Reactions Glossary](#-bot-reaction-glossary)
- [Troubleshooting and Support](#-troubleshooting-and-support)
  - [Pwngotchi Side Troubleshooting](#-pwngotchi-side-troubleshooting)
  - [Discord Bot Side Troubleshooting](#-discord-bot-side-troubleshooting)
  - [Common Issues](#-common-issues)
    - [Plugin Loading Issues](#-plugin-not-loading-pwngotchi-side)
    - [Discord Upload Fails](#-discord-upload-fails-both)
    - [Log File Issues](#-log-file-issues-both)
    - [Plugin Configuration Issues](#-plugin-configuration-issues-pwngotchi-side)
- [Frequently Asked Questions](#-frequently-asked-questions)
  - [Can I use multiple webhook URLs?](#-can-i-use-multiple-webhook-urls)
  - [How do I update the plugin?](#-how-do-i-update-the-plugin)
  - [Is there a way to filter `.pcap` files?](#-is-there-a-way-to-filter-pcap-files)
- [Contributing](#-contributing)
- [Support and Community](#-support-and-community)
- [Donations](#-giving-back)
- [License](#-license)
- [Additional Resources](#-additional-resources)
- [Contact](#-contact)

## 📜 Introduction

### 🪟 Overview

This project integrates an AutoPcap plugin
with a Discord bot to automate the capture and analysis of `.pcap` files.
The AutoPcap plugin enhances Pwngotchi's capabilities
by automating the upload of captured packets to Discord via a webhook.
Simultaneously, the Discord bot facilitates interaction with Discord servers,
specifically managing messages related to pcap files. 
It extracts, decrypts, and analyzes these files, 
offering a streamlined workflow for cybersecurity enthusiasts.

### 📖 Purpose

The primary aim of this project is to simplify 
the process of capturing, uploading, and analyzing network traffic 
for educational and cybersecurity purposes.
By automating these tasks, users can focus more on analysis rather than manual processing.

## 📦 Installation

### 📄 Prerequisites

#### 🧠 For Pwngotchi

- Ensure Pwngotchi is correctly set up and operational without any plugins initially.
- Familiarity with Pwngotchi's operation and configuration.

#### 🤖 For Discord Bot

- Python 3.x installed.
- Access to the Discord Developer Portal.
- Basic knowledge of Discord bot development.
- A Linux environment for running the bot's code due to specific requirements in the cracking function.
  - Kali Linux is recommended for ease of use and availability of necessary tools.
  - Required Linux Packages: `airmon-ng`, `tshark`, `editcap`, `pcapfix`.

### 🪜 Steps to Install

#### 🛜 Pwngotchi Side

1. Clone the repository or download the plugin script.
2. Place the `AutoPCAP.py` script in the `/usr/local/share/pwngotchi/custom-plugins/` directory on your SD card.
3. Modify your Pwngotchi configuration file (`/etc/pwngotchi/config.toml`) to enable custom plugins by adding or updating the line:
   ```toml
   main.custom_plugins = "/usr/local/share/pwngotchi/custom-plugins/"
   ```

#### 🤖 Discord Bot Side

1. Clone the repository or download the Discord bot script.
2. Place the `Bot.py` script in a suitable location on your computer/SD card.
3. Configure the script to start automatically on boot with sudo permissions.

## 🛠️ Configuration

### 🛜 Pwngotchi Configuration

Create a `config.json` file in the plugin's directory with the following structure:
```json
{
  "webhookUrl": "YOUR_DISCORD_WEBHOOK_URL_HERE"
}
```
Replace `"YOUR_DISCORD_WEBHOOK_URL_HERE"` with your actual Discord webhook URL.

### 🤖 Discord Bot Configuration

Discord Bot Creation
1. Visit the [Discord Developer Portal](https://discord.com/developers/applications).
2. Create a new application and add a bot to it.
3. Make sure the bot has these permissions when creating it:
   - View Channels
   - Read Message History
   - Send Messages
   - Manage Messages (for clearing reactions)
   - Add Reactions
   - Attach Files
   - Create Invites
4. Make sure all the intents in the `intents` section are enabled, these are found in the `oauth2` section.
5. Make sure the bot is added to the server you want to interact with.
6. Navigate to the bot page and copy the bot token. This token will be used later.

Account Activation
1. Activate your Discord account for developer mode to access channel IDs.
2. Go to your account's settings and navigate to the "Advanced" tab.
3. Enable "Developer Mode" and click "Save Changes".
4. Go to your 2 channels in your server and copy the channel IDs of a channel where pcap files should be sent (by the webhook, for security reasons make it a public restricted channel where only mods can talk in it) and a channel where logs should be sent (For privacy reasons, this should be a private channel).

Configuration
1. Update the `api.json` file with your bot's token, channel IDs, and other necessary configurations as per the instructions below.
2. Replace placeholders in the code with actual usernames and passwords as needed. Ensure to follow the format specified in the comments.
3. The bot's behavior and settings are configurable through the `api.json` file located in the project directory. Here's what you need to know:
   - **Token**: Your bot's token obtained from the Discord Developer Portal.
   - **Channel IDs**: Two channel IDs are required:
     - `channel_id_(for_pcaps)`: The ID of the channel where pcap files should be sent.
     - `channel_id_(for_logs)`: The ID of the channel where logs should be sent.
   - **Webhooks Username**: A list of usernames that the bot should respond to. Include `#0000` for webhook usernames.
   - **Log Using Debug**: A boolean value indicating whether to log using debug level, for production purposes set this to `false`.


Running the Bot
1. Ensure you have Python installed on your system.
2. Install required Python packages from the `requirements.txt` file using pip.
3. Run the bot in a Linux environment with sudo privileges for cracking purposes.

## 🚦 Usage

### 🛜 Pwngotchi Usage

After installation and configuration, 
the AutoPcap plugin will automatically capture `.pcap` files and upload them to Discord
upon detecting handshakes. The plugin logs all activities, aiding in tracking progress and troubleshooting.

The plugin is able to upload `pcap` files only if connected to the internet. 
To do that follow this [guide](https://www.youtube.com/watch?v=z5yb43PlhEA).

### 🤖 Discord Bot Usage

Ensure the bot is running in a Linux environment with sudo privileges.
Users can interact with the bot by sending messages in the configured channels,
triggering responses based on message content and settings.

## ⚙️ Bot Reaction Glossary

The bot will generate many types of reactions to respond to various messages that include the pcaps uploaded.
As part of its job, if an error occurs a reaction will be generated, 
and if a pcap has already been cracked, a different reaction will be generated.
Here they are:-

### ⛔ Reaction
The bot is not running in a linux environment.

### 👍 Reaction
The bot successfully cracked and uploaded the pcap file.

### 👎 Reaction
The bot failed to crack the pcap file.

### ❔ Reaction
An unknown return occurred in cracking process

### ❌ Reaction
An error with python occurred, cracking failed

### 🚫 Reaction
An error occurred with discord, processing failed, usually relating to permissions, 
this is an exception for HTTP errors

### ⚠️ Reaction
An unknown exception was caught, an error that handles the discord bot, occurs if the error
is not related to HTTP errors

### ⁉️ Reaction
The whole script failed without any handling, this is unexpected and shouldn't happen

### 👀 Reaction
The bot is handling the pcap currently, will later give it a different reaction

## 🐛 Troubleshooting and Support

### 🛜 Pwngotchi Side Troubleshooting
If you encounter any issues, check the following:
- Ensure your `config.json` file is correctly formatted and contains a valid Discord webhook URL.
- Verify that Pwngotchi is configured to use custom plugins.
- Check the plugin logs for any error messages.

### 🤖 Discord Bot Side Troubleshooting
If you encounter any issues, check the following:
- Ensure your `api.json` file is correctly formatted and contains valid channel IDs.
- Verify that the bot is properly configured.
- Check the bot logs for any error messages.
- Ensure the bot is running in a Linux environment with sudo privileges.
- Make sure the bot has proper [permissions](#-discord-bot-configuration) in the server.

### 💬 Common Issues
Here are some common issues and solutions to help you get back on track:-

#### 🔃 Plugin Not Loading (Pwngotchi Side)
- Ensure the plugin is placed in the correct directory as specified in your Pwngotchi configuration file.
- Verify that the `config.toml` file has been correctly updated to include the path to custom plugins.

#### ⏱️ Discord Upload Fails (Both)
- Check your internet connection to ensure it's stable.
- Verify the webhook URL/token in your `config.json` file is correct and active.
- Ensure the Discord channel associated with the webhook allows file uploads.

#### 📜 Log File Issues (Both)
- If the log file grows too large, consider reducing the `max_size` parameter or implementing a log rotation mechanism.

#### 🔌 Plugin Configuration Issues (Pwngotchi Side)
- Ensure your `config.json` file is correctly formatted and contains a valid Discord webhook URL.
- Verify that Pwngotchi is configured to use custom plugins.

## ❓ Frequently Asked Questions

### 📶 Can I use multiple webhook URLs?

- Currently, the plugin supports one webhook URL. Modifications can be made to support multiple URLs.

### 🔃 How do I update the plugin?

- Replace the existing `AutoPcap.py` script with the new version in the `/usr/local/share/pwngotchi/custom-plugins/` directory. Restart Pwngotchi to apply changes.

### ⚙️ Is there a way to filter `.pcap` files?

- Customize the `on_handshake` function to filter `.pcap` files based on criteria such as file size, SSID, or timestamp.

## 📈 Contributing

Contributions are encouraged! Fork the repository, make changes, and submit pull requests.
Contributions to improve functionality, security, and usability are welcomed.

We would appreciate any contributions to the `crack` function.

## 📢 Support and Community

Join the Pwngotchi and Discord communities for support, discussions, and feature requests. Active forums and Discord channels offer assistance.

## 🌟 Giving Back

Consider contributing to the project, sharing experiences, or supporting the developers through donations.

## 📜 License

This project is licensed under the MIT License. See the LICENSE file for details.

## 📚 Additional Resources

- Pwngotchi Official Documentation: [https://pwngotchi.net/](https://pwngotchi.net/)
- Discord Developer Portal: [https://discord.com/developers/docs](https://discord.com/developers/docs)

## 📧 Contact

For inquiries, feedback, or contributions, please contact Shahm Najeeb using my [email](mailto:Nirt_12023@outlook.com)
