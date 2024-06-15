# Github Action Notifier

This repository listens to Github actions for the repository [https://github.com/dhimanparas20/action-repo](https://github.com/dhimanparas20/action-repo). It captures any push, pull, or merge actions on this repository using webhooks and displays them on a front-end UI.

## Project Overview

- **Backend:** Built using Flask-RESTful
- **Database:** MongoDB to store all Github changes
- **Frontend:** Displays the captured actions with details

## Screenshot

![Screenshot](ss.png)

## How to Use

1. **Clone the Repository:**

   ```sh
   git clone https://github.com/dhimanparas20/webhook-repo
   cd webhook-repo
   ```

2. **Install Dependencies:**

    ```sh
    pip3 install -r requirements.txt
    ```

2. **Deploy the Project:**    
    
    ```
    Deploy this project on a server and get a domain or use ngrok to expose the local server.
    ```

2. **Set Up Webhook:**     

    ```
    In the settings of the target repository (action-repo), go to Settings -> Webhooks, and add the domain followed by /api/event/ as the payload URL.

    Example: http://yourdomain.com/api/event/ or http://yourngrokaddress.ngrok.io/api/event/
    ```

### That's it! Now, any push, pull, or merge actions on the target repository will be captured and displayed in the front-end UI of this project.    