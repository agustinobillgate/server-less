# using conversion tools version: 1.0.0.119
"""_yusufwijasena_07/11/2025

    Ticket ID: F6D79E
        _remark_:   - fix python indentation
                    - import from function_py
                    - fix closing bracet on timedelta(days=1)
"""
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, Reslin_queasy, Res_line

del_list_data, Del_list = create_model(
    "Del_list",
    {
        "recid_reslin": int,
        "resnr": int,
        "reslinnr": int,
        "date1": date,
        "date2": date,
        "ankunft": date,
        "abreise": date
    })


def delete_reslin_queasy1_webbl(case_type: int, int1: int, char1: string, date1: date, del_list_data: list[Del_list]):

    prepare_cache([Htparam, Reslin_queasy, Res_line])

    success_flag = False
    user_init = ""
    loopdate: date = None
    bill_date: date = None
    htparam = reslin_queasy = res_line = None

    del_list = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, user_init, loopdate, bill_date, htparam, reslin_queasy, res_line
        nonlocal case_type, int1, char1, date1
        nonlocal del_list

        return {
            "success_flag": success_flag
        }

    def res_changes():
        nonlocal success_flag, user_init, loopdate, bill_date, htparam, reslin_queasy, res_line
        nonlocal case_type, int1, char1, date1
        nonlocal del_list

        cid = ""
        cdate = " "
        rqy = None
        Rqy = create_buffer("Rqy", Reslin_queasy)

        if not res_line:
            return

        if res_line.active_flag == 2:
            return

        if res_line.changed is not None:
            cid = res_line.changed_id
            cdate = to_string(res_line.changed)

        rqy = Reslin_queasy()
        db_session.add(rqy)

        rqy.key = "ResChanges"
        rqy.resnr = res_line.resnr
        rqy.reslinnr = res_line.reslinnr
        rqy.date2 = get_current_date()
        rqy.number2 = get_current_time_in_seconds()

        rqy.char3 = to_string(res_line.ankunft) + ";" + \
            to_string(res_line.ankunft) + ";" + \
            to_string(res_line.abreise) + ";" + \
            to_string(res_line.abreise) + ";" + \
            to_string(res_line.zimmeranz) + ";" + \
            to_string(res_line.zimmeranz) + ";" + \
            to_string(res_line.erwachs) + ";" + \
            to_string(res_line.erwachs) + ";" + \
            to_string(res_line.kind1) + ";" + \
            to_string(res_line.kind1) + ";" + \
            to_string(res_line.gratis) + ";" + \
            to_string(res_line.gratis) + ";" + \
            to_string(res_line.zikatnr) + ";" + \
            to_string(res_line.zikatnr) + ";" + \
            to_string(res_line.zinr) + ";" + \
            to_string(res_line.zinr) + ";" + \
            to_string(res_line.arrangement) + ";" + \
            to_string(res_line.arrangement) + ";" + \
            to_string(res_line.zipreis) + ";" + \
            to_string(res_line.zipreis) + ";" + \
            to_string(cid) + ";" + \
            to_string(user_init) + ";" + \
            to_string(cdate, "x(8)") + ";" + \
            to_string(get_current_date()) + ";" + \
            to_string("Fixrate DELETED:") + ";" + \
            to_string(reslin_queasy.date1) + "-" + to_string(reslin_queasy.deci1) + ";" + \
            to_string("YES", "x(3)") + ";" + \
            to_string("YES", "x(3)") + ";"

    htparam = get_cache(
        Htparam, {"paramnr": [(eq, 87)]})

    if htparam:
        bill_date = htparam.fdate

    if case_type == 1:
        user_init = char1

        for del_list in query(del_list_data):
            reslin_queasy = get_cache(
                Reslin_queasy, {"_recid": [(eq, del_list.recid_reslin)]})

            if reslin_queasy:
                res_line = get_cache(
                    Res_line, {"resnr": [(eq, reslin_queasy.resnr)], "reslinnr": [(eq, reslin_queasy.reslinnr)]})
                res_changes()
                db_session.delete(reslin_queasy)
                success_flag = True
    elif case_type == 2:
        user_init = char1

        for del_list in query(del_list_data):
            for loopdate in date_range(del_list.date1, del_list.date2):
                # if loopdate < bill_date:
                #     pass
                # else:
                if loopdate > bill_date:
                    reslin_queasy = get_cache(
                        Reslin_queasy, {"key": [(eq, "arrangement")], "resnr": [(eq, del_list.resnr)], "reslinnr": [(eq, del_list.reslinnr)], "date1": [(le, loopdate)], "date2": [(ge, loopdate)]})

                    if reslin_queasy:
                        res_line = get_cache(
                            Res_line, {"resnr": [(eq, reslin_queasy.resnr)], "reslinnr": [(eq, reslin_queasy.reslinnr)]})
                        res_changes()
                        db_session.delete(reslin_queasy)
                        success_flag = True

        del_list = query(del_list_data, first=True)

        if del_list:
            reslin_queasy = db_session.query(Reslin_queasy).filter(
                (Reslin_queasy.key == "arrangement") & (Reslin_queasy.resnr == del_list.resnr) & (Reslin_queasy.reslinnr == del_list.reslinnr) & ((Reslin_queasy.date1 < del_list.ankunft) | (Reslin_queasy.date1 > del_list.abreise))).first()

            if reslin_queasy:
                for reslin_queasy in db_session.query(Reslin_queasy).filter(
                        (Reslin_queasy.key == "arrangement") & (Reslin_queasy.resnr == del_list.resnr) & (Reslin_queasy.reslinnr == del_list.reslinnr) & ((Reslin_queasy.date1 < del_list.ankunft) | (Reslin_queasy.date1 > del_list.abreise))).order_by(Reslin_queasy._recid).all():
                    db_session.delete(reslin_queasy)

    return generate_output()
