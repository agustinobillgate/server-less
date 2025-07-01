#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from functions.htpint import htpint
from functions.htpchar import htpchar
from models import Reservation, Artikel, Htparam, Waehrung

def prepare_deposit_refundbl(resnr:int):

    prepare_cache ([Htparam, Waehrung])

    deposit_exrate = 1
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
    t_artikel_list, T_artikel = create_model_like(Artikel, {"pay_exrate":Decimal, "w_wabkurz":string}, {"pay_exrate": 1})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal deposit_exrate, depobezeich, depoart, flag_err, p_60, p_152, t_reservation_list, t_artikel_list, reservation, artikel, htparam, waehrung
        nonlocal resnr


        nonlocal t_reservation, t_artikel
        nonlocal t_reservation_list, t_artikel_list

        return {"deposit_exrate": deposit_exrate, "depobezeich": depobezeich, "depoart": depoart, "flag_err": flag_err, "p_60": p_60, "p_152": p_152, "t-reservation": t_reservation_list, "t-artikel": t_artikel_list}

    p_60 = get_output(htpint(60))
    p_152 = get_output(htpchar(152))

    htparam = get_cache (Htparam, {"paramnr": [(eq, 120)]})

    artikel = get_cache (Artikel, {"artnr": [(eq, htparam.finteger)],"departement": [(eq, 0)]})

    if not artikel:
        flag_err = 1

        return generate_output()
    else:
        depoart = artikel.artnr
        depobezeich = artikel.bezeich

        if artikel.pricetab:

            waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, artikel.betriebsnr)]})

            if waehrung:
                deposit_exrate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)

    reservation = get_cache (Reservation, {"resnr": [(eq, resnr)]})
    t_reservation = T_reservation()
    t_reservation_list.append(t_reservation)

    buffer_copy(reservation, t_reservation)

    for artikel in db_session.query(Artikel).filter(
             (Artikel.departement == 0) & ((Artikel.artart == 6) | (Artikel.artart == 7)) & (Artikel.activeflag)).order_by(Artikel._recid).all():
        t_artikel = T_artikel()
        t_artikel_list.append(t_artikel)

        buffer_copy(artikel, t_artikel)

        if artikel.pricetab:

            waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, artikel.betriebsnr)]})

            if waehrung:
                t_artikel.pay_exrate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)
                t_artikel.w_wabkurz = waehrung.wabkurz


            else:
                t_artikel.pay_exrate =  to_decimal("1")

    return generate_output()