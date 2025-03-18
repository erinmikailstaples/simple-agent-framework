# Deploying to Cloudflare Pages

This guide will help you deploy the Simple Agent Framework to Cloudflare Pages.

## Prerequisites

- A [Cloudflare](https://dash.cloudflare.com) account
- [Wrangler CLI](https://developers.cloudflare.com/workers/wrangler/install-and-update/) installed
- Git repository with your project code
- Required API keys:
  - WEATHERAPI_KEY from [WeatherAPI](https://www.weatherapi.com/)
  - YOUTUBE_API_KEY from [Google Cloud Console](https://console.cloud.google.com/)

## Step 1: Install Wrangler CLI

```bash
npm install -g wrangler
```

## Step 2: Login to Cloudflare

```bash
wrangler login
```

## Step 3: Configure Environment Variables

1. Go to your [Cloudflare Dashboard](https://dash.cloudflare.com)
2. Navigate to Workers & Pages > your project > Settings > Environment variables
3. Add the following variables:
   - WEATHERAPI_KEY
   - YOUTUBE_API_KEY
   - Any other variables from your .env.template file

## Step 4: Deploy to Cloudflare Pages

### Option 1: Deploy via Cloudflare Dashboard

1. Go to your Cloudflare Dashboard
2. Navigate to "Pages"
3. Click "Create a project"
4. Choose "Connect to Git"
5. Select your repository
6. Configure your build settings:
   - Framework preset: Next.js
   - Build command: cd frontend && npm run build
   - Build output directory: frontend/.next
   - Root directory location: /
7. Click "Save and Deploy"

### Option 2: Deploy via Wrangler CLI

```bash
wrangler pages publish frontend/.next --project-name=simple-agent-framework
```

## Step 5: Configure Backend Functions

1. Navigate to the `backend/api` directory
2. Create or update functions to use Cloudflare Workers
3. Deploy each function:
```bash
wrangler deploy
```

## Continuous Deployment

Once set up, Cloudflare Pages will automatically deploy when you push changes to your repository:

1. Make changes to your code
2. Commit and push to your repository
3. Cloudflare will automatically trigger a new build and deployment

## Environment Variables in Development

For local development, continue using your .env file. For production, make sure all environment variables are set in your Cloudflare Dashboard.

## API Deployment

The backend API is deployed as a Cloudflare Worker:

1. Navigate to the `cloudflare/workers/api` directory
2. Deploy the API worker:
```bash
cd cloudflare/workers
wrangler publish
```

3. Configure the API URL in your frontend environment:
```bash
# In your frontend .env file
NEXT_PUBLIC_API_URL=https://your-worker-name.workers.dev
```

Remember to set up the following environment variables in your Cloudflare Workers:
- OPENAI_API_KEY
- Other API keys from your .env.template

## Troubleshooting

- If builds fail, check the build logs in your Cloudflare Dashboard
- Ensure all environment variables are properly set
- Verify your wrangler.toml configuration
- Check that all required dependencies are installed

For more information, visit the [Cloudflare Pages documentation](https://developers.cloudflare.com/pages).

# Deploying to Cloudflare Pages

This guide will help you deploy the Simple Agent Framework to Cloudflare Pages.

## Prerequisites

- A [Cloudflare](https://dash.cloudflare.com) account
- [Wrangler CLI](https://developers.cloudflare.com/workers/wrangler/install-and-update/) installed
- Git repository with your project code
- Required API keys:
  - WEATHERAPI_KEY from [WeatherAPI](https://www.weatherapi.com/)
  - YOUTUBE_API_KEY from [Google Cloud Console](https://console.cloud.google.com/)

## Step 1: Install Wrangler CLI

```bash
npm install -g wrangler
```

## Step 2: Login to Cloudflare

```bash
wrangler login
```

## Step 3: Configure Environment Variables

1. Go to your [Cloudflare Dashboard](https://dash.cloudflare.com)
2. Navigate to Workers & Pages > your project > Settings > Environment variables
3. Add the following variables:
   - WEATHERAPI_KEY
   - YOUTUBE_API_KEY
   - Any other variables from your .env.template file

## Step 4: Deploy to Cloudflare Pages

### Option 1: Deploy via Cloudflare Dashboard

1. Go to your Cloudflare Dashboard
2. Navigate to "Pages"
3. Click "Create a project"
4. Choose "Connect to Git"
5. Select your repository
6. Configure your build settings:
   - Framework preset: Next.js
   - Build command: cd frontend && npm run build
   - Build output directory: frontend/.next
   - Root directory location: /
7. Click "Save and Deploy"

### Option 2: Deploy via Wrangler CLI

```bash
wrangler pages publish frontend/.next --project-name=simple-agent-framework
```

## Step 5: Configure Backend Functions

1. Navigate to the `backend/api` directory
2. Create or update functions to use Cloudflare Workers
3. Deploy each function:
```bash
wrangler deploy
```

## Continuous Deployment

Once set up, Cloudflare Pages will automatically deploy when you push changes to your repository:

1. Make changes to your code
2. Commit and push to your repository
3. Cloudflare will automatically trigger a new build and deployment

## Environment Variables in Development

For local development, continue using your .env file. For production, make sure all environment variables are set in your Cloudflare Dashboard.

## Troubleshooting

- If builds fail, check the build logs in your Cloudflare Dashboard
- Ensure all environment variables are properly set
- Verify your wrangler.toml configuration
- Check that all required dependencies are installed

For more information, visit the [Cloudflare Pages documentation](https://developers.cloudflare.com/pages).

