# encoding=utf-8
import urllib.parse
from asyncio import gather, run
from typing import Optional

from httpx import AsyncClient
from unidecode import unidecode

from .clean_response import CleanResponse
from .logger import Logger
from .settings import LOG_LVL

logger = Logger(LOG_LVL)


class AsyncProductRequests:

    AMAZON = "https://www.amazon.com.br/s?k={search}"
    MERCADO_LIVRE = "https://lista.mercadolivre.com.br/{search}"
    KABUM = "https://www.kabum.com.br/busca?query={search}"
    MAGAZINE = "https://www.magazineluiza.com.br/busca/{search}/"

    cleaned_response = {}

    @staticmethod
    def uri_encode(search: str, space_enconde: Optional[str] = "+"):
        return unidecode(search.replace(" ", space_enconde).lower())

    @staticmethod
    def get_default_domain(url):
        return (
            urllib.parse.urlparse(url)
            .hostname.replace("www.", "")
            .replace(".com.br", "")
            .replace(".com", "")
            .replace("lista.", "")
        )

    def __encoding_uri(self, s, url):
        if "mercadolivre" in url:
            return url.format(search=self.uri_encode(s, space_enconde="-"))
        return url.format(search=self.uri_encode(s))

    def get_list_urls(self, search):
        return list(
            map(
                lambda u: self.__encoding_uri(search, u),
                [link for link in self.__get_links_list()],
            )
        )

    def __get_links_list(self):
        return [
            getattr(self, const)
            for const in dir(self)
            if not callable(getattr(self, const)) and const == const.upper()
        ]

    def __init__(self, product: Optional[str] = None):
        if product:
            try:
                response_values = run(self.__scrapy(product))[0]
                self.cleaned_response = self.clean_response(response_values)
            except Exception as e:
                logger.log(e, lvl=logger.ERROR)

    async def get_response(self, search):
        urls = self.get_list_urls(search)
        values = []
        for link in urls:
            async with AsyncClient() as client:
                response = await client.get(
                    link,
                    timeout=None,
                    headers={
                        "Accept": "*/*",
                        "User-Agent": "Thunder Client (https://www.thunderclient.io)",
                    },
                )
                domain = self.get_default_domain(link)
                if response.is_error or response.is_redirect:
                    logger.log(
                        f"{domain} response code {response.status_code}",
                        lvl=logger.WARNING,
                    )
                values.append(
                    {f"{domain}": response}
                    if response.is_success
                    else {
                        f"{domain}": {
                            "Error": {
                                "code": response.status_code,
                                "message": response.reason_phrase,
                                "redirect_link": str(response.next_request.url)
                                if response.is_redirect
                                else None,
                            }
                        }
                    }
                )
        return values

    async def __scrapy(self, search):
        return await gather(self.get_response(search))

    def scrapy(self, search):
        return run(self.__scrapy(search))[0]

    def clean_response(self, response_values):
        cleaner = CleanResponse()
        return cleaner.clean_response(response_values)
