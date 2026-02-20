import os
import time
import threading
from dotenv import load_dotenv

from elevenlabs.client import ElevenLabs
from elevenlabs.conversational_ai.conversation import Conversation
from elevenlabs.conversational_ai.default_audio_interface import DefaultAudioInterface
from elevenlabs.types import ConversationConfig

# ---------------------------
# 1. Load Environment
# ---------------------------

load_dotenv()

AGENT_ID = os.getenv("AGENT_ID")
API_KEY = os.getenv("API_KEY")

print("Agent:", AGENT_ID)
print("API:", API_KEY[:10] + "..." if API_KEY else "Missing")

# ---------------------------
# 2. Assistant Configuration
# ---------------------------

user_name = "Deniz"
schedule = "Work on AI project at 14:00; Gym at 18:00"

prompt = f"You are a helpful personal assistant. The user has the following schedule: {schedule}."
first_message = f"Hello {user_name}, how can I help you today?"

conversation_override = {
    "agent": {
        "prompt": {
            "prompt": prompt,
        },
        "first_message": first_message,
    }
}

config = ConversationConfig(
    conversation_config_override=conversation_override,
    extra_body={},            # SDK hatasını önler
    dynamic_variables={}
)

# ---------------------------
# 3. Callbacks
# ---------------------------

def print_agent_response(response):
    print(f"Agent: {response}")

def print_interrupted_response(original, corrected):
    print(f"Agent interrupted. Corrected: {corrected}")

def print_user_transcript(transcript):
    print(f"User: {transcript}")

# ---------------------------
# 4. ElevenLabs Client
# ---------------------------

client = ElevenLabs(api_key=API_KEY)
print("ElevenLabs connected successfully")

conversation = Conversation(
    client=client,
    agent_id=AGENT_ID,
    config=config,
    requires_auth=True,
    audio_interface=DefaultAudioInterface(),
    callback_agent_response=print_agent_response,
    callback_agent_response_correction=print_interrupted_response,
    callback_user_transcript=print_user_transcript,
)

print("Conversation configured successfully.")
print("Starting conversation... Speak into your microphone.")

# ---------------------------
# 5. Start Session
# ---------------------------

conversation.start_session()