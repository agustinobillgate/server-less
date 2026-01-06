# using conversion tools version: 1.0.0.119
"""_yusufwijasena_05/01/2025

    remark: - updated from FDL (2C320F)
            - fix python indentation
            - added with_for_update
            - added flag_modified
"""
from functions.additional_functions import *
from decimal import Decimal
from models import Guestbook, Bediener, Res_history, Queasy

from sqlalchemy.orm.attributes import flag_modified

esign_list_data, Esign_list = create_model(
    "Esign_list",
    {
        "sign_nr": int,
        "sign_name": string,
        "sign_img": bytes,
        "sign_use_for": string,
        "sign_position": string,
        "sign_userinit": string,
        "sign_id": int,
        "sign_select": bool,
        "sign_pass": string,
        "sign_pr": bool,
        "sign_po": bool,
        "sign_dml": bool
    })


def esign_setup_2bl(case_type: int, user_init: string, esign_list_data: [Esign_list]):

    prepare_cache([Bediener, Res_history])

    t_error_list_data = []
    booknr: int = 0
    guestbook = bediener = res_history = queasy = None

    esign_list = t_error_list = gbook = None

    t_error_list_data, T_error_list = create_model(
        "T_error_list",
        {
            "error_number": int,
            "error_message": string
        })

    Gbook = create_buffer("Gbook", Guestbook)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_error_list_data, booknr, guestbook, bediener, res_history, queasy
        nonlocal case_type, user_init
        nonlocal gbook
        nonlocal esign_list, t_error_list, gbook
        nonlocal t_error_list_data

        return {
            "esign-list": esign_list_data,
            "t-error-list": t_error_list_data
        }

    t_error_list = T_error_list()
    t_error_list_data.append(t_error_list)

    if case_type == 0:

        for guestbook in db_session.query(Guestbook).filter(
                (Guestbook.gastnr >= -271150) & 
                (Guestbook.gastnr <= -271080)).order_by(Guestbook.reserve_int[inc_value(0)]).all():
            esign_list = Esign_list()
            esign_list_data.append(esign_list)

            esign_list.sign_nr = to_int(entry(0, guestbook.infostr, "|"))
            esign_list.sign_name = entry(1, guestbook.infostr, "|")
            esign_list.sign_img = guestbook.imagefile
            esign_list.sign_use_for = entry(2, guestbook.infostr, "|")
            esign_list.sign_position = entry(3, guestbook.infostr, "|")
            esign_list.sign_userinit = guestbook.userinit
            esign_list.sign_id = guestbook.gastnr
            esign_list.sign_pass = guestbook.reserve_char[0]
            esign_list.sign_pr = guestbook.reserve_logic[0]
            esign_list.sign_po = guestbook.reserve_logic[1]
            esign_list.sign_dml = guestbook.reserve_logic[2]

        bediener = get_cache(Bediener, {"userinit": [(eq, user_init)]})
        res_history = Res_history()
        db_session.add(res_history)

        res_history.nr = bediener.nr
        res_history.datum = get_current_date()
        res_history.zeit = get_current_time_in_seconds()
        res_history.aenderung = "VIEWING DATA E-Signature"
        res_history.action = "E-Signature Setup"

    elif case_type == 1:

        for esign_list in query(esign_list_data):

            # guestbook = get_cache(Guestbook, {"gastnr": [(eq, esign_list.sign_id)]})
            guestbook = db_session.query(Guestbook).filter(Guestbook.gastnr == esign_list.sign_id).with_for_update().first()

            if guestbook:
                pass
                guestbook.infostr = to_string(esign_list.sign_nr) + "|" +\
                    esign_list.sign_name + "|" +\
                    esign_list.sign_use_for + "|" +\
                    esign_list.sign_position
                guestbook.imagefile = esign_list.sign_img
                guestbook.userinit = esign_list.sign_userinit
                guestbook.reserve_char[0] = esign_list.sign_pass
                guestbook.reserve_logic[0] = esign_list.sign_pr
                guestbook.reserve_logic[1] = esign_list.sign_po
                guestbook.reserve_logic[2] = esign_list.sign_dml
                
                flag_modified(guestbook, "reserve_char")
                flag_modified(guestbook, "reserve_logic")

                bediener = get_cache(Bediener, {"userinit": [(eq, user_init)]})
                res_history = Res_history()
                db_session.add(res_history)

                res_history.nr = bediener.nr
                res_history.datum = get_current_date()
                res_history.zeit = get_current_time_in_seconds()
                res_history.aenderung = "MODIFY E-Sign: ID Name " + esign_list.sign_name
                res_history.action = "E-Signature Setup"

            else:

                gbook = db_session.query(Gbook).filter(
                    (Gbook.gastnr >= -271150) & (Gbook.gastnr <= -271080)).first()

                if gbook:

                    for guestbook in db_session.query(Guestbook).filter(
                            (Guestbook.gastnr >= -271150) & (Guestbook.gastnr <= -271080)).order_by(Guestbook.gastnr).all():
                        booknr = guestbook.gastnr - 1
                        break
                else:
                    booknr = - 271080
                pass
                guestbook = Guestbook()
                db_session.add(guestbook)

                guestbook.gastnr = booknr
                guestbook.reserve_int[0] = esign_list.sign_nr
                guestbook.infostr = to_string(esign_list.sign_nr) + "|" +\
                    esign_list.sign_name + "|" +\
                    esign_list.sign_use_for + "|" +\
                    esign_list.sign_position
                guestbook.imagefile = esign_list.sign_img
                guestbook.userinit = esign_list.sign_userinit
                guestbook.reserve_char[0] = esign_list.sign_pass
                guestbook.reserve_logic[0] = esign_list.sign_pr
                guestbook.reserve_logic[1] = esign_list.sign_po
                guestbook.reserve_logic[2] = esign_list.sign_dml
                esign_list.sign_id = booknr
                
                flag_modified(guestbook, "reserve_char")
                flag_modified(guestbook, "reserve_logic")

                bediener = get_cache(Bediener, {"userinit": [(eq, user_init)]})
                res_history = Res_history()
                db_session.add(res_history)

                res_history.nr = bediener.nr
                res_history.datum = get_current_date()
                res_history.zeit = get_current_time_in_seconds()
                res_history.aenderung = "ADD E-Sign: ID Name " + esign_list.sign_name
                res_history.action = "E-Signature Setup"


    elif case_type == 2:

        esign_list = query(esign_list_data, filters=(
            lambda esign_list: esign_list.sign_select), first=True)

        if esign_list:

            queasy = get_cache(
                Queasy, {"key": [(eq, 245)], "number2": [(eq, esign_list.sign_id)]})

            if queasy:
                t_error_list.error_number = 1
                t_error_list.error_message = "E-Sign is already used in PR/PO/DML." + \
                    chr_unicode(10) + "Deletion is not allowed."

                return generate_output()

            queasy = get_cache(
                Queasy, {"key": [(eq, 227)], "number2": [(eq, esign_list.sign_id)]})

            if queasy:
                t_error_list.error_number = 1
                t_error_list.error_message = "E-Sign is already used in PR/PO/DML." + \
                    chr_unicode(10) + "Deletion is not allowed."

                return generate_output()

            queasy = get_cache(
                Queasy, {"key": [(eq, 352)], "number2": [(eq, esign_list.sign_id)]})

            if queasy:
                t_error_list.error_number = 1
                t_error_list.error_message = "E-Sign is already used in PR/PO/DML." + \
                    chr_unicode(10) + "Deletion is not allowed."

                return generate_output()

            # guestbook = get_cache(Guestbook, {"gastnr": [(eq, esign_list.sign_id)]})
            
            guestbook = db_session.query(Guestbook).filter(Guestbook.gastnr == esign_list.sign_id).with_for_update().first()

            if guestbook:
                db_session.delete(guestbook)

                bediener = get_cache(Bediener, {"userinit": [(eq, user_init)]})
                res_history = Res_history()
                db_session.add(res_history)

                res_history.nr = bediener.nr
                res_history.datum = get_current_date()
                res_history.zeit = get_current_time_in_seconds()
                res_history.aenderung = "DELETE E-Sign: ID Name " + esign_list.sign_name
                res_history.action = "E-Signature Setup"

    return generate_output()
