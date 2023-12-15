import logging
from logging import LogRecord
import sqlite3

CREATE_SQL = """
CREATE TABLE IF NOT EXISTS LOGS(
    name text,
    msg text,
    args text,
    levelname text,
    levelno integer,
    pathname text,
    filename text,
    module text,
    exc_info text,
    exc_test text,
    stack_info text,
    lineno integer,
    funcName text,
    created real,
    msecs real,
    relativeCreated real,
    thread integer,
    threadName text,
    processName text,
    process integer,
    message text,
    asctime text
)
"""

INSERT_SQL = """
INSERT INTO LOGS(
    name,
    msg,
    args,
    levelname,
    levelno,
    pathname,
    filename,
    module,
    exc_info,
    exc_test,
    stack_info,
    lineno,
    funcName,
    created,
    msecs,
    relativeCreated,
    thread,
    threadName,
    processName,
    process,
    message,
    asctime
) VALUES(
    :name,
    :msg,
    :args,
    :levelname,
    :levelno,
    :pathname,
    :filename,
    :module,
    :exc_info,
    :exc_test,
    :stack_info,
    :lineno,
    :funcName,
    :created,
    :msecs,
    :relativeCreated,
    :thread,
    :threadName,
    :processName,
    :process,
    :message,
    :asctime
)
"""


class SQLiteHandler(logging.Handler):
    """
    custom handler that writes logs to SQLite DB
    """
    def __init__(self, db):
        logging.Handler.__init__(self)
        self.db = db
        with sqlite3.connect(self.db) as con:
            con.execute(CREATE_SQL)
            con.commit()
    
    def emit(self, record: LogRecord):
        with sqlite3.connect(self.db) as con:
            con.execute(
                INSERT_SQL,
                {
                    'name': record.name,
                    'msg': record.msg,
                    'args': str(record.args),
                    'levelname': record.levelname,
                    'levelno': record.levelno,
                    'pathname': record.pathname,
                    'filename': record.filename,
                    'module': record.module,
                    'exc_info': record.exc_info,
                    'exc_test': record.exc_text,
                    'stack_info': record.stack_info,
                    'lineno': record.lineno,
                    'funcName': record.funcName,
                    'created': record.created,
                    'msecs': record.msecs,
                    'relativeCreated': record.relativeCreated,
                    'thread': record.thread,
                    'threadName': record.threadName,
                    'processName': record.processName,
                    'process': record.process,
                    'message': record.message,
                    'asctime': record.asctime
                }
            )
            con.commit()
            


if __name__ == '__main__':
    logger = logging.getLogger('my-logger')
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        '%(asctime)s - [%(levelname)s] - %(name)s - %(message)s',
        datefmt='%m/%d/%Y %I:%M:%S %p'
    )
    # console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    # sqlite handler
    sql_handler = SQLiteHandler('logs.sqlite')
    sql_handler.setLevel(logging.DEBUG)
    logger.addHandler(sql_handler)

    logger.info("hello from logger")
    logger.error("this is an error message")
