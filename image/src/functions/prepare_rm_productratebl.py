from functions.additional_functions import *
import decimal
from models import Bediener, Htparam

def prepare_rm_productratebl(lnl_prog:str, lnl_prog1:str):
    lnl_filepath = ""
    lnl_filepath1 = ""
    price_decimal = 0
    p_547 = 0
    t_bediener_list = []
    bediener = htparam = None

    t_bediener = None

    t_bediener_list, T_bediener = create_model_like(Bediener)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal lnl_filepath, lnl_filepath1, price_decimal, p_547, t_bediener_list, bediener, htparam


        nonlocal t_bediener
        nonlocal t_bediener_list
        return {"lnl_filepath": lnl_filepath, "lnl_filepath1": lnl_filepath1, "price_decimal": price_decimal, "p_547": p_547, "t-bediener": t_bediener_list}

    def fill_salesid():

        nonlocal lnl_filepath, lnl_filepath1, price_decimal, p_547, t_bediener_list, bediener, htparam


        nonlocal t_bediener
        nonlocal t_bediener_list

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 547)).first()

        if htparam.paramnr == 0:

            return
        p_547 = htparam.paramnr

        for bediener in db_session.query(Bediener).filter(
                (Bediener.user_group == htparam.finteger)).all():
            t_bediener = T_bediener()
            t_bediener_list.append(t_bediener)

            buffer_copy(bediener, t_bediener)

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 417)).first()

    if htparam.fchar != "":
        lnl_filepath = htparam.fchar

        if substring(lnl_filepath, len(lnl_filepath) - 1, 1) != "\\":
            lnl_filepath = lnl_filepath + "\\"
        lnl_filepath = lnl_filepath + lnl_prog
        lnl_filepath1 = htparam.fchar

        if substring(lnl_filepath1, len(lnl_filepath1) - 1, 1) != "\\":
            lnl_filepath1 = lnl_filepath1 + "\\"
        lnl_filepath1 = lnl_filepath1 + lnl_prog1

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 491)).first()
    price_decimal = htparam.finteger
    fill_salesid()

    return generate_output()