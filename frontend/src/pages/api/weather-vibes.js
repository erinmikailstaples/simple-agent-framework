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

    // For now, return mock data
    // This can be replaced with actual agent integration later
    const mockData = getMockWeatherData(location);
    
    // Return mock response
    return res.status(200).json(mockData);
  } catch (error) {
    console.error('Error processing weather vibes request:', error);
    return res.status(500).json({ error: 'Failed to process request' });
  }
}

// Function to generate mock weather data
function getMockWeatherData(location) {
  // Create different mock responses based on location to simulate variety
  const locationLower = location.toLowerCase();
  
  // Generate random temperature between ranges based on first letter
  const firstChar = locationLower.charAt(0);
  let temperature, condition, umbrella, videos;
  
  if (firstChar <= 'h') {
    // Sunny locations
    temperature = Math.floor(Math.random() * 15) + 70; // 70-85°F
    condition = 'sunny';
    umbrella = false;
    videos = [
      { title: 'Summer Vibes Mix 2023', url: 'https://youtube.com/example1' },
      { title: 'Beach Day Playlist', url: 'https://youtube.com/example2' },
      { title: 'Happy Day Music Collection', url: 'https://youtube.com/example3' }
    ];
  } else if (firstChar <= 'p') {
    // Cloudy locations
    temperature = Math.floor(Math.random() * 15) + 55; // 55-70°F
    condition = 'cloudy';
    umbrella = Math.random() > 0.5; // 50% chance of needing umbrella
    videos = [
      { title: 'Cozy Coffee Shop Music', url: 'https://youtube.com/example4' },
      { title: 'Relaxing Jazz Playlist', url: 'https://youtube.com/example5' },
      { title: 'Chill Afternoon Beats', url: 'https://youtube.com/example6' }
    ];
  } else {
    // Rainy locations
    temperature = Math.floor(Math.random() * 15) + 40; // 40-55°F
    condition = 'rainy';
    umbrella = true;
    videos = [
      { title: 'Rainy Day Jazz', url: 'https://youtube.com/example7' },
      { title: 'Relaxing Rain Sounds', url: 'https://youtube.com/example8' },
      { title: 'Piano Music with Rain', url: 'https://youtube.com/example9' }
    ];
  }

  return {
    location: location,
    weather: {
      temperature: `${temperature}°F`,
      condition: condition,
      forecast: `Expect ${condition} conditions to continue for the next few hours.`
    },
    need_umbrella: umbrella,
    recommendations: {
      videos: videos,
      message: `Based on the ${condition} weather in ${location}, we've selected some ${condition} day vibes for you!`
    },
    timestamp: new Date().toISOString()
  };
}

// For future implementation: connect to the actual weather vibes agent
/*
async function getWeatherVibesFromAgent(location) {
  // This function would be implemented when ready to connect to the actual agent
  // It would make requests to the Python agent and return the results
  
  // Example implementation:
  // const response = await fetch('http://localhost:8000/api/weather-vibes', {
  //   method: 'POST',
  //   headers: { 'Content-Type': 'application/json' },
  //   body: JSON.stringify({ location })
  // });
  // return await response.json();
}
*/

