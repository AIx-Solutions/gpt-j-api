import json
from enum import Enum
import requests


class AIxResource:

    __url = "https://api.aixsolutionsgroup.com/v1/"

    class RequestMethod(Enum):
        GET = "GET"
        POST = "POST"
        PATCH = "PATCH"
        DELETE = "DELETE"

    def __init__(self, api_key):
        """
        Initializes the AIx Resource.
        :param api_key: Your API key. To get an API key, go to api.aixsolutionsgroup.com. Sign in / sign up
        and then click on the "API KEYS" tab.
        """
        if type(api_key) is not str:
            raise Exception("API key must be a string.")
        self.api_key = api_key

    def _get_headers(self):
        """
        Get the headers with the appropriate authentication parameters
        :return: The headers
        """
        return {
            'APIKey': self.api_key
        }

    def _request(self, payload, endpoint, request_method, files=None, headers=None):
        """
        Makes a POST request.
        :param payload: the payload containing the parameters
        :param endpoint: the desired endpoint
        :param request_method: the method (e.g. POST, GET, PATCH, DELETE)
        :param files: files to send. only used when changing a profile image
        :param headers: headers for the request. only specified when changing a profile image
        :return:
        """
        if headers is None:
            headers = self._get_headers()

        if files is None:
            r = requests.request(
                request_method.value,
                url=self.__url + endpoint,
                data=json.dumps(payload),
                headers=headers
            )
        else:
            r = requests.request(
                request_method.value,
                url=self.__url + endpoint,
                data=payload,
                files=files,
                headers=headers
            )
        try:
            json_content = json.loads(r.content)
        except json.decoder.JSONDecodeError:
            return r
        return json_content

    def compose(
        self,
        prompt: str,
        response_length: int = 64,
        temperature: float = 0.7,
        top_p: float = 1.0,
        stop_sequence: str = str()
    ):
        """
        Sends a prompt to be completed by the GPT engine.

        :param prompt: A string that prompts the AI. The AI will complete it.
        :param response_length: Valid values 64 to 2048. The maximum number of tokens to generate. Requests can use up
        to 2048 tokens shared between prompt and completion. (One token is roughly 4 characters for normal English
        text.)
        :param temperature: Valid values 0.00 to 1.00. Controls randomness. Lowering results in less random completions.
        As the temperature approaches zero, the model will become deterministic and repetitive.
        :param top_p: Valid values 0.00 to 1.00. Controls diversity via nucleus sampling: 0.5 means half of all
        likelihood-weighted options are considered.
        :param stop_sequence: A sequence where the API will stop generating further tokens. The returned text will not
        contain the stop sequence.
        :return:
            :compute_time: The time taken to compute the response
            :model: GPT-J-6B (Will vary in the future when we add more NLP models)
            :text: The response by the AI
            :prompt: The value you provided
            :token_max_length: The value you provided
            :temperature: The value you provided
            :top_p: The value you provided
            :stop_sequence: The value you provided

        """
        assert type(response_length) is int
        assert type(temperature) is float
        assert type(top_p) is float
        assert type(prompt) is str
        assert type(stop_sequence) is str

        return self._request(
            payload={
                "prompt": prompt,
                "response_length": response_length,
                "temperature": temperature,
                "top_p": top_p,
                "stop_sequence": stop_sequence
            },
            endpoint="compose",
            request_method=self.RequestMethod.POST
        )
