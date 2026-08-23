import os
import asyncio
import tempfile
from typing import Optional

# Thai Neural Voices
VOICE_FEMALE = "th-TH-PremwadeeNeural"
VOICE_MALE = "th-TH-NiwatNeural"

async def synthesize_thai_audio(text: str, voice: str = VOICE_FEMALE) -> Optional[bytes]:
    """Synthesize natural Thai speech into MP3 bytes using edge-tts."""
    try:
        import edge_tts
        communicate = edge_tts.Communicate(text, voice, rate="+5%")
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp:
            tmp_path = tmp.name
        
        await communicate.save(tmp_path)
        
        with open(tmp_path, "rb") as f:
            audio_bytes = f.read()
            
        try:
            os.remove(tmp_path)
        except Exception:
            pass
            
        return audio_bytes
    except Exception as e:
        print(f"[TTS Error] {e}")
        return None
