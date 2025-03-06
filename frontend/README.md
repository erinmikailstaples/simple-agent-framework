# Weather Vibes Frontend

This directory contains a Next.js frontend application for the Weather Vibes Agent, allowing users to input their location and receive personalized weather information and content recommendations based on the current weather conditions.

## Project Setup

### Prerequisites

Before you begin, ensure you have the following installed:
- Node.js (v14 or higher)
- npm (v6 or higher)

### Installation

1. Navigate to the frontend directory:
   ```
   cd frontend
   ```

2. Install the dependencies:
   ```
   npm install
   ```

## Running the Application

### Development Server

To start the development server:

```
npm run dev
```

The application will be available at [http://localhost:3000](http://localhost:3000).

### Production Build

To create a production build:

```
npm run build
```

To start the production server:

```
npm start
```

## Project Structure

```
frontend/
├── src/
│   ├── components/     # Reusable React components
│   ├── pages/          # Next.js pages for routing
│   │   ├── api/        # API routes
│   │   │   └── weather-vibes.js  # API endpoint for weather vibes
│   │   ├── _app.js     # App initialization
│   │   └── index.js    # Home page with location input
│   └── styles/         # CSS styles
│       └── globals.css # Global styles
├── package.json        # Project dependencies and scripts
└── README.md           # Project documentation
```

## Integration with Weather Vibes Agent

The frontend communicates with the Weather Vibes Agent through the `/api/weather-vibes` endpoint. 

### Current Implementation

The current implementation uses mock data to simulate responses from the Weather Vibes Agent. When a user submits a location in the form, the frontend sends a POST request to the API endpoint, which currently returns predefined weather information and content suggestions.

### Future Integration

To fully integrate with the actual Weather Vibes Agent:

1. Update the `weather-vibes.js` API route to make calls to the Weather Vibes Agent backend
2. Pass the user's location from the form submission to the agent
3. Process and display the real weather data and content recommendations returned by the agent

Example integration code for the API route:

```javascript
// Example code for integrating with the Weather Vibes Agent
import { fetchFromWeatherVibesAgent } from '../../utils/agent-api';

export default async function handler(req, res) {
  if (req.method === 'POST') {
    try {
      const { location } = req.body;
      
      // Call the Weather Vibes Agent with the location
      const agentResponse = await fetchFromWeatherVibesAgent(location);
      
      // Return the agent's response
      res.status(200).json(agentResponse);
    } catch (error) {
      res.status(500).json({ error: 'Failed to fetch weather vibes' });
    }
  } else {
    res.setHeader('Allow', ['POST']);
    res.status(405).end(`Method ${req.method} Not Allowed`);
  }
}
```

## Contributing

To contribute to this project:

1. Make your changes in a new branch
2. Test your changes thoroughly
3. Submit a pull request with a clear description of your improvements

## Troubleshooting

If you encounter any issues:

- Make sure all dependencies are installed
- Check that you're using compatible versions of Node.js and npm
- Verify that the API endpoint is correctly configured to communicate with the Weather Vibes Agent

