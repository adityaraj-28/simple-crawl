import structlog
from playwright.sync_api import sync_playwright

from constants import Status
from service.crawl_status_service import CrawlStatusService
from service.proxy_service import ProxyService
from service.user_agent_service import UserAgentService
from utils import calculate_md5_hash
from utils.s3_client import S3Client


class Crawler:
    def __init__(self):
        self.proxy_service = ProxyService()
        self.crawl_status_service = CrawlStatusService()
        self.s3_client = S3Client()
        self.logger = structlog.getLogger(__name__)
        self.user_agent_service = UserAgentService()

    def crawl(self, domain, url):
        url_md5 = calculate_md5_hash(url)
        self.crawl_status_service.create_crawl_status_entry(domain=domain, url=url, level=0, url_md5=url_md5)
        proxy_args = self.proxy_service.generate_playwright_proxy_params()
        with sync_playwright() as p:
            browser = p.chromium.launch(
                proxy=proxy_args,
                headless=True,
                timeout=20 * 1000,
                args=[
                    "--disable-web-security",
                    "--ignore-https-error",
                    "-ignore-certificate-errors"
                ]
            )
            page = browser.new_page()
            user_agent = self.user_agent_service.get_random_user_agent()
            page.set_extra_http_headers({'User-Agent': user_agent})
            response = page.goto(url=url, wait_until='domcontentloaded', timeout=30*1000)
            self.logger.info(f"url: {url}, proxy-used: {proxy_args['server']}, user_agent: {user_agent}, response code: {response.status}")
            if response.status // 100 == 2 or response.status // 100 == 3:
                redirect_urls = self.__build_redirect_url(response)
                s3_uri = self.s3_client.upload_to_s3(domain=domain, data=response.text())
                self.crawl_status_service.update_crawl_details(url_md5=url_md5, update_args={
                    'redirection_chain': str(redirect_urls),
                    'status': Status.FILE_UPLOADED.value,
                    's3_uri': s3_uri,
                    'error_message': None
                })
            else:
                self.crawl_status_service.update_crawl_details(url_md5=url_md5, update_args={
                    'status': Status.CRAWL_FAILED.value,
                    'error_message': f'StatusCode:{response.status}'
                })
            browser.close()

    @staticmethod
    def __build_redirect_url(response):
        redirect_urls = [response.url]
        redirected = response.request.redirected_from
        while redirected is not None:
            redirect_urls.append(redirected.url)
            redirected = redirected.redirected_from
        return redirect_urls


if __name__ == '__main__':
    Crawler().crawl("theuselessweb.com", "https://theuselessweb.com")
