from bose import *
from .urls import urls
import random

random.seed(9)
my_urls = [url['loc'] for url in urls]
random.shuffle(my_urls)

class Task(BaseTask):

    def run(self, driver: BoseDriver, data):
        result = []

        for url in my_urls:
            print(url)
            driver.get(url)

            save_name = url.replace(
                "https://www.dentalkart.com/", "").replace("/", '-')

            title = driver.get_element_or_none_by_selector(
                'h1.productInformation_heading__28NgY', Wait.SHORT)
            if title is not None:
                price = driver.get_element_or_none_by_selector(
                    'span.productInformation_discounted_price__nmQpW > span:nth-child(2)', Wait.SHORT)
            else:
                price = None

            if price is None or title is None:
                driver.save_screenshot(save_name)
            else:
                new_data = {"title": title.text,
                            "price": price.text, "url": url}
                
                print(new_data)
     
                result += [new_data]
                Output.write_json(result, 'data')

        return result
