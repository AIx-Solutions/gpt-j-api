from aix.resource import AIxResource


class Examples:
    __resource = None

    def __init__(self, resource):
        """
        Initializes an instance of Examples. You can try the different examples in this class.
        To do so, initialize the class and then call one of the functions.
        :param resource: an instance of AIxResource
        """
        assert type(resource) == AIxResource
        self.__resource = resource

    def simple_prompt_completion_example(self):
        """
        Sends a simple push notification.
        :return: the result of the call to push
        """
        response = self.__resource.compose(
            "Hello!"
        )
        print(response)
        return response


if __name__ == "__main__":
    # Try an example...
    # Get your API Key at apps.aixsolutionsgroup.com
    api_key = "INSERT_YOUR_API_KEY_HERE"
    aix_resource = AIxResource(api_key)

    try:
        assert api_key != "INSERT_YOUR_API_KEY_HERE"
    except AssertionError:
        raise(Exception("Enter your API key! You can get one for FREE at apps.aixsolutionsgroup.com."))

    example_instance = Examples(aix_resource)

    prompt_completion = example_instance.simple_prompt_completion_example()
    gpt_response = str(prompt_completion.get('data', dict()).get('text'))

    print("-" * 250)

    print("Simple prompt completion example result: " + gpt_response)
    print("If there was no response, try again!")
    print("Keep running this and get a different result because the temperature is greater than 0.0.")

    print("-" * 250)

    # To see documentation, run:
    help(AIxResource)
