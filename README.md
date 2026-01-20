# Ollama Luxembourgish - LLaMAX3-8B-Alpaca

Dedicated Ollama instance enforced for Luxembourgish language responses using LLaMAX3-8B-Alpaca model.

## Model Information

**Model**: LLaMAX3-8B-Alpaca
**Parameters**: 8B
**Language Support**: 102 languages including **Luxembourgish (lb)**
**Ollama ID**: `mannix/llamax3-8b-alpaca`

### Why This Model?

- **Explicit Luxembourgish Support**: One of the few 8B models with proven Luxembourgish capabilities
- **Multilingual**: Supports code-switching between Luxembourgish, German, and French (common in Luxembourg)
- **Recent**: Released in 2024 with state-of-the-art multilingual performance
- **Optimized**: 10+ spBLEU points improvement over other open-source LLMs
- **Available**: Ready to use on Ollama

## Quick Start

### Deployment on Unraid

```bash
# SSH to Unraid
ssh root@192.168.10.100

# Navigate to deployment directory
cd /mnt/user/appdata/ai/ollama-luxembourgish

# Start container
docker-compose up -d

# Wait for container to start (30 seconds)
sleep 30

# Pull the Luxembourgish model (2-5 minutes, ~4.7GB)
docker exec ollama-luxembourgish ollama pull mannix/llamax3-8b-alpaca

# Create custom Luxembourgish-enforced model
docker exec ollama-luxembourgish ollama create lux-assistant -f /modelfile

# Test it
docker exec -it ollama-luxembourgish ollama run lux-assistant "Wéi geet et?"
```

## Configuration

### Network
- **IP Address**: 192.168.106.22
- **Port**: 11434
- **Network**: br0.106 (macvlan)

### GPU
- **Enabled**: Yes (NVIDIA GPU)
- **Memory**: Shared with system

### Storage
- **Models Directory**: /mnt/user/appdata/ai/ollama-luxembourgish
- **Persistent**: Yes

## Usage

### API Endpoint
```bash
curl http://192.168.106.22:11434/api/generate -d '{
  "model": "lux-assistant",
  "prompt": "Wat ass d'Haaptstad vu Lëtzebuerg?",
  "stream": false
}'
```

### Interactive Chat
```bash
# SSH to Unraid
ssh root@192.168.10.100

# Run interactive chat
docker exec -it ollama-luxembourgish ollama run lux-assistant
```

### From OllamaUI (192.168.106.8)
1. Open http://192.168.106.8
2. Add new Ollama connection:
   - URL: `http://192.168.106.22:11434`
   - Name: Ollama Luxembourgish
3. Select model: `lux-assistant`
4. Start chatting in Luxembourgish!

## Model Behavior

The custom `lux-assistant` model is configured to:

### Always Respond in Luxembourgish
- Regardless of input language
- Enforced through system prompt
- Code-switching support (understands German/French/English)

### Examples

**User (English)**: "What is the capital of Luxembourg?"
**Response**: "D'Haaptstad vu Lëtzebuerg ass d'Stad Lëtzebuerg selwer."

**User (German)**: "Wie spät ist es?"
**Response**: "Ech äntweren op Lëtzebuergesch. Wéi spéit et ass, dat hänkt vun Ärer Zäitzon of."

**User (Luxembourgish)**: "Wéi kann ech Iech hëllefen?"
**Response**: "Merci fir d'Offer! Ech sinn hei fir Iech ze hëllefen mat all Froen oder Aufgaben op Lëtzebuergesch."

## Models Available

### 1. mannix/llamax3-8b-alpaca (Base Model)
- Original multilingual model
- Responds in input language
- General-purpose

```bash
docker exec -it ollama-luxembourgish ollama run mannix/llamax3-8b-alpaca
```

### 2. lux-assistant (Luxembourgish-Enforced)
- Custom model with Luxembourgish system prompt
- Always responds in Luxembourgish
- Optimized parameters

```bash
docker exec -it ollama-luxembourgish ollama run lux-assistant
```

## Management Commands

### Check Running Models
```bash
docker exec ollama-luxembourgish ollama list
```

### View Container Logs
```bash
docker logs ollama-luxembourgish -f
```

### Restart Container
```bash
cd /mnt/user/appdata/ai/ollama-luxembourgish
docker-compose restart
```

### Update Model
```bash
docker exec ollama-luxembourgish ollama pull mannix/llamax3-8b-alpaca
docker exec ollama-luxembourgish ollama create lux-assistant -f /modelfile
```

### Remove Model
```bash
docker exec ollama-luxembourgish ollama rm lux-assistant
docker exec ollama-luxembourgish ollama rm mannix/llamax3-8b-alpaca
```

## Technical Details

### Model Architecture
- **Base**: LLaMA 3 8B
- **Training**: Continued pre-training for multilingual support
- **Languages**: 102 (including Luxembourgish)
- **Context Window**: 4096 tokens
- **Quantization**: GGUF format for efficient inference

### System Requirements
- **GPU**: NVIDIA GPU recommended (CUDA)
- **RAM**: 8GB+ recommended
- **Storage**: ~5GB for model
- **Network**: 1Gbps+ for model download

### Performance
- **First Token**: ~200-500ms (GPU)
- **Generation Speed**: ~30-50 tokens/second (GPU)
- **Context**: 4096 tokens

## Integration Examples

### Python
```python
import requests

def ask_luxembourgish(question):
    response = requests.post(
        "http://192.168.106.22:11434/api/generate",
        json={
            "model": "lux-assistant",
            "prompt": question,
            "stream": False
        }
    )
    return response.json()["response"]

# Test
print(ask_luxembourgish("Wat ass Lëtzebuerg?"))
```

### Home Assistant
```yaml
# configuration.yaml
conversation:
  intents:
    LuxembourghishIntent:
      - "Schwätz Lëtzebuergesch"

rest_command:
  ollama_luxembourgish:
    url: http://192.168.106.22:11434/api/generate
    method: POST
    payload: >
      {
        "model": "lux-assistant",
        "prompt": "{{ prompt }}",
        "stream": false
      }
    content_type: "application/json"
```

### curl Examples
```bash
# Simple generation
curl http://192.168.106.22:11434/api/generate -d '{
  "model": "lux-assistant",
  "prompt": "Erklär mir wat en Computer ass.",
  "stream": false
}'

# Chat conversation
curl http://192.168.106.22:11434/api/chat -d '{
  "model": "lux-assistant",
  "messages": [
    {"role": "user", "content": "Moien! Wéi geet et?"}
  ],
  "stream": false
}'
```

## Troubleshooting

### Model Not Responding in Luxembourgish
- Verify custom model is created: `docker exec ollama-luxembourgish ollama list`
- Recreate model: `docker exec ollama-luxembourgish ollama create lux-assistant -f /modelfile`
- Check system prompt is loaded

### Container Won't Start
- Check GPU availability: `nvidia-smi`
- Verify network br0.106 exists: `docker network ls`
- Check IP address availability: `ping 192.168.106.22`

### Model Download Fails
- Check internet connection
- Verify disk space: `df -h /mnt/user/appdata/ai/ollama-luxembourgish`
- Try manual pull: `docker exec ollama-luxembourgish ollama pull mannix/llamax3-8b-alpaca`

### Slow Performance
- Verify GPU is being used: `docker logs ollama-luxembourgish | grep -i gpu`
- Check GPU memory: `nvidia-smi`
- Reduce context window in modelfile

## Resources

- **Model on Hugging Face**: https://huggingface.co/LLaMAX/LLaMAX3-8B
- **Ollama Model**: https://ollama.com/mannix/llamax3-8b-alpaca
- **Research Paper**: Text Generation Models for Luxembourgish
- **Ollama Documentation**: https://ollama.com/docs

## Version History

- **v1.0** (2026-01-20): Initial deployment with LLaMAX3-8B-Alpaca
  - Luxembourgish-enforced system prompt
  - GPU acceleration
  - Network integration on br0.106

## License

Models and code follow their respective licenses:
- LLaMAX3-8B-Alpaca: Apache 2.0
- Ollama: MIT
- This configuration: MIT

---

**Deployed**: 2026-01-20
**Model**: LLaMAX3-8B-Alpaca
**IP**: 192.168.106.22:11434
**Status**: Luxembourgish-enforced
