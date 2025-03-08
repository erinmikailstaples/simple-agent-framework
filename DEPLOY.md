# Deploying Your Vibes Agent to Vercel

This document outlines the steps to deploy your Vibes Agent application to Vercel.

## Prerequisites

- A [Vercel](https://vercel.com) account
- [Vercel CLI](https://vercel.com/docs/cli) installed (optional for command-line deployment)
- Git repository with your project code
- API keys:
  - WEATHERAPI_KEY from [WeatherAPI](https://www.weatherapi.com/)
  - YOUTUBE_API_KEY from [Google Cloud Console](https://console.cloud.google.com/)

## Step 1: Prepare Your Project for Deployment

Ensure your project has the following configuration files:

1. **vercel.json** (in the root directory):
   ```json
   {
     "version": 2,
     "builds": [
       { "src": "frontend/package.json", "use": "@vercel/next" },
       { "src": "backend/api/*.py", "use": "@vercel/python" }
     ],
     "routes": [
       { "src": "/api/(.*)", "dest": "backend/api/$1" },
       { "src": "/(.*)", "dest": "frontend/$1" }
     ]
   }
   ```

2. **Serverless Backend Configuration**:
   Make sure your backend is configured to work as serverless functions via `backend/api/index.py`

3. **Frontend API Calls**:
   Ensure your frontend makes API calls using relative paths (e.g., `/api/weather` instead of `http://localhost:1234/weather`)

## Step 2: Set Up Environment Variables

You'll need to configure environment variables in Vercel:

### Option 1: Using Vercel Dashboard

1. Log in to your [Vercel Dashboard](https://vercel.com/dashboard)
2. Select your project
3. Go to "Settings" > "Environment Variables"
4. Add the following variables:
   - `WEATHERAPI_KEY` - Your Weather API key
   - `YOUTUBE_API_KEY` - Your YouTube API key
   - Any other variables from your `.env.template` file

### Option 2: Using Vercel CLI

1. Create a `.env` file in your project root with your environment variables
2. Deploy with the `--env` flag:
   ```bash
   vercel --env WEATHERAPI_KEY=your_weather_api_key --env YOUTUBE_API_KEY=your_youtube_api_key
   ```

## Step 3: Deploy to Vercel

### Option 1: Deploy via Vercel Dashboard (Recommended for First Deployment)

1. Log in to your [Vercel Dashboard](https://vercel.com/dashboard)
2. Click "New Project"
3. Import your Git repository
4. Configure your project:
   - Framework Preset: Select "Next.js" (for the frontend)
   - Root Directory: Leave blank to use the project root
   - Build Command: Leave as default or set to `cd frontend && npm run build`
   - Output Directory: Leave as default
5. Click "Deploy"

### Option 2: Deploy via Vercel CLI

1. Navigate to your project directory in your terminal
2. Run:
   ```bash
   vercel
   ```
3. Follow the interactive prompts to configure your deployment

## Step 4: Verify Your Deployment

1. Once deployed, Vercel will provide you with a URL (e.g., `https://your-project.vercel.app`)
2. Visit this URL to check if your application is working correctly
3. Test the weather and YouTube API functionality to ensure the environment variables are working properly

## Troubleshooting

If you encounter issues during deployment:

1. **API Errors**: Check your environment variables in the Vercel dashboard
2. **Build Errors**: Check the build logs in the Vercel dashboard
3. **Serverless Function Errors**: 
   - Verify your `backend/api/index.py` is correctly set up
   - Check if all required packages are listed in `backend/api/requirements.txt`
4. **CORS Issues**: Ensure your API routes are properly configured in `vercel.json`

## Continuous Deployment

Vercel automatically deploys new changes when you push to your Git repository:

1. Make changes to your code locally
2. Commit and push to your Git repository
3. Vercel will automatically trigger a new deployment

## Conclusion

Your Vibes Agent application should now be successfully deployed on Vercel. The frontend Next.js application and the backend FastAPI serverless functions should be working together seamlessly.

For more information on Vercel deployments, visit the [Vercel Documentation](https://vercel.com/docs).

