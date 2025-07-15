from functions.additional_functions import *
import decimal
from datetime import date
from models import Guest_pr, Ratecode, Pricecod

def mk_resline_chg_reservation2bl(gastno:int, new_contrate:bool, ci_date:date):
    flag1 = False
    avail_ratecode1 = False
    avail_ratecode2 = False
    avail_ratecode3 = False
    avail_pricecod = False
    t_guest_pr_list = []
    guest_pr = ratecode = pricecod = None

    t_guest_pr = None

    t_guest_pr_list, T_guest_pr = create_model_like(Guest_pr)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal flag1, avail_ratecode1, avail_ratecode2, avail_ratecode3, avail_pricecod, t_guest_pr_list, guest_pr, ratecode, pricecod
        nonlocal gastno, new_contrate, ci_date


        nonlocal t_guest_pr
        nonlocal t_guest_pr_list
        return {"flag1": flag1, "avail_ratecode1": avail_ratecode1, "avail_ratecode2": avail_ratecode2, "avail_ratecode3": avail_ratecode3, "avail_pricecod": avail_pricecod, "t-guest-pr": t_guest_pr_list}

    guest_pr = db_session.query(Guest_pr).filter(
             (Guest_pr.gastnr == gastno)).first()

    if guest_pr:

        if new_contrate:
            while None != guest_pr:

                ratecode = db_session.query(Ratecode).filter(
                         (Ratecode.code == guest_pr.code) & (ci_date <= Ratecode.endperiode)).first()

                if ratecode:
                    avail_ratecode1 = True

                ratecode = db_session.query(Ratecode).filter(
                         (Ratecode.code == guest_pr.code) & (Ratecode.char1[inc_value(0)] != "")).first()

                if ratecode:
                    avail_ratecode2 = True

                ratecode = db_session.query(Ratecode).filter(
                         (Ratecode.code == guest_pr.code) & (Ratecode.char1[inc_value(1)] != "")).first()

                if ratecode:
                    avail_ratecode3 = True

                curr_recid = guest_pr._recid
                guest_pr = db_session.query(Guest_pr).filter(
                         (Guest_pr.gastnr == gastnr)).filter(Guest_pr._recid > curr_recid).first()
            flag1 = True
        else:

            pricecod = db_session.query(Pricecod).filter(
                     (Pricecod.code == guest_pr.code) & (ci_date <= Pricecod.endperiode)).first()

            if pricecod:
                avail_pricecod = True

    guest_pr = db_session.query(Guest_pr).filter(
             (Guest_pr.gastnr == gastno)).first()

    if guest_pr:

        for guest_pr in db_session.query(Guest_pr).filter(
                 (Guest_pr.gastnr == gastno)).order_by(Guest_pr.code).all():
            t_guest_pr = T_guest_pr()
            t_guest_pr_list.append(t_guest_pr)

            buffer_copy(guest_pr, t_guest_pr)

    return generate_output()