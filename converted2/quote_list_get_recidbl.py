#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import L_quote

t_quote_data, T_quote = create_model("T_quote", {"artnr":int, "lief_nr":int, "docu_nr":string, "from_date":date, "to_date":date})

def quote_list_get_recidbl(t_quote_data:[T_quote]):

    prepare_cache ([L_quote])

    quote_recid = 0
    msg_result = ""
    l_quote = None

    t_quote = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal quote_recid, msg_result, l_quote


        nonlocal t_quote

        return {"quote_recid": quote_recid, "msg_result": msg_result}

    t_quote = query(t_quote_data, first=True)

    if not t_quote:
        msg_result = "No record available"

        return generate_output()

    l_quote = get_cache (L_quote, {"artnr": [(eq, t_quote.artnr)],"lief_nr": [(eq, t_quote.lief_nr)],"docu_nr": [(eq, t_quote.docu_nr)],"from_date": [(eq, t_quote.from_date)],"to_date": [(eq, t_quote.to_date)]})

    if not l_quote:
        msg_result = "No record available"

        return generate_output()
    quote_recid = l_quote._recid

    return generate_output()