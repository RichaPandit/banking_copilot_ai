Create an Azure Web App (Python)
1. In Azure Portal -> Create Web App
2. Configuration:
   a. Publish: Code
   b. Runtime stack: Python 3.10+
   c. Operating System: Linux
   d. App Service Plan: Basic/B1 (or higher)
3. Once created, note:
   a. Web App name
   b. Resource Group
   c. Default domain (https://<app-name>.azurewebsites.net)
This Web App will host the MCP server endpoint (/mcp).

Create a GitHub Repository & Push Code
1. Create GitHub repository
2. From your local directory:
   git init
   git checkout -b main
   git add .
   git commit -m "Iniyial MCP server Setup"
   git remote add origin https://github.com/<username>/<repo-name>.git
   git push -u origin main

Connect GitHub to Azure WebApp (CI/CD)
1. In Azure Portal -> Web App -> Deployment Center
2. Choose:
   a. Source: GitHub
   b. Organization/Reo/Branch: main
3. Save configuration

Azure will now:
a. Auto-build on every push
b. Restart the app after deployment

Configure Startup Command
In Web App  -> Configuration ->
