from functions.additional_functions import *
import decimal
from functions.htpint import htpint
from models import Reservation, Htparam, Waehrung, Artikel

def prepare_deposit_paybl(pvilanguage:int, inp_resnr:int, depositgef:decimal):
    price_decimal = 0
    exchg_rate = 0
    depoart = 0
    depobezeich = ""
    ask_voucher = False
    deposit_exrate = 0
    f_tittle = ""
    msg_str = ""
    balance = 0
    paybez1 = ""
    paybez2 = ""
    artikel_list_list = []
    t_reservation_list = []
    lvcarea:str = "deposit_pay"
    unallocated_subgrp:int = 0
    sorttype:int = 0
    reservation = htparam = waehrung = artikel = None

    t_reservation = artikel_list = None

    t_reservation_list, T_reservation = create_model_like(Reservation)
    artikel_list_list, Artikel_list = create_model("Artikel_list", {"artnr":int, "departement":int, "bezeich":str, "artart":int, "payment":decimal, "pay_exrate":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal price_decimal, exchg_rate, depoart, depobezeich, ask_voucher, deposit_exrate, f_tittle, msg_str, balance, paybez1, paybez2, artikel_list_list, t_reservation_list, lvcarea, unallocated_subgrp, sorttype, reservation, htparam, waehrung, artikel


        nonlocal t_reservation, artikel_list
        nonlocal t_reservation_list, artikel_list_list
        return {"price_decimal": price_decimal, "exchg_rate": exchg_rate, "depoart": depoart, "depobezeich": depobezeich, "ask_voucher": ask_voucher, "deposit_exrate": deposit_exrate, "f_tittle": f_tittle, "msg_str": msg_str, "balance": balance, "paybez1": paybez1, "paybez2": paybez2, "artikel-list": artikel_list_list, "t-reservation": t_reservation_list}

    def display_artikel():

        nonlocal price_decimal, exchg_rate, depoart, depobezeich, ask_voucher, deposit_exrate, f_tittle, msg_str, balance, paybez1, paybez2, artikel_list_list, t_reservation_list, lvcarea, unallocated_subgrp, sorttype, reservation, htparam, waehrung, artikel


        nonlocal t_reservation, artikel_list
        nonlocal t_reservation_list, artikel_list_list

        if sorttype == 1:

            for artikel in db_session.query(Artikel).filter(
                    (Artikel.departement == 0) &  (((Artikel.artart == 6) |  (Artikel.artart == 7)) |  ((Artikel.artart == 2) &  ((Artikel.zwkum == unallocated_subgrp)))) &  (Artikel.activeflag)).all():
                assign_it()

        else:

            for artikel in db_session.query(Artikel).filter(
                    (Artikel.departement == 0) &  (((Artikel.artart == 6) |  (Artikel.artart == 7)) |  ((Artikel.artart == 2) &  ((Artikel.zwkum == unallocated_subgrp)))) &  (Artikel.activeflag)).all():
                assign_it()


    def assign_it():

        nonlocal price_decimal, exchg_rate, depoart, depobezeich, ask_voucher, deposit_exrate, f_tittle, msg_str, balance, paybez1, paybez2, artikel_list_list, t_reservation_list, lvcarea, unallocated_subgrp, sorttype, reservation, htparam, waehrung, artikel


        nonlocal t_reservation, artikel_list
        nonlocal t_reservation_list, artikel_list_list


        artikel_list = Artikel_list()
        artikel_list_list.append(artikel_list)

        artikel_list.artnr = artikel.artnr
        artikel_list.departement = artikel.departement
        artikel_list.bezeich = artikel.bezeich
        artikel_list.artart = artikel.artart
        artikel_list.payment = - balance * deposit_exrate
        artikel_list.pay_exrate = 1

        if artikel.pricetab:

            waehrung = db_session.query(Waehrung).filter(
                    (Waehrungsnr == artikel.betriebsnr)).first()

            if waehrung:
                artikel_list.pay_exrate = waehrung.ankauf / waehrung.einheit


        artikel_list.payment = artikel_list.payment / pay_exrate

    unallocated_subgrp = get_output(htpint(116))

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 491)).first()
    price_decimal = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 144)).first()

    waehrung = db_session.query(Waehrung).filter(
            (Waehrung.wabkurz == htparam.fchar)).first()

    if waehrung:
        exchg_rate = waehrung.ankauf / waehrung.einheit

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 120)).first()

    artikel = db_session.query(Artikel).filter(
            (Artikel.artnr == htparam.finteger) &  (Artikel.departement == 0)).first()

    if not artikel:
        msg_str = msg_str + chr(2) + translateExtended ("Deposit article not yet defined (group 5, no 120.)", lvcarea, "")

        return generate_output()
    else:
        depoart = artikel.artnr
        depobezeich = artikel.bezeich
        ask_voucher = artikel.resart

        if artikel.pricetab:

            waehrung = db_session.query(Waehrung).filter(
                    (Waehrungsnr == artikel.betriebsnr)).first()

            if waehrung:
                deposit_exrate = waehrung.ankauf / waehrung.einheit

    reservation = db_session.query(Reservation).filter(
            (Reservation.resnr == inp_resnr)).first()
    balance = depositgef - reservation.depositbez -\
            reservation.depositbez2


    f_tittle = translateExtended ("Deposit Payment", lvcarea, "") + "  -  " + reservation.name + " / " + translateExtended ("ResNo:", lvcarea, "") + " " + to_string(reservation.resnr)
    sorttype = 1
    display_artikel()

    if reservation.zahlkonto != 0:

        artikel = db_session.query(Artikel).filter(
                (Artikel.artnr == reservation.zahlkonto) &  (Artikel.departement == 0)).first()

        if artikel:
            paybez1 = artikel.bezeich

    if reservation.zahlkonto2 != 0:

        artikel = db_session.query(Artikel).filter(
                (Artikel.artnr == reservation.zahlkonto2) &  (Artikel.departement == 0)).first()

        if artikel:
            paybez2 = artikel.bezeich
    t_reservation = T_reservation()
    t_reservation_list.append(t_reservation)

    buffer_copy(reservation, t_reservation)
    t_reservation.depositgef = depositgef

    return generate_output()