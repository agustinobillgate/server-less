#using conversion tools version: 1.0.0.119
"""_yusufwijasena_26/01/2026

        remark: - added update from "Malik EF3176 - FA E-Sign PO"
                - fix usage lower func in validation
    """
from functions.additional_functions import *
from decimal import Decimal
from models import Guestbook, Queasy

def check_esignature1_webbl(case_type:int, user_init:string, docu_nr:string, flag_type:string):

    prepare_cache ([Guestbook, Queasy])

    found_flag = False
    esign_list_data = []
    esign_print_data = []
    i: int = 0
    guestbook = queasy = None

    esign_list = esign_print = reorder_esign_print = None

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
    esign_print_data, Esign_print = create_model(
        "Esign_print",
        {
            "sign_nr": int,
            "sign_name": string,
            "sign_img": bytes,
            "sign_date": string,
            "sign_position": string
        })
    reorder_esign_print_data, Reorder_esign_print = create_model_like(
        Esign_print)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal found_flag, esign_list_data, esign_print_data, i, guestbook, queasy
        nonlocal case_type, user_init, docu_nr, flag_type
        nonlocal esign_list, esign_print, reorder_esign_print
        nonlocal esign_list_data, esign_print_data, reorder_esign_print_data

        return {
            "found_flag": found_flag,
            "esign-list": esign_list_data,
            "esign-print": esign_print_data
        }

    if case_type == 1:
        # -- add esign for pr --
        if flag_type.lower() == "pr":

            guestbook = db_session.query(Guestbook).filter(
                (Guestbook.gastnr >= -271150) &
                (Guestbook.gastnr <= -271080) &
                (Guestbook.userinit == (user_init).lower()) &
                (Guestbook.reserve_logic[inc_value(0)])).first()

            if guestbook:
                found_flag = True
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

            else:
                found_flag = False

        elif flag_type.lower() == "po":
            # -- add esign for po --
            guestbook = db_session.query(Guestbook).filter(
                (Guestbook.gastnr >= -271150) &
                (Guestbook.gastnr <= -271080) &
                (Guestbook.userinit == (user_init).lower()) &
                (Guestbook.reserve_logic[inc_value(1)])).first()

            if guestbook:
                found_flag = True
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

            else:
                found_flag = False

        elif flag_type.lower() == "dml":
            # -- add esign for dml --
            guestbook = db_session.query(Guestbook).filter(
                (Guestbook.gastnr >= -271150) &
                (Guestbook.gastnr <= -271080) &
                (Guestbook.userinit == (user_init).lower()) &
                (Guestbook.reserve_logic[inc_value(2)])).first()

            if guestbook:
                found_flag = True
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

            else:
                found_flag = False

        elif flag_type.lower() == "fa po":
            # -- add esign for po fixed asset --
            guestbook = db_session.query(Guestbook).filter(
                (Guestbook.gastnr >= -271350) &
                (Guestbook.gastnr <= -271280) &
                (Guestbook.userinit == (user_init).lower()) &
                (Guestbook.reserve_logic[inc_value(1)])).first()

            if guestbook:
                found_flag = True
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

            else:
                found_flag = False

    elif case_type == 2:
        # -- add esign for pr --
        if flag_type.lower() == "pr":

            for queasy in db_session.query(Queasy).filter(
                    (Queasy.key == 227) &
                    (Queasy.char1 == (docu_nr).lower())).order_by(Queasy._recid):

                guestbook = db_session.query(Guestbook).filter(
                    (Guestbook.gastnr == queasy.number2) &
                    (Guestbook.reserve_logic[inc_value(0)])).first()

                if guestbook:
                    esign_print = Esign_print()
                    esign_print_data.append(esign_print)

                    esign_print.sign_nr = queasy.number1
                    esign_print.sign_name = entry(1, guestbook.infostr, "|")
                    esign_print.sign_img = guestbook.imagefile
                    esign_print.sign_date = entry(1, queasy.char3, "|")
                    esign_print.sign_position = entry(3, guestbook.infostr, "|")

        elif flag_type.lower() == "po":
            # -- add esign for po --
            for queasy in db_session.query(Queasy).filter(
                    (Queasy.key == 245) &
                    (Queasy.char1 == (docu_nr).lower())).order_by(Queasy._recid):

                guestbook = db_session.query(Guestbook).filter(
                    (Guestbook.gastnr == queasy.number2) &
                    (Guestbook.reserve_logic[inc_value(1)])).first()

                if guestbook:
                    esign_print = Esign_print()
                    esign_print_data.append(esign_print)

                    esign_print.sign_nr = queasy.number1
                    esign_print.sign_name = entry(1, guestbook.infostr, "|")
                    esign_print.sign_img = guestbook.imagefile
                    esign_print.sign_date = entry(1, queasy.char3, "|")
                    esign_print.sign_position = entry(3, guestbook.infostr, "|")


            for i in range(1, 4 + 1):
                esign_print = query(esign_print_data, filters=(
                    lambda esign_print: esign_print.sign_nr == i), first=True)

                if esign_print:
                    reorder_esign_print = Reorder_esign_print()
                    reorder_esign_print_data.append(reorder_esign_print)

                    buffer_copy(esign_print, reorder_esign_print)
                else:
                    reorder_esign_print = Reorder_esign_print()
                    reorder_esign_print_data.append(reorder_esign_print)

                    reorder_esign_print.sign_nr = i
            esign_print_data.clear()

            for reorder_esign_print in query(reorder_esign_print_data):
                esign_print = Esign_print()
                esign_print_data.append(esign_print)

                buffer_copy(reorder_esign_print, esign_print)

        elif flag_type.lower() == "dml":
            for queasy in db_session.query(Queasy).filter(
                    (Queasy.key == 352) &
                    (Queasy.char1 == (docu_nr).lower())).order_by(Queasy._recid):

                guestbook = db_session.query(Guestbook).filter(
                    (Guestbook.gastnr == queasy.number2) &
                    (Guestbook.reserve_logic[inc_value(2)])).first()

                if guestbook:
                    esign_print = Esign_print()
                    esign_print_data.append(esign_print)

                    esign_print.sign_nr = queasy.number1
                    esign_print.sign_name = entry(1, guestbook.infostr, "|")
                    esign_print.sign_img = guestbook.imagefile
                    esign_print.sign_date = entry(1, queasy.char3, "|")
                    esign_print.sign_position = entry(3, guestbook.infostr, "|")

        elif flag_type.lower() == "fa po":
            # -- add esign for po fixed asset--
            for queasy in db_session.query(Queasy).filter(
                (Queasy.key == 382) &
                (Queasy.char1 == (docu_nr).lower()) &
                    (Queasy.deci1 == 2)).order_by(Queasy._recid):

                guestbook = db_session.query(Guestbook).filter(
                    (Guestbook.gastnr == queasy.number2) &
                    (Guestbook.reserve_logic[inc_value(0)])).first()

                if guestbook:
                    esign_print = Esign_print()
                    esign_print_data.append(esign_print)

                    esign_print.sign_nr = queasy.number1
                    esign_print.sign_name = entry(1, guestbook.infostr, "|")
                    esign_print.sign_img = guestbook.imagefile
                    esign_print.sign_date = entry(1, queasy.char3, "|")
                    esign_print.sign_position = entry(3, guestbook.infostr, "|")

            for i in range(1, 4 + 1):
                esign_print = query(esign_print_data, filters=(
                    lambda esign_print: esign_print.sign_nr == i), first=True)

                if esign_print:
                    reorder_esign_print = Reorder_esign_print()
                    reorder_esign_print_data.append(reorder_esign_print)

                    buffer_copy(esign_print, reorder_esign_print)
                else:
                    reorder_esign_print = Reorder_esign_print()
                    reorder_esign_print_data.append(reorder_esign_print)

                    reorder_esign_print.sign_nr = i
            esign_print_data.clear()

            for reorder_esign_print in query(reorder_esign_print_data):
                esign_print = Esign_print()
                esign_print_data.append(esign_print)

                buffer_copy(reorder_esign_print, esign_print)

    return generate_output()