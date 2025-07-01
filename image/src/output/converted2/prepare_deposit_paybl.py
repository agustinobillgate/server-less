#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from functions.htpint import htpint
from models import Reservation, Htparam, Waehrung, Artikel

def prepare_deposit_paybl(pvilanguage:int, inp_resnr:int, depositgef:Decimal):

    prepare_cache ([Htparam, Waehrung, Artikel])

    price_decimal = 0
    exchg_rate = to_decimal("0.0")
    depoart = 0
    depobezeich = ""
    ask_voucher = False
    deposit_exrate = 1
    f_tittle = ""
    msg_str = ""
    balance = to_decimal("0.0")
    paybez1 = ""
    paybez2 = ""
    artikel_list_list = []
    t_reservation_list = []
    lvcarea:string = "deposit-pay"
    unallocated_subgrp:int = 0
    sorttype:int = 0
    reservation = htparam = waehrung = artikel = None

    t_reservation = artikel_list = None

    t_reservation_list, T_reservation = create_model_like(Reservation)
    artikel_list_list, Artikel_list = create_model("Artikel_list", {"artnr":int, "departement":int, "bezeich":string, "artart":int, "payment":Decimal, "pay_exrate":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal price_decimal, exchg_rate, depoart, depobezeich, ask_voucher, deposit_exrate, f_tittle, msg_str, balance, paybez1, paybez2, artikel_list_list, t_reservation_list, lvcarea, unallocated_subgrp, sorttype, reservation, htparam, waehrung, artikel
        nonlocal pvilanguage, inp_resnr, depositgef


        nonlocal t_reservation, artikel_list
        nonlocal t_reservation_list, artikel_list_list

        return {"price_decimal": price_decimal, "exchg_rate": exchg_rate, "depoart": depoart, "depobezeich": depobezeich, "ask_voucher": ask_voucher, "deposit_exrate": deposit_exrate, "f_tittle": f_tittle, "msg_str": msg_str, "balance": balance, "paybez1": paybez1, "paybez2": paybez2, "artikel-list": artikel_list_list, "t-reservation": t_reservation_list}

    def display_artikel():

        nonlocal price_decimal, exchg_rate, depoart, depobezeich, ask_voucher, deposit_exrate, f_tittle, msg_str, balance, paybez1, paybez2, artikel_list_list, t_reservation_list, lvcarea, unallocated_subgrp, sorttype, reservation, htparam, waehrung, artikel
        nonlocal pvilanguage, inp_resnr, depositgef


        nonlocal t_reservation, artikel_list
        nonlocal t_reservation_list, artikel_list_list

        if sorttype == 1:

            for artikel in db_session.query(Artikel).filter(
                     (Artikel.departement == 0) & (((Artikel.artart == 6) | (Artikel.artart == 7)) | ((Artikel.artart == 2) & ((Artikel.zwkum == unallocated_subgrp)))) & (Artikel.activeflag)).order_by(Artikel.artnr).all():
                assign_it()

        else:

            for artikel in db_session.query(Artikel).filter(
                     (Artikel.departement == 0) & (((Artikel.artart == 6) | (Artikel.artart == 7)) | ((Artikel.artart == 2) & ((Artikel.zwkum == unallocated_subgrp)))) & (Artikel.activeflag)).order_by(Artikel.bezeich).all():
                assign_it()

    def assign_it():

        nonlocal price_decimal, exchg_rate, depoart, depobezeich, ask_voucher, deposit_exrate, f_tittle, msg_str, balance, paybez1, paybez2, artikel_list_list, t_reservation_list, lvcarea, unallocated_subgrp, sorttype, reservation, htparam, waehrung, artikel
        nonlocal pvilanguage, inp_resnr, depositgef


        nonlocal t_reservation, artikel_list
        nonlocal t_reservation_list, artikel_list_list


        artikel_list = Artikel_list()
        artikel_list_list.append(artikel_list)

        artikel_list.artnr = artikel.artnr
        artikel_list.departement = artikel.departement
        artikel_list.bezeich = artikel.bezeich
        artikel_list.artart = artikel.artart
        artikel_list.payment =  - to_decimal(balance) * to_decimal(deposit_exrate)
        artikel_list.pay_exrate = 1

        if artikel.pricetab:

            waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, artikel.betriebsnr)]})

            if waehrung:
                artikel_list.pay_exrate = waehrung.ankauf / waehrung.einheit


        artikel_list.payment =  to_decimal(artikel_list.payment) / to_decimal(artikel_list.pay_exrate)


    unallocated_subgrp = get_output(htpint(116))

    htparam = get_cache (Htparam, {"paramnr": [(eq, 491)]})
    price_decimal = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 144)]})

    waehrung = get_cache (Waehrung, {"wabkurz": [(eq, htparam.fchar)]})

    if waehrung:
        exchg_rate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)

    htparam = get_cache (Htparam, {"paramnr": [(eq, 120)]})

    artikel = get_cache (Artikel, {"artnr": [(eq, htparam.finteger)],"departement": [(eq, 0)]})

    if not artikel:
        msg_str = msg_str + chr_unicode(2) + translateExtended ("Deposit article not yet defined (group 5, no 120.)", lvcarea, "")

        return generate_output()
    else:
        depoart = artikel.artnr
        depobezeich = artikel.bezeich
        ask_voucher = artikel.resart

        if artikel.pricetab:

            waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, artikel.betriebsnr)]})

            if waehrung:
                deposit_exrate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)

    reservation = get_cache (Reservation, {"resnr": [(eq, inp_resnr)]})

    if not reservation:

        return generate_output()
    balance =  to_decimal(depositgef) - to_decimal(reservation.depositbez) -\
            reservation.depositbez2


    f_tittle = translateExtended ("Deposit Payment", lvcarea, "") + " - " + reservation.name + " / " + translateExtended ("ResNo:", lvcarea, "") + " " + to_string(reservation.resnr)
    sorttype = 1
    display_artikel()

    if reservation.zahlkonto != 0:

        artikel = get_cache (Artikel, {"artnr": [(eq, reservation.zahlkonto)],"departement": [(eq, 0)]})

        if artikel:
            paybez1 = artikel.bezeich

    if reservation.zahlkonto2 != 0:

        artikel = get_cache (Artikel, {"artnr": [(eq, reservation.zahlkonto2)],"departement": [(eq, 0)]})

        if artikel:
            paybez2 = artikel.bezeich
    t_reservation = T_reservation()
    t_reservation_list.append(t_reservation)

    buffer_copy(reservation, t_reservation)
    t_reservation.depositgef =  to_decimal(depositgef)

    return generate_output()