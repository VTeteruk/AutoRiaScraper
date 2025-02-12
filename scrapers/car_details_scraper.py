from bs4 import BeautifulSoup


class CarDetailsScraper:
    @staticmethod
    def get_car_name(soup: BeautifulSoup) -> str:
        return soup.find("h1", {"class": "head"}).get("title")

    @staticmethod
    def get_car_price(soup: BeautifulSoup) -> str:
        return soup.find("div", {"class": "price_value"}).get_text(strip=True)

    @staticmethod
    def get_car_bidfax_url(soup: BeautifulSoup) -> str | None:
        try:
            return soup.find("a", {"class": "unlink size16"}).get("href")
        except AttributeError:
            return

    @staticmethod
    def get_car_pictures(soup: BeautifulSoup) -> list:
        pictures = soup.find("div", {"photocontainer": "photo"}).find_all("img")
        links = [picture.get("src") for picture in pictures]
        return [link for link in links][:-1]

    def get_car_data(self, soup: BeautifulSoup) -> dict:
        return {
            "name": self.get_car_name(soup),
            "price": self.get_car_price(soup),
            "bidfax_url": self.get_car_bidfax_url(soup),
            "pictures": self.get_car_pictures(soup)
        }
