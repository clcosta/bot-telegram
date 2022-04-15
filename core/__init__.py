# encoding=utf-8
from .clean_response import CleanResponse
from .handler import Handlers
from .logger import Logger
from .scrapper import AsyncProductRequests
from .settings import BOT_TOKEN


class VeiaDasCompra(Handlers):
    """'Veia das Compras'.
    Um BOT de telegram criado baseado em uma API interna que faz uma busca de 4 sites diferentes: Amazon, Mercado Livre, Kabum e Magazine Luiza.
    Este Bot tem 2 comandos principais:

    "/p :PRODUTO:" -> return: Messagem no chat
    "/produto :PRODUTO:" -> return: Arquivos Json no chat

    Commands Examples:
    "/start"
    "/help"
    "/p Iphoone 13"
    "/produto Iphoone 13"
    """

    ...
