  } catch (error) {
    console.error('Error processing weather vibes request:', error);
    
    // Provide more specific error messages based on the error type
    if (error.name === 'AbortError') {
      return res.status(504).json({ error: 'Request timed out while connecting to the weather service' });
    } else if (error.code === 'ECONNREFUSED') {
      return res.status(503).json({ error: 'Weather service is currently unavailable' });
    } else if (error.message && error.message.includes('fetch')) {
      return res.status(502).json({ error: 'Network error while connecting to weather service' });
    }
    
    // Default error response
    return res.status(500).json({ 
      error: 'Failed to connect to backend agent',
      message: process.env.NODE_ENV === 'development' ? error.message : undefined
    });
  }
