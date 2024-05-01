import structlog
from sqlalchemy import create_engine, func, null, or_
from sqlalchemy.orm import sessionmaker

from constants import MysqlDBNames
from settings.global_settings import BROAD_CRAWL_MYSQL_ENGINE, BROAD_CRAWL_CENTRAL_MYSQL_ENGINE, LABS_CORE_MYSQL_ENGINE


class Mysql:
    def __init__(self):
        self.broad_crawl_engine = create_engine(BROAD_CRAWL_MYSQL_ENGINE, echo=False)
        self.broad_crawl_central_engine = create_engine(BROAD_CRAWL_CENTRAL_MYSQL_ENGINE, echo=False)
        self.labs_core_engine = create_engine(LABS_CORE_MYSQL_ENGINE, echo=True)
        self.logger = structlog.getLogger(__name__)

    def get(self, model_cls, db_name, filter_args=None, negative_filters=None, selected_columns=None,
            or_filter_args=None, case_insensitive_columns=[], **kwargs):
        try:
            engine = self.__get_engine(db_name)
            Session = sessionmaker(bind=engine)
            with Session() as session:
                query = session.query(model_cls)

                if selected_columns and isinstance(selected_columns, list):
                    # Select specific columns if provided
                    selected_column_entities = []
                    for col in selected_columns:
                        attr = getattr(model_cls, col)
                        if col in case_insensitive_columns:
                            attr = func.lower(attr)
                        selected_column_entities.append(attr)
                    query = query.with_entities(*selected_column_entities)

                if filter_args is not None:
                    for field, value in filter_args.items():
                        attr = getattr(model_cls, field)
                        if field in case_insensitive_columns:
                            attr = func.lower(attr)
                        if isinstance(value, list):
                            query = query.filter(attr.in_(value))
                        else:
                            query = query.filter(attr == value)

                if or_filter_args is not None:
                    or_conditions = []

                    for field, value in or_filter_args.items():
                        attr = getattr(model_cls, field)
                        if field in case_insensitive_columns:
                            attr = func.lower(attr)
                        if isinstance(value, list):
                            or_conditions.append(attr.in_(value))
                        else:
                            or_conditions.append(attr == value)

                    query = query.filter(or_(*or_conditions))

                if negative_filters is not None:
                    for key, value in negative_filters.items():
                        attr = getattr(model_cls, key)
                        if key in case_insensitive_columns:
                            attr = func.lower(attr)
                        if value is None:
                            query = query.filter(attr != null())
                        else:
                            query = query.filter(attr != value)

                if 'order_by' in kwargs:
                    query = query.order_by(kwargs['order_by'])

                if 'limit' in kwargs and kwargs['limit'] is not None:
                    query = query.limit(int(kwargs['limit']))
                if 'offset' in kwargs and kwargs['offset']:
                    query = query.offset(int(kwargs['offset']))

                res_list = query.all()
                session.expunge_all()

                result = []
                if selected_columns and isinstance(selected_columns, list):
                    for res in res_list:
                        cls = model_cls()
                        for index in range(len(selected_columns)):
                            setattr(cls, selected_columns[index], res[index])

                        result.append(cls)
                else:
                    result = res_list
        except Exception as e:
            self.logger.error(f"Error while executing get: {str(e)}")
            raise e
        return result

    def insert(self, model_cls, params, db_name):
        try:
            engine = self.__get_engine(db_name)
            Session = sessionmaker(bind=engine, expire_on_commit=False)
            with Session() as session:
                new_record = model_cls(**params)
                session.add(new_record)
                session.commit()
                session.expunge_all()
                return new_record
        except Exception as e:
            self.logger.error(f"Error while executing insert: {str(e)}")
            raise e

    def update(self, model_cls, filter_args, update_dict, db_name, case_insensitive_columns=[]):
        try:
            engine = self.__get_engine(db_name)
            Session = sessionmaker(bind=engine, expire_on_commit=False)
            with Session() as session:
                query = session.query(model_cls)

                if filter_args is not None:
                    for field, value in filter_args.items():
                        attr = getattr(model_cls, field)
                        if field in case_insensitive_columns:
                            attr = func.lower(attr)
                        if isinstance(value, list):
                            query = query.filter(attr.in_(value))
                        else:
                            query = query.filter(attr == value)

                target_obj = query.first()

                for field, value in update_dict.items():
                    if hasattr(target_obj, field):
                        setattr(target_obj, field, value)
                    else:
                        self.logger.error(f"Field {field} not found in target object")
                session.commit()
                session.expunge_all()
                return target_obj
        except Exception as e:
            self.logger.error(f"Error while executing update: {str(e)}")
            raise e

    def __get_engine(self, db_name):
        if db_name == MysqlDBNames.BROAD_CRAWL_DB:
            return self.broad_crawl_engine
        elif db_name == MysqlDBNames.LABS_CORE_DB:
            return self.labs_core_engine
        elif db_name == MysqlDBNames.BROAD_CRAWL_CENTRAL_DB:
            return self.broad_crawl_central_engine
