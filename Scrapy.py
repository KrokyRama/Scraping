import scrapy
from selenium import webdriver
from scrapy.selector import Selector
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

class GameSpider(scrapy.Spider):
    name = 'game_spider'
    start_urls = ['https://bit.ly/scrapingtry']

    def __init__(self):
        self.driver = webdriver.ChromiumEdge()
        self.wait = WebDriverWait(self.driver, 10)

    def parse(self, response):
        self.driver.get(response.url)

        while True:
            # Tunggu hingga elemen game muncul
            self.wait.until(EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, 'span.psw-t-body.psw-c-t-1.psw-t-truncate-2.psw-m-b-2')))
            sel = Selector(text=self.driver.page_source)

            for game in sel.css('span.psw-t-body.psw-c-t-1.psw-t-truncate-2.psw-m-b-2'):
                yield {
                    'title': game.css('::text').get(),
                    'price': sel.css('span.psw-m-r-3::text').get().replace('\xa0', ' '),
                }

            try:
                next_button = self.wait.until(EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, 'button[data-qa="ems-sdk-grid#ems-sdk-top-paginator-root#next"]')))
                self.driver.execute_script("arguments[0].scrollIntoView();", next_button)
                self.driver.execute_script("arguments[0].click();", next_button)

                # Tunggu hingga halaman selesai dimuat
                self.wait.until(EC.staleness_of(next_button))
            except:
                break

