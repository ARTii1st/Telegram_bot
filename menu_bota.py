from telegram import  InlineKeyboardMarkup, InlineKeyboardButton
class Menu:
    def __init__(self):

        self.models = [
            ["Qwen3 Coder", "huihui_ai/qwen3-coder-abliterated:latest"]]

        self.menu = {
            "model":[
                (name, f"model:{i}")
                for i, (name, _) in enumerate(self.models)],
            "settings": [
                ("Лимит запроса", "menu:border"),
                ("Креативность", "menu:creati"),
                ("Назад", "menu:model"),],
            "border":[
                ("Безлимитный", "border:-1"),
                ("Средний | 700", "border:700"),
                ("Короткий | 150", "border:150"),
                ("Назад", "menu:settings"),],
            "creati":[
                ("Лаконичный", "creati:0.2"),
                ("Вдумчивый", "creati:0.7"),
                ("Хаотичный", "creati:1.5"),
                ("Назад", "menu:settings"),]}

        self.handlers = {
            "model": self.select_model,
            "menu": self.open_menu,
            "border": self.select,
            "creati": self.select}


    def keyboard(self, name):
        return InlineKeyboardMarkup([[InlineKeyboardButton(text, callback_data=data)]
            for text, data in self.menu[name]])


    async def callback(self, update, context):
        call = update.callback_query
        await call.answer()
        prefix, value = call.data.split(":", 1)
        await self.handlers[prefix](call,context.user_data["settings"],value)

    def text(self, settings):
        return (
            f"Параметры выбранной модели:\n"
            f"<i>————————————————</i>\n"
            f"Модель <b>{settings['model'][0]}</b>\n"
            f"Креативность <b>{settings['creati']}</b>\n"
            f"Лимит запроса <b>{settings['border']}</b>\n"
            f"<i>————————————————</i>\n"
            f"<b>Можете написать запрос ✍️</b>"
        )


    async def show(self, target, settings):
        await target.edit_text(self.text(settings),
            reply_markup=self.keyboard("settings"),
            parse_mode="HTML")#под будущие функцию менюшки что бы показать красивое
                                # сообщение сеттинга с шмль(мб сюда вставлю еще одну что бы не дублировать один раз код)


    async def select_model(self, call, settings, value):
        settings["model"] = self.models[int(value)]

        await call.edit_message_text(
            self.text(settings),
            reply_markup=self.keyboard("settings"),
            parse_mode="HTML"
        )

    async def open_menu(self, call,settings,value):
        await call.edit_message_reply_markup(reply_markup=self.keyboard(value))

    async def select(self, call, settings, value):
        key = call.data.split(":")[0]

        settings[key] = float(value) if "." in value else int(value)

        await call.edit_message_text(
            self.text(settings),
            reply_markup=self.keyboard("settings"),
            parse_mode="HTML"
        )