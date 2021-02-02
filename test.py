import requests
import urllib.parse

req = requests.get("http://127.0.0.1:5000/" + urllib.parse.quote("""{
    "string": "I am a string",
    "int": 100,
    "bool true": true,
    "bool false": false,
    "list": [
        true,
        false,
        "string",
        "10"
    ],
    "dict":
    {
        "list_in_dict": [
            10
        ],
        "string": "strin,g",
    }
}"""))
print(req.text)