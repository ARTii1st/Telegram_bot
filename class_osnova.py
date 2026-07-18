import httpx
import whisper
import os
from pypdf import PdfReader
from docx import Document

class Model:

    def __init__(self):
        self.url = "http://localhost:11434/api/generate"
        self.whisper = whisper.load_model("base")
        self.length = 4096
        self.client = httpx.AsyncClient(timeout=100)
        self.reader = {".pdf": self.read_pdf,".docx": self.read_docx,}

    def read_docx(self, path):
        doc = Document(path)

        return "\n".join(p.text[50000] for p in doc.paragraphs)


    def read_pdf(self, path):
        reader = PdfReader(path)
        text = []

        for page in reader.pages:
            t = page.extract_text()
            if t:
                text.append(t)

        return "\n".join(text[:50000])#ограничения

    async def length_message(self,update, text):
        parts = [text[i:i + self.length]
                 for i in range(0, len(text), self.length)]
        for part in parts:
            await update.message.reply_text(part)


    async def model_ask(self,update,text,setting):

        try:
            data = {
                "model": setting["model"][1],
                "prompt": text,
                "stream": False,
                "options":
                {"temperature":setting["creati"],
                "num_predict": setting["border"]}}

            await update.message.reply_text(f"{setting["model"][0]} думает..")
            res = await  self.client.post(self.url, json=data)
            to_json = res.json()

            if len(to_json["response"])  >  self.length :
                    await  self.length_message(update,to_json["response"])
                    return

            await update.message.reply_text(to_json["response"])
            return

        except Exception as ex:
            await update.message.reply_text(f"Что то пошло не так, код ошибки {ex}")


    async def decoder_voice(self,update,voice,setting):
        try:
            result = self.whisper.transcribe(voice)

            await update.message.reply_text("Слушаю ваше аудио..")

            return await self.model_ask(update,result["text"],setting)

        except Exception as ex:
            await update.message.reply_text(f"Что то пошло не так, код ошибки {ex}")

        finally:
            os.remove(voice)



    async def read(self,update, path):
        try:
            ext = os.path.splitext(path)[1].lower()

            await update.message.reply_text(f"Читаю файл📖..")

            if ext in self.reader:
                return self.reader[ext](path)

            with open(path, encoding="utf-8", errors="ignore") as f:
                return f.read()
        finally:
            os.remove(path)