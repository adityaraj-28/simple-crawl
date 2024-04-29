from playwright.sync_api import sync_playwright

from service.proxy_service import ProxyService


class Crawler:
    def __init__(self):
        self.proxy_service = ProxyService()

    def crawl(self, url):
        with sync_playwright() as p:
            browser = p.chromium.launch(proxy=self.proxy_service.generate_playwright_proxy_params())
            page = browser.new_page()
            page.goto(url)
            print(page.content())
            browser.close()


if __name__ == '__main__':
    Crawler().crawl("http://playwright.dev")

