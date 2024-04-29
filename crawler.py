from playwright.sync_api import sync_playwright

from constants import Status
from service.crawl_status_service import CrawlStatusService
from service.proxy_service import ProxyService
from utils import calculate_md5_hash


class Crawler:
    def __init__(self):
        self.proxy_service = ProxyService()
        self.crawl_status_service = CrawlStatusService()

    def crawl(self, domain, url):
        url_md5 = calculate_md5_hash(url)
        self.crawl_status_service.create_crawl_status_entry(domain=domain, url=url, level=0, url_md5=url_md5)
        with sync_playwright() as p:
            browser = p.chromium.launch(
                proxy=self.proxy_service.generate_playwright_proxy_params(),
                headless=True,
                timeout=20*1000,
                args=[
                    "--disable-web-security",
                    "--ignore-https-error",
                    "-ignore-certificate-errors"
                ]
            )
            page = browser.new_page()
            response = page.goto(url)
            redirect_urls = self.__build_redirect_url(response)
            browser.close()
        self.crawl_status_service.update_crawl_details(
            url_md5=url_md5, status=Status.CRAWL_SUCCESS, redirection_chain=redirect_urls
        )

    @staticmethod
    def __build_redirect_url(response):
        redirect_urls = [response.url]
        redirected = response.request.redirected_from
        while redirected is not None:
            redirect_urls.append(redirected.url)
            redirected = redirected.redirected_from
        return redirect_urls


if __name__ == '__main__':
    Crawler().crawl("128technology.com", "http://128technology.com/")

