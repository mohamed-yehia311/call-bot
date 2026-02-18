import uvicorn
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Importing our renamed engine accessor and modified routes
from ..infrastructure.superlinked.service import get_search_service
from .routes import health, superlinked
from .routes.voice import mount_voice_stream

@asynccontextmanager
async def app_lifecycle(app: FastAPI):
    """
    Handles the orchestration of service initialization 
    and resource cleanup during the app's runtime.
    """
    # Bootstrapping the vector search engine into the application state
    app.state.property_service = get_search_service()
    
    yield
    
    # Optional: Add logic to close database connections or clear cache here
    pass

def create_application() -> FastAPI:
    """Factory function to configure and return the FastAPI instance."""
    
    fastapi_app = FastAPI(
        title="Conversational AI Gateway",
        description="Next-gen property search and voice streaming interface powered by Superlinked and FastRTC",
        version="1.0.0",
        docs_url="/api/docs",  # Changed documentation path
        lifespan=app_lifecycle,
    )

    # Security configuration for cross-origin resource sharing
    fastapi_app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Adjust this to specific domains in production
        allow_credentials=True,
        allow_methods=["GET", "POST", "OPTIONS"], # More explicit than "*"
        allow_headers=["Content-Type", "Authorization"],
    )

    # Registering endpoint modules
    fastapi_app.include_router(health.router)
    fastapi_app.include_router(superlinked.router)

    # Integrate the WebRTC/Twilio voice streaming layer
    mount_voice_stream(fastapi_app)
    
    return fastapi_app

app = create_application()

if __name__ == "__main__":
    uvicorn.run(
        "main:app", # Use string import for hot-reloading capability
        host="0.0.0.0", 
        port=8000, 
        reload=True
    )