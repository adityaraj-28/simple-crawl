import random

from repository.user_agent_repository import UserAgentRepository
from settings.global_settings import USER_AGENT


class UserAgentService:
    def __init__(self):
        self.default_user_agent = USER_AGENT
        self.user_agent_repository = UserAgentRepository()
        self.user_agent_list = self.user_agent_repository.get_user_agent_list()

    def get_random_user_agent(self, use_default=False):
        if use_default:
            return self.default_user_agent
        return random.choice(self.user_agent_list)
