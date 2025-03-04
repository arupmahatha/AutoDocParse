import base64
import requests

api_key = ""

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def analyze_image(image_path):

    base64_image = encode_image(image_path)
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Strictly output only and only a list of 'key'-'value' pairs from the document. the output should have double quotes in the keys and values. If document is an invoice, keys are: Customer name, Destination name, Invoice number, Date, Payment terms, Currency, Due date, items, quantities, unit price, total amount. If it is a Bill of Lading list, keys are: Bill number, port for release, shipper details, consignee details, port of loading, port of discharge, final destination, voyage number, and container number. If it is a permit, keys are: permit number, importer details, exporter details, arrival date, departure date, and license number. If it is a packaging list, keys are: item and no of cartons. For a key for which no value is extracted - return value as NA. If the type of document is not invoice/packaging list/bill of lading/permit, assume it is an invoice."
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 500
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
   
    return response.json()['choices'][0]['message']['content']