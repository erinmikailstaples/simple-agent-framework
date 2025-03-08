import os
import sys

# Add the parent directory to sys.path to allow importing from the app directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mangum import Mangum
from app.main import app

# Set any environment variables or configurations needed for serverless
# For example, you might want to disable docs in production
if os.environ.get("ENVIRONMENT") == "production":
    app.docs_url = None
    app.redoc_url = None

# Create the handler for Vercel serverless functions
handler = Mangum(app)

