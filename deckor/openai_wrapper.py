import logging
from openai import OpenAI
import os
import json
import time

logger = logging.getLogger(__name__)

def pretty_print(messages):
    print("# Messages")
    for m in messages:
        print(f"{m.role}: {m.content[0].text.value}")
    print()

def show_json(obj):
    # Convert JSON string to a Python dictionary
    parsed_json = json.loads(obj.model_dump_json())
    # Pretty print the JSON
    print(json.dumps(parsed_json, indent=4, sort_keys=True))


class OpenAIClient:
    OPENAI_API_KEY = "OPENAI_API_KEY"

    def __init__(self):
        self.client = OpenAI(api_key=self.api_key)

    @property
    def api_key(self):
        # This will return the API key from environment or None if not found
        return os.environ.get(self.OPENAI_API_KEY)
    
    @property
    def assistants(self, limit="20", order="desc"):
        my_assistants = self.client.beta.assistants.list(
            order=order,
            limit=limit,
        )
        return my_assistants.data
    
    @api_key.setter
    def api_key(self, value):
        # Set the API key both as an environment variable and in the client
        os.environ[self.OPENAI_API_KEY] = value
        self.client = OpenAI(api_key=value)

    def find_openai_assistant_id(self, target_name):
        for assistant in self.assistants:
            if assistant.name == target_name:
                return assistant.id
        return None

    def create_openai_assistant(self, assistant_name, instructions, tools, model):
        assistant = self.client.beta.assistants.create(
            name=assistant_name,
            instructions=instructions,
            tools=[{"type": tools}],
            model=model,
        )
        return show_json(assistant)

    def get_response(self, thread):
        return self.client.beta.threads.messages.list(thread_id=thread.id, order="asc")

class OpenAIAssistant:
    def __init__(self, client, assistant_id):
        """
        Initialize the Assistant instance.

        :param client: An instance of OpenAIClient.
        :param assistant_id: The unique identifier for the assistant.
        """
        self.client = client.client  # Assuming 'client' is an instance of some wrapper around OpenAI's API.
        self.assistant_id = assistant_id

    def create_thread(self):
        """
        Creates a new conversation thread.

        :return: The thread object.
        """
        return self.client.beta.threads.create()

    def submit_message(self, thread, user_message):
        """
        Submits a message to a specific thread and initiates processing by the assistant.

        :param thread: The thread object.
        :param user_message: The message text to send.
        :return: The run object, representing the processing task.
        """
        self.client.beta.threads.messages.create(
            thread_id=thread.id, role="user", content=user_message
        )
        return self.client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=self.assistant_id,
        )

    def wait_on_run(self, run, thread):
        """
        Waits for a submitted run to complete.

        :param run: The run object to wait on.
        :param thread: The thread object associated with the run.
        :return: The completed run object.
        """
        while run.status in ["queued", "in_progress"]:
            run = self.client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id,
            )
            time.sleep(0.5)
        return run

    def get_thread_responses(self, thread):
        """
        Retrieves all messages from a thread.

        :param thread: The thread object to retrieve messages from.
        :return: A list of messages.
        """
        return self.client.beta.threads.messages.list(thread_id=thread.id, order="asc")
    
    def upload_file(self, path):
        with open(path, "rb") as file:
            uploaded_file = self.client.files.create(
                file=file,
                purpose="assistants",
            )
        assistant = self.client.beta.assistants.update(
            assistant_id=self.assistant_id,
            tools=[{"type": "retrieval"}],
            file_ids=[uploaded_file.id],
        )
        return show_json(assistant)

    def update(self, **kwargs):
        """
        Update assistant settings.

        :param kwargs: Keyword arguments for settings to update.
        """
        # This method would use the client to update assistant settings based on provided arguments
        # Example implementation could be self.client.update_assistant(self.assistant_id, **kwargs)
        pass

    def retrieve_history(self):
        """
        Retrieve the message history with this assistant.

        :return: A list of message exchanges with the assistant.
        """
        # Assuming there's a method in OpenAIClient to get the message history
        history = self.client.get_response(self.assistant_id)
        return history