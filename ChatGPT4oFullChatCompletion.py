import azure.functions as func
from openai import AzureOpenAI
import json
import logging

full_chat_completion_blueprint = func.Blueprint()

@full_chat_completion_blueprint.route(route="ChatGPT4oFullChatCompletion")
def ChatGPT4oFUllChatCompletion(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('HTTP trigger for Full Chat Completion processed a request.')

    req_body = req.get_json()
    messages = req_body.get('messages')

    print("messages: ", messages)

    if messages:
        client = AzureOpenAI(
            api_key = "51d81d5599c64e03bd24323dfe69b1c8",  
            api_version = "2024-02-01",
            azure_endpoint = "https://smc-openai-eastus2.openai.azure.com/"
        )

        response = client.chat.completions.create(
            model="smc-gpt-4o",
            messages=messages
        )

        response_object = {
            "message_content": response.choices[0].message.content
        }

        return func.HttpResponse(body=json.dumps(response_object), status_code=200, mimetype="application/json")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass messages in the request body for a correct response.",
             status_code=200
        )