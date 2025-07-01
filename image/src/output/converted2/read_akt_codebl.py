#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Akt_code

def read_akt_codebl(case_type:int, bezeich:string, aktionscode:int):
    t_akt_code_list = []
    akt_code = None

    t_akt_code = None

    t_akt_code_list, T_akt_code = create_model_like(Akt_code)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_akt_code_list, akt_code
        nonlocal case_type, bezeich, aktionscode


        nonlocal t_akt_code
        nonlocal t_akt_code_list

        return {"t-akt-code": t_akt_code_list}

    if case_type == 1:

        for akt_code in db_session.query(Akt_code).filter(
                 (Akt_code.aktiongrup == 1)).order_by(Akt_code._recid).all():
            t_akt_code = T_akt_code()
            t_akt_code_list.append(t_akt_code)

            buffer_copy(akt_code, t_akt_code)
    elif case_type == 2:

        akt_code = get_cache (Akt_code, {"aktiongrup": [(eq, 1)],"bezeich": [(eq, bezeich)]})

        if akt_code:
            t_akt_code = T_akt_code()
            t_akt_code_list.append(t_akt_code)

            buffer_copy(akt_code, t_akt_code)
    elif case_type == 3:

        akt_code = get_cache (Akt_code, {"aktionscode": [(eq, aktionscode)]})

        if akt_code:
            t_akt_code = T_akt_code()
            t_akt_code_list.append(t_akt_code)

            buffer_copy(akt_code, t_akt_code)
    elif case_type == 4:

        akt_code = get_cache (Akt_code, {"aktiongrup": [(eq, 1)],"aktionscode": [(eq, aktionscode)]})

        if akt_code:
            t_akt_code = T_akt_code()
            t_akt_code_list.append(t_akt_code)

            buffer_copy(akt_code, t_akt_code)
    elif case_type == 5:

        for akt_code in db_session.query(Akt_code).order_by(Akt_code._recid).all():
            t_akt_code = T_akt_code()
            t_akt_code_list.append(t_akt_code)

            buffer_copy(akt_code, t_akt_code)
    elif case_type == 6:

        akt_code = get_cache (Akt_code, {"aktiongrup": [(eq, 2)],"aktionscode": [(eq, 1)]})

        if akt_code:
            t_akt_code = T_akt_code()
            t_akt_code_list.append(t_akt_code)

            buffer_copy(akt_code, t_akt_code)
    elif case_type == 7:

        akt_code = get_cache (Akt_code, {"aktiongrup": [(eq, aktionscode)],"bezeich": [(eq, bezeich)]})

        if akt_code:
            t_akt_code = T_akt_code()
            t_akt_code_list.append(t_akt_code)

            buffer_copy(akt_code, t_akt_code)
    elif case_type == 8:

        akt_code = get_cache (Akt_code, {"aktiongrup": [(eq, 4)],"aktionscode": [(eq, aktionscode)]})

        if akt_code:
            t_akt_code = T_akt_code()
            t_akt_code_list.append(t_akt_code)

            buffer_copy(akt_code, t_akt_code)
    elif case_type == 9:

        for akt_code in db_session.query(Akt_code).filter(
                 (Akt_code.aktiongrup == aktionscode)).order_by(Akt_code._recid).all():
            t_akt_code = T_akt_code()
            t_akt_code_list.append(t_akt_code)

            buffer_copy(akt_code, t_akt_code)

    return generate_output()