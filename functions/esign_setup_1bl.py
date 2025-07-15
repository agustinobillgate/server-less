#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Guestbook, Bediener, Res_history

esign_list_data, Esign_list = create_model("Esign_list", {"sign_nr":int, "sign_name":string, "sign_img":bytes, "sign_use_for":string, "sign_position":string, "sign_userinit":string, "sign_id":int, "sign_select":bool, "sign_pass":string, "sign_pr":bool, "sign_po":bool, "sign_dml":bool})

def esign_setup_1bl(case_type:int, user_init:string, esign_list_data:[Esign_list]):

    prepare_cache ([Bediener, Res_history])

    booknr:int = 0
    guestbook = bediener = res_history = None

    esign_list = gbook = None

    Gbook = create_buffer("Gbook",Guestbook)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal booknr, guestbook, bediener, res_history
        nonlocal case_type, user_init
        nonlocal gbook


        nonlocal esign_list, gbook

        return {"esign-list": esign_list_data}

    if case_type == 0:

        for guestbook in db_session.query(Guestbook).filter(
                 (Guestbook.gastnr >= -271150) & (Guestbook.gastnr <= -271080)).order_by(Guestbook.reserve_int[inc_value(0)]).all():
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

        bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})
        res_history = Res_history()
        db_session.add(res_history)

        res_history.nr = bediener.nr
        res_history.datum = get_current_date()
        res_history.zeit = get_current_time_in_seconds()
        res_history.aenderung = "VIEWING DATA E-Signature"
        res_history.action = "E-Signature Setup"


        pass
        pass
        pass
        pass

    elif case_type == 1:

        for esign_list in query(esign_list_data):

            guestbook = get_cache (Guestbook, {"gastnr": [(eq, esign_list.sign_id)]})

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

                bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})
                res_history = Res_history()
                db_session.add(res_history)

                res_history.nr = bediener.nr
                res_history.datum = get_current_date()
                res_history.zeit = get_current_time_in_seconds()
                res_history.aenderung = "MODIFY E-Sign: ID Name " + esign_list.sign_name
                res_history.action = "E-Signature Setup"


                pass
                pass
                pass
                pass
                pass
                pass
            else:

                gbook = db_session.query(Gbook).filter(
                         (Gbook.gastnr >= -271150) & (Gbook.gastnr <= -271080)).first()

                if gbook:

                    for guestbook in db_session.query(Guestbook).filter(
                             (Guestbook.gastnr >= -271150) & (Guestbook.gastnr <= -271080)).order_by(Guestbook.gastnr).yield_per(100):
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

                bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})
                res_history = Res_history()
                db_session.add(res_history)

                res_history.nr = bediener.nr
                res_history.datum = get_current_date()
                res_history.zeit = get_current_time_in_seconds()
                res_history.aenderung = "ADD E-Sign: ID Name " + esign_list.sign_name
                res_history.action = "E-Signature Setup"


                pass
                pass
                pass
                pass
                pass
                pass

    elif case_type == 2:

        esign_list = query(esign_list_data, filters=(lambda esign_list: esign_list.sign_select), first=True)

        if esign_list:

            guestbook = get_cache (Guestbook, {"gastnr": [(eq, esign_list.sign_id)]})

            if guestbook:
                pass
                db_session.delete(guestbook)

                bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})
                res_history = Res_history()
                db_session.add(res_history)

                res_history.nr = bediener.nr
                res_history.datum = get_current_date()
                res_history.zeit = get_current_time_in_seconds()
                res_history.aenderung = "DELETE E-Sign: ID Name " + esign_list.sign_name
                res_history.action = "E-Signature Setup"


                pass
                pass
                pass
                pass
                pass

    return generate_output()