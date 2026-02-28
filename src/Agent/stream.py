from typing import Any, Callable, Literal
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
from gradio.components.base import Component
from fastrtc import Stream
from fastrtc.tracks import HandlerType
from fastrtc.utils import RTCConfigurationCallable

class VoiceAgentStream(Stream):
    """
    A specialized FastRTC Stream for voice agents, handling both web-based
    audio streaming and traditional telephony connections (e.g., Twilio).
    """

    def __init__(
        self,
        handler: HandlerType,
        *,
        mode: Literal["send-receive", "receive", "send"] = "send-receive",
        modality: Literal["video", "audio", "audio-video"] = "audio",
        additional_outputs_handler: Callable | None = None,
        additional_inputs: list[Component] | None = None,
        additional_outputs: list[Component] | None = None,
        rtc_configuration: RTCConfigurationCallable | None = None,
        ui_args: dict[str, Any] | None = None,
        **kwargs,
    ):
        # Set default modality to 'audio' for a voice agent
        super().__init__(
            handler=handler,
            mode=mode,
            modality=modality,
            additional_outputs_handler=additional_outputs_handler,
            additional_inputs=additional_inputs,
            additional_outputs=additional_outputs,
            rtc_configuration=rtc_configuration,
            ui_args=ui_args,
            **kwargs,
        )

    async def handle_incoming_call(self, request: Request) -> HTMLResponse:
        """
        Handles incoming telephone calls, generating TwiML to connect
        the call to the WebSocket handler.
        """
        from twilio.twiml.voice_response import Connect, VoiceResponse

        # Determine the host for the WebSocket connection
        hostname = request.headers.get("x-forwarded-host", request.url.hostname)
        path = request.url.path.removesuffix("/telephone/incoming")
        ws_url = f"wss://{hostname}{path}/telephone/handler"

        # Construct TwiML response
        response = VoiceResponse()
        response.say("Connecting to the AI assistant.")
        
        connect = Connect()
        connect.stream(url=ws_url)
        response.append(connect)
        
        response.say("The call has been disconnected.")
        return HTMLResponse(content=str(response), media_type="application/xml")