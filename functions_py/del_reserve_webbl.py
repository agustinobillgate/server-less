# using conversion tools version: 1.0.0.119
"""_yusufwijasena_04/11/2025

    Ticket ID: F6D79E
        _remark_:   - fix var decklaration
                    - fix python indentation
                    - changed string to str
                    - fix string.lower()
"""
#----------------------------------------------------------------
# Rd, 25/11/2025, with_for_update
#----------------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
# from functions.del_reslinebl import del_reslinebl
# from functions.leasing_cancel_rsvbl import leasing_cancel_rsvbl
from functions_py.del_reslinebl import del_reslinebl
from functions_py.leasing_cancel_rsvbl import leasing_cancel_rsvbl
from models import Res_line, Queasy, Bediener, Htparam


def del_reserve_webbl(pvilanguage: int, res_mode: str, resnr: int, user_init: str, cancel_str: str):

    prepare_cache([Queasy])

    msg_str = ""
    del_mainres: bool = False
    lvcarea: str = "del-reserve"
    res_line = queasy = bediener = htparam = None
    rline = bqueasy = None

    Rline = create_buffer("Rline", Res_line)
    Bqueasy = create_buffer("Bqueasy", Queasy)

    db_session = local_storage.db_session
    res_mode = res_mode.strip()
    cancel_str = cancel_str.strip()

    def generate_output():
        nonlocal msg_str, del_mainres, lvcarea, res_line, queasy, bediener, htparam
        nonlocal pvilanguage, res_mode, resnr, user_init, cancel_str
        nonlocal rline, bqueasy
        nonlocal rline, bqueasy

        return {
            "msg_str": msg_str
        }

    bediener = get_cache(Bediener, {"userinit": [(eq, user_init)]})

    htparam = get_cache(Htparam, {"paramnr": [(eq, 87)]})

    if res_mode.lower() == "cancel" or res_mode.lower() == "delete":
        res_line = get_cache(
            Res_line, {"resnr": [(eq, resnr)], "active_flag": [(eq, 0)], "l_zuordnung[2]": [(eq, 0)]})
        while res_line is not None:
            del_mainres, msg_str = get_output(del_reslinebl(
                pvilanguage, res_mode, res_line.resnr, res_line.reslinnr, user_init, cancel_str))

            curr_recid = res_line._recid
            res_line = db_session.query(Res_line).filter(
                (Res_line.resnr == resnr) & (Res_line.active_flag == 0) & (Res_line.l_zuordnung[inc_value(2)] == 0) & (Res_line._recid > curr_recid)).first()

        # bqueasy = get_cache(
        #     Queasy, {"key": [(eq, 329)], "number1": [(eq, resnr)], "logi1": [(eq, False)]})
        bqueasy = db_session.query(Bqueasy).filter(
                 (Bqueasy.key == 329) & (Bqueasy.number1 == resnr) & (Bqueasy.logi1 == False)).with_for_update().first()
        if bqueasy:
            get_output(leasing_cancel_rsvbl(bqueasy._recid, user_init))
            bqueasy.logi1 = True

    return generate_output()
