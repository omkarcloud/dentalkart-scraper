from botasaurus import *
from botasaurus.cache import DontCache
from urls import urls
import random

def write_output(data, result):
    bt.write_json(bt.remove_nones(result), 'products')
    bt.write_csv(bt.remove_nones(result), 'products')

def clean_url(url):
    return url.replace("https://www.dentalkart.com/", "").replace("/", '-')
                
@browser(parallel=bt.calc_max_parallel_browsers, headless=True, cache=True, output=write_output, reuse_driver=True)
def scrape_products_task(driver: AntiDetectDriver, url):
    driver.get(url)

    save_name = clean_url(url)

    title_selector = 'h1.productInformation_heading__28NgY'
    price_selector = 'span.productInformation_discounted_price__nmQpW > span:nth-child(2)'

    title = driver.get_element_or_none_by_selector(title_selector, bt.Wait.SHORT)
    price = driver.get_element_or_none_by_selector(price_selector, bt.Wait.SHORT) if title else None

    if price is None or title is None:
        driver.save_screenshot(save_name)
        return DontCache(None)
    else:
        new_data = {"title": title.text, "price": price.text, "url": url}
        print(new_data)
        return new_data

if __name__ == "__main__":
    my_urls = [url['loc'] for url in urls]
    random.shuffle(my_urls) # Shuffle the urls to make it look more natural and not automated.
    # Initiate the web scraping task
    scrape_products_task(my_urls)
