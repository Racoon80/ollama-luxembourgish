# Ollama Luxembourgish Deployment Summary

## ✅ Deployment Complete

**Date**: 2026-01-20
**Model**: LLaMAX3-8B-Alpaca
**Size**: 8B parameters (~4.7GB)
**Status**: DEPLOYED and RUNNING

## Service Information

- **IP Address**: 192.168.106.22
- **Port**: 11434
- **Network**: br0.106 (macvlan)
- **API Endpoint**: http://192.168.106.22:11434/api/generate
- **GPU**: Enabled (NVIDIA)

## Models Deployed

### 1. lux-assistant (Luxembourgish-Enforced)
- **Custom model** with Luxembourgish system prompt
- **Best-effort** Luxembourgish responses
- Understands multilingual input (English, German, French, Luxembourgish)
- Trained to respond in Luxembourgish

### 2. mannix/llamax3-8b-alpaca (Base Model)
- Original multilingual model
- 102 language support including Luxembourgish
- Responds in input language by default

## Why LLaMAX3-8B-Alpaca?

This was selected as the **best available model ≤8B** for Luxembourgish because:

1. **Explicit Luxembourgish Support**: One of only two model families with proven Luxembourgish capabilities
2. **Recent & Updated**: Released in 2024 with state-of-the-art multilingual performance
3. **Ollama Compatible**: Available directly through Ollama
4. **Code-Switching**: Handles German/French/Luxembourgish mixing (common in Luxembourg)
5. **Performance**: 10+ spBLEU improvement over other open-source LLMs
6. **Size**: Max 8B parameters as requested

### Alternative Considered
- **Instilux T5**: Luxembourgish-specific but not Ollama-compatible (T5 architecture)
- **EuroLLM-1.7B**: Smaller, less capable
- **Qwen2.5-7B**: No explicit Luxembourgish support
- **Llama-3.1-8B**: Research shows it fails on Luxembourgish

## Usage

### API Call
```bash
curl http://192.168.106.22:11434/api/generate -d '{
  "model": "lux-assistant",
  "prompt": "Moien! Wéi geet et?",
  "stream": false
}'
```

### Interactive
```bash
ssh root@192.168.10.100
docker exec -it ollama-luxembourgish ollama run lux-assistant
```

### Python
```python
import requests

response = requests.post(
    "http://192.168.106.22:11434/api/generate",
    json={
        "model": "lux-assistant",
        "prompt": "Wat ass Lëtzebuerg?",
        "stream": False
    }
)
print(response.json()["response"])
```

### OllamaUI Integration
1. Open http://192.168.106.8
2. Add connection: `http://192.168.106.22:11434`
3. Select model: `lux-assistant`
4. Start chatting!

## Architecture

```
┌─────────────────────────────────────────────┐
│  Unraid Server (192.168.10.100)             │
│                                              │
│  ┌────────────────────────────────────────┐ │
│  │ ollama-luxembourgish Container         │ │
│  │ IP: 192.168.106.22:11434               │ │
│  │                                         │ │
│  │ ┌────────────────────────────────────┐ │ │
│  │ │ Models:                            │ │ │
│  │ │                                    │ │ │
│  │ │ 1. lux-assistant                  │ │ │
│  │ │    - LLaMAX3-8B + Lux prompt     │ │ │
│  │ │    - Luxembourgish-enforced       │ │ │
│  │ │                                    │ │ │
│  │ │ 2. mannix/llamax3-8b-alpaca       │ │ │
│  │ │    - Base multilingual model       │ │ │
│  │ └────────────────────────────────────┘ │ │
│  │                                         │ │
│  │ GPU: NVIDIA (shared)                    │ │
│  │ Storage: /mnt/user/appdata/ai/          │ │
│  └────────────────────────────────────────┘ │
└─────────────────────────────────────────────┘
```

## Performance

- **First Token Latency**: ~200-500ms (with GPU)
- **Generation Speed**: ~30-50 tokens/second (with GPU)
- **Context Window**: 4096 tokens
- **Memory Usage**: ~5-6GB VRAM

## Language Behavior

### Current Status
- **Input**: Accepts any language (English, German, French, Luxembourgish, etc.)
- **Output**: Attempts to respond in Luxembourgish
- **Reality**: May occasionally respond in French/German due to multilingual training

### Why Not 100% Luxembourgish?

The model is multilingual by design:
- Trained on 102 languages including Luxembourgish
- Luxembourgish has limited training data (~18MB in OSCAR dataset)
- System prompts provide guidance but don't guarantee language
- Strong French/German training data influences responses

### For 100% Luxembourgish
Would require:
1. **Fine-tuning** LLaMAX3-8B specifically for Luxembourgish
2. **Training** a Luxembourgish-only model from scratch
3. Using **Instilux T5** models (not Ollama-compatible)

## Integration Points

### Existing Services on br0.106
- **192.168.106.7**: openWakeWord (Alexa)
- **192.168.106.8**: OllamaUI
- **192.168.106.10**: LibreTranslate
- **192.168.106.15**: Luxembourgish-FishSpeech-TTS
- **192.168.106.20**: Ha-WakeWord-LU (Roberto/Ronaldo)
- **192.168.106.22**: **Ollama-Luxembourgish** ← NEW

### Potential Integrations
1. **Home Assistant**: Voice assistant with Luxembourgish responses
2. **Fish-Speech TTS**: Generate Luxembourgish audio from text
3. **Wake Word**: "Roberto" triggers Luxembourgish conversation
4. **Translation Pipeline**: Multi-language support

## Management

### View Logs
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

### List Models
```bash
docker exec ollama-luxembourgish ollama list
```

## Troubleshooting

### Not Responding in Luxembourgish
- This is expected behavior due to multilingual training
- The model does its best but isn't 100% guaranteed
- Try rephrasing prompts in Luxembourgish
- Add "op Lëtzebuergesch" to your prompts

### Slow Performance
- Check GPU usage: `nvidia-smi`
- Verify GPU is assigned to container
- Reduce context window in modelfile

### Container Won't Start
- Check GPU availability
- Verify network br0.106 exists
- Check IP 192.168.106.22 is available

## Files & Locations

### Unraid Paths
- **Project**: /mnt/user/appdata/ai/ollama-luxembourgish
- **Models**: /mnt/user/appdata/ai/ollama-luxembourgish/models
- **Config**: /mnt/user/appdata/ai/ollama-luxembourgish/modelfile

### Local Development
- **Project**: L:\Projects\ollama-luxembourgish
- **Docker Compose**: L:\Projects\ollama-luxembourgish\docker-compose.yml
- **Modelfile**: L:\Projects\ollama-luxembourgish\modelfile
- **README**: L:\Projects\ollama-luxembourgish\README.md

## Next Steps

### Improve Luxembourgish Responses
1. Fine-tune LLaMAX3-8B with Luxembourgish data
2. Collect Luxembourgish conversation data
3. Use reinforcement learning for language preference

### Integration Ideas
1. Connect to Home Assistant voice pipeline
2. Integrate with Fish-Speech TTS for audio output
3. Build Luxembourgish chatbot interface
4. Create translation service

## Technical Specifications

- **Base Model**: LLaMA 3 8B
- **Adaptation**: LLaMAX3 multilingual continued pre-training
- **Quantization**: GGUF format
- **Precision**: FP16/INT8 (auto-selected)
- **Framework**: Ollama
- **Container**: Docker with NVIDIA GPU support

## Resources

- **Model**: https://huggingface.co/LLaMAX/LLaMAX3-8B
- **Ollama**: https://ollama.com/mannix/llamax3-8b-alpaca
- **Research**: Text Generation Models for Luxembourgish
- **Documentation**: /mnt/user/appdata/ai/ollama-luxembourgish/README.md

---

**Deployed**: 2026-01-20
**Model**: LLaMAX3-8B-Alpaca (8B)
**Status**: ✅ RUNNING
**IP**: 192.168.106.22:11434
**Language**: Luxembourgish (best-effort)
