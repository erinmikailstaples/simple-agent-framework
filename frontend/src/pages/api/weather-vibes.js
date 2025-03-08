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

    // Determine the API URL - use environment variable if available, otherwise use relative path
    const apiUrl = process.env.BACKEND_API_URL || '/api/weather';
    
    // Connect to the backend agent
    const response = await fetch(apiUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        location: location
      }),
      // Set a reasonable timeout to prevent hanging requests
      timeout: 10000,
    });

    // Handle non-OK responses
    if (!response.ok) {
      let errorData = { error: 'Error connecting to backend agent' };
      
      try {
        // Check if there's content to parse
        const contentType = response.headers.get('content-type');
        if (contentType && contentType.includes('application/json')) {
          const text = await response.text();
          if (text) {
            errorData = JSON.parse(text);
          }
        }
      } catch (parseError) {
        console.error('Error parsing error response:', parseError);
      }
      
      return res.status(response.status).json({
        error: errorData.error || 'Error connecting to backend agent'
      });
    }

    // Format the weather data into a human-readable response for the frontend
    const data = await response.json();
    
    // Create a formatted weather string from the backend data
    const formattedWeather = formatWeatherResponse(data);
    
    // Check if we're dealing with mock data and return appropriate message
    let responseObj = { response: formattedWeather };
    
    // If mock data is detected, add a warning message
    if (data.mock_data === true) {
      responseObj.warning = "MOCK DATA DETECTED: You are seeing simulated data, not real API results.";
      
      // Include information about missing API keys if available
      if (data.missing_api_keys || data.missing_api_key) {
        const missingKeys = data.missing_api_keys || [data.missing_api_key].filter(Boolean);
        responseObj.missing_api_keys = missingKeys;
      }
    }
    
    // Return the formatted response that the frontend expects
    return res.status(200).json(responseObj);
  } catch (error) {
    console.error('Error processing weather vibes request:', error);
    return res.status(500).json({ error: 'Failed to connect to backend agent' });
  }
}

/**
 * Formats the weather data from the backend into a human-readable string
 * @param {Object} data - Weather data from the backend
 * @returns {string} Formatted weather description
 */
function formatWeatherResponse(data) {
  // Extract weather data from the backend response
  const { temperature, conditions, humidity, wind_speed, location } = data;
  
  // Build a human-readable weather description
  let weatherDescription = "";
  
  // Add warning about mock data at the beginning if applicable
  if (data.mock_data === true) {
    weatherDescription += "⚠️ WARNING: You are viewing MOCK DATA ⚠️\n\n";
    
    // Add information about which API keys are missing
    if (data.missing_api_keys) {
      weatherDescription += `Missing API keys: ${data.missing_api_keys.join(", ")}\n`;
    } else if (data.missing_api_key) {
      weatherDescription += `Missing API key: ${data.missing_api_key}\n`;
    }
    
    weatherDescription += "To see real data, please follow these steps:\n\n";
    weatherDescription += "1. Create a `.env` file based on the `.env.template`\n";
    weatherDescription += "2. Sign up for API keys:\n";
    weatherDescription += "   - Get a `WEATHERAPI_KEY` from https://www.weatherapi.com/\n";
    weatherDescription += "   - Get a `YOUTUBE_API_KEY` from the Google Developer Console\n";
    weatherDescription += "3. Add these keys to your `.env` file\n";
    weatherDescription += "4. Restart your backend\n\n";
  }
  
  weatherDescription += `Weather for ${location}:\n`;
  
  if (temperature !== undefined) {
    weatherDescription += `Temperature: ${temperature}°C\n`;
  }
  
  if (conditions) {
    weatherDescription += `Conditions: ${conditions}\n`;
  }
  
  if (humidity !== undefined) {
    weatherDescription += `Humidity: ${humidity}%\n`;
  }
  
  if (wind_speed !== undefined) {
    weatherDescription += `Wind Speed: ${wind_speed} km/h\n`;
  }
  
  // If no weather data was found, provide a fallback message
  if (weatherDescription === `Weather for ${location}:\n`) {
    weatherDescription += "Weather data is currently unavailable.";
  }
  
  return weatherDescription;
}

