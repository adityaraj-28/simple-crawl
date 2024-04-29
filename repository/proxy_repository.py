from constants import MysqlDBNames
from model.proxy import Proxy
from utils.mysql import Mysql


class ProxyRepository:

    def __init(self):
        self.mysql = Mysql()

    def list(self, filter_args, fields):
        if not filter_args:
            filter_args = {}
        case_insensitive_columns = []
        if 'domain' in filter_args:
            case_insensitive_columns.append('domain')
        res = self.mysql.get(
            model_cls=Proxy,
            db_name=MysqlDBNames.LABS_CORE_DB,
            filter_args=filter_args,
            selected_columns=fields,
            case_insensitive_columns=case_insensitive_columns,
            limit=1
        )
        if len(res) > 0:
            return res[0]
        return None
