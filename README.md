---
title: MediFlow Clinic TTS
emoji: 🔊
colorFrom: pink
colorTo: blue
sdk: docker
app_port: 8000
---

# MediFlow Clinic TTS Backend

FastAPI service that generates English clinic queue announcements with Microsoft Edge TTS and returns MP3 bytes directly. It does not save, open, or launch generated audio files.

## Local setup (PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Health check:

```powershell
Invoke-RestMethod http://localhost:8000/health
```

Generate and save a manual test response:

```powershell
$body = @{ text = 'Queue number UM zero zero one, patient Sean, please proceed to General Clinic.' } | ConvertTo-Json
Invoke-WebRequest -Method Post -Uri http://localhost:8000/tts -ContentType 'application/json' -Body $body -OutFile test_call.mp3
```

## Compare voices

Generate the same sentence with Sonia, Jenny, and Ava:

```powershell
python scripts/compare_voices.py
```

Listen to the MP3 files inside `voice_samples/` and compare clarity, calmness, naturalness, and pace. The default is `en-GB-SoniaNeural` at `-8%`, selected as the conservative calm-clinic default. Change only `EDGE_TTS_VOICE` in `.env` to switch voices.

`pip-system-certs` keeps TLS verification enabled while allowing Edge TTS to use the operating system trust store. This is especially useful on managed Windows networks with an organization-issued root certificate.

## Configuration

Copy `.env.example` to `.env`. `TTS_CORS_ORIGINS` accepts comma-separated release origins. Localhost and `127.0.0.1` HTTP origins are allowed automatically for development.

## Deployment

Build and deploy the included Dockerfile to a Python-capable HTTPS host. Configure the environment variables from `.env.example`, set `PORT` as required by the host, and add the released Flutter web origin to `TTS_CORS_ORIGINS`.

The Flutter release must be built with the deployed HTTPS URL:

```powershell
flutter build apk --dart-define=TTS_BACKEND_URL=https://your-deployed-tts-backend.com
```
