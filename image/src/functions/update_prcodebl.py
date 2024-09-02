from functions.additional_functions import *
import decimal
from functions.update_bookengine_configbl import update_bookengine_configbl
from models import Guest_pr, Queasy, Htparam, Ratecode, Pricecod

def update_prcodebl(gastnr:int, q2_list:[Q2_list]):
    new_contrate:bool = False
    new_flag:bool = False
    guest_pr = queasy = htparam = ratecode = pricecod = None

    q2_list = g_pr = qsy = None

    q2_list_list, Q2_list = create_model("Q2_list", {"char1":str, "char2":str, "logi2":bool, "number3":int, "selected":bool})

    G_pr = Guest_pr
    Qsy = Queasy

    db_session = local_storage.db_session

    def generate_output():
        nonlocal new_contrate, new_flag, guest_pr, queasy, htparam, ratecode, pricecod
        nonlocal g_pr, qsy


        nonlocal q2_list, g_pr, qsy
        nonlocal q2_list_list
        return {}

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 550)).first()

    if htparam.feldtyp == 4:
        new_contrate = htparam.flogical

    for guest_pr in db_session.query(Guest_pr).filter(
            (Guest_pr.gastnr == gastnr)).all():

        q2_list = query(q2_list_list, filters=(lambda q2_list :q2_list.char1 == guest_pr.CODE), first=True)

        if not q2_list:

            g_pr = db_session.query(G_pr).filter(
                    (G_pr.code == guest_pr.CODE) &  (G_pr.gastnr != guest_pr.gastnr)).first()

            if not g_pr:

                if new_contrate:

                    for ratecode in db_session.query(Ratecode).filter(
                            (Ratecode.code == guest_pr.CODE)).all():
                        db_session.delete(ratecode)

                else:

                    for pricecod in db_session.query(Pricecod).filter(
                            (Pricecod.code == guest_pr.CODE)).all():
                        db_session.delete(pricecod)


            queasy = db_session.query(Queasy).filter(
                    (Queasy.key == 159) &  (Queasy.number2 == gastnr)).first()

            if queasy:

                qsy = db_session.query(Qsy).filter(
                        (Qsy.key == 161) &  (entry(0, Qsy.char1, ";") == guest_pr.CODE)).first()
                while None != qsy:

                    qsy = db_session.query(Qsy).first()
                    db_session.delete(qsy)


                    qsy = db_session.query(Qsy).filter(
                            (Qsy.key == 161) &  (entry(0, Qsy.char1, ";") == guest_pr.CODE)).first()

                qsy = db_session.query(Qsy).filter(
                        (Qsy.key == 170) &  (Qsy.char1 == guest_pr.CODE)).first()
                while None != qsy:

                    qsy = db_session.query(Qsy).first()
                    db_session.delete(qsy)


                    qsy = db_session.query(Qsy).filter(
                            (Qsy.key == 170) &  (Qsy.char1 == guest_pr.CODE)).first()

                qsy = db_session.query(Qsy).filter(
                        (Qsy.key == 171) &  (Qsy.char1 == guest_pr.CODE)).first()
                while None != qsy:

                    qsy = db_session.query(Qsy).first()
                    db_session.delete(qsy)


                    qsy = db_session.query(Qsy).filter(
                            (Qsy.key == 171) &  (Qsy.char1 == guest_pr.CODE)).first()

            g_pr = db_session.query(G_pr).filter(
                    (G_pr._recid == guest_pr._recid)).first()
            db_session.delete(g_pr)


    for q2_list in query(q2_list_list):

        guest_pr = db_session.query(Guest_pr).filter(
                (Guest_pr.gastnr == gastnr) &  (Guest_pr.CODE == q2_list.char1)).first()

        if not guest_pr:
            new_flag = True
            guest_pr = Guest_pr()
            db_session.add(guest_pr)

            guest_pr.gastnr = gastnr
            guest_pr.CODE = q2_list.char1

    queasy = db_session.query(Queasy).filter(
            (Queasy.key == 159) &  (Queasy.number2 == gastnr)).first()

    if queasy and new_flag:
        get_output(update_bookengine_configbl(9, queasy.number1, True, ""))

    return generate_output()