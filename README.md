# Microsoft Bot Setup Guide

This guide will walk you through the process of setting up a Microsoft Bot, including creating necessary resources in the Azure Portal and configuring ngrok for local development.

## Table of Contents

1.  [Prerequisites](#1-prerequisites)
2.  [Azure Portal Setup](#azure-portal-setup)
    * [Create a Resource Group](#create-a-resource-group)
    * [Create an Azure Bot Resource](#create-an-azure-bot-resource)
    * [Configure Channels](#configure-channels)
    * [Get Bot Credentials](#get-bot-credentials)
3.  [Local Bot Development Setup](#local-bot-development-setup)
    * [Clone your Bot Project](#clone-your-bot-project)
    * [Install Dependencies](#install-dependencies)
    * [Configure Environment Variables](#configure-environment-variables)
4.  [Ngrok Setup](#ngrok-setup)
    * [Download Ngrok](#download-ngrok)
    * [Authenticate Ngrok](#authenticate-ngrok)
    * [Start Ngrok Tunnel](#start-ngrok-tunnel)
5.  [Connect Bot to Ngrok](#connect-bot-to-ngrok)
6.  [Microsoft Teams App Manifest Configuration](#testing-your-bot)

## 1. Prerequisites

Before you begin, ensure you have the following:

* An Azure subscription. If you don't have one, you can create a [free Azure account](https://azure.microsoft.com/free/).
* Node.js (LTS version recommended) and npm installed.
* A code editor (e.g., Visual Studio Code).
* Git installed.
* Your bot's source code.

## 2. Azure Portal Setup

This section guides you through creating the necessary resources in the Azure Portal.

### Create a Resource Group

A resource group is a container that holds related resources for an Azure solution.

1.  Go to the [Azure Portal](https://portal.azure.com/).
2.  In the search bar at the top, type "Resource groups" and select it.
3.  Click on `+ Create`.
4.  Fill in the following details:
    * **Subscription:** Select your Azure subscription.
    * **Resource group name:** Choose a unique name for your resource group (e.g., `myBotResourceGroup`).
    * **Region:** Select a region close to you (e.g., `East US`).
5.  Click `Review + create`, then `Create`.

### Create an Azure Bot Resource

The Azure Bot resource provides the necessary infrastructure for your bot, including messaging endpoints and channel configuration.

1.  In the Azure Portal, search for "Azure Bot" and select it.
2.  Click on `+ Create`.
3.  Fill in the following details:
    * **Bot handle:** Enter a globally unique name for your bot (e.g., `myAwesomeBot123`).
    * **Subscription:** Select your Azure subscription.
    * **Resource Group:** Choose the resource group you created earlier.
    * **Pricing tier:** Select a pricing tier (e.g., `Standard`).
    * **Type of App:** Select `Multi Tenant`.
    * **Creation type:** Choose `Create new Microsoft App ID`.
    * **Region:** Select the same region as your resource group.
4.  Click `Review + create`, then `Create`.

### Configure Channels

**Channels** are the communication services your bot can interact with (e.g., Web Chat, Microsoft Teams, Facebook).

1.  Once your Azure Bot resource is deployed, navigate to it.
2.  In the left-hand navigation, under `Settings`, click on `Channels`.
3.  To set up **Microsoft Teams**:
    * In the `Channels` blade, click on `Microsoft Teams`.
    * Read the Microsoft Teams Channel Terms of Service and click `Agree`.
    * You might be presented with configuration options depending on your bot's capabilities (e.g., calling, group chat). For a basic messaging bot, you can usually proceed with the default settings.
    * Click `Save`.
    * Your bot is now configured to work with Microsoft Teams.

### Get Bot Credentials

You will need your Bot's Microsoft App ID and App Password (Client Secret) for your local development environment.

1.  Navigate back to your Azure Bot resource overview.
2.  Copy the **Microsoft App ID**(this is the Application (client) ID).
3.  In the left-hand navigation, under `Settings`, click on `Configuration`.
4.  Next to `Microsoft App ID`, click on `Manage`. This will take you to the `App registrations` blade for your bot.
5.  Under `Client secrets`, click `+ New client secret`.
    * Add a description (e.g., `Bot secret`).
    * Set an expiration (e.g., `12 months`).
    * Click `Add`.
  
      
      <img width="537" alt="Screenshot 2025-06-11 at 12 09 00 AM" src="https://github.com/user-attachments/assets/fdea4911-109a-4cc8-ac1d-36c193d01a37" />

6.  **Important:** Copy the `Value` of the new client secret immediately. This value is only shown once and will be hidden after you leave this page. This is your **Microsoft App Password**.

## 3. Local Bot Development Setup

This section covers setting up your bot's source code locally.

### Clone your Bot Project

If you haven't already, clone your bot's repository to your local machine.

```bash
git clone <your-bot-repository-url>
cd <your-bot-project-directory>
````

### Install Dependencies

Navigate to your bot's project directory and install the necessary npm packages.

```bash
npm install
```

### Configure Environment Variables

Your bot code will likely use environment variables to access the Microsoft App ID and App Password. Create a `.env` file in the root of your bot project (if one doesn't exist) and add the following:

```
MicrosoftAppId=<YOUR_MICROSOFT_APP_ID>
MicrosoftAppPassword=<YOUR_MICROSOFT_APP_PASSWORD>
```

Replace `<YOUR_MICROSOFT_APP_ID>` and `<YOUR_MICROSOFT_APP_PASSWORD>` with the values you obtained from the Azure Portal.

## 4\. Ngrok Setup

Ngrok creates a secure tunnel to your localhost, making your local bot accessible from the internet. This is crucial for connecting your Azure Bot to your local development environment.

### Download Ngrok

1.  Go to the [ngrok download page](https://ngrok.com/download).
2.  Download the appropriate ngrok version for your operating system.
3.  Extract the downloaded zip file. You should find a single `ngrok` executable file.
4.  Move the `ngrok` executable to a directory included in your system's PATH, or to your bot's project directory for simplicity.

### Authenticate Ngrok

1.  If you don't have one, create a free ngrok account at [ngrok.com](https://ngrok.com/).

2.  After logging in, go to the [Your Authtoken](https://dashboard.ngrok.com/get-started/your-authtoken) page.

3.  Copy your authtoken.

4.  Open your terminal or command prompt and run the following command, replacing `<YOUR_NGROK_AUTHTOKEN>` with your actual authtoken:

    ```bash
    ngrok authtoken <YOUR_NGROK_AUTHTOKEN>
    ```

    This command will add your authtoken to the ngrok configuration file.

### Start Ngrok Tunnel

1.  First, ensure your bot is running locally. Typically, you can start your bot with:

    ```bash
    npm start
    ```

    Your bot will usually listen on port `3978` by default, but check your bot's code if it uses a different port.

2.  Open a **new** terminal or command prompt window (keep your bot running in the first terminal).

3.  Navigate to the directory where you placed the `ngrok` executable.

4.  Run the following command to expose your bot's port (assuming port `3978`):

    ```bash
    ngrok http 3978
    ```

    You will see output similar to this:

    ```
    ngrok by @inconshreveable

    Session Status                online
    Account                       YourName (Plan: Free)
    Version                       x.x.x
    Region                        United States (us)
    Web Interface                 [http://127.0.0.1:4040](http://127.0.0.1:4040)
    Forwarding                    http://<YOUR_NGROK_URL>.ngrok-free.app -> http://localhost:3978
    Forwarding                    https://<YOUR_NGROK_URL>.ngrok-free.app -> http://localhost:3978

    Connections                   ttl     opn     rt1     rt5     p50     p90
                                  0       0       0.00    0.00    0.00    0.00
    ```

    Copy the `https` forwarding URL (e.g., `https://<YOUR_NGROK_URL>.ngrok-free.app`). This is your public endpoint.

## 5\. Connect Bot to Ngrok

Now, you need to update your Azure Bot's messaging endpoint to point to your ngrok URL.

1.  Go back to the [Azure Portal](https://www.google.com/url?sa=E&source=gmail&q=https://portal.azure.com/).

2.  Navigate to your Azure Bot resource.

3.  In the left-hand navigation, under `Settings`, click on `Configuration`.

4.  In the `Messaging endpoint` field, paste your `https` ngrok forwarding URL, appended with `/api/messages`.

    For example: `https://<YOUR_NGROK_URL>.ngrok-free.app/api/messages`

5.  Click `Apply` at the top to save the changes.

Here's the formatted section for your `README.md` file, covering the `manifest.json` for Microsoft Teams app uploads:

---

## 6. Microsoft Teams App Manifest Configuration

To upload your bot as a custom app to Microsoft Teams, you need a `manifest.json` file (along with `color.png` and `outline.png` icons) packaged into a `.zip` file. This `manifest.json` describes your bot to Teams.

Create a `manifest.json` file (for example, in a `teams_app_package` directory) with the following structure. Fill in the placeholders with your specific details:

```json
{
  "$schema": "https://developer.microsoft.com/en-us/json-schemas/teams/v1.11/MicrosoftTeams.schema.json",
  "manifestVersion": "1.11",
  "version": "1.0.0",
  "id": "YOUR_MICROSOFT_APP_ID",
  "developer": {
    "name": "Your Company Name",
    "websiteUrl": "https://www.microsoft.com",
    "privacyUrl": "https://www.microsoft.com/privacy",
    "termsOfUseUrl": "https://www.microsoft.com/legal/terms-of-use"
  },
  "name": {
    "short": "Your Bot Name",
    "full": "Your Awesome Bot for Teams"
  },
  "description": {
    "short": "A short description of your bot.",
    "full": "This is a full description of your awesome bot that explains its features and how it helps users in Microsoft Teams."
  },
  "icons": {
    "color": "color.png",
    "outline": "outline.png"
  },
  "bots": [
    {
      "botId": "YOUR_MICROSOFT_APP_ID",
      "scopes": [ "personal", "team", "groupchat" ],
      "needsChannelSelector": false,
      "supportsFiles": false,
      "isNotificationOnly": false
    }
  ],
   "permissions": [
    "identity",
    "messageTeamMembers"
  ],
  "accentColor": "#60A18E",
  "validDomains": [
    "*.ngrok-free.app", // Essential for ngrok testing
    "<YOUR_NGROK_URL>.ngrok-free.app", // Your bot's public domain, if any
  ]
}
```

**Key fields to update:**

* **`id`**: This should be your **Microsoft App ID**.
* **`packageName`**: A unique identifier for your app (e.g., `com.mycompany.mybot`).
* **`developer`**: Update with your company's name and relevant URLs.
* **`name`**: Set the **short** and **full** names for your bot as they'll appear in Teams.
* **`description`**: Provide clear **short** and **full** descriptions of your bot's functionality.
* **`accentColor`**: A hexadecimal color code for the app's theme.
* **`icons`**: Ensure you have **`color.png`** (192x192 pixels) and **`outline.png`** (32x32 pixels) in the same directory as your `manifest.json`.
* **`bots[0].botId`**: This should also be your **Microsoft App ID**.
* **`bots[0].scopes`**: Defines where your bot can be used (`personal` for 1:1 chats, `team` for channels, `groupchat` for group chats).
* **`webApplicationInfo.id`**: Your **Microsoft App ID**.
* **`webApplicationInfo.resource`**: The **Azure Bot resource URI**. Replace `YOUR_MICROSOFT_APP_ID` with your actual ID.
* **`validDomains`**:
    * Add **`*.ngrok-free.app`** (or your specific ngrok domain) to allow Teams to communicate with your local bot via the tunnel.
    * Include your bot's public domain if it has one (e.g., `yourwebsite.com`).
    * **`token.botframework.com`** is crucial for bot authentication.

### Packaging for Teams:

1.  Create a new folder (e.g., `teams_app_package`).
2.  Place your `manifest.json`, `color.png`, and `outline.png` files inside this folder.
3.  **Compress (zip) the *contents* of this folder**, not the folder itself. The `.zip` file should contain `manifest.json`, `color.png`, and `outline.png` directly at its root.
4.  This `.zip` file is what you will upload to Teams.

This README provides a comprehensive guide for setting up your Microsoft Bot. Happy coding\!
