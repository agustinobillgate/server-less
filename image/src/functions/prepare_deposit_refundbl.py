from functions.additional_functions import *
import decimal
from functions.htpint import htpint
from functions.htpchar import htpchar
from models import Reservation, Artikel, Htparam, Waehrung

def prepare_deposit_refundbl(resnr:int):
    deposit_exrate = 0
    depobezeich = ""
    depoart = 0
    flag_err = 0
    p_60 = 0
    p_152 = ""
    t_reservation_list = []
    t_artikel_list = []
    reservation = artikel = htparam = waehrung = None

    t_reservation = t_artikel = None

    t_reservation_list, T_reservation = create_model_like(Reservation)
    t_artikel_list, T_artikel = create_model_like(Artikel, {"pay_exrate":decimal, "w_wabkurz":str}, {"pay_exrate": 1})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal deposit_exrate, depobezeich, depoart, flag_err, p_60, p_152, t_reservation_list, t_artikel_list, reservation, artikel, htparam, waehrung


        nonlocal t_reservation, t_artikel
        nonlocal t_reservation_list, t_artikel_list
        return {"deposit_exrate": deposit_exrate, "depobezeich": depobezeich, "depoart": depoart, "flag_err": flag_err, "p_60": p_60, "p_152": p_152, "t-reservation": t_reservation_list, "t-artikel": t_artikel_list}

    p_60 = get_output(htpint(60))
    p_152 = get_output(htpchar(152))

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 120)).first()

    artikel = db_session.query(Artikel).filter(
            (Artikel.artnr == htparam.finteger) &  (Artikel.departement == 0)).first()

    if not artikel:
        flag_err = 1

        return generate_output()
    else:
        depoart = artikel.artnr
        depobezeich = artikel.bezeich

        if artikel.pricetab:

            waehrung = db_session.query(Waehrung).filter(
                    (Waehrungsnr == artikel.betriebsnr)).first()

            if waehrung:
                deposit_exrate = waehrung.ankauf / waehrung.einheit

    reservation = db_session.query(Reservation).filter(
            (Reservation.resnr == resnr)).first()
    t_reservation = T_reservation()
    t_reservation_list.append(t_reservation)

    buffer_copy(reservation, t_reservation)

    for artikel in db_session.query(Artikel).filter(
            (Artikel.departement == 0) &  ((Artikel.artart == 6) |  (Artikel.artart == 7)) &  (Artikel.activeflag)).all():
        t_artikel = T_artikel()
        t_artikel_list.append(t_artikel)

        buffer_copy(artikel, t_artikel)

        if artikel.pricetab:

            waehrung = db_session.query(Waehrung).filter(
                    (Waehrungsnr == artikel.betriebsnr)).first()

            if waehrung:
                t_artikel.pay_exrate = waehrung.ankauf / waehrung.einheit
                t_artikel.w_wabkurz = waehrung.wabkurz


            else:
                t_artikel.pay_exrate = 1

    return generate_output()