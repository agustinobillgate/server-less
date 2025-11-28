#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 28/11/2025, with_for_update added
#-------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from functions.update_bookengine_configbl import update_bookengine_configbl
from models import Guest_pr, Queasy, Htparam, Ratecode, Pricecod

q2_list_data, Q2_list = create_model("Q2_list", {"char1":string, "char2":string, "logi2":bool, "number3":int, "selected":bool})

def update_prcodebl(gastnr:int, q2_list_data:[Q2_list]):

    prepare_cache ([Htparam])

    new_contrate:bool = False
    new_flag:bool = False
    guest_pr = queasy = htparam = ratecode = pricecod = None

    q2_list = g_pr = qsy = None

    G_pr = create_buffer("G_pr",Guest_pr)
    Qsy = create_buffer("Qsy",Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal new_contrate, new_flag, guest_pr, queasy, htparam, ratecode, pricecod
        nonlocal gastnr, q2_list_data
        nonlocal g_pr, qsy


        nonlocal q2_list, g_pr, qsy

        return {}

    htparam = get_cache (Htparam, {"paramnr": [(eq, 550)]})

    if htparam.feldtyp == 4:
        new_contrate = htparam.flogical

    for guest_pr in db_session.query(Guest_pr).filter(
             (Guest_pr.gastnr == gastnr)).order_by(Guest_pr._recid).all():
        pass

        q2_list = query(q2_list_data, filters=(lambda q2_list: q2_list.char1 == guest_pr.code), first=True)

        if not q2_list:

            g_pr = db_session.query(G_pr).filter(
                     (G_pr.code == guest_pr.code) & (G_pr.gastnr != guest_pr.gastnr)).first()

            if not g_pr:

                if new_contrate:

                    for ratecode in db_session.query(Ratecode).filter(
                             (Ratecode.code == guest_pr.code)).order_by(Ratecode._recid).with_for_update().all():
                        db_session.delete(ratecode)

                else:

                    for pricecod in db_session.query(Pricecod).filter(
                             (Pricecod.code == guest_pr.code)).order_by(Pricecod._recid).with_for_update().all():
                        db_session.delete(pricecod)


            queasy = get_cache (Queasy, {"key": [(eq, 159)],"number2": [(eq, gastnr)]})

            if queasy:

                qsy = db_session.query(Qsy).filter(
                         (Qsy.key == 161) & (entry(0, Qsy.char1, ";") == guest_pr.code)).with_for_update().first()
                while None != qsy:
                    pass
                    db_session.delete(qsy)
                    pass

                    curr_recid = qsy._recid
                    qsy = db_session.query(Qsy).filter(
                             (Qsy.key == 161) & (entry(0, Qsy.char1, ";") == guest_pr.code) & (Qsy._recid > curr_recid)).first()

                qsy = db_session.query(Qsy).filter(
                         (Qsy.key == 170) & (Qsy.char1 == guest_pr.code)).with_for_update().first()
                while None != qsy:
                    pass
                    db_session.delete(qsy)
                    pass

                    curr_recid = qsy._recid
                    qsy = db_session.query(Qsy).filter(
                             (Qsy.key == 170) & (Qsy.char1 == guest_pr.code) & (Qsy._recid > curr_recid)).first()

                qsy = db_session.query(Qsy).filter(
                         (Qsy.key == 171) & (Qsy.char1 == guest_pr.code)).with_for_update().first()
                while None != qsy:
                    pass
                    db_session.delete(qsy)
                    pass

                    curr_recid = qsy._recid
                    qsy = db_session.query(Qsy).filter(
                             (Qsy.key == 171) & (Qsy.char1 == guest_pr.code) & (Qsy._recid > curr_recid)).first()

            g_pr = db_session.query(G_pr).filter(
                     (G_pr._recid == guest_pr._recid)).with_for_update().first()
            db_session.delete(g_pr)
            pass

    for q2_list in query(q2_list_data):

        guest_pr = get_cache (Guest_pr, {"gastnr": [(eq, gastnr)],"code": [(eq, q2_list.char1)]})

        if not guest_pr:
            new_flag = True
            guest_pr = Guest_pr()
            db_session.add(guest_pr)

            guest_pr.gastnr = gastnr
            guest_pr.code = q2_list.char1

    queasy = get_cache (Queasy, {"key": [(eq, 159)],"number2": [(eq, gastnr)]})

    if queasy and new_flag:
        get_output(update_bookengine_configbl(9, queasy.number1, True, ""))

    return generate_output()