export async function onRequest({ request, env }) {
  // Add CORS headers
  const corsHeaders = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type, Authorization',
  };

  // Handle OPTIONS requests
  if (request.method === 'OPTIONS') {
    return new Response(null, {
      headers: corsHeaders,
    });
  }

  // Add CORS headers to all responses
  const response = await fetch(request);
  const newResponse = new Response(response.body, response);
  Object.keys(corsHeaders).forEach((key) => {
    newResponse.headers.set(key, corsHeaders[key]);
  });

  return newResponse;
}

