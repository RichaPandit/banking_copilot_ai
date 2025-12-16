**Create an Azure Web App (Python)**
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

**Create a GitHub Repository & Push Code**
1. Create GitHub repository
2. From your local directory:
   git init
   git checkout -b main
   git add .
   git commit -m "Iniyial MCP server Setup"
   git remote add origin https://github.com/<username>/<repo-name>.git
   git push -u origin main

**Connect GitHub to Azure WebApp (CI/CD)**
1. In Azure Portal -> Web App -> Deployment Center
2. Choose:
   a. Source: GitHub
   b. Organization/Reo/Branch: main
3. Save configuration

Azure will now:
a. Auto-build on every push
b. Restart the app after deployment

**Configure Startup Command**
In Web App  -> Settings -> Configuration -> Stack Settings, set your startup command as:

      gunicorn -k uvicorn.workers.UvicornWorker -w 1 mcp_server.main:app
      
**Define Environment Variables (No Hardcoding)**
All secrets and config are injected via Application Setings.
In Web App -> Settings -> Environment variables, add:

Variable Name               | Description
----------------------------|---------------------------------------------
MCP_DEV_ASSUME_KEY          | Token used by Copilot Studio to authenticate
TEAMS_WORKFLOW_WEBHOOK_URL  | Microsoft Teams workflow webhook
APP_BASE_DIR                | Writable base path (/home/site/wwwroot)
MCP_RESOURCE_FEATURED_ID    | Optional featured company ID

No secrets are committed to webhook

**Monitor with Log Stream**
To debug and monitor runtime behavior:
1. In Azure portal, Web App -> Moitoring -> Log stream
2. Watch for:
   a. MCP server startup logs
   b. Tool invocation requests
   c. Authentication failures
   d. Report generation paths
This is especially useful when validating:
1. Copilot -> MCP auth headers
2. Tool execution from Copilot Studio
3. File write permissions

**CI/CD via Github Actions**
Create file under the <project_folder>/.github/workflows


