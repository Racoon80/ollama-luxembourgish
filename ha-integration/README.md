# Home Assistant Integration for Ollama Luxembourgish

This integration makes the Ollama Luxembourgish model compatible with Home Assistant's conversation/voice assistant features.

## Architecture

```
Home Assistant (ha.racoon.lu)
          ↓
OpenAI-Compatible Proxy (192.168.106.23:8000)
          ↓
Ollama Luxembourgish (192.168.106.22:11434)
          ↓
LLaMAX3-8B-Alpaca Model (lux-assistant)
```

## Components

1. **OpenAI-Compatible Proxy**: Translates OpenAI API format to Ollama format
2. **Home Assistant OpenAI Conversation**: Built-in integration using the proxy
3. **Voice Assistant Pipeline**: Complete Luxembourgish voice assistant

## Quick Start

### 1. Deploy the Proxy

```bash
# SSH to Unraid
ssh root@192.168.10.100

# Navigate to integration directory
cd /mnt/user/appdata/ai/ollama-luxembourgish/ha-integration

# Build and start the proxy
docker-compose up -d

# Verify it's running
curl http://192.168.106.23:8000/health
```

### 2. Configure Home Assistant

Add to your `configuration.yaml`:

```yaml
conversation:
  - platform: openai
    name: "Lux Assistant"
    api_key: "sk-lux-homeassistant"
    base_url: "http://192.168.106.23:8000/v1"
    model: "lux-assistant"
    temperature: 0.7
    max_tokens: 2000
```

### 3. Restart Home Assistant

```bash
# Via Home Assistant UI
Settings → System → Restart

# Or via command line
ssh root@192.168.10.77
ha core restart
```

### 4. Test the Integration

Go to Home Assistant → Settings → Voice Assistants → Assist → Try It

Ask: "Moien! Wéi geet et?"

## Configuration Options

### Temperature
Controls randomness (0.0 = deterministic, 1.0 = creative)
```yaml
temperature: 0.7  # Balanced
```

### Max Tokens
Maximum length of response
```yaml
max_tokens: 2000  # ~1500 words
```

### Context Threshold
Number of conversation turns to remember
```yaml
context_threshold: 1  # Only current message (faster)
context_threshold: 5  # Remember 5 turns (better context)
```

## Voice Assistant Setup

### Complete Pipeline with Wyoming Services

```yaml
assist_pipeline:
  - name: "Luxembourgish Voice Assistant"
    language: "lb"

    # Wake Word
    wake_word_entity: "binary_sensor.roberto_wake_word"

    # Speech-to-Text (if you have Luxembourgish STT)
    stt_engine: "faster_whisper"
    stt_language: "lb"

    # Conversation (Ollama Luxembourgish)
    conversation_engine: "Lux Assistant"
    conversation_language: "lb"

    # Text-to-Speech (Fish-Speech TTS)
    tts_engine: "fish_speech_luxembourgish"
    tts_language: "lb"
```

### Services Integration

Connect your existing services:
- **Wake Word**: Ha-WakeWord-LU (192.168.106.20) - "Roberto"
- **STT**: Your Luxembourgish STT service
- **Conversation**: Ollama Luxembourgish (via proxy) - NEW
- **TTS**: Fish-Speech Luxembourgish (192.168.106.15)

## API Endpoints

### List Models
```bash
curl http://192.168.106.23:8000/v1/models
```

### Chat Completion
```bash
curl http://192.168.106.23:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer sk-lux-homeassistant" \
  -d '{
    "model": "lux-assistant",
    "messages": [
      {"role": "user", "content": "Moien! Wéi geet et?"}
    ]
  }'
```

### Streaming Chat
```bash
curl http://192.168.106.23:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer sk-lux-homeassistant" \
  -d '{
    "model": "lux-assistant",
    "messages": [
      {"role": "user", "content": "Erziel mir eng Geschicht"}
    ],
    "stream": true
  }'
```

## Security

### API Key
The proxy requires an API key for authentication:
- **Default**: `sk-lux-homeassistant`
- **Change**: Edit `ollama-openai-proxy.py` and rebuild

### Network
- Proxy runs on internal network (br0.106)
- Not exposed to internet
- Only accessible from Home Assistant

## Troubleshooting

### Proxy Not Responding
```bash
# Check container status
docker ps | grep ollama-openai-proxy

# View logs
docker logs ollama-openai-proxy -f

# Restart
cd /mnt/user/appdata/ai/ollama-luxembourgish/ha-integration
docker-compose restart
```

### Home Assistant Can't Connect
```bash
# Test from Home Assistant host
curl http://192.168.106.23:8000/health

# Check Home Assistant logs
Settings → System → Logs → Filter: "openai"
```

### Slow Responses
- Check Ollama GPU usage: `nvidia-smi`
- Reduce `max_tokens` in config
- Increase timeout in Home Assistant

### Not Responding in Luxembourgish
- Model is multilingual, may respond in other languages
- Add Luxembourgish examples in conversation
- Use Extended OpenAI Conversation for better prompts

## Advanced Configuration

### Extended OpenAI Conversation

For more control, use the Extended OpenAI Conversation custom component:

1. Install via HACS: https://github.com/jekalmin/extended_openai_conversation

2. Add to `configuration.yaml`:
```yaml
extended_openai_conversation:
  - name: "Lux Assistant Extended"
    api_key: "sk-lux-homeassistant"
    base_url: "http://192.168.106.23:8000/v1"
    model: "lux-assistant"
    temperature: 0.7
    max_tokens: 2000

    # Custom system prompt
    prompt: |
      Du bass en Lëtzebuergesche Assistent fir en Smart Home.
      Schwätz ËMMER Lëtzebuergesch.
      Hëllef de Benotzer mat Hausautomatiséierung.

    # Function calling for HA entities
    functions:
      - spec:
          name: execute_services
          description: Execute Home Assistant services
          parameters:
            type: object
            properties:
              list:
                type: array
```

### Custom System Prompt

Edit `ollama-openai-proxy.py` to add a default system message:

```python
# In chat_completions() function, before processing messages:
messages.insert(0, {
    "role": "system",
    "content": "Du bass en Lëtzebuergesche Smart Home Assistent. Schwätz ëmmer Lëtzebuergesch."
})
```

## Performance

- **Response Time**: 1-3 seconds (first token)
- **Streaming**: ~30-50 tokens/second
- **Memory**: ~5-6GB VRAM
- **Concurrent Requests**: 1-2 (single GPU)

## Network Topology

```
br0.106 Network:
├── 192.168.106.7   - openWakeWord (Alexa)
├── 192.168.106.8   - OllamaUI
├── 192.168.106.15  - Fish-Speech TTS (Luxembourgish)
├── 192.168.106.20  - Ha-WakeWord-LU (Roberto)
├── 192.168.106.22  - Ollama Luxembourgish (LLM)
└── 192.168.106.23  - OpenAI Proxy (NEW)
```

## Files

- `docker-compose.yml` - Proxy deployment
- `Dockerfile` - Proxy image
- `ollama-openai-proxy.py` - Proxy server
- `home-assistant-config.yaml` - HA configuration template
- `README.md` - This file

## Testing

### Test the Proxy
```python
import requests

response = requests.post(
    "http://192.168.106.23:8000/v1/chat/completions",
    headers={"Authorization": "Bearer sk-lux-homeassistant"},
    json={
        "model": "lux-assistant",
        "messages": [
            {"role": "user", "content": "Moien!"}
        ]
    }
)
print(response.json())
```

### Test in Home Assistant

**Developer Tools → Services:**
```yaml
service: conversation.process
data:
  text: "Moien! Wéi geet et?"
  agent_id: conversation.lux_assistant
```

## Updating

### Update Proxy
```bash
cd /mnt/user/appdata/ai/ollama-luxembourgish/ha-integration
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### Update Model
The proxy automatically uses the latest Ollama model. Just restart:
```bash
docker-compose restart
```

## Resources

- **OpenAI API Docs**: https://platform.openai.com/docs/api-reference
- **HA Conversation**: https://www.home-assistant.io/integrations/conversation/
- **HA Voice Pipeline**: https://www.home-assistant.io/voice_control/
- **Extended OpenAI**: https://github.com/jekalmin/extended_openai_conversation

---

**Status**: ✅ Ready for Deployment
**Proxy**: http://192.168.106.23:8000
**API**: OpenAI-compatible
**Model**: lux-assistant (Luxembourgish)
