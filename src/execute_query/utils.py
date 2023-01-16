from sqlalchemy import null
from sqlalchemy.sql import text
import logging
from typing import Any
from sqlalchemy.engine import Engine
from fastapi.responses import HTMLResponse
import pandas as pd


error_logger = logging.getLogger('error_logger')


def execute_query_commit(db_engine, raw_query: str, **kwargs) -> None:
    try:
        raw_query = text(raw_query)
        with db_engine.begin() as conn:
            conn.execute(raw_query, **kwargs)
    except Exception as e:
        error_logger.error(
            f"Raw commit failed: query {raw_query}: error: {e}", exc_info=True)


# type: ignore
def execute_raw_query(db_engine, raw_query: str, **kwargs) -> list[tuple[Any, ...]]:
    try:
        query = text(raw_query)
        rr = db_engine.execute(query, **kwargs).fetchall()
        res = [tuple(i) for i in rr]
        return res
    except Exception as e:
        error_logger.error(
            f"Raw query failed: query {raw_query}: error: {e}", exc_info=True)


def block_acc(uid: int, reason: str, conn: Engine):
    """
        Block user permanently from SSS Market
        (Cant unblock automatically, only do through Backend Database)
    """
    content_block_reason="Tài khoản của bạn đang bị tạm khóa do phát hiện có hoạt động bất thường liên quan tới chính sách của SSSMarket. Nếu bạn cảm thấy đây là một sự nhầm lẫn, vui lòng liên hệ fanpage của SSSMarket facebook.com/sssmarketvn để được trợ giúp."
    sql = """
    update account_user au
    set private_metadata = private_metadata || '{"detail_block_reason": "%s", "block_reason":"%s"}' #- '{ban_until_reason}',
        is_blocked = true,
        ban_until_date = null
    where id = %d
    and (au.is_blocked is null or au.is_blocked=false)
    """ % (reason,content_block_reason ,uid)
    execute_query_commit(conn, sql)


def ban_shop_period(uid: int, reason: str, conn: Engine, interval: str = "30 days"):
    sql = """
    update account_user
    set private_metadata = private_metadata || '{"ban_until_reason": "%s"}',
        ban_until_date = now() + interval '%s'::interval
    where id = %d
    -- and ban_until_date is null
    """ % (reason, interval, uid)
    execute_query_commit(conn, sql)


def limit_shop_period(uid: int, reason: str, conn: Engine, interval: str = "30 days"):
    sql = """
    update account_user
    set private_metadata = private_metadata || '{"limited_until_reason": "%s"}',
        limited_until_date = now() + interval '%s'::interval
    where id = %d 
    and (limited_until_date is null or limited_until_date < now())
    -- and limited_until_date is null
    """ % (reason, interval, uid)
    execute_query_commit(conn, sql)


def unblock_acc(uid: int, conn: Engine):
    """
        Block user permanently from SSS Market
        (Cant unblock automatically, only do through Backend Database)
    """
    sql = """
    update account_user au
    set private_metadata = private_metadata #- '{block_reason}' #- '{ban_until_reason}'  #- '{detail_block_reason}',
        is_blocked = false,
        ban_until_date = null
    where id = %d
    and (au.is_blocked=true)
    """ % (uid)
    execute_query_commit(conn, sql)


def get_sql(uid: int, account_level_id: str):
    if account_level_id == '6':
        sql = '''
    update account_user 
    set account_level_id = %d
    where id = %d
    ''' % (int(account_level_id), uid)
    elif account_level_id == 'NULL':
        sql = '''
        update account_user 
        set is_business_acc = False, account_level_id = null, subscription_until = null
        where id = %d
        ''' % (uid)
    else:
        sql = '''
        update account_user 
        set is_business_acc = True, account_level_id = %d, subscription_until = now(), limited_until_date = null
        where id = %d
        ''' % (int(account_level_id), uid)
    return sql


def unban_shop_period(uid: int, conn: Engine):
    sql = """
    update account_user
    set private_metadata = private_metadata #- '{ban_until_reason}',
        ban_until_date = null
    where id = %d
    """ % (uid)
    execute_query_commit(conn, sql)


def unlimit_shop_period(uid: int, conn: Engine):
    sql = """
    update account_user
    set private_metadata = private_metadata #- '{limited_until_reason}',

        limited_until_date = null
    where id = %d
    and (limited_until_date is not null)
    """ % (uid)
    execute_query_commit(conn, sql)


def get_sql(uid: int, account_level_id: str):
    if account_level_id == '6':
        sql = '''
    update account_user 
    set account_level_id = %d
    where id = %d
    ''' % (int(account_level_id), uid)
    elif account_level_id == 'NULL':
        sql = '''
        update account_user 
        set is_business_acc = False, account_level_id = null, subscription_until = null
        where id = %d
        ''' % (uid)
    else:
        sql = '''
        update account_user 
        set is_business_acc = True, account_level_id = %d, subscription_until = now(), limited_until_date = null
        where id = %d
        ''' % (int(account_level_id), uid)
    return sql


def get_userid(sss_id: str, conn: Engine):
    query = """
    select id
    from account_user
    where sss_id = '%s'
    """ % (sss_id)
    return execute_raw_query(conn, query)


def html_response_from_dict(dictionary: dict):
    df = pd.DataFrame(data=dictionary.items(), columns=['Content', 'Reason'])
    html_content = df.to_html()

    return html_content


def html_response_str(titile: str, body: str):
    html_content = """
    <html>
        <head>
            <title>%s</title>
        </head>
        <body>
            <h1>%s</h1>
        </body>
    </html>
    """ % (titile, body)

    return html_content


def set_voucher(conn: Engine, user_id, value, limit, name='Freeship %sK', code='freeship%K', dur='1 month'):
    if name == 'Freeship %sK':
        name = name % (value)
        code = code % (value)
    sql = '''
    insert into discount_voucher (type, name, code, usage_limit, used, start_date, end_date, apply_once_per_order, apply_once_per_customer, max_discount_value, discount_value_type, discount_value, currency, min_spent_amount, buyer_ids, seller_ids, visible, provider)
    values ('entire_order', '%s', '%s', %d, 0, current_date, current_date + interval '%s', false, true, NULL, \'fixed\', %d, \'VND\', 0, \'{}\', \'{%s}\', true, 'system')    
    ''' % (name, code, limit, dur, value * 1000, user_id)

    execute_query_commit(conn, sql)


def update_voucher(conn: Engine, limit, value, code='freeship%K', dur='1 month', user_id=''):
    sql = '''
    update discount_voucher
    set usage_limit = %d, used = 0, start_date = current_date, end_date = current_date + interval '%s', discount_value_type = 'fixed', max_discount_value = NULL, discount_value = %s, seller_ids = '{%s}'
    where code = '%s'
    ''' % (limit, dur, value * 1000, user_id, code)

    execute_query_commit(conn, sql)


def is_new_check(sss_id: str, conn: Engine):
    query = """
    select subscription_until
    from account_user
    where sss_id = '%s'
    """ % (sss_id)
    subscription_until_value = execute_raw_query(conn, query)
    if subscription_until_value[0][0] == null:
        return True
    else:
        return False
