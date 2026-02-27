import time
import requests
import runpod
from ...src.config import settings


def create_faster_whisper_pod():
    """Create a RunPod instance for the Faster Whisper server."""
    runpod.api_key = settings.runpod.api_key

    pod = runpod.create_pod(
        name="Faster Whisper Server",
        image_name="theneuralmaze/faster-whisper-server:latest",
        gpu_type_id=settings.runpod.faster_whisper_gpu_type,
        cloud_type="SECURE",
        gpu_count=1,
        volume_in_gb=20,
        volume_mount_path="/workspace",
        ports="8000/http",
        env={
            "DEFAULT_MODEL": settings.runpod.faster_whisper_model,
            "COMPUTE_TYPE": "int8",
            "LOOPBACK_HOST_URL": "http://localhost:8000",
        },
    )

    pod_id = pod.get("id")
    pod_url = f"https://{pod_id}-8000.proxy.runpod.net"

    print(f"✓ Pod created successfully (ID: {pod_id})")
    print(f"✓ Pod URL: {pod_url}")

    return pod_url


def wait_for_server(pod_url, max_attempts=60, interval=5):
    """Wait until the Faster Whisper API becomes available."""
    print("\nWaiting for server to become ready...")

    for attempt in range(1, max_attempts + 1):
        try:
            response = requests.get(f"{pod_url}/v1/models", timeout=10)
            if response.status_code == 200:
                print("✓ Server is ready!")
                return True
        except requests.RequestException:
            pass

        print(f"  Attempt {attempt}/{max_attempts} - Not ready yet...")
        time.sleep(interval)

    print("✗ Server did not become ready in time.")
    return False


def download_model(pod_url):
    """Trigger model download on the Faster Whisper server."""
    model_name = settings.runpod.faster_whisper_model
    print(f"\nDownloading model: {model_name}")

    try:
        response = requests.post(
            f"{pod_url}/v1/models/{model_name}",
            timeout=300,
        )

        if response.status_code == 200:
            print(f"✓ Model '{model_name}' downloaded successfully!")
        else:
            print(f"✗ Failed to download model (Status: {response.status_code})")
            print(f"  Response: {response.text}")

    except requests.RequestException as error:
        print(f"✗ Error while downloading model: {error}")


def main():
    pod_url = create_faster_whisper_pod()

    if not wait_for_server(pod_url):
        exit(1)

    download_model(pod_url)

    print("\n" + "=" * 70)
    print("🎉 Setup Complete!")
    print("=" * 70)
    print("\nAdd the following to your .env file:\n")
    print(f"RUNPOD__FASTER_WHISPER_POD_URL={pod_url}")
    print("\n" + "=" * 70)


if __name__ == "__main__":
    main()