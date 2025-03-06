// Next.js API route for weather vibes
// This initially returns mock data but can be updated to connect to the actual agent

export default async function handler(req, res) {
  // Only allow POST requests
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    // Extract location from request body
    const { location } = req.body;

    if (!location) {
      return res.status(400).json({ error: 'Location is required' });
    }

    // Connect to the backend agent
    const response = await fetch('http://localhost:5000/agent', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        message: `What's the weather like in ${location}?`,
        agent_type: 'weather-vibes'
      }),
    });

    // Handle non-OK responses
    if (!response.ok) {
      const errorData = await response.json();
      return res.status(response.status).json({
        error: errorData.error || 'Error connecting to backend agent'
      });
    }

    // Return the agent response
    const data = await response.json();
    return res.status(200).json(data);
  } catch (error) {
    console.error('Error processing weather vibes request:', error);
    return res.status(500).json({ error: 'Failed to connect to backend agent' });
  }
}

