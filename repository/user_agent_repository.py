class UserAgentRepository:
    def __init__(self):
        self.user_agent_file_path = 'settings/user-agent.txt'
        self.user_agent_list = self.__load()

    def __load(self):
        user_agents = []
        for line in open(self.user_agent_file_path):
            if len(line) == 0:
                continue
            if line[-1] == '\n':
                line = line[:-1]
            user_agents.append(line)
        return user_agents

    def get_user_agent_list(self):
        return self.user_agent_list
