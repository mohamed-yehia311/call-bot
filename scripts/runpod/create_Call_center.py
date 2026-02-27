"""
Script to deploy the Property Search Call Center pod on RunPod Cloud.
"""

import sys
from typing import Dict, Any

import runpod
from loguru import logger
from ...src.config import settings

# --- Configuration ---

def get_pod_env_vars() -> Dict[str, str]:
    """
    Generates the environment variables dictionary for the RunPod container.
    Maps application settings to container environment variables.
    """
    return {
        # Groq Configuration
        "GROQ__API_KEY": settings.groq.api_key,
        "GROQ__BASE_URL": settings.groq.base_url,
        "GROQ__MODEL": settings.groq.model,
        "GROQ__STT_MODEL": settings.groq.stt_model,
        
        # OpenAI Configuration
        "OPENAI__API_KEY": settings.openai.api_key,
        "OPENAI__MODEL": settings.openai.model,
        
        # Superlinked Configuration
        "SUPERLINKED__EMBEDDING_MODEL": settings.superlinked.embedding_model,
        "SUPERLINKED__SQFT_MIN_VALUE": str(settings.superlinked.sqft_min_value),
        "SUPERLINKED__SQFT_MAX_VALUE": str(settings.superlinked.sqft_max_value),
        "SUPERLINKED__PRICE_MIN_VALUE": str(settings.superlinked.price_min_value),
        "SUPERLINKED__PRICE_MAX_VALUE": str(settings.superlinked.price_max_value),
        
        # Qdrant Configuration
        "QDRANT__HOST": settings.qdrant.host,
        "QDRANT__PORT": str(settings.qdrant.port),
        "QDRANT__API_KEY": settings.qdrant.api_key,
        "QDRANT__CLUSTER_URL": settings.qdrant.cluster_url,
        "QDRANT__USE_QDRANT_CLOUD": str(settings.qdrant.use_qdrant_cloud),
        
        # RunPod Configuration
        "RUNPOD__API_KEY": settings.runpod.api_key,
        "RUNPOD__FASTER_WHISPER_GPU_TYPE": settings.runpod.faster_whisper_gpu_type,
        "RUNPOD__ORPHEUS_GPU_TYPE": settings.runpod.orpheus_gpu_type,
        
        # Faster Whisper Configuration
        "FASTER_WHISPER__API_URL": settings.faster_whisper.api_url,
        "FASTER_WHISPER__MODEL": settings.faster_whisper.model,
        
        # Orpheus TTS Configuration
        "ORPHEUS__API_URL": settings.orpheus.api_url,
        "ORPHEUS__MODEL": settings.orpheus.model,
        "ORPHEUS__VOICE": settings.orpheus.voice,
        "ORPHEUS__TEMPERATURE": str(settings.orpheus.temperature),
        "ORPHEUS__TOP_P": str(settings.orpheus.top_p),
        "ORPHEUS__MAX_TOKENS": str(settings.orpheus.max_tokens),
        "ORPHEUS__REPETITION_PENALTY": str(settings.orpheus.repetition_penalty),
        "ORPHEUS__SAMPLE_RATE": str(settings.orpheus.sample_rate),
        "ORPHEUS__DEBUG": str(settings.orpheus.debug),
        
        # Together AI TTS Configuration
        "TOGETHER__API_KEY": settings.together.api_key,
        "TOGETHER__API_URL": settings.together.api_url,
        "TOGETHER__MODEL": settings.together.model,
        "TOGETHER__VOICE": settings.together.voice,
        "TOGETHER__SAMPLE_RATE": str(settings.together.sample_rate),
        
        # Opik Configuration
        "OPIK__API_KEY": settings.opik.api_key,
        "OPIK__PROJECT_NAME": settings.opik.project_name,
        
        # Model Selection
        "STT_MODEL": settings.stt_model,
        "TTS_MODEL": settings.tts_model,
    }

# --- Deployment Logic ---

def deploy_call_center_pod() -> Dict[str, Any]:
    """Handles the creation and configuration of the RunPod pod."""
    
    # Configure RunPod API Key
    runpod.api_key = settings.runpod.api_key
    
    logger.info("Initiating Call Center pod creation...")
    
    # Define Pod specifications
    pod_config = {
        "name": "Call Center",
        "image_name": "theneuralmaze/agent-call-center:latest",
        "cloud_type": "SECURE",
        "volume_in_gb": 20,
        "volume_mount_path": "/workspace",
        "instance_id": "cpu5c-2-4", # Recommend reviewing if this is enough for real-time STT/TTS
        "ports": "8000/http,443/tcp,80/tcp,22/tcp",
        "env": get_pod_env_vars()
    }
    
    try:
        pod = runpod.create_pod(**pod_config)
        return pod
    except Exception as e:
        logger.error(f"Failed to create pod: {e}")
        raise

def main():
    """Main function to run the deployment."""
    try:
        pod = deploy_call_center_pod()
        
        pod_id = pod.get("id")
        pod_url = f"https://{pod_id}-8000.proxy.runpod.net"
        
        logger.success("Pod created successfully!")
        logger.info(f"Pod ID: {pod_id}")
        logger.info(f"Pod URL: {pod_url}")
        
        print(f"\n{'='*60}")
        print("🎉 Call Center Pod is deploying!")
        print(f"👉 Access URL: {pod_url}")
        print(f"{'='*60}\n")
        
    except Exception:
        sys.exit(1)

if __name__ == "__main__":
    main()