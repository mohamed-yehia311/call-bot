"""
Interactive application to make outbound calls using the Twilio integration.
.
"""

import sys
from dataclasses import dataclass
from typing import Callable, Optional, Tuple

import requests
from loguru import logger


@dataclass
class CallConfig:
    """Configuration for the outbound call."""
    from_number: str
    to_number: str
    voice_agent_url: str
    api_base_url: str = "http://localhost:8000"


# --- Validation Functions ---

def validate_phone_number(number: str) -> Tuple[bool, str]:
    """Validates phone number format (E.164)."""
    if not number.startswith("+"):
        return False, "Phone number should be in E.164 format (starting with +)"
    if len(number) < 10:
        return False, "Phone number seems too short"
    if not number[1:].replace(" ", "").isdigit():
        return False, "Phone number should only contain digits after the +"
    return True, ""


def validate_url(url: str) -> Tuple[bool, str]:
    """Validates URL format."""
    if not (url.startswith("http://") or url.startswith("https://")):
        return False, "URL should start with http:// or https://"
    return True, ""


# --- UI Helpers ---

def print_banner():
    """Print welcome banner."""
    banner = """
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║    📞    OUTBOUND CALL CENTER SYSTEM    📞              ║
║                                                           ║
║      Make AI-powered phone calls with ease!               ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
"""
    print(banner)


def print_section_header(title: str):
    """Print a formatted section header."""
    print(f"\n{'═' * 60}\n  {title}\n{'═' * 60}\n")


def get_validated_input(
    prompt: str,
    example: str = "",
    validator: Optional[Callable[[str], Tuple[bool, str]]] = None
) -> str:
    """Gets and validates user input."""
    while True:
        display_prompt = f"📝 {prompt}"
        if example:
            display_prompt += f"\n   Example: {example}"
        
        value = input(f"{display_prompt}\n   → ").strip()

        if not value:
            print("   ❌ This field is required.\n")
            continue

        if validator:
            is_valid, message = validator(value)
            if not is_valid:
                print(f"   ⚠️  {message}\n")
                if input("   Continue anyway? (y/n): ").strip().lower() != "y":
                    continue
        
        return value


# --- Core Logic ---

def initiate_call(config: CallConfig) -> dict:
    """Initiates an outbound call through the API."""
    endpoint = f"{config.api_base_url}/call"
    payload = {
        "from": config.from_number,
        "to": config.to_number,
        "voice_agent_url": config.voice_agent_url,
    }

    try:
        response = requests.post(endpoint, json=payload, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        error_detail = e.response.text if e.response is not None else str(e)
        raise RuntimeError(f"API call failed: {error_detail}")


def run_interactive_session() -> Optional[CallConfig]:
    """Guides the user through setting up call parameters."""
    print_banner()
    print("Welcome! Let's set up your outbound call.\n"
          "ℹ️  Numbers: E.164 format (e.g., +1234567890)\n"
          "ℹ️  URL: Publicly accessible (e.g., ngrok)\n")

    from_num = get_validated_input(
        "Enter Twilio number (From)", "+11234567890", validate_phone_number
    )
    agent_url = get_validated_input(
        "Enter Voice Agent URL", "https://abc.ngrok.io", validate_url
    )
    to_num = get_validated_input(
        "Enter Recipient number (To)", "+10987654321", validate_phone_number
    )

    # Confirmation step
    print_section_header("📋 CONFIRM CALL DETAILS")
    print(f"   From: {from_num}\n   To: {to_num}\n   Agent: {agent_url}\n")
    
    if input("   Proceed? (y/n): ").strip().lower() != "y":
        print("\n❌ Call cancelled by user.")
        return None

    return CallConfig(from_number=from_num, to_number=to_num, voice_agent_url=agent_url)


# --- Main ---

def main():
    """Main execution function."""
    logger.remove()  # Disable logger for clean CLI output

    config = run_interactive_session()
    if not config:
        return 0

    print_section_header("📞 INITIATING CALL")
    print("   Please wait...\n")

    try:
        result = initiate_call(config)
        print(f"   ✅ SUCCESS! SID: {result.get('sid')}")
        print(f"   📱 Ringing {config.to_number}...\n")
        return 0
    except Exception as e:
        print(f"   ❌ ERROR: {e}\n")
        print("   Troubleshooting: Check API status and .env credentials.\n")
        return 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n❌ Cancelled by user.\n")
        sys.exit(0)