# encoding=utf-8
import itertools
import json
import tempfile

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext, CallbackQueryHandler, CommandHandler, Updater

from .logger import Logger
from .scrapper import AsyncProductRequests
from .settings import BOT_TOKEN, LOG_LVL


class Handlers:

    """Classe responsável pelos "comandos" do BOT, é aqui que foi construida toda a estrutura do chat com o BOT, além de ser a classe responsável pela chamada do BOT.
    Dentro de outra estutura também tem a função responsável por iniciar o BOT [main()].
    """

    logger = Logger(LOG_LVL)

    def start_handler(self, update: Update, context: CallbackContext) -> None:
        self.logger.log(f"Start acionado!")
        update.message.reply_text(
            "Use /p <PRODUTO> para receber as informações dos 10 primeiros resultados correspondente a seu produto;\
                \n\n Use /produto <PRODUTO> para receber os arquivos json como resultado;"
        )

    def help_handler(self, update: Update, context: CallbackContext) -> None:
        self.logger.log(f"Help acionado!")
        update.message.reply_text(
            "Este BOT é a VeiaDasCompra. Uma API totalmente gratuita que realizar o scrapping de informações publicas de sites como:\
            \namazon.com.br\nkabum.com.br\nmercadolivre.com\nmagazineluiza.com.br\
            \n O principal objetivo da API é facilitar a busca por produtos e comparação de preços, sendo levado em consideração que a\
             API pode devolver os preços no formato de JSON"
        )

    def create_temp_files(self, values_dict):
        self.logger.log(f"Tempfile Criado")
        tempdir = tempfile.mkdtemp(prefix="arquivotemp")
        files = []
        for k in values_dict.keys():
            filename = k + ".json"
            file_path = tempdir + f"\\{filename}"
            files.append((file_path, filename))
            self.logger.log(f"Arquivo criado em {file_path}")
            with open(file_path, "w", encoding="utf-8") as f:
                self.logger.log(f"Conteudo escrito em {filename}")
                f.write(json.dumps(values_dict.get(k)))
        return files

    def _get_produto(self, update, context):
        produto = " ".join(context.args)
        if produto:
            return produto
        msg = "É necessário passar um produto para pesquisa logo após o comando!"
        update.message.reply_text(msg)
        self.logger.log(msg, Logger.WARNING)
        raise ValueError(msg)

    def produto_json_handler(self, update: Update, context: CallbackContext) -> None:
        produto = self._get_produto(update, context)
        update.message.reply_text(f"Pesquisando por {produto} ...")
        self.logger.log(f"Iniciando o scrapping do {produto}")
        p = AsyncProductRequests(produto)
        values = p.cleaned_response
        _files = self.create_temp_files(values)
        for path, name in _files:
            update.message.reply_document(document=open(path, "rb"), filename=name)
        update.message.reply_text("Finalizado!")
        self.logger.log("Finalizado com sucesso!")

    def produtos_handler(self, update: Update, context: CallbackContext) -> None:
        produto = self._get_produto(update, context)
        update.message.reply_text(f"Pesquisando por {produto} ...")
        self.logger.log(f"Iniciando o scrapping do {produto}")
        p = AsyncProductRequests(produto)
        values = p.cleaned_response
        dict_sliced = self.slicing_dict(values)
        self.logger.log("Finalizado o scrapping com sucesso!")
        self.select_product(products=dict_sliced, update=update, context=context)

    def slicing_dict(self, dict_values: dict, n: int = 10) -> dict:
        slice_dict = {}
        for k in dict_values:
            if "Error" in dict_values[k].keys():
                slice_dict[k] = dict_values[k]
                continue
            slice_dict[k] = dict(itertools.islice(dict_values[k].items(), n))
        return slice_dict

    def select_product(self, products, update: Update, context: CallbackContext):
        self.answers = {
            "AMAZON_CALLBACK": products.get("amazon"),
            "MERCADOLIVRE_CALLBACK": products.get("mercadolivre"),
            "KABUM_CALLBACK": products.get("kabum"),
            "MAGAZINE_CALLBACK": products.get("magazineluiza"),
        }
        keyboard = [
            [
                InlineKeyboardButton("Amazon", callback_data="AMAZON_CALLBACK"),
                InlineKeyboardButton(
                    "Mercado Livre", callback_data="MERCADOLIVRE_CALLBACK"
                ),
            ],
            [
                InlineKeyboardButton("Kabum", callback_data="KABUM_CALLBACK"),
                InlineKeyboardButton(
                    "Magazine Luiza", callback_data="MAGAZINE_CALLBACK"
                ),
            ],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(
            "Selecione o site que você deseja ver os resultados",
            reply_markup=reply_markup,
        )
        self.logger.log("Aguardando resposta do Usuário...")

    def get_domain_response_handler(self, update: Update, context: CallbackContext):
        query = update.callback_query

        if not hasattr(self, "answers"):
            msg = "Algo deu errado, infelizmente não consegui pegar os produtos!"
            query.edit_message_text(text=msg)
            self.logger.log(msg, lvl=self.logger.CRITICAL)
            raise ValueError(msg)

        context.bot.send_message(
            chat_id=query.message.chat.id,
            text=self.__formated_answers(self.answers[query.data]),
        )

    def __formated_answers(self, data):
        result = ""
        for p in data:
            if p == "Error":
                return f"{p}: {data[p]['code']}({data[p]['message']}) - Redirect to :{data[p]['redirect_link']}"
            result += (
                f"Produto: {p}"
                + f"\nPreço: {data[p]['price']}"
                + f"\nLink: {data[p]['url']}\n\n"
            )
        return result

    def main(self):
        updater = Updater(BOT_TOKEN)
        dispatcher = updater.dispatcher
        dispatcher.add_handler(CommandHandler("start", self.start_handler))
        dispatcher.add_handler(CommandHandler("help", self.help_handler))
        dispatcher.add_handler(CommandHandler("p", self.produtos_handler))
        dispatcher.add_handler(CommandHandler("produto", self.produto_json_handler))
        dispatcher.add_handler(CallbackQueryHandler(self.get_domain_response_handler))

        self.logger.log("Bot Iniciado com sucesso!", Logger.INFO)
        updater.start_polling()

        updater.idle()
