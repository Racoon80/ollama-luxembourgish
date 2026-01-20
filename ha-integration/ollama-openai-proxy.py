#!/usr/bin/env python3
"""
OpenAI-compatible API proxy for Ollama Luxembourgish
Allows Home Assistant to use Ollama as a conversation agent
"""

from flask import Flask, request, jsonify, Response
import requests
import json
import time
from datetime import datetime

app = Flask(__name__)

# Configuration
OLLAMA_URL = "http://192.168.106.22:11434"
OLLAMA_MODEL = "lux-assistant"
API_KEY = "sk-lux-homeassistant"

def validate_api_key():
    """Validate API key from request"""
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return False
    token = auth_header.replace('Bearer ', '')
    return token == API_KEY

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy"}), 200

@app.route('/v1/models', methods=['GET'])
def list_models():
    """List available models (OpenAI format)"""
    return jsonify({
        "object": "list",
        "data": [
            {
                "id": "lux-assistant",
                "object": "model",
                "created": int(time.time()),
                "owned_by": "ollama",
                "permission": [],
                "root": "lux-assistant",
                "parent": None
            }
        ]
    })

@app.route('/v1/chat/completions', methods=['POST'])
def chat_completions():
    """OpenAI-compatible chat completions endpoint"""

    # Validate API key
    if not validate_api_key():
        return jsonify({"error": "Unauthorized"}), 401

    data = request.json
    messages = data.get('messages', [])
    stream = data.get('stream', False)
    temperature = data.get('temperature', 0.7)
    max_tokens = data.get('max_tokens', 2000)

    # Convert OpenAI messages to Ollama prompt
    prompt = ""
    for msg in messages:
        role = msg.get('role', '')
        content = msg.get('content', '')

        if role == 'system':
            prompt += f"System: {content}\n\n"
        elif role == 'user':
            prompt += f"User: {content}\n\n"
        elif role == 'assistant':
            prompt += f"Assistant: {content}\n\n"

    prompt += "Assistant: "

    # Call Ollama API
    ollama_request = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": stream,
        "options": {
            "temperature": temperature,
            "num_predict": max_tokens
        }
    }

    if stream:
        return stream_response(ollama_request)
    else:
        return non_stream_response(ollama_request)

def non_stream_response(ollama_request):
    """Handle non-streaming response"""
    try:
        response = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json=ollama_request,
            timeout=60
        )

        if response.status_code != 200:
            return jsonify({"error": "Ollama request failed"}), 500

        ollama_response = response.json()
        assistant_message = ollama_response.get('response', '')

        # Convert to OpenAI format
        openai_response = {
            "id": f"chatcmpl-{int(time.time())}",
            "object": "chat.completion",
            "created": int(time.time()),
            "model": "lux-assistant",
            "choices": [
                {
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": assistant_message
                    },
                    "finish_reason": "stop"
                }
            ],
            "usage": {
                "prompt_tokens": 0,
                "completion_tokens": 0,
                "total_tokens": 0
            }
        }

        return jsonify(openai_response)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

def stream_response(ollama_request):
    """Handle streaming response"""
    def generate():
        try:
            response = requests.post(
                f"{OLLAMA_URL}/api/generate",
                json=ollama_request,
                stream=True,
                timeout=120
            )

            for line in response.iter_lines():
                if line:
                    ollama_chunk = json.loads(line)
                    content = ollama_chunk.get('response', '')

                    if content:
                        # Convert to OpenAI streaming format
                        openai_chunk = {
                            "id": f"chatcmpl-{int(time.time())}",
                            "object": "chat.completion.chunk",
                            "created": int(time.time()),
                            "model": "lux-assistant",
                            "choices": [
                                {
                                    "index": 0,
                                    "delta": {
                                        "role": "assistant",
                                        "content": content
                                    },
                                    "finish_reason": None
                                }
                            ]
                        }

                        yield f"data: {json.dumps(openai_chunk)}\n\n"

                    # Check if done
                    if ollama_chunk.get('done', False):
                        # Send final chunk
                        final_chunk = {
                            "id": f"chatcmpl-{int(time.time())}",
                            "object": "chat.completion.chunk",
                            "created": int(time.time()),
                            "model": "lux-assistant",
                            "choices": [
                                {
                                    "index": 0,
                                    "delta": {},
                                    "finish_reason": "stop"
                                }
                            ]
                        }
                        yield f"data: {json.dumps(final_chunk)}\n\n"
                        yield "data: [DONE]\n\n"

        except Exception as e:
            error_chunk = {
                "error": {
                    "message": str(e),
                    "type": "server_error"
                }
            }
            yield f"data: {json.dumps(error_chunk)}\n\n"

    return Response(generate(), mimetype='text/event-stream')

@app.route('/v1/completions', methods=['POST'])
def completions():
    """OpenAI-compatible completions endpoint (legacy)"""

    # Validate API key
    if not validate_api_key():
        return jsonify({"error": "Unauthorized"}), 401

    data = request.json
    prompt = data.get('prompt', '')
    temperature = data.get('temperature', 0.7)
    max_tokens = data.get('max_tokens', 2000)

    ollama_request = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": temperature,
            "num_predict": max_tokens
        }
    }

    try:
        response = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json=ollama_request,
            timeout=60
        )

        ollama_response = response.json()
        text = ollama_response.get('response', '')

        openai_response = {
            "id": f"cmpl-{int(time.time())}",
            "object": "text_completion",
            "created": int(time.time()),
            "model": "lux-assistant",
            "choices": [
                {
                    "text": text,
                    "index": 0,
                    "logprobs": None,
                    "finish_reason": "stop"
                }
            ],
            "usage": {
                "prompt_tokens": 0,
                "completion_tokens": 0,
                "total_tokens": 0
            }
        }

        return jsonify(openai_response)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("Starting Ollama-OpenAI Proxy for Home Assistant")
    print(f"Ollama: {OLLAMA_URL}")
    print(f"Model: {OLLAMA_MODEL}")
    print(f"API Key: {API_KEY}")
    print("Listening on 0.0.0.0:8000")
    app.run(host='0.0.0.0', port=8000, debug=False)
