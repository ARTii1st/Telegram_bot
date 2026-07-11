import httpx

class Model:
    def __init__(self,name_model):
        self.name_model  = name_model
        self.url = "http://localhost:11434/api/generate"

    async def model_ask(self,text):
        data = {
            "model": self.name_model,
            "prompt": text,
            "stream": False
        }

        async with httpx.AsyncClient(timeout=100) as cl:
            res = await  cl.post(self.url, json=data)

        to_json = res.json()

        return to_json["response"]
