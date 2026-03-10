# Call Bot - Realtime Phone Agents

A sophisticated real-time phone agent system that combines conversational AI, voice processing, and property search capabilities. This project enables building intelligent conversational agents that can conduct natural phone conversations with advanced speech-to-text, text-to-speech, and semantic search capabilities.

## Overview

Call Bot is an enterprise-grade framework for building AI-powered phone agents using:
- **Real-time Voice Communication**: WebRTC-based bidirectional audio streaming via FastRTC
- **Advanced LLM Integration**: Support for Groq, Gemini, and compatible OpenAI-based models
- **Flexible STT/TTS**: Multiple speech processing backends (local, Groq, RunPod)
- **Semantic Search**: Superlinked vector database integration for intelligent property search
- **Voice Effects**: Audio processing, keyboard effects, and sound management
- **Multi-Avatar Support**: Configurable agent personalities with YAML-based definitions

## Features

✨ **Core Capabilities**
- Real-time bidirectional voice streaming via WebRTC
- Multiple large language model integrations (Groq, OpenAI, Gemini)
- Speech-to-text processing with multiple backends
- Natural text-to-speech synthesis
- Voice activity detection (VAD)
- Semantic property search with vector embeddings
- Customizable agent avatars and personalities

🎯 **Speech Processing Options**
- **STT**: Groq Whisper (cloud), Local Moonshine, RunPod Faster Whisper (GPU)
- **TTS**: Local Kokoro, RunPod Orphus, TogetherAI

🔧 **Infrastructure**
- FastAPI-based REST API
- Qdrant vector database for similarity search
- Superlinked for intelligent indexing and querying
- RunPod integration for scalable GPU inference
- Twilio integration for phone infrastructure

## Project Structure

```
call_bot/
├── src/
│   ├── api/                    # FastAPI application and routes
│   │   ├── main.py            # FastAPI app factory
│   │   ├── models.py          # Pydantic data models
│   │   └── routes/            # API endpoint modules
│   │       ├── health.py       # Health check endpoints
│   │       ├── voice.py        # Voice streaming endpoints
│   │       └── superlinked.py  # Property search endpoints
│   ├── Agent/                  # Core agent logic
│   │   ├── fastrtcagent.py    # FastRTC agent implementation
│   │   ├── stream.py          # Audio stream management
│   │   ├── utils.py           # Agent utilities
│   │   └── tools/             # Agent tools
│   │       └── property_search.py  # Property search integration
│   ├── infrastructure/         # Backend services
│   │   └── superlinked/       # Vector search service
│   │       ├── index.py       # Index management
│   │       ├── query.py       # Search queries
│   │       ├── service.py     # Service layer
│   │       └── constants.py   # Configuration constants
│   ├── stt/                   # Speech-to-text implementations
│   │   ├── base.py            # Base STT class
│   │   ├── groq/              # Groq Whisper STT
│   │   ├── local/             # Local Moonshine STT
│   │   └── runpod/            # RunPod Faster Whisper STT
│   ├── tts/                   # Text-to-speech implementations
│   │   ├── base.py            # Base TTS class
│   │   ├── local/             # Local Kokoro TTS
│   │   ├── runpod/            # RunPod Orphus TTS
│   │   └── togetherai/        # TogetherAI TTS
│   ├── voice/                 # Voice processing and effects
│   │   ├── effects/           # Audio effects (keyboard, etc.)
│   │   └── utils/             # Audio utilities and loaders
│   ├── avatars/               # Agent avatar definitions
│   │   ├── base.py            # Base avatar class
│   │   ├── registry.py        # Avatar registry
│   │   └── definitions/       # YAML avatar configs
│   ├── observablility/        # Monitoring and observability
│   │   └── prompt_versioning.py  # Prompt version tracking
│   └── config.py              # Configuration management
├── scripts/                   # Utility scripts
│   ├── ingest_properties.py   # Property data ingestion
│   ├── make_outbound_call.py  # Outbound call script
│   ├── run_gradio_application.py  # Gradio UI launcher
│   └── runpod/               # RunPod deployment scripts
├── data/
│   └── properties.csv         # Property dataset
├── pyproject.toml             # Project dependencies and metadata
└── README.md                  # This file
```

## Installation

### Prerequisites
- Python 3.11+
- CUDA-capable GPU (optional, recommended for local STT/TTS)
- Docker & Docker Compose (for vector database)

### Quick Start

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/call-bot.git
cd call-bot
```

2. **Install dependencies**
```bash
pip install -e .
```

3. **Set up environment variables**
Create a `.env` file in the project root:
```env
# Language Model APIs
GROQ_API_KEY=your_groq_api_key
OPENAI_API_KEY=your_openai_api_key
GEMINI_API_KEY=your_gemini_api_key

# Qdrant Vector Database
QDRANT_API_KEY=your_qdrant_api_key
QDRANT_URL=your_qdrant_cluster_url

# RunPod (if using GPU backends)
RUNPOD_API_KEY=your_runpod_api_key

# Twilio (optional, for phone integration)
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
```

4. **Start the vector database (Qdrant)**
```bash
docker-compose up -d qdrant
```

5. **Run the API server**
```bash
python -m src.api.main
```

The API will be available at `http://localhost:8000` with documentation at `/api/docs`.

## Usage

### Running a Voice Agent Session

```python
from src.Agent.fastrtcagent import FastRTCAgent
from src.config import Settings

# Initialize configuration
settings = Settings()

# Create agent instance
agent = FastRTCAgent(
    name="Property Assistant",
    llm_provider="groq",
    stt_backend="groq",  # or "local", "runpod"
    tts_backend="local",  # or "runpod", "togetherai"
)

# Start listening and responding
await agent.start()
```

### Property Search
```python
from src.infrastructure.superlinked.service import get_search_service

service = get_search_service()
results = service.search(
    query="2 bedroom apartment under 500k EGP in Cairo",
    limit=10
)
```

### Data Ingestion

Ingest property data into the vector database:
```bash
python scripts/ingest_properties.py --csv-path data/properties.csv
```

### Gradio Interface

Run the interactive Gradio application:
```bash
python scripts/run_gradio_application.py
```

## Configuration

Configuration is managed through `src/config.py` and environment variables. Key settings include:

### LLM Settings
- **Groq**: OpenAI-compatible LLM provider
- **Gemini**: Google's latest generative model
- **OpenAI**: GPT models

### STT/TTS Settings
- **Groq Whisper**: Fast cloud-based speech recognition
- **Local Moonshine**: On-device STT (privacy-focused)

### Vector Search
- **Superlinked**: Intelligent semantic indexing and retrieval
- **Qdrant**: Scalable vector database with cloud support

### Voice Processing
- **Sample Rate**: 16kHz (configurable)
- **Audio Effects**: Keyboard sounds, voice modulation
- **Voice Activity Detection**: Configurable sensitivity

## Development

### Running Tests
```bash
pytest tests/ -v
```

### Code Structure Guidelines
- **API Routes**: Define FastAPI endpoints in `src/api/routes/`
- **Agent Logic**: Implement agent behaviors in `src/Agent/`
- **Tools**: Add new tools in `src/Agent/tools/`
- **STT/TTS**: Extend base classes in `src/stt/` and `src/tts/`
- **Avatars**: Add new avatars as YAML files in `src/avatars/definitions/`

### Adding a New STT Backend
1. Create a new module in `src/stt/`
2. Extend the `BaseSTT` class
3. Register in the STT factory

### Adding a New Avatar
1. Create a YAML file in `src/avatars/definitions/`
2. Define personality, voice characteristics, and behaviors
3. Register in the avatar registry

## Deployment

### Docker Deployment
Build and run with Docker:
```bash
docker build -t call-bot .
docker run -p 8000:8000 call-bot
```

### RunPod Deployment
Deploy GPU-accelerated components to RunPod:
```bash
python scripts/runpod/create_faster_whisper_pod.py
python scripts/runpod/create_call_center.py
```

### Cloud Deployment (Azure, AWS, GCP)
The system is containerized and compatible with standard cloud platforms.

## Architecture

### Voice Pipeline
```
User Voice (WebRTC)
    ↓
[Voice Activity Detection]
    ↓
[Speech-to-Text] (Groq/Local/RunPod)
    ↓
[LLM Agent] (Groq/OpenAI/Gemini)
    ↓
[Text-to-Speech] (Local/RunPod/TogetherAI)
    ↓
User Speaker (WebRTC)
```

### Search Pipeline
```
User Query
    ↓
[Text Embedding] (Superlinked)
    ↓
[Vector Search] (Qdrant)
    ↓
[Re-ranking]
    ↓
[Context Integration] (to LLM)
```

## Performance Considerations

- **Latency**: Stream processing enables <500ms response times
- **Throughput**: Horizontal scaling via API instances
- **Concurrency**: Support for multiple simultaneous calls
- **GPU Usage**: Efficient batching with RunPod backends

## Troubleshooting

### Common Issues

**WebRTC Connection Failed**
- Verify firewall settings and port accessibility
- Check CORS configuration in `src/api/main.py`
- Ensure browser has microphone permissions

**STT Errors**
- Verify API keys for cloud backends (Groq, RunPod)
- Check audio quality and sample rate
- Review logs in `logs/`

**Search Not Returning Results**
- Ensure properties are ingested: `python scripts/ingest_properties.py`
- Verify Qdrant connection
- Check embedding model configuration

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## License

[Add your license here]

## Support

For issues and questions:
- 📧 Email: [your-email]
- 💬 Discord: [your-discord-link]
- 🐛 Issues: [GitHub Issues Link]

## Acknowledgments

- [FastRTC](https://github.com/pipecat-ai/pipecat) for real-time voice processing
- [Superlinked](https://superlinked.com) for vector search infrastructure
- [Groq](https://groq.com) for fast LLM inference
- [Qdrant](https://qdrant.tech) for vector database

---

**Made with ❤️ for building the next generation of voice AI**