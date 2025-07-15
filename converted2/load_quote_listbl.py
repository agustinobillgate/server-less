#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Htparam, Waehrung, L_quote

t_quote_data, T_quote = create_model("T_quote", {"artnr":int, "lief_nr":int, "supname":string, "artname":string, "devunit":string, "content":Decimal, "unitprice":Decimal, "curr":string, "from_date":date, "to_date":date, "remark":string, "filname":string, "activeflag":bool, "docu_nr":string, "minqty":Decimal, "delivday":int, "disc":Decimal, "avl":bool}, {"activeflag": True, "avl": True})

def load_quote_listbl(user_init:string, t_quote_data:[T_quote]):

    prepare_cache ([Htparam, Waehrung, L_quote])

    local_curr:string = ""
    htparam = waehrung = l_quote = None

    t_quote = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal local_curr, htparam, waehrung, l_quote
        nonlocal user_init


        nonlocal t_quote

        return {}

    htparam = get_cache (Htparam, {"paramnr": [(eq, 152)]})

    waehrung = get_cache (Waehrung, {"wabkurz": [(eq, htparam.fchar)]})

    if waehrung:
        local_curr = waehrung.wabkurz

    for t_quote in query(t_quote_data):

        l_quote = get_cache (L_quote, {"artnr": [(eq, t_quote.artnr)],"lief_nr": [(eq, t_quote.lief_nr)],"from_date": [(eq, t_quote.from_date)],"to_date": [(eq, t_quote.to_date)]})

        if not l_quote:
            l_quote = L_quote()
            db_session.add(l_quote)

            buffer_copy(t_quote, l_quote)
            l_quote.createid = user_init
            l_quote.createdate = date_mdy(get_month(get_current_date()) , get_day(get_current_date()) , get_year(get_current_date()))
            l_quote.createtime = get_current_time_in_seconds()
            l_quote.reserve_char[0] = local_curr
            l_quote.reserve_deci[0] = t_quote.minqty
            l_quote.reserve_deci[1] = t_quote.disc
            l_quote.reserve_logic[0] = not t_quote.avl
            l_quote.reserve_int[0] = t_quote.delivDay
            l_quote.reserve_int[4] = 1


    return generate_output()