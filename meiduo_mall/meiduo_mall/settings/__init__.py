import pymysql
from .develop import LOGGER_NAME
from .develop import DEFAULT_CACHE_ALIAS
from .develop import SESSION_CACHE_ALIAS
from .develop import VERIFY_CODE_CACHE_ALIAS

pymysql.install_as_MySQLdb()
