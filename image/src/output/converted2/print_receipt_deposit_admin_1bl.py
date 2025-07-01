#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from sqlalchemy import func
from models import Printer, Waehrung, Htparam, Reservation, Artikel, Guest, Res_line, Debitor

def print_receipt_deposit_admin_1bl(resnr:int, printer_nr:int):

    prepare_cache ([Waehrung, Htparam, Reservation, Artikel, Guest, Res_line, Debitor])

    curr_local = ""
    ch = ""
    ch1 = ""
    secondpay = ""
    string_guest = ""
    string_reslinename = ""
    string_deposit = ""
    balance = to_decimal("0.0")
    voucher_no = ""
    ci_date = None
    co_date = None
    rmno = ""
    t_printer_list = []
    printer = waehrung = htparam = reservation = artikel = guest = res_line = debitor = None

    t_printer = w1 = None

    t_printer_list, T_printer = create_model_like(Printer)

    W1 = create_buffer("W1",Waehrung)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal curr_local, ch, ch1, secondpay, string_guest, string_reslinename, string_deposit, balance, voucher_no, ci_date, co_date, rmno, t_printer_list, printer, waehrung, htparam, reservation, artikel, guest, res_line, debitor
        nonlocal resnr, printer_nr
        nonlocal w1


        nonlocal t_printer, w1
        nonlocal t_printer_list

        return {"curr_local": curr_local, "ch": ch, "ch1": ch1, "secondpay": secondpay, "string_guest": string_guest, "string_reslinename": string_reslinename, "string_deposit": string_deposit, "balance": balance, "voucher_no": voucher_no, "ci_date": ci_date, "co_date": co_date, "rmno": rmno, "t-printer": t_printer_list}

    if printer_nr == 0:
        printer_nr = 1

    printer = get_cache (Printer, {"nr": [(eq, printer_nr)]})
    t_printer = T_printer()
    t_printer_list.append(t_printer)

    buffer_copy(printer, t_printer)

    htparam = get_cache (Htparam, {"paramnr": [(eq, 152)]})
    curr_local = htparam.fchar

    reservation = get_cache (Reservation, {"resnr": [(eq, resnr)]})

    if reservation:

        if reservation.depositbez >= 1:

            artikel = get_cache (Artikel, {"artnr": [(eq, reservation.zahlkonto)],"departement": [(eq, 0)]})

            if artikel:

                if not artikel.pricetab:
                    ch = to_string(curr_local, "x(8) ") + to_string(artikel.bezeich, "x(24) ") + to_string(reservation.depositbez, "->>,>>>,>>9.99")
                else:

                    w1 = get_cache (Waehrung, {"waehrungsnr": [(eq, artikel.betriebsnr)]})
                    ch = to_string(w1.wabkurz, "x(8) ") + to_string(artikel.bezeich, "x(24) ") + to_string(reservation.depositbez, "->>,>>>,>>9.99")

        if reservation.depositbez2 >= 1:

            artikel = get_cache (Artikel, {"artnr": [(eq, reservation.zahlkonto2)],"departement": [(eq, 0)]})

            if artikel:

                if not artikel.pricetab:
                    ch1 = to_string(curr_local, "x(8) ") + to_string(artikel.bezeich, "x(24) ") + to_string(reservation.depositbez2, "->>,>>>,>>9.99")
                else:

                    w1 = get_cache (Waehrung, {"waehrungsnr": [(eq, artikel.betriebsnr)]})
                    ch1 = to_string(w1.wabkurz, "x(8) ") + to_string(artikel.bezeich, "x(24) ") + to_string(reservation.depositbez2, "->>,>>>,>>9.99")

        if reservation.depositbez2 != 0:
            secondpay = "1"
        string_guest = ""
        string_reslinename = ""

        guest = get_cache (Guest, {"gastnr": [(eq, reservation.gastnr)]})

        if guest:
            string_guest = guest.name + " " + guest.vorname1 + ", " + guest.anredefirma + guest.vorname1

        res_line = db_session.query(Res_line).filter(
                 (Res_line.resnr == reservation.resnr) & ((Res_line.resstatus <= 2) | (Res_line.resstatus == 5))).first()

        if not res_line:

            res_line = get_cache (Res_line, {"resnr": [(eq, reservation.resnr)],"resstatus": [(eq, 6)]})

        if res_line:
            string_reslinename = to_string(res_line.name, "x(36)")
        string_deposit = to_string(reservation.depositgef , "->>,>>>,>>>,>>9")
        balance =  to_decimal(reservation.depositgef) - to_decimal(reservation.depositbez) -\
                reservation.depositbez2

        debitor = db_session.query(Debitor).filter(
                 (Debitor.gastnr == reservation.gastnr) & (Debitor.gastnrmember == reservation.gastnr) & (matches(Debitor.vesrcod,"Deposit*")) & (matches(Debitor.vesrcod,"*" + to_string(reservation.resnr) + "*"))).first()

        if debitor:

            if num_entries(entry(1, debitor.vesrcod, ":") , ";") > 1:
                voucher_no = entry(1, entry(1, debitor.vesrcod, ":") , ";")


            else:
                voucher_no = " "


        else:
            voucher_no = " "

    res_line = get_cache (Res_line, {"resnr": [(eq, resnr)]})

    if res_line:
        ci_date = res_line.ankunft
        co_date = res_line.abreise
        rmno = res_line.zinr

    return generate_output()