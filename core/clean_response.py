# encoding=utf-8
from bs4 import BeautifulSoup
from bs4.element import Tag


class CleanResponse:
    def clean_amazon(self, response):

        AMAZON_LINK = "https://www.amazon.com.br"
        COIN = "R$"

        bs = BeautifulSoup(response.text, "html.parser")
        tag_preco = bs.find_all("span", attrs={"class": "a-price-whole"})
        tag_preco_decimal = bs.find_all("span", attrs={"class": "a-price-fraction"})
        tag_nomes = bs.find_all(
            "span",
            attrs={"class": "a-size-base-plus a-color-base a-text-normal"},
        )
        tag_links = bs.find_all("a", attrs={"class": "a-link-normal s-no-outline"})
        real_links = list(map(lambda x: AMAZON_LINK + x.get("href"), tag_links))
        real_names = list(map(Tag.get_text, tag_nomes))
        temp_prices = list(
            zip(
                list(map(Tag.get_text, tag_preco)),
                list(map(Tag.get_text, tag_preco_decimal)),
            )
        )
        real_prices = list(map(lambda price: COIN + "".join(price), temp_prices))
        price_and_link = list(
            map(
                lambda x: dict(price=x[0], url=x[1]),
                list(zip(real_prices, real_links)),
            )
        )
        dict_products = dict(zip(real_names, price_and_link))
        return dict_products

    def clean_mercado_livre(self, response):
        bs = BeautifulSoup(response.text, "html.parser")
        tag_preco = bs.select(
            "li.ui-search-layout__item > div > div > div > div > div > div > div > div > div > span > span > span.price-tag-fraction"
        )
        tag_links = bs.select("div.ui-search-result__image > a.ui-search-link")
        tag_nomes = bs.select("h2.ui-search-item__title")
        real_prices = list(map(Tag.get_text, tag_preco))
        real_links = list(map(lambda x: x.get("href"), tag_links))
        real_names = list(map(Tag.get_text, tag_nomes))
        price_and_link = list(
            map(
                lambda x: dict(price=x[0], url=x[1]),
                list(zip(real_prices, real_links)),
            )
        )
        dict_products = dict(zip(real_names, price_and_link))
        return dict_products

    def clean_kabum(self, response):

        KABUM_LINK = "https://www.kabum.com.br"

        bs = BeautifulSoup(response.text, "html.parser")
        tag_preco = bs.find_all("span", attrs={"class": "priceCard"})
        tag_nomes = bs.find_all("span", attrs={"class": "nameCard"})
        tag_links = list(
            map(
                lambda x: x.parent,
                bs.find_all("img", attrs={"class": "imageCard"}),
            )
        )
        real_prices = list(
            map(
                lambda x: x.get_text().replace("\xa0", "")
                if x.get_text().replace("\xa0", "") != "R$---"
                else "Sem estoque!",
                tag_preco,
            )
        )
        real_links = list(map(lambda x: KABUM_LINK + x.get("href"), tag_links))
        real_names = list(map(Tag.get_text, tag_nomes))
        price_and_link = list(
            map(
                lambda x: dict(price=x[0], url=x[1]),
                list(zip(real_prices, real_links)),
            )
        )
        dict_products = dict(zip(real_names, price_and_link))
        return dict_products

    def clean_magazine(self, response):

        MAGAZINE_LINK = "https://www.magazineluiza.com.br"

        bs = BeautifulSoup(response.text, "html.parser")
        tag_nomes = bs.find_all("h2", attrs={"data-testid": "product-title"})
        tag_preco = bs.find_all("p", attrs={"data-testid": "price-value"})
        tag_links = bs.find_all("a", attrs={"data-testid": "product-card-container"})
        real_prices = list(
            map(
                lambda x: x.get_text().replace("\xa0", ""),
                tag_preco,
            )
        )
        real_names = list(map(Tag.get_text, tag_nomes))
        real_links = list(map(lambda x: MAGAZINE_LINK + x.get("href"), tag_links))
        price_and_link = list(
            map(
                lambda x: dict(price=x[0], url=x[1]),
                list(zip(real_prices, real_links)),
            )
        )
        dict_products = dict(zip(real_names, price_and_link))
        return dict_products

    def clean_response(self, list_reponses):
        if not isinstance(list_reponses, list):
            raise ValueError("clean_response takes a 'list of dict'")
        cleaned_response = {}
        kwargs = {
            list(item.keys())[0]: list(item.values())[0] for item in list_reponses
        }
        for k in kwargs:
            if isinstance(kwargs.get(k), dict):
                cleaned_response[k] = kwargs.get(k)
                continue
            if k == "amazon":
                cleaned_response[k] = self.clean_amazon(kwargs.get(k))
            elif k == "kabum":
                cleaned_response[k] = self.clean_kabum(kwargs.get(k))
            elif k == "magazineluiza":
                cleaned_response[k] = self.clean_magazine(kwargs.get(k))
            elif k == "mercadolivre":
                cleaned_response[k] = self.clean_mercado_livre(kwargs.get(k))
        return cleaned_response
