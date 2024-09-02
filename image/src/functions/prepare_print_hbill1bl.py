from functions.additional_functions import *
import decimal
from models import H_bill, Queasy, Htparam, H_artikel

def prepare_print_hbill1bl(hbrecid:int):
    order_id = ""
    prdisc_flag = False
    disc_art1 = 0
    disc_art2 = 0
    disc_art3 = 0
    disc_zwkum = 0
    print_balance = False
    incl_service = False
    incl_mwst = False
    service_taxable = False
    print_fbtotal = False
    curr_dept:int = 0
    h_bill = queasy = htparam = h_artikel = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal order_id, prdisc_flag, disc_art1, disc_art2, disc_art3, disc_zwkum, print_balance, incl_service, incl_mwst, service_taxable, print_fbtotal, curr_dept, h_bill, queasy, htparam, h_artikel


        return {"order_id": order_id, "prdisc_flag": prdisc_flag, "disc_art1": disc_art1, "disc_art2": disc_art2, "disc_art3": disc_art3, "disc_zwkum": disc_zwkum, "print_balance": print_balance, "incl_service": incl_service, "incl_mwst": incl_mwst, "service_taxable": service_taxable, "print_fbtotal": print_fbtotal}


    h_bill = db_session.query(H_bill).filter(
            (H_bill._recid == hbrecid)).first()
    curr_dept = h_bill.departement

    if h_bill.betriebsnr != 0:

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == 10) &  (Queasy.number1 == h_bill.betriebsnr)).first()

        if queasy:
            order_id = "/" + queasy.char2

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 857)).first()
    prdisc_flag = htparam.flogical

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 557)).first()

    if htparam.finteger > 0:
        disc_art1 = htparam.finteger

    h_artikel = db_session.query(H_artikel).filter(
            (H_artikel.artnr == disc_art1) &  (H_artikel.departement == curr_dept)).first()

    if h_artikel:
        disc_zwkum = h_artikel.zwkum

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 596)).first()

    if htparam.finteger > 0:
        disc_art2 = htparam.finteger

    if disc_zwkum == 0 and disc_art2 != 0:

        h_artikel = db_session.query(H_artikel).filter(
                (H_artikel.artnr == disc_art2) &  (H_artikel.departement == curr_dept)).first()

        if h_artikel:
            disc_zwkum = h_artikel.zwkum

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 556)).first()

    if htparam.finteger > 0:
        disc_art3 = htparam.finteger

    if disc_zwkum == 0 and disc_art3 != 0:

        h_artikel = db_session.query(H_artikel).filter(
                (H_artikel.artnr == disc_art3) &  (H_artikel.departement == curr_dept)).first()

        if h_artikel:
            disc_zwkum = h_artikel.zwkum

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 899)).first()
    print_balance = htparam.flogical

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 135)).first()
    incl_service = htparam.flogical

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 134)).first()
    incl_mwst = htparam.flogical

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 479)).first()
    service_taxable = htparam.flogical

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 948)).first()

    if htparam.paramgruppe == 19 and htparam.flogical:
        print_fbtotal = htparam.flogical

    return generate_output()