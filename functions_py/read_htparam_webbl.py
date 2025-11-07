# using conversion tools version: 1.0.0.119
"""_yusufwijasena_03/11/2025

    Ticket ID: F6D79E
        _remark_:   - fix var declaration
                    - fix python indentation
                    - add import from function_py
                    - changed string to str
                    - use f"string"
                    - fix string.lower() 
"""
from functions.additional_functions import *
from decimal import Decimal
from sqlalchemy import func
from models import Htparam

payload_list_data, Payload_list = create_model(
    "Payload_list",
    {
        "htp_bezeich": str
    })


def read_htparam_webbl(case_type: int, paramno: int, paramgrup: int, payload_list_data: Payload_list):
    t_htparam_data = []
    paramnr_email: List[int] = [1379, 2404, 2405, 2406, 2407, 2408]
    count_i: int = 0
    desc_bez = ""
    htparam = None

    t_htparam = hide_emailparam = payload_list = None

    t_htparam_data, T_htparam = create_model_like(Htparam)
    hide_emailparam_data, Hide_emailparam = create_model(
        "Hide_emailparam",
        {
            "paramnr": int
        })

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_htparam_data, paramnr_email, count_i, desc_bez, htparam
        nonlocal case_type, paramno, paramgrup
        nonlocal t_htparam, hide_emailparam, payload_list
        nonlocal t_htparam_data, hide_emailparam_data

        return {
            "t-htparam": t_htparam_data
        }

    payload_list = query(payload_list_data, first=True)

    if payload_list:
        # desc_bez = "*" + payload_list.htp_bezeich + "*"
        desc_bez = f"*{payload_list.htp_bezeich}*"
    for count_i in range(1, 6 + 1):
        hide_emailparam = Hide_emailparam()
        hide_emailparam_data.append(hide_emailparam)

        hide_emailparam.paramnr = paramnr_email[count_i - 1]

    if case_type == 1:
        htparam = get_cache(
            Htparam, {"paramnr": [(eq, paramno)]})

        if htparam:
            t_htparam = T_htparam()
            t_htparam_data.append(t_htparam)

            buffer_copy(htparam, t_htparam)
    elif case_type == 2:
        for htparam in db_session.query(Htparam).filter(
                (Htparam.paramgruppe == paramgrup)).order_by(Htparam._recid).all():
            t_htparam = T_htparam()
            t_htparam_data.append(t_htparam)

            buffer_copy(htparam, t_htparam)
    elif case_type == 3:
        htparam = get_cache(
            Htparam, {"paramnr": [(eq, paramno)], "paramgruppe": [(eq, paramgrup)]})

        if htparam:
            t_htparam = T_htparam()
            t_htparam_data.append(t_htparam)

            buffer_copy(htparam, t_htparam)
    elif case_type == 4:
        for htparam in db_session.query(Htparam).filter(
                (Htparam.paramnr <= paramno)).order_by(Htparam._recid).all():
            t_htparam = T_htparam()
            t_htparam_data.append(t_htparam)

            buffer_copy(htparam, t_htparam)
    elif case_type == 5:
        for htparam in db_session.query(Htparam).filter(
                (Htparam.paramnr >= 1) & (Htparam.paramnr <= 16)).order_by(Htparam._recid).all():
            t_htparam = T_htparam()
            t_htparam_data.append(t_htparam)

            buffer_copy(htparam, t_htparam)
    elif case_type == 6:
        for htparam in db_session.query(Htparam).filter(
                (Htparam.paramgruppe == paramgrup)).order_by(Htparam._recid).all():
            t_htparam = T_htparam()
            t_htparam_data.append(t_htparam)

            buffer_copy(htparam, t_htparam)

            hide_emailparam = query(hide_emailparam_data, filters=(
                lambda hide_emailparam: hide_emailparam.paramnr == t_htparam.paramnr), first=True)

            if hide_emailparam:
                if trim(t_htparam.fchar) != "" and t_htparam.fchar != None:
                    t_htparam.flogical = True
                else:
                    t_htparam.flogical = False
                t_htparam.fchar = ""
    elif case_type == 7:
        htparam = get_cache(
            Htparam, {"paramnr": [(eq, paramno)], "bezeichnung": [(ne, "not used")]})

        if htparam:
            t_htparam = T_htparam()
            t_htparam_data.append(t_htparam)

            buffer_copy(htparam, t_htparam)

            hide_emailparam = query(hide_emailparam_data, filters=(
                lambda hide_emailparam: hide_emailparam.paramnr == t_htparam.paramnr), first=True)

            if hide_emailparam:
                if trim(t_htparam.fchar) != "" and t_htparam.fchar != None:
                    t_htparam.flogical = True
                else:
                    t_htparam.flogical = False
                t_htparam.fchar = ""
    elif case_type == 8:
        for htparam in db_session.query(Htparam).filter(
                (matches(Htparam.bezeichnung, desc_bez)) & (Htparam.bezeichnung != "not used")).order_by(Htparam._recid).all():
            t_htparam = T_htparam()
            t_htparam_data.append(t_htparam)

            buffer_copy(htparam, t_htparam)

            hide_emailparam = query(hide_emailparam_data, filters=(
                lambda hide_emailparam: hide_emailparam.paramnr == t_htparam.paramnr), first=True)

            if hide_emailparam:
                if trim(t_htparam.fchar) != "" and t_htparam.fchar != None:
                    t_htparam.flogical = True
                else:
                    t_htparam.flogical = False
                t_htparam.fchar = ""

    return generate_output()
