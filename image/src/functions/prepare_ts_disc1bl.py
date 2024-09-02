from functions.additional_functions import *
import decimal
from models import H_bill, Htparam

def prepare_ts_disc1bl(room:str, dept:int, tischnr:int):
    disc_alert = False
    disc_service = False
    disc_tax = False
    voucher_art = 0
    disc_art1 = 0
    disc_art2 = 0
    disc_art3 = 0
    prefix_rm = ""
    procent = 0
    t_h_bill_list = []
    h_bill = htparam = None

    t_h_bill = None

    t_h_bill_list, T_h_bill = create_model_like(H_bill, {"rec_id":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal disc_alert, disc_service, disc_tax, voucher_art, disc_art1, disc_art2, disc_art3, prefix_rm, procent, t_h_bill_list, h_bill, htparam


        nonlocal t_h_bill
        nonlocal t_h_bill_list
        return {"disc_alert": disc_alert, "disc_service": disc_service, "disc_tax": disc_tax, "voucher_art": voucher_art, "disc_art1": disc_art1, "disc_art2": disc_art2, "disc_art3": disc_art3, "prefix_rm": prefix_rm, "procent": procent, "t-h-bill": t_h_bill_list}

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1203)).first()

    if htparam.paramgruppe == 19 and htparam.feldtyp == 4:
        disc_alert = htparam.flogical

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 468)).first()
    disc_service = flogical

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 469)).first()
    disc_tax = flogical

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1001)).first()
    voucher_art = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 557)).first()
    disc_art1 = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 596)).first()
    disc_art2 = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 556)).first()
    disc_art3 = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 790)).first()

    if htparam.finteger != 0:
        prefix_rm = to_string(htparam.finteger)

        if substring(room, 0, 1) == prefix_rm:

            htparam = db_session.query(Htparam).filter(
                    (Htparam.paramnr == 791)).first()
            procent = htparam.fdecimal

    h_bill = db_session.query(H_bill).filter(
            (H_bill.departement == dept) &  (H_bill.tischnr == tischnr) &  (H_bill.flag == 0)).first()

    if h_bill:
        t_h_bill = T_h_bill()
        t_h_bill_list.append(t_h_bill)

        buffer_copy(h_bill, t_h_bill)
        t_h_bill.rec_id = h_bill._recid

    return generate_output()