import azure.functions as func
from openai import AzureOpenAI
import json
import logging

simple_chat_completion_blueprint = func.Blueprint()

@simple_chat_completion_blueprint.route(route="ChatGPT4oSimpleChatCompletion")
def ChatGPT4oSimpleChatCompletion(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('HTTP trigger for Simple Chat Completion processed a request.')

    req_body = req.get_json()
    system_text = req_body.get('system_text')
    user_text = req_body.get('user_text')
    image_url = req_body.get('image_url')

    print("system_text: ", system_text)
    print("user_text: ", user_text)
    print("image_url: ", image_url)

    if system_text and user_text and  image_url:
        client = AzureOpenAI(
            api_key = "51d81d5599c64e03bd24323dfe69b1c8",  
            api_version = "2024-02-01",
            azure_endpoint = "https://smc-openai-eastus2.openai.azure.com/"
        )

        response = client.chat.completions.create(
            model="smc-gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": [
                        {
                            "type": "text",
                            "text": system_text
                        }
                    ]
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": image_url
                            }
                        },
                        {
                            "type": "text",
                            "text": user_text
                        }
                    ]
                }
            ]
        )

        response_object = {
            "message_content": response.choices[0].message.content
        }

        return func.HttpResponse(body=json.dumps(response_object), status_code=200, mimetype="application/json")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass system_text,user_text & image)url  in the request body for a correct response.",
             status_code=200
        )