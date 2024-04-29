import random

from repository.proxy_repository import ProxyRepository


class ProxyService:
    def __init__(self):
        self.proxy_repository = ProxyRepository()
        self.proxy_list = self.proxy_repository.list(
            fields=['ip_address', 'password', 'port', 'username'], filter_args=None
        )

    def generate_playwright_proxy_params(self):
        proxy = random.choice(self.proxy_list)
        return {
            "server": f"{proxy.ip_address}:{proxy.port}",
            "username": proxy.ip_address,
            "password": proxy.password
        }
