#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Bediener, Htparam

def prepare_rm_productratebl(lnl_prog:string, lnl_prog1:string):

    prepare_cache ([Htparam])

    lnl_filepath = ""
    lnl_filepath1 = ""
    price_decimal = 0
    p_547 = 0
    t_bediener_data = []
    bediener = htparam = None

    t_bediener = None

    t_bediener_data, T_bediener = create_model_like(Bediener)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal lnl_filepath, lnl_filepath1, price_decimal, p_547, t_bediener_data, bediener, htparam
        nonlocal lnl_prog, lnl_prog1


        nonlocal t_bediener
        nonlocal t_bediener_data

        return {"lnl_filepath": lnl_filepath, "lnl_filepath1": lnl_filepath1, "price_decimal": price_decimal, "p_547": p_547, "t-bediener": t_bediener_data}

    def fill_salesid():

        nonlocal lnl_filepath, lnl_filepath1, price_decimal, p_547, t_bediener_data, bediener, htparam
        nonlocal lnl_prog, lnl_prog1


        nonlocal t_bediener
        nonlocal t_bediener_data

        htparam = get_cache (Htparam, {"paramnr": [(eq, 547)]})

        if htparam.paramnr == 0:

            return
        p_547 = htparam.paramnr

        for bediener in db_session.query(Bediener).filter(
                 (Bediener.flag == 0) & (Bediener.user_group == htparam.finteger)).order_by(Bediener.username).all():
            t_bediener = T_bediener()
            t_bediener_data.append(t_bediener)

            buffer_copy(bediener, t_bediener)


    htparam = get_cache (Htparam, {"paramnr": [(eq, 417)]})

    if htparam.fchar != "":
        lnl_filepath = htparam.fchar

        if substring(lnl_filepath, length(lnl_filepath) - 1, 1) != ("\\").lower() :
            lnl_filepath = lnl_filepath + "\\"
        lnl_filepath = lnl_filepath + lnl_prog
        lnl_filepath1 = htparam.fchar

        if substring(lnl_filepath1, length(lnl_filepath1) - 1, 1) != ("\\").lower() :
            lnl_filepath1 = lnl_filepath1 + "\\"
        lnl_filepath1 = lnl_filepath1 + lnl_prog1

    htparam = get_cache (Htparam, {"paramnr": [(eq, 491)]})
    price_decimal = htparam.finteger
    fill_salesid()

    return generate_output()