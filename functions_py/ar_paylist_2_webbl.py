# using conversion tools version: 1.0.0.117
# ------------------------------------------
# Rd, 29/8/2025
# strip comment, bill_name
# bQ -> bq

# yusufwijasena, 28/11/2025
# - fixed spacing on long string
# - added substring gastname & bill_rcv to 34 character 
# ------------------------------------------

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, Guest, Debitor, Artikel, Bill, Bediener, Waehrung
from functions import log_program


def ar_paylist_2_webbl(comment: string, cledger: bool, ccard: bool, last_sort: int, from_date: date, to_date: date, from_art: int, to_art: int, mi_payment: bool, mi_transfer: bool, show_inv: bool, bill_name: string, bill_nr: int):

    prepare_cache([Htparam, Guest, Debitor, Artikel, Bill, Bediener, Waehrung])

    r_no = 0
    s_list_data = []
    t_list_data = []
    t_ar_paylist_data = []
    long_digit: bool = False
    htparam = guest = debitor = artikel = bill = bediener = waehrung = None

    s_list = t_list = output_list = t_ar_paylist = bguest = bdebitor = tbuff = bq = None

    s_list_data, S_list = create_model(
        "S_list",
        {
            "artnr": int,
            "bezeich": string,
            "betrag": Decimal
        })
    t_list_data, T_list = create_model(
        "T_list",
        {
            "artnr": int,
            "bezeich": string,
            "betrag": Decimal
        })
    output_list_data, Output_list = create_model(
        "Output_list",
        {
            "artnr": int,
            "pay_count": int,
            "flag": int,
            "pay_amt": Decimal,
            "dbetrag": Decimal,
            "sbetrag": string,
            "inv_no": string,
            "str": string,
            "bill_art": int,
            "debt_counter": int,
            "art_bezeich": string,
            "tbetrag": Decimal,
            "gastname": string,
            "soa_inv": string,
            "famt": string,
            "bill_num": int,
            "pay_famt": Decimal
        })
    t_ar_paylist_data, T_ar_paylist = create_model(
        "T_ar_paylist",
        {
            "bill_date": string,
            "bill_num": string,
            "inv_num": string,
            "bill_rcv": string,
            "debt_amt": string,
            "pay_amt": string,
            "pay_famt": string,
            "curr": string,
            "pay_art": string,
            "pay_date": string,
            "uid": string,
            "pay_comment": string,
            "tot_pay": string,
            "artno": string,
            "debt_counter": string,
            "art_bezeich": string,
            "tbetrag": string,
            "gastname": string,
            "soa_inv": string,
            "famt": string,
            "bill_num2": string
        })

    Bguest = create_buffer("Bguest", Guest)
    Bdebitor = create_buffer("Bdebitor", Debitor)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal r_no, s_list_data, t_list_data, t_ar_paylist_data, long_digit, htparam, guest, debitor, artikel, bill, bediener, waehrung
        nonlocal comment, cledger, ccard, last_sort, from_date, to_date, from_art, to_art, mi_payment, mi_transfer, show_inv, bill_name, bill_nr
        nonlocal bguest, bdebitor

        nonlocal s_list, t_list, output_list, t_ar_paylist, bguest, bdebitor, tbuff, bq
        nonlocal s_list_data, t_list_data, output_list_data, t_ar_paylist_data
                
        return {
            "r_no": r_no,
            "s-list": s_list_data,
            "t-list": t_list_data,
            "t-ar-paylist": t_ar_paylist_data
        }

    def create_list():
        nonlocal r_no, s_list_data, t_list_data, t_ar_paylist_data, long_digit, htparam, guest, debitor, artikel, bill, bediener, waehrung
        nonlocal comment, cledger, ccard, last_sort, from_date, to_date, from_art, to_art, mi_payment, mi_transfer, show_inv, bill_name, bill_nr
        nonlocal bguest, bdebitor
        nonlocal s_list, t_list, output_list, t_ar_paylist, bguest, bdebitor, tbuff, bq
        nonlocal s_list_data, t_list_data, output_list_data, t_ar_paylist_data

        s_list_data.clear()
        t_list_data.clear()
        output_list_data.clear()

        # Rd 29/8/2025
        comment = comment.strip()
        bill_name = bill_name.strip()

        if comment == "":
            if cledger and ccard:
                if last_sort == 1:
                    create_list1()
                elif last_sort == 2:
                    create_list1a()
                elif last_sort == 3:
                    create_list1b()
                elif last_sort == 4:
                    create_list1c()
                elif last_sort == 5:
                    create_list1d()
                elif last_sort == 6:
                    create_list1e()
                elif last_sort == 7:
                    if bill_nr != None:
                        create_list1f()
                    else:
                        create_list1fs()

            elif cledger and not ccard:
                if last_sort == 1:
                    create_list2()
                elif last_sort == 2:
                    create_list2a()
                elif last_sort == 3:
                    create_list2b()
                elif last_sort == 4:
                    create_list2c()
                elif last_sort == 5:
                    create_list2d()
                elif last_sort == 6:
                    create_list2e()
                elif last_sort == 7:
                    if bill_nr != None:
                        create_list2f()
                    else:
                        create_list2fs()

            elif ccard and not cledger:
                if last_sort == 1:
                    create_list3()
                elif last_sort == 2:
                    create_list3a()
                elif last_sort == 3:
                    create_list3b()
                elif last_sort == 4:
                    create_list3c()
                elif last_sort == 5:
                    create_list3d()
                elif last_sort == 6:
                    create_list3e()
                elif last_sort == 7:
                    if bill_nr != None:
                        create_list3f()
                    else:
                        create_list3fs()

        elif comment != "":
            if cledger and ccard:
                create_list11()
            elif cledger and not ccard:
                create_list21()
            elif ccard and not cledger:
                create_list31()

    def create_tot_payment():
        nonlocal r_no, s_list_data, t_list_data, t_ar_paylist_data, long_digit, htparam, guest, debitor, artikel, bill, bediener, waehrung
        nonlocal comment, cledger, ccard, last_sort, from_date, to_date, from_art, to_art, mi_payment, mi_transfer, show_inv, bill_name, bill_nr
        nonlocal bguest, bdebitor
        nonlocal s_list, t_list, output_list, t_ar_paylist, bguest, bdebitor, tbuff, bq
        nonlocal s_list_data, t_list_data, output_list_data, t_ar_paylist_data

        curr_artno: int = 0
        tbetrag: Decimal = to_decimal("0.0")
        curr_count: int = 0
        Tbuff = Output_list
        tbuff_data = output_list_data
        bq = Output_list
        bq_data = output_list_data

        bq = query(bq_data, filters=(lambda bq: bq.pay_count != 0), first=True)

        if not bq:
            return

        for bq in query(bq_data, filters=(lambda bq: bq.flag == 1 and bq.pay_count != 0), sort_by=[("pay_count", False)]):
            if curr_count == 0:
                curr_count = bq.pay_count

            if (curr_count != bq.pay_count):
                for tbuff in query(tbuff_data, filters=(lambda tbuff: tbuff.pay_count == curr_count)):
                    if not long_digit:
                        tbuff.sbetrag = to_string(tbetrag, "->,>>>,>>>,>>9.99")
                    else:
                        tbuff.sbetrag = to_string(tbetrag, " ->>>,>>>,>>>,>>9")
                    tbuff.dbetrag = to_decimal(tbetrag)
                tbetrag = to_decimal("0")
            curr_count = bq.pay_count
            tbetrag = to_decimal(tbetrag) + to_decimal(bq.pay_amt)

        for tbuff in query(tbuff_data, filters=(lambda tbuff: tbuff.pay_count == curr_count)):

            if not long_digit:
                tbuff.sbetrag = to_string(tbetrag, "->,>>>,>>>,>>9.99")
            else:
                tbuff.sbetrag = to_string(tbetrag, " ->>>,>>>,>>>,>>9")
            tbuff.dbetrag = to_decimal(tbetrag)

    def create_list1():
        nonlocal r_no, s_list_data, t_list_data, t_ar_paylist_data, long_digit, htparam, guest, debitor, artikel, bill, bediener, waehrung
        nonlocal comment, cledger, ccard, last_sort, from_date, to_date, from_art, to_art, mi_payment, mi_transfer, show_inv, bill_name, bill_nr
        nonlocal bguest, bdebitor
        nonlocal s_list, t_list, output_list, t_ar_paylist, bguest, bdebitor, tbuff, bq
        nonlocal s_list_data, t_list_data, output_list_data, t_ar_paylist_data

        artnr: int = 0
        i: int = 0
        curr_gastnr: int = 0
        t_credit: Decimal = to_decimal("0.0")
        tot_credit: Decimal = to_decimal("0.0")
        t_famt: Decimal = to_decimal("0.0")
        tot_famt: Decimal = to_decimal("0.0")
        tot_saldo: Decimal = to_decimal("0.0")
        tot_foreign: Decimal = to_decimal("0.0")
        receiver: string = ""
        do_it: bool = False
        temp_name: string = ""
        temp_vorname1: string = ""
        temp_anredefirma: string = ""
        temp_anrede1: string = ""
        debt = None
        art = None
        t_guest = None
        tstr: string = ""
        Debt = create_buffer("Debt", Debitor)
        Art = create_buffer("Art", Artikel)
        T_guest = create_buffer("T_guest", Guest)

        debitor_obj_list = {}
        debitor = Debitor()
        debt = Debitor()
        artikel = Artikel()
        art = Artikel()
        guest = Guest()
        for debitor.gastnr, debitor.saldo, debitor.zahlkonto, debitor.betriebsnr, debitor.counter, debitor.rechnr, debitor.debref, debitor.rgdatum, debitor.gastnrmember, debitor.bediener_nr, debitor.vesrcod, debitor.vesrdep, debitor.betrieb_gastmem, debitor._recid, debt.gastnr, debt.saldo, debt.zahlkonto, debt.betriebsnr, debt.counter, debt.rechnr, debt.debref, debt.rgdatum, debt.gastnrmember, debt.bediener_nr, debt.vesrcod, debt.vesrdep, debt.betrieb_gastmem, debt._recid, artikel.artnr, artikel.bezeich, artikel.artart, artikel._recid, art.artnr, art.bezeich, art.artart, art._recid, guest.name, guest.vorname1, guest.anredefirma, guest.anrede1, guest._recid in db_session.query(Debitor.gastnr, Debitor.saldo, Debitor.zahlkonto, Debitor.betriebsnr, Debitor.counter, Debitor.rechnr, Debitor.debref, Debitor.rgdatum, Debitor.gastnrmember, Debitor.bediener_nr, Debitor.vesrcod, Debitor.vesrdep, Debitor.betrieb_gastmem, Debitor._recid, Debt.gastnr, Debt.saldo, Debt.zahlkonto, Debt.betriebsnr, Debt.counter, Debt.rechnr, Debt.debref, Debt.rgdatum, Debt.gastnrmember, Debt.bediener_nr, Debt.vesrcod, Debt.vesrdep, Debt.betrieb_gastmem, Debt._recid, Artikel.artnr, Artikel.bezeich, Artikel.artart, Artikel._recid, Art.artnr, Art.bezeich, Art.artart, Art._recid, Guest.name, Guest.vorname1, Guest.anredefirma, Guest.anrede1, Guest._recid).join(Debt, (Debt.counter == Debitor.counter) & (Debt.zahlkonto == 0)).join(Artikel, (Artikel.artnr == Debitor.artnr) & (Artikel.departement == 0)).join(Art, (Art.artnr == Debitor.zahlkonto) & (Art.departement == 0)).join(Guest, (Guest.gastnr == Debitor.gastnr)).filter(
                (Debitor.rgdatum >= from_date) & (Debitor.rgdatum <= to_date) & (Debitor.zahlkonto > 0) & (Debitor.artnr >= from_art) & (Debitor.artnr <= to_art) & (Debitor.counter > 0) & (Debitor.opart > 0)).order_by(Artikel.artnr, Debitor.name, Debitor.gastnr, Debitor.rgdatum, Debitor.zahlkonto, Debitor.betriebsnr, Debitor.rechnr).all():
            if debitor_obj_list.get(debitor._recid):
                continue
            else:
                debitor_obj_list[debitor._recid] = True
            do_it = True

            if mi_payment:
                if artikel.artart == 2 and art.artart != 4 and art.artart != 7:
                    do_it = False

                elif artikel.artart == 7 and art.artart != 4:
                    do_it = False

            elif mi_transfer:

                if artikel.artart == 2 and (art.artart == 4 or art.artart == 7):
                    do_it = False

                elif artikel.artart == 7 and art.artart == 4:
                    do_it = False

            if do_it and (bill_name != "") and (substring(bill_name, 0, 1) != ("*").lower()):

                if not matches(guest.name, r"*" + bill_name + r"*"):
                    do_it = False

            if do_it and (bill_name != "") and (substring(bill_name, 0, 1) == ("*").lower()):

                if not matches(guest.name, bill_name):
                    do_it = False

            if do_it:

                if curr_gastnr == 0:
                    curr_gastnr = debitor.gastnr

                if curr_gastnr != debitor.gastnr:
                    curr_gastnr = debitor.gastnr
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    for i in range(1, 58 + 1):
                        output_list.str = output_list.str + "   "
                    output_list.pay_amt = to_decimal(tot_saldo)
                    output_list.pay_famt = to_decimal(tot_foreign)

                    if not long_digit:
                        output_list.str = output_list.str + "T O T A L " +\
                            to_string(tot_saldo, "->,>>>,>>>,>>9.99") +\
                            fill(" ", 78) +\
                            to_string(tot_foreign, " ->>,>>>,>>>,>>9.99")
                    else:
                        output_list.str = output_list.str + "T O T A L " +\
                            to_string(tot_saldo, " ->>>,>>>,>>>,>>9") +\
                            fill(" ", 78) +\
                            to_string(tot_foreign, "   ->>>,>>>,>>>,>>9")
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    tot_saldo = to_decimal("0")
                    tot_foreign = to_decimal("0")

                if artnr != artikel.artnr:
                    t_list = T_list()
                    t_list_data.append(t_list)

                    t_list.artnr = artikel.artnr
                    t_list.bezeich = artikel.bezeich

                    if artnr != 0:

                        if tot_saldo != 0:
                            output_list = Output_list()
                            output_list_data.append(output_list)

                            for i in range(1, 58 + 1):
                                output_list.str = output_list.str + "   "
                            output_list.pay_amt = to_decimal(tot_saldo)
                            output_list.pay_famt = to_decimal(tot_foreign)

                            if not long_digit:
                                output_list.str = output_list.str + "T O T A L " +\
                                    to_string(tot_saldo, "->,>>>,>>>,>>9.99") +\
                                    fill(" ", 78) +\
                                    to_string(
                                        tot_foreign, " ->>,>>>,>>>,>>9.99")
                            else:
                                output_list.str = output_list.str + "T O T A L " +\
                                    to_string(tot_saldo, " ->>>,>>>,>>>,>>9") +\
                                    fill(" ", 78) +\
                                    to_string(
                                        tot_foreign, "   ->>>,>>>,>>>,>>9")
                            output_list = Output_list()
                            output_list_data.append(output_list)

                            tot_saldo = to_decimal("0")
                            tot_foreign = to_decimal("0")
                        output_list = Output_list()
                        output_list_data.append(output_list)

                        for i in range(1, 58 + 1):
                            output_list.str = output_list.str + "   "
                        output_list.pay_amt = to_decimal(t_credit)
                        output_list.pay_famt = to_decimal(t_famt)

                        if not long_digit:
                            output_list.str = output_list.str + "Sub-Total " +\
                                to_string(t_credit, "->,>>>,>>>,>>9.99") +\
                                fill(" ", 78) +\
                                to_string(t_famt, "->>,>>>,>>>,>>9.99")
                        else:
                            output_list.str = output_list.str + "Sub-Total " +\
                                to_string(t_credit, " ->>>,>>>,>>>,>>9") +\
                                fill(" ", 78) +\
                                to_string(t_famt, "  ->>>,>>>,>>>,>>9")
                        output_list = Output_list()
                        output_list_data.append(output_list)

                        t_credit = to_decimal("0")
                        t_famt = to_decimal("0")
                        tot_saldo = to_decimal("0")
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    for i in range(1, 19 + 1):
                        output_list.str = output_list.str + " "
                    output_list.str = output_list.str +\
                        to_string(artikel.artnr, ">>>>9") + " - " +\
                        to_string(artikel.bezeich, "x(24)")
                    artnr = artikel.artnr
                t_list.betrag = to_decimal(
                    t_list.betrag) - to_decimal(debitor.saldo)

                if guest.name != None:
                    temp_name = guest.name

                else:
                    temp_name = ""

                if guest.vorname1 != None:
                    temp_vorname1 = guest.vorname1

                else:
                    temp_vorname1 = ""

                if guest.anredefirma != None:
                    temp_anredefirma = guest.anredefirma

                else:
                    temp_anredefirma = ""

                if guest.anrede1 != None:
                    temp_anrede1 = guest.anrede1

                else:
                    temp_anrede1 = ""
                receiver = temp_name + ", " + temp_vorname1 + " " + temp_anredefirma + \
                    temp_anrede1
                output_list = Output_list()
                output_list_data.append(output_list)

                output_list.flag = 1
                output_list.artnr = debitor.zahlkonto
                output_list.pay_amt = to_decimal(debitor.saldo)
                output_list.pay_count = debitor.betriebsnr
                output_list.bill_art = artikel.artnr
                output_list.debt_counter = debitor.counter
                output_list.famt = to_string(
                    debt.vesrdep, "->>,>>>,>>>,>>9.99")
                output_list.pay_famt = to_decimal(debt.vesrdep)

                if show_inv:

                    bill = get_cache(Bill, {"rechnr": [(eq, debitor.rechnr)]})

                    if bill:
                        output_list.inv_no = to_string(
                            bill.rechnr2, ">>>>>>>>>")

                        if bill.billref != 0:
                            output_list.soa_inv = "INV" + \
                                to_string(bill.billref, "9999999")
                    else:

                        bdebitor = get_cache(
                            Debitor, {"rechnr": [(eq, debitor.rechnr)], "debref": [(gt, 0)]})

                        if bdebitor:
                            output_list.soa_inv = "INV" + \
                                to_string(debitor.debref, "9999999")

                if not long_digit:
                    output_list.str = to_string(debt.rgdatum) +\
                        to_string(debitor.rechnr, ">>>,>>>,>>9") +\
                        to_string(receiver, "x(32)") +\
                        to_string(debt.saldo, "->,>>>,>>>,>>9.99") +\
                        to_string(debitor.saldo, "->,>>>,>>>,>>9.99") +\
                        to_string(art.bezeich, "x(34)") +\
                        to_string(debitor.rgdatum)
                else:
                    output_list.str = to_string(debt.rgdatum) +\
                        to_string(debitor.rechnr, ">>>,>>>,>>9") +\
                        to_string(receiver, "x(32)") +\
                        to_string(debt.saldo, " ->>>,>>>,>>>,>>9") +\
                        to_string(debitor.saldo, " ->>>,>>>,>>>,>>9") +\
                        to_string(art.bezeich, "x(34)") +\
                        to_string(debitor.rgdatum)
                output_list.bill_num = debitor.rechnr
                output_list.art_bezeich = artikel.bezeich
                output_list.tbetrag = to_decimal(
                    output_list.tbetrag) - to_decimal(debitor.saldo)

                bguest = get_cache(
                    Guest, {"gastnr": [(eq, debitor.gastnrmember)]})

                if bguest:
                    output_list.gastname = substring(f"{bguest.name}, {bguest.vorname1}{bguest.anredefirma} {bguest.anrede1}", 0, 32)

                bediener = get_cache(
                    Bediener, {"nr": [(eq, debitor.bediener_nr)]})

                if bediener:
                    output_list.str = output_list.str + \
                        to_string(bediener.userinit, "x(3)")
                else:
                    output_list.str = output_list.str + "   "
                    
                output_list.str = output_list.str + to_string(debitor.vesrcod, "x(34)")
                t_credit = to_decimal(t_credit) + to_decimal(debitor.saldo)
                t_famt = to_decimal(t_famt) + to_decimal(debitor.vesrdep)
                tot_credit = to_decimal(tot_credit) + to_decimal(debitor.saldo)
                tot_saldo = to_decimal(tot_saldo) + to_decimal(debitor.saldo)
                tot_foreign = to_decimal(tot_foreign) + to_decimal(debitor.vesrdep)
                tot_famt = to_decimal(tot_famt) + to_decimal(debitor.vesrdep)

                s_list = query(s_list_data, filters=(
                    lambda s_list: s_list.artnr == art.artnr), first=True)

                if not s_list:
                    s_list = S_list()
                    s_list_data.append(s_list)

                    s_list.artnr = art.artnr
                    s_list.bezeich = art.bezeich
                output_list.str = output_list.str + to_string(debitor.vesrdep, "->>,>>>,>>>,>>9.99")

                waehrung = get_cache(
                    Waehrung, {"waehrungsnr": [(eq, debitor.betrieb_gastmem)]})

                if waehrung:
                    output_list.str = output_list.str + \
                        to_string(waehrung.wabkurz, "x(4)")
                else:
                    output_list.str = output_list.str + "    "

                t_guest = get_cache(
                    Guest, {"gastnr": [(eq, debt.gastnrmember)]})

                if t_guest:
                    tstr = substring(f"{t_guest.name}, {t_guest.vorname1}{t_guest.anrede1}", 0, 34)
                else:
                    tstr = " "
                output_list.str = output_list.str + to_string(tstr, "x(50)")
                output_list.str = output_list.str + to_string(debitor.vesrdep, "->,>>>,>>>,>>9.99")
                output_list.str = output_list.str + to_string(debitor.zahlkonto, ">>>>9")
                output_list.str = output_list.str + to_string(debitor.vesrdep, "->,>>>,>>>,>>9.99")
                output_list.str = output_list.str + to_string(artikel.bezeich, "x(40)")

                s_list.betrag = to_decimal(
                    s_list.betrag) + to_decimal(debitor.saldo)
        output_list = Output_list()
        output_list_data.append(output_list)

        for i in range(1, 58 + 1):
            output_list.str = output_list.str + "   "
        output_list.pay_amt = to_decimal(tot_saldo)
        output_list.pay_famt = to_decimal(tot_foreign)

        if not long_digit:
            output_list.str = output_list.str + "T O T A L " +\
                to_string(tot_saldo, "->,>>>,>>>,>>9.99") +\
                fill(" ", 78) +\
                to_string(tot_foreign, " ->>,>>>,>>>,>>9.99")
        else:
            output_list.str = output_list.str + "T O T A L " +\
                to_string(tot_saldo, " ->>>,>>>,>>>,>>9") +\
                fill(" ", 78) +\
                to_string(tot_foreign, "   ->>>,>>>,>>>,>>9")
        output_list = Output_list()
        output_list_data.append(output_list)

        output_list = Output_list()
        output_list_data.append(output_list)

        for i in range(1, 58 + 1):
            output_list.str = output_list.str + "   "
        output_list.pay_amt = to_decimal(t_credit)
        output_list.pay_famt = to_decimal(t_famt)

        if not long_digit:
            output_list.str = output_list.str + "Sub-Total " +\
                to_string(t_credit, "->,>>>,>>>,>>9.99") +\
                fill(" ", 78) +\
                to_string(t_famt, "->>,>>>,>>>,>>9.99")
        else:
            output_list.str = output_list.str + "Sub-Total " +\
                to_string(t_credit, " ->>>,>>>,>>>,>>9") +\
                fill(" ", 78) +\
                to_string(t_famt, "  ->>>,>>>,>>>,>>9")
        output_list = Output_list()
        output_list_data.append(output_list)

        output_list = Output_list()
        output_list_data.append(output_list)

        for i in range(1, 56 + 1):
            output_list.str = output_list.str + " "
        output_list.pay_amt = to_decimal(tot_credit)
        output_list.pay_famt = to_decimal(tot_famt)

        if not long_digit:
            output_list.str = output_list.str + "Grand TOTAL " +\
                to_string(tot_credit, "->,>>>,>>>,>>9.99") +\
                fill(" ", 78) +\
                to_string(tot_famt, "->>,>>>,>>>,>>9.99")
        else:
            output_list.str = output_list.str + "Grand TOTAL " +\
                to_string(tot_credit, " ->>>,>>>,>>>,>>9") +\
                fill(" ", 78) +\
                to_string(tot_famt, "  ->>>,>>>,>>>,>>9")
        create_tot_payment()

    def create_list1a():

        nonlocal r_no, s_list_data, t_list_data, t_ar_paylist_data, long_digit, htparam, guest, debitor, artikel, bill, bediener, waehrung
        nonlocal comment, cledger, ccard, last_sort, from_date, to_date, from_art, to_art, mi_payment, mi_transfer, show_inv, bill_name, bill_nr
        nonlocal bguest, bdebitor

        nonlocal s_list, t_list, output_list, t_ar_paylist, bguest, bdebitor, tbuff, bq
        nonlocal s_list_data, t_list_data, output_list_data, t_ar_paylist_data

        artnr: int = 0
        i: int = 0
        curr_gastnr: int = 0
        t_credit: Decimal = to_decimal("0.0")
        tot_credit: Decimal = to_decimal("0.0")
        t_famt: Decimal = to_decimal("0.0")
        tot_famt: Decimal = to_decimal("0.0")
        tot_saldo: Decimal = to_decimal("0.0")
        tot_foreign: Decimal = to_decimal("0.0")
        receiver: string = ""
        do_it: bool = False
        temp_name: string = ""
        temp_vorname1: string = ""
        temp_anredefirma: string = ""
        temp_anrede1: string = ""
        debt = None
        art = None
        t_guest = None
        tstr: string = ""
        Debt = create_buffer("Debt", Debitor)
        Art = create_buffer("Art", Artikel)
        T_guest = create_buffer("T_guest", Guest)

        debitor_obj_list = {}
        debitor = Debitor()
        debt = Debitor()
        artikel = Artikel()
        art = Artikel()
        guest = Guest()
        for debitor.gastnr, debitor.saldo, debitor.zahlkonto, debitor.betriebsnr, debitor.counter, debitor.rechnr, debitor.debref, debitor.rgdatum, debitor.gastnrmember, debitor.bediener_nr, debitor.vesrcod, debitor.vesrdep, debitor.betrieb_gastmem, debitor._recid, debt.gastnr, debt.saldo, debt.zahlkonto, debt.betriebsnr, debt.counter, debt.rechnr, debt.debref, debt.rgdatum, debt.gastnrmember, debt.bediener_nr, debt.vesrcod, debt.vesrdep, debt.betrieb_gastmem, debt._recid, artikel.artnr, artikel.bezeich, artikel.artart, artikel._recid, art.artnr, art.bezeich, art.artart, art._recid, guest.name, guest.vorname1, guest.anredefirma, guest.anrede1, guest._recid in db_session.query(Debitor.gastnr, Debitor.saldo, Debitor.zahlkonto, Debitor.betriebsnr, Debitor.counter, Debitor.rechnr, Debitor.debref, Debitor.rgdatum, Debitor.gastnrmember, Debitor.bediener_nr, Debitor.vesrcod, Debitor.vesrdep, Debitor.betrieb_gastmem, Debitor._recid, Debt.gastnr, Debt.saldo, Debt.zahlkonto, Debt.betriebsnr, Debt.counter, Debt.rechnr, Debt.debref, Debt.rgdatum, Debt.gastnrmember, Debt.bediener_nr, Debt.vesrcod, Debt.vesrdep, Debt.betrieb_gastmem, Debt._recid, Artikel.artnr, Artikel.bezeich, Artikel.artart, Artikel._recid, Art.artnr, Art.bezeich, Art.artart, Art._recid, Guest.name, Guest.vorname1, Guest.anredefirma, Guest.anrede1, Guest._recid).join(Debt, (Debt.counter == Debitor.counter) & (Debt.zahlkonto == 0)).join(Artikel, (Artikel.artnr == Debitor.artnr) & (Artikel.departement == 0)).join(Art, (Art.artnr == Debitor.zahlkonto) & (Art.departement == 0)).join(Guest, (Guest.gastnr == Debitor.gastnr)).filter(
                (Debitor.rgdatum >= from_date) & (Debitor.rgdatum <= to_date) & (Debitor.zahlkonto > 0) & (Debitor.artnr >= from_art) & (Debitor.artnr <= to_art) & (Debitor.counter > 0) & (Debitor.opart > 0)).order_by(Artikel.artnr, Debitor.zahlkonto, Debitor.name, Debitor.rgdatum, Debitor.rechnr).all():
            if debitor_obj_list.get(debitor._recid):
                continue
            else:
                debitor_obj_list[debitor._recid] = True

            do_it = True

            if mi_payment:

                if artikel.artart == 2 and art.artart != 4 and art.artart != 7:
                    do_it = False

                elif artikel.artart == 7 and art.artart != 4:
                    do_it = False

            elif mi_transfer:

                if artikel.artart == 2 and (art.artart == 4 or art.artart == 7):
                    do_it = False

                elif artikel.artart == 7 and art.artart == 4:
                    do_it = False

            if do_it and (bill_name != "") and (substring(bill_name, 0, 1) != ("*").lower()):

                if not matches(guest.name, r"*" + bill_name + r"*"):
                    do_it = False

            if do_it and (bill_name != "") and (substring(bill_name, 0, 1) == ("*").lower()):

                if not matches(guest.name, bill_name):
                    do_it = False

            if do_it:

                if curr_gastnr == 0:
                    curr_gastnr = debitor.zahlkonto

                if curr_gastnr != debitor.zahlkonto:
                    curr_gastnr = debitor.zahlkonto
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    for i in range(1, 58 + 1):
                        output_list.str = output_list.str + "   "
                    output_list.pay_amt = to_decimal(tot_saldo)
                    output_list.pay_famt = to_decimal(tot_foreign)

                    if not long_digit:
                        output_list.str = output_list.str + "T O T A L " +\
                            to_string(tot_saldo, "->,>>>,>>>,>>9.99") +\
                            fill(" ", 78) +\
                            to_string(tot_foreign, " ->>,>>>,>>>,>>9.99")
                    else:
                        output_list.str = output_list.str + "T O T A L " +\
                            to_string(tot_saldo, " ->>>,>>>,>>>,>>9") +\
                            fill(" ", 78) +\
                            to_string(tot_foreign, "   ->>>,>>>,>>>,>>9")
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    tot_saldo = to_decimal("0")
                    tot_foreign = to_decimal("0")

                if artnr != artikel.artnr:
                    t_list = T_list()
                    t_list_data.append(t_list)

                    t_list.artnr = artikel.artnr
                    t_list.bezeich = artikel.bezeich

                    if artnr != 0:
                        output_list = Output_list()
                        output_list_data.append(output_list)

                        for i in range(1, 58 + 1):
                            output_list.str = output_list.str + "   "
                        output_list.pay_amt = to_decimal(t_credit)
                        output_list.pay_famt = to_decimal(t_famt)

                        if not long_digit:
                            output_list.str = output_list.str + "Sub-Total " +\
                                to_string(t_credit, "->,>>>,>>>,>>9.99") +\
                                fill(" ", 78) +\
                                to_string(t_famt, "->>,>>>,>>>,>>9.99")
                        else:
                            output_list.str = output_list.str + "Sub-Total " +\
                                to_string(t_credit, " ->>>,>>>,>>>,>>9") +\
                                fill(" ", 78) +\
                                to_string(t_famt, "  ->>>,>>>,>>>,>>9")
                        output_list = Output_list()
                        output_list_data.append(output_list)

                        t_credit = to_decimal("0")
                        t_famt = to_decimal("0")
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    for i in range(1, 19 + 1):
                        output_list.str = output_list.str + " "
                    output_list.str = output_list.str +\
                        to_string(artikel.artnr, ">>>>9") + " - " +\
                        to_string(artikel.bezeich, "x(34)")
                    artnr = artikel.artnr
                t_list.betrag = to_decimal(
                    t_list.betrag) - to_decimal(debitor.saldo)

                if guest.name != None:
                    temp_name = guest.name

                else:
                    temp_name = ""

                if guest.vorname1 != None:
                    temp_vorname1 = guest.vorname1

                else:
                    temp_vorname1 = ""

                if guest.anredefirma != None:
                    temp_anredefirma = guest.anredefirma

                else:
                    temp_anredefirma = ""

                if guest.anrede1 != None:
                    temp_anrede1 = guest.anrede1

                else:
                    temp_anrede1 = ""
                receiver = substring(f"{temp_name}, {temp_vorname1} {temp_anredefirma}{temp_anrede1}", 0, 32)
                output_list = Output_list()
                output_list_data.append(output_list)

                output_list.bill_art = artikel.artnr
                output_list.debt_counter = debitor.counter
                output_list.famt = to_string(
                    debt.vesrdep, "->>,>>>,>>>,>>9.99")

                output_list.pay_amt = to_decimal(debitor.saldo)
                output_list.pay_famt = to_decimal(debitor.vesrdep)

                if not long_digit:
                    output_list.str = to_string(debt.rgdatum) +\
                        to_string(debitor.rechnr, ">>>,>>>,>>9") +\
                        to_string(receiver, "x(32)") +\
                        to_string(debt.saldo, "->,>>>,>>>,>>9.99") +\
                        to_string(debitor.saldo, "->,>>>,>>>,>>9.99") +\
                        to_string(art.bezeich, "x(34)") +\
                        to_string(debitor.rgdatum)
                else:
                    output_list.str = to_string(debt.rgdatum) +\
                        to_string(debitor.rechnr, ">>>,>>>,>>9") +\
                        to_string(receiver, "x(32)") +\
                        to_string(debt.saldo, " ->>>,>>>,>>>,>>9") +\
                        to_string(debitor.saldo, " ->>>,>>>,>>>,>>9") +\
                        to_string(art.bezeich, "x(34)") +\
                        to_string(debitor.rgdatum)

                if show_inv:

                    bill = get_cache(Bill, {"rechnr": [(eq, debitor.rechnr)]})

                    if bill:
                        output_list.inv_no = to_string(
                            bill.rechnr2, ">>>>>>>>>")

                        if bill.billref != 0:
                            output_list.soa_inv = "INV" + \
                                to_string(bill.billref, "9999999")
                    else:

                        bdebitor = get_cache(
                            Debitor, {"rechnr": [(eq, debitor.rechnr)], "debref": [(gt, 0)]})

                        if bdebitor:
                            output_list.soa_inv = "INV" + \
                                to_string(debitor.debref, "9999999")

                output_list.bill_num = debitor.rechnr
                output_list.art_bezeich = artikel.bezeich
                output_list.tbetrag = to_decimal(
                    output_list.tbetrag) - to_decimal(debitor.saldo)

                bguest = get_cache(
                    Guest, {"gastnr": [(eq, debitor.gastnrmember)]})

                if bguest:
                    output_list.gastname = substring(f"{bguest.name}, {bguest.vorname1}{bguest.anredefirma} {bguest.anrede1}", 0, 32)

                bediener = get_cache(
                    Bediener, {"nr": [(eq, debitor.bediener_nr)]})

                if bediener:
                    output_list.str = output_list.str + \
                        to_string(bediener.userinit, "x(3)")
                else:
                    output_list.str = output_list.str + "   "
                output_list.str = output_list.str + to_string(debitor.vesrcod, "x(34)")
                output_list.str = output_list.str + to_string(" ", "x(22)")

                t_guest = get_cache(
                    Guest, {"gastnr": [(eq, debt.gastnrmember)]})

                if t_guest:
                    tstr = substring(f"{t_guest.name}, {t_guest.vorname1}{t_guest.anrede1}", 0, 34)
                else:
                    tstr = " "
                output_list.str = output_list.str + to_string(tstr, "x(50)")
                output_list.str = output_list.str + to_string(debitor.vesrdep, "->,>>>,>>>,>>9.99")
                output_list.str = output_list.str + to_string(debitor.zahlkonto, ">>>>9")
                output_list.str = output_list.str + to_string(debitor.vesrdep, "->,>>>,>>>,>>9.99")
                output_list.str = output_list.str + to_string(artikel.bezeich, "x(40)")

                t_credit = to_decimal(t_credit) + to_decimal(debitor.saldo)
                t_famt = to_decimal(t_famt) + to_decimal(debitor.vesrdep)
                tot_credit = to_decimal(tot_credit) + to_decimal(debitor.saldo)
                tot_saldo = to_decimal(tot_saldo) + to_decimal(debitor.saldo)
                tot_foreign = to_decimal(
                    tot_foreign) + to_decimal(debitor.vesrdep)
                tot_famt = to_decimal(tot_famt) + to_decimal(debitor.vesrdep)

                s_list = query(s_list_data, filters=(
                    lambda s_list: s_list.artnr == art.artnr), first=True)

                if not s_list:
                    s_list = S_list()
                    s_list_data.append(s_list)

                    s_list.artnr = art.artnr
                    s_list.bezeich = art.bezeich
                s_list.betrag = to_decimal(
                    s_list.betrag) + to_decimal(debitor.saldo)
        output_list = Output_list()
        output_list_data.append(output_list)

        for i in range(1, 58 + 1):
            output_list.str = output_list.str + "   "
        output_list.pay_amt = to_decimal(tot_saldo)
        output_list.pay_famt = to_decimal(tot_foreign)

        if not long_digit:
            output_list.str = output_list.str + "T O T A L " +\
                to_string(tot_saldo, "->,>>>,>>>,>>9.99") +\
                fill(" ", 78) +\
                to_string(tot_foreign, " ->>,>>>,>>>,>>9.99")
        else:
            output_list.str = output_list.str + "T O T A L " +\
                to_string(tot_saldo, " ->>>,>>>,>>>,>>9") +\
                fill(" ", 78) +\
                to_string(tot_foreign, "   ->>>,>>>,>>>,>>9")
        output_list = Output_list()
        output_list_data.append(output_list)

        output_list = Output_list()
        output_list_data.append(output_list)

        for i in range(1, 58 + 1):
            output_list.str = output_list.str + "   "
        output_list.pay_amt = to_decimal(t_credit)
        output_list.pay_famt = to_decimal(t_famt)

        if not long_digit:
            output_list.str = output_list.str + "Sub-Total " +\
                to_string(t_credit, "->,>>>,>>>,>>9.99") +\
                fill(" ", 78) +\
                to_string(t_famt, "->>,>>>,>>>,>>9.99")
        else:
            output_list.str = output_list.str + "Sub-Total " +\
                to_string(t_credit, " ->>>,>>>,>>>,>>9") +\
                fill(" ", 78) +\
                to_string(t_famt, "  ->>>,>>>,>>>,>>9")
        output_list = Output_list()
        output_list_data.append(output_list)

        output_list = Output_list()
        output_list_data.append(output_list)

        for i in range(1, 56 + 1):
            output_list.str = output_list.str + " "
        output_list.pay_amt = to_decimal(tot_credit)
        output_list.pay_famt = to_decimal(tot_famt)

        if not long_digit:
            output_list.str = output_list.str + "Grand TOTAL " +\
                to_string(tot_credit, "->,>>>,>>>,>>9.99") +\
                fill(" ", 78) +\
                to_string(tot_famt, "->>,>>>,>>>,>>9.99")
        else:
            output_list.str = output_list.str + "Grand TOTAL " +\
                to_string(tot_credit, " ->>>,>>>,>>>,>>9") +\
                fill(" ", 78) +\
                to_string(tot_famt, "->>,>>>,>>>,>>9.99")

    def create_list1b():
        nonlocal r_no, s_list_data, t_list_data, t_ar_paylist_data, long_digit, htparam, guest, debitor, artikel, bill, bediener, waehrung
        nonlocal comment, cledger, ccard, last_sort, from_date, to_date, from_art, to_art, mi_payment, mi_transfer, show_inv, bill_name, bill_nr
        nonlocal bguest, bdebitor
        nonlocal s_list, t_list, output_list, t_ar_paylist, bguest, bdebitor, tbuff, bq
        nonlocal s_list_data, t_list_data, output_list_data, t_ar_paylist_data

        artnr: int = 0
        i: int = 0
        curr_gastnr: int = 0
        t_credit: Decimal = to_decimal("0.0")
        tot_credit: Decimal = to_decimal("0.0")
        t_famt: Decimal = to_decimal("0.0")
        tot_famt: Decimal = to_decimal("0.0")
        tot_saldo: Decimal = to_decimal("0.0")
        tot_foreign: Decimal = to_decimal("0.0")
        receiver: string = ""
        do_it: bool = False
        temp_name: string = ""
        temp_vorname1: string = ""
        temp_anredefirma: string = ""
        temp_anrede1: string = ""
        debt = None
        art = None
        t_guest = None
        tstr: string = ""
        Debt = create_buffer("Debt", Debitor)
        Art = create_buffer("Art", Artikel)
        T_guest = create_buffer("T_guest", Guest)

        debitor_obj_list = {}
        debitor = Debitor()
        debt = Debitor()
        artikel = Artikel()
        art = Artikel()
        guest = Guest()
        for debitor.gastnr, debitor.saldo, debitor.zahlkonto, debitor.betriebsnr, debitor.counter, debitor.rechnr, debitor.debref, debitor.rgdatum, debitor.gastnrmember, debitor.bediener_nr, debitor.vesrcod, debitor.vesrdep, debitor.betrieb_gastmem, debitor._recid, debt.gastnr, debt.saldo, debt.zahlkonto, debt.betriebsnr, debt.counter, debt.rechnr, debt.debref, debt.rgdatum, debt.gastnrmember, debt.bediener_nr, debt.vesrcod, debt.vesrdep, debt.betrieb_gastmem, debt._recid, artikel.artnr, artikel.bezeich, artikel.artart, artikel._recid, art.artnr, art.bezeich, art.artart, art._recid, guest.name, guest.vorname1, guest.anredefirma, guest.anrede1, guest._recid in db_session.query(Debitor.gastnr, Debitor.saldo, Debitor.zahlkonto, Debitor.betriebsnr, Debitor.counter, Debitor.rechnr, Debitor.debref, Debitor.rgdatum, Debitor.gastnrmember, Debitor.bediener_nr, Debitor.vesrcod, Debitor.vesrdep, Debitor.betrieb_gastmem, Debitor._recid, Debt.gastnr, Debt.saldo, Debt.zahlkonto, Debt.betriebsnr, Debt.counter, Debt.rechnr, Debt.debref, Debt.rgdatum, Debt.gastnrmember, Debt.bediener_nr, Debt.vesrcod, Debt.vesrdep, Debt.betrieb_gastmem, Debt._recid, Artikel.artnr, Artikel.bezeich, Artikel.artart, Artikel._recid, Art.artnr, Art.bezeich, Art.artart, Art._recid, Guest.name, Guest.vorname1, Guest.anredefirma, Guest.anrede1, Guest._recid).join(Debt, (Debt.counter == Debitor.counter) & (Debt.zahlkonto == 0)).join(Artikel, (Artikel.artnr == Debitor.artnr) & (Artikel.departement == 0)).join(Art, (Art.artnr == Debitor.zahlkonto) & (Art.departement == 0)).join(Guest, (Guest.gastnr == Debitor.gastnr)).filter(
                (Debitor.rgdatum >= from_date) & (Debitor.rgdatum <= to_date) & (Debitor.zahlkonto > 0) & (Debitor.artnr >= from_art) & (Debitor.artnr <= to_art) & (Debitor.counter > 0) & (Debitor.opart > 0)).order_by(Artikel.artnr, Debt.rgdatum, Debitor.name, Debitor.zahlkonto, Debitor.rechnr).all():
            if debitor_obj_list.get(debitor._recid):
                continue
            else:
                debitor_obj_list[debitor._recid] = True

            do_it = True

            if mi_payment:

                if artikel.artart == 2 and art.artart != 4 and art.artart != 7:
                    do_it = False

                elif artikel.artart == 7 and art.artart != 4:
                    do_it = False

            elif mi_transfer:

                if artikel.artart == 2 and (art.artart == 4 or art.artart == 7):
                    do_it = False

                elif artikel.artart == 7 and art.artart == 4:
                    do_it = False

            if do_it and (bill_name != "") and (substring(bill_name, 0, 1) != ("*").lower()):

                if not matches(guest.name, r"*" + bill_name + r"*"):
                    do_it = False

            if do_it and (bill_name != "") and (substring(bill_name, 0, 1) == ("*").lower()):

                if not matches(guest.name, bill_name):
                    do_it = False

            if do_it:

                if curr_gastnr == 0:
                    curr_gastnr = debitor.gastnr

                if curr_gastnr != debitor.gastnr:
                    curr_gastnr = debitor.gastnr
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    for i in range(1, 58 + 1):
                        output_list.str = output_list.str + "   "
                    output_list.pay_amt = to_decimal(tot_saldo)
                    output_list.pay_famt = to_decimal(tot_foreign)

                    if not long_digit:
                        output_list.str = output_list.str + "T O T A L " +\
                            to_string(tot_saldo, "->,>>>,>>>,>>9.99") +\
                            fill(" ", 78) +\
                            to_string(tot_foreign, " ->>,>>>,>>>,>>9.99")
                    else:
                        output_list.str = output_list.str + "T O T A L " +\
                            to_string(tot_saldo, " ->>>,>>>,>>>,>>9") +\
                            fill(" ", 78) +\
                            to_string(tot_foreign, "   ->>>,>>>,>>>,>>9")
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    tot_saldo = to_decimal("0")
                    tot_foreign = to_decimal("0")

                if artnr != artikel.artnr:
                    t_list = T_list()
                    t_list_data.append(t_list)

                    t_list.artnr = artikel.artnr
                    t_list.bezeich = artikel.bezeich

                    if artnr != 0:
                        output_list = Output_list()
                        output_list_data.append(output_list)

                        for i in range(1, 58 + 1):
                            output_list.str = output_list.str + "   "
                        output_list.pay_amt = to_decimal(t_credit)
                        output_list.pay_famt = to_decimal(t_famt)

                        if not long_digit:
                            output_list.str = output_list.str + "Sub-Total " +\
                                to_string(t_credit, "->,>>>,>>>,>>9.99") +\
                                fill(" ", 78) +\
                                to_string(t_famt, "->>,>>>,>>>,>>9.99")
                        else:
                            output_list.str = output_list.str + "Sub-Total " +\
                                to_string(t_credit, " ->>>,>>>,>>>,>>9") +\
                                fill(" ", 78) +\
                                to_string(t_famt, "  ->>>,>>>,>>>,>>9")
                        output_list = Output_list()
                        output_list_data.append(output_list)

                        t_credit = to_decimal("0")
                        t_famt = to_decimal("0")
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    for i in range(1, 19 + 1):
                        output_list.str = output_list.str + " "
                    output_list.str = output_list.str +\
                        to_string(artikel.artnr, ">>>>9") + " - " +\
                        to_string(artikel.bezeich, "x(24)")
                    artnr = artikel.artnr
                t_list.betrag = to_decimal(
                    t_list.betrag) - to_decimal(debitor.saldo)

                if guest.name != None:
                    temp_name = guest.name

                else:
                    temp_name = ""

                if guest.vorname1 != None:
                    temp_vorname1 = guest.vorname1

                else:
                    temp_vorname1 = ""

                if guest.anredefirma != None:
                    temp_anredefirma = guest.anredefirma

                else:
                    temp_anredefirma = ""

                if guest.anrede1 != None:
                    temp_anrede1 = guest.anrede1

                else:
                    temp_anrede1 = ""
                receiver = substring(f"{temp_name}, {temp_vorname1} {temp_anredefirma}{temp_anrede1}", 0, 32)
                output_list = Output_list()
                output_list_data.append(output_list)

                output_list.flag = 1
                output_list.artnr = debitor.zahlkonto
                output_list.pay_amt = to_decimal(debitor.saldo)
                output_list.pay_count = debitor.betriebsnr
                output_list.bill_art = artikel.artnr
                output_list.debt_counter = debitor.Counter
                output_list.famt = to_string(
                    debt.vesrdep, "->>,>>>,>>>,>>9.99")
                output_list.pay_famt = to_decimal(debt.vesrdep)

                if show_inv:

                    bill = get_cache(Bill, {"rechnr": [(eq, debitor.rechnr)]})

                    if bill:
                        output_list.inv_no = to_string(
                            bill.rechnr2, ">>>>>>>>>")

                        if bill.billref != 0:
                            output_list.soa_inv = "INV" + \
                                to_string(bill.billref, "9999999")
                    else:

                        bdebitor = get_cache(
                            Debitor, {"rechnr": [(eq, debitor.rechnr)], "debref": [(gt, 0)]})

                        if bdebitor:
                            output_list.soa_inv = "INV" + \
                                to_string(debitor.debref, "9999999")

                if not long_digit:
                    output_list.str = to_string(debt.rgdatum) +\
                        to_string(debitor.rechnr, ">>>,>>>,>>9") +\
                        to_string(receiver, "x(32)") +\
                        to_string(debt.saldo, "->,>>>,>>>,>>9.99") +\
                        to_string(debitor.saldo, "->,>>>,>>>,>>9.99") +\
                        to_string(art.bezeich, "x(34)") +\
                        to_string(debitor.rgdatum)
                else:
                    output_list.str = to_string(debt.rgdatum) +\
                        to_string(debitor.rechnr, ">>>,>>>,>>9") +\
                        to_string(receiver, "x(32)") +\
                        to_string(debt.saldo, " ->>>,>>>,>>>,>>9") +\
                        to_string(debitor.saldo, " ->>>,>>>,>>>,>>9") +\
                        to_string(art.bezeich, "x(34)") +\
                        to_string(debitor.rgdatum)
                output_list.bill_num = debitor.rechnr
                output_list.art_bezeich = artikel.bezeich
                output_list.tbetrag = to_decimal(
                    output_list.tbetrag) - to_decimal(debitor.saldo)

                bguest = get_cache(
                    Guest, {"gastnr": [(eq, debitor.gastnrmember)]})

                if bguest:
                    output_list.gastname = substring(f"{bguest.name}, {bguest.vorname1}{bguest.anredefirma} {bguest.anrede1}", 0, 32)

                bediener = get_cache(
                    Bediener, {"nr": [(eq, debitor.bediener_nr)]})

                if bediener:
                    output_list.str = output_list.str + \
                        to_string(bediener.userinit, "x(3)")
                else:
                    output_list.str = output_list.str + "   "
                output_list.str = output_list.str + \
                    to_string(debitor.vesrcod, "x(34)")
                t_credit = to_decimal(t_credit) + to_decimal(debitor.saldo)
                t_famt = to_decimal(t_famt) + to_decimal(debitor.vesrdep)
                tot_credit = to_decimal(tot_credit) + to_decimal(debitor.saldo)
                tot_saldo = to_decimal(tot_saldo) + to_decimal(debitor.saldo)
                tot_foreign = to_decimal(
                    tot_foreign) + to_decimal(debitor.vesrdep)
                tot_famt = to_decimal(tot_famt) + to_decimal(debitor.vesrdep)

                s_list = query(s_list_data, filters=(
                    lambda s_list: s_list.artnr == art.artnr), first=True)

                if not s_list:
                    s_list = S_list()
                    s_list_data.append(s_list)

                    s_list.artnr = art.artnr
                    s_list.bezeich = art.bezeich
                output_list.str = output_list.str + \
                    to_string(debitor.vesrdep, "->>,>>>,>>>,>>9.99")

                waehrung = get_cache(
                    Waehrung, {"waehrungsnr": [(eq, debitor.betrieb_gastmem)]})

                if waehrung:
                    output_list.str = output_list.str + \
                        to_string(waehrung.wabkurz, "x(4)")
                else:
                    output_list.str = output_list.str + "   "

                t_guest = get_cache(
                    Guest, {"gastnr": [(eq, debt.gastnrmember)]})

                if t_guest:
                    tstr = substring(f"{t_guest.name}, {t_guest.vorname1}{t_guest.anrede1}", 0, 34)
                else:
                    tstr = " "
                output_list.str = output_list.str + to_string(tstr, "x(50)")
                output_list.str = output_list.str + \
                    to_string(debitor.vesrdep, "->,>>>,>>>,>>9.99")
                output_list.str = output_list.str + \
                    to_string(debitor.zahlkonto, ">>>>9")
                output_list.str = output_list.str + \
                    to_string(debitor.vesrdep, "->,>>>,>>>,>>9.99")
                output_list.str = output_list.str + \
                    to_string(artikel.bezeich, "x(40)")

                s_list.betrag = to_decimal(
                    s_list.betrag) + to_decimal(debitor.saldo)
        output_list = Output_list()
        output_list_data.append(output_list)

        for i in range(1, 58 + 1):
            output_list.str = output_list.str + "   "
        output_list.pay_amt = to_decimal(tot_saldo)
        output_list.pay_famt = to_decimal(tot_foreign)

        if not long_digit:
            output_list.str = output_list.str + "T O T A L " +\
                to_string(tot_saldo, "->,>>>,>>>,>>9.99") +\
                fill(" ", 78) +\
                to_string(tot_foreign, " ->>,>>>,>>>,>>9.99")
        else:
            output_list.str = output_list.str + "T O T A L " +\
                to_string(tot_saldo, " ->>>,>>>,>>>,>>9") +\
                fill(" ", 78) +\
                to_string(tot_foreign, "   ->>>,>>>,>>>,>>9")
        output_list = Output_list()
        output_list_data.append(output_list)

        output_list = Output_list()
        output_list_data.append(output_list)

        for i in range(1, 58 + 1):
            output_list.str = output_list.str + "   "
        output_list.pay_amt = to_decimal(t_credit)
        output_list.pay_famt = to_decimal(t_famt)

        if not long_digit:
            output_list.str = output_list.str + "Sub-Total " +\
                to_string(t_credit, "->,>>>,>>>,>>9.99") +\
                fill(" ", 78) +\
                to_string(t_famt, "->>,>>>,>>>,>>9.99")
        else:
            output_list.str = output_list.str + "Sub-Total " +\
                to_string(t_credit, " ->>>,>>>,>>>,>>9") +\
                fill(" ", 78) +\
                to_string(t_famt, "  ->>>,>>>,>>>,>>9")
        output_list = Output_list()
        output_list_data.append(output_list)

        output_list = Output_list()
        output_list_data.append(output_list)

        for i in range(1, 56 + 1):
            output_list.str = output_list.str + " "
        output_list.pay_amt = to_decimal(tot_credit)
        output_list.pay_famt = to_decimal(tot_famt)

        if not long_digit:
            output_list.str = output_list.str + "Grand TOTAL " +\
                to_string(tot_credit, "->,>>>,>>>,>>9.99") +\
                fill(" ", 78) +\
                to_string(tot_famt, "->>,>>>,>>>,>>9.99")
        else:
            output_list.str = output_list.str + "Grand TOTAL " +\
                to_string(tot_credit, " ->>>,>>>,>>>,>>9") +\
                fill(" ", 78) +\
                to_string(tot_famt, "  ->>>,>>>,>>>,>>9")
        create_tot_payment()

    def create_list1c():

        nonlocal r_no, s_list_data, t_list_data, t_ar_paylist_data, long_digit, htparam, guest, debitor, artikel, bill, bediener, waehrung
        nonlocal comment, cledger, ccard, last_sort, from_date, to_date, from_art, to_art, mi_payment, mi_transfer, show_inv, bill_name, bill_nr
        nonlocal bguest, bdebitor

        nonlocal s_list, t_list, output_list, t_ar_paylist, bguest, bdebitor, tbuff, bq
        nonlocal s_list_data, t_list_data, output_list_data, t_ar_paylist_data

        artnr: int = 0
        i: int = 0
        curr_gastnr: int = 0
        t_credit: Decimal = to_decimal("0.0")
        tot_credit: Decimal = to_decimal("0.0")
        t_famt: Decimal = to_decimal("0.0")
        tot_famt: Decimal = to_decimal("0.0")
        tot_saldo: Decimal = to_decimal("0.0")
        tot_foreign: Decimal = to_decimal("0.0")
        receiver: string = ""
        do_it: bool = False
        temp_name: string = ""
        temp_vorname1: string = ""
        temp_anredefirma: string = ""
        temp_anrede1: string = ""
        debt = None
        art = None
        t_guest = None
        tstr: string = ""
        Debt = create_buffer("Debt", Debitor)
        Art = create_buffer("Art", Artikel)
        T_guest = create_buffer("T_guest", Guest)

        debitor_obj_list = {}
        debitor = Debitor()
        debt = Debitor()
        artikel = Artikel()
        art = Artikel()
        guest = Guest()
        for debitor.gastnr, debitor.saldo, debitor.zahlkonto, debitor.betriebsnr, debitor.counter, debitor.rechnr, debitor.debref, debitor.rgdatum, debitor.gastnrmember, debitor.bediener_nr, debitor.vesrcod, debitor.vesrdep, debitor.betrieb_gastmem, debitor._recid, debt.gastnr, debt.saldo, debt.zahlkonto, debt.betriebsnr, debt.counter, debt.rechnr, debt.debref, debt.rgdatum, debt.gastnrmember, debt.bediener_nr, debt.vesrcod, debt.vesrdep, debt.betrieb_gastmem, debt._recid, artikel.artnr, artikel.bezeich, artikel.artart, artikel._recid, art.artnr, art.bezeich, art.artart, art._recid, guest.name, guest.vorname1, guest.anredefirma, guest.anrede1, guest._recid in db_session.query(Debitor.gastnr, Debitor.saldo, Debitor.zahlkonto, Debitor.betriebsnr, Debitor.counter, Debitor.rechnr, Debitor.debref, Debitor.rgdatum, Debitor.gastnrmember, Debitor.bediener_nr, Debitor.vesrcod, Debitor.vesrdep, Debitor.betrieb_gastmem, Debitor._recid, Debt.gastnr, Debt.saldo, Debt.zahlkonto, Debt.betriebsnr, Debt.counter, Debt.rechnr, Debt.debref, Debt.rgdatum, Debt.gastnrmember, Debt.bediener_nr, Debt.vesrcod, Debt.vesrdep, Debt.betrieb_gastmem, Debt._recid, Artikel.artnr, Artikel.bezeich, Artikel.artart, Artikel._recid, Art.artnr, Art.bezeich, Art.artart, Art._recid, Guest.name, Guest.vorname1, Guest.anredefirma, Guest.anrede1, Guest._recid).join(Debt, (Debt.counter == Debitor.counter) & (Debt.zahlkonto == 0)).join(Artikel, (Artikel.artnr == Debitor.artnr) & (Artikel.departement == 0)).join(Art, (Art.artnr == Debitor.zahlkonto) & (Art.departement == 0)).join(Guest, (Guest.gastnr == Debitor.gastnr)).filter(
                (Debitor.rgdatum >= from_date) & (Debitor.rgdatum <= to_date) & (Debitor.zahlkonto > 0) & (Debitor.artnr >= from_art) & (Debitor.artnr <= to_art) & (Debitor.counter > 0) & (Debitor.opart > 0)).order_by(Artikel.artnr, Debitor.rechnr, Debitor.name, Debitor.rgdatum, Debitor.zahlkonto).all():
            if debitor_obj_list.get(debitor._recid):
                continue
            else:
                debitor_obj_list[debitor._recid] = True

            do_it = True

            if mi_payment:

                if artikel.artart == 2 and art.artart != 4 and art.artart != 7:
                    do_it = False

                elif artikel.artart == 7 and art.artart != 4:
                    do_it = False

            elif mi_transfer:

                if artikel.artart == 2 and (art.artart == 4 or art.artart == 7):
                    do_it = False

                elif artikel.artart == 7 and art.artart == 4:
                    do_it = False

            if do_it and (bill_name != "") and (substring(bill_name, 0, 1) != ("*").lower()):

                if not matches(guest.name, r"*" + bill_name + r"*"):
                    do_it = False

            if do_it and (bill_name != "") and (substring(bill_name, 0, 1) == ("*").lower()):

                if not matches(guest.name, bill_name):
                    do_it = False

            if do_it:

                if curr_gastnr == 0:
                    curr_gastnr = debitor.gastnr

                if curr_gastnr != debitor.gastnr:
                    curr_gastnr = debitor.gastnr
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    for i in range(1, 58 + 1):
                        output_list.str = output_list.str + "   "
                    output_list.pay_amt = to_decimal(tot_saldo)
                    output_list.pay_famt = to_decimal(tot_foreign)

                    if not long_digit:
                        output_list.str = output_list.str + "T O T A L " +\
                            to_string(tot_saldo, "->,>>>,>>>,>>9.99") +\
                            fill(" ", 78) +\
                            to_string(tot_foreign, " ->>,>>>,>>>,>>9.99")
                    else:
                        output_list.str = output_list.str + "T O T A L " +\
                            to_string(tot_saldo, " ->>>,>>>,>>>,>>9") +\
                            fill(" ", 78) +\
                            to_string(tot_foreign, "   ->>>,>>>,>>>,>>9")
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    tot_saldo = to_decimal("0")
                    tot_foreign = to_decimal("0")

                if artnr != artikel.artnr:
                    t_list = T_list()
                    t_list_data.append(t_list)

                    t_list.artnr = artikel.artnr
                    t_list.bezeich = artikel.bezeich

                    if artnr != 0:
                        output_list = Output_list()
                        output_list_data.append(output_list)

                        for i in range(1, 58 + 1):
                            output_list.str = output_list.str + "   "
                        output_list.pay_amt = to_decimal(t_credit)
                        output_list.pay_famt = to_decimal(t_famt)

                        if not long_digit:
                            output_list.str = output_list.str + "Sub-Total " +\
                                to_string(t_credit, "->,>>>,>>>,>>9.99") +\
                                fill(" ", 78) +\
                                to_string(t_famt, "->>,>>>,>>>,>>9.99")
                        else:
                            output_list.str = output_list.str + "Sub-Total " +\
                                to_string(t_credit, " ->>>,>>>,>>>,>>9") +\
                                fill(" ", 78) +\
                                to_string(t_famt, "  ->>>,>>>,>>>,>>9")
                        output_list = Output_list()
                        output_list_data.append(output_list)

                        t_credit = to_decimal("0")
                        t_famt = to_decimal("0")
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    for i in range(1, 19 + 1):
                        output_list.str = output_list.str + " "
                    output_list.str = output_list.str +\
                        to_string(artikel.artnr, ">>>>9") + " - " +\
                        to_string(artikel.bezeich, "x(24)")
                    artnr = artikel.artnr
                t_list.betrag = to_decimal(
                    t_list.betrag) - to_decimal(debitor.saldo)

                if guest.name != None:
                    temp_name = guest.name

                else:
                    temp_name = ""

                if guest.vorname1 != None:
                    temp_vorname1 = guest.vorname1

                else:
                    temp_vorname1 = ""

                if guest.anredefirma != None:
                    temp_anredefirma = guest.anredefirma

                else:
                    temp_anredefirma = ""

                if guest.anrede1 != None:
                    temp_anrede1 = guest.anrede1

                else:
                    temp_anrede1 = ""
                receiver = substring(f"{temp_name}, {temp_vorname1} {temp_anredefirma}{temp_anrede1}", 0, 32)
                output_list = Output_list()
                output_list_data.append(output_list)

                output_list.flag = 1
                output_list.artnr = debitor.zahlkonto
                output_list.pay_amt = to_decimal(debitor.saldo)
                output_list.pay_count = debitor.betriebsnr
                output_list.bill_art = artikel.artnr
                output_list.debt_counter = debitor.counter
                output_list.famt = to_string(
                    debt.vesrdep, "->>,>>>,>>>,>>9.99")
                output_list.pay_famt = to_decimal(debt.vesrdep)

                if show_inv:

                    bill = get_cache(Bill, {"rechnr": [(eq, debitor.rechnr)]})

                    if bill:
                        output_list.inv_no = to_string(
                            bill.rechnr2, ">>>>>>>>>")

                        if bill.billref != 0:
                            output_list.soa_inv = "INV" + \
                                to_string(bill.billref, "9999999")
                    else:

                        bdebitor = get_cache(
                            Debitor, {"rechnr": [(eq, debitor.rechnr)], "debref": [(gt, 0)]})

                        if bdebitor:
                            output_list.soa_inv = "INV" + \
                                to_string(debitor.debref, "9999999")

                if not long_digit:
                    output_list.str = to_string(debt.rgdatum) +\
                        to_string(debitor.rechnr, ">>>,>>>,>>9") +\
                        to_string(receiver, "x(32)") +\
                        to_string(debt.saldo, "->,>>>,>>>,>>9.99") +\
                        to_string(debitor.saldo, "->,>>>,>>>,>>9.99") +\
                        to_string(art.bezeich, "x(34)") +\
                        to_string(debitor.rgdatum)
                else:
                    output_list.str = to_string(debt.rgdatum) +\
                        to_string(debitor.rechnr, ">>>,>>>,>>9") +\
                        to_string(receiver, "x(32)") +\
                        to_string(debt.saldo, " ->>>,>>>,>>>,>>9") +\
                        to_string(debitor.saldo, " ->>>,>>>,>>>,>>9") +\
                        to_string(art.bezeich, "x(34)") +\
                        to_string(debitor.rgdatum)
                output_list.bill_num = debitor.rechnr
                output_list.art_bezeich = artikel.bezeich
                output_list.tbetrag = to_decimal(
                    output_list.tbetrag) - to_decimal(debitor.saldo)

                bguest = get_cache(
                    Guest, {"gastnr": [(eq, debitor.gastnrmember)]})

                if bguest:
                    output_list.gastname = substring(f"{bguest.name}, {bguest.vorname1}{bguest.anredefirma} {bguest.anrede1}", 0, 32)

                bediener = get_cache(
                    Bediener, {"nr": [(eq, debitor.bediener_nr)]})

                if bediener:
                    output_list.str = output_list.str + \
                        to_string(bediener.userinit, "x(3)")
                else:
                    output_list.str = output_list.str + "   "
                output_list.str = output_list.str + \
                    to_string(debitor.vesrcod, "x(34)")
                t_credit = to_decimal(t_credit) + to_decimal(debitor.saldo)
                t_famt = to_decimal(t_famt) + to_decimal(debitor.vesrdep)
                tot_credit = to_decimal(tot_credit) + to_decimal(debitor.saldo)
                tot_saldo = to_decimal(tot_saldo) + to_decimal(debitor.saldo)
                tot_foreign = to_decimal(
                    tot_foreign) + to_decimal(debitor.vesrdep)
                tot_famt = to_decimal(tot_famt) + to_decimal(debitor.vesrdep)

                s_list = query(s_list_data, filters=(
                    lambda s_list: s_list.artnr == art.artnr), first=True)

                if not s_list:
                    s_list = S_list()
                    s_list_data.append(s_list)

                    s_list.artnr = art.artnr
                    s_list.bezeich = art.bezeich
                output_list.str = output_list.str + \
                    to_string(debitor.vesrdep, "->>,>>>,>>>,>>9.99")

                waehrung = get_cache(
                    Waehrung, {"waehrungsnr": [(eq, debitor.betrieb_gastmem)]})

                if waehrung:
                    output_list.str = output_list.str + \
                        to_string(waehrung.wabkurz, "x(4)")
                else:
                    output_list.str = output_list.str + "   "

                t_guest = get_cache(
                    Guest, {"gastnr": [(eq, debt.gastnrmember)]})

                if t_guest:
                    tstr = substring(f"{t_guest.name}, {t_guest.vorname1}{t_guest.anrede1}", 0, 34)
                else:
                    tstr = " "
                output_list.str = output_list.str + to_string(tstr, "x(50)")
                output_list.str = output_list.str + \
                    to_string(debitor.vesrdep, "->,>>>,>>>,>>9.99")
                output_list.str = output_list.str + \
                    to_string(debitor.zahlkonto, ">>>>9")
                output_list.str = output_list.str + \
                    to_string(debitor.vesrdep, "->,>>>,>>>,>>9.99")
                output_list.str = output_list.str + \
                    to_string(artikel.bezeich, "x(40)")

                s_list.betrag = to_decimal(
                    s_list.betrag) + to_decimal(debitor.saldo)
        output_list = Output_list()
        output_list_data.append(output_list)

        for i in range(1, 58 + 1):
            output_list.str = output_list.str + "   "
        output_list.pay_amt = to_decimal(tot_saldo)
        output_list.pay_famt = to_decimal(tot_foreign)

        if not long_digit:
            output_list.str = output_list.str + "T O T A L " +\
                to_string(tot_saldo, "->,>>>,>>>,>>9.99") +\
                fill(" ", 78) +\
                to_string(tot_foreign, " ->>,>>>,>>>,>>9.99")
        else:
            output_list.str = output_list.str + "T O T A L " +\
                to_string(tot_saldo, " ->>>,>>>,>>>,>>9") +\
                fill(" ", 78) +\
                to_string(tot_foreign, "   ->>>,>>>,>>>,>>9")
        output_list = Output_list()
        output_list_data.append(output_list)

        output_list = Output_list()
        output_list_data.append(output_list)

        for i in range(1, 58 + 1):
            output_list.str = output_list.str + "   "
        output_list.pay_amt = to_decimal(t_credit)
        output_list.pay_famt = to_decimal(t_famt)

        if not long_digit:
            output_list.str = output_list.str + "Sub-Total " +\
                to_string(t_credit, "->,>>>,>>>,>>9.99") +\
                fill(" ", 78) +\
                to_string(t_famt, "->>,>>>,>>>,>>9.99")
        else:
            output_list.str = output_list.str + "Sub-Total " +\
                to_string(t_credit, " ->>>,>>>,>>>,>>9") +\
                fill(" ", 78) +\
                to_string(t_famt, "  ->>>,>>>,>>>,>>9")
        output_list = Output_list()
        output_list_data.append(output_list)

        output_list = Output_list()
        output_list_data.append(output_list)

        for i in range(1, 56 + 1):
            output_list.str = output_list.str + " "
        output_list.pay_amt = to_decimal(tot_credit)
        output_list.pay_famt = to_decimal(tot_famt)

        if not long_digit:
            output_list.str = output_list.str + "Grand TOTAL " +\
                to_string(tot_credit, "->,>>>,>>>,>>9.99") +\
                fill(" ", 78) + \
                to_string(tot_famt, "->>,>>>,>>>,>>9.99")
        else:
            output_list.str = output_list.str + "Grand TOTAL " +\
                to_string(tot_credit, " ->>>,>>>,>>>,>>9") +\
                fill(" ", 78) + \
                to_string(tot_famt, "  ->>>,>>>,>>>,>>9")
        create_tot_payment()

    def create_list1d():

        nonlocal r_no, s_list_data, t_list_data, t_ar_paylist_data, long_digit, htparam, guest, debitor, artikel, bill, bediener, waehrung
        nonlocal comment, cledger, ccard, last_sort, from_date, to_date, from_art, to_art, mi_payment, mi_transfer, show_inv, bill_name, bill_nr
        nonlocal bguest, bdebitor

        nonlocal s_list, t_list, output_list, t_ar_paylist, bguest, bdebitor, tbuff, bq
        nonlocal s_list_data, t_list_data, output_list_data, t_ar_paylist_data

        artnr: int = 0
        i: int = 0
        curr_gastnr: int = 0
        t_credit: Decimal = to_decimal("0.0")
        tot_credit: Decimal = to_decimal("0.0")
        t_famt: Decimal = to_decimal("0.0")
        tot_famt: Decimal = to_decimal("0.0")
        tot_saldo: Decimal = to_decimal("0.0")
        tot_foreign: Decimal = to_decimal("0.0")
        receiver: string = ""
        do_it: bool = False
        temp_name: string = ""
        temp_vorname1: string = ""
        temp_anredefirma: string = ""
        temp_anrede1: string = ""
        debt = None
        art = None
        t_guest = None
        tstr: string = ""
        Debt = create_buffer("Debt", Debitor)
        Art = create_buffer("Art", Artikel)
        T_guest = create_buffer("T_guest", Guest)

        debitor_obj_list = {}
        debitor = Debitor()
        debt = Debitor()
        artikel = Artikel()
        art = Artikel()
        guest = Guest()
        for debitor.gastnr, debitor.saldo, debitor.zahlkonto, debitor.betriebsnr, debitor.counter, debitor.rechnr, debitor.debref, debitor.rgdatum, debitor.gastnrmember, debitor.bediener_nr, debitor.vesrcod, debitor.vesrdep, debitor.betrieb_gastmem, debitor._recid, debt.gastnr, debt.saldo, debt.zahlkonto, debt.betriebsnr, debt.counter, debt.rechnr, debt.debref, debt.rgdatum, debt.gastnrmember, debt.bediener_nr, debt.vesrcod, debt.vesrdep, debt.betrieb_gastmem, debt._recid, artikel.artnr, artikel.bezeich, artikel.artart, artikel._recid, art.artnr, art.bezeich, art.artart, art._recid, guest.name, guest.vorname1, guest.anredefirma, guest.anrede1, guest._recid in db_session.query(Debitor.gastnr, Debitor.saldo, Debitor.zahlkonto, Debitor.betriebsnr, Debitor.counter, Debitor.rechnr, Debitor.debref, Debitor.rgdatum, Debitor.gastnrmember, Debitor.bediener_nr, Debitor.vesrcod, Debitor.vesrdep, Debitor.betrieb_gastmem, Debitor._recid, Debt.gastnr, Debt.saldo, Debt.zahlkonto, Debt.betriebsnr, Debt.counter, Debt.rechnr, Debt.debref, Debt.rgdatum, Debt.gastnrmember, Debt.bediener_nr, Debt.vesrcod, Debt.vesrdep, Debt.betrieb_gastmem, Debt._recid, Artikel.artnr, Artikel.bezeich, Artikel.artart, Artikel._recid, Art.artnr, Art.bezeich, Art.artart, Art._recid, Guest.name, Guest.vorname1, Guest.anredefirma, Guest.anrede1, Guest._recid).join(Debt, (Debt.counter == Debitor.counter) & (Debt.zahlkonto == 0)).join(Artikel, (Artikel.artnr == Debitor.artnr) & (Artikel.departement == 0)).join(Art, (Art.artnr == Debitor.zahlkonto) & (Art.departement == 0)).join(Guest, (Guest.gastnr == Debitor.gastnr)).filter(
                (Debitor.rgdatum >= from_date) & (Debitor.rgdatum <= to_date) & (Debitor.zahlkonto > 0) & (Debitor.artnr >= from_art) & (Debitor.artnr <= to_art) & (Debitor.counter > 0) & (Debitor.opart > 0)).order_by(Artikel.artnr, Debitor.vesrcod, Debitor.name, Debitor.rgdatum, Debitor.zahlkonto, Debitor.rechnr).all():
            if debitor_obj_list.get(debitor._recid):
                continue
            else:
                debitor_obj_list[debitor._recid] = True

            do_it = True

            if mi_payment:

                if artikel.artart == 2 and art.artart != 4 and art.artart != 7:
                    do_it = False

                elif artikel.artart == 7 and art.artart != 4:
                    do_it = False

            elif mi_transfer:

                if artikel.artart == 2 and (art.artart == 4 or art.artart == 7):
                    do_it = False

                elif artikel.artart == 7 and art.artart == 4:
                    do_it = False

            if do_it and (bill_name != "") and (substring(bill_name, 0, 1) != ("*").lower()):

                if not matches(guest.name, r"*" + bill_name + r"*"):
                    do_it = False

            if do_it and (bill_name != "") and (substring(bill_name, 0, 1) == ("*").lower()):

                if not matches(guest.name, bill_name):
                    do_it = False

            if do_it:

                if curr_gastnr == 0:
                    curr_gastnr = debitor.gastnr

                if curr_gastnr != debitor.gastnr:
                    curr_gastnr = debitor.gastnr
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    for i in range(1, 58 + 1):
                        output_list.str = output_list.str + "   "
                    output_list.pay_amt = to_decimal(tot_saldo)
                    output_list.pay_famt = to_decimal(tot_foreign)

                    if not long_digit:
                        output_list.str = output_list.str + "T O T A L " +\
                            to_string(tot_saldo, "->,>>>,>>>,>>9.99") +\
                            fill(" ", 78) +\
                            to_string(tot_foreign, " ->>,>>>,>>>,>>9.99")
                    else:
                        output_list.str = output_list.str + "T O T A L " +\
                            to_string(tot_saldo, " ->>>,>>>,>>>,>>9") +\
                            fill(" ", 78) +\
                            to_string(tot_foreign, "   ->>>,>>>,>>>,>>9")
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    tot_saldo = to_decimal("0")
                    tot_foreign = to_decimal("0")

                if artnr != artikel.artnr:
                    t_list = T_list()
                    t_list_data.append(t_list)

                    t_list.artnr = artikel.artnr
                    t_list.bezeich = artikel.bezeich

                    if artnr != 0:
                        output_list = Output_list()
                        output_list_data.append(output_list)

                        for i in range(1, 58 + 1):
                            output_list.str = output_list.str + "   "
                        output_list.pay_amt = to_decimal(t_credit)
                        output_list.pay_famt = to_decimal(t_famt)

                        if not long_digit:
                            output_list.str = output_list.str + "Sub-Total " +\
                                to_string(t_credit, "->,>>>,>>>,>>9.99") +\
                                fill(" ", 78) +\
                                to_string(t_famt, "->>,>>>,>>>,>>9.99")
                        else:
                            output_list.str = output_list.str + "Sub-Total " +\
                                to_string(t_credit, " ->>>,>>>,>>>,>>9") +\
                                fill(" ", 78) +\
                                to_string(t_famt, "  ->>>,>>>,>>>,>>9")
                        output_list = Output_list()
                        output_list_data.append(output_list)

                        t_credit = to_decimal("0")
                        t_famt = to_decimal("0")
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    for i in range(1, 19 + 1):
                        output_list.str = output_list.str + " "
                    output_list.str = output_list.str +\
                        to_string(artikel.artnr, ">>>>9") + " - " +\
                        to_string(artikel.bezeich, "x(24)")
                    artnr = artikel.artnr
                t_list.betrag = to_decimal(
                    t_list.betrag) - to_decimal(debitor.saldo)

                if guest.name != None:
                    temp_name = guest.name

                else:
                    temp_name = ""

                if guest.vorname1 != None:
                    temp_vorname1 = guest.vorname1

                else:
                    temp_vorname1 = ""

                if guest.anredefirma != None:
                    temp_anredefirma = guest.anredefirma

                else:
                    temp_anredefirma = ""

                if guest.anrede1 != None:
                    temp_anrede1 = guest.anrede1

                else:
                    temp_anrede1 = ""
                receiver = substring(f"{temp_name}, {temp_vorname1} {temp_anredefirma}{temp_anrede1}", 0, 32)
                output_list = Output_list()
                output_list_data.append(output_list)

                output_list.flag = 1
                output_list.artnr = debitor.zahlkonto
                output_list.pay_amt = to_decimal(debitor.saldo)
                output_list.pay_count = debitor.betriebsnr
                output_list.bill_art = artikel.artnr
                output_list.debt_counter = debitor.counter
                output_list.famt = to_string(
                    debt.vesrdep, "->>,>>>,>>>,>>9.99")
                output_list.pay_famt = to_decimal(debt.vesrdep)

                if show_inv:

                    bill = get_cache(Bill, {"rechnr": [(eq, debitor.rechnr)]})

                    if bill:
                        output_list.inv_no = to_string(
                            bill.rechnr2, ">>>>>>>>>")

                        if bill.billref != 0:
                            output_list.soa_inv = "INV" + \
                                to_string(bill.billref, "9999999")
                    else:

                        bdebitor = get_cache(
                            Debitor, {"rechnr": [(eq, debitor.rechnr)], "debref": [(gt, 0)]})

                        if bdebitor:
                            output_list.soa_inv = "INV" + \
                                to_string(debitor.debref, "9999999")

                if not long_digit:
                    output_list.str = to_string(debt.rgdatum) +\
                        to_string(debitor.rechnr, ">>>,>>>,>>9") +\
                        to_string(receiver, "x(32)") +\
                        to_string(debt.saldo, "->,>>>,>>>,>>9.99") +\
                        to_string(debitor.saldo, "->,>>>,>>>,>>9.99") +\
                        to_string(art.bezeich, "x(34)") +\
                        to_string(debitor.rgdatum)
                else:
                    output_list.str = to_string(debt.rgdatum) +\
                        to_string(debitor.rechnr, ">>>,>>>,>>9") +\
                        to_string(receiver, "x(32)") +\
                        to_string(debt.saldo, " ->>>,>>>,>>>,>>9") +\
                        to_string(debitor.saldo, " ->>>,>>>,>>>,>>9") +\
                        to_string(art.bezeich, "x(34)") +\
                        to_string(debitor.rgdatum)
                output_list.bill_num = debitor.rechnr
                output_list.art_bezeich = artikel.bezeich
                output_list.tbetrag = to_decimal(
                    output_list.tbetrag) - to_decimal(debitor.saldo)

                bguest = get_cache(
                    Guest, {"gastnr": [(eq, debitor.gastnrmember)]})

                if bguest:
                    output_list.gastname = substring(f"{bguest.name}, {bguest.vorname1}{bguest.anredefirma} {bguest.anrede1}", 0, 32)

                bediener = get_cache(
                    Bediener, {"nr": [(eq, debitor.bediener_nr)]})

                if bediener:
                    output_list.str = output_list.str + \
                        to_string(bediener.userinit, "x(3)")
                else:
                    output_list.str = output_list.str + "   "
                output_list.str = output_list.str + \
                    to_string(debitor.vesrcod, "x(34)")
                t_credit = to_decimal(t_credit) + to_decimal(debitor.saldo)
                t_famt = to_decimal(t_famt) + to_decimal(debitor.vesrdep)
                tot_credit = to_decimal(tot_credit) + to_decimal(debitor.saldo)
                tot_saldo = to_decimal(tot_saldo) + to_decimal(debitor.saldo)
                tot_foreign = to_decimal(
                    tot_foreign) + to_decimal(debitor.vesrdep)
                tot_famt = to_decimal(tot_famt) + to_decimal(debitor.vesrdep)

                s_list = query(s_list_data, filters=(
                    lambda s_list: s_list.artnr == art.artnr), first=True)

                if not s_list:
                    s_list = S_list()
                    s_list_data.append(s_list)

                    s_list.artnr = art.artnr
                    s_list.bezeich = art.bezeich
                output_list.str = output_list.str + \
                    to_string(debitor.vesrdep, "->>,>>>,>>>,>>9.99")

                waehrung = get_cache(
                    Waehrung, {"waehrungsnr": [(eq, debitor.betrieb_gastmem)]})

                if waehrung:
                    output_list.str = output_list.str + \
                        to_string(waehrung.wabkurz, "x(4)")
                else:
                    output_list.str = output_list.str + "   "

                t_guest = get_cache(
                    Guest, {"gastnr": [(eq, debt.gastnrmember)]})

                if t_guest:
                    tstr = substring(f"{t_guest.name}, {t_guest.vorname1}{t_guest.anrede1}", 0, 34)
                else:
                    tstr = " "
                output_list.str = output_list.str + to_string(tstr, "x(50)")
                output_list.str = output_list.str + to_string(debitor.vesrdep, "->,>>>,>>>,>>9.99")
                output_list.str = output_list.str + to_string(debitor.zahlkonto, ">>>>9")
                output_list.str = output_list.str + to_string(debitor.vesrdep, "->,>>>,>>>,>>9.99")
                output_list.str = output_list.str + to_string(artikel.bezeich, "x(40)")

                s_list.betrag = to_decimal(
                    s_list.betrag) + to_decimal(debitor.saldo)
        output_list = Output_list()
        output_list_data.append(output_list)

        for i in range(1, 58 + 1):
            output_list.str = output_list.str + "   "
        output_list.pay_amt = to_decimal(tot_saldo)
        output_list.pay_famt = to_decimal(tot_foreign)

        if not long_digit:
            output_list.str = output_list.str + "T O T A L " +\
                to_string(tot_saldo, "->,>>>,>>>,>>9.99") +\
                fill(" ", 78) +\
                to_string(tot_foreign, " ->>,>>>,>>>,>>9.99")
        else:
            output_list.str = output_list.str + "T O T A L " +\
                to_string(tot_saldo, " ->>>,>>>,>>>,>>9") +\
                fill(" ", 78) +\
                to_string(tot_foreign, "   ->>>,>>>,>>>,>>9")
        output_list = Output_list()
        output_list_data.append(output_list)

        output_list = Output_list()
        output_list_data.append(output_list)

        for i in range(1, 58 + 1):
            output_list.str = output_list.str + "   "
        output_list.pay_amt = to_decimal(t_credit)
        output_list.pay_famt = to_decimal(t_famt)

        if not long_digit:
            output_list.str = output_list.str + "Sub-Total " +\
                to_string(t_credit, "->,>>>,>>>,>>9.99") +\
                fill(" ", 78) +\
                to_string(t_famt, "->>,>>>,>>>,>>9.99")
        else:
            output_list.str = output_list.str + "Sub-Total " +\
                to_string(t_credit, " ->>>,>>>,>>>,>>9") +\
                fill(" ", 78) +\
                to_string(t_famt, "  ->>>,>>>,>>>,>>9")
        output_list = Output_list()
        output_list_data.append(output_list)

        output_list = Output_list()
        output_list_data.append(output_list)

        for i in range(1, 56 + 1):
            output_list.str = output_list.str + " "
        output_list.pay_amt = to_decimal(tot_credit)
        output_list.pay_famt = to_decimal(tot_famt)

        if not long_digit:
            output_list.str = output_list.str + "Grand TOTAL " +\
                to_string(tot_credit, "->,>>>,>>>,>>9.99") +\
                fill(" ", 78) + \
                to_string(tot_famt, "->>,>>>,>>>,>>9.99")
        else:
            output_list.str = output_list.str + "Grand TOTAL " +\
                to_string(tot_credit, " ->>>,>>>,>>>,>>9") +\
                fill(" ", 78) + \
                to_string(tot_famt, "  ->>>,>>>,>>>,>>9")
        create_tot_payment()

    def create_list1e():

        nonlocal r_no, s_list_data, t_list_data, t_ar_paylist_data, long_digit, htparam, guest, debitor, artikel, bill, bediener, waehrung
        nonlocal comment, cledger, ccard, last_sort, from_date, to_date, from_art, to_art, mi_payment, mi_transfer, show_inv, bill_name, bill_nr
        nonlocal bguest, bdebitor

        nonlocal s_list, t_list, output_list, t_ar_paylist, bguest, bdebitor, tbuff, bq
        nonlocal s_list_data, t_list_data, output_list_data, t_ar_paylist_data

        artnr: int = 0
        i: int = 0
        curr_date: date = None
        t_credit: Decimal = to_decimal("0.0")
        tot_credit: Decimal = to_decimal("0.0")
        t_famt: Decimal = to_decimal("0.0")
        tot_famt: Decimal = to_decimal("0.0")
        tot_saldo: Decimal = to_decimal("0.0")
        tot_foreign: Decimal = to_decimal("0.0")
        receiver: string = ""
        do_it: bool = False
        temp_name: string = ""
        temp_vorname1: string = ""
        temp_anredefirma: string = ""
        temp_anrede1: string = ""
        debt = None
        art = None
        t_guest = None
        tstr: string = ""
        Debt = create_buffer("Debt", Debitor)
        Art = create_buffer("Art", Artikel)
        T_guest = create_buffer("T_guest", Guest)

        debitor_obj_list = {}
        debitor = Debitor()
        debt = Debitor()
        artikel = Artikel()
        art = Artikel()
        guest = Guest()
        for debitor.gastnr, debitor.saldo, debitor.zahlkonto, debitor.betriebsnr, debitor.counter, debitor.rechnr, debitor.debref, debitor.rgdatum, debitor.gastnrmember, debitor.bediener_nr, debitor.vesrcod, debitor.vesrdep, debitor.betrieb_gastmem, debitor._recid, debt.gastnr, debt.saldo, debt.zahlkonto, debt.betriebsnr, debt.counter, debt.rechnr, debt.debref, debt.rgdatum, debt.gastnrmember, debt.bediener_nr, debt.vesrcod, debt.vesrdep, debt.betrieb_gastmem, debt._recid, artikel.artnr, artikel.bezeich, artikel.artart, artikel._recid, art.artnr, art.bezeich, art.artart, art._recid, guest.name, guest.vorname1, guest.anredefirma, guest.anrede1, guest._recid in db_session.query(Debitor.gastnr, Debitor.saldo, Debitor.zahlkonto, Debitor.betriebsnr, Debitor.counter, Debitor.rechnr, Debitor.debref, Debitor.rgdatum, Debitor.gastnrmember, Debitor.bediener_nr, Debitor.vesrcod, Debitor.vesrdep, Debitor.betrieb_gastmem, Debitor._recid, Debt.gastnr, Debt.saldo, Debt.zahlkonto, Debt.betriebsnr, Debt.counter, Debt.rechnr, Debt.debref, Debt.rgdatum, Debt.gastnrmember, Debt.bediener_nr, Debt.vesrcod, Debt.vesrdep, Debt.betrieb_gastmem, Debt._recid, Artikel.artnr, Artikel.bezeich, Artikel.artart, Artikel._recid, Art.artnr, Art.bezeich, Art.artart, Art._recid, Guest.name, Guest.vorname1, Guest.anredefirma, Guest.anrede1, Guest._recid).join(Debt, (Debt.counter == Debitor.counter) & (Debt.zahlkonto == 0)).join(Artikel, (Artikel.artnr == Debitor.artnr) & (Artikel.departement == 0)).join(Art, (Art.artnr == Debitor.zahlkonto) & (Art.departement == 0)).join(Guest, (Guest.gastnr == Debitor.gastnr)).filter(
                (Debitor.rgdatum >= from_date) & (Debitor.rgdatum <= to_date) & (Debitor.zahlkonto > 0) & (Debitor.artnr >= from_art) & (Debitor.artnr <= to_art) & (Debitor.counter > 0) & (Debitor.opart > 0)).order_by(Artikel.artnr, Debitor.rgdatum, Debitor.rgdatum, Debitor.vesrcod, Debitor.name, Debitor.zahlkonto, Debitor.rechnr).all():
            if debitor_obj_list.get(debitor._recid):
                continue
            else:
                debitor_obj_list[debitor._recid] = True

            do_it = True

            if mi_payment:

                if artikel.artart == 2 and art.artart != 4 and art.artart != 7:
                    do_it = False

                elif artikel.artart == 7 and art.artart != 4:
                    do_it = False

            elif mi_transfer:

                if artikel.artart == 2 and (art.artart == 4 or art.artart == 7):
                    do_it = False

                elif artikel.artart == 7 and art.artart == 4:
                    do_it = False

            if do_it and (bill_name != "") and (substring(bill_name, 0, 1) != ("*").lower()):

                if not matches(guest.name, r"*" + bill_name + r"*"):
                    do_it = False

            if do_it and (bill_name != "") and (substring(bill_name, 0, 1) == ("*").lower()):

                if not matches(guest.name, bill_name):
                    do_it = False

            if do_it:

                if curr_date == None:
                    curr_date = debitor.rgdatum

                if curr_date != debitor.rgdatum:
                    curr_date = debitor.rgdatum
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    for i in range(1, 58 + 1):
                        output_list.str = output_list.str + "   "
                    output_list.pay_amt = to_decimal(tot_saldo)
                    output_list.pay_famt = to_decimal(tot_foreign)

                    if not long_digit:
                        output_list.str = output_list.str + "T O T A L " +\
                            to_string(tot_saldo, "->,>>>,>>>,>>9.99") +\
                            fill(" ", 78) +\
                            to_string(tot_foreign, " ->>,>>>,>>>,>>9.99")
                    else:
                        output_list.str = output_list.str + "T O T A L " +\
                            to_string(tot_saldo, " ->>>,>>>,>>>,>>9") +\
                            fill(" ", 78) +\
                            to_string(tot_foreign, "   ->>>,>>>,>>>,>>9")
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    tot_saldo = to_decimal("0")
                    tot_foreign = to_decimal("0")

                if artnr != artikel.artnr:
                    t_list = T_list()
                    t_list_data.append(t_list)

                    t_list.artnr = artikel.artnr
                    t_list.bezeich = artikel.bezeich

                    if artnr != 0:
                        output_list = Output_list()
                        output_list_data.append(output_list)

                        for i in range(1, 58 + 1):
                            output_list.str = output_list.str + "   "
                        output_list.pay_amt = to_decimal(t_credit)
                        output_list.pay_famt = to_decimal(t_famt)

                        if not long_digit:
                            output_list.str = output_list.str + "Sub-Total " +\
                                to_string(t_credit, "->,>>>,>>>,>>9.99") +\
                                fill(" ", 78) +\
                                to_string(t_famt, "->>,>>>,>>>,>>9.99")
                        else:
                            output_list.str = output_list.str + "Sub-Total " +\
                                to_string(t_credit, " ->>>,>>>,>>>,>>9") +\
                                fill(" ", 78) +\
                                to_string(t_famt, "  ->>>,>>>,>>>,>>9")
                        output_list = Output_list()
                        output_list_data.append(output_list)

                        t_credit = to_decimal("0")
                        t_famt = to_decimal("0")
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    for i in range(1, 19 + 1):
                        output_list.str = output_list.str + " "
                    output_list.str = output_list.str +\
                        to_string(artikel.artnr, ">>>>9") + " - " +\
                        to_string(artikel.bezeich, "x(24)")
                    artnr = artikel.artnr
                t_list.betrag = to_decimal(
                    t_list.betrag) - to_decimal(debitor.saldo)

                if guest.name != None:
                    temp_name = guest.name

                else:
                    temp_name = ""

                if guest.vorname1 != None:
                    temp_vorname1 = guest.vorname1

                else:
                    temp_vorname1 = ""

                if guest.anredefirma != None:
                    temp_anredefirma = guest.anredefirma

                else:
                    temp_anredefirma = ""

                if guest.anrede1 != None:
                    temp_anrede1 = guest.anrede1

                else:
                    temp_anrede1 = ""
                receiver = substring(f"{temp_name}, {temp_vorname1} {temp_anredefirma}{temp_anrede1}", 0, 32)
                output_list = Output_list()
                output_list_data.append(output_list)

                output_list.flag = 1
                output_list.artnr = debitor.zahlkonto
                output_list.pay_amt = to_decimal(debitor.saldo)
                output_list.pay_count = debitor.betriebsnr
                output_list.bill_art = artikel.artnr
                output_list.debt_counter = debitor.counter
                output_list.famt = to_string(
                    debt.vesrdep, "->>,>>>,>>>,>>9.99")
                output_list.pay_famt = to_decimal(debt.vesrdep)

                if show_inv:

                    bill = get_cache(Bill, {"rechnr": [(eq, debitor.rechnr)]})

                    if bill:
                        output_list.inv_no = to_string(
                            bill.rechnr2, ">>>>>>>>>")

                        if bill.billref != 0:
                            output_list.soa_inv = "INV" + \
                                to_string(bill.billref, "9999999")
                    else:

                        bdebitor = get_cache(
                            Debitor, {"rechnr": [(eq, debitor.rechnr)], "debref": [(gt, 0)]})

                        if bdebitor:
                            output_list.soa_inv = "INV" + \
                                to_string(debitor.debref, "9999999")

                if not long_digit:
                    output_list.str = to_string(debt.rgdatum) +\
                        to_string(debitor.rechnr, ">>>,>>>,>>9") +\
                        to_string(receiver, "x(32)") +\
                        to_string(debt.saldo, "->,>>>,>>>,>>9.99") +\
                        to_string(debitor.saldo, "->,>>>,>>>,>>9.99") +\
                        to_string(art.bezeich, "x(34)") +\
                        to_string(debitor.rgdatum)
                else:
                    output_list.str = to_string(debt.rgdatum) +\
                        to_string(debitor.rechnr, ">>>,>>>,>>9") +\
                        to_string(receiver, "x(32)") +\
                        to_string(debt.saldo, " ->>>,>>>,>>>,>>9") +\
                        to_string(debitor.saldo, " ->>>,>>>,>>>,>>9") +\
                        to_string(art.bezeich, "x(34)") +\
                        to_string(debitor.rgdatum)
                output_list.bill_num = debitor.rechnr
                output_list.art_bezeich = artikel.bezeich
                output_list.tbetrag = to_decimal(
                    output_list.tbetrag) - to_decimal(debitor.saldo)

                bguest = get_cache(
                    Guest, {"gastnr": [(eq, debitor.gastnrmember)]})

                if bguest:
                    output_list.gastname = substring(f"{bguest.name}, {bguest.vorname1}{bguest.anredefirma} {bguest.anrede1}", 0, 32)

                bediener = get_cache(
                    Bediener, {"nr": [(eq, debitor.bediener_nr)]})

                if bediener:
                    output_list.str = output_list.str + \
                        to_string(bediener.userinit, "x(3)")
                else:
                    output_list.str = output_list.str + "   "
                output_list.str = output_list.str + \
                    to_string(debitor.vesrcod, "x(34)")
                t_credit = to_decimal(t_credit) + to_decimal(debitor.saldo)
                t_famt = to_decimal(t_famt) + to_decimal(debitor.vesrdep)
                tot_credit = to_decimal(tot_credit) + to_decimal(debitor.saldo)
                tot_saldo = to_decimal(tot_saldo) + to_decimal(debitor.saldo)
                tot_foreign = to_decimal(
                    tot_foreign) + to_decimal(debitor.vesrdep)
                tot_famt = to_decimal(tot_famt) + to_decimal(debitor.vesrdep)

                s_list = query(s_list_data, filters=(
                    lambda s_list: s_list.artnr == art.artnr), first=True)

                if not s_list:
                    s_list = S_list()
                    s_list_data.append(s_list)

                    s_list.artnr = art.artnr
                    s_list.bezeich = art.bezeich
                output_list.str = output_list.str + \
                    to_string(debitor.vesrdep, "->>,>>>,>>>,>>9.99")

                waehrung = get_cache(
                    Waehrung, {"waehrungsnr": [(eq, debitor.betrieb_gastmem)]})

                if waehrung:
                    output_list.str = output_list.str + \
                        to_string(waehrung.wabkurz, "x(4)")
                else:
                    output_list.str = output_list.str + "    "

                t_guest = get_cache(
                    Guest, {"gastnr": [(eq, debt.gastnrmember)]})

                if t_guest:
                    tstr = substring(f"{t_guest.name}, {t_guest.vorname1}{t_guest.anrede1}", 0, 34)
                else:
                    tstr = " "
                output_list.str = output_list.str + to_string(tstr, "x(50)")
                output_list.str = output_list.str + to_string(debitor.vesrdep, "->,>>>,>>>,>>9.99")
                output_list.str = output_list.str + to_string(debitor.zahlkonto, ">>>>9")
                output_list.str = output_list.str + to_string(debitor.vesrdep, "->,>>>,>>>,>>9.99")
                output_list.str = output_list.str + to_string(artikel.bezeich, "x(40)")

                s_list.betrag = to_decimal(
                    s_list.betrag) + to_decimal(debitor.saldo)
        output_list = Output_list()
        output_list_data.append(output_list)

        for i in range(1, 58 + 1):
            output_list.str = output_list.str + "   "
        output_list.pay_amt = to_decimal(tot_saldo)
        output_list.pay_famt = to_decimal(tot_foreign)

        if not long_digit:
            output_list.str = output_list.str + "T O T A L " +\
                to_string(tot_saldo, "->,>>>,>>>,>>9.99") +\
                fill(" ", 78) +\
                to_string(tot_foreign, " ->>,>>>,>>>,>>9.99")
        else:
            output_list.str = output_list.str + "T O T A L " +\
                to_string(tot_saldo, " ->>>,>>>,>>>,>>9") +\
                fill(" ", 78) +\
                to_string(tot_foreign, "   ->>>,>>>,>>>,>>9")
        output_list = Output_list()
        output_list_data.append(output_list)

        output_list = Output_list()
        output_list_data.append(output_list)

        for i in range(1, 58 + 1):
            output_list.str = output_list.str + "   "
        output_list.pay_amt = to_decimal(t_credit)
        output_list.pay_famt = to_decimal(t_famt)

        if not long_digit:
            output_list.str = output_list.str + "Sub-Total " +\
                to_string(t_credit, "->,>>>,>>>,>>9.99") +\
                fill(" ", 78) +\
                to_string(t_famt, "->>,>>>,>>>,>>9.99")
        else:
            output_list.str = output_list.str + "Sub-Total " +\
                to_string(t_credit, " ->>>,>>>,>>>,>>9") +\
                fill(" ", 78) +\
                to_string(t_famt, "  ->>>,>>>,>>>,>>9")
        output_list = Output_list()
        output_list_data.append(output_list)

        output_list = Output_list()
        output_list_data.append(output_list)

        for i in range(1, 56 + 1):
            output_list.str = output_list.str + " "
        output_list.pay_amt = to_decimal(tot_credit)
        output_list.pay_famt = to_decimal(tot_famt)

        if not long_digit:
            output_list.str = output_list.str + "Grand TOTAL " +\
                to_string(tot_credit, "->,>>>,>>>,>>9.99") +\
                fill(" ", 78) + \
                to_string(tot_famt, "->>,>>>,>>>,>>9.99")
        else:
            output_list.str = output_list.str + "Grand TOTAL " +\
                to_string(tot_credit, " ->>>,>>>,>>>,>>9") +\
                fill(" ", 78) + \
                to_string(tot_famt, "  ->>>,>>>,>>>,>>9")
        create_tot_payment()

    def create_list1f():

        nonlocal r_no, s_list_data, t_list_data, t_ar_paylist_data, long_digit, htparam, guest, debitor, artikel, bill, bediener, waehrung
        nonlocal comment, cledger, ccard, last_sort, from_date, to_date, from_art, to_art, mi_payment, mi_transfer, show_inv, bill_name, bill_nr
        nonlocal bguest, bdebitor

        nonlocal s_list, t_list, output_list, t_ar_paylist, bguest, bdebitor, tbuff, bq
        nonlocal s_list_data, t_list_data, output_list_data, t_ar_paylist_data

        artnr: int = 0
        i: int = 0
        curr_gastnr: int = 0
        t_credit: Decimal = to_decimal("0.0")
        tot_credit: Decimal = to_decimal("0.0")
        t_famt: Decimal = to_decimal("0.0")
        tot_famt: Decimal = to_decimal("0.0")
        tot_saldo: Decimal = to_decimal("0.0")
        tot_foreign: Decimal = to_decimal("0.0")
        receiver: string = ""
        do_it: bool = False
        temp_name: string = ""
        temp_vorname1: string = ""
        temp_anredefirma: string = ""
        temp_anrede1: string = ""
        debt = None
        art = None
        t_guest = None
        tstr: string = ""
        Debt = create_buffer("Debt", Debitor)
        Art = create_buffer("Art", Artikel)
        T_guest = create_buffer("T_guest", Guest)

        debitor_obj_list = {}
        debitor = Debitor()
        debt = Debitor()
        artikel = Artikel()
        art = Artikel()
        guest = Guest()
        for debitor.gastnr, debitor.saldo, debitor.zahlkonto, debitor.betriebsnr, debitor.counter, debitor.rechnr, debitor.debref, debitor.rgdatum, debitor.gastnrmember, debitor.bediener_nr, debitor.vesrcod, debitor.vesrdep, debitor.betrieb_gastmem, debitor._recid, debt.gastnr, debt.saldo, debt.zahlkonto, debt.betriebsnr, debt.counter, debt.rechnr, debt.debref, debt.rgdatum, debt.gastnrmember, debt.bediener_nr, debt.vesrcod, debt.vesrdep, debt.betrieb_gastmem, debt._recid, artikel.artnr, artikel.bezeich, artikel.artart, artikel._recid, art.artnr, art.bezeich, art.artart, art._recid, guest.name, guest.vorname1, guest.anredefirma, guest.anrede1, guest._recid in db_session.query(Debitor.gastnr, Debitor.saldo, Debitor.zahlkonto, Debitor.betriebsnr, Debitor.counter, Debitor.rechnr, Debitor.debref, Debitor.rgdatum, Debitor.gastnrmember, Debitor.bediener_nr, Debitor.vesrcod, Debitor.vesrdep, Debitor.betrieb_gastmem, Debitor._recid, Debt.gastnr, Debt.saldo, Debt.zahlkonto, Debt.betriebsnr, Debt.counter, Debt.rechnr, Debt.debref, Debt.rgdatum, Debt.gastnrmember, Debt.bediener_nr, Debt.vesrcod, Debt.vesrdep, Debt.betrieb_gastmem, Debt._recid, Artikel.artnr, Artikel.bezeich, Artikel.artart, Artikel._recid, Art.artnr, Art.bezeich, Art.artart, Art._recid, Guest.name, Guest.vorname1, Guest.anredefirma, Guest.anrede1, Guest._recid).join(Debt, (Debt.counter == Debitor.counter) & (Debt.zahlkonto == 0)).join(Artikel, (Artikel.artnr == Debitor.artnr) & (Artikel.departement == 0)).join(Art, (Art.artnr == Debitor.zahlkonto) & (Art.departement == 0)).join(Guest, (Guest.gastnr == Debitor.gastnr)).filter(
                (Debitor.zahlkonto > 0) & (Debitor.artnr >= from_art) & (Debitor.artnr <= to_art) & (Debitor.counter > 0) & (Debitor.opart > 0) & (Debitor.rechnr == bill_nr)).order_by(Artikel.artnr, Debitor.name, Debitor.gastnr, Debitor.rgdatum, Debitor.zahlkonto, Debitor.betriebsnr, Debitor.rechnr).all():
            if debitor_obj_list.get(debitor._recid):
                continue
            else:
                debitor_obj_list[debitor._recid] = True

            do_it = True

            if mi_payment:

                if artikel.artart == 2 and art.artart != 4 and art.artart != 7:
                    do_it = False

                elif artikel.artart == 7 and art.artart != 4:
                    do_it = False

            elif mi_transfer:

                if artikel.artart == 2 and (art.artart == 4 or art.artart == 7):
                    do_it = False

                elif artikel.artart == 7 and art.artart == 4:
                    do_it = False

            if do_it and (bill_name != "") and (substring(bill_name, 0, 1) != ("*").lower()):

                if not matches(guest.name, r"*" + bill_name + r"*"):
                    do_it = False

            if do_it and (bill_name != "") and (substring(bill_name, 0, 1) == ("*").lower()):

                if not matches(guest.name, bill_name):
                    do_it = False

            if do_it:

                if curr_gastnr == 0:
                    curr_gastnr = debitor.gastnr

                if curr_gastnr != debitor.gastnr:
                    curr_gastnr = debitor.gastnr
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    for i in range(1, 58 + 1):
                        output_list.str = output_list.str + "   "
                    output_list.pay_amt = to_decimal(tot_saldo)
                    output_list.pay_famt = to_decimal(tot_foreign)

                    if not long_digit:
                        output_list.str = output_list.str + "T O T A L " +\
                            to_string(tot_saldo, "->,>>>,>>>,>>9.99") +\
                            fill(" ", 78) +\
                            to_string(tot_foreign, " ->>,>>>,>>>,>>9.99")
                    else:
                        output_list.str = output_list.str + "T O T A L " +\
                            to_string(tot_saldo, " ->>>,>>>,>>>,>>9") +\
                            fill(" ", 78) +\
                            to_string(tot_foreign, "   ->>>,>>>,>>>,>>9")
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    tot_saldo = to_decimal("0")
                    tot_foreign = to_decimal("0")

                if artnr != artikel.artnr:
                    t_list = T_list()
                    t_list_data.append(t_list)

                    t_list.artnr = artikel.artnr
                    t_list.bezeich = artikel.bezeich

                    if artnr != 0:

                        if tot_saldo != 0:
                            output_list = Output_list()
                            output_list_data.append(output_list)

                            for i in range(1, 58 + 1):
                                output_list.str = output_list.str + "   "
                            output_list.pay_amt = to_decimal(tot_saldo)
                            output_list.pay_famt = to_decimal(tot_foreign)

                            if not long_digit:
                                output_list.str = output_list.str + "T O T A L " +\
                                    to_string(tot_saldo, "->,>>>,>>>,>>9.99") +\
                                    fill(" ", 78) +\
                                    to_string(tot_foreign, " ->>,>>>,>>>,>>9.99")
                            else:
                                output_list.str = output_list.str + "T O T A L " +\
                                    to_string(tot_saldo, " ->>>,>>>,>>>,>>9") +\
                                    fill(" ", 78) +\
                                    to_string(tot_foreign, "   ->>>,>>>,>>>,>>9")
                            output_list = Output_list()
                            output_list_data.append(output_list)

                            tot_saldo = to_decimal("0")
                            tot_foreign = to_decimal("0")
                        output_list = Output_list()
                        output_list_data.append(output_list)

                        for i in range(1, 58 + 1):
                            output_list.str = output_list.str + "   "
                        output_list.pay_amt = to_decimal(t_credit)
                        output_list.pay_famt = to_decimal(t_famt)

                        if not long_digit:
                            output_list.str = output_list.str + "Sub-Total " +\
                                to_string(t_credit, "->,>>>,>>>,>>9.99") +\
                                fill(" ", 78) +\
                                to_string(t_famt, "->>,>>>,>>>,>>9.99")
                        else:
                            output_list.str = output_list.str + "Sub-Total " +\
                                to_string(t_credit, " ->>>,>>>,>>>,>>9") +\
                                fill(" ", 78) +\
                                to_string(t_famt, "  ->>>,>>>,>>>,>>9")
                        output_list = Output_list()
                        output_list_data.append(output_list)

                        t_credit = to_decimal("0")
                        t_famt = to_decimal("0")
                        tot_saldo = to_decimal("0")
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    for i in range(1, 19 + 1):
                        output_list.str = output_list.str + " "
                    output_list.str = output_list.str +\
                        to_string(artikel.artnr, ">>>>9") + " - " +\
                        to_string(artikel.bezeich, "x(24)")
                    artnr = artikel.artnr
                t_list.betrag = to_decimal(
                    t_list.betrag) - to_decimal(debitor.saldo)

                if guest.name != None:
                    temp_name = guest.name

                else:
                    temp_name = ""

                if guest.vorname1 != None:
                    temp_vorname1 = guest.vorname1

                else:
                    temp_vorname1 = ""

                if guest.anredefirma != None:
                    temp_anredefirma = guest.anredefirma

                else:
                    temp_anredefirma = ""

                if guest.anrede1 != None:
                    temp_anrede1 = guest.anrede1

                else:
                    temp_anrede1 = ""
                receiver = substring(f"{temp_name}, {temp_vorname1} {temp_anredefirma}{temp_anrede1}", 0, 32)
                output_list = Output_list()
                output_list_data.append(output_list)

                output_list.flag = 1
                output_list.artnr = debitor.zahlkonto
                output_list.pay_amt = to_decimal(debitor.saldo)
                output_list.pay_count = debitor.betriebsnr
                output_list.bill_art = artikel.artnr
                output_list.debt_counter = debitor.counter
                output_list.famt = to_string(
                    debt.vesrdep, "->>,>>>,>>>,>>9.99")
                output_list.pay_famt = to_decimal(debt.vesrdep)

                if show_inv:

                    bill = get_cache(Bill, {"rechnr": [(eq, debitor.rechnr)]})

                    if bill:
                        output_list.inv_no = to_string(
                            bill.rechnr2, ">>>>>>>>>")

                        if bill.billref != 0:
                            output_list.soa_inv = "INV" + \
                                to_string(bill.billref, "9999999")
                    else:

                        bdebitor = get_cache(
                            Debitor, {"rechnr": [(eq, debitor.rechnr)], "debref": [(gt, 0)]})

                        if bdebitor:
                            output_list.soa_inv = "INV" + \
                                to_string(debitor.debref, "9999999")

                if not long_digit:
                    output_list.str = to_string(debt.rgdatum) +\
                        to_string(debitor.rechnr, ">>>,>>>,>>9") +\
                        to_string(receiver, "x(32)") +\
                        to_string(debt.saldo, "->,>>>,>>>,>>9.99") +\
                        to_string(debitor.saldo, "->,>>>,>>>,>>9.99") +\
                        to_string(art.bezeich, "x(34)") +\
                        to_string(debitor.rgdatum)
                else:
                    output_list.str = to_string(debt.rgdatum) +\
                        to_string(debitor.rechnr, ">>>,>>>,>>9") +\
                        to_string(receiver, "x(32)") +\
                        to_string(debt.saldo, " ->>>,>>>,>>>,>>9") +\
                        to_string(debitor.saldo, " ->>>,>>>,>>>,>>9") +\
                        to_string(art.bezeich, "x(34)") +\
                        to_string(debitor.rgdatum)
                output_list.bill_num = debitor.rechnr
                output_list.art_bezeich = artikel.bezeich
                output_list.tbetrag = to_decimal(
                    output_list.tbetrag) - to_decimal(debitor.saldo)

                bguest = get_cache(
                    Guest, {"gastnr": [(eq, debitor.gastnrmember)]})

                if bguest:
                    output_list.gastname = substring(f"{bguest.name}, {bguest.vorname1}{bguest.anredefirma} {bguest.anrede1}", 0, 32)

                bediener = get_cache(
                    Bediener, {"nr": [(eq, debitor.bediener_nr)]})

                if bediener:
                    output_list.str = output_list.str + \
                        to_string(bediener.userinit, "x(3)")
                else:
                    output_list.str = output_list.str + "   "
                output_list.str = output_list.str + \
                    to_string(debitor.vesrcod, "x(34)")
                t_credit = to_decimal(t_credit) + to_decimal(debitor.saldo)
                t_famt = to_decimal(t_famt) + to_decimal(debitor.vesrdep)
                tot_credit = to_decimal(tot_credit) + to_decimal(debitor.saldo)
                tot_saldo = to_decimal(tot_saldo) + to_decimal(debitor.saldo)
                tot_foreign = to_decimal(
                    tot_foreign) + to_decimal(debitor.vesrdep)
                tot_famt = to_decimal(tot_famt) + to_decimal(debitor.vesrdep)

                s_list = query(s_list_data, filters=(
                    lambda s_list: s_list.artnr == art.artnr), first=True)

                if not s_list:
                    s_list = S_list()
                    s_list_data.append(s_list)

                    s_list.artnr = art.artnr
                    s_list.bezeich = art.bezeich
                output_list.str = output_list.str + \
                    to_string(debitor.vesrdep, "->>,>>>,>>>,>>9.99")

                waehrung = get_cache(
                    Waehrung, {"waehrungsnr": [(eq, debitor.betrieb_gastmem)]})

                if waehrung:
                    output_list.str = output_list.str + \
                        to_string(waehrung.wabkurz, "x(4)")
                else:
                    output_list.str = output_list.str + "    "

                t_guest = get_cache(
                    Guest, {"gastnr": [(eq, debt.gastnrmember)]})

                if t_guest:
                    tstr = substring(f"{t_guest.name}, {t_guest.vorname1}{t_guest.anrede1}", 0, 34)
                else:
                    tstr = " "
                output_list.str = output_list.str + to_string(tstr, "x(50)")
                output_list.str = output_list.str + \
                    to_string(debitor.vesrdep, "->,>>>,>>>,>>9.99")
                output_list.str = output_list.str + \
                    to_string(debitor.zahlkonto, ">>>>9")
                output_list.str = output_list.str + \
                    to_string(debitor.vesrdep, "->,>>>,>>>,>>9.99")
                output_list.str = output_list.str + \
                    to_string(artikel.bezeich, "x(40)")

                s_list.betrag = to_decimal(
                    s_list.betrag) + to_decimal(debitor.saldo)
        output_list = Output_list()
        output_list_data.append(output_list)

        for i in range(1, 58 + 1):
            output_list.str = output_list.str + "   "
        output_list.pay_amt = to_decimal(tot_saldo)
        output_list.pay_famt = to_decimal(tot_foreign)

        if not long_digit:
            output_list.str = output_list.str + "T O T A L " +\
                to_string(tot_saldo, "->,>>>,>>>,>>9.99") +\
                fill(" ", 78) +\
                to_string(tot_foreign, " ->>,>>>,>>>,>>9.99")
        else:
            output_list.str = output_list.str + "T O T A L " +\
                to_string(tot_saldo, " ->>>,>>>,>>>,>>9") +\
                fill(" ", 78) +\
                to_string(tot_foreign, "   ->>>,>>>,>>>,>>9")
        output_list = Output_list()
        output_list_data.append(output_list)

        output_list = Output_list()
        output_list_data.append(output_list)

        for i in range(1, 58 + 1):
            output_list.str = output_list.str + "   "
        output_list.pay_amt = to_decimal(t_credit)
        output_list.pay_famt = to_decimal(t_famt)

        if not long_digit:
            output_list.str = output_list.str + "Sub-Total " +\
                to_string(t_credit, "->,>>>,>>>,>>9.99") +\
                fill(" ", 78) +\
                to_string(t_famt, "->>,>>>,>>>,>>9.99")
        else:
            output_list.str = output_list.str + "Sub-Total " +\
                to_string(t_credit, " ->>>,>>>,>>>,>>9") +\
                fill(" ", 78) +\
                to_string(t_famt, "  ->>>,>>>,>>>,>>9")
        output_list = Output_list()
        output_list_data.append(output_list)

        output_list = Output_list()
        output_list_data.append(output_list)

        for i in range(1, 56 + 1):
            output_list.str = output_list.str + " "
        output_list.pay_amt = to_decimal(tot_credit)
        output_list.pay_famt = to_decimal(tot_famt)

        if not long_digit:
            output_list.str = output_list.str + "Grand TOTAL " +\
                to_string(tot_credit, "->,>>>,>>>,>>9.99") +\
                fill(" ", 78) + \
                to_string(tot_famt, "->>,>>>,>>>,>>9.99")
        else:
            output_list.str = output_list.str + "Grand TOTAL " +\
                to_string(tot_credit, " ->>>,>>>,>>>,>>9") +\
                fill(" ", 78) + \
                to_string(tot_famt, "  ->>>,>>>,>>>,>>9")
        create_tot_payment()

    def create_list1fs():
        nonlocal r_no, s_list_data, t_list_data, t_ar_paylist_data, long_digit, htparam, guest, debitor, artikel, bill, bediener, waehrung
        nonlocal comment, cledger, ccard, last_sort, from_date, to_date, from_art, to_art, mi_payment, mi_transfer, show_inv, bill_name, bill_nr
        nonlocal bguest, bdebitor
        nonlocal s_list, t_list, output_list, t_ar_paylist, bguest, bdebitor, tbuff, bq
        nonlocal s_list_data, t_list_data, output_list_data, t_ar_paylist_data

        artnr: int = 0
        i: int = 0
        curr_gastnr: int = 0
        t_credit: Decimal = to_decimal("0.0")
        tot_credit: Decimal = to_decimal("0.0")
        t_famt: Decimal = to_decimal("0.0")
        tot_famt: Decimal = to_decimal("0.0")
        tot_saldo: Decimal = to_decimal("0.0")
        tot_foreign: Decimal = to_decimal("0.0")
        receiver: string = ""
        do_it: bool = False
        temp_name: string = ""
        temp_vorname1: string = ""
        temp_anredefirma: string = ""
        temp_anrede1: string = ""
        debt = None
        art = None
        t_guest = None
        tstr: string = ""
        Debt = create_buffer("Debt", Debitor)
        Art = create_buffer("Art", Artikel)
        T_guest = create_buffer("T_guest", Guest)

        debitor_obj_list = {}
        debitor = Debitor()
        debt = Debitor()
        artikel = Artikel()
        art = Artikel()
        guest = Guest()
        for debitor.gastnr, debitor.saldo, debitor.zahlkonto, debitor.betriebsnr, debitor.counter, debitor.rechnr, debitor.debref, debitor.rgdatum, debitor.gastnrmember, debitor.bediener_nr, debitor.vesrcod, debitor.vesrdep, debitor.betrieb_gastmem, debitor._recid, debt.gastnr, debt.saldo, debt.zahlkonto, debt.betriebsnr, debt.counter, debt.rechnr, debt.debref, debt.rgdatum, debt.gastnrmember, debt.bediener_nr, debt.vesrcod, debt.vesrdep, debt.betrieb_gastmem, debt._recid, artikel.artnr, artikel.bezeich, artikel.artart, artikel._recid, art.artnr, art.bezeich, art.artart, art._recid, guest.name, guest.vorname1, guest.anredefirma, guest.anrede1, guest._recid in db_session.query(Debitor.gastnr, Debitor.saldo, Debitor.zahlkonto, Debitor.betriebsnr, Debitor.counter, Debitor.rechnr, Debitor.debref, Debitor.rgdatum, Debitor.gastnrmember, Debitor.bediener_nr, Debitor.vesrcod, Debitor.vesrdep, Debitor.betrieb_gastmem, Debitor._recid, Debt.gastnr, Debt.saldo, Debt.zahlkonto, Debt.betriebsnr, Debt.counter, Debt.rechnr, Debt.debref, Debt.rgdatum, Debt.gastnrmember, Debt.bediener_nr, Debt.vesrcod, Debt.vesrdep, Debt.betrieb_gastmem, Debt._recid, Artikel.artnr, Artikel.bezeich, Artikel.artart, Artikel._recid, Art.artnr, Art.bezeich, Art.artart, Art._recid, Guest.name, Guest.vorname1, Guest.anredefirma, Guest.anrede1, Guest._recid).join(Debt, (Debt.counter == Debitor.counter) & (Debt.zahlkonto == 0)).join(Artikel, (Artikel.artnr == Debitor.artnr) & (Artikel.departement == 0)).join(Art, (Art.artnr == Debitor.zahlkonto) & (Art.departement == 0)).join(Guest, (Guest.gastnr == Debitor.gastnr)).filter(
                (Debitor.rgdatum >= from_date) & (Debitor.rgdatum <= to_date) & (Debitor.zahlkonto > 0) & (Debitor.artnr >= from_art) & (Debitor.artnr <= to_art) & (Debitor.counter > 0) & (Debitor.opart > 0)).order_by(Artikel.artnr, Debitor.name, Debitor.gastnr, Debitor.rgdatum, Debitor.zahlkonto, Debitor.betriebsnr, Debitor.rechnr).all():
            if debitor_obj_list.get(debitor._recid):
                continue
            else:
                debitor_obj_list[debitor._recid] = True

            do_it = True

            if mi_payment:

                if artikel.artart == 2 and art.artart != 4 and art.artart != 7:
                    do_it = False

                elif artikel.artart == 7 and art.artart != 4:
                    do_it = False

            elif mi_transfer:

                if artikel.artart == 2 and (art.artart == 4 or art.artart == 7):
                    do_it = False

                elif artikel.artart == 7 and art.artart == 4:
                    do_it = False

            if do_it and (bill_name != "") and (substring(bill_name, 0, 1) != ("*").lower()):

                if not matches(guest.name, r"*" + bill_name + r"*"):
                    do_it = False

            if do_it and (bill_name != "") and (substring(bill_name, 0, 1) == ("*").lower()):

                if not matches(guest.name, bill_name):
                    do_it = False

            if do_it:

                if curr_gastnr == 0:
                    curr_gastnr = debitor.gastnr

                if curr_gastnr != debitor.gastnr:
                    curr_gastnr = debitor.gastnr
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    for i in range(1, 58 + 1):
                        output_list.str = output_list.str + "   "
                    output_list.pay_amt = to_decimal(tot_saldo)
                    output_list.pay_famt = to_decimal(tot_foreign)

                    if not long_digit:
                        output_list.str = output_list.str + "T O T A L " +\
                            to_string(tot_saldo, "->,>>>,>>>,>>9.99") +\
                            fill(" ", 78) +\
                            to_string(tot_foreign, " ->>,>>>,>>>,>>9.99")
                    else:
                        output_list.str = output_list.str + "T O T A L " +\
                            to_string(tot_saldo, " ->>>,>>>,>>>,>>9") +\
                            fill(" ", 78) +\
                            to_string(tot_foreign, "   ->>>,>>>,>>>,>>9")
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    tot_saldo = to_decimal("0")
                    tot_foreign = to_decimal("0")

                if artnr != artikel.artnr:
                    t_list = T_list()
                    t_list_data.append(t_list)

                    t_list.artnr = artikel.artnr
                    t_list.bezeich = artikel.bezeich

                    if artnr != 0:

                        if tot_saldo != 0:
                            output_list = Output_list()
                            output_list_data.append(output_list)

                            for i in range(1, 58 + 1):
                                output_list.str = output_list.str + "   "
                            output_list.pay_amt = to_decimal(tot_saldo)
                            output_list.pay_famt = to_decimal(tot_foreign)

                            if not long_digit:
                                output_list.str = output_list.str + "T O T A L " +\
                                    to_string(tot_saldo, "->,>>>,>>>,>>9.99") +\
                                    fill(" ", 78) +\
                                    to_string(tot_foreign, " ->>,>>>,>>>,>>9.99")
                            else:
                                output_list.str = output_list.str + "T O T A L " +\
                                    to_string(tot_saldo, " ->>>,>>>,>>>,>>9") +\
                                    fill(" ", 78) +\
                                    to_string(tot_foreign, "   ->>>,>>>,>>>,>>9")
                            output_list = Output_list()
                            output_list_data.append(output_list)

                            tot_saldo = to_decimal("0")
                            tot_foreign = to_decimal("0")
                        output_list = Output_list()
                        output_list_data.append(output_list)

                        for i in range(1, 58 + 1):
                            output_list.str = output_list.str + "   "
                        output_list.pay_amt = to_decimal(t_credit)
                        output_list.pay_famt = to_decimal(t_famt)

                        if not long_digit:
                            output_list.str = output_list.str + "Sub-Total " +\
                                to_string(t_credit, "->,>>>,>>>,>>9.99") +\
                                fill(" ", 78) +\
                                to_string(t_famt, "->>,>>>,>>>,>>9.99")
                        else:
                            output_list.str = output_list.str + "Sub-Total " +\
                                to_string(t_credit, " ->>>,>>>,>>>,>>9") +\
                                fill(" ", 78) +\
                                to_string(t_famt, "  ->>>,>>>,>>>,>>9")
                        output_list = Output_list()
                        output_list_data.append(output_list)

                        t_credit = to_decimal("0")
                        t_famt = to_decimal("0")
                        tot_saldo = to_decimal("0")
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    for i in range(1, 19 + 1):
                        output_list.str = output_list.str + " "
                    output_list.str = output_list.str +\
                        to_string(artikel.artnr, ">>>>9") + " - " +\
                        to_string(artikel.bezeich, "x(24)")
                    artnr = artikel.artnr
                t_list.betrag = to_decimal(
                    t_list.betrag) - to_decimal(debitor.saldo)

                if guest.name != None:
                    temp_name = guest.name

                else:
                    temp_name = ""

                if guest.vorname1 != None:
                    temp_vorname1 = guest.vorname1

                else:
                    temp_vorname1 = ""

                if guest.anredefirma != None:
                    temp_anredefirma = guest.anredefirma

                else:
                    temp_anredefirma = ""

                if guest.anrede1 != None:
                    temp_anrede1 = guest.anrede1

                else:
                    temp_anrede1 = ""
                receiver = substring(f"{temp_name}, {temp_vorname1} {temp_anredefirma}{temp_anrede1}", 0, 32)
                output_list = Output_list()
                output_list_data.append(output_list)

                output_list.flag = 1
                output_list.artnr = debitor.zahlkonto
                output_list.pay_amt = to_decimal(debitor.saldo)
                output_list.pay_count = debitor.betriebsnr
                output_list.bill_art = artikel.artnr
                output_list.debt_counter = debitor.counter
                output_list.famt = to_string(
                    debt.vesrdep, "->>,>>>,>>>,>>9.99")
                output_list.pay_famt = to_decimal(debt.vesrdep)

                if show_inv:

                    bill = get_cache(Bill, {"rechnr": [(eq, debitor.rechnr)]})

                    if bill:
                        output_list.inv_no = to_string(
                            bill.rechnr2, ">>>>>>>>>")

                        if bill.billref != 0:
                            output_list.soa_inv = "INV" + \
                                to_string(bill.billref, "9999999")
                    else:

                        bdebitor = get_cache(
                            Debitor, {"rechnr": [(eq, debitor.rechnr)], "debref": [(gt, 0)]})

                        if bdebitor:
                            output_list.soa_inv = "INV" + \
                                to_string(debitor.debref, "9999999")

                if not long_digit:
                    output_list.str = to_string(debt.rgdatum) +\
                        to_string(debitor.rechnr, ">>>,>>>,>>9") +\
                        to_string(receiver, "x(32)") +\
                        to_string(debt.saldo, "->,>>>,>>>,>>9.99") +\
                        to_string(debitor.saldo, "->,>>>,>>>,>>9.99") +\
                        to_string(art.bezeich, "x(34)") +\
                        to_string(debitor.rgdatum)
                else:
                    output_list.str = to_string(debt.rgdatum) +\
                        to_string(debitor.rechnr, ">>>,>>>,>>9") +\
                        to_string(receiver, "x(32)") +\
                        to_string(debt.saldo, " ->>>,>>>,>>>,>>9") +\
                        to_string(debitor.saldo, " ->>>,>>>,>>>,>>9") +\
                        to_string(art.bezeich, "x(34)") +\
                        to_string(debitor.rgdatum)
                output_list.bill_num = debitor.rechnr
                output_list.art_bezeich = artikel.bezeich
                output_list.tbetrag = to_decimal(
                    output_list.tbetrag) - to_decimal(debitor.saldo)

                bguest = get_cache(
                    Guest, {"gastnr": [(eq, debitor.gastnrmember)]})

                if bguest:
                    output_list.gastname = substring(f"{bguest.name}, {bguest.vorname1}{bguest.anredefirma} {bguest.anrede1}", 0, 32)

                bediener = get_cache(
                    Bediener, {"nr": [(eq, debitor.bediener_nr)]})

                if bediener:
                    output_list.str = output_list.str + \
                        to_string(bediener.userinit, "x(3)")
                else:
                    output_list.str = output_list.str + "   "
                output_list.str = output_list.str + \
                    to_string(debitor.vesrcod, "x(34)")
                t_credit = to_decimal(t_credit) + to_decimal(debitor.saldo)
                t_famt = to_decimal(t_famt) + to_decimal(debitor.vesrdep)
                tot_credit = to_decimal(tot_credit) + to_decimal(debitor.saldo)
                tot_saldo = to_decimal(tot_saldo) + to_decimal(debitor.saldo)
                tot_foreign = to_decimal(
                    tot_foreign) + to_decimal(debitor.vesrdep)
                tot_famt = to_decimal(tot_famt) + to_decimal(debitor.vesrdep)

                s_list = query(s_list_data, filters=(
                    lambda s_list: s_list.artnr == art.artnr), first=True)

                if not s_list:
                    s_list = S_list()
                    s_list_data.append(s_list)

                    s_list.artnr = art.artnr
                    s_list.bezeich = art.bezeich
                output_list.str = output_list.str + \
                    to_string(debitor.vesrdep, "->>,>>>,>>>,>>9.99")

                waehrung = get_cache(
                    Waehrung, {"waehrungsnr": [(eq, debitor.betrieb_gastmem)]})

                if waehrung:
                    output_list.str = output_list.str + \
                        to_string(waehrung.wabkurz, "x(4)")
                else:
                    output_list.str = output_list.str + "    "

                t_guest = get_cache(
                    Guest, {"gastnr": [(eq, debt.gastnrmember)]})

                if t_guest:
                    tstr = substring(f"{t_guest.name}, {t_guest.vorname1}{t_guest.anrede1}", 0, 34)
                else:
                    tstr = " "
                output_list.str = output_list.str + to_string(tstr, "x(50)")
                output_list.str = output_list.str + \
                    to_string(debitor.vesrdep, "->,>>>,>>>,>>9.99")
                output_list.str = output_list.str + \
                    to_string(debitor.zahlkonto, ">>>>9")
                output_list.str = output_list.str + \
                    to_string(debitor.vesrdep, "->,>>>,>>>,>>9.99")
                output_list.str = output_list.str + \
                    to_string(artikel.bezeich, "x(40)")

                s_list.betrag = to_decimal(
                    s_list.betrag) + to_decimal(debitor.saldo)
        output_list = Output_list()
        output_list_data.append(output_list)

        for i in range(1, 58 + 1):
            output_list.str = output_list.str + "   "
        output_list.pay_amt = to_decimal(tot_saldo)
        output_list.pay_famt = to_decimal(tot_foreign)

        if not long_digit:
            output_list.str = output_list.str + "T O T A L " +\
                to_string(tot_saldo, "->,>>>,>>>,>>9.99") +\
                fill(" ", 78) +\
                to_string(tot_foreign, " ->>,>>>,>>>,>>9.99")
        else:
            output_list.str = output_list.str + "T O T A L " +\
                to_string(tot_saldo, " ->>>,>>>,>>>,>>9") +\
                fill(" ", 78) +\
                to_string(tot_foreign, "   ->>>,>>>,>>>,>>9")
        output_list = Output_list()
        output_list_data.append(output_list)

        output_list = Output_list()
        output_list_data.append(output_list)

        for i in range(1, 58 + 1):
            output_list.str = output_list.str + "   "
        output_list.pay_amt = to_decimal(t_credit)
        output_list.pay_famt = to_decimal(t_famt)

        if not long_digit:
            output_list.str = output_list.str + "Sub-Total " +\
                to_string(t_credit, "->,>>>,>>>,>>9.99") +\
                fill(" ", 78) +\
                to_string(t_famt, "->>,>>>,>>>,>>9.99")
        else:
            output_list.str = output_list.str + "Sub-Total " +\
                to_string(t_credit, " ->>>,>>>,>>>,>>9") +\
                fill(" ", 78) +\
                to_string(t_famt, "  ->>>,>>>,>>>,>>9")
        output_list = Output_list()
        output_list_data.append(output_list)

        output_list = Output_list()
        output_list_data.append(output_list)

        for i in range(1, 56 + 1):
            output_list.str = output_list.str + " "
        output_list.pay_amt = to_decimal(tot_credit)
        output_list.pay_famt = to_decimal(tot_famt)

        if not long_digit:
            output_list.str = output_list.str + "Grand TOTAL " +\
                to_string(tot_credit, "->,>>>,>>>,>>9.99") +\
                fill(" ", 78) + \
                to_string(tot_famt, "->>,>>>,>>>,>>9.99")
        else:
            output_list.str = output_list.str + "Grand TOTAL " +\
                to_string(tot_credit, " ->>>,>>>,>>>,>>9") +\
                fill(" ", 78) + \
                to_string(tot_famt, "  ->>>,>>>,>>>,>>9")
        create_tot_payment()

    def create_list2():

        nonlocal r_no, s_list_data, t_list_data, t_ar_paylist_data, long_digit, htparam, guest, debitor, artikel, bill, bediener, waehrung
        nonlocal comment, cledger, ccard, last_sort, from_date, to_date, from_art, to_art, mi_payment, mi_transfer, show_inv, bill_name, bill_nr
        nonlocal bguest, bdebitor

        nonlocal s_list, t_list, output_list, t_ar_paylist, bguest, bdebitor, tbuff, bq
        nonlocal s_list_data, t_list_data, output_list_data, t_ar_paylist_data

        artnr: int = 0
        i: int = 0
        curr_gastnr: int = 0
        t_credit: Decimal = to_decimal("0.0")
        tot_credit: Decimal = to_decimal("0.0")
        t_famt: Decimal = to_decimal("0.0")
        tot_famt: Decimal = to_decimal("0.0")
        tot_saldo: Decimal = to_decimal("0.0")
        tot_foreign: Decimal = to_decimal("0.0")
        receiver: string = ""
        do_it: bool = False
        temp_name: string = ""
        temp_vorname1: string = ""
        temp_anredefirma: string = ""
        temp_anrede1: string = ""
        debt = None
        art = None
        t_guest = None
        tstr: string = ""
        Debt = create_buffer("Debt", Debitor)
        Art = create_buffer("Art", Artikel)
        T_guest = create_buffer("T_guest", Guest)

        debitor_obj_list = {}
        debitor = Debitor()
        debt = Debitor()
        artikel = Artikel()
        art = Artikel()
        guest = Guest()
        for debitor.gastnr, debitor.saldo, debitor.zahlkonto, debitor.betriebsnr, debitor.counter, debitor.rechnr, debitor.debref, debitor.rgdatum, debitor.gastnrmember, debitor.bediener_nr, debitor.vesrcod, debitor.vesrdep, debitor.betrieb_gastmem, debitor._recid, debt.gastnr, debt.saldo, debt.zahlkonto, debt.betriebsnr, debt.counter, debt.rechnr, debt.debref, debt.rgdatum, debt.gastnrmember, debt.bediener_nr, debt.vesrcod, debt.vesrdep, debt.betrieb_gastmem, debt._recid, artikel.artnr, artikel.bezeich, artikel.artart, artikel._recid, art.artnr, art.bezeich, art.artart, art._recid, guest.name, guest.vorname1, guest.anredefirma, guest.anrede1, guest._recid in db_session.query(Debitor.gastnr, Debitor.saldo, Debitor.zahlkonto, Debitor.betriebsnr, Debitor.counter, Debitor.rechnr, Debitor.debref, Debitor.rgdatum, Debitor.gastnrmember, Debitor.bediener_nr, Debitor.vesrcod, Debitor.vesrdep, Debitor.betrieb_gastmem, Debitor._recid, Debt.gastnr, Debt.saldo, Debt.zahlkonto, Debt.betriebsnr, Debt.counter, Debt.rechnr, Debt.debref, Debt.rgdatum, Debt.gastnrmember, Debt.bediener_nr, Debt.vesrcod, Debt.vesrdep, Debt.betrieb_gastmem, Debt._recid, Artikel.artnr, Artikel.bezeich, Artikel.artart, Artikel._recid, Art.artnr, Art.bezeich, Art.artart, Art._recid, Guest.name, Guest.vorname1, Guest.anredefirma, Guest.anrede1, Guest._recid).join(Debt, (Debt.counter == Debitor.counter) & (Debt.zahlkonto == 0)).join(Artikel, (Artikel.artnr == Debitor.artnr) & (Artikel.departement == 0) & (Artikel.artart == 2)).join(Art, (Art.artnr == Debitor.zahlkonto) & (Art.departement == 0)).join(Guest, (Guest.gastnr == Debitor.gastnr)).filter(
                (Debitor.rgdatum >= from_date) & (Debitor.rgdatum <= to_date) & (Debitor.zahlkonto > 0) & (Debitor.artnr >= from_art) & (Debitor.artnr <= to_art) & (Debitor.counter > 0) & (Debitor.opart > 0)).order_by(Artikel.artnr, Debitor.name, Debitor.gastnr, Debitor.rgdatum, Debitor.zahlkonto, Debitor.betriebsnr, Debitor.rechnr).all():
            if debitor_obj_list.get(debitor._recid):
                continue
            else:
                debitor_obj_list[debitor._recid] = True

            do_it = True

            if mi_payment:

                if artikel.artart == 2 and art.artart != 4 and art.artart != 7:
                    do_it = False

                elif artikel.artart == 7 and art.artart != 4:
                    do_it = False

            elif mi_transfer:

                if artikel.artart == 2 and (art.artart == 4 or art.artart == 7):
                    do_it = False

                elif artikel.artart == 7 and art.artart == 4:
                    do_it = False

            if do_it and (bill_name != "") and (substring(bill_name, 0, 1) != ("*").lower()):

                if not matches(guest.name, r"*" + bill_name + r"*"):
                    do_it = False

            if do_it and (bill_name != "") and (substring(bill_name, 0, 1) == ("*").lower()):

                if not matches(guest.name, bill_name):
                    do_it = False

            if do_it:

                if curr_gastnr == 0:
                    curr_gastnr = debitor.gastnr

                if curr_gastnr != debitor.gastnr:
                    curr_gastnr = debitor.gastnr
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    for i in range(1, 58 + 1):
                        output_list.str = output_list.str + "   "
                    output_list.pay_amt = to_decimal(tot_saldo)
                    output_list.pay_famt = to_decimal(tot_foreign)

                    if not long_digit:
                        output_list.str = output_list.str + "T O T A L " +\
                            to_string(tot_saldo, "->,>>>,>>>,>>9.99") +\
                            fill(" ", 78) +\
                            to_string(tot_foreign, " ->>,>>>,>>>,>>9.99")
                    else:
                        output_list.str = output_list.str + "T O T A L " +\
                            to_string(tot_saldo, " ->>>,>>>,>>>,>>9") +\
                            fill(" ", 78) +\
                            to_string(tot_foreign, "   ->>>,>>>,>>>,>>9")
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    tot_saldo = to_decimal("0")
                    tot_foreign = to_decimal("0")

                if artnr != artikel.artnr:
                    t_list = T_list()
                    t_list_data.append(t_list)

                    t_list.artnr = artikel.artnr
                    t_list.bezeich = artikel.bezeich

                    if artnr != 0:
                        output_list = Output_list()
                        output_list_data.append(output_list)

                        for i in range(1, 58 + 1):
                            output_list.str = output_list.str + "   "
                        output_list.pay_amt = to_decimal(t_credit)
                        output_list.pay_famt = to_decimal(t_famt)

                        if not long_digit:
                            output_list.str = output_list.str + "Sub-Total " +\
                                to_string(t_credit, "->,>>>,>>>,>>9.99") +\
                                fill(" ", 78) +\
                                to_string(t_famt, "->>,>>>,>>>,>>9.99")
                        else:
                            output_list.str = output_list.str + "Sub-Total " +\
                                to_string(t_credit, " ->>>,>>>,>>>,>>9") +\
                                fill(" ", 78) +\
                                to_string(t_famt, "  ->>>,>>>,>>>,>>9")
                        output_list = Output_list()
                        output_list_data.append(output_list)

                        t_credit = to_decimal("0")
                        t_famt = to_decimal("0")
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    for i in range(1, 19 + 1):
                        output_list.str = output_list.str + " "
                    output_list.str = output_list.str +\
                        to_string(artikel.artnr, ">>>>9") + " - " +\
                        to_string(artikel.bezeich, "x(24)")
                    artnr = artikel.artnr
                t_list.betrag = to_decimal(
                    t_list.betrag) - to_decimal(debitor.saldo)

                if guest.name != None:
                    temp_name = guest.name

                else:
                    temp_name = ""

                if guest.vorname1 != None:
                    temp_vorname1 = guest.vorname1

                else:
                    temp_vorname1 = ""

                if guest.anredefirma != None:
                    temp_anredefirma = guest.anredefirma

                else:
                    temp_anredefirma = ""

                if guest.anrede1 != None:
                    temp_anrede1 = guest.anrede1

                else:
                    temp_anrede1 = ""
                receiver = substring(f"{temp_name}, {temp_vorname1} {temp_anredefirma}{temp_anrede1}", 0, 32)
                output_list = Output_list()
                output_list_data.append(output_list)

                output_list.bill_art = artikel.artnr
                output_list.debt_counter = debitor.counter
                output_list.famt = to_string(
                    debt.vesrdep, "->>,>>>,>>>,>>9.99")

                if show_inv:

                    bill = get_cache(Bill, {"rechnr": [(eq, debitor.rechnr)]})

                    if bill:
                        output_list.inv_no = to_string(
                            bill.rechnr2, ">>>>>>>>>")

                        if bill.billref != 0:
                            output_list.soa_inv = "INV" + \
                                to_string(bill.billref, "9999999")
                    else:

                        bdebitor = get_cache(
                            Debitor, {"rechnr": [(eq, debitor.rechnr)], "debref": [(gt, 0)]})

                        if bdebitor:
                            output_list.soa_inv = "INV" + \
                                to_string(debitor.debref, "9999999")

                output_list.pay_amt = to_decimal(debitor.saldo)
                output_list.pay_famt = to_decimal(debitor.vesrdep)

                if not long_digit:
                    output_list.str = to_string(debt.rgdatum) +\
                        to_string(debitor.rechnr, ">>>,>>>,>>9") +\
                        to_string(receiver, "x(32)") +\
                        to_string(debt.saldo, "->,>>>,>>>,>>9.99") +\
                        to_string(debitor.saldo, "->,>>>,>>>,>>9.99") +\
                        to_string(art.bezeich, "x(34)") +\
                        to_string(debitor.rgdatum)
                else:
                    output_list.str = to_string(debt.rgdatum) +\
                        to_string(debitor.rechnr, ">>>,>>>,>>9") +\
                        to_string(receiver, "x(32)") +\
                        to_string(debt.saldo, " ->>>,>>>,>>>,>>9") +\
                        to_string(debitor.saldo, " ->>>,>>>,>>>,>>9") +\
                        to_string(art.bezeich, "x(34)") +\
                        to_string(debitor.rgdatum)
                output_list.bill_num = debitor.rechnr
                output_list.art_bezeich = artikel.bezeich
                output_list.tbetrag = to_decimal(
                    output_list.tbetrag) - to_decimal(debitor.saldo)

                bguest = get_cache(
                    Guest, {"gastnr": [(eq, debitor.gastnrmember)]})

                if bguest:
                    output_list.gastname = substring(f"{bguest.name}, {bguest.vorname1}{bguest.anredefirma} {bguest.anrede1}", 0, 32)

                bediener = get_cache(
                    Bediener, {"nr": [(eq, debitor.bediener_nr)]})

                if bediener:
                    output_list.str = output_list.str + \
                        to_string(bediener.userinit, "x(3)")
                else:
                    output_list.str = output_list.str + "   "
                output_list.str = output_list.str + \
                    to_string(debitor.vesrcod, "x(34)")
                output_list.str = output_list.str + to_string(" ", "x(22)")

                t_guest = get_cache(
                    Guest, {"gastnr": [(eq, debt.gastnrmember)]})

                if t_guest:
                    tstr = substring(f"{t_guest.name}, {t_guest.vorname1}{t_guest.anrede1}", 0, 34)
                else:
                    tstr = " "
                output_list.str = output_list.str + to_string(tstr, "x(50)")
                output_list.str = output_list.str + \
                    to_string(debitor.vesrdep, "->,>>>,>>>,>>9.99")
                output_list.str = output_list.str + \
                    to_string(debitor.zahlkonto, ">>>>9")
                output_list.str = output_list.str + \
                    to_string(debitor.vesrdep, "->,>>>,>>>,>>9.99")
                output_list.str = output_list.str + \
                    to_string(artikel.bezeich, "x(40)")

                t_credit = to_decimal(t_credit) + to_decimal(debitor.saldo)
                t_famt = to_decimal(t_famt) + to_decimal(debitor.vesrdep)
                tot_credit = to_decimal(tot_credit) + to_decimal(debitor.saldo)
                tot_saldo = to_decimal(tot_saldo) + to_decimal(debitor.saldo)
                tot_foreign = to_decimal(
                    tot_foreign) + to_decimal(debitor.vesrdep)
                tot_famt = to_decimal(tot_famt) + to_decimal(debitor.vesrdep)

                s_list = query(s_list_data, filters=(
                    lambda s_list: s_list.artnr == art.artnr), first=True)

                if not s_list:
                    s_list = S_list()
                    s_list_data.append(s_list)

                    s_list.artnr = art.artnr
                    s_list.bezeich = art.bezeich
                s_list.betrag = to_decimal(
                    s_list.betrag) + to_decimal(debitor.saldo)
        output_list = Output_list()
        output_list_data.append(output_list)

        for i in range(1, 58 + 1):
            output_list.str = output_list.str + "   "
        output_list.pay_amt = to_decimal(tot_saldo)
        output_list.pay_famt = to_decimal(tot_foreign)

        if not long_digit:
            output_list.str = output_list.str + "T O T A L " +\
                to_string(tot_saldo, "->,>>>,>>>,>>9.99") +\
                fill(" ", 78) +\
                to_string(tot_foreign, " ->>,>>>,>>>,>>9.99")
        else:
            output_list.str = output_list.str + "T O T A L " +\
                to_string(tot_saldo, " ->>>,>>>,>>>,>>9") +\
                fill(" ", 78) +\
                to_string(tot_foreign, "   ->>>,>>>,>>>,>>9")
        output_list = Output_list()
        output_list_data.append(output_list)

        output_list = Output_list()
        output_list_data.append(output_list)

        for i in range(1, 58 + 1):
            output_list.str = output_list.str + "   "
        output_list.pay_amt = to_decimal(t_credit)
        output_list.pay_famt = to_decimal(t_famt)

        if not long_digit:
            output_list.str = output_list.str + "Sub-Total " +\
                to_string(t_credit, "->,>>>,>>>,>>9.99") +\
                fill(" ", 78) +\
                to_string(t_famt, "->>,>>>,>>>,>>9.99")
        else:
            output_list.str = output_list.str + "Sub-Total " +\
                to_string(t_credit, " ->>>,>>>,>>>,>>9") +\
                fill(" ", 78) +\
                to_string(t_famt, "  ->>>,>>>,>>>,>>9")
        output_list = Output_list()
        output_list_data.append(output_list)

        output_list = Output_list()
        output_list_data.append(output_list)

        for i in range(1, 56 + 1):
            output_list.str = output_list.str + " "
        output_list.pay_amt = to_decimal(tot_credit)
        output_list.pay_famt = to_decimal(tot_famt)

        if not long_digit:
            output_list.str = output_list.str + "Grand TOTAL " +\
                to_string(tot_credit, "->,>>>,>>>,>>9.99") +\
                fill(" ", 78) + \
                to_string(tot_famt, "->>,>>>,>>>,>>9.99")
        else:
            output_list.str = output_list.str + "Grand TOTAL " +\
                to_string(tot_credit, " ->>>,>>>,>>>,>>9") +\
                fill(" ", 78) + \
                to_string(tot_famt, "  ->>>,>>>,>>>,>>9")
        create_tot_payment()

    def create_list2a():

        nonlocal r_no, s_list_data, t_list_data, t_ar_paylist_data, long_digit, htparam, guest, debitor, artikel, bill, bediener, waehrung
        nonlocal comment, cledger, ccard, last_sort, from_date, to_date, from_art, to_art, mi_payment, mi_transfer, show_inv, bill_name, bill_nr
        nonlocal bguest, bdebitor

        nonlocal s_list, t_list, output_list, t_ar_paylist, bguest, bdebitor, tbuff, bq
        nonlocal s_list_data, t_list_data, output_list_data, t_ar_paylist_data

        artnr: int = 0
        i: int = 0
        curr_gastnr: int = 0
        t_credit: Decimal = to_decimal("0.0")
        tot_credit: Decimal = to_decimal("0.0")
        t_famt: Decimal = to_decimal("0.0")
        tot_famt: Decimal = to_decimal("0.0")
        tot_saldo: Decimal = to_decimal("0.0")
        tot_foreign: Decimal = to_decimal("0.0")
        receiver: string = ""
        do_it: bool = False
        temp_name: string = ""
        temp_vorname1: string = ""
        temp_anredefirma: string = ""
        temp_anrede1: string = ""
        debt = None
        art = None
        t_guest = None
        tstr: string = ""
        Debt = create_buffer("Debt", Debitor)
        Art = create_buffer("Art", Artikel)
        T_guest = create_buffer("T_guest", Guest)

        debitor_obj_list = {}
        debitor = Debitor()
        debt = Debitor()
        artikel = Artikel()
        art = Artikel()
        guest = Guest()
        for debitor.gastnr, debitor.saldo, debitor.zahlkonto, debitor.betriebsnr, debitor.counter, debitor.rechnr, debitor.debref, debitor.rgdatum, debitor.gastnrmember, debitor.bediener_nr, debitor.vesrcod, debitor.vesrdep, debitor.betrieb_gastmem, debitor._recid, debt.gastnr, debt.saldo, debt.zahlkonto, debt.betriebsnr, debt.counter, debt.rechnr, debt.debref, debt.rgdatum, debt.gastnrmember, debt.bediener_nr, debt.vesrcod, debt.vesrdep, debt.betrieb_gastmem, debt._recid, artikel.artnr, artikel.bezeich, artikel.artart, artikel._recid, art.artnr, art.bezeich, art.artart, art._recid, guest.name, guest.vorname1, guest.anredefirma, guest.anrede1, guest._recid in db_session.query(Debitor.gastnr, Debitor.saldo, Debitor.zahlkonto, Debitor.betriebsnr, Debitor.counter, Debitor.rechnr, Debitor.debref, Debitor.rgdatum, Debitor.gastnrmember, Debitor.bediener_nr, Debitor.vesrcod, Debitor.vesrdep, Debitor.betrieb_gastmem, Debitor._recid, Debt.gastnr, Debt.saldo, Debt.zahlkonto, Debt.betriebsnr, Debt.counter, Debt.rechnr, Debt.debref, Debt.rgdatum, Debt.gastnrmember, Debt.bediener_nr, Debt.vesrcod, Debt.vesrdep, Debt.betrieb_gastmem, Debt._recid, Artikel.artnr, Artikel.bezeich, Artikel.artart, Artikel._recid, Art.artnr, Art.bezeich, Art.artart, Art._recid, Guest.name, Guest.vorname1, Guest.anredefirma, Guest.anrede1, Guest._recid).join(Debt, (Debt.counter == Debitor.counter) & (Debt.zahlkonto == 0)).join(Artikel, (Artikel.artnr == Debitor.artnr) & (Artikel.departement == 0) & (Artikel.artart == 2)).join(Art, (Art.artnr == Debitor.zahlkonto) & (Art.departement == 0)).join(Guest, (Guest.gastnr == Debitor.gastnr)).filter(
                (Debitor.rgdatum >= from_date) & (Debitor.rgdatum <= to_date) & (Debitor.zahlkonto > 0) & (Debitor.artnr >= from_art) & (Debitor.artnr <= to_art) & (Debitor.counter > 0) & (Debitor.opart > 0)).order_by(Artikel.artnr, Debitor.zahlkonto, Debitor.name, Debitor.rgdatum, Debitor.rechnr).all():
            if debitor_obj_list.get(debitor._recid):
                continue
            else:
                debitor_obj_list[debitor._recid] = True

            do_it = True

            if mi_payment:

                if artikel.artart == 2 and art.artart != 4 and art.artart != 7:
                    do_it = False

                elif artikel.artart == 7 and art.artart != 4:
                    do_it = False

            elif mi_transfer:

                if artikel.artart == 2 and (art.artart == 4 or art.artart == 7):
                    do_it = False

                elif artikel.artart == 7 and art.artart == 4:
                    do_it = False

            if do_it and (bill_name != "") and (substring(bill_name, 0, 1) != ("*").lower()):

                if not matches(guest.name, r"*" + bill_name + r"*"):
                    do_it = False

            if do_it and (bill_name != "") and (substring(bill_name, 0, 1) == ("*").lower()):

                if not matches(guest.name, bill_name):
                    do_it = False

            if do_it:

                if curr_gastnr == 0:
                    curr_gastnr = debitor.zahlkonto

                if curr_gastnr != debitor.zahlkonto:
                    curr_gastnr = debitor.zahlkonto
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    for i in range(1, 58 + 1):
                        output_list.str = output_list.str + "   "
                    output_list.pay_amt = to_decimal(tot_saldo)
                    output_list.pay_famt = to_decimal(tot_foreign)

                    if not long_digit:
                        output_list.str = output_list.str + "T O T A L " +\
                            to_string(tot_saldo, "->,>>>,>>>,>>9.99") +\
                            fill(" ", 78) +\
                            to_string(tot_foreign, " ->>,>>>,>>>,>>9.99")
                    else:
                        output_list.str = output_list.str + "T O T A L " +\
                            to_string(tot_saldo, " ->>>,>>>,>>>,>>9") +\
                            fill(" ", 78) +\
                            to_string(tot_foreign, "   ->>>,>>>,>>>,>>9")
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    tot_saldo = to_decimal("0")
                    tot_foreign = to_decimal("0")

                if artnr != artikel.artnr:
                    t_list = T_list()
                    t_list_data.append(t_list)

                    t_list.artnr = artikel.artnr
                    t_list.bezeich = artikel.bezeich

                    if artnr != 0:
                        output_list = Output_list()
                        output_list_data.append(output_list)

                        for i in range(1, 58 + 1):
                            output_list.str = output_list.str + "   "
                        output_list.pay_amt = to_decimal(t_credit)
                        output_list.pay_famt = to_decimal(t_famt)

                        if not long_digit:
                            output_list.str = output_list.str + "Sub-Total " +\
                                to_string(t_credit, "->,>>>,>>>,>>9.99") +\
                                fill(" ", 78) +\
                                to_string(t_famt, "->>,>>>,>>>,>>9.99")
                        else:
                            output_list.str = output_list.str + "Sub-Total " +\
                                to_string(t_credit, " ->>>,>>>,>>>,>>9") +\
                                fill(" ", 78) +\
                                to_string(t_famt, "  ->>>,>>>,>>>,>>9")
                        output_list = Output_list()
                        output_list_data.append(output_list)

                        t_credit = to_decimal("0")
                        t_famt = to_decimal("0")
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    for i in range(1, 19 + 1):
                        output_list.str = output_list.str + " "
                    output_list.str = output_list.str +\
                        to_string(artikel.artnr, ">>>>9") + " - " +\
                        to_string(artikel.bezeich, "x(34)")
                    artnr = artikel.artnr
                t_list.betrag = to_decimal(
                    t_list.betrag) - to_decimal(debitor.saldo)

                if guest.name != None:
                    temp_name = guest.name

                else:
                    temp_name = ""

                if guest.vorname1 != None:
                    temp_vorname1 = guest.vorname1

                else:
                    temp_vorname1 = ""

                if guest.anredefirma != None:
                    temp_anredefirma = guest.anredefirma

                else:
                    temp_anredefirma = ""

                if guest.anrede1 != None:
                    temp_anrede1 = guest.anrede1

                else:
                    temp_anrede1 = ""
                receiver = substring(f"{temp_name}, {temp_vorname1} {temp_anredefirma}{temp_anrede1}", 0, 32)
                output_list = Output_list()
                output_list_data.append(output_list)

                output_list.bill_art = artikel.artnr
                output_list.debt_counter = debitor.counter
                output_list.famt = to_string(
                    debt.vesrdep, "->>,>>>,>>>,>>9.99")

                if show_inv:

                    bill = get_cache(Bill, {"rechnr": [(eq, debitor.rechnr)]})

                    if bill:
                        output_list.inv_no = to_string(
                            bill.rechnr2, ">>>>>>>>>")

                        if bill.billref != 0:
                            output_list.soa_inv = "INV" + \
                                to_string(bill.billref, "9999999")
                    else:

                        bdebitor = get_cache(
                            Debitor, {"rechnr": [(eq, debitor.rechnr)], "debref": [(gt, 0)]})

                        if bdebitor:
                            output_list.soa_inv = "INV" + \
                                to_string(debitor.debref, "9999999")

                output_list.pay_amt = to_decimal(debitor.saldo)
                output_list.pay_famt = to_decimal(debitor.vesrdep)

                if not long_digit:
                    output_list.str = to_string(debt.rgdatum) +\
                        to_string(debitor.rechnr, ">>>,>>>,>>9") +\
                        to_string(receiver, "x(32)") +\
                        to_string(debt.saldo, "->,>>>,>>>,>>9.99") +\
                        to_string(debitor.saldo, "->,>>>,>>>,>>9.99") +\
                        to_string(art.bezeich, "x(34)") +\
                        to_string(debitor.rgdatum)
                else:
                    output_list.str = to_string(debt.rgdatum) +\
                        to_string(debitor.rechnr, ">>>,>>>,>>9") +\
                        to_string(receiver, "x(32)") +\
                        to_string(debt.saldo, " ->>>,>>>,>>>,>>9") +\
                        to_string(debitor.saldo, " ->>>,>>>,>>>,>>9") +\
                        to_string(art.bezeich, "x(34)") +\
                        to_string(debitor.rgdatum)
                output_list.bill_num = debitor.rechnr
                output_list.art_bezeich = artikel.bezeich
                output_list.tbetrag = to_decimal(
                    output_list.tbetrag) - to_decimal(debitor.saldo)

                bguest = get_cache(
                    Guest, {"gastnr": [(eq, debitor.gastnrmember)]})

                if bguest:
                    output_list.gastname = substring(f"{bguest.name}, {bguest.vorname1}{bguest.anredefirma} {bguest.anrede1}", 0, 32)

                bediener = get_cache(
                    Bediener, {"nr": [(eq, debitor.bediener_nr)]})

                if bediener:
                    output_list.str = output_list.str + \
                        to_string(bediener.userinit, "x(3)")
                else:
                    output_list.str = output_list.str + "   "
                output_list.str = output_list.str + \
                    to_string(debitor.vesrcod, "x(34)")
                output_list.str = output_list.str + to_string(" ", "x(22)")

                t_guest = get_cache(
                    Guest, {"gastnr": [(eq, debt.gastnrmember)]})

                if t_guest:
                    tstr = substring(f"{t_guest.name}, {t_guest.vorname1}{t_guest.anrede1}", 0, 34)
                else:
                    tstr = " "
                output_list.str = output_list.str + to_string(tstr, "x(50)")
                output_list.str = output_list.str + \
                    to_string(debitor.vesrdep, "->,>>>,>>>,>>9.99")
                output_list.str = output_list.str + \
                    to_string(debitor.zahlkonto, ">>>>9")
                output_list.str = output_list.str + \
                    to_string(debitor.vesrdep, "->,>>>,>>>,>>9.99")
                output_list.str = output_list.str + \
                    to_string(artikel.bezeich, "x(40)")

                t_credit = to_decimal(t_credit) + to_decimal(debitor.saldo)
                t_famt = to_decimal(t_famt) + to_decimal(debitor.vesrdep)
                tot_credit = to_decimal(tot_credit) + to_decimal(debitor.saldo)
                tot_saldo = to_decimal(tot_saldo) + to_decimal(debitor.saldo)
                tot_foreign = to_decimal(
                    tot_foreign) + to_decimal(debitor.vesrdep)
                tot_famt = to_decimal(tot_famt) + to_decimal(debitor.vesrdep)

                s_list = query(s_list_data, filters=(
                    lambda s_list: s_list.artnr == art.artnr), first=True)

                if not s_list:
                    s_list = S_list()
                    s_list_data.append(s_list)

                    s_list.artnr = art.artnr
                    s_list.bezeich = art.bezeich
                s_list.betrag = to_decimal(
                    s_list.betrag) + to_decimal(debitor.saldo)
        output_list = Output_list()
        output_list_data.append(output_list)

        for i in range(1, 58 + 1):
            output_list.str = output_list.str + "   "
        output_list.pay_amt = to_decimal(tot_saldo)
        output_list.pay_famt = to_decimal(tot_foreign)

        if not long_digit:
            output_list.str = output_list.str + "T O T A L " +\
                to_string(tot_saldo, "->,>>>,>>>,>>9.99") +\
                fill(" ", 78) +\
                to_string(tot_foreign, " ->>,>>>,>>>,>>9.99")
        else:
            output_list.str = output_list.str + "T O T A L " +\
                to_string(tot_saldo, " ->>>,>>>,>>>,>>9") +\
                fill(" ", 78) +\
                to_string(tot_foreign, "   ->>>,>>>,>>>,>>9")
        output_list = Output_list()
        output_list_data.append(output_list)

        output_list = Output_list()
        output_list_data.append(output_list)

        for i in range(1, 58 + 1):
            output_list.str = output_list.str + "   "
        output_list.pay_amt = to_decimal(t_credit)
        output_list.pay_famt = to_decimal(t_famt)

        if not long_digit:
            output_list.str = output_list.str + "Sub-Total " +\
                to_string(t_credit, "->,>>>,>>>,>>9.99") +\
                fill(" ", 78) +\
                to_string(t_famt, "->>,>>>,>>>,>>9.99")
        else:
            output_list.str = output_list.str + "Sub-Total " +\
                to_string(t_credit, " ->>>,>>>,>>>,>>9") +\
                fill(" ", 78) +\
                to_string(t_famt, "  ->>>,>>>,>>>,>>9")
        output_list = Output_list()
        output_list_data.append(output_list)

        output_list = Output_list()
        output_list_data.append(output_list)

        for i in range(1, 56 + 1):
            output_list.str = output_list.str + " "
        output_list.pay_amt = to_decimal(tot_credit)
        output_list.pay_famt = to_decimal(tot_famt)

        if not long_digit:
            output_list.str = output_list.str + "Grand TOTAL " +\
                to_string(tot_credit, "->,>>>,>>>,>>9.99") +\
                fill(" ", 78) + \
                to_string(tot_famt, "->>,>>>,>>>,>>9.99")
        else:
            output_list.str = output_list.str + "Grand TOTAL " +\
                to_string(tot_credit, " ->>>,>>>,>>>,>>9") +\
                fill(" ", 78) + \
                to_string(tot_famt, "  ->>>,>>>,>>>,>>9")

    def create_list3():

        nonlocal r_no, s_list_data, t_list_data, t_ar_paylist_data, long_digit, htparam, guest, debitor, artikel, bill, bediener, waehrung
        nonlocal comment, cledger, ccard, last_sort, from_date, to_date, from_art, to_art, mi_payment, mi_transfer, show_inv, bill_name, bill_nr
        nonlocal bguest, bdebitor

        nonlocal s_list, t_list, output_list, t_ar_paylist, bguest, bdebitor, tbuff, bq
        nonlocal s_list_data, t_list_data, output_list_data, t_ar_paylist_data

        artnr: int = 0
        i: int = 0
        curr_gastnr: int = 0
        t_credit: Decimal = to_decimal("0.0")
        tot_credit: Decimal = to_decimal("0.0")
        t_famt: Decimal = to_decimal("0.0")
        tot_famt: Decimal = to_decimal("0.0")
        tot_saldo: Decimal = to_decimal("0.0")
        tot_foreign: Decimal = to_decimal("0.0")
        receiver: string = ""
        do_it: bool = False
        temp_name: string = ""
        temp_vorname1: string = ""
        temp_anredefirma: string = ""
        temp_anrede1: string = ""
        debt = None
        art = None
        t_guest = None
        tstr: string = ""
        Debt = create_buffer("Debt", Debitor)
        Art = create_buffer("Art", Artikel)
        T_guest = create_buffer("T_guest", Guest)

        debitor_obj_list = {}
        debitor = Debitor()
        debt = Debitor()
        artikel = Artikel()
        art = Artikel()
        guest = Guest()
        for debitor.gastnr, debitor.saldo, debitor.zahlkonto, debitor.betriebsnr, debitor.counter, debitor.rechnr, debitor.debref, debitor.rgdatum, debitor.gastnrmember, debitor.bediener_nr, debitor.vesrcod, debitor.vesrdep, debitor.betrieb_gastmem, debitor._recid, debt.gastnr, debt.saldo, debt.zahlkonto, debt.betriebsnr, debt.counter, debt.rechnr, debt.debref, debt.rgdatum, debt.gastnrmember, debt.bediener_nr, debt.vesrcod, debt.vesrdep, debt.betrieb_gastmem, debt._recid, artikel.artnr, artikel.bezeich, artikel.artart, artikel._recid, art.artnr, art.bezeich, art.artart, art._recid, guest.name, guest.vorname1, guest.anredefirma, guest.anrede1, guest._recid in db_session.query(Debitor.gastnr, Debitor.saldo, Debitor.zahlkonto, Debitor.betriebsnr, Debitor.counter, Debitor.rechnr, Debitor.debref, Debitor.rgdatum, Debitor.gastnrmember, Debitor.bediener_nr, Debitor.vesrcod, Debitor.vesrdep, Debitor.betrieb_gastmem, Debitor._recid, Debt.gastnr, Debt.saldo, Debt.zahlkonto, Debt.betriebsnr, Debt.counter, Debt.rechnr, Debt.debref, Debt.rgdatum, Debt.gastnrmember, Debt.bediener_nr, Debt.vesrcod, Debt.vesrdep, Debt.betrieb_gastmem, Debt._recid, Artikel.artnr, Artikel.bezeich, Artikel.artart, Artikel._recid, Art.artnr, Art.bezeich, Art.artart, Art._recid, Guest.name, Guest.vorname1, Guest.anredefirma, Guest.anrede1, Guest._recid).join(Debt, (Debt.counter == Debitor.counter) & (Debt.zahlkonto == 0)).join(Artikel, (Artikel.artnr == Debitor.artnr) & (Artikel.departement == 0) & (Artikel.artart == 7)).join(Art, (Art.artnr == Debitor.zahlkonto) & (Art.departement == 0)).join(Guest, (Guest.gastnr == Debitor.gastnr)).filter(
                (Debitor.rgdatum >= from_date) & (Debitor.rgdatum <= to_date) & (Debitor.zahlkonto > 0) & (Debitor.artnr >= from_art) & (Debitor.artnr <= to_art) & (Debitor.counter > 0) & (Debitor.opart > 0)).order_by(Artikel.artnr, Debitor.name, Debitor.gastnr, Debitor.rgdatum, Debitor.zahlkonto, Debitor.betriebsnr, Debitor.rechnr).all():
            if debitor_obj_list.get(debitor._recid):
                continue
            else:
                debitor_obj_list[debitor._recid] = True

            do_it = True

            if mi_payment:

                if artikel.artart == 2 and art.artart != 4 and art.artart != 7:
                    do_it = False

                elif artikel.artart == 7 and art.artart != 4:
                    do_it = False

            elif mi_transfer:

                if artikel.artart == 2 and (art.artart == 4 or art.artart == 7):
                    do_it = False

                elif artikel.artart == 7 and art.artart == 4:
                    do_it = False

            if do_it:

                if curr_gastnr == 0:
                    curr_gastnr = debitor.gastnr

                if curr_gastnr != debitor.gastnr:
                    curr_gastnr = debitor.gastnr
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    for i in range(1, 58 + 1):
                        output_list.str = output_list.str + "   "
                    output_list.pay_amt = to_decimal(tot_saldo)
                    output_list.pay_famt = to_decimal(tot_foreign)

                    if not long_digit:
                        output_list.str = output_list.str + "T O T A L " +\
                            to_string(tot_saldo, "->,>>>,>>>,>>9.99") +\
                            fill(" ", 78) +\
                            to_string(tot_foreign, " ->>,>>>,>>>,>>9.99")
                    else:
                        output_list.str = output_list.str + "T O T A L " +\
                            to_string(tot_saldo, " ->>>,>>>,>>>,>>9") +\
                            fill(" ", 78) +\
                            to_string(tot_foreign, "   ->>>,>>>,>>>,>>9")
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    tot_saldo = to_decimal("0")
                    tot_foreign = to_decimal("0")

                if artnr != artikel.artnr:
                    t_list = T_list()
                    t_list_data.append(t_list)

                    t_list.artnr = artikel.artnr
                    t_list.bezeich = artikel.bezeich

                    if artnr != 0:

                        if tot_saldo != 0:
                            output_list = Output_list()
                            output_list_data.append(output_list)

                            for i in range(1, 58 + 1):
                                output_list.str = output_list.str + "   "
                            output_list.pay_amt = to_decimal(tot_saldo)
                            output_list.pay_famt = to_decimal(tot_foreign)

                            if not long_digit:
                                output_list.str = output_list.str + "T O T A L " +\
                                    to_string(tot_saldo, "->,>>>,>>>,>>9.99") +\
                                    fill(" ", 78) +\
                                    to_string(tot_foreign, " ->>,>>>,>>>,>>9.99")
                            else:
                                output_list.str = output_list.str + "T O T A L " +\
                                    to_string(tot_saldo, " ->>>,>>>,>>>,>>9") +\
                                    fill(" ", 78) +\
                                    to_string(tot_foreign, "   ->>>,>>>,>>>,>>9")
                            output_list = Output_list()
                            output_list_data.append(output_list)

                            tot_saldo = to_decimal("0")
                            tot_foreign = to_decimal("0")
                        output_list = Output_list()
                        output_list_data.append(output_list)

                        for i in range(1, 58 + 1):
                            output_list.str = output_list.str + "   "
                        output_list.pay_amt = to_decimal(t_credit)
                        output_list.pay_famt = to_decimal(t_famt)

                        if not long_digit:
                            output_list.str = output_list.str + "Sub-Total " +\
                                to_string(t_credit, "->,>>>,>>>,>>9.99") +\
                                fill(" ", 78) +\
                                to_string(t_famt, "->>,>>>,>>>,>>9.99")
                        else:
                            output_list.str = output_list.str + "Sub-Total " +\
                                to_string(t_credit, " ->>>,>>>,>>>,>>9") +\
                                fill(" ", 78) +\
                                to_string(t_famt, "  ->>>,>>>,>>>,>>9")
                        output_list = Output_list()
                        output_list_data.append(output_list)

                        t_credit = to_decimal("0")
                        t_famt = to_decimal("0")
                        tot_saldo = to_decimal("0")
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    for i in range(1, 19 + 1):
                        output_list.str = output_list.str + " "
                    output_list.str = output_list.str +\
                        to_string(artikel.artnr, ">>>>9") + " - " +\
                        to_string(artikel.bezeich, "x(34)")
                    artnr = artikel.artnr
                t_list.betrag = to_decimal(
                    t_list.betrag) - to_decimal(debitor.saldo)

                if guest.name != None:
                    temp_name = guest.name

                else:
                    temp_name = ""

                if guest.vorname1 != None:
                    temp_vorname1 = guest.vorname1

                else:
                    temp_vorname1 = ""

                if guest.anredefirma != None:
                    temp_anredefirma = guest.anredefirma

                else:
                    temp_anredefirma = ""

                if guest.anrede1 != None:
                    temp_anrede1 = guest.anrede1

                else:
                    temp_anrede1 = ""
                receiver = substring(f"{temp_name}, {temp_vorname1} {temp_anredefirma}{temp_anrede1}", 0, 32)
                output_list = Output_list()
                output_list_data.append(output_list)

                output_list.bill_art = artikel.artnr
                output_list.debt_counter = debitor.counter
                output_list.famt = to_string(
                    debt.vesrdep, "->>,>>>,>>>,>>9.99")

                if show_inv:

                    bill = get_cache(Bill, {"rechnr": [(eq, debitor.rechnr)]})

                    if bill:
                        output_list.inv_no = to_string(
                            bill.rechnr2, ">>>>>>>>>")

                        if bill.billref != 0:
                            output_list.soa_inv = "INV" + \
                                to_string(bill.billref, "9999999")
                    else:

                        bdebitor = get_cache(
                            Debitor, {"rechnr": [(eq, debitor.rechnr)], "debref": [(gt, 0)]})

                        if bdebitor:
                            output_list.soa_inv = "INV" + \
                                to_string(debitor.debref, "9999999")

                output_list.pay_amt = to_decimal(debitor.saldo)
                output_list.pay_famt = to_decimal(debitor.vesrdep)

                if not long_digit:
                    output_list.str = to_string(debt.rgdatum) +\
                        to_string(debitor.rechnr, ">>>,>>>,>>9") +\
                        to_string(receiver, "x(32)") +\
                        to_string(debt.saldo, "->,>>>,>>>,>>9.99") +\
                        to_string(debitor.saldo, "->,>>>,>>>,>>9.99") +\
                        to_string(art.bezeich, "x(34)") +\
                        to_string(debitor.rgdatum)
                else:
                    output_list.str = to_string(debt.rgdatum) +\
                        to_string(debitor.rechnr, ">>>,>>>,>>9") +\
                        to_string(receiver, "x(32)") +\
                        to_string(debt.saldo, " ->>>,>>>,>>>,>>9") +\
                        to_string(debitor.saldo, " ->>>,>>>,>>>,>>9") +\
                        to_string(art.bezeich, "x(34)") +\
                        to_string(debitor.rgdatum)
                output_list.bill_num = debitor.rechnr
                output_list.art_bezeich = artikel.bezeich
                output_list.tbetrag = to_decimal(
                    output_list.tbetrag) - to_decimal(debitor.saldo)

                bguest = get_cache(
                    Guest, {"gastnr": [(eq, debitor.gastnrmember)]})

                if bguest:
                    output_list.gastname = substring(f"{bguest.name}, {bguest.vorname1}{bguest.anredefirma} {bguest.anrede1}", 0, 32)

                bediener = get_cache(
                    Bediener, {"nr": [(eq, debitor.bediener_nr)]})

                if bediener:
                    output_list.str = output_list.str + \
                        to_string(bediener.userinit, "x(3)")
                else:
                    output_list.str = output_list.str + "   "
                output_list.str = output_list.str + \
                    to_string(debitor.vesrcod, "x(34)")
                output_list.str = output_list.str + to_string(" ", "x(22)")

                t_guest = get_cache(
                    Guest, {"gastnr": [(eq, debt.gastnrmember)]})

                if t_guest:
                    tstr = substring(f"{t_guest.name}, {t_guest.vorname1}{t_guest.anrede1}", 0, 34)
                else:
                    tstr = " "
                output_list.str = output_list.str + to_string(tstr, "x(50)")
                output_list.str = output_list.str + \
                    to_string(debitor.vesrdep, "->,>>>,>>>,>>9.99")
                output_list.str = output_list.str + \
                    to_string(debitor.zahlkonto, ">>>>9")
                output_list.str = output_list.str + \
                    to_string(debitor.vesrdep, "->,>>>,>>>,>>9.99")
                output_list.str = output_list.str + \
                    to_string(artikel.bezeich, "x(40)")

                t_credit = to_decimal(t_credit) + to_decimal(debitor.saldo)
                t_famt = to_decimal(t_famt) + to_decimal(debitor.vesrdep)
                tot_credit = to_decimal(tot_credit) + to_decimal(debitor.saldo)
                tot_saldo = to_decimal(tot_saldo) + to_decimal(debitor.saldo)
                tot_foreign = to_decimal(
                    tot_foreign) + to_decimal(debitor.vesrdep)
                tot_famt = to_decimal(tot_famt) + to_decimal(debitor.vesrdep)

                s_list = query(s_list_data, filters=(
                    lambda s_list: s_list.artnr == art.artnr), first=True)

                if not s_list:
                    s_list = S_list()
                    s_list_data.append(s_list)

                    s_list.artnr = art.artnr
                    s_list.bezeich = art.bezeich
                s_list.betrag = to_decimal(
                    s_list.betrag) + to_decimal(debitor.saldo)
        output_list = Output_list()
        output_list_data.append(output_list)

        for i in range(1, 58 + 1):
            output_list.str = output_list.str + "   "
        output_list.pay_amt = to_decimal(tot_saldo)
        output_list.pay_famt = to_decimal(tot_foreign)

        if not long_digit:
            output_list.str = output_list.str + "T O T A L " +\
                to_string(tot_saldo, "->,>>>,>>>,>>9.99") +\
                fill(" ", 78) +\
                to_string(tot_foreign, " ->>,>>>,>>>,>>9.99")
        else:
            output_list.str = output_list.str + "T O T A L " +\
                to_string(tot_saldo, " ->>>,>>>,>>>,>>9") +\
                fill(" ", 78) +\
                to_string(tot_foreign, "   ->>>,>>>,>>>,>>9")
        output_list = Output_list()
        output_list_data.append(output_list)

        output_list = Output_list()
        output_list_data.append(output_list)

        for i in range(1, 58 + 1):
            output_list.str = output_list.str + "   "
        output_list.pay_amt = to_decimal(t_credit)
        output_list.pay_famt = to_decimal(t_famt)

        if not long_digit:
            output_list.str = output_list.str + "Sub-Total " +\
                to_string(t_credit, "->,>>>,>>>,>>9.99") +\
                fill(" ", 78) +\
                to_string(t_famt, "->>,>>>,>>>,>>9.99")
        else:
            output_list.str = output_list.str + "Sub-Total " +\
                to_string(t_credit, " ->>>,>>>,>>>,>>9") +\
                fill(" ", 78) +\
                to_string(t_famt, "  ->>>,>>>,>>>,>>9")
        output_list = Output_list()
        output_list_data.append(output_list)

        output_list = Output_list()
        output_list_data.append(output_list)

        for i in range(1, 56 + 1):
            output_list.str = output_list.str + " "
        output_list.pay_amt = to_decimal(tot_credit)
        output_list.pay_famt = to_decimal(tot_famt)

        if not long_digit:
            output_list.str = output_list.str + "Grand TOTAL " +\
                to_string(tot_credit, "->,>>>,>>>,>>9.99") +\
                fill(" ", 78) + \
                to_string(tot_famt, "->>,>>>,>>>,>>9.99")
        else:
            output_list.str = output_list.str + "Grand TOTAL " +\
                to_string(tot_credit, " ->>>,>>>,>>>,>>9") +\
                fill(" ", 78) + \
                to_string(tot_famt, "  ->>>,>>>,>>>,>>9")
        create_tot_payment()

    def create_list3a():

        nonlocal r_no, s_list_data, t_list_data, t_ar_paylist_data, long_digit, htparam, guest, debitor, artikel, bill, bediener, waehrung
        nonlocal comment, cledger, ccard, last_sort, from_date, to_date, from_art, to_art, mi_payment, mi_transfer, show_inv, bill_name, bill_nr
        nonlocal bguest, bdebitor

        nonlocal s_list, t_list, output_list, t_ar_paylist, bguest, bdebitor, tbuff, bq
        nonlocal s_list_data, t_list_data, output_list_data, t_ar_paylist_data

        artnr: int = 0
        i: int = 0
        curr_gastnr: int = 0
        t_credit: Decimal = to_decimal("0.0")
        tot_credit: Decimal = to_decimal("0.0")
        t_famt: Decimal = to_decimal("0.0")
        tot_famt: Decimal = to_decimal("0.0")
        tot_saldo: Decimal = to_decimal("0.0")
        tot_foreign: Decimal = to_decimal("0.0")
        receiver: string = ""
        do_it: bool = False
        temp_name: string = ""
        temp_vorname1: string = ""
        temp_anredefirma: string = ""
        temp_anrede1: string = ""
        debt = None
        art = None
        t_guest = None
        tstr: string = ""
        Debt = create_buffer("Debt", Debitor)
        Art = create_buffer("Art", Artikel)
        T_guest = create_buffer("T_guest", Guest)

        debitor_obj_list = {}
        debitor = Debitor()
        debt = Debitor()
        artikel = Artikel()
        art = Artikel()
        guest = Guest()
        for debitor.gastnr, debitor.saldo, debitor.zahlkonto, debitor.betriebsnr, debitor.counter, debitor.rechnr, debitor.debref, debitor.rgdatum, debitor.gastnrmember, debitor.bediener_nr, debitor.vesrcod, debitor.vesrdep, debitor.betrieb_gastmem, debitor._recid, debt.gastnr, debt.saldo, debt.zahlkonto, debt.betriebsnr, debt.counter, debt.rechnr, debt.debref, debt.rgdatum, debt.gastnrmember, debt.bediener_nr, debt.vesrcod, debt.vesrdep, debt.betrieb_gastmem, debt._recid, artikel.artnr, artikel.bezeich, artikel.artart, artikel._recid, art.artnr, art.bezeich, art.artart, art._recid, guest.name, guest.vorname1, guest.anredefirma, guest.anrede1, guest._recid in db_session.query(Debitor.gastnr, Debitor.saldo, Debitor.zahlkonto, Debitor.betriebsnr, Debitor.counter, Debitor.rechnr, Debitor.debref, Debitor.rgdatum, Debitor.gastnrmember, Debitor.bediener_nr, Debitor.vesrcod, Debitor.vesrdep, Debitor.betrieb_gastmem, Debitor._recid, Debt.gastnr, Debt.saldo, Debt.zahlkonto, Debt.betriebsnr, Debt.counter, Debt.rechnr, Debt.debref, Debt.rgdatum, Debt.gastnrmember, Debt.bediener_nr, Debt.vesrcod, Debt.vesrdep, Debt.betrieb_gastmem, Debt._recid, Artikel.artnr, Artikel.bezeich, Artikel.artart, Artikel._recid, Art.artnr, Art.bezeich, Art.artart, Art._recid, Guest.name, Guest.vorname1, Guest.anredefirma, Guest.anrede1, Guest._recid).join(Debt, (Debt.counter == Debitor.counter) & (Debt.zahlkonto == 0)).join(Artikel, (Artikel.artnr == Debitor.artnr) & (Artikel.departement == 0) & (Artikel.artart == 7)).join(Art, (Art.artnr == Debitor.zahlkonto) & (Art.departement == 0)).join(Guest, (Guest.gastnr == Debitor.gastnr)).filter(
                (Debitor.rgdatum >= from_date) & (Debitor.rgdatum <= to_date) & (Debitor.zahlkonto > 0) & (Debitor.artnr >= from_art) & (Debitor.artnr <= to_art) & (Debitor.counter > 0) & (Debitor.opart > 0)).order_by(Artikel.artnr, Debitor.zahlkonto, Debitor.name, Debitor.rgdatum, Debitor.rechnr).all():
            if debitor_obj_list.get(debitor._recid):
                continue
            else:
                debitor_obj_list[debitor._recid] = True

            do_it = True

            if mi_payment:

                if artikel.artart == 2 and art.artart != 4 and art.artart != 7:
                    do_it = False

                elif artikel.artart == 7 and art.artart != 4:
                    do_it = False

            elif mi_transfer:

                if artikel.artart == 2 and (art.artart == 4 or art.artart == 7):
                    do_it = False

                elif artikel.artart == 7 and art.artart == 4:
                    do_it = False

            if do_it and (bill_name != "") and (substring(bill_name, 0, 1) != ("*").lower()):

                if not matches(guest.name, r"*" + bill_name + r"*"):
                    do_it = False

            if do_it and (bill_name != "") and (substring(bill_name, 0, 1) == ("*").lower()):

                if not matches(guest.name, bill_name):
                    do_it = False

            if do_it:

                if curr_gastnr == 0:
                    curr_gastnr = debitor.zahlkonto

                if curr_gastnr != debitor.zahlkonto:
                    curr_gastnr = debitor.zahlkonto
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    for i in range(1, 58 + 1):
                        output_list.str = output_list.str + "   "
                    output_list.pay_amt = to_decimal(tot_saldo)
                    output_list.pay_famt = to_decimal(tot_foreign)

                    if not long_digit:
                        output_list.str = output_list.str + "T O T A L " +\
                            to_string(tot_saldo, "->,>>>,>>>,>>9.99") +\
                            fill(" ", 78) +\
                            to_string(tot_foreign, " ->>,>>>,>>>,>>9.99")
                    else:
                        output_list.str = output_list.str + "T O T A L " +\
                            to_string(tot_saldo, " ->>>,>>>,>>>,>>9") +\
                            fill(" ", 78) +\
                            to_string(tot_foreign, "   ->>>,>>>,>>>,>>9")
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    tot_saldo = to_decimal("0")

                if artnr != artikel.artnr:
                    t_list = T_list()
                    t_list_data.append(t_list)

                    t_list.artnr = artikel.artnr
                    t_list.bezeich = artikel.bezeich

                    if artnr != 0:
                        output_list = Output_list()
                        output_list_data.append(output_list)

                        for i in range(1, 58 + 1):
                            output_list.str = output_list.str + "   "
                        output_list.pay_amt = to_decimal(t_credit)
                        output_list.pay_famt = to_decimal(t_famt)

                        if not long_digit:
                            output_list.str = output_list.str + "Sub-Total " +\
                                to_string(t_credit, "->,>>>,>>>,>>9.99") +\
                                fill(" ", 78) +\
                                to_string(t_famt, "->>,>>>,>>>,>>9.99")
                        else:
                            output_list.str = output_list.str + "Sub-Total " +\
                                to_string(t_credit, " ->>>,>>>,>>>,>>9") +\
                                fill(" ", 78) +\
                                to_string(t_famt, "  ->>>,>>>,>>>,>>9")
                        output_list = Output_list()
                        output_list_data.append(output_list)

                        t_credit = to_decimal("0")
                        t_famt = to_decimal("0")
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    for i in range(1, 19 + 1):
                        output_list.str = output_list.str + " "
                    output_list.str = output_list.str +\
                        to_string(artikel.artnr, ">>>>9") + " - " +\
                        to_string(artikel.bezeich, "x(34)")
                    artnr = artikel.artnr
                t_list.betrag = to_decimal(
                    t_list.betrag) - to_decimal(debitor.saldo)

                if guest.name != None:
                    temp_name = guest.name

                else:
                    temp_name = ""

                if guest.vorname1 != None:
                    temp_vorname1 = guest.vorname1

                else:
                    temp_vorname1 = ""

                if guest.anredefirma != None:
                    temp_anredefirma = guest.anredefirma

                else:
                    temp_anredefirma = ""

                if guest.anrede1 != None:
                    temp_anrede1 = guest.anrede1

                else:
                    temp_anrede1 = ""
                receiver = substring(f"{temp_name}, {temp_vorname1} {temp_anredefirma}{temp_anrede1}", 0, 32)
                output_list = Output_list()
                output_list_data.append(output_list)

                output_list.bill_art = artikel.artnr
                output_list.debt_counter = debitor.counter
                output_list.famt = to_string(
                    debt.vesrdep, "->>,>>>,>>>,>>9.99")

                if show_inv:

                    bill = get_cache(Bill, {"rechnr": [(eq, debitor.rechnr)]})

                    if bill:
                        output_list.inv_no = to_string(
                            bill.rechnr2, ">>>>>>>>>")

                        if bill.billref != 0:
                            output_list.soa_inv = "INV" + \
                                to_string(bill.billref, "9999999")
                    else:

                        bdebitor = get_cache(
                            Debitor, {"rechnr": [(eq, debitor.rechnr)], "debref": [(gt, 0)]})

                        if bdebitor:
                            output_list.soa_inv = "INV" + \
                                to_string(debitor.debref, "9999999")

                output_list.pay_amt = to_decimal(debitor.saldo)
                output_list.pay_famt = to_decimal(debitor.vesrdep)

                if not long_digit:
                    output_list.str = to_string(debt.rgdatum) +\
                        to_string(debitor.rechnr, ">>>,>>>,>>9") +\
                        to_string(receiver, "x(32)") +\
                        to_string(debt.saldo, "->,>>>,>>>,>>9.99") +\
                        to_string(debitor.saldo, "->,>>>,>>>,>>9.99") +\
                        to_string(art.bezeich, "x(34)") +\
                        to_string(debitor.rgdatum)
                else:
                    output_list.str = to_string(debt.rgdatum) +\
                        to_string(debitor.rechnr, ">>>,>>>,>>9") +\
                        to_string(receiver, "x(32)") +\
                        to_string(debt.saldo, " ->>>,>>>,>>>,>>9") +\
                        to_string(debitor.saldo, " ->>>,>>>,>>>,>>9") +\
                        to_string(art.bezeich, "x(34)") +\
                        to_string(debitor.rgdatum)
                output_list.bill_num = debitor.rechnr
                output_list.art_bezeich = artikel.bezeich
                output_list.tbetrag = to_decimal(
                    output_list.tbetrag) - to_decimal(debitor.saldo)

                bguest = get_cache(
                    Guest, {"gastnr": [(eq, debitor.gastnrmember)]})

                if bguest:
                    output_list.gastname = substring(f"{bguest.name}, {bguest.vorname1}{bguest.anredefirma} {bguest.anrede1}", 0, 32)

                bediener = get_cache(
                    Bediener, {"nr": [(eq, debitor.bediener_nr)]})

                if bediener:
                    output_list.str = output_list.str + \
                        to_string(bediener.userinit, "x(3)")
                else:
                    output_list.str = output_list.str + "   "
                output_list.str = output_list.str + \
                    to_string(debitor.vesrcod, "x(34)")
                output_list.str = output_list.str + to_string(" ", "x(22)")

                t_guest = get_cache(
                    Guest, {"gastnr": [(eq, debt.gastnrmember)]})

                if t_guest:
                    tstr = substring(f"{t_guest.name}, {t_guest.vorname1}{t_guest.anrede1}", 0, 34)
                else:
                    tstr = " "
                output_list.str = output_list.str + to_string(tstr, "x(50)")
                output_list.str = output_list.str + \
                    to_string(debitor.vesrdep, "->,>>>,>>>,>>9.99")
                output_list.str = output_list.str + \
                    to_string(debitor.zahlkonto, ">>>>9")
                output_list.str = output_list.str + \
                    to_string(debitor.vesrdep, "->,>>>,>>>,>>9.99")
                output_list.str = output_list.str + \
                    to_string(artikel.bezeich, "x(40)")

                t_credit = to_decimal(t_credit) + to_decimal(debitor.saldo)
                t_famt = to_decimal(t_famt) + to_decimal(debitor.vesrdep)
                tot_credit = to_decimal(tot_credit) + to_decimal(debitor.saldo)
                tot_saldo = to_decimal(tot_saldo) + to_decimal(debitor.saldo)
                tot_famt = to_decimal(tot_famt) + to_decimal(debitor.vesrdep)

                s_list = query(s_list_data, filters=(
                    lambda s_list: s_list.artnr == art.artnr), first=True)

                if not s_list:
                    s_list = S_list()
                    s_list_data.append(s_list)

                    s_list.artnr = art.artnr
                    s_list.bezeich = art.bezeich
                s_list.betrag = to_decimal(
                    s_list.betrag) + to_decimal(debitor.saldo)
        output_list = Output_list()
        output_list_data.append(output_list)

        for i in range(1, 58 + 1):
            output_list.str = output_list.str + "   "
        output_list.pay_amt = to_decimal(tot_saldo)
        output_list.pay_famt = to_decimal(tot_foreign)

        if not long_digit:
            output_list.str = output_list.str + "T O T A L " +\
                to_string(tot_saldo, "->,>>>,>>>,>>9.99") +\
                fill(" ", 78) +\
                to_string(tot_foreign, " ->>,>>>,>>>,>>9.99")
        else:
            output_list.str = output_list.str + "T O T A L " +\
                to_string(tot_saldo, " ->>>,>>>,>>>,>>9") +\
                fill(" ", 78) +\
                to_string(tot_foreign, "   ->>>,>>>,>>>,>>9")
        output_list = Output_list()
        output_list_data.append(output_list)

        output_list = Output_list()
        output_list_data.append(output_list)

        for i in range(1, 58 + 1):
            output_list.str = output_list.str + "   "
        output_list.pay_amt = to_decimal(t_credit)
        output_list.pay_famt = to_decimal(t_famt)

        if not long_digit:
            output_list.str = output_list.str + "Sub-Total " +\
                to_string(t_credit, "->,>>>,>>>,>>9.99") +\
                fill(" ", 78) +\
                to_string(t_famt, "->>,>>>,>>>,>>9.99")
        else:
            output_list.str = output_list.str + "Sub-Total " +\
                to_string(t_credit, " ->>>,>>>,>>>,>>9") +\
                fill(" ", 78) +\
                to_string(t_famt, "  ->>>,>>>,>>>,>>9")
        output_list = Output_list()
        output_list_data.append(output_list)

        output_list = Output_list()
        output_list_data.append(output_list)

        for i in range(1, 56 + 1):
            output_list.str = output_list.str + " "
        output_list.pay_amt = to_decimal(tot_credit)
        output_list.pay_famt = to_decimal(tot_famt)

        if not long_digit:
            output_list.str = output_list.str + "Grand TOTAL " +\
                to_string(tot_credit, "->,>>>,>>>,>>9.99") +\
                fill(" ", 78) + \
                to_string(tot_famt, "->>,>>>,>>>,>>9.99")
        else:
            output_list.str = output_list.str + "Grand TOTAL " +\
                to_string(tot_credit, " ->>>,>>>,>>>,>>9") +\
                fill(" ", 78) + \
                to_string(tot_famt, "  ->>>,>>>,>>>,>>9")

    def create_list11():

        nonlocal r_no, s_list_data, t_list_data, t_ar_paylist_data, long_digit, htparam, guest, debitor, artikel, bill, bediener, waehrung
        nonlocal comment, cledger, ccard, last_sort, from_date, to_date, from_art, to_art, mi_payment, mi_transfer, show_inv, bill_name, bill_nr
        nonlocal bguest, bdebitor

        nonlocal s_list, t_list, output_list, t_ar_paylist, bguest, bdebitor, tbuff, bq
        nonlocal s_list_data, t_list_data, output_list_data, t_ar_paylist_data

        artnr: int = 0
        i: int = 0
        curr_gastnr: int = 0
        t_credit: Decimal = to_decimal("0.0")
        tot_credit: Decimal = to_decimal("0.0")
        t_famt: Decimal = to_decimal("0.0")
        tot_famt: Decimal = to_decimal("0.0")
        tot_saldo: Decimal = to_decimal("0.0")
        tot_foreign: Decimal = to_decimal("0.0")
        receiver: string = ""
        do_it: bool = False
        temp_name: string = ""
        temp_vorname1: string = ""
        temp_anredefirma: string = ""
        temp_anrede1: string = ""
        debt = None
        art = None
        t_guest = None
        tstr: string = ""
        Debt = create_buffer("Debt", Debitor)
        Art = create_buffer("Art", Artikel)
        T_guest = create_buffer("T_guest", Guest)

        debitor_obj_list = {}
        debitor = Debitor()
        debt = Debitor()
        artikel = Artikel()
        art = Artikel()
        guest = Guest()
        for debitor.gastnr, debitor.saldo, debitor.zahlkonto, debitor.betriebsnr, debitor.counter, debitor.rechnr, debitor.debref, debitor.rgdatum, debitor.gastnrmember, debitor.bediener_nr, debitor.vesrcod, debitor.vesrdep, debitor.betrieb_gastmem, debitor._recid, debt.gastnr, debt.saldo, debt.zahlkonto, debt.betriebsnr, debt.counter, debt.rechnr, debt.debref, debt.rgdatum, debt.gastnrmember, debt.bediener_nr, debt.vesrcod, debt.vesrdep, debt.betrieb_gastmem, debt._recid, artikel.artnr, artikel.bezeich, artikel.artart, artikel._recid, art.artnr, art.bezeich, art.artart, art._recid, guest.name, guest.vorname1, guest.anredefirma, guest.anrede1, guest._recid in db_session.query(Debitor.gastnr, Debitor.saldo, Debitor.zahlkonto, Debitor.betriebsnr, Debitor.counter, Debitor.rechnr, Debitor.debref, Debitor.rgdatum, Debitor.gastnrmember, Debitor.bediener_nr, Debitor.vesrcod, Debitor.vesrdep, Debitor.betrieb_gastmem, Debitor._recid, Debt.gastnr, Debt.saldo, Debt.zahlkonto, Debt.betriebsnr, Debt.counter, Debt.rechnr, Debt.debref, Debt.rgdatum, Debt.gastnrmember, Debt.bediener_nr, Debt.vesrcod, Debt.vesrdep, Debt.betrieb_gastmem, Debt._recid, Artikel.artnr, Artikel.bezeich, Artikel.artart, Artikel._recid, Art.artnr, Art.bezeich, Art.artart, Art._recid, Guest.name, Guest.vorname1, Guest.anredefirma, Guest.anrede1, Guest._recid).join(Debt, (Debt.counter == Debitor.counter) & (Debt.zahlkonto == 0)).join(Artikel, (Artikel.artnr == Debitor.artnr) & (Artikel.departement == 0)).join(Art, (Art.artnr == Debitor.zahlkonto) & (Art.departement == 0)).join(Guest, (Guest.gastnr == Debitor.gastnr)).filter(
                (Debitor.rgdatum >= from_date) & (Debitor.rgdatum <= to_date) & (Debitor.zahlkonto > 0) & (Debitor.artnr >= from_art) & (Debitor.artnr <= to_art) & (Debitor.vesrcod == (comment).lower()) & (Debitor.counter > 0) & (Debitor.opart > 0)).order_by(Artikel.artnr, Debitor.name, Debitor.gastnr, Debitor.rgdatum, Debitor.rechnr).all():
            if debitor_obj_list.get(debitor._recid):
                continue
            else:
                debitor_obj_list[debitor._recid] = True

            do_it = True

            if mi_payment:

                if artikel.artart == 2 and art.artart != 4 and art.artart != 7:
                    do_it = False

                elif artikel.artart == 7 and art.artart != 4:
                    do_it = False

            elif mi_transfer:

                if artikel.artart == 2 and (art.artart == 4 or art.artart == 7):
                    do_it = False

                elif artikel.artart == 7 and art.artart == 4:
                    do_it = False

            if do_it and (bill_name != "") and (substring(bill_name, 0, 1) != ("*").lower()):

                if not matches(guest.name, r"*" + bill_name + r"*"):
                    do_it = False

            if do_it and (bill_name != "") and (substring(bill_name, 0, 1) == ("*").lower()):

                if not matches(guest.name, bill_name):
                    do_it = False

            if do_it:

                if curr_gastnr == 0:
                    curr_gastnr = debitor.gastnr

                if curr_gastnr != debitor.gastnr:
                    curr_gastnr = debitor.gastnr
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    for i in range(1, 58 + 1):
                        output_list.str = output_list.str + "   "
                    output_list.pay_amt = to_decimal(tot_saldo)
                    output_list.pay_famt = to_decimal(tot_foreign)

                    if not long_digit:
                        output_list.str = output_list.str + "T O T A L " +\
                            to_string(tot_saldo, "->,>>>,>>>,>>9.99") +\
                            fill(" ", 78) +\
                            to_string(tot_foreign, " ->>,>>>,>>>,>>9.99")
                    else:
                        output_list.str = output_list.str + "T O T A L " +\
                            to_string(tot_saldo, " ->>>,>>>,>>>,>>9") +\
                            fill(" ", 78) +\
                            to_string(tot_foreign, "   ->>>,>>>,>>>,>>9")
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    tot_saldo = to_decimal("0")
                    tot_foreign = to_decimal("0")

                if artnr != artikel.artnr:
                    t_list = T_list()
                    t_list_data.append(t_list)

                    t_list.artnr = artikel.artnr
                    t_list.bezeich = artikel.bezeich

                    if artnr != 0:
                        output_list = Output_list()
                        output_list_data.append(output_list)

                        for i in range(1, 58 + 1):
                            output_list.str = output_list.str + "   "
                        output_list.pay_amt = to_decimal(t_credit)
                        output_list.pay_famt = to_decimal(t_famt)

                        if not long_digit:
                            output_list.str = output_list.str + "Sub-Total " +\
                                to_string(t_credit, "->,>>>,>>>,>>9.99") +\
                                fill(" ", 78) +\
                                to_string(t_famt, "->>,>>>,>>>,>>9.99")
                        else:
                            output_list.str = output_list.str + "Sub-Total " +\
                                to_string(t_credit, " ->>>,>>>,>>>,>>9") +\
                                fill(" ", 78) +\
                                to_string(t_famt, "  ->>>,>>>,>>>,>>9")
                        output_list = Output_list()
                        output_list_data.append(output_list)

                        t_credit = to_decimal("0")
                        t_famt = to_decimal("0")
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    for i in range(1, 19 + 1):
                        output_list.str = output_list.str + " "
                    output_list.str = output_list.str +\
                        to_string(artikel.artnr, ">>>>9") + " - " +\
                        to_string(artikel.bezeich, "x(34)")
                    artnr = artikel.artnr
                t_list.betrag = to_decimal(
                    t_list.betrag) - to_decimal(debitor.saldo)

                if guest.name != None:
                    temp_name = guest.name

                else:
                    temp_name = ""

                if guest.vorname1 != None:
                    temp_vorname1 = guest.vorname1

                else:
                    temp_vorname1 = ""

                if guest.anredefirma != None:
                    temp_anredefirma = guest.anredefirma

                else:
                    temp_anredefirma = ""

                if guest.anrede1 != None:
                    temp_anrede1 = guest.anrede1

                else:
                    temp_anrede1 = ""
                receiver = substring(f"{temp_name}, {temp_vorname1} {temp_anredefirma}{temp_anrede1}", 0, 32)
                output_list = Output_list()
                output_list_data.append(output_list)

                output_list.bill_art = artikel.artnr
                output_list.debt_counter = debitor.counter
                output_list.famt = to_string(
                    debt.vesrdep, "->>,>>>,>>>,>>9.99")

                if show_inv:

                    bill = get_cache(Bill, {"rechnr": [(eq, debitor.rechnr)]})

                    if bill:
                        output_list.inv_no = to_string(
                            bill.rechnr2, ">>>>>>>>>")

                        if bill.billref != 0:
                            output_list.soa_inv = "INV" + \
                                to_string(bill.billref, "9999999")
                    else:

                        bdebitor = get_cache(
                            Debitor, {"rechnr": [(eq, debitor.rechnr)], "debref": [(gt, 0)]})

                        if bdebitor:
                            output_list.soa_inv = "INV" + \
                                to_string(debitor.debref, "9999999")

                output_list.pay_amt = to_decimal(debitor.saldo)
                output_list.pay_famt = to_decimal(debitor.vesrdep)

                if not long_digit:
                    output_list.str = to_string(debt.rgdatum) +\
                        to_string(debitor.rechnr, ">>>,>>>,>>9") +\
                        to_string(receiver, "x(32)") +\
                        to_string(debt.saldo, "->,>>>,>>>,>>9.99") +\
                        to_string(debitor.saldo, "->,>>>,>>>,>>9.99") +\
                        to_string(art.bezeich, "x(34)") +\
                        to_string(debitor.rgdatum)
                else:
                    output_list.str = to_string(debt.rgdatum) +\
                        to_string(debitor.rechnr, ">>>,>>>,>>9") +\
                        to_string(receiver, "x(32)") +\
                        to_string(debt.saldo, " ->>>,>>>,>>>,>>9") +\
                        to_string(debitor.saldo, " ->>>,>>>,>>>,>>9") +\
                        to_string(art.bezeich, "x(34)") +\
                        to_string(debitor.rgdatum)
                output_list.bill_num = debitor.rechnr
                output_list.art_bezeich = artikel.bezeich
                output_list.tbetrag = to_decimal(
                    output_list.tbetrag) - to_decimal(debitor.saldo)

                bguest = get_cache(
                    Guest, {"gastnr": [(eq, debitor.gastnrmember)]})

                if bguest:
                    output_list.gastname = substring(f"{bguest.name}, {bguest.vorname1}{bguest.anredefirma} {bguest.anrede1}", 0, 32)

                bediener = get_cache(
                    Bediener, {"nr": [(eq, debitor.bediener_nr)]})

                if bediener:
                    output_list.str = output_list.str + \
                        to_string(bediener.userinit, "x(3)")
                else:
                    output_list.str = output_list.str + "   "
                output_list.str = output_list.str + \
                    to_string(debitor.vesrcod, "x(34)")
                output_list.str = output_list.str + to_string(" ", "x(22)")

                t_guest = get_cache(
                    Guest, {"gastnr": [(eq, debt.gastnrmember)]})

                if t_guest:
                    tstr = substring(f"{t_guest.name}, {t_guest.vorname1}{t_guest.anrede1}", 0, 34)
                else:
                    tstr = " "
                output_list.str = output_list.str + to_string(tstr, "x(50)")
                output_list.str = output_list.str + \
                    to_string(debitor.vesrdep, "->,>>>,>>>,>>9.99")
                output_list.str = output_list.str + \
                    to_string(debitor.zahlkonto, ">>>>9")
                output_list.str = output_list.str + \
                    to_string(debitor.vesrdep, "->,>>>,>>>,>>9.99")
                output_list.str = output_list.str + \
                    to_string(artikel.bezeich, "x(40)")

                t_credit = to_decimal(t_credit) + to_decimal(debitor.saldo)
                t_famt = to_decimal(t_famt) + to_decimal(debitor.vesrdep)
                tot_credit = to_decimal(tot_credit) + to_decimal(debitor.saldo)
                tot_saldo = to_decimal(tot_saldo) + to_decimal(debitor.saldo)
                tot_foreign = to_decimal(
                    tot_foreign) + to_decimal(debitor.vesrdep)
                tot_famt = to_decimal(tot_famt) + to_decimal(debitor.vesrdep)

                s_list = query(s_list_data, filters=(
                    lambda s_list: s_list.artnr == art.artnr), first=True)

                if not s_list:
                    s_list = S_list()
                    s_list_data.append(s_list)

                    s_list.artnr = art.artnr
                    s_list.bezeich = art.bezeich
                s_list.betrag = to_decimal(
                    s_list.betrag) + to_decimal(debitor.saldo)
        output_list = Output_list()
        output_list_data.append(output_list)

        for i in range(1, 58 + 1):
            output_list.str = output_list.str + "   "
        output_list.pay_amt = to_decimal(tot_saldo)
        output_list.pay_famt = to_decimal(tot_foreign)

        if not long_digit:
            output_list.str = output_list.str + "T O T A L " +\
                to_string(tot_saldo, "->,>>>,>>>,>>9.99") +\
                fill(" ", 78) +\
                to_string(tot_foreign, " ->>,>>>,>>>,>>9.99")
        else:
            output_list.str = output_list.str + "T O T A L " +\
                to_string(tot_saldo, " ->>>,>>>,>>>,>>9") +\
                fill(" ", 78) +\
                to_string(tot_foreign, "   ->>>,>>>,>>>,>>9")
        output_list = Output_list()
        output_list_data.append(output_list)

        output_list = Output_list()
        output_list_data.append(output_list)

        for i in range(1, 58 + 1):
            output_list.str = output_list.str + "   "
        output_list.pay_amt = to_decimal(t_credit)
        output_list.pay_famt = to_decimal(t_famt)

        if not long_digit:
            output_list.str = output_list.str + "Sub-Total " +\
                to_string(t_credit, "->,>>>,>>>,>>9.99") +\
                fill(" ", 78) +\
                to_string(t_famt, "->>,>>>,>>>,>>9.99")
        else:
            output_list.str = output_list.str + "Sub-Total " +\
                to_string(t_credit, " ->>>,>>>,>>>,>>9") +\
                fill(" ", 78) +\
                to_string(t_famt, "  ->>>,>>>,>>>,>>9")
        output_list = Output_list()
        output_list_data.append(output_list)

        output_list = Output_list()
        output_list_data.append(output_list)

        for i in range(1, 56 + 1):
            output_list.str = output_list.str + " "
        output_list.pay_amt = to_decimal(tot_credit)
        output_list.pay_famt = to_decimal(tot_famt)

        if not long_digit:
            output_list.str = output_list.str + "Grand TOTAL " +\
                to_string(tot_credit, "->,>>>,>>>,>>9.99") +\
                fill(" ", 78) + \
                to_string(tot_famt, "->>,>>>,>>>,>>9.99")
        else:
            output_list.str = output_list.str + "Grand TOTAL " +\
                to_string(tot_credit, " ->>>,>>>,>>>,>>9") +\
                fill(" ", 78) + \
                to_string(tot_famt, "  ->>>,>>>,>>>,>>9")

    def create_list21():

        nonlocal r_no, s_list_data, t_list_data, t_ar_paylist_data, long_digit, htparam, guest, debitor, artikel, bill, bediener, waehrung
        nonlocal comment, cledger, ccard, last_sort, from_date, to_date, from_art, to_art, mi_payment, mi_transfer, show_inv, bill_name, bill_nr
        nonlocal bguest, bdebitor

        nonlocal s_list, t_list, output_list, t_ar_paylist, bguest, bdebitor, tbuff, bq
        nonlocal s_list_data, t_list_data, output_list_data, t_ar_paylist_data

        artnr: int = 0
        i: int = 0
        curr_gastnr: int = 0
        t_credit: Decimal = to_decimal("0.0")
        tot_credit: Decimal = to_decimal("0.0")
        t_famt: Decimal = to_decimal("0.0")
        tot_famt: Decimal = to_decimal("0.0")
        tot_saldo: Decimal = to_decimal("0.0")
        tot_foreign: Decimal = to_decimal("0.0")
        receiver: string = ""
        do_it: bool = False
        temp_name: string = ""
        temp_vorname1: string = ""
        temp_anredefirma: string = ""
        temp_anrede1: string = ""
        debt = None
        art = None
        t_guest = None
        tstr: string = ""
        Debt = create_buffer("Debt", Debitor)
        Art = create_buffer("Art", Artikel)
        T_guest = create_buffer("T_guest", Guest)

        debitor_obj_list = {}
        debitor = Debitor()
        debt = Debitor()
        artikel = Artikel()
        art = Artikel()
        guest = Guest()
        for debitor.gastnr, debitor.saldo, debitor.zahlkonto, debitor.betriebsnr, debitor.counter, debitor.rechnr, debitor.debref, debitor.rgdatum, debitor.gastnrmember, debitor.bediener_nr, debitor.vesrcod, debitor.vesrdep, debitor.betrieb_gastmem, debitor._recid, debt.gastnr, debt.saldo, debt.zahlkonto, debt.betriebsnr, debt.counter, debt.rechnr, debt.debref, debt.rgdatum, debt.gastnrmember, debt.bediener_nr, debt.vesrcod, debt.vesrdep, debt.betrieb_gastmem, debt._recid, artikel.artnr, artikel.bezeich, artikel.artart, artikel._recid, art.artnr, art.bezeich, art.artart, art._recid, guest.name, guest.vorname1, guest.anredefirma, guest.anrede1, guest._recid in db_session.query(Debitor.gastnr, Debitor.saldo, Debitor.zahlkonto, Debitor.betriebsnr, Debitor.counter, Debitor.rechnr, Debitor.debref, Debitor.rgdatum, Debitor.gastnrmember, Debitor.bediener_nr, Debitor.vesrcod, Debitor.vesrdep, Debitor.betrieb_gastmem, Debitor._recid, Debt.gastnr, Debt.saldo, Debt.zahlkonto, Debt.betriebsnr, Debt.counter, Debt.rechnr, Debt.debref, Debt.rgdatum, Debt.gastnrmember, Debt.bediener_nr, Debt.vesrcod, Debt.vesrdep, Debt.betrieb_gastmem, Debt._recid, Artikel.artnr, Artikel.bezeich, Artikel.artart, Artikel._recid, Art.artnr, Art.bezeich, Art.artart, Art._recid, Guest.name, Guest.vorname1, Guest.anredefirma, Guest.anrede1, Guest._recid).join(Debt, (Debt.counter == Debitor.counter) & (Debt.zahlkonto == 0) & (Debitor.vesrcod == (comment).lower())).join(Artikel, (Artikel.artnr == Debitor.artnr) & (Artikel.departement == 0) & (Artikel.artart == 2)).join(Art, (Art.artnr == Debitor.zahlkonto) & (Art.departement == 0)).join(Guest, (Guest.gastnr == Debitor.gastnr)).filter(
                (Debitor.rgdatum >= from_date) & (Debitor.rgdatum <= to_date) & (Debitor.zahlkonto > 0) & (Debitor.artnr >= from_art) & (Debitor.artnr <= to_art) & (Debitor.counter > 0) & (Debitor.opart > 0)).order_by(Artikel.artnr, Debitor.name, Debitor.gastnr, Debitor.rgdatum, Debitor.rechnr).all():
            if debitor_obj_list.get(debitor._recid):
                continue
            else:
                debitor_obj_list[debitor._recid] = True

            do_it = True

            if mi_payment:

                if artikel.artart == 2 and art.artart != 4 and art.artart != 7:
                    do_it = False

                elif artikel.artart == 7 and art.artart != 4:
                    do_it = False

            elif mi_transfer:

                if artikel.artart == 2 and (art.artart == 4 or art.artart == 7):
                    do_it = False

                elif artikel.artart == 7 and art.artart == 4:
                    do_it = False

            if do_it and (bill_name != "") and (substring(bill_name, 0, 1) != ("*").lower()):

                if not matches(guest.name, r"*" + bill_name + r"*"):
                    do_it = False

            if do_it and (bill_name != "") and (substring(bill_name, 0, 1) == ("*").lower()):

                if not matches(guest.name, bill_name):
                    do_it = False

            if do_it:

                if curr_gastnr == 0:
                    curr_gastnr = debitor.gastnr

                if curr_gastnr != debitor.gastnr:
                    curr_gastnr = debitor.gastnr
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    for i in range(1, 58 + 1):
                        output_list.str = output_list.str + "   "
                    output_list.pay_amt = to_decimal(tot_saldo)
                    output_list.pay_famt = to_decimal(tot_foreign)

                    if not long_digit:
                        output_list.str = output_list.str + "T O T A L " +\
                            to_string(tot_saldo, "->,>>>,>>>,>>9.99") +\
                            fill(" ", 78) +\
                            to_string(tot_foreign, " ->>,>>>,>>>,>>9.99")
                    else:
                        output_list.str = output_list.str + "T O T A L " +\
                            to_string(tot_saldo, " ->>>,>>>,>>>,>>9") +\
                            fill(" ", 78) +\
                            to_string(tot_foreign, "   ->>>,>>>,>>>,>>9")
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    tot_saldo = to_decimal("0")
                    tot_foreign = to_decimal("0")

                if artnr != artikel.artnr:
                    t_list = T_list()
                    t_list_data.append(t_list)

                    t_list.artnr = artikel.artnr
                    t_list.bezeich = artikel.bezeich

                    if artnr != 0:
                        output_list = Output_list()
                        output_list_data.append(output_list)

                        for i in range(1, 58 + 1):
                            output_list.str = output_list.str + "   "
                        output_list.pay_amt = to_decimal(t_credit)
                        output_list.pay_famt = to_decimal(t_famt)

                        if not long_digit:
                            output_list.str = output_list.str + "Sub-Total " +\
                                to_string(t_credit, "->,>>>,>>>,>>9.99") +\
                                fill(" ", 78) +\
                                to_string(t_famt, "->>,>>>,>>>,>>9.99")
                        else:
                            output_list.str = output_list.str + "Sub-Total " +\
                                to_string(t_credit, " ->>>,>>>,>>>,>>9") +\
                                fill(" ", 78) +\
                                to_string(t_famt, "  ->>>,>>>,>>>,>>9")
                        output_list = Output_list()
                        output_list_data.append(output_list)

                        t_credit = to_decimal("0")
                        t_famt = to_decimal("0")
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    for i in range(1, 19 + 1):
                        output_list.str = output_list.str + " "
                    output_list.str = output_list.str +\
                        to_string(artikel.artnr, ">>>>9") + " - " +\
                        to_string(artikel.bezeich, "x(34)")
                    artnr = artikel.artnr
                t_list.betrag = to_decimal(
                    t_list.betrag) - to_decimal(debitor.saldo)

                if guest.name != None:
                    temp_name = guest.name

                else:
                    temp_name = ""

                if guest.vorname1 != None:
                    temp_vorname1 = guest.vorname1

                else:
                    temp_vorname1 = ""

                if guest.anredefirma != None:
                    temp_anredefirma = guest.anredefirma

                else:
                    temp_anredefirma = ""

                if guest.anrede1 != None:
                    temp_anrede1 = guest.anrede1

                else:
                    temp_anrede1 = ""
                receiver = substring(f"{temp_name}, {temp_vorname1} {temp_anredefirma}{temp_anrede1}", 0, 32)
                output_list = Output_list()
                output_list_data.append(output_list)

                output_list.bill_art = artikel.artnr
                output_list.debt_counter = debitor.counter
                output_list.famt = to_string(
                    debt.vesrdep, "->>,>>>,>>>,>>9.99")

                if show_inv:

                    bill = get_cache(Bill, {"rechnr": [(eq, debitor.rechnr)]})

                    if bill:
                        output_list.inv_no = to_string(
                            bill.rechnr2, ">>>>>>>>>")

                        if bill.billref != 0:
                            output_list.soa_inv = "INV" + \
                                to_string(bill.billref, "9999999")
                    else:

                        bdebitor = get_cache(
                            Debitor, {"rechnr": [(eq, debitor.rechnr)], "debref": [(gt, 0)]})

                        if bdebitor:
                            output_list.soa_inv = "INV" + \
                                to_string(debitor.debref, "9999999")

                output_list.pay_amt = to_decimal(debitor.saldo)
                output_list.pay_famt = to_decimal(debitor.vesrdep)

                if not long_digit:
                    output_list.str = to_string(debt.rgdatum) +\
                        to_string(debitor.rechnr, ">>>,>>>,>>9") +\
                        to_string(receiver, "x(32)") +\
                        to_string(debt.saldo, "->,>>>,>>>,>>9.99") +\
                        to_string(debitor.saldo, "->,>>>,>>>,>>9.99") +\
                        to_string(art.bezeich, "x(34)") +\
                        to_string(debitor.rgdatum)
                else:
                    output_list.str = to_string(debt.rgdatum) + to_string(debitor.rechnr, ">>>,>>>,>>9") + to_string(receiver, "x(32)") + to_string(
                        debt.saldo, "->,>>>,>>>,>>9.99") + to_string(debitor.saldo, " ->>>,>>>,>>>,>>9") + to_string(art.bezeich, "x(34)") + to_string(debitor.rgdatum)
                output_list.bill_num = debitor.rechnr
                output_list.art_bezeich = artikel.bezeich
                output_list.tbetrag = to_decimal(
                    output_list.tbetrag) - to_decimal(debitor.saldo)

                bguest = get_cache(
                    Guest, {"gastnr": [(eq, debitor.gastnrmember)]})

                if bguest:
                    output_list.gastname = substring(f"{bguest.name}, {bguest.vorname1}{bguest.anredefirma} {bguest.anrede1}", 0, 32)

                bediener = get_cache(
                    Bediener, {"nr": [(eq, debitor.bediener_nr)]})

                if bediener:
                    output_list.str = output_list.str + \
                        to_string(bediener.userinit, "x(3)")
                else:
                    output_list.str = output_list.str + "   "
                output_list.str = output_list.str + \
                    to_string(debitor.vesrcod, "x(34)")
                output_list.str = output_list.str + to_string(" ", "x(22)")

                t_guest = get_cache(
                    Guest, {"gastnr": [(eq, debt.gastnrmember)]})

                if t_guest:
                    tstr = substring(f"{t_guest.name}, {t_guest.vorname1}{t_guest.anrede1}", 0, 34)
                else:
                    tstr = " "
                output_list.str = output_list.str + to_string(tstr, "x(50)")
                output_list.str = output_list.str + \
                    to_string(debitor.vesrdep, "->,>>>,>>>,>>9.99")
                output_list.str = output_list.str + \
                    to_string(debitor.zahlkonto, ">>>>9")
                output_list.str = output_list.str + \
                    to_string(debitor.vesrdep, "->,>>>,>>>,>>9.99")
                output_list.str = output_list.str + \
                    to_string(artikel.bezeich, "x(40)")

                t_credit = to_decimal(t_credit) + to_decimal(debitor.saldo)
                t_famt = to_decimal(t_famt) + to_decimal(debitor.vesrdep)
                tot_credit = to_decimal(tot_credit) + to_decimal(debitor.saldo)
                tot_saldo = to_decimal(tot_saldo) + to_decimal(debitor.saldo)
                tot_foreign = to_decimal(
                    tot_foreign) + to_decimal(debitor.vesrdep)
                tot_famt = to_decimal(tot_famt) + to_decimal(debitor.vesrdep)

                s_list = query(s_list_data, filters=(
                    lambda s_list: s_list.artnr == art.artnr), first=True)

                if not s_list:
                    s_list = S_list()
                    s_list_data.append(s_list)

                    s_list.artnr = art.artnr
                    s_list.bezeich = art.bezeich
                s_list.betrag = to_decimal(
                    s_list.betrag) + to_decimal(debitor.saldo)
        output_list = Output_list()
        output_list_data.append(output_list)

        for i in range(1, 58 + 1):
            output_list.str = output_list.str + "   "
        output_list.pay_amt = to_decimal(tot_saldo)
        output_list.pay_famt = to_decimal(tot_foreign)

        if not long_digit:
            output_list.str = output_list.str + "T O T A L " +\
                to_string(tot_saldo, "->,>>>,>>>,>>9.99") +\
                fill(" ", 78) +\
                to_string(tot_foreign, " ->>,>>>,>>>,>>9.99")
        else:
            output_list.str = output_list.str + "T O T A L " +\
                to_string(tot_saldo, " ->>>,>>>,>>>,>>9") +\
                fill(" ", 78) +\
                to_string(tot_foreign, "   ->>>,>>>,>>>,>>9")
        output_list = Output_list()
        output_list_data.append(output_list)

        output_list = Output_list()
        output_list_data.append(output_list)

        for i in range(1, 58 + 1):
            output_list.str = output_list.str + "   "
        output_list.pay_amt = to_decimal(t_credit)
        output_list.pay_famt = to_decimal(t_famt)

        if not long_digit:
            output_list.str = output_list.str + "Sub-Total " +\
                to_string(t_credit, "->,>>>,>>>,>>9.99") +\
                fill(" ", 78) +\
                to_string(t_famt, "->>,>>>,>>>,>>9.99")
        else:
            output_list.str = output_list.str + "Sub-Total " +\
                to_string(t_credit, " ->>>,>>>,>>>,>>9") +\
                fill(" ", 78) +\
                to_string(t_famt, "  ->>>,>>>,>>>,>>9")
        output_list = Output_list()
        output_list_data.append(output_list)

        output_list = Output_list()
        output_list_data.append(output_list)

        for i in range(1, 56 + 1):
            output_list.str = output_list.str + " "
        output_list.pay_amt = to_decimal(tot_credit)
        output_list.pay_famt = to_decimal(tot_famt)

        if not long_digit:
            output_list.str = output_list.str + "Grand TOTAL " +\
                to_string(tot_credit, "->,>>>,>>>,>>9.99") +\
                fill(" ", 78) + \
                to_string(tot_famt, "->>,>>>,>>>,>>9.99")
        else:
            output_list.str = output_list.str + "Grand TOTAL " +\
                to_string(tot_credit, " ->>>,>>>,>>>,>>9") +\
                fill(" ", 78) + \
                to_string(tot_famt, "  ->>>,>>>,>>>,>>9")

    def create_list31():

        nonlocal r_no, s_list_data, t_list_data, t_ar_paylist_data, long_digit, htparam, guest, debitor, artikel, bill, bediener, waehrung
        nonlocal comment, cledger, ccard, last_sort, from_date, to_date, from_art, to_art, mi_payment, mi_transfer, show_inv, bill_name, bill_nr
        nonlocal bguest, bdebitor

        nonlocal s_list, t_list, output_list, t_ar_paylist, bguest, bdebitor, tbuff, bq
        nonlocal s_list_data, t_list_data, output_list_data, t_ar_paylist_data

        artnr: int = 0
        i: int = 0
        curr_gastnr: int = 0
        t_credit: Decimal = to_decimal("0.0")
        tot_credit: Decimal = to_decimal("0.0")
        t_famt: Decimal = to_decimal("0.0")
        tot_famt: Decimal = to_decimal("0.0")
        tot_saldo: Decimal = to_decimal("0.0")
        tot_foreign: Decimal = to_decimal("0.0")
        receiver: string = ""
        do_it: bool = False
        temp_name: string = ""
        temp_vorname1: string = ""
        temp_anredefirma: string = ""
        temp_anrede1: string = ""
        debt = None
        art = None
        t_guest = None
        tstr: string = ""
        Debt = create_buffer("Debt", Debitor)
        Art = create_buffer("Art", Artikel)
        T_guest = create_buffer("T_guest", Guest)

        debitor_obj_list = {}
        debitor = Debitor()
        debt = Debitor()
        artikel = Artikel()
        art = Artikel()
        guest = Guest()
        for debitor.gastnr, debitor.saldo, debitor.zahlkonto, debitor.betriebsnr, debitor.counter, debitor.rechnr, debitor.debref, debitor.rgdatum, debitor.gastnrmember, debitor.bediener_nr, debitor.vesrcod, debitor.vesrdep, debitor.betrieb_gastmem, debitor._recid, debt.gastnr, debt.saldo, debt.zahlkonto, debt.betriebsnr, debt.counter, debt.rechnr, debt.debref, debt.rgdatum, debt.gastnrmember, debt.bediener_nr, debt.vesrcod, debt.vesrdep, debt.betrieb_gastmem, debt._recid, artikel.artnr, artikel.bezeich, artikel.artart, artikel._recid, art.artnr, art.bezeich, art.artart, art._recid, guest.name, guest.vorname1, guest.anredefirma, guest.anrede1, guest._recid in db_session.query(Debitor.gastnr, Debitor.saldo, Debitor.zahlkonto, Debitor.betriebsnr, Debitor.counter, Debitor.rechnr, Debitor.debref, Debitor.rgdatum, Debitor.gastnrmember, Debitor.bediener_nr, Debitor.vesrcod, Debitor.vesrdep, Debitor.betrieb_gastmem, Debitor._recid, Debt.gastnr, Debt.saldo, Debt.zahlkonto, Debt.betriebsnr, Debt.counter, Debt.rechnr, Debt.debref, Debt.rgdatum, Debt.gastnrmember, Debt.bediener_nr, Debt.vesrcod, Debt.vesrdep, Debt.betrieb_gastmem, Debt._recid, Artikel.artnr, Artikel.bezeich, Artikel.artart, Artikel._recid, Art.artnr, Art.bezeich, Art.artart, Art._recid, Guest.name, Guest.vorname1, Guest.anredefirma, Guest.anrede1, Guest._recid).join(Debt, (Debt.counter == Debitor.counter) & (Debt.zahlkonto == 0) & (Debitor.vesrcod == (comment).lower())).join(Artikel, (Artikel.artnr == Debitor.artnr) & (Artikel.departement == 0) & (Artikel.artart == 7)).join(Art, (Art.artnr == Debitor.zahlkonto) & (Art.departement == 0)).join(Guest, (Guest.gastnr == Debitor.gastnr)).filter(
                (Debitor.rgdatum >= from_date) & (Debitor.rgdatum <= to_date) & (Debitor.zahlkonto > 0) & (Debitor.artnr >= from_art) & (Debitor.artnr <= to_art) & (Debitor.counter > 0) & (Debitor.opart > 0)).order_by(Artikel.artnr, Debitor.name, Debitor.gastnr, Debitor.rgdatum, Debitor.rechnr).all():
            if debitor_obj_list.get(debitor._recid):
                continue
            else:
                debitor_obj_list[debitor._recid] = True

            do_it = True

            if mi_payment:

                if artikel.artart == 2 and art.artart != 4 and art.artart != 7:
                    do_it = False

                elif artikel.artart == 7 and art.artart != 4:
                    do_it = False

            elif mi_transfer:

                if artikel.artart == 2 and (art.artart == 4 or art.artart == 7):
                    do_it = False

                elif artikel.artart == 7 and art.artart == 4:
                    do_it = False

            if do_it and (bill_name != "") and (substring(bill_name, 0, 1) != ("*").lower()):

                if not matches(guest.name, r"*" + bill_name + r"*"):
                    do_it = False

            if do_it and (bill_name != "") and (substring(bill_name, 0, 1) == ("*").lower()):

                if not matches(guest.name, bill_name):
                    do_it = False

            if do_it:

                if curr_gastnr == 0:
                    curr_gastnr = debitor.gastnr

                if curr_gastnr != debitor.gastnr:
                    curr_gastnr = debitor.gastnr
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    for i in range(1, 58 + 1):
                        output_list.str = output_list.str + "   "
                    output_list.pay_amt = to_decimal(tot_saldo)
                    output_list.pay_famt = to_decimal(tot_foreign)

                    if not long_digit:
                        output_list.str = output_list.str + "T O T A L " +\
                            to_string(tot_saldo, "->,>>>,>>>,>>9.99") +\
                            fill(" ", 78) +\
                            to_string(tot_foreign, " ->>,>>>,>>>,>>9.99")
                    else:
                        output_list.str = output_list.str + "T O T A L " +\
                            to_string(tot_saldo, " ->>>,>>>,>>>,>>9") +\
                            fill(" ", 78) +\
                            to_string(tot_foreign, "   ->>>,>>>,>>>,>>9")
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    tot_saldo = to_decimal("0")
                    tot_foreign = to_decimal("0")

                if artnr != artikel.artnr:
                    t_list = T_list()
                    t_list_data.append(t_list)

                    t_list.artnr = artikel.artnr
                    t_list.bezeich = artikel.bezeich

                    if artnr != 0:
                        output_list = Output_list()
                        output_list_data.append(output_list)

                        for i in range(1, 58 + 1):
                            output_list.str = output_list.str + "   "
                        output_list.pay_amt = to_decimal(t_credit)
                        output_list.pay_famt = to_decimal(t_famt)

                        if not long_digit:
                            output_list.str = output_list.str + "Sub-Total " +\
                                to_string(t_credit, "->,>>>,>>>,>>9.99") +\
                                fill(" ", 78) +\
                                to_string(t_famt, "->>,>>>,>>>,>>9.99")
                        else:
                            output_list.str = output_list.str + "Sub-Total " +\
                                to_string(t_credit, " ->>>,>>>,>>>,>>9") +\
                                fill(" ", 78) +\
                                to_string(t_famt, "  ->>>,>>>,>>>,>>9")
                        output_list = Output_list()
                        output_list_data.append(output_list)

                        t_credit = to_decimal("0")
                        t_famt = to_decimal("0")
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    for i in range(1, 19 + 1):
                        output_list.str = output_list.str + " "
                    output_list.str = output_list.str +\
                        to_string(artikel.artnr, ">>>>9") + " - " +\
                        to_string(artikel.bezeich, "x(24)")
                    artnr = artikel.artnr
                t_list.betrag = to_decimal(
                    t_list.betrag) - to_decimal(debitor.saldo)

                if guest.name != None:
                    temp_name = guest.name

                else:
                    temp_name = ""

                if guest.vorname1 != None:
                    temp_vorname1 = guest.vorname1

                else:
                    temp_vorname1 = ""

                if guest.anredefirma != None:
                    temp_anredefirma = guest.anredefirma

                else:
                    temp_anredefirma = ""

                if guest.anrede1 != None:
                    temp_anrede1 = guest.anrede1

                else:
                    temp_anrede1 = ""
                receiver = substring(f"{temp_name}, {temp_vorname1} {temp_anredefirma}{temp_anrede1}", 0, 32)
                output_list = Output_list()
                output_list_data.append(output_list)

                output_list.bill_art = artikel.artnr
                output_list.debt_counter = debitor.counter
                output_list.famt = to_string(
                    debt.vesrdep, "->>,>>>,>>>,>>9.99")

                if show_inv:

                    bill = get_cache(Bill, {"rechnr": [(eq, debitor.rechnr)]})

                    if bill:
                        output_list.inv_no = to_string(
                            bill.rechnr2, ">>>>>>>>>")

                        if bill.billref != 0:
                            output_list.soa_inv = "INV" + \
                                to_string(bill.billref, "9999999")
                    else:

                        bdebitor = get_cache(
                            Debitor, {"rechnr": [(eq, debitor.rechnr)], "debref": [(gt, 0)]})

                        if bdebitor:
                            output_list.soa_inv = "INV" + \
                                to_string(debitor.debref, "9999999")

                output_list.pay_amt = to_decimal(debitor.saldo)
                output_list.pay_famt = to_decimal(debitor.vesrdep)

                if not long_digit:
                    output_list.str = to_string(debt.rgdatum) +\
                        to_string(debitor.rechnr, ">>>,>>>,>>9") +\
                        to_string(receiver, "x(32)") +\
                        to_string(debt.saldo, "->,>>>,>>>,>>9.99") +\
                        to_string(debitor.saldo, "->,>>>,>>>,>>9.99") +\
                        to_string(art.bezeich, "x(34)") +\
                        to_string(debitor.rgdatum)
                else:
                    output_list.str = to_string(debt.rgdatum) +\
                        to_string(debitor.rechnr, ">>>,>>>,>>9") +\
                        to_string(receiver, "x(32)") +\
                        to_string(debt.saldo, " ->>>,>>>,>>>,>>9") +\
                        to_string(debitor.saldo, " ->>>,>>>,>>>,>>9") +\
                        to_string(art.bezeich, "x(34)") +\
                        to_string(debitor.rgdatum)
                output_list.bill_num = debitor.rechnr
                output_list.art_bezeich = artikel.bezeich
                output_list.tbetrag = to_decimal(
                    output_list.tbetrag) - to_decimal(debitor.saldo)

                bguest = get_cache(
                    Guest, {"gastnr": [(eq, debitor.gastnrmember)]})

                if bguest:
                    output_list.gastname = substring(f"{bguest.name}, {bguest.vorname1}{bguest.anredefirma} {bguest.anrede1}", 0, 32)

                bediener = get_cache(
                    Bediener, {"nr": [(eq, debitor.bediener_nr)]})

                if bediener:
                    output_list.str = output_list.str + \
                        to_string(bediener.userinit, "x(3)")
                else:
                    output_list.str = output_list.str + "   "
                output_list.str = output_list.str + \
                    to_string(debitor.vesrcod, "x(34)")
                output_list.str = output_list.str + to_string(" ", "x(22)")

                t_guest = get_cache(
                    Guest, {"gastnr": [(eq, debt.gastnrmember)]})

                if t_guest:
                    tstr = substring(f"{t_guest.name}, {t_guest.vorname1}{t_guest.anrede1}", 0, 34)
                else:
                    tstr = " "
                output_list.str = output_list.str + to_string(tstr, "x(50)")
                output_list.str = output_list.str + \
                    to_string(debitor.vesrdep, "->,>>>,>>>,>>9.99")
                output_list.str = output_list.str + \
                    to_string(debitor.zahlkonto, ">>>>9")
                output_list.str = output_list.str + \
                    to_string(debitor.vesrdep, "->,>>>,>>>,>>9.99")
                output_list.str = output_list.str + \
                    to_string(artikel.bezeich, "x(40)")

                t_credit = to_decimal(t_credit) + to_decimal(debitor.saldo)
                t_famt = to_decimal(t_famt) + to_decimal(debitor.vesrdep)
                tot_credit = to_decimal(tot_credit) + to_decimal(debitor.saldo)
                tot_saldo = to_decimal(tot_saldo) + to_decimal(debitor.saldo)
                tot_foreign = to_decimal(
                    tot_foreign) + to_decimal(debitor.vesrdep)
                tot_famt = to_decimal(tot_famt) + to_decimal(debitor.vesrdep)

                s_list = query(s_list_data, filters=(
                    lambda s_list: s_list.artnr == art.artnr), first=True)

                if not s_list:
                    s_list = S_list()
                    s_list_data.append(s_list)

                    s_list.artnr = art.artnr
                    s_list.bezeich = art.bezeich
                s_list.betrag = to_decimal(
                    s_list.betrag) + to_decimal(debitor.saldo)
        output_list = Output_list()
        output_list_data.append(output_list)

        for i in range(1, 58 + 1):
            output_list.str = output_list.str + "   "
        output_list.pay_amt = to_decimal(tot_saldo)
        output_list.pay_famt = to_decimal(tot_foreign)

        if not long_digit:
            output_list.str = output_list.str + "T O T A L " +\
                to_string(tot_saldo, "->,>>>,>>>,>>9.99") +\
                fill(" ", 78) +\
                to_string(tot_foreign, " ->>,>>>,>>>,>>9.99")
        else:
            output_list.str = output_list.str + "T O T A L " +\
                to_string(tot_saldo, " ->>>,>>>,>>>,>>9") +\
                fill(" ", 78) +\
                to_string(tot_foreign, "   ->>>,>>>,>>>,>>9")
        output_list = Output_list()
        output_list_data.append(output_list)

        output_list = Output_list()
        output_list_data.append(output_list)

        for i in range(1, 58 + 1):
            output_list.str = output_list.str + "   "
        output_list.pay_amt = to_decimal(t_credit)
        output_list.pay_famt = to_decimal(t_famt)

        if not long_digit:
            output_list.str = output_list.str + "Sub-Total " +\
                to_string(t_credit, "->,>>>,>>>,>>9.99") +\
                fill(" ", 78) +\
                to_string(t_famt, "->>,>>>,>>>,>>9.99")
        else:
            output_list.str = output_list.str + "Sub-Total " +\
                to_string(t_credit, " ->>>,>>>,>>>,>>9") +\
                fill(" ", 78) +\
                to_string(t_famt, "  ->>>,>>>,>>>,>>9")
        output_list = Output_list()
        output_list_data.append(output_list)

        output_list = Output_list()
        output_list_data.append(output_list)

        for i in range(1, 56 + 1):
            output_list.str = output_list.str + " "
        output_list.pay_amt = to_decimal(tot_credit)
        output_list.pay_famt = to_decimal(tot_famt)

        if not long_digit:
            output_list.str = output_list.str + "Grand TOTAL " +\
                to_string(tot_credit, "->,>>>,>>>,>>9.99") +\
                fill(" ", 78) + \
                to_string(tot_famt, "->>,>>>,>>>,>>9.99")
        else:
            output_list.str = output_list.str + "Grand TOTAL " +\
                to_string(tot_credit, " ->>>,>>>,>>>,>>9") +\
                fill(" ", 78) + \
                to_string(tot_famt, "  ->>>,>>>,>>>,>>9")

    def create_list2b():

        nonlocal r_no, s_list_data, t_list_data, t_ar_paylist_data, long_digit, htparam, guest, debitor, artikel, bill, bediener, waehrung
        nonlocal comment, cledger, ccard, last_sort, from_date, to_date, from_art, to_art, mi_payment, mi_transfer, show_inv, bill_name, bill_nr
        nonlocal bguest, bdebitor

        nonlocal s_list, t_list, output_list, t_ar_paylist, bguest, bdebitor, tbuff, bq
        nonlocal s_list_data, t_list_data, output_list_data, t_ar_paylist_data

        artnr: int = 0
        i: int = 0
        curr_gastnr: int = 0
        t_credit: Decimal = to_decimal("0.0")
        tot_credit: Decimal = to_decimal("0.0")
        t_famt: Decimal = to_decimal("0.0")
        tot_famt: Decimal = to_decimal("0.0")
        tot_saldo: Decimal = to_decimal("0.0")
        tot_foreign: Decimal = to_decimal("0.0")
        receiver: string = ""
        do_it: bool = False
        temp_name: string = ""
        temp_vorname1: string = ""
        temp_anredefirma: string = ""
        temp_anrede1: string = ""
        debt = None
        art = None
        t_guest = None
        tstr: string = ""
        Debt = create_buffer("Debt", Debitor)
        Art = create_buffer("Art", Artikel)
        T_guest = create_buffer("T_guest", Guest)

        debitor_obj_list = {}
        debitor = Debitor()
        debt = Debitor()
        artikel = Artikel()
        art = Artikel()
        guest = Guest()
        for debitor.gastnr, debitor.saldo, debitor.zahlkonto, debitor.betriebsnr, debitor.counter, debitor.rechnr, debitor.debref, debitor.rgdatum, debitor.gastnrmember, debitor.bediener_nr, debitor.vesrcod, debitor.vesrdep, debitor.betrieb_gastmem, debitor._recid, debt.gastnr, debt.saldo, debt.zahlkonto, debt.betriebsnr, debt.counter, debt.rechnr, debt.debref, debt.rgdatum, debt.gastnrmember, debt.bediener_nr, debt.vesrcod, debt.vesrdep, debt.betrieb_gastmem, debt._recid, artikel.artnr, artikel.bezeich, artikel.artart, artikel._recid, art.artnr, art.bezeich, art.artart, art._recid, guest.name, guest.vorname1, guest.anredefirma, guest.anrede1, guest._recid in db_session.query(Debitor.gastnr, Debitor.saldo, Debitor.zahlkonto, Debitor.betriebsnr, Debitor.counter, Debitor.rechnr, Debitor.debref, Debitor.rgdatum, Debitor.gastnrmember, Debitor.bediener_nr, Debitor.vesrcod, Debitor.vesrdep, Debitor.betrieb_gastmem, Debitor._recid, Debt.gastnr, Debt.saldo, Debt.zahlkonto, Debt.betriebsnr, Debt.counter, Debt.rechnr, Debt.debref, Debt.rgdatum, Debt.gastnrmember, Debt.bediener_nr, Debt.vesrcod, Debt.vesrdep, Debt.betrieb_gastmem, Debt._recid, Artikel.artnr, Artikel.bezeich, Artikel.artart, Artikel._recid, Art.artnr, Art.bezeich, Art.artart, Art._recid, Guest.name, Guest.vorname1, Guest.anredefirma, Guest.anrede1, Guest._recid).join(Debt, (Debt.counter == Debitor.counter) & (Debt.zahlkonto == 0)).join(Artikel, (Artikel.artnr == Debitor.artnr) & (Artikel.departement == 0) & (Artikel.artart == 2)).join(Art, (Art.artnr == Debitor.zahlkonto) & (Art.departement == 0)).join(Guest, (Guest.gastnr == Debitor.gastnr)).filter(
                (Debitor.rgdatum >= from_date) & (Debitor.rgdatum <= to_date) & (Debitor.zahlkonto > 0) & (Debitor.artnr >= from_art) & (Debitor.artnr <= to_art) & (Debitor.counter > 0) & (Debitor.opart > 0)).order_by(Artikel.artnr, Debt.rgdatum, Debitor.name, Debitor.zahlkonto, Debitor.rechnr).all():
            if debitor_obj_list.get(debitor._recid):
                continue
            else:
                debitor_obj_list[debitor._recid] = True

            do_it = True

            if mi_payment:

                if artikel.artart == 2 and art.artart != 4 and art.artart != 7:
                    do_it = False

                elif artikel.artart == 7 and art.artart != 4:
                    do_it = False

            elif mi_transfer:

                if artikel.artart == 2 and (art.artart == 4 or art.artart == 7):
                    do_it = False

                elif artikel.artart == 7 and art.artart == 4:
                    do_it = False

            if do_it and (bill_name != "") and (substring(bill_name, 0, 1) != ("*").lower()):

                if not matches(guest.name, r"*" + bill_name + r"*"):
                    do_it = False

            if do_it and (bill_name != "") and (substring(bill_name, 0, 1) == ("*").lower()):

                if not matches(guest.name, bill_name):
                    do_it = False

            if do_it:

                if curr_gastnr == 0:
                    curr_gastnr = debitor.gastnr

                if curr_gastnr != debitor.gastnr:
                    curr_gastnr = debitor.gastnr
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    for i in range(1, 58 + 1):
                        output_list.str = output_list.str + "   "
                    output_list.pay_amt = to_decimal(tot_saldo)
                    output_list.pay_famt = to_decimal(tot_foreign)

                    if not long_digit:
                        output_list.str = output_list.str + "T O T A L " +\
                            to_string(tot_saldo, "->,>>>,>>>,>>9.99") +\
                            fill(" ", 78) +\
                            to_string(tot_foreign, " ->>,>>>,>>>,>>9.99")
                    else:
                        output_list.str = output_list.str + "T O T A L " +\
                            to_string(tot_saldo, " ->>>,>>>,>>>,>>9") +\
                            fill(" ", 78) +\
                            to_string(tot_foreign, "   ->>>,>>>,>>>,>>9")
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    tot_saldo = to_decimal("0")
                    tot_foreign = to_decimal("0")

                if artnr != artikel.artnr:
                    t_list = T_list()
                    t_list_data.append(t_list)

                    t_list.artnr = artikel.artnr
                    t_list.bezeich = artikel.bezeich

                    if artnr != 0:
                        output_list = Output_list()
                        output_list_data.append(output_list)

                        for i in range(1, 58 + 1):
                            output_list.str = output_list.str + "   "
                        output_list.pay_amt = to_decimal(t_credit)
                        output_list.pay_famt = to_decimal(t_famt)

                        if not long_digit:
                            output_list.str = output_list.str + "Sub-Total " +\
                                to_string(t_credit, "->,>>>,>>>,>>9.99") +\
                                fill(" ", 78) +\
                                to_string(t_famt, "->>,>>>,>>>,>>9.99")
                        else:
                            output_list.str = output_list.str + "Sub-Total " +\
                                to_string(t_credit, " ->>>,>>>,>>>,>>9") +\
                                fill(" ", 78) +\
                                to_string(t_famt, "  ->>>,>>>,>>>,>>9")
                        output_list = Output_list()
                        output_list_data.append(output_list)

                        t_credit = to_decimal("0")
                        t_famt = to_decimal("0")
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    for i in range(1, 19 + 1):
                        output_list.str = output_list.str + " "
                    output_list.str = output_list.str +\
                        to_string(artikel.artnr, ">>>>9") + " - " +\
                        to_string(artikel.bezeich, "x(24)")
                    artnr = artikel.artnr
                t_list.betrag = to_decimal(
                    t_list.betrag) - to_decimal(debitor.saldo)

                if guest.name != None:
                    temp_name = guest.name

                else:
                    temp_name = ""

                if guest.vorname1 != None:
                    temp_vorname1 = guest.vorname1

                else:
                    temp_vorname1 = ""

                if guest.anredefirma != None:
                    temp_anredefirma = guest.anredefirma

                else:
                    temp_anredefirma = ""

                if guest.anrede1 != None:
                    temp_anrede1 = guest.anrede1

                else:
                    temp_anrede1 = ""
                receiver = substring(f"{temp_name}, {temp_vorname1} {temp_anredefirma}{temp_anrede1}", 0, 32)
                output_list = Output_list()
                output_list_data.append(output_list)

                output_list.bill_art = artikel.artnr
                output_list.debt_counter = debitor.counter
                output_list.famt = to_string(
                    debt.vesrdep, "->>,>>>,>>>,>>9.99")

                if show_inv:

                    bill = get_cache(Bill, {"rechnr": [(eq, debitor.rechnr)]})

                    if bill:
                        output_list.inv_no = to_string(
                            bill.rechnr2, ">>>>>>>>>")

                        if bill.billref != 0:
                            output_list.soa_inv = "INV" + \
                                to_string(bill.billref, "9999999")
                    else:

                        bdebitor = get_cache(
                            Debitor, {"rechnr": [(eq, debitor.rechnr)], "debref": [(gt, 0)]})

                        if bdebitor:
                            output_list.soa_inv = "INV" + \
                                to_string(debitor.debref, "9999999")

                output_list.pay_amt = to_decimal(debitor.saldo)
                output_list.pay_famt = to_decimal(debitor.vesrdep)

                if not long_digit:
                    output_list.str = to_string(debt.rgdatum) +\
                        to_string(debitor.rechnr, ">>>,>>>,>>9") +\
                        to_string(receiver, "x(32)") +\
                        to_string(debt.saldo, "->,>>>,>>>,>>9.99") +\
                        to_string(debitor.saldo, "->,>>>,>>>,>>9.99") +\
                        to_string(art.bezeich, "x(34)") +\
                        to_string(debitor.rgdatum)
                else:
                    output_list.str = to_string(debt.rgdatum) +\
                        to_string(debitor.rechnr, ">>>,>>>,>>9") +\
                        to_string(receiver, "x(32)") +\
                        to_string(debt.saldo, " ->>>,>>>,>>>,>>9") +\
                        to_string(debitor.saldo, " ->>>,>>>,>>>,>>9") +\
                        to_string(art.bezeich, "x(34)") +\
                        to_string(debitor.rgdatum)
                output_list.bill_num = debitor.rechnr
                output_list.art_bezeich = artikel.bezeich
                output_list.tbetrag = to_decimal(
                    output_list.tbetrag) - to_decimal(debitor.saldo)

                bguest = get_cache(
                    Guest, {"gastnr": [(eq, debitor.gastnrmember)]})

                if bguest:
                    output_list.gastname = substring(f"{bguest.name}, {bguest.vorname1}{bguest.anredefirma} {bguest.anrede1}", 0, 32)

                bediener = get_cache(
                    Bediener, {"nr": [(eq, debitor.bediener_nr)]})

                if bediener:
                    output_list.str = output_list.str + \
                        to_string(bediener.userinit, "x(3)")
                else:
                    output_list.str = output_list.str + "   "
                output_list.str = output_list.str + \
                    to_string(debitor.vesrcod, "x(34)")
                output_list.str = output_list.str + to_string(" ", "x(22)")

                t_guest = get_cache(
                    Guest, {"gastnr": [(eq, debt.gastnrmember)]})

                if t_guest:
                    tstr = substring(f"{t_guest.name}, {t_guest.vorname1}{t_guest.anrede1}", 0, 34)
                else:
                    tstr = " "
                output_list.str = output_list.str + to_string(tstr, "x(50)")
                output_list.str = output_list.str + \
                    to_string(debitor.vesrdep, "->,>>>,>>>,>>9.99")
                output_list.str = output_list.str + \
                    to_string(debitor.zahlkonto, ">>>>9")
                output_list.str = output_list.str + \
                    to_string(debitor.vesrdep, "->,>>>,>>>,>>9.99")
                output_list.str = output_list.str + \
                    to_string(artikel.bezeich, "x(40)")

                t_credit = to_decimal(t_credit) + to_decimal(debitor.saldo)
                t_famt = to_decimal(t_famt) + to_decimal(debitor.vesrdep)
                tot_credit = to_decimal(tot_credit) + to_decimal(debitor.saldo)
                tot_saldo = to_decimal(tot_saldo) + to_decimal(debitor.saldo)
                tot_foreign = to_decimal(
                    tot_foreign) + to_decimal(debitor.vesrdep)
                tot_famt = to_decimal(tot_famt) + to_decimal(debitor.vesrdep)

                s_list = query(s_list_data, filters=(
                    lambda s_list: s_list.artnr == art.artnr), first=True)

                if not s_list:
                    s_list = S_list()
                    s_list_data.append(s_list)

                    s_list.artnr = art.artnr
                    s_list.bezeich = art.bezeich
                s_list.betrag = to_decimal(
                    s_list.betrag) + to_decimal(debitor.saldo)
        output_list = Output_list()
        output_list_data.append(output_list)

        for i in range(1, 58 + 1):
            output_list.str = output_list.str + "   "
        output_list.pay_amt = to_decimal(tot_saldo)
        output_list.pay_famt = to_decimal(tot_foreign)

        if not long_digit:
            output_list.str = output_list.str + "T O T A L " +\
                to_string(tot_saldo, "->,>>>,>>>,>>9.99") +\
                fill(" ", 78) +\
                to_string(tot_foreign, " ->>,>>>,>>>,>>9.99")
        else:
            output_list.str = output_list.str + "T O T A L " +\
                to_string(tot_saldo, " ->>>,>>>,>>>,>>9") +\
                fill(" ", 78) +\
                to_string(tot_foreign, "   ->>>,>>>,>>>,>>9")
        output_list = Output_list()
        output_list_data.append(output_list)

        output_list = Output_list()
        output_list_data.append(output_list)

        for i in range(1, 58 + 1):
            output_list.str = output_list.str + "   "
        output_list.pay_amt = to_decimal(t_credit)
        output_list.pay_famt = to_decimal(t_famt)

        if not long_digit:
            output_list.str = output_list.str + "Sub-Total " +\
                to_string(t_credit, "->,>>>,>>>,>>9.99") +\
                fill(" ", 78) +\
                to_string(t_famt, "->>,>>>,>>>,>>9.99")
        else:
            output_list.str = output_list.str + "Sub-Total " +\
                to_string(t_credit, " ->>>,>>>,>>>,>>9") +\
                fill(" ", 78) +\
                to_string(t_famt, "  ->>>,>>>,>>>,>>9")
        output_list = Output_list()
        output_list_data.append(output_list)

        output_list = Output_list()
        output_list_data.append(output_list)

        for i in range(1, 56 + 1):
            output_list.str = output_list.str + " "
        output_list.pay_amt = to_decimal(tot_credit)
        output_list.pay_famt = to_decimal(tot_famt)

        if not long_digit:
            output_list.str = output_list.str + "Grand TOTAL " +\
                to_string(tot_credit, "->,>>>,>>>,>>9.99") +\
                fill(" ", 78) + \
                to_string(tot_famt, "->>,>>>,>>>,>>9.99")
        else:
            output_list.str = output_list.str + "Grand TOTAL " +\
                to_string(tot_credit, " ->>>,>>>,>>>,>>9") +\
                fill(" ", 78) + \
                to_string(tot_famt, "  ->>>,>>>,>>>,>>9")
        create_tot_payment()

    def create_list2c():

        nonlocal r_no, s_list_data, t_list_data, t_ar_paylist_data, long_digit, htparam, guest, debitor, artikel, bill, bediener, waehrung
        nonlocal comment, cledger, ccard, last_sort, from_date, to_date, from_art, to_art, mi_payment, mi_transfer, show_inv, bill_name, bill_nr
        nonlocal bguest, bdebitor

        nonlocal s_list, t_list, output_list, t_ar_paylist, bguest, bdebitor, tbuff, bq
        nonlocal s_list_data, t_list_data, output_list_data, t_ar_paylist_data

        artnr: int = 0
        i: int = 0
        curr_gastnr: int = 0
        t_credit: Decimal = to_decimal("0.0")
        tot_credit: Decimal = to_decimal("0.0")
        t_famt: Decimal = to_decimal("0.0")
        tot_famt: Decimal = to_decimal("0.0")
        tot_saldo: Decimal = to_decimal("0.0")
        tot_foreign: Decimal = to_decimal("0.0")
        receiver: string = ""
        do_it: bool = False
        temp_name: string = ""
        temp_vorname1: string = ""
        temp_anredefirma: string = ""
        temp_anrede1: string = ""
        debt = None
        art = None
        t_guest = None
        tstr: string = ""
        Debt = create_buffer("Debt", Debitor)
        Art = create_buffer("Art", Artikel)
        T_guest = create_buffer("T_guest", Guest)

        debitor_obj_list = {}
        debitor = Debitor()
        debt = Debitor()
        artikel = Artikel()
        art = Artikel()
        guest = Guest()
        for debitor.gastnr, debitor.saldo, debitor.zahlkonto, debitor.betriebsnr, debitor.counter, debitor.rechnr, debitor.debref, debitor.rgdatum, debitor.gastnrmember, debitor.bediener_nr, debitor.vesrcod, debitor.vesrdep, debitor.betrieb_gastmem, debitor._recid, debt.gastnr, debt.saldo, debt.zahlkonto, debt.betriebsnr, debt.counter, debt.rechnr, debt.debref, debt.rgdatum, debt.gastnrmember, debt.bediener_nr, debt.vesrcod, debt.vesrdep, debt.betrieb_gastmem, debt._recid, artikel.artnr, artikel.bezeich, artikel.artart, artikel._recid, art.artnr, art.bezeich, art.artart, art._recid, guest.name, guest.vorname1, guest.anredefirma, guest.anrede1, guest._recid in db_session.query(Debitor.gastnr, Debitor.saldo, Debitor.zahlkonto, Debitor.betriebsnr, Debitor.counter, Debitor.rechnr, Debitor.debref, Debitor.rgdatum, Debitor.gastnrmember, Debitor.bediener_nr, Debitor.vesrcod, Debitor.vesrdep, Debitor.betrieb_gastmem, Debitor._recid, Debt.gastnr, Debt.saldo, Debt.zahlkonto, Debt.betriebsnr, Debt.counter, Debt.rechnr, Debt.debref, Debt.rgdatum, Debt.gastnrmember, Debt.bediener_nr, Debt.vesrcod, Debt.vesrdep, Debt.betrieb_gastmem, Debt._recid, Artikel.artnr, Artikel.bezeich, Artikel.artart, Artikel._recid, Art.artnr, Art.bezeich, Art.artart, Art._recid, Guest.name, Guest.vorname1, Guest.anredefirma, Guest.anrede1, Guest._recid).join(Debt, (Debt.counter == Debitor.counter) & (Debt.zahlkonto == 0)).join(Artikel, (Artikel.artnr == Debitor.artnr) & (Artikel.departement == 0) & (Artikel.artart == 2)).join(Art, (Art.artnr == Debitor.zahlkonto) & (Art.departement == 0)).join(Guest, (Guest.gastnr == Debitor.gastnr)).filter(
                (Debitor.rgdatum >= from_date) & (Debitor.rgdatum <= to_date) & (Debitor.zahlkonto > 0) & (Debitor.artnr >= from_art) & (Debitor.artnr <= to_art) & (Debitor.counter > 0) & (Debitor.opart > 0)).order_by(Artikel.artnr, Debitor.rechnr, Debitor.name, Debitor.rgdatum, Debitor.zahlkonto).all():
            if debitor_obj_list.get(debitor._recid):
                continue
            else:
                debitor_obj_list[debitor._recid] = True

            do_it = True

            if mi_payment:

                if artikel.artart == 2 and art.artart != 4 and art.artart != 7:
                    do_it = False

                elif artikel.artart == 7 and art.artart != 4:
                    do_it = False

            elif mi_transfer:

                if artikel.artart == 2 and (art.artart == 4 or art.artart == 7):
                    do_it = False

                elif artikel.artart == 7 and art.artart == 4:
                    do_it = False

            if do_it and (bill_name != "") and (substring(bill_name, 0, 1) != ("*").lower()):

                if not matches(guest.name, r"*" + bill_name + r"*"):
                    do_it = False

            if do_it and (bill_name != "") and (substring(bill_name, 0, 1) == ("*").lower()):

                if not matches(guest.name, bill_name):
                    do_it = False

            if do_it:

                if curr_gastnr == 0:
                    curr_gastnr = debitor.gastnr

                if curr_gastnr != debitor.gastnr:
                    curr_gastnr = debitor.gastnr
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    for i in range(1, 58 + 1):
                        output_list.str = output_list.str + "   "
                    output_list.pay_amt = to_decimal(tot_saldo)
                    output_list.pay_famt = to_decimal(tot_foreign)

                    if not long_digit:
                        output_list.str = output_list.str + "T O T A L " +\
                            to_string(tot_saldo, "->,>>>,>>>,>>9.99") +\
                            fill(" ", 78) +\
                            to_string(tot_foreign, " ->>,>>>,>>>,>>9.99")
                    else:
                        output_list.str = output_list.str + "T O T A L " +\
                            to_string(tot_saldo, " ->>>,>>>,>>>,>>9") +\
                            fill(" ", 78) +\
                            to_string(tot_foreign, "   ->>>,>>>,>>>,>>9")
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    tot_saldo = to_decimal("0")
                    tot_foreign = to_decimal("0")

                if artnr != artikel.artnr:
                    t_list = T_list()
                    t_list_data.append(t_list)

                    t_list.artnr = artikel.artnr
                    t_list.bezeich = artikel.bezeich

                    if artnr != 0:
                        output_list = Output_list()
                        output_list_data.append(output_list)

                        for i in range(1, 58 + 1):
                            output_list.str = output_list.str + "   "
                        output_list.pay_amt = to_decimal(t_credit)
                        output_list.pay_famt = to_decimal(t_famt)

                        if not long_digit:
                            output_list.str = output_list.str + "Sub-Total " +\
                                to_string(t_credit, "->,>>>,>>>,>>9.99") +\
                                fill(" ", 78) +\
                                to_string(t_famt, "->>,>>>,>>>,>>9.99")
                        else:
                            output_list.str = output_list.str + "Sub-Total " +\
                                to_string(t_credit, " ->>>,>>>,>>>,>>9") +\
                                fill(" ", 78) +\
                                to_string(t_famt, "  ->>>,>>>,>>>,>>9")
                        output_list = Output_list()
                        output_list_data.append(output_list)

                        t_credit = to_decimal("0")
                        t_famt = to_decimal("0")
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    for i in range(1, 19 + 1):
                        output_list.str = output_list.str + " "
                    output_list.str = output_list.str +\
                        to_string(artikel.artnr, ">>>>9") + " - " +\
                        to_string(artikel.bezeich, "x(24)")
                    artnr = artikel.artnr
                t_list.betrag = to_decimal(
                    t_list.betrag) - to_decimal(debitor.saldo)

                if guest.name != None:
                    temp_name = guest.name

                else:
                    temp_name = ""

                if guest.vorname1 != None:
                    temp_vorname1 = guest.vorname1

                else:
                    temp_vorname1 = ""

                if guest.anredefirma != None:
                    temp_anredefirma = guest.anredefirma

                else:
                    temp_anredefirma = ""

                if guest.anrede1 != None:
                    temp_anrede1 = guest.anrede1

                else:
                    temp_anrede1 = ""
                receiver = substring(f"{temp_name}, {temp_vorname1} {temp_anredefirma}{temp_anrede1}", 0, 32)
                output_list = Output_list()
                output_list_data.append(output_list)

                output_list.bill_art = artikel.artnr
                output_list.debt_counter = debitor.counter
                output_list.famt = to_string(
                    debt.vesrdep, "->>,>>>,>>>,>>9.99")

                if show_inv:

                    bill = get_cache(Bill, {"rechnr": [(eq, debitor.rechnr)]})

                    if bill:
                        output_list.inv_no = to_string(
                            bill.rechnr2, ">>>>>>>>>")

                        if bill.billref != 0:
                            output_list.soa_inv = "INV" + \
                                to_string(bill.billref, "9999999")
                    else:

                        bdebitor = get_cache(
                            Debitor, {"rechnr": [(eq, debitor.rechnr)], "debref": [(gt, 0)]})

                        if bdebitor:
                            output_list.soa_inv = "INV" + \
                                to_string(debitor.debref, "9999999")

                output_list.pay_amt = to_decimal(debitor.saldo)
                output_list.pay_famt = to_decimal(debitor.vesrdep)

                if not long_digit:
                    output_list.str = to_string(debt.rgdatum) +\
                        to_string(debitor.rechnr, ">>>,>>>,>>9") +\
                        to_string(receiver, "x(32)") +\
                        to_string(debt.saldo, "->,>>>,>>>,>>9.99") +\
                        to_string(debitor.saldo, "->,>>>,>>>,>>9.99") +\
                        to_string(art.bezeich, "x(34)") +\
                        to_string(debitor.rgdatum)
                else:
                    output_list.str = to_string(debt.rgdatum) +\
                        to_string(debitor.rechnr, ">>>,>>>,>>9") +\
                        to_string(receiver, "x(32)") +\
                        to_string(debt.saldo, " ->>>,>>>,>>>,>>9") +\
                        to_string(debitor.saldo, " ->>>,>>>,>>>,>>9") +\
                        to_string(art.bezeich, "x(34)") +\
                        to_string(debitor.rgdatum)
                output_list.bill_num = debitor.rechnr
                output_list.art_bezeich = artikel.bezeich
                output_list.tbetrag = to_decimal(
                    output_list.tbetrag) - to_decimal(debitor.saldo)

                bguest = get_cache(
                    Guest, {"gastnr": [(eq, debitor.gastnrmember)]})

                if bguest:
                    output_list.gastname = substring(f"{bguest.name}, {bguest.vorname1}{bguest.anredefirma} {bguest.anrede1}", 0, 32)

                bediener = get_cache(
                    Bediener, {"nr": [(eq, debitor.bediener_nr)]})

                if bediener:
                    output_list.str = output_list.str + \
                        to_string(bediener.userinit, "x(3)")
                else:
                    output_list.str = output_list.str + "   "
                output_list.str = output_list.str + \
                    to_string(debitor.vesrcod, "x(34)")
                output_list.str = output_list.str + to_string(" ", "x(22)")

                t_guest = get_cache(
                    Guest, {"gastnr": [(eq, debt.gastnrmember)]})

                if t_guest:
                    tstr = substring(f"{t_guest.name}, {t_guest.vorname1}{t_guest.anrede1}", 0, 34)
                else:
                    tstr = " "
                output_list.str = output_list.str + to_string(tstr, "x(50)")
                output_list.str = output_list.str + \
                    to_string(debitor.vesrdep, "->,>>>,>>>,>>9.99")
                output_list.str = output_list.str + \
                    to_string(debitor.zahlkonto, ">>>>9")
                output_list.str = output_list.str + \
                    to_string(debitor.vesrdep, "->,>>>,>>>,>>9.99")
                output_list.str = output_list.str + \
                    to_string(artikel.bezeich, "x(40)")

                t_credit = to_decimal(t_credit) + to_decimal(debitor.saldo)
                t_famt = to_decimal(t_famt) + to_decimal(debitor.vesrdep)
                tot_credit = to_decimal(tot_credit) + to_decimal(debitor.saldo)
                tot_saldo = to_decimal(tot_saldo) + to_decimal(debitor.saldo)
                tot_foreign = to_decimal(
                    tot_foreign) + to_decimal(debitor.vesrdep)
                tot_famt = to_decimal(tot_famt) + to_decimal(debitor.vesrdep)

                s_list = query(s_list_data, filters=(
                    lambda s_list: s_list.artnr == art.artnr), first=True)

                if not s_list:
                    s_list = S_list()
                    s_list_data.append(s_list)

                    s_list.artnr = art.artnr
                    s_list.bezeich = art.bezeich
                s_list.betrag = to_decimal(
                    s_list.betrag) + to_decimal(debitor.saldo)
        output_list = Output_list()
        output_list_data.append(output_list)

        for i in range(1, 58 + 1):
            output_list.str = output_list.str + "   "
        output_list.pay_amt = to_decimal(tot_saldo)
        output_list.pay_famt = to_decimal(tot_foreign)

        if not long_digit:
            output_list.str = output_list.str + "T O T A L " +\
                to_string(tot_saldo, "->,>>>,>>>,>>9.99") +\
                fill(" ", 78) +\
                to_string(tot_foreign, " ->>,>>>,>>>,>>9.99")
        else:
            output_list.str = output_list.str + "T O T A L " +\
                to_string(tot_saldo, " ->>>,>>>,>>>,>>9") +\
                fill(" ", 78) +\
                to_string(tot_foreign, "   ->>>,>>>,>>>,>>9")
        output_list = Output_list()
        output_list_data.append(output_list)

        output_list = Output_list()
        output_list_data.append(output_list)

        for i in range(1, 58 + 1):
            output_list.str = output_list.str + "   "
        output_list.pay_amt = to_decimal(t_credit)
        output_list.pay_famt = to_decimal(t_famt)

        if not long_digit:
            output_list.str = output_list.str + "Sub-Total " +\
                to_string(t_credit, "->,>>>,>>>,>>9.99") +\
                fill(" ", 78) +\
                to_string(t_famt, "->>,>>>,>>>,>>9.99")
        else:
            output_list.str = output_list.str + "Sub-Total " +\
                to_string(t_credit, " ->>>,>>>,>>>,>>9") +\
                fill(" ", 78) +\
                to_string(t_famt, "  ->>>,>>>,>>>,>>9")
        output_list = Output_list()
        output_list_data.append(output_list)

        output_list = Output_list()
        output_list_data.append(output_list)

        for i in range(1, 56 + 1):
            output_list.str = output_list.str + " "
        output_list.pay_amt = to_decimal(tot_credit)
        output_list.pay_famt = to_decimal(tot_famt)

        if not long_digit:
            output_list.str = output_list.str + "Grand TOTAL " +\
                to_string(tot_credit, "->,>>>,>>>,>>9.99") +\
                fill(" ", 78) + \
                to_string(tot_famt, "->>,>>>,>>>,>>9.99")
        else:
            output_list.str = output_list.str + "Grand TOTAL " +\
                to_string(tot_credit, " ->>>,>>>,>>>,>>9") +\
                fill(" ", 78) + \
                to_string(tot_famt, "  ->>>,>>>,>>>,>>9")
        create_tot_payment()

    def create_list2d():

        nonlocal r_no, s_list_data, t_list_data, t_ar_paylist_data, long_digit, htparam, guest, debitor, artikel, bill, bediener, waehrung
        nonlocal comment, cledger, ccard, last_sort, from_date, to_date, from_art, to_art, mi_payment, mi_transfer, show_inv, bill_name, bill_nr
        nonlocal bguest, bdebitor

        nonlocal s_list, t_list, output_list, t_ar_paylist, bguest, bdebitor, tbuff, bq
        nonlocal s_list_data, t_list_data, output_list_data, t_ar_paylist_data

        artnr: int = 0
        i: int = 0
        curr_gastnr: int = 0
        t_credit: Decimal = to_decimal("0.0")
        tot_credit: Decimal = to_decimal("0.0")
        t_famt: Decimal = to_decimal("0.0")
        tot_famt: Decimal = to_decimal("0.0")
        tot_saldo: Decimal = to_decimal("0.0")
        tot_foreign: Decimal = to_decimal("0.0")
        receiver: string = ""
        do_it: bool = False
        temp_name: string = ""
        temp_vorname1: string = ""
        temp_anredefirma: string = ""
        temp_anrede1: string = ""
        debt = None
        art = None
        t_guest = None
        tstr: string = ""
        Debt = create_buffer("Debt", Debitor)
        Art = create_buffer("Art", Artikel)
        T_guest = create_buffer("T_guest", Guest)

        debitor_obj_list = {}
        debitor = Debitor()
        debt = Debitor()
        artikel = Artikel()
        art = Artikel()
        guest = Guest()
        for debitor.gastnr, debitor.saldo, debitor.zahlkonto, debitor.betriebsnr, debitor.counter, debitor.rechnr, debitor.debref, debitor.rgdatum, debitor.gastnrmember, debitor.bediener_nr, debitor.vesrcod, debitor.vesrdep, debitor.betrieb_gastmem, debitor._recid, debt.gastnr, debt.saldo, debt.zahlkonto, debt.betriebsnr, debt.counter, debt.rechnr, debt.debref, debt.rgdatum, debt.gastnrmember, debt.bediener_nr, debt.vesrcod, debt.vesrdep, debt.betrieb_gastmem, debt._recid, artikel.artnr, artikel.bezeich, artikel.artart, artikel._recid, art.artnr, art.bezeich, art.artart, art._recid, guest.name, guest.vorname1, guest.anredefirma, guest.anrede1, guest._recid in db_session.query(Debitor.gastnr, Debitor.saldo, Debitor.zahlkonto, Debitor.betriebsnr, Debitor.counter, Debitor.rechnr, Debitor.debref, Debitor.rgdatum, Debitor.gastnrmember, Debitor.bediener_nr, Debitor.vesrcod, Debitor.vesrdep, Debitor.betrieb_gastmem, Debitor._recid, Debt.gastnr, Debt.saldo, Debt.zahlkonto, Debt.betriebsnr, Debt.counter, Debt.rechnr, Debt.debref, Debt.rgdatum, Debt.gastnrmember, Debt.bediener_nr, Debt.vesrcod, Debt.vesrdep, Debt.betrieb_gastmem, Debt._recid, Artikel.artnr, Artikel.bezeich, Artikel.artart, Artikel._recid, Art.artnr, Art.bezeich, Art.artart, Art._recid, Guest.name, Guest.vorname1, Guest.anredefirma, Guest.anrede1, Guest._recid).join(Debt, (Debt.counter == Debitor.counter) & (Debt.zahlkonto == 0)).join(Artikel, (Artikel.artnr == Debitor.artnr) & (Artikel.departement == 0) & (Artikel.artart == 2)).join(Art, (Art.artnr == Debitor.zahlkonto) & (Art.departement == 0)).join(Guest, (Guest.gastnr == Debitor.gastnr)).filter(
                (Debitor.rgdatum >= from_date) & (Debitor.rgdatum <= to_date) & (Debitor.zahlkonto > 0) & (Debitor.artnr >= from_art) & (Debitor.artnr <= to_art) & (Debitor.counter > 0) & (Debitor.opart > 0)).order_by(Artikel.artnr, Debitor.vesrcod, Debitor.name, Debitor.rgdatum, Debitor.zahlkonto, Debitor.rechnr).all():
            if debitor_obj_list.get(debitor._recid):
                continue
            else:
                debitor_obj_list[debitor._recid] = True

            do_it = True

            if mi_payment:

                if artikel.artart == 2 and art.artart != 4 and art.artart != 7:
                    do_it = False

                elif artikel.artart == 7 and art.artart != 4:
                    do_it = False

            elif mi_transfer:

                if artikel.artart == 2 and (art.artart == 4 or art.artart == 7):
                    do_it = False

                elif artikel.artart == 7 and art.artart == 4:
                    do_it = False

            if do_it and (bill_name != "") and (substring(bill_name, 0, 1) != ("*").lower()):

                if not matches(guest.name, r"*" + bill_name + r"*"):
                    do_it = False

            if do_it and (bill_name != "") and (substring(bill_name, 0, 1) == ("*").lower()):

                if not matches(guest.name, bill_name):
                    do_it = False

            if do_it:

                if curr_gastnr == 0:
                    curr_gastnr = debitor.gastnr

                if curr_gastnr != debitor.gastnr:
                    curr_gastnr = debitor.gastnr
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    for i in range(1, 58 + 1):
                        output_list.str = output_list.str + "   "
                    output_list.pay_amt = to_decimal(tot_saldo)
                    output_list.pay_famt = to_decimal(tot_foreign)

                    if not long_digit:
                        output_list.str = output_list.str + "T O T A L " +\
                            to_string(tot_saldo, "->,>>>,>>>,>>9.99") +\
                            fill(" ", 78) +\
                            to_string(tot_foreign, " ->>,>>>,>>>,>>9.99")
                    else:
                        output_list.str = output_list.str + "T O T A L " +\
                            to_string(tot_saldo, " ->>>,>>>,>>>,>>9") +\
                            fill(" ", 78) +\
                            to_string(tot_foreign, "   ->>>,>>>,>>>,>>9")
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    tot_saldo = to_decimal("0")
                    tot_foreign = to_decimal("0")

                if artnr != artikel.artnr:
                    t_list = T_list()
                    t_list_data.append(t_list)

                    t_list.artnr = artikel.artnr
                    t_list.bezeich = artikel.bezeich

                    if artnr != 0:
                        output_list = Output_list()
                        output_list_data.append(output_list)

                        for i in range(1, 58 + 1):
                            output_list.str = output_list.str + "   "
                        output_list.pay_amt = to_decimal(t_credit)
                        output_list.pay_famt = to_decimal(t_famt)

                        if not long_digit:
                            output_list.str = output_list.str + "Sub-Total " +\
                                to_string(t_credit, "->,>>>,>>>,>>9.99") +\
                                fill(" ", 78) +\
                                to_string(t_famt, "->>,>>>,>>>,>>9.99")
                        else:
                            output_list.str = output_list.str + "Sub-Total " +\
                                to_string(t_credit, " ->>>,>>>,>>>,>>9") +\
                                fill(" ", 78) +\
                                to_string(t_famt, "  ->>>,>>>,>>>,>>9")
                        output_list = Output_list()
                        output_list_data.append(output_list)

                        t_credit = to_decimal("0")
                        t_famt = to_decimal("0")
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    for i in range(1, 19 + 1):
                        output_list.str = output_list.str + " "
                    output_list.str = output_list.str +\
                        to_string(artikel.artnr, ">>>>9") + " - " +\
                        to_string(artikel.bezeich, "x(34)")
                    artnr = artikel.artnr
                t_list.betrag = to_decimal(
                    t_list.betrag) - to_decimal(debitor.saldo)

                if guest.name != None:
                    temp_name = guest.name

                else:
                    temp_name = ""

                if guest.vorname1 != None:
                    temp_vorname1 = guest.vorname1

                else:
                    temp_vorname1 = ""

                if guest.anredefirma != None:
                    temp_anredefirma = guest.anredefirma

                else:
                    temp_anredefirma = ""

                if guest.anrede1 != None:
                    temp_anrede1 = guest.anrede1

                else:
                    temp_anrede1 = ""
                receiver = substring(f"{temp_name}, {temp_vorname1} {temp_anredefirma}{temp_anrede1}", 0, 32)
                output_list = Output_list()
                output_list_data.append(output_list)

                output_list.bill_art = artikel.artnr
                output_list.debt_counter = debitor.counter
                output_list.famt = to_string(
                    debt.vesrdep, "->>,>>>,>>>,>>9.99")

                if show_inv:

                    bill = get_cache(Bill, {"rechnr": [(eq, debitor.rechnr)]})

                    if bill:
                        output_list.inv_no = to_string(
                            bill.rechnr2, ">>>>>>>>>")

                        if bill.billref != 0:
                            output_list.soa_inv = "INV" + \
                                to_string(bill.billref, "9999999")
                    else:

                        bdebitor = get_cache(
                            Debitor, {"rechnr": [(eq, debitor.rechnr)], "debref": [(gt, 0)]})

                        if bdebitor:
                            output_list.soa_inv = "INV" + \
                                to_string(debitor.debref, "9999999")

                output_list.pay_amt = to_decimal(debitor.saldo)
                output_list.pay_famt = to_decimal(debitor.vesrdep)

                if not long_digit:
                    output_list.str = to_string(debt.rgdatum) +\
                        to_string(debitor.rechnr, ">>>,>>>,>>9") +\
                        to_string(receiver, "x(32)") +\
                        to_string(debt.saldo, "->,>>>,>>>,>>9.99") +\
                        to_string(debitor.saldo, "->,>>>,>>>,>>9.99") +\
                        to_string(art.bezeich, "x(34)") +\
                        to_string(debitor.rgdatum)
                else:
                    output_list.str = to_string(debt.rgdatum) +\
                        to_string(debitor.rechnr, ">>>,>>>,>>9") +\
                        to_string(receiver, "x(32)") +\
                        to_string(debt.saldo, " ->>>,>>>,>>>,>>9") +\
                        to_string(debitor.saldo, " ->>>,>>>,>>>,>>9") +\
                        to_string(art.bezeich, "x(34)") +\
                        to_string(debitor.rgdatum)
                output_list.bill_num = debitor.rechnr
                output_list.art_bezeich = artikel.bezeich
                output_list.tbetrag = to_decimal(
                    output_list.tbetrag) - to_decimal(debitor.saldo)

                bguest = get_cache(
                    Guest, {"gastnr": [(eq, debitor.gastnrmember)]})

                if bguest:
                    output_list.gastname = substring(f"{bguest.name}, {bguest.vorname1}{bguest.anredefirma} {bguest.anrede1}", 0, 32)

                bediener = get_cache(
                    Bediener, {"nr": [(eq, debitor.bediener_nr)]})

                if bediener:
                    output_list.str = output_list.str + \
                        to_string(bediener.userinit, "x(3)")
                else:
                    output_list.str = output_list.str + "   "
                output_list.str = output_list.str + \
                    to_string(debitor.vesrcod, "x(34)")
                output_list.str = output_list.str + to_string(" ", "x(22)")

                t_guest = get_cache(
                    Guest, {"gastnr": [(eq, debt.gastnrmember)]})

                if t_guest:
                    tstr = substring(f"{t_guest.name}, {t_guest.vorname1}{t_guest.anrede1}", 0, 34)
                else:
                    tstr = " "
                output_list.str = output_list.str + to_string(tstr, "x(50)")
                output_list.str = output_list.str + \
                    to_string(debitor.vesrdep, "->,>>>,>>>,>>9.99")
                output_list.str = output_list.str + \
                    to_string(debitor.zahlkonto, ">>>>9")
                output_list.str = output_list.str + \
                    to_string(debitor.vesrdep, "->,>>>,>>>,>>9.99")
                output_list.str = output_list.str + \
                    to_string(artikel.bezeich, "x(40)")

                t_credit = to_decimal(t_credit) + to_decimal(debitor.saldo)
                t_famt = to_decimal(t_famt) + to_decimal(debitor.vesrdep)
                tot_credit = to_decimal(tot_credit) + to_decimal(debitor.saldo)
                tot_saldo = to_decimal(tot_saldo) + to_decimal(debitor.saldo)
                tot_foreign = to_decimal(
                    tot_foreign) + to_decimal(debitor.vesrdep)
                tot_famt = to_decimal(tot_famt) + to_decimal(debitor.vesrdep)

                s_list = query(s_list_data, filters=(
                    lambda s_list: s_list.artnr == art.artnr), first=True)

                if not s_list:
                    s_list = S_list()
                    s_list_data.append(s_list)

                    s_list.artnr = art.artnr
                    s_list.bezeich = art.bezeich
                s_list.betrag = to_decimal(
                    s_list.betrag) + to_decimal(debitor.saldo)
        output_list = Output_list()
        output_list_data.append(output_list)

        for i in range(1, 58 + 1):
            output_list.str = output_list.str + "   "
        output_list.pay_amt = to_decimal(tot_saldo)
        output_list.pay_famt = to_decimal(tot_foreign)

        if not long_digit:
            output_list.str = output_list.str + "T O T A L " +\
                to_string(tot_saldo, "->,>>>,>>>,>>9.99") +\
                fill(" ", 78) +\
                to_string(tot_foreign, " ->>,>>>,>>>,>>9.99")
        else:
            output_list.str = output_list.str + "T O T A L " +\
                to_string(tot_saldo, " ->>>,>>>,>>>,>>9") +\
                fill(" ", 78) +\
                to_string(tot_foreign, "   ->>>,>>>,>>>,>>9")
        output_list = Output_list()
        output_list_data.append(output_list)

        output_list = Output_list()
        output_list_data.append(output_list)

        for i in range(1, 58 + 1):
            output_list.str = output_list.str + "   "
        output_list.pay_amt = to_decimal(t_credit)
        output_list.pay_famt = to_decimal(t_famt)

        if not long_digit:
            output_list.str = output_list.str + "Sub-Total " +\
                to_string(t_credit, "->,>>>,>>>,>>9.99") +\
                fill(" ", 78) +\
                to_string(t_famt, "->>,>>>,>>>,>>9.99")
        else:
            output_list.str = output_list.str + "Sub-Total " +\
                to_string(t_credit, " ->>>,>>>,>>>,>>9") +\
                fill(" ", 78) +\
                to_string(t_famt, "  ->>>,>>>,>>>,>>9")
        output_list = Output_list()
        output_list_data.append(output_list)

        output_list = Output_list()
        output_list_data.append(output_list)

        for i in range(1, 56 + 1):
            output_list.str = output_list.str + " "
        output_list.pay_amt = to_decimal(tot_credit)
        output_list.pay_famt = to_decimal(tot_famt)

        if not long_digit:
            output_list.str = output_list.str + "Grand TOTAL " +\
                to_string(tot_credit, "->,>>>,>>>,>>9.99") +\
                fill(" ", 78) + \
                to_string(tot_famt, "->>,>>>,>>>,>>9.99")
        else:
            output_list.str = output_list.str + "Grand TOTAL " +\
                to_string(tot_credit, " ->>>,>>>,>>>,>>9") +\
                fill(" ", 78) + \
                to_string(tot_famt, "->>,>>>,>>>,>>9.99")
        create_tot_payment()

    def create_list2e():

        nonlocal r_no, s_list_data, t_list_data, t_ar_paylist_data, long_digit, htparam, guest, debitor, artikel, bill, bediener, waehrung
        nonlocal comment, cledger, ccard, last_sort, from_date, to_date, from_art, to_art, mi_payment, mi_transfer, show_inv, bill_name, bill_nr
        nonlocal bguest, bdebitor

        nonlocal s_list, t_list, output_list, t_ar_paylist, bguest, bdebitor, tbuff, bq
        nonlocal s_list_data, t_list_data, output_list_data, t_ar_paylist_data

        artnr: int = 0
        i: int = 0
        curr_date: date = None
        t_credit: Decimal = to_decimal("0.0")
        tot_credit: Decimal = to_decimal("0.0")
        t_famt: Decimal = to_decimal("0.0")
        tot_famt: Decimal = to_decimal("0.0")
        tot_saldo: Decimal = to_decimal("0.0")
        tot_foreign: Decimal = to_decimal("0.0")
        receiver: string = ""
        do_it: bool = False
        temp_name: string = ""
        temp_vorname1: string = ""
        temp_anredefirma: string = ""
        temp_anrede1: string = ""
        debt = None
        art = None
        t_guest = None
        tstr: string = ""
        Debt = create_buffer("Debt", Debitor)
        Art = create_buffer("Art", Artikel)
        T_guest = create_buffer("T_guest", Guest)

        debitor_obj_list = {}
        debitor = Debitor()
        debt = Debitor()
        artikel = Artikel()
        art = Artikel()
        guest = Guest()
        for debitor.gastnr, debitor.saldo, debitor.zahlkonto, debitor.betriebsnr, debitor.counter, debitor.rechnr, debitor.debref, debitor.rgdatum, debitor.gastnrmember, debitor.bediener_nr, debitor.vesrcod, debitor.vesrdep, debitor.betrieb_gastmem, debitor._recid, debt.gastnr, debt.saldo, debt.zahlkonto, debt.betriebsnr, debt.counter, debt.rechnr, debt.debref, debt.rgdatum, debt.gastnrmember, debt.bediener_nr, debt.vesrcod, debt.vesrdep, debt.betrieb_gastmem, debt._recid, artikel.artnr, artikel.bezeich, artikel.artart, artikel._recid, art.artnr, art.bezeich, art.artart, art._recid, guest.name, guest.vorname1, guest.anredefirma, guest.anrede1, guest._recid in db_session.query(Debitor.gastnr, Debitor.saldo, Debitor.zahlkonto, Debitor.betriebsnr, Debitor.counter, Debitor.rechnr, Debitor.debref, Debitor.rgdatum, Debitor.gastnrmember, Debitor.bediener_nr, Debitor.vesrcod, Debitor.vesrdep, Debitor.betrieb_gastmem, Debitor._recid, Debt.gastnr, Debt.saldo, Debt.zahlkonto, Debt.betriebsnr, Debt.counter, Debt.rechnr, Debt.debref, Debt.rgdatum, Debt.gastnrmember, Debt.bediener_nr, Debt.vesrcod, Debt.vesrdep, Debt.betrieb_gastmem, Debt._recid, Artikel.artnr, Artikel.bezeich, Artikel.artart, Artikel._recid, Art.artnr, Art.bezeich, Art.artart, Art._recid, Guest.name, Guest.vorname1, Guest.anredefirma, Guest.anrede1, Guest._recid).join(Debt, (Debt.counter == Debitor.counter) & (Debt.zahlkonto == 0)).join(Artikel, (Artikel.artnr == Debitor.artnr) & (Artikel.departement == 0) & (Artikel.artart == 2)).join(Art, (Art.artnr == Debitor.zahlkonto) & (Art.departement == 0)).join(Guest, (Guest.gastnr == Debitor.gastnr)).filter(
                (Debitor.rgdatum >= from_date) & (Debitor.rgdatum <= to_date) & (Debitor.zahlkonto > 0) & (Debitor.artnr >= from_art) & (Debitor.artnr <= to_art) & (Debitor.counter > 0) & (Debitor.opart > 0)).order_by(Artikel.artnr, Debitor.rgdatum, Debitor.vesrcod, Debitor.name, Debitor.zahlkonto, Debitor.rechnr).all():
            if debitor_obj_list.get(debitor._recid):
                continue
            else:
                debitor_obj_list[debitor._recid] = True

            do_it = True

            if mi_payment:

                if artikel.artart == 2 and art.artart != 4 and art.artart != 7:
                    do_it = False

                elif artikel.artart == 7 and art.artart != 4:
                    do_it = False

            elif mi_transfer:

                if artikel.artart == 2 and (art.artart == 4 or art.artart == 7):
                    do_it = False

                elif artikel.artart == 7 and art.artart == 4:
                    do_it = False

            if do_it and (bill_name != "") and (substring(bill_name, 0, 1) != ("*").lower()):

                if not matches(guest.name, r"*" + bill_name + r"*"):
                    do_it = False

            if do_it and (bill_name != "") and (substring(bill_name, 0, 1) == ("*").lower()):

                if not matches(guest.name, bill_name):
                    do_it = False

            if do_it:

                if curr_date == None:
                    curr_date = debitor.rgdatum

                if curr_date != debitor.rgdatum:
                    curr_date = debitor.rgdatum
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    for i in range(1, 58 + 1):
                        output_list.str = output_list.str + "   "
                    output_list.pay_amt = to_decimal(tot_saldo)
                    output_list.pay_famt = to_decimal(tot_foreign)

                    if not long_digit:
                        output_list.str = output_list.str + "T O T A L " +\
                            to_string(tot_saldo, "->,>>>,>>>,>>9.99") +\
                            fill(" ", 78) +\
                            to_string(tot_foreign, " ->>,>>>,>>>,>>9.99")
                    else:
                        output_list.str = output_list.str + "T O T A L " +\
                            to_string(tot_saldo, " ->>>,>>>,>>>,>>9") +\
                            fill(" ", 78) +\
                            to_string(tot_foreign, "   ->>>,>>>,>>>,>>9")
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    tot_saldo = to_decimal("0")
                    tot_foreign = to_decimal("0")

                if artnr != artikel.artnr:
                    t_list = T_list()
                    t_list_data.append(t_list)

                    t_list.artnr = artikel.artnr
                    t_list.bezeich = artikel.bezeich

                    if artnr != 0:
                        output_list = Output_list()
                        output_list_data.append(output_list)

                        for i in range(1, 58 + 1):
                            output_list.str = output_list.str + "   "
                        output_list.pay_amt = to_decimal(tot_saldo)
                        output_list.pay_famt = to_decimal(t_famt)

                        if not long_digit:
                            output_list.str = output_list.str + "Sub-Total " +\
                                to_string(t_credit, "->,>>>,>>>,>>9.99") +\
                                fill(" ", 78) +\
                                to_string(t_famt, "->>,>>>,>>>,>>9.99")
                        else:
                            output_list.str = output_list.str + "Sub-Total " +\
                                to_string(t_credit, " ->>>,>>>,>>>,>>9") +\
                                fill(" ", 78) +\
                                to_string(t_famt, "  ->>>,>>>,>>>,>>9")
                        output_list = Output_list()
                        output_list_data.append(output_list)

                        t_credit = to_decimal("0")
                        t_famt = to_decimal("0")
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    for i in range(1, 19 + 1):
                        output_list.str = output_list.str + " "
                    output_list.str = output_list.str +\
                        to_string(artikel.artnr, ">>>>9") + " - " +\
                        to_string(artikel.bezeich, "x(34)")
                    artnr = artikel.artnr
                t_list.betrag = to_decimal(
                    t_list.betrag) - to_decimal(debitor.saldo)

                if guest.name != None:
                    temp_name = guest.name

                else:
                    temp_name = ""

                if guest.vorname1 != None:
                    temp_vorname1 = guest.vorname1

                else:
                    temp_vorname1 = ""

                if guest.anredefirma != None:
                    temp_anredefirma = guest.anredefirma

                else:
                    temp_anredefirma = ""

                if guest.anrede1 != None:
                    temp_anrede1 = guest.anrede1

                else:
                    temp_anrede1 = ""
                receiver = substring(f"{temp_name}, {temp_vorname1} {temp_anredefirma}{temp_anrede1}", 0, 32)
                output_list = Output_list()
                output_list_data.append(output_list)

                output_list.bill_art = artikel.artnr
                output_list.debt_counter = debitor.counter
                output_list.famt = to_string(
                    debt.vesrdep, "->>,>>>,>>>,>>9.99")

                if show_inv:

                    bill = get_cache(Bill, {"rechnr": [(eq, debitor.rechnr)]})

                    if bill:
                        output_list.inv_no = to_string(
                            bill.rechnr2, ">>>>>>>>>")

                        if bill.billref != 0:
                            output_list.soa_inv = "INV" + \
                                to_string(bill.billref, "9999999")
                    else:

                        bdebitor = get_cache(
                            Debitor, {"rechnr": [(eq, debitor.rechnr)], "debref": [(gt, 0)]})

                        if bdebitor:
                            output_list.soa_inv = "INV" + \
                                to_string(debitor.debref, "9999999")

                output_list.pay_amt = to_decimal(debitor.saldo)
                output_list.pay_famt = to_decimal(debitor.vesrdep)

                if not long_digit:
                    output_list.str = to_string(debt.rgdatum) +\
                        to_string(debitor.rechnr, ">>>,>>>,>>9") +\
                        to_string(receiver, "x(32)") +\
                        to_string(debt.saldo, "->,>>>,>>>,>>9.99") +\
                        to_string(debitor.saldo, "->,>>>,>>>,>>9.99") +\
                        to_string(art.bezeich, "x(34)") +\
                        to_string(debitor.rgdatum)
                else:
                    output_list.str = to_string(debt.rgdatum) +\
                        to_string(debitor.rechnr, ">>>,>>>,>>9") +\
                        to_string(receiver, "x(32)") +\
                        to_string(debt.saldo, " ->>>,>>>,>>>,>>9") +\
                        to_string(debitor.saldo, " ->>>,>>>,>>>,>>9") +\
                        to_string(art.bezeich, "x(34)") +\
                        to_string(debitor.rgdatum)
                output_list.bill_num = debitor.rechnr
                output_list.art_bezeich = artikel.bezeich
                output_list.tbetrag = to_decimal(
                    output_list.tbetrag) - to_decimal(debitor.saldo)

                bguest = get_cache(
                    Guest, {"gastnr": [(eq, debitor.gastnrmember)]})

                if bguest:
                    output_list.gastname = substring(f"{bguest.name}, {bguest.vorname1}{bguest.anredefirma} {bguest.anrede1}", 0, 32)

                bediener = get_cache(
                    Bediener, {"nr": [(eq, debitor.bediener_nr)]})

                if bediener:
                    output_list.str = output_list.str + \
                        to_string(bediener.userinit, "x(3)")
                else:
                    output_list.str = output_list.str + "   "
                output_list.str = output_list.str + \
                    to_string(debitor.vesrcod, "x(34)")
                output_list.str = output_list.str + to_string(" ", "x(22)")

                t_guest = get_cache(
                    Guest, {"gastnr": [(eq, debt.gastnrmember)]})

                if t_guest:
                    tstr = substring(f"{t_guest.name}, {t_guest.vorname1}{t_guest.anrede1}", 0, 34)
                else:
                    tstr = " "
                output_list.str = output_list.str + to_string(tstr, "x(50)")
                output_list.str = output_list.str + \
                    to_string(debitor.vesrdep, "->,>>>,>>>,>>9.99")
                output_list.str = output_list.str + \
                    to_string(debitor.zahlkonto, ">>>>9")
                output_list.str = output_list.str + \
                    to_string(debitor.vesrdep, "->,>>>,>>>,>>9.99")
                output_list.str = output_list.str + \
                    to_string(artikel.bezeich, "x(40)")

                t_credit = to_decimal(t_credit) + to_decimal(debitor.saldo)
                t_famt = to_decimal(t_famt) + to_decimal(debitor.vesrdep)
                tot_credit = to_decimal(tot_credit) + to_decimal(debitor.saldo)
                tot_saldo = to_decimal(tot_saldo) + to_decimal(debitor.saldo)
                tot_foreign = to_decimal(
                    tot_foreign) + to_decimal(debitor.vesrdep)
                tot_famt = to_decimal(tot_famt) + to_decimal(debitor.vesrdep)

                s_list = query(s_list_data, filters=(
                    lambda s_list: s_list.artnr == art.artnr), first=True)

                if not s_list:
                    s_list = S_list()
                    s_list_data.append(s_list)

                    s_list.artnr = art.artnr
                    s_list.bezeich = art.bezeich
                s_list.betrag = to_decimal(
                    s_list.betrag) + to_decimal(debitor.saldo)
        output_list = Output_list()
        output_list_data.append(output_list)

        for i in range(1, 58 + 1):
            output_list.str = output_list.str + "   "
        output_list.pay_amt = to_decimal(tot_saldo)
        output_list.pay_famt = to_decimal(tot_foreign)

        if not long_digit:
            output_list.str = output_list.str + "T O T A L " +\
                to_string(tot_saldo, "->,>>>,>>>,>>9.99") +\
                fill(" ", 78) +\
                to_string(tot_foreign, " ->>,>>>,>>>,>>9.99")
        else:
            output_list.str = output_list.str + "T O T A L " +\
                to_string(tot_saldo, " ->>>,>>>,>>>,>>9") +\
                fill(" ", 78) +\
                to_string(tot_foreign, "   ->>>,>>>,>>>,>>9")
        output_list = Output_list()
        output_list_data.append(output_list)

        output_list = Output_list()
        output_list_data.append(output_list)

        for i in range(1, 58 + 1):
            output_list.str = output_list.str + "   "
        output_list.pay_amt = to_decimal(t_credit)
        output_list.pay_famt = to_decimal(t_famt)

        if not long_digit:
            output_list.str = output_list.str + "Sub-Total " +\
                to_string(t_credit, "->,>>>,>>>,>>9.99") +\
                fill(" ", 78) +\
                to_string(t_famt, "->>,>>>,>>>,>>9.99")
        else:
            output_list.str = output_list.str + "Sub-Total " +\
                to_string(t_credit, " ->>>,>>>,>>>,>>9") +\
                fill(" ", 78) +\
                to_string(t_famt, "  ->>>,>>>,>>>,>>9")
        output_list = Output_list()
        output_list_data.append(output_list)

        output_list = Output_list()
        output_list_data.append(output_list)

        for i in range(1, 56 + 1):
            output_list.str = output_list.str + " "
        output_list.pay_amt = to_decimal(tot_credit)
        output_list.pay_famt = to_decimal(tot_famt)

        if not long_digit:
            output_list.str = output_list.str + "Grand TOTAL " +\
                to_string(tot_credit, "->,>>>,>>>,>>9.99") +\
                fill(" ", 78) + \
                to_string(tot_famt, "->>,>>>,>>>,>>9.99")
        else:
            output_list.str = output_list.str + "Grand TOTAL " +\
                to_string(tot_credit, " ->>>,>>>,>>>,>>9") +\
                fill(" ", 78) + \
                to_string(tot_famt, "->>,>>>,>>>,>>9.99")
        create_tot_payment()

    def create_list2f():

        nonlocal r_no, s_list_data, t_list_data, t_ar_paylist_data, long_digit, htparam, guest, debitor, artikel, bill, bediener, waehrung
        nonlocal comment, cledger, ccard, last_sort, from_date, to_date, from_art, to_art, mi_payment, mi_transfer, show_inv, bill_name, bill_nr
        nonlocal bguest, bdebitor

        nonlocal s_list, t_list, output_list, t_ar_paylist, bguest, bdebitor, tbuff, bq
        nonlocal s_list_data, t_list_data, output_list_data, t_ar_paylist_data

        artnr: int = 0
        i: int = 0
        curr_gastnr: int = 0
        t_credit: Decimal = to_decimal("0.0")
        tot_credit: Decimal = to_decimal("0.0")
        t_famt: Decimal = to_decimal("0.0")
        tot_famt: Decimal = to_decimal("0.0")
        tot_saldo: Decimal = to_decimal("0.0")
        tot_foreign: Decimal = to_decimal("0.0")
        receiver: string = ""
        do_it: bool = False
        temp_name: string = ""
        temp_vorname1: string = ""
        temp_anredefirma: string = ""
        temp_anrede1: string = ""
        debt = None
        art = None
        t_guest = None
        tstr: string = ""
        Debt = create_buffer("Debt", Debitor)
        Art = create_buffer("Art", Artikel)
        T_guest = create_buffer("T_guest", Guest)

        debitor_obj_list = {}
        debitor = Debitor()
        debt = Debitor()
        artikel = Artikel()
        art = Artikel()
        guest = Guest()
        for debitor.gastnr, debitor.saldo, debitor.zahlkonto, debitor.betriebsnr, debitor.counter, debitor.rechnr, debitor.debref, debitor.rgdatum, debitor.gastnrmember, debitor.bediener_nr, debitor.vesrcod, debitor.vesrdep, debitor.betrieb_gastmem, debitor._recid, debt.gastnr, debt.saldo, debt.zahlkonto, debt.betriebsnr, debt.counter, debt.rechnr, debt.debref, debt.rgdatum, debt.gastnrmember, debt.bediener_nr, debt.vesrcod, debt.vesrdep, debt.betrieb_gastmem, debt._recid, artikel.artnr, artikel.bezeich, artikel.artart, artikel._recid, art.artnr, art.bezeich, art.artart, art._recid, guest.name, guest.vorname1, guest.anredefirma, guest.anrede1, guest._recid in db_session.query(Debitor.gastnr, Debitor.saldo, Debitor.zahlkonto, Debitor.betriebsnr, Debitor.counter, Debitor.rechnr, Debitor.debref, Debitor.rgdatum, Debitor.gastnrmember, Debitor.bediener_nr, Debitor.vesrcod, Debitor.vesrdep, Debitor.betrieb_gastmem, Debitor._recid, Debt.gastnr, Debt.saldo, Debt.zahlkonto, Debt.betriebsnr, Debt.counter, Debt.rechnr, Debt.debref, Debt.rgdatum, Debt.gastnrmember, Debt.bediener_nr, Debt.vesrcod, Debt.vesrdep, Debt.betrieb_gastmem, Debt._recid, Artikel.artnr, Artikel.bezeich, Artikel.artart, Artikel._recid, Art.artnr, Art.bezeich, Art.artart, Art._recid, Guest.name, Guest.vorname1, Guest.anredefirma, Guest.anrede1, Guest._recid).join(Debt, (Debt.counter == Debitor.counter) & (Debt.zahlkonto == 0)).join(Artikel, (Artikel.artnr == Debitor.artnr) & (Artikel.departement == 0) & (Artikel.artart == 2)).join(Art, (Art.artnr == Debitor.zahlkonto) & (Art.departement == 0)).join(Guest, (Guest.gastnr == Debitor.gastnr)).filter(
                (Debitor.zahlkonto > 0) & (Debitor.artnr >= from_art) & (Debitor.artnr <= to_art) & (Debitor.counter > 0) & (Debitor.opart > 0) & (Debitor.rechnr == bill_nr)).order_by(Artikel.artnr, Debitor.name, Debitor.gastnr, Debitor.rgdatum, Debitor.zahlkonto, Debitor.betriebsnr, Debitor.rechnr).all():
            if debitor_obj_list.get(debitor._recid):
                continue
            else:
                debitor_obj_list[debitor._recid] = True

            do_it = True

            if mi_payment:

                if artikel.artart == 2 and art.artart != 4 and art.artart != 7:
                    do_it = False

                elif artikel.artart == 7 and art.artart != 4:
                    do_it = False

            elif mi_transfer:

                if artikel.artart == 2 and (art.artart == 4 or art.artart == 7):
                    do_it = False

                elif artikel.artart == 7 and art.artart == 4:
                    do_it = False

            if do_it and (bill_name != "") and (substring(bill_name, 0, 1) != ("*").lower()):

                if not matches(guest.name, r"*" + bill_name + r"*"):
                    do_it = False

            if do_it and (bill_name != "") and (substring(bill_name, 0, 1) == ("*").lower()):

                if not matches(guest.name, bill_name):
                    do_it = False

            if do_it:

                if curr_gastnr == 0:
                    curr_gastnr = debitor.gastnr

                if curr_gastnr != debitor.gastnr:
                    curr_gastnr = debitor.gastnr
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    for i in range(1, 58 + 1):
                        output_list.str = output_list.str + "   "
                    output_list.pay_amt = to_decimal(tot_saldo)
                    output_list.pay_famt = to_decimal(tot_foreign)

                    if not long_digit:
                        output_list.str = output_list.str + "T O T A L " +\
                            to_string(tot_saldo, "->,>>>,>>>,>>9.99") +\
                            fill(" ", 78) +\
                            to_string(tot_foreign, " ->>,>>>,>>>,>>9.99")
                    else:
                        output_list.str = output_list.str + "T O T A L " +\
                            to_string(tot_saldo, " ->>>,>>>,>>>,>>9") +\
                            fill(" ", 78) +\
                            to_string(tot_foreign, "   ->>>,>>>,>>>,>>9")
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    tot_saldo = to_decimal("0")
                    tot_foreign = to_decimal("0")

                if artnr != artikel.artnr:
                    t_list = T_list()
                    t_list_data.append(t_list)

                    t_list.artnr = artikel.artnr
                    t_list.bezeich = artikel.bezeich

                    if artnr != 0:
                        output_list = Output_list()
                        output_list_data.append(output_list)

                        for i in range(1, 58 + 1):
                            output_list.str = output_list.str + "   "
                        output_list.pay_amt = to_decimal(t_credit)
                        output_list.pay_famt = to_decimal(t_famt)

                        if not long_digit:
                            output_list.str = output_list.str + "Sub-Total " +\
                                to_string(t_credit, "->,>>>,>>>,>>9.99") +\
                                fill(" ", 78) +\
                                to_string(t_famt, "->>,>>>,>>>,>>9.99")
                        else:
                            output_list.str = output_list.str + "Sub-Total " +\
                                to_string(t_credit, " ->>>,>>>,>>>,>>9") +\
                                fill(" ", 78) +\
                                to_string(t_famt, "  ->>>,>>>,>>>,>>9")
                        output_list = Output_list()
                        output_list_data.append(output_list)

                        t_credit = to_decimal("0")
                        t_famt = to_decimal("0")
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    for i in range(1, 19 + 1):
                        output_list.str = output_list.str + " "
                    output_list.str = output_list.str +\
                        to_string(artikel.artnr, ">>>>9") + " - " +\
                        to_string(artikel.bezeich, "x(24)")
                    artnr = artikel.artnr
                t_list.betrag = to_decimal(
                    t_list.betrag) - to_decimal(debitor.saldo)

                if guest.name != None:
                    temp_name = guest.name

                else:
                    temp_name = ""

                if guest.vorname1 != None:
                    temp_vorname1 = guest.vorname1

                else:
                    temp_vorname1 = ""

                if guest.anredefirma != None:
                    temp_anredefirma = guest.anredefirma

                else:
                    temp_anredefirma = ""

                if guest.anrede1 != None:
                    temp_anrede1 = guest.anrede1

                else:
                    temp_anrede1 = ""
                receiver = substring(f"{temp_name}, {temp_vorname1} {temp_anredefirma}{temp_anrede1}", 0, 32)
                output_list = Output_list()
                output_list_data.append(output_list)

                output_list.bill_art = artikel.artnr
                output_list.debt_counter = debitor.counter
                output_list.famt = to_string(
                    debt.vesrdep, "->>,>>>,>>>,>>9.99")

                if show_inv:

                    bill = get_cache(Bill, {"rechnr": [(eq, debitor.rechnr)]})

                    if bill:
                        output_list.inv_no = to_string(
                            bill.rechnr2, ">>>>>>>>>")

                        if bill.billref != 0:
                            output_list.soa_inv = "INV" + \
                                to_string(bill.billref, "9999999")
                    else:

                        bdebitor = get_cache(
                            Debitor, {"rechnr": [(eq, debitor.rechnr)], "debref": [(gt, 0)]})

                        if bdebitor:
                            output_list.soa_inv = "INV" + \
                                to_string(debitor.debref, "9999999")

                output_list.pay_amt = to_decimal(debitor.saldo)
                output_list.pay_famt = to_decimal(debitor.vesrdep)

                if not long_digit:
                    output_list.str = to_string(debt.rgdatum) +\
                        to_string(debitor.rechnr, ">>>,>>>,>>9") +\
                        to_string(receiver, "x(32)") +\
                        to_string(debt.saldo, "->,>>>,>>>,>>9.99") +\
                        to_string(debitor.saldo, "->,>>>,>>>,>>9.99") +\
                        to_string(art.bezeich, "x(34)") +\
                        to_string(debitor.rgdatum)
                else:
                    output_list.str = to_string(debt.rgdatum) +\
                        to_string(debitor.rechnr, ">>>,>>>,>>9") +\
                        to_string(receiver, "x(32)") +\
                        to_string(debt.saldo, " ->>>,>>>,>>>,>>9") +\
                        to_string(debitor.saldo, " ->>>,>>>,>>>,>>9") +\
                        to_string(art.bezeich, "x(34)") +\
                        to_string(debitor.rgdatum)
                output_list.bill_num = debitor.rechnr
                output_list.art_bezeich = artikel.bezeich
                output_list.tbetrag = to_decimal(
                    output_list.tbetrag) - to_decimal(debitor.saldo)

                bguest = get_cache(
                    Guest, {"gastnr": [(eq, debitor.gastnrmember)]})

                if bguest:
                    output_list.gastname = substring(f"{bguest.name}, {bguest.vorname1}{bguest.anredefirma} {bguest.anrede1}", 0, 32)

                bediener = get_cache(
                    Bediener, {"nr": [(eq, debitor.bediener_nr)]})

                if bediener:
                    output_list.str = output_list.str + \
                        to_string(bediener.userinit, "x(3)")
                else:
                    output_list.str = output_list.str + "   "
                output_list.str = output_list.str + \
                    to_string(debitor.vesrcod, "x(34)")
                output_list.str = output_list.str + to_string(" ", "x(22)")

                t_guest = get_cache(
                    Guest, {"gastnr": [(eq, debt.gastnrmember)]})

                if t_guest:
                    tstr = substring(f"{t_guest.name}, {t_guest.vorname1}{t_guest.anrede1}", 0, 34)
                else:
                    tstr = " "
                output_list.str = output_list.str + to_string(tstr, "x(50)")
                output_list.str = output_list.str + \
                    to_string(debitor.vesrdep, "->,>>>,>>>,>>9.99")
                output_list.str = output_list.str + \
                    to_string(debitor.zahlkonto, ">>>>9")
                output_list.str = output_list.str + \
                    to_string(debitor.vesrdep, "->,>>>,>>>,>>9.99")
                output_list.str = output_list.str + \
                    to_string(artikel.bezeich, "x(40)")

                t_credit = to_decimal(t_credit) + to_decimal(debitor.saldo)
                t_famt = to_decimal(t_famt) + to_decimal(debitor.vesrdep)
                tot_credit = to_decimal(tot_credit) + to_decimal(debitor.saldo)
                tot_saldo = to_decimal(tot_saldo) + to_decimal(debitor.saldo)
                tot_foreign = to_decimal(
                    tot_foreign) + to_decimal(debitor.vesrdep)
                tot_famt = to_decimal(tot_famt) + to_decimal(debitor.vesrdep)

                s_list = query(s_list_data, filters=(
                    lambda s_list: s_list.artnr == art.artnr), first=True)

                if not s_list:
                    s_list = S_list()
                    s_list_data.append(s_list)

                    s_list.artnr = art.artnr
                    s_list.bezeich = art.bezeich
                s_list.betrag = to_decimal(
                    s_list.betrag) + to_decimal(debitor.saldo)
        output_list = Output_list()
        output_list_data.append(output_list)

        for i in range(1, 58 + 1):
            output_list.str = output_list.str + "   "
        output_list.pay_amt = to_decimal(tot_saldo)
        output_list.pay_famt = to_decimal(tot_foreign)

        if not long_digit:
            output_list.str = output_list.str + "T O T A L " +\
                to_string(tot_saldo, "->,>>>,>>>,>>9.99") +\
                fill(" ", 78) +\
                to_string(tot_foreign, " ->>,>>>,>>>,>>9.99")
        else:
            output_list.str = output_list.str + "T O T A L " +\
                to_string(tot_saldo, " ->>>,>>>,>>>,>>9") +\
                fill(" ", 78) +\
                to_string(tot_foreign, "   ->>>,>>>,>>>,>>9")
        output_list = Output_list()
        output_list_data.append(output_list)

        output_list = Output_list()
        output_list_data.append(output_list)

        for i in range(1, 58 + 1):
            output_list.str = output_list.str + "   "
        output_list.pay_amt = to_decimal(t_credit)
        output_list.pay_famt = to_decimal(t_famt)

        if not long_digit:
            output_list.str = output_list.str + "Sub-Total " +\
                to_string(t_credit, "->,>>>,>>>,>>9.99") +\
                fill(" ", 78) +\
                to_string(t_famt, "->>,>>>,>>>,>>9.99")
        else:
            output_list.str = output_list.str + "Sub-Total " +\
                to_string(t_credit, " ->>>,>>>,>>>,>>9") +\
                fill(" ", 78) +\
                to_string(t_famt, "  ->>>,>>>,>>>,>>9")
        output_list = Output_list()
        output_list_data.append(output_list)

        output_list = Output_list()
        output_list_data.append(output_list)

        for i in range(1, 56 + 1):
            output_list.str = output_list.str + " "
        output_list.pay_amt = to_decimal(tot_credit)
        output_list.pay_famt = to_decimal(tot_famt)

        if not long_digit:
            output_list.str = output_list.str + "Grand TOTAL " +\
                to_string(tot_credit, "->,>>>,>>>,>>9.99") +\
                fill(" ", 78) + \
                to_string(tot_famt, "->>,>>>,>>>,>>9.99")
        else:
            output_list.str = output_list.str + "Grand TOTAL " +\
                to_string(tot_credit, " ->>>,>>>,>>>,>>9") +\
                fill(" ", 78) + \
                to_string(tot_famt, "  ->>>,>>>,>>>,>>9")
        create_tot_payment()

    def create_list2fs():

        nonlocal r_no, s_list_data, t_list_data, t_ar_paylist_data, long_digit, htparam, guest, debitor, artikel, bill, bediener, waehrung
        nonlocal comment, cledger, ccard, last_sort, from_date, to_date, from_art, to_art, mi_payment, mi_transfer, show_inv, bill_name, bill_nr
        nonlocal bguest, bdebitor

        nonlocal s_list, t_list, output_list, t_ar_paylist, bguest, bdebitor, tbuff, bq
        nonlocal s_list_data, t_list_data, output_list_data, t_ar_paylist_data

        artnr: int = 0
        i: int = 0
        curr_gastnr: int = 0
        t_credit: Decimal = to_decimal("0.0")
        tot_credit: Decimal = to_decimal("0.0")
        t_famt: Decimal = to_decimal("0.0")
        tot_famt: Decimal = to_decimal("0.0")
        tot_saldo: Decimal = to_decimal("0.0")
        tot_foreign: Decimal = to_decimal("0.0")
        receiver: string = ""
        do_it: bool = False
        temp_name: string = ""
        temp_vorname1: string = ""
        temp_anredefirma: string = ""
        temp_anrede1: string = ""
        debt = None
        art = None
        t_guest = None
        tstr: string = ""
        Debt = create_buffer("Debt", Debitor)
        Art = create_buffer("Art", Artikel)
        T_guest = create_buffer("T_guest", Guest)

        debitor_obj_list = {}
        debitor = Debitor()
        debt = Debitor()
        artikel = Artikel()
        art = Artikel()
        guest = Guest()
        for debitor.gastnr, debitor.saldo, debitor.zahlkonto, debitor.betriebsnr, debitor.counter, debitor.rechnr, debitor.debref, debitor.rgdatum, debitor.gastnrmember, debitor.bediener_nr, debitor.vesrcod, debitor.vesrdep, debitor.betrieb_gastmem, debitor._recid, debt.gastnr, debt.saldo, debt.zahlkonto, debt.betriebsnr, debt.counter, debt.rechnr, debt.debref, debt.rgdatum, debt.gastnrmember, debt.bediener_nr, debt.vesrcod, debt.vesrdep, debt.betrieb_gastmem, debt._recid, artikel.artnr, artikel.bezeich, artikel.artart, artikel._recid, art.artnr, art.bezeich, art.artart, art._recid, guest.name, guest.vorname1, guest.anredefirma, guest.anrede1, guest._recid in db_session.query(Debitor.gastnr, Debitor.saldo, Debitor.zahlkonto, Debitor.betriebsnr, Debitor.counter, Debitor.rechnr, Debitor.debref, Debitor.rgdatum, Debitor.gastnrmember, Debitor.bediener_nr, Debitor.vesrcod, Debitor.vesrdep, Debitor.betrieb_gastmem, Debitor._recid, Debt.gastnr, Debt.saldo, Debt.zahlkonto, Debt.betriebsnr, Debt.counter, Debt.rechnr, Debt.debref, Debt.rgdatum, Debt.gastnrmember, Debt.bediener_nr, Debt.vesrcod, Debt.vesrdep, Debt.betrieb_gastmem, Debt._recid, Artikel.artnr, Artikel.bezeich, Artikel.artart, Artikel._recid, Art.artnr, Art.bezeich, Art.artart, Art._recid, Guest.name, Guest.vorname1, Guest.anredefirma, Guest.anrede1, Guest._recid).join(Debt, (Debt.counter == Debitor.counter) & (Debt.zahlkonto == 0)).join(Artikel, (Artikel.artnr == Debitor.artnr) & (Artikel.departement == 0) & (Artikel.artart == 2)).join(Art, (Art.artnr == Debitor.zahlkonto) & (Art.departement == 0)).join(Guest, (Guest.gastnr == Debitor.gastnr)).filter(
                (Debitor.rgdatum >= from_date) & (Debitor.rgdatum <= to_date) & (Debitor.zahlkonto > 0) & (Debitor.artnr >= from_art) & (Debitor.artnr <= to_art) & (Debitor.counter > 0) & (Debitor.opart > 0)).order_by(Artikel.artnr, Debitor.name, Debitor.gastnr, Debitor.rgdatum, Debitor.zahlkonto, Debitor.betriebsnr, Debitor.rechnr).all():
            if debitor_obj_list.get(debitor._recid):
                continue
            else:
                debitor_obj_list[debitor._recid] = True

            do_it = True

            if mi_payment:

                if artikel.artart == 2 and art.artart != 4 and art.artart != 7:
                    do_it = False

                elif artikel.artart == 7 and art.artart != 4:
                    do_it = False

            elif mi_transfer:

                if artikel.artart == 2 and (art.artart == 4 or art.artart == 7):
                    do_it = False

                elif artikel.artart == 7 and art.artart == 4:
                    do_it = False

            if do_it and (bill_name != "") and (substring(bill_name, 0, 1) != ("*").lower()):

                if not matches(guest.name, r"*" + bill_name + r"*"):
                    do_it = False

            if do_it and (bill_name != "") and (substring(bill_name, 0, 1) == ("*").lower()):

                if not matches(guest.name, bill_name):
                    do_it = False

            if do_it:

                if curr_gastnr == 0:
                    curr_gastnr = debitor.gastnr

                if curr_gastnr != debitor.gastnr:
                    curr_gastnr = debitor.gastnr
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    for i in range(1, 58 + 1):
                        output_list.str = output_list.str + "   "
                    output_list.pay_amt = to_decimal(tot_saldo)
                    output_list.pay_famt = to_decimal(tot_foreign)

                    if not long_digit:
                        output_list.str = output_list.str + "T O T A L " +\
                            to_string(tot_saldo, "->,>>>,>>>,>>9.99") +\
                            fill(" ", 78) +\
                            to_string(tot_foreign, " ->>,>>>,>>>,>>9.99")
                    else:
                        output_list.str = output_list.str + "T O T A L " +\
                            to_string(tot_saldo, " ->>>,>>>,>>>,>>9") +\
                            fill(" ", 78) +\
                            to_string(tot_foreign, "   ->>>,>>>,>>>,>>9")
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    tot_saldo = to_decimal("0")
                    tot_foreign = to_decimal("0")

                if artnr != artikel.artnr:
                    t_list = T_list()
                    t_list_data.append(t_list)

                    t_list.artnr = artikel.artnr
                    t_list.bezeich = artikel.bezeich

                    if artnr != 0:
                        output_list = Output_list()
                        output_list_data.append(output_list)

                        for i in range(1, 58 + 1):
                            output_list.str = output_list.str + "   "
                        output_list.pay_amt = to_decimal(t_credit)
                        output_list.pay_famt = to_decimal(t_famt)

                        if not long_digit:
                            output_list.str = output_list.str + "Sub-Total " +\
                                to_string(t_credit, "->,>>>,>>>,>>9.99") +\
                                fill(" ", 78) +\
                                to_string(t_famt, "->>,>>>,>>>,>>9.99")
                        else:
                            output_list.str = output_list.str + "Sub-Total " +\
                                to_string(t_credit, " ->>>,>>>,>>>,>>9") +\
                                fill(" ", 78) +\
                                to_string(t_famt, "  ->>>,>>>,>>>,>>9")
                        output_list = Output_list()
                        output_list_data.append(output_list)

                        t_credit = to_decimal("0")
                        t_famt = to_decimal("0")
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    for i in range(1, 19 + 1):
                        output_list.str = output_list.str + " "
                    output_list.str = output_list.str +\
                        to_string(artikel.artnr, ">>>>9") + " - " +\
                        to_string(artikel.bezeich, "x(24)")
                    artnr = artikel.artnr
                t_list.betrag = to_decimal(
                    t_list.betrag) - to_decimal(debitor.saldo)

                if guest.name != None:
                    temp_name = guest.name

                else:
                    temp_name = ""

                if guest.vorname1 != None:
                    temp_vorname1 = guest.vorname1

                else:
                    temp_vorname1 = ""

                if guest.anredefirma != None:
                    temp_anredefirma = guest.anredefirma

                else:
                    temp_anredefirma = ""

                if guest.anrede1 != None:
                    temp_anrede1 = guest.anrede1

                else:
                    temp_anrede1 = ""
                receiver = substring(f"{temp_name}, {temp_vorname1} {temp_anredefirma}{temp_anrede1}", 0, 32)
                output_list = Output_list()
                output_list_data.append(output_list)

                output_list.bill_art = artikel.artnr
                output_list.debt_counter = debitor.counter
                output_list.famt = to_string(
                    debt.vesrdep, "->>,>>>,>>>,>>9.99")

                if show_inv:

                    bill = get_cache(Bill, {"rechnr": [(eq, debitor.rechnr)]})

                    if bill:
                        output_list.inv_no = to_string(
                            bill.rechnr2, ">>>>>>>>>")

                        if bill.billref != 0:
                            output_list.soa_inv = "INV" + \
                                to_string(bill.billref, "9999999")
                    else:

                        bdebitor = get_cache(
                            Debitor, {"rechnr": [(eq, debitor.rechnr)], "debref": [(gt, 0)]})

                        if bdebitor:
                            output_list.soa_inv = "INV" + \
                                to_string(debitor.debref, "9999999")

                output_list.pay_amt = to_decimal(debitor.saldo)
                output_list.pay_famt = to_decimal(debitor.vesrdep)

                if not long_digit:
                    output_list.str = to_string(debt.rgdatum) +\
                        to_string(debitor.rechnr, ">>>,>>>,>>9") +\
                        to_string(receiver, "x(32)") +\
                        to_string(debt.saldo, "->,>>>,>>>,>>9.99") +\
                        to_string(debitor.saldo, "->,>>>,>>>,>>9.99") +\
                        to_string(art.bezeich, "x(34)") +\
                        to_string(debitor.rgdatum)
                else:
                    output_list.str = to_string(debt.rgdatum) +\
                        to_string(debitor.rechnr, ">>>,>>>,>>9") +\
                        to_string(receiver, "x(32)") +\
                        to_string(debt.saldo, " ->>>,>>>,>>>,>>9") +\
                        to_string(debitor.saldo, " ->>>,>>>,>>>,>>9") +\
                        to_string(art.bezeich, "x(34)") +\
                        to_string(debitor.rgdatum)
                output_list.bill_num = debitor.rechnr
                output_list.art_bezeich = artikel.bezeich
                output_list.tbetrag = to_decimal(
                    output_list.tbetrag) - to_decimal(debitor.saldo)

                bguest = get_cache(
                    Guest, {"gastnr": [(eq, debitor.gastnrmember)]})

                if bguest:
                    output_list.gastname = substring(f"{bguest.name}, {bguest.vorname1}{bguest.anredefirma} {bguest.anrede1}", 0, 32)

                bediener = get_cache(
                    Bediener, {"nr": [(eq, debitor.bediener_nr)]})

                if bediener:
                    output_list.str = output_list.str + \
                        to_string(bediener.userinit, "x(3)")
                else:
                    output_list.str = output_list.str + "   "
                output_list.str = output_list.str + \
                    to_string(debitor.vesrcod, "x(34)")
                output_list.str = output_list.str + to_string(" ", "x(22)")

                t_guest = get_cache(
                    Guest, {"gastnr": [(eq, debt.gastnrmember)]})

                if t_guest:
                    tstr = substring(f"{t_guest.name}, {t_guest.vorname1}{t_guest.anrede1}", 0, 34)
                else:
                    tstr = " "
                output_list.str = output_list.str + to_string(tstr, "x(50)")
                output_list.str = output_list.str + \
                    to_string(debitor.vesrdep, "->,>>>,>>>,>>9.99")
                output_list.str = output_list.str + \
                    to_string(debitor.zahlkonto, ">>>>9")
                output_list.str = output_list.str + \
                    to_string(debitor.vesrdep, "->,>>>,>>>,>>9.99")
                output_list.str = output_list.str + \
                    to_string(artikel.bezeich, "x(40)")

                t_credit = to_decimal(t_credit) + to_decimal(debitor.saldo)
                t_famt = to_decimal(t_famt) + to_decimal(debitor.vesrdep)
                tot_credit = to_decimal(tot_credit) + to_decimal(debitor.saldo)
                tot_saldo = to_decimal(tot_saldo) + to_decimal(debitor.saldo)
                tot_foreign = to_decimal(
                    tot_foreign) + to_decimal(debitor.vesrdep)
                tot_famt = to_decimal(tot_famt) + to_decimal(debitor.vesrdep)

                s_list = query(s_list_data, filters=(
                    lambda s_list: s_list.artnr == art.artnr), first=True)

                if not s_list:
                    s_list = S_list()
                    s_list_data.append(s_list)

                    s_list.artnr = art.artnr
                    s_list.bezeich = art.bezeich
                s_list.betrag = to_decimal(
                    s_list.betrag) + to_decimal(debitor.saldo)
        output_list = Output_list()
        output_list_data.append(output_list)

        for i in range(1, 58 + 1):
            output_list.str = output_list.str + "   "
        output_list.pay_amt = to_decimal(tot_saldo)
        output_list.pay_famt = to_decimal(tot_foreign)

        if not long_digit:
            output_list.str = output_list.str + "T O T A L " +\
                to_string(tot_saldo, "->,>>>,>>>,>>9.99") +\
                fill(" ", 78) +\
                to_string(tot_foreign, " ->>,>>>,>>>,>>9.99")
        else:
            output_list.str = output_list.str + "T O T A L " +\
                to_string(tot_saldo, " ->>>,>>>,>>>,>>9") +\
                fill(" ", 78) +\
                to_string(tot_foreign, "   ->>>,>>>,>>>,>>9")
        output_list = Output_list()
        output_list_data.append(output_list)

        output_list = Output_list()
        output_list_data.append(output_list)

        for i in range(1, 58 + 1):
            output_list.str = output_list.str + "   "
        output_list.pay_amt = to_decimal(t_credit)
        output_list.pay_famt = to_decimal(t_famt)

        if not long_digit:
            output_list.str = output_list.str + "Sub-Total " +\
                to_string(t_credit, "->,>>>,>>>,>>9.99") +\
                fill(" ", 78) +\
                to_string(t_famt, "->>,>>>,>>>,>>9.99")
        else:
            output_list.str = output_list.str + "Sub-Total " +\
                to_string(t_credit, " ->>>,>>>,>>>,>>9") +\
                fill(" ", 78) +\
                to_string(t_famt, "  ->>>,>>>,>>>,>>9")
        output_list = Output_list()
        output_list_data.append(output_list)

        output_list = Output_list()
        output_list_data.append(output_list)

        for i in range(1, 56 + 1):
            output_list.str = output_list.str + " "
        output_list.pay_amt = to_decimal(tot_credit)
        output_list.pay_famt = to_decimal(tot_famt)

        if not long_digit:
            output_list.str = output_list.str + "Grand TOTAL " +\
                to_string(tot_credit, "->,>>>,>>>,>>9.99") +\
                fill(" ", 78) + \
                to_string(tot_famt, "->>,>>>,>>>,>>9.99")
        else:
            output_list.str = output_list.str + "Grand TOTAL " +\
                to_string(tot_credit, " ->>>,>>>,>>>,>>9") +\
                fill(" ", 78) + \
                to_string(tot_famt, "  ->>>,>>>,>>>,>>9")
        create_tot_payment()

    def create_list3b():

        nonlocal r_no, s_list_data, t_list_data, t_ar_paylist_data, long_digit, htparam, guest, debitor, artikel, bill, bediener, waehrung
        nonlocal comment, cledger, ccard, last_sort, from_date, to_date, from_art, to_art, mi_payment, mi_transfer, show_inv, bill_name, bill_nr
        nonlocal bguest, bdebitor

        nonlocal s_list, t_list, output_list, t_ar_paylist, bguest, bdebitor, tbuff, bq
        nonlocal s_list_data, t_list_data, output_list_data, t_ar_paylist_data

        artnr: int = 0
        i: int = 0
        curr_gastnr: int = 0
        t_credit: Decimal = to_decimal("0.0")
        tot_credit: Decimal = to_decimal("0.0")
        t_famt: Decimal = to_decimal("0.0")
        tot_famt: Decimal = to_decimal("0.0")
        tot_saldo: Decimal = to_decimal("0.0")
        tot_foreign: Decimal = to_decimal("0.0")
        receiver: string = ""
        do_it: bool = False
        temp_name: string = ""
        temp_vorname1: string = ""
        temp_anredefirma: string = ""
        temp_anrede1: string = ""
        debt = None
        art = None
        t_guest = None
        tstr: string = ""
        Debt = create_buffer("Debt", Debitor)
        Art = create_buffer("Art", Artikel)
        T_guest = create_buffer("T_guest", Guest)

        debitor_obj_list = {}
        debitor = Debitor()
        debt = Debitor()
        artikel = Artikel()
        art = Artikel()
        guest = Guest()
        for debitor.gastnr, debitor.saldo, debitor.zahlkonto, debitor.betriebsnr, debitor.counter, debitor.rechnr, debitor.debref, debitor.rgdatum, debitor.gastnrmember, debitor.bediener_nr, debitor.vesrcod, debitor.vesrdep, debitor.betrieb_gastmem, debitor._recid, debt.gastnr, debt.saldo, debt.zahlkonto, debt.betriebsnr, debt.counter, debt.rechnr, debt.debref, debt.rgdatum, debt.gastnrmember, debt.bediener_nr, debt.vesrcod, debt.vesrdep, debt.betrieb_gastmem, debt._recid, artikel.artnr, artikel.bezeich, artikel.artart, artikel._recid, art.artnr, art.bezeich, art.artart, art._recid, guest.name, guest.vorname1, guest.anredefirma, guest.anrede1, guest._recid in db_session.query(Debitor.gastnr, Debitor.saldo, Debitor.zahlkonto, Debitor.betriebsnr, Debitor.counter, Debitor.rechnr, Debitor.debref, Debitor.rgdatum, Debitor.gastnrmember, Debitor.bediener_nr, Debitor.vesrcod, Debitor.vesrdep, Debitor.betrieb_gastmem, Debitor._recid, Debt.gastnr, Debt.saldo, Debt.zahlkonto, Debt.betriebsnr, Debt.counter, Debt.rechnr, Debt.debref, Debt.rgdatum, Debt.gastnrmember, Debt.bediener_nr, Debt.vesrcod, Debt.vesrdep, Debt.betrieb_gastmem, Debt._recid, Artikel.artnr, Artikel.bezeich, Artikel.artart, Artikel._recid, Art.artnr, Art.bezeich, Art.artart, Art._recid, Guest.name, Guest.vorname1, Guest.anredefirma, Guest.anrede1, Guest._recid).join(Debt, (Debt.counter == Debitor.counter) & (Debt.zahlkonto == 0)).join(Artikel, (Artikel.artnr == Debitor.artnr) & (Artikel.departement == 0) & (Artikel.artart == 7)).join(Art, (Art.artnr == Debitor.zahlkonto) & (Art.departement == 0)).join(Guest, (Guest.gastnr == Debitor.gastnr)).filter(
                (Debitor.rgdatum >= from_date) & (Debitor.rgdatum <= to_date) & (Debitor.zahlkonto > 0) & (Debitor.artnr >= from_art) & (Debitor.artnr <= to_art) & (Debitor.counter > 0) & (Debitor.opart > 0)).order_by(Artikel.artnr, Debt.rgdatum, Debitor.name, Debitor.zahlkonto, Debitor.rechnr).all():
            if debitor_obj_list.get(debitor._recid):
                continue
            else:
                debitor_obj_list[debitor._recid] = True

            do_it = True

            if mi_payment:

                if artikel.artart == 2 and art.artart != 4 and art.artart != 7:
                    do_it = False

                elif artikel.artart == 7 and art.artart != 4:
                    do_it = False

            elif mi_transfer:

                if artikel.artart == 2 and (art.artart == 4 or art.artart == 7):
                    do_it = False

                elif artikel.artart == 7 and art.artart == 4:
                    do_it = False

            if do_it and (bill_name != "") and (substring(bill_name, 0, 1) != ("*").lower()):

                if not matches(guest.name, r"*" + bill_name + r"*"):
                    do_it = False

            if do_it and (bill_name != "") and (substring(bill_name, 0, 1) == ("*").lower()):

                if not matches(guest.name, bill_name):
                    do_it = False

            if do_it:

                if curr_gastnr == 0:
                    curr_gastnr = debitor.gastnr

                if curr_gastnr != debitor.gastnr:
                    curr_gastnr = debitor.gastnr
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    for i in range(1, 58 + 1):
                        output_list.str = output_list.str + "   "
                    output_list.pay_amt = to_decimal(tot_saldo)
                    output_list.pay_famt = to_decimal(tot_foreign)

                    if not long_digit:
                        output_list.str = output_list.str + "T O T A L " +\
                            to_string(tot_saldo, "->,>>>,>>>,>>9.99") +\
                            fill(" ", 78) +\
                            to_string(tot_foreign, " ->>,>>>,>>>,>>9.99")
                    else:
                        output_list.str = output_list.str + "T O T A L " +\
                            to_string(tot_saldo, " ->>>,>>>,>>>,>>9") +\
                            fill(" ", 78) +\
                            to_string(tot_foreign, "   ->>>,>>>,>>>,>>9")
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    tot_saldo = to_decimal("0")
                    tot_foreign = to_decimal("0")

                if artnr != artikel.artnr:
                    t_list = T_list()
                    t_list_data.append(t_list)

                    t_list.artnr = artikel.artnr
                    t_list.bezeich = artikel.bezeich

                    if artnr != 0:
                        output_list = Output_list()
                        output_list_data.append(output_list)

                        for i in range(1, 58 + 1):
                            output_list.str = output_list.str + "   "
                        output_list.pay_amt = to_decimal(t_credit)
                        output_list.pay_famt = to_decimal(t_famt)

                        if not long_digit:
                            output_list.str = output_list.str + "Sub-Total " +\
                                to_string(t_credit, "->,>>>,>>>,>>9.99") +\
                                fill(" ", 78) +\
                                to_string(t_famt, "->>,>>>,>>>,>>9.99")
                        else:
                            output_list.str = output_list.str + "Sub-Total " +\
                                to_string(t_credit, " ->>>,>>>,>>>,>>9") +\
                                fill(" ", 78) +\
                                to_string(t_famt, "  ->>>,>>>,>>>,>>9")
                        output_list = Output_list()
                        output_list_data.append(output_list)

                        t_credit = to_decimal("0")
                        t_famt = to_decimal("0")
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    for i in range(1, 19 + 1):
                        output_list.str = output_list.str + " "
                    output_list.str = output_list.str +\
                        to_string(artikel.artnr, ">>>>9") + " - " +\
                        to_string(artikel.bezeich, "x(34)")
                    artnr = artikel.artnr
                t_list.betrag = to_decimal(
                    t_list.betrag) - to_decimal(debitor.saldo)

                if guest.name != None:
                    temp_name = guest.name

                else:
                    temp_name = ""

                if guest.vorname1 != None:
                    temp_vorname1 = guest.vorname1

                else:
                    temp_vorname1 = ""

                if guest.anredefirma != None:
                    temp_anredefirma = guest.anredefirma

                else:
                    temp_anredefirma = ""

                if guest.anrede1 != None:
                    temp_anrede1 = guest.anrede1

                else:
                    temp_anrede1 = ""
                receiver = substring(f"{temp_name}, {temp_vorname1} {temp_anredefirma}{temp_anrede1}", 0, 32)
                output_list = Output_list()
                output_list_data.append(output_list)

                output_list.bill_art = artikel.artnr
                output_list.debt_counter = debitor.counter
                output_list.famt = to_string(debt.vesrdep, "->>,>>>,>>>,>>9.99")

                if show_inv:

                    bill = get_cache(Bill, {"rechnr": [(eq, debitor.rechnr)]})

                    if bill:
                        output_list.inv_no = to_string(
                            bill.rechnr2, ">>>>>>>>>")

                        if bill.billref != 0:
                            output_list.soa_inv = "INV" + \
                                to_string(bill.billref, "9999999")
                    else:

                        bdebitor = get_cache(
                            Debitor, {"rechnr": [(eq, debitor.rechnr)], "debref": [(gt, 0)]})

                        if bdebitor:
                            output_list.soa_inv = "INV" + \
                                to_string(debitor.debref, "9999999")

                output_list.pay_amt = to_decimal(debitor.saldo)
                output_list.pay_famt = to_decimal(debitor.vesrdep)

                if not long_digit:
                    output_list.str = to_string(debt.rgdatum) +\
                        to_string(debitor.rechnr, ">>>,>>>,>>9") +\
                        to_string(receiver, "x(32)") +\
                        to_string(debt.saldo, "->,>>>,>>>,>>9.99") +\
                        to_string(debitor.saldo, "->,>>>,>>>,>>9.99") +\
                        to_string(art.bezeich, "x(34)") +\
                        to_string(debitor.rgdatum)
                else:
                    output_list.str = to_string(debt.rgdatum) +\
                        to_string(debitor.rechnr, ">>>,>>>,>>9") +\
                        to_string(receiver, "x(32)") +\
                        to_string(debt.saldo, " ->>>,>>>,>>>,>>9") +\
                        to_string(debitor.saldo, " ->>>,>>>,>>>,>>9") +\
                        to_string(art.bezeich, "x(34)") +\
                        to_string(debitor.rgdatum)
                output_list.bill_num = debitor.rechnr
                output_list.art_bezeich = artikel.bezeich
                output_list.tbetrag = to_decimal(
                    output_list.tbetrag) - to_decimal(debitor.saldo)

                bguest = get_cache(
                    Guest, {"gastnr": [(eq, debitor.gastnrmember)]})

                if bguest:
                    output_list.gastname = substring(f"{bguest.name}, {bguest.vorname1}{bguest.anredefirma} {bguest.anrede1}", 0, 32)

                bediener = get_cache(
                    Bediener, {"nr": [(eq, debitor.bediener_nr)]})

                if bediener:
                    output_list.str = output_list.str + \
                        to_string(bediener.userinit, "x(3)")
                else:
                    output_list.str = output_list.str + "   "
                output_list.str = output_list.str + \
                    to_string(debitor.vesrcod, "x(34)")
                output_list.str = output_list.str + to_string(" ", "x(22)")

                t_guest = get_cache(
                    Guest, {"gastnr": [(eq, debt.gastnrmember)]})

                if t_guest:
                    tstr = substring(f"{t_guest.name}, {t_guest.vorname1}{t_guest.anrede1}", 0, 34)
                else:
                    tstr = " "
                output_list.str = output_list.str + to_string(tstr, "x(50)")
                output_list.str = output_list.str + \
                    to_string(debitor.vesrdep, "->,>>>,>>>,>>9.99")
                output_list.str = output_list.str + \
                    to_string(debitor.zahlkonto, ">>>>9")
                output_list.str = output_list.str + \
                    to_string(debitor.vesrdep, "->,>>>,>>>,>>9.99")
                output_list.str = output_list.str + \
                    to_string(artikel.bezeich, "x(40)")

                t_credit = to_decimal(t_credit) + to_decimal(debitor.saldo)
                t_famt = to_decimal(t_famt) + to_decimal(debitor.vesrdep)
                tot_credit = to_decimal(tot_credit) + to_decimal(debitor.saldo)
                tot_saldo = to_decimal(tot_saldo) + to_decimal(debitor.saldo)
                tot_foreign = to_decimal(
                    tot_foreign) + to_decimal(debitor.vesrdep)
                tot_famt = to_decimal(tot_famt) + to_decimal(debitor.vesrdep)

                s_list = query(s_list_data, filters=(
                    lambda s_list: s_list.artnr == art.artnr), first=True)

                if not s_list:
                    s_list = S_list()
                    s_list_data.append(s_list)

                    s_list.artnr = art.artnr
                    s_list.bezeich = art.bezeich
                s_list.betrag = to_decimal(
                    s_list.betrag) + to_decimal(debitor.saldo)
        output_list = Output_list()
        output_list_data.append(output_list)

        for i in range(1, 58 + 1):
            output_list.str = output_list.str + "   "
        output_list.pay_amt = to_decimal(tot_saldo)
        output_list.pay_famt = to_decimal(tot_foreign)

        if not long_digit:
            output_list.str = output_list.str + "T O T A L " +\
                to_string(tot_saldo, "->,>>>,>>>,>>9.99") +\
                fill(" ", 78) +\
                to_string(tot_foreign, " ->>,>>>,>>>,>>9.99")
        else:
            output_list.str = output_list.str + "T O T A L " +\
                to_string(tot_saldo, " ->>>,>>>,>>>,>>9") +\
                fill(" ", 78) +\
                to_string(tot_foreign, "   ->>>,>>>,>>>,>>9")
        output_list = Output_list()
        output_list_data.append(output_list)

        output_list = Output_list()
        output_list_data.append(output_list)

        for i in range(1, 58 + 1):
            output_list.str = output_list.str + "   "
        output_list.pay_amt = to_decimal(t_credit)
        output_list.pay_famt = to_decimal(t_famt)

        if not long_digit:
            output_list.str = output_list.str + "Sub-Total " +\
                to_string(t_credit, "->,>>>,>>>,>>9.99") +\
                fill(" ", 78) +\
                to_string(t_famt, "->>,>>>,>>>,>>9.99")
        else:
            output_list.str = output_list.str + "Sub-Total " +\
                to_string(t_credit, " ->>>,>>>,>>>,>>9") +\
                fill(" ", 78) +\
                to_string(t_famt, "  ->>>,>>>,>>>,>>9")
        output_list = Output_list()
        output_list_data.append(output_list)

        output_list = Output_list()
        output_list_data.append(output_list)

        for i in range(1, 56 + 1):
            output_list.str = output_list.str + " "
        output_list.pay_amt = to_decimal(tot_credit)
        output_list.pay_famt = to_decimal(tot_famt)

        if not long_digit:
            output_list.str = output_list.str + "Grand TOTAL " +\
                to_string(tot_credit, "->,>>>,>>>,>>9.99") +\
                fill(" ", 78) + \
                to_string(tot_famt, "->>,>>>,>>>,>>9.99")
        else:
            output_list.str = output_list.str + "Grand TOTAL " +\
                to_string(tot_credit, " ->>>,>>>,>>>,>>9") +\
                fill(" ", 78) + \
                to_string(tot_famt, "  ->>>,>>>,>>>,>>9")
        create_tot_payment()

    def create_list3c():

        nonlocal r_no, s_list_data, t_list_data, t_ar_paylist_data, long_digit, htparam, guest, debitor, artikel, bill, bediener, waehrung
        nonlocal comment, cledger, ccard, last_sort, from_date, to_date, from_art, to_art, mi_payment, mi_transfer, show_inv, bill_name, bill_nr
        nonlocal bguest, bdebitor

        nonlocal s_list, t_list, output_list, t_ar_paylist, bguest, bdebitor, tbuff, bq
        nonlocal s_list_data, t_list_data, output_list_data, t_ar_paylist_data

        artnr: int = 0
        i: int = 0
        curr_gastnr: int = 0
        t_credit: Decimal = to_decimal("0.0")
        tot_credit: Decimal = to_decimal("0.0")
        t_famt: Decimal = to_decimal("0.0")
        tot_famt: Decimal = to_decimal("0.0")
        tot_saldo: Decimal = to_decimal("0.0")
        tot_foreign: Decimal = to_decimal("0.0")
        receiver: string = ""
        do_it: bool = False
        temp_name: string = ""
        temp_vorname1: string = ""
        temp_anredefirma: string = ""
        temp_anrede1: string = ""
        debt = None
        art = None
        t_guest = None
        tstr: string = ""
        Debt = create_buffer("Debt", Debitor)
        Art = create_buffer("Art", Artikel)
        T_guest = create_buffer("T_guest", Guest)

        debitor_obj_list = {}
        debitor = Debitor()
        debt = Debitor()
        artikel = Artikel()
        art = Artikel()
        guest = Guest()
        for debitor.gastnr, debitor.saldo, debitor.zahlkonto, debitor.betriebsnr, debitor.counter, debitor.rechnr, debitor.debref, debitor.rgdatum, debitor.gastnrmember, debitor.bediener_nr, debitor.vesrcod, debitor.vesrdep, debitor.betrieb_gastmem, debitor._recid, debt.gastnr, debt.saldo, debt.zahlkonto, debt.betriebsnr, debt.counter, debt.rechnr, debt.debref, debt.rgdatum, debt.gastnrmember, debt.bediener_nr, debt.vesrcod, debt.vesrdep, debt.betrieb_gastmem, debt._recid, artikel.artnr, artikel.bezeich, artikel.artart, artikel._recid, art.artnr, art.bezeich, art.artart, art._recid, guest.name, guest.vorname1, guest.anredefirma, guest.anrede1, guest._recid in db_session.query(Debitor.gastnr, Debitor.saldo, Debitor.zahlkonto, Debitor.betriebsnr, Debitor.counter, Debitor.rechnr, Debitor.debref, Debitor.rgdatum, Debitor.gastnrmember, Debitor.bediener_nr, Debitor.vesrcod, Debitor.vesrdep, Debitor.betrieb_gastmem, Debitor._recid, Debt.gastnr, Debt.saldo, Debt.zahlkonto, Debt.betriebsnr, Debt.counter, Debt.rechnr, Debt.debref, Debt.rgdatum, Debt.gastnrmember, Debt.bediener_nr, Debt.vesrcod, Debt.vesrdep, Debt.betrieb_gastmem, Debt._recid, Artikel.artnr, Artikel.bezeich, Artikel.artart, Artikel._recid, Art.artnr, Art.bezeich, Art.artart, Art._recid, Guest.name, Guest.vorname1, Guest.anredefirma, Guest.anrede1, Guest._recid).join(Debt, (Debt.counter == Debitor.counter) & (Debt.zahlkonto == 0)).join(Artikel, (Artikel.artnr == Debitor.artnr) & (Artikel.departement == 0) & (Artikel.artart == 7)).join(Art, (Art.artnr == Debitor.zahlkonto) & (Art.departement == 0)).join(Guest, (Guest.gastnr == Debitor.gastnr)).filter(
                (Debitor.rgdatum >= from_date) & (Debitor.rgdatum <= to_date) & (Debitor.zahlkonto > 0) & (Debitor.artnr >= from_art) & (Debitor.artnr <= to_art) & (Debitor.counter > 0) & (Debitor.opart > 0)).order_by(Artikel.artnr, Debitor.rechnr, Debitor.name, Debitor.rgdatum, Debitor.zahlkonto).all():
            if debitor_obj_list.get(debitor._recid):
                continue
            else:
                debitor_obj_list[debitor._recid] = True

            do_it = True

            if mi_payment:

                if artikel.artart == 2 and art.artart != 4 and art.artart != 7:
                    do_it = False

                elif artikel.artart == 7 and art.artart != 4:
                    do_it = False

            elif mi_transfer:

                if artikel.artart == 2 and (art.artart == 4 or art.artart == 7):
                    do_it = False

                elif artikel.artart == 7 and art.artart == 4:
                    do_it = False

            if do_it and (bill_name != "") and (substring(bill_name, 0, 1) != ("*").lower()):

                if not matches(guest.name, r"*" + bill_name + r"*"):
                    do_it = False

            if do_it and (bill_name != "") and (substring(bill_name, 0, 1) == ("*").lower()):

                if not matches(guest.name, bill_name):
                    do_it = False

            if do_it:

                if curr_gastnr == 0:
                    curr_gastnr = debitor.gastnr

                if curr_gastnr != debitor.gastnr:
                    curr_gastnr = debitor.gastnr
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    for i in range(1, 58 + 1):
                        output_list.str = output_list.str + "   "
                    output_list.pay_amt = to_decimal(tot_saldo)
                    output_list.pay_famt = to_decimal(tot_foreign)

                    if not long_digit:
                        output_list.str = output_list.str + "T O T A L " +\
                            to_string(tot_saldo, "->,>>>,>>>,>>9.99") +\
                            fill(" ", 78) +\
                            to_string(tot_foreign, " ->>,>>>,>>>,>>9.99")
                    else:
                        output_list.str = output_list.str + "T O T A L " +\
                            to_string(tot_saldo, " ->>>,>>>,>>>,>>9") +\
                            fill(" ", 78) +\
                            to_string(tot_foreign, "   ->>>,>>>,>>>,>>9")
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    tot_saldo = to_decimal("0")
                    tot_foreign = to_decimal("0")

                if artnr != artikel.artnr:
                    t_list = T_list()
                    t_list_data.append(t_list)

                    t_list.artnr = artikel.artnr
                    t_list.bezeich = artikel.bezeich

                    if artnr != 0:
                        output_list = Output_list()
                        output_list_data.append(output_list)

                        for i in range(1, 58 + 1):
                            output_list.str = output_list.str + "   "
                        output_list.pay_amt = to_decimal(t_credit)
                        output_list.pay_famt = to_decimal(t_famt)

                        if not long_digit:
                            output_list.str = output_list.str + "Sub-Total " +\
                                to_string(t_credit, "->,>>>,>>>,>>9.99") +\
                                fill(" ", 78) +\
                                to_string(t_famt, "->>,>>>,>>>,>>9.99")
                        else:
                            output_list.str = output_list.str + "Sub-Total " +\
                                to_string(t_credit, " ->>>,>>>,>>>,>>9") +\
                                fill(" ", 78) +\
                                to_string(t_famt, "  ->>>,>>>,>>>,>>9")
                        output_list = Output_list()
                        output_list_data.append(output_list)

                        t_credit = to_decimal("0")
                        t_famt = to_decimal("0")
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    for i in range(1, 19 + 1):
                        output_list.str = output_list.str + " "
                    output_list.str = output_list.str +\
                        to_string(artikel.artnr, ">>>>9") + " - " +\
                        to_string(artikel.bezeich, "x(34)")
                    artnr = artikel.artnr
                t_list.betrag = to_decimal(
                    t_list.betrag) - to_decimal(debitor.saldo)

                if guest.name != None:
                    temp_name = guest.name

                else:
                    temp_name = ""

                if guest.vorname1 != None:
                    temp_vorname1 = guest.vorname1

                else:
                    temp_vorname1 = ""

                if guest.anredefirma != None:
                    temp_anredefirma = guest.anredefirma

                else:
                    temp_anredefirma = ""

                if guest.anrede1 != None:
                    temp_anrede1 = guest.anrede1

                else:
                    temp_anrede1 = ""
                receiver = substring(f"{temp_name}, {temp_vorname1} {temp_anredefirma}{temp_anrede1}", 0, 32)
                output_list = Output_list()
                output_list_data.append(output_list)

                output_list.bill_art = artikel.artnr
                output_list.debt_counter = debitor.counter
                output_list.famt = to_string(
                    debt.vesrdep, "->>,>>>,>>>,>>9.99")

                if show_inv:

                    bill = get_cache(Bill, {"rechnr": [(eq, debitor.rechnr)]})

                    if bill:
                        output_list.inv_no = to_string(
                            bill.rechnr2, ">>>>>>>>>")

                        if bill.billref != 0:
                            output_list.soa_inv = "INV" + \
                                to_string(bill.billref, "9999999")
                    else:

                        bdebitor = get_cache(
                            Debitor, {"rechnr": [(eq, debitor.rechnr)], "debref": [(gt, 0)]})

                        if bdebitor:
                            output_list.soa_inv = "INV" + \
                                to_string(debitor.debref, "9999999")

                output_list.pay_amt = to_decimal(debitor.saldo)
                output_list.pay_famt = to_decimal(debitor.vesrdep)

                if not long_digit:
                    output_list.str = to_string(debt.rgdatum) +\
                        to_string(debitor.rechnr, ">>>,>>>,>>9") +\
                        to_string(receiver, "x(32)") +\
                        to_string(debt.saldo, "->,>>>,>>>,>>9.99") +\
                        to_string(debitor.saldo, "->,>>>,>>>,>>9.99") +\
                        to_string(art.bezeich, "x(34)") +\
                        to_string(debitor.rgdatum)
                else:
                    output_list.str = to_string(debt.rgdatum) +\
                        to_string(debitor.rechnr, ">>>,>>>,>>9") +\
                        to_string(receiver, "x(32)") +\
                        to_string(debt.saldo, " ->>>,>>>,>>>,>>9") +\
                        to_string(debitor.saldo, " ->>>,>>>,>>>,>>9") +\
                        to_string(art.bezeich, "x(34)") +\
                        to_string(debitor.rgdatum)
                output_list.bill_num = debitor.rechnr
                output_list.art_bezeich = artikel.bezeich
                output_list.tbetrag = to_decimal(
                    output_list.tbetrag) - to_decimal(debitor.saldo)

                bguest = get_cache(
                    Guest, {"gastnr": [(eq, debitor.gastnrmember)]})

                if bguest:
                    output_list.gastname = substring(f"{bguest.name}, {bguest.vorname1}{bguest.anredefirma} {bguest.anrede1}", 0, 32)

                bediener = get_cache(
                    Bediener, {"nr": [(eq, debitor.bediener_nr)]})

                if bediener:
                    output_list.str = output_list.str + \
                        to_string(bediener.userinit, "x(3)")
                else:
                    output_list.str = output_list.str + "   "
                output_list.str = output_list.str + \
                    to_string(debitor.vesrcod, "x(34)")
                output_list.str = output_list.str + to_string(" ", "x(22)")

                t_guest = get_cache(
                    Guest, {"gastnr": [(eq, debt.gastnrmember)]})

                if t_guest:
                    tstr = substring(f"{t_guest.name}, {t_guest.vorname1}{t_guest.anrede1}", 0, 34)
                else:
                    tstr = " "
                output_list.str = output_list.str + to_string(tstr, "x(50)")
                output_list.str = output_list.str + \
                    to_string(debitor.vesrdep, "->,>>>,>>>,>>9.99")
                output_list.str = output_list.str + \
                    to_string(debitor.zahlkonto, ">>>>9")
                output_list.str = output_list.str + \
                    to_string(debitor.vesrdep, "->,>>>,>>>,>>9.99")
                output_list.str = output_list.str + \
                    to_string(artikel.bezeich, "x(40)")

                t_credit = to_decimal(t_credit) + to_decimal(debitor.saldo)
                t_famt = to_decimal(t_famt) + to_decimal(debitor.vesrdep)
                tot_credit = to_decimal(tot_credit) + to_decimal(debitor.saldo)
                tot_saldo = to_decimal(tot_saldo) + to_decimal(debitor.saldo)
                tot_foreign = to_decimal(
                    tot_foreign) + to_decimal(debitor.vesrdep)
                tot_famt = to_decimal(tot_famt) + to_decimal(debitor.vesrdep)

                s_list = query(s_list_data, filters=(
                    lambda s_list: s_list.artnr == art.artnr), first=True)

                if not s_list:
                    s_list = S_list()
                    s_list_data.append(s_list)

                    s_list.artnr = art.artnr
                    s_list.bezeich = art.bezeich
                s_list.betrag = to_decimal(
                    s_list.betrag) + to_decimal(debitor.saldo)
        output_list = Output_list()
        output_list_data.append(output_list)

        for i in range(1, 58 + 1):
            output_list.str = output_list.str + "   "
        output_list.pay_amt = to_decimal(tot_saldo)
        output_list.pay_famt = to_decimal(tot_foreign)

        if not long_digit:
            output_list.str = output_list.str + "T O T A L " +\
                to_string(tot_saldo, "->,>>>,>>>,>>9.99") +\
                fill(" ", 78) +\
                to_string(tot_foreign, " ->>,>>>,>>>,>>9.99")
        else:
            output_list.str = output_list.str + "T O T A L " +\
                to_string(tot_saldo, " ->>>,>>>,>>>,>>9") +\
                fill(" ", 78) +\
                to_string(tot_foreign, "   ->>>,>>>,>>>,>>9")
        output_list = Output_list()
        output_list_data.append(output_list)

        output_list = Output_list()
        output_list_data.append(output_list)

        for i in range(1, 58 + 1):
            output_list.str = output_list.str + "   "
        output_list.pay_amt = to_decimal(t_credit)
        output_list.pay_famt = to_decimal(t_famt)

        if not long_digit:
            output_list.str = output_list.str + "Sub-Total " +\
                to_string(t_credit, "->,>>>,>>>,>>9.99") +\
                fill(" ", 78) +\
                to_string(t_famt, "->>,>>>,>>>,>>9.99")
        else:
            output_list.str = output_list.str + "Sub-Total " +\
                to_string(t_credit, " ->>>,>>>,>>>,>>9") +\
                fill(" ", 78) +\
                to_string(t_famt, "  ->>>,>>>,>>>,>>9")
        output_list = Output_list()
        output_list_data.append(output_list)

        output_list = Output_list()
        output_list_data.append(output_list)

        for i in range(1, 56 + 1):
            output_list.str = output_list.str + " "
        output_list.pay_amt = to_decimal(tot_credit)
        output_list.pay_famt = to_decimal(tot_famt)

        if not long_digit:
            output_list.str = output_list.str + "Grand TOTAL " +\
                to_string(tot_credit, "->,>>>,>>>,>>9.99") +\
                fill(" ", 78) + \
                to_string(tot_famt, "->>,>>>,>>>,>>9.99")
        else:
            output_list.str = output_list.str + "Grand TOTAL " +\
                to_string(tot_credit, " ->>>,>>>,>>>,>>9") +\
                fill(" ", 78) + \
                to_string(tot_famt, "  ->>>,>>>,>>>,>>9")
        create_tot_payment()

    def create_list3d():

        nonlocal r_no, s_list_data, t_list_data, t_ar_paylist_data, long_digit, htparam, guest, debitor, artikel, bill, bediener, waehrung
        nonlocal comment, cledger, ccard, last_sort, from_date, to_date, from_art, to_art, mi_payment, mi_transfer, show_inv, bill_name, bill_nr
        nonlocal bguest, bdebitor

        nonlocal s_list, t_list, output_list, t_ar_paylist, bguest, bdebitor, tbuff, bq
        nonlocal s_list_data, t_list_data, output_list_data, t_ar_paylist_data

        artnr: int = 0
        i: int = 0
        curr_gastnr: int = 0
        t_credit: Decimal = to_decimal("0.0")
        tot_credit: Decimal = to_decimal("0.0")
        t_famt: Decimal = to_decimal("0.0")
        tot_famt: Decimal = to_decimal("0.0")
        tot_saldo: Decimal = to_decimal("0.0")
        tot_foreign: Decimal = to_decimal("0.0")
        receiver: string = ""
        do_it: bool = False
        temp_name: string = ""
        temp_vorname1: string = ""
        temp_anredefirma: string = ""
        temp_anrede1: string = ""
        debt = None
        art = None
        t_guest = None
        tstr: string = ""
        Debt = create_buffer("Debt", Debitor)
        Art = create_buffer("Art", Artikel)
        T_guest = create_buffer("T_guest", Guest)

        debitor_obj_list = {}
        debitor = Debitor()
        debt = Debitor()
        artikel = Artikel()
        art = Artikel()
        guest = Guest()
        for debitor.gastnr, debitor.saldo, debitor.zahlkonto, debitor.betriebsnr, debitor.counter, debitor.rechnr, debitor.debref, debitor.rgdatum, debitor.gastnrmember, debitor.bediener_nr, debitor.vesrcod, debitor.vesrdep, debitor.betrieb_gastmem, debitor._recid, debt.gastnr, debt.saldo, debt.zahlkonto, debt.betriebsnr, debt.counter, debt.rechnr, debt.debref, debt.rgdatum, debt.gastnrmember, debt.bediener_nr, debt.vesrcod, debt.vesrdep, debt.betrieb_gastmem, debt._recid, artikel.artnr, artikel.bezeich, artikel.artart, artikel._recid, art.artnr, art.bezeich, art.artart, art._recid, guest.name, guest.vorname1, guest.anredefirma, guest.anrede1, guest._recid in db_session.query(Debitor.gastnr, Debitor.saldo, Debitor.zahlkonto, Debitor.betriebsnr, Debitor.counter, Debitor.rechnr, Debitor.debref, Debitor.rgdatum, Debitor.gastnrmember, Debitor.bediener_nr, Debitor.vesrcod, Debitor.vesrdep, Debitor.betrieb_gastmem, Debitor._recid, Debt.gastnr, Debt.saldo, Debt.zahlkonto, Debt.betriebsnr, Debt.counter, Debt.rechnr, Debt.debref, Debt.rgdatum, Debt.gastnrmember, Debt.bediener_nr, Debt.vesrcod, Debt.vesrdep, Debt.betrieb_gastmem, Debt._recid, Artikel.artnr, Artikel.bezeich, Artikel.artart, Artikel._recid, Art.artnr, Art.bezeich, Art.artart, Art._recid, Guest.name, Guest.vorname1, Guest.anredefirma, Guest.anrede1, Guest._recid).join(Debt, (Debt.counter == Debitor.counter) & (Debt.zahlkonto == 0)).join(Artikel, (Artikel.artnr == Debitor.artnr) & (Artikel.departement == 0) & (Artikel.artart == 7)).join(Art, (Art.artnr == Debitor.zahlkonto) & (Art.departement == 0)).join(Guest, (Guest.gastnr == Debitor.gastnr)).filter(
                (Debitor.rgdatum >= from_date) & (Debitor.rgdatum <= to_date) & (Debitor.zahlkonto > 0) & (Debitor.artnr >= from_art) & (Debitor.artnr <= to_art) & (Debitor.counter > 0) & (Debitor.opart > 0)).order_by(Artikel.artnr, Debitor.vesrcod, Debitor.name, Debitor.rgdatum, Debitor.zahlkonto, Debitor.rechnr).all():
            if debitor_obj_list.get(debitor._recid):
                continue
            else:
                debitor_obj_list[debitor._recid] = True

            do_it = True

            if mi_payment:

                if artikel.artart == 2 and art.artart != 4 and art.artart != 7:
                    do_it = False

                elif artikel.artart == 7 and art.artart != 4:
                    do_it = False

            elif mi_transfer:

                if artikel.artart == 2 and (art.artart == 4 or art.artart == 7):
                    do_it = False

                elif artikel.artart == 7 and art.artart == 4:
                    do_it = False

            if do_it and (bill_name != "") and (substring(bill_name, 0, 1) != ("*").lower()):

                if not matches(guest.name, r"*" + bill_name + r"*"):
                    do_it = False

            if do_it and (bill_name != "") and (substring(bill_name, 0, 1) == ("*").lower()):

                if not matches(guest.name, bill_name):
                    do_it = False

            if do_it:

                if curr_gastnr == 0:
                    curr_gastnr = debitor.gastnr

                if curr_gastnr != debitor.gastnr:
                    curr_gastnr = debitor.gastnr
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    for i in range(1, 58 + 1):
                        output_list.str = output_list.str + "   "
                    output_list.pay_amt = to_decimal(tot_saldo)
                    output_list.pay_famt = to_decimal(tot_foreign)

                    if not long_digit:
                        output_list.str = output_list.str + "T O T A L " +\
                            to_string(tot_saldo, "->,>>>,>>>,>>9.99") +\
                            fill(" ", 78) +\
                            to_string(tot_foreign, " ->>,>>>,>>>,>>9.99")
                    else:
                        output_list.str = output_list.str + "T O T A L " +\
                            to_string(tot_saldo, " ->>>,>>>,>>>,>>9") +\
                            fill(" ", 78) +\
                            to_string(tot_foreign, "   ->>>,>>>,>>>,>>9")
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    tot_saldo = to_decimal("0")
                    tot_foreign = to_decimal("0")

                if artnr != artikel.artnr:
                    t_list = T_list()
                    t_list_data.append(t_list)

                    t_list.artnr = artikel.artnr
                    t_list.bezeich = artikel.bezeich

                    if artnr != 0:
                        output_list = Output_list()
                        output_list_data.append(output_list)

                        for i in range(1, 58 + 1):
                            output_list.str = output_list.str + "   "
                        output_list.pay_amt = to_decimal(tot_saldo)
                        output_list.pay_famt = to_decimal(t_famt)

                        if not long_digit:
                            output_list.str = output_list.str + "Sub-Total " +\
                                to_string(t_credit, "->,>>>,>>>,>>9.99") +\
                                fill(" ", 78) +\
                                to_string(t_famt, "->>,>>>,>>>,>>9.99")
                        else:
                            output_list.str = output_list.str + "Sub-Total " +\
                                to_string(t_credit, " ->>>,>>>,>>>,>>9") +\
                                fill(" ", 78) +\
                                to_string(t_famt, "  ->>>,>>>,>>>,>>9")
                        output_list = Output_list()
                        output_list_data.append(output_list)

                        t_credit = to_decimal("0")
                        t_famt = to_decimal("0")
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    for i in range(1, 19 + 1):
                        output_list.str = output_list.str + " "
                    output_list.str = output_list.str +\
                        to_string(artikel.artnr, ">>>>9") + " - " +\
                        to_string(artikel.bezeich, "x(34)")
                    artnr = artikel.artnr
                t_list.betrag = to_decimal(
                    t_list.betrag) - to_decimal(debitor.saldo)

                if guest.name != None:
                    temp_name = guest.name

                else:
                    temp_name = ""

                if guest.vorname1 != None:
                    temp_vorname1 = guest.vorname1

                else:
                    temp_vorname1 = ""

                if guest.anredefirma != None:
                    temp_anredefirma = guest.anredefirma

                else:
                    temp_anredefirma = ""

                if guest.anrede1 != None:
                    temp_anrede1 = guest.anrede1

                else:
                    temp_anrede1 = ""
                receiver = substring(f"{temp_name}, {temp_vorname1} {temp_anredefirma}{temp_anrede1}", 0, 32)
                output_list = Output_list()
                output_list_data.append(output_list)

                output_list.bill_art = artikel.artnr
                output_list.debt_counter = debitor.counter
                output_list.famt = to_string(
                    debt.vesrdep, "->>,>>>,>>>,>>9.99")

                if show_inv:

                    bill = get_cache(Bill, {"rechnr": [(eq, debitor.rechnr)]})

                    if bill:
                        output_list.inv_no = to_string(
                            bill.rechnr2, ">>>>>>>>>")

                        if bill.billref != 0:
                            output_list.soa_inv = "INV" + \
                                to_string(bill.billref, "9999999")
                    else:

                        bdebitor = get_cache(
                            Debitor, {"rechnr": [(eq, debitor.rechnr)], "debref": [(gt, 0)]})

                        if bdebitor:
                            output_list.soa_inv = "INV" + \
                                to_string(debitor.debref, "9999999")

                output_list.pay_amt = to_decimal(debitor.saldo)
                output_list.pay_famt = to_decimal(debitor.vesrdep)

                if not long_digit:
                    output_list.str = to_string(debt.rgdatum) +\
                        to_string(debitor.rechnr, ">>>,>>>,>>9") +\
                        to_string(receiver, "x(32)") +\
                        to_string(debt.saldo, "->,>>>,>>>,>>9.99") +\
                        to_string(debitor.saldo, "->,>>>,>>>,>>9.99") +\
                        to_string(art.bezeich, "x(34)") +\
                        to_string(debitor.rgdatum)
                else:
                    output_list.str = to_string(debt.rgdatum) +\
                        to_string(debitor.rechnr, ">>>,>>>,>>9") +\
                        to_string(receiver, "x(32)") +\
                        to_string(debt.saldo, " ->>>,>>>,>>>,>>9") +\
                        to_string(debitor.saldo, " ->>>,>>>,>>>,>>9") +\
                        to_string(art.bezeich, "x(34)") +\
                        to_string(debitor.rgdatum)
                output_list.bill_num = debitor.rechnr
                output_list.art_bezeich = artikel.bezeich
                output_list.tbetrag = to_decimal(
                    output_list.tbetrag) - to_decimal(debitor.saldo)

                bguest = get_cache(
                    Guest, {"gastnr": [(eq, debitor.gastnrmember)]})

                if bguest:
                    output_list.gastname = substring(f"{bguest.name}, {bguest.vorname1}{bguest.anredefirma} {bguest.anrede1}", 0, 32)

                bediener = get_cache(
                    Bediener, {"nr": [(eq, debitor.bediener_nr)]})

                if bediener:
                    output_list.str = output_list.str + \
                        to_string(bediener.userinit, "x(3)")
                else:
                    output_list.str = output_list.str + "   "
                output_list.str = output_list.str + \
                    to_string(debitor.vesrcod, "x(34)")
                output_list.str = output_list.str + to_string(" ", "x(22)")

                t_guest = get_cache(
                    Guest, {"gastnr": [(eq, debt.gastnrmember)]})

                if t_guest:
                    tstr = substring(f"{t_guest.name}, {t_guest.vorname1}{t_guest.anrede1}", 0, 34)
                else:
                    tstr = " "
                output_list.str = output_list.str + to_string(tstr, "x(50)")
                output_list.str = output_list.str + \
                    to_string(debitor.vesrdep, "->,>>>,>>>,>>9.99")
                output_list.str = output_list.str + \
                    to_string(debitor.zahlkonto, ">>>>9")
                output_list.str = output_list.str + \
                    to_string(debitor.vesrdep, "->,>>>,>>>,>>9.99")
                output_list.str = output_list.str + \
                    to_string(artikel.bezeich, "x(40)")

                t_credit = to_decimal(t_credit) + to_decimal(debitor.saldo)
                t_famt = to_decimal(t_famt) + to_decimal(debitor.vesrdep)
                tot_credit = to_decimal(tot_credit) + to_decimal(debitor.saldo)
                tot_saldo = to_decimal(tot_saldo) + to_decimal(debitor.saldo)
                tot_foreign = to_decimal(
                    tot_foreign) + to_decimal(debitor.vesrdep)
                tot_famt = to_decimal(tot_famt) + to_decimal(debitor.vesrdep)

                s_list = query(s_list_data, filters=(
                    lambda s_list: s_list.artnr == art.artnr), first=True)

                if not s_list:
                    s_list = S_list()
                    s_list_data.append(s_list)

                    s_list.artnr = art.artnr
                    s_list.bezeich = art.bezeich
                s_list.betrag = to_decimal(
                    s_list.betrag) + to_decimal(debitor.saldo)
        output_list = Output_list()
        output_list_data.append(output_list)

        for i in range(1, 58 + 1):
            output_list.str = output_list.str + "   "
        output_list.pay_amt = to_decimal(tot_saldo)
        output_list.pay_famt = to_decimal(tot_foreign)

        if not long_digit:
            output_list.str = output_list.str + "T O T A L " +\
                to_string(tot_saldo, "->,>>>,>>>,>>9.99") +\
                fill(" ", 78) +\
                to_string(tot_foreign, " ->>,>>>,>>>,>>9.99")
        else:
            output_list.str = output_list.str + "T O T A L " +\
                to_string(tot_saldo, " ->>>,>>>,>>>,>>9") +\
                fill(" ", 78) +\
                to_string(tot_foreign, "   ->>>,>>>,>>>,>>9")
        output_list = Output_list()
        output_list_data.append(output_list)

        output_list = Output_list()
        output_list_data.append(output_list)

        for i in range(1, 58 + 1):
            output_list.str = output_list.str + "   "
        output_list.pay_amt = to_decimal(t_credit)
        output_list.pay_famt = to_decimal(t_famt)

        if not long_digit:
            output_list.str = output_list.str + "Sub-Total " +\
                to_string(t_credit, "->,>>>,>>>,>>9.99") +\
                fill(" ", 78) +\
                to_string(t_famt, "->>,>>>,>>>,>>9.99")
        else:
            output_list.str = output_list.str + "Sub-Total " +\
                to_string(t_credit, " ->>>,>>>,>>>,>>9") +\
                fill(" ", 78) +\
                to_string(t_famt, "  ->>>,>>>,>>>,>>9")
        output_list = Output_list()
        output_list_data.append(output_list)

        output_list = Output_list()
        output_list_data.append(output_list)

        for i in range(1, 56 + 1):
            output_list.str = output_list.str + " "
        output_list.pay_amt = to_decimal(tot_credit)
        output_list.pay_famt = to_decimal(tot_famt)

        if not long_digit:
            output_list.str = output_list.str + "Grand TOTAL " +\
                to_string(tot_credit, "->,>>>,>>>,>>9.99") +\
                fill(" ", 78) + \
                to_string(tot_famt, "->>,>>>,>>>,>>9.99")
        else:
            output_list.str = output_list.str + "Grand TOTAL " +\
                to_string(tot_credit, " ->>>,>>>,>>>,>>9") +\
                fill(" ", 78) + \
                to_string(tot_famt, "  ->>>,>>>,>>>,>>9")
        create_tot_payment()

    def create_list3e():

        nonlocal r_no, s_list_data, t_list_data, t_ar_paylist_data, long_digit, htparam, guest, debitor, artikel, bill, bediener, waehrung
        nonlocal comment, cledger, ccard, last_sort, from_date, to_date, from_art, to_art, mi_payment, mi_transfer, show_inv, bill_name, bill_nr
        nonlocal bguest, bdebitor

        nonlocal s_list, t_list, output_list, t_ar_paylist, bguest, bdebitor, tbuff, bq
        nonlocal s_list_data, t_list_data, output_list_data, t_ar_paylist_data

        artnr: int = 0
        i: int = 0
        curr_date: date = None
        t_credit: Decimal = to_decimal("0.0")
        tot_credit: Decimal = to_decimal("0.0")
        t_famt: Decimal = to_decimal("0.0")
        tot_famt: Decimal = to_decimal("0.0")
        tot_saldo: Decimal = to_decimal("0.0")
        tot_foreign: Decimal = to_decimal("0.0")
        receiver: string = ""
        do_it: bool = False
        temp_name: string = ""
        temp_vorname1: string = ""
        temp_anredefirma: string = ""
        temp_anrede1: string = ""
        debt = None
        art = None
        t_guest = None
        tstr: string = ""
        Debt = create_buffer("Debt", Debitor)
        Art = create_buffer("Art", Artikel)
        T_guest = create_buffer("T_guest", Guest)

        debitor_obj_list = {}
        debitor = Debitor()
        debt = Debitor()
        artikel = Artikel()
        art = Artikel()
        guest = Guest()
        for debitor.gastnr, debitor.saldo, debitor.zahlkonto, debitor.betriebsnr, debitor.counter, debitor.rechnr, debitor.debref, debitor.rgdatum, debitor.gastnrmember, debitor.bediener_nr, debitor.vesrcod, debitor.vesrdep, debitor.betrieb_gastmem, debitor._recid, debt.gastnr, debt.saldo, debt.zahlkonto, debt.betriebsnr, debt.counter, debt.rechnr, debt.debref, debt.rgdatum, debt.gastnrmember, debt.bediener_nr, debt.vesrcod, debt.vesrdep, debt.betrieb_gastmem, debt._recid, artikel.artnr, artikel.bezeich, artikel.artart, artikel._recid, art.artnr, art.bezeich, art.artart, art._recid, guest.name, guest.vorname1, guest.anredefirma, guest.anrede1, guest._recid in db_session.query(Debitor.gastnr, Debitor.saldo, Debitor.zahlkonto, Debitor.betriebsnr, Debitor.counter, Debitor.rechnr, Debitor.debref, Debitor.rgdatum, Debitor.gastnrmember, Debitor.bediener_nr, Debitor.vesrcod, Debitor.vesrdep, Debitor.betrieb_gastmem, Debitor._recid, Debt.gastnr, Debt.saldo, Debt.zahlkonto, Debt.betriebsnr, Debt.counter, Debt.rechnr, Debt.debref, Debt.rgdatum, Debt.gastnrmember, Debt.bediener_nr, Debt.vesrcod, Debt.vesrdep, Debt.betrieb_gastmem, Debt._recid, Artikel.artnr, Artikel.bezeich, Artikel.artart, Artikel._recid, Art.artnr, Art.bezeich, Art.artart, Art._recid, Guest.name, Guest.vorname1, Guest.anredefirma, Guest.anrede1, Guest._recid).join(Debt, (Debt.counter == Debitor.counter) & (Debt.zahlkonto == 0)).join(Artikel, (Artikel.artnr == Debitor.artnr) & (Artikel.departement == 0) & (Artikel.artart == 7)).join(Art, (Art.artnr == Debitor.zahlkonto) & (Art.departement == 0)).join(Guest, (Guest.gastnr == Debitor.gastnr)).filter(
                (Debitor.rgdatum >= from_date) & (Debitor.rgdatum <= to_date) & (Debitor.zahlkonto > 0) & (Debitor.artnr >= from_art) & (Debitor.artnr <= to_art) & (Debitor.counter > 0) & (Debitor.opart > 0)).order_by(Artikel.artnr, Debitor.rgdatum, Debitor.vesrcod, Debitor.name, Debitor.zahlkonto, Debitor.rechnr).all():
            if debitor_obj_list.get(debitor._recid):
                continue
            else:
                debitor_obj_list[debitor._recid] = True

            do_it = True

            if mi_payment:

                if artikel.artart == 2 and art.artart != 4 and art.artart != 7:
                    do_it = False

                elif artikel.artart == 7 and art.artart != 4:
                    do_it = False

            elif mi_transfer:

                if artikel.artart == 2 and (art.artart == 4 or art.artart == 7):
                    do_it = False

                elif artikel.artart == 7 and art.artart == 4:
                    do_it = False

            if do_it and (bill_name != "") and (substring(bill_name, 0, 1) != ("*").lower()):

                if not matches(guest.name, r"*" + bill_name + r"*"):
                    do_it = False

            if do_it and (bill_name != "") and (substring(bill_name, 0, 1) == ("*").lower()):

                if not matches(guest.name, bill_name):
                    do_it = False

            if do_it:

                if curr_date == None:
                    curr_date = debitor.rgdatum

                if curr_date != debitor.rgdatum:
                    curr_date = debitor.rgdatum
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    for i in range(1, 58 + 1):
                        output_list.str = output_list.str + "   "
                    output_list.pay_amt = to_decimal(tot_saldo)
                    output_list.pay_famt = to_decimal(tot_foreign)

                    if not long_digit:
                        output_list.str = output_list.str + "T O T A L " +\
                            to_string(tot_saldo, "->,>>>,>>>,>>9.99") +\
                            fill(" ", 78) +\
                            to_string(tot_foreign, " ->>,>>>,>>>,>>9.99")
                    else:
                        output_list.str = output_list.str + "T O T A L " +\
                            to_string(tot_saldo, " ->>>,>>>,>>>,>>9") +\
                            fill(" ", 78) +\
                            to_string(tot_foreign, "   ->>>,>>>,>>>,>>9")
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    tot_saldo = to_decimal("0")
                    tot_foreign = to_decimal("0")

                if artnr != artikel.artnr:
                    t_list = T_list()
                    t_list_data.append(t_list)

                    t_list.artnr = artikel.artnr
                    t_list.bezeich = artikel.bezeich

                    if artnr != 0:
                        output_list = Output_list()
                        output_list_data.append(output_list)

                        for i in range(1, 58 + 1):
                            output_list.str = output_list.str + "   "
                        output_list.pay_amt = to_decimal(t_credit)
                        output_list.pay_famt = to_decimal(t_famt)

                        if not long_digit:
                            output_list.str = output_list.str + "Sub-Total " +\
                                to_string(t_credit, "->,>>>,>>>,>>9.99") +\
                                fill(" ", 78) +\
                                to_string(t_famt, "->>,>>>,>>>,>>9.99")
                        else:
                            output_list.str = output_list.str + "Sub-Total " +\
                                to_string(t_credit, " ->>>,>>>,>>>,>>9") +\
                                fill(" ", 78) +\
                                to_string(t_famt, "  ->>>,>>>,>>>,>>9")
                        output_list = Output_list()
                        output_list_data.append(output_list)

                        t_credit = to_decimal("0")
                        t_famt = to_decimal("0")
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    for i in range(1, 19 + 1):
                        output_list.str = output_list.str + " "
                    output_list.str = output_list.str +\
                        to_string(artikel.artnr, ">>>>9") + " - " +\
                        to_string(artikel.bezeich, "x(34)")
                    artnr = artikel.artnr
                t_list.betrag = to_decimal(
                    t_list.betrag) - to_decimal(debitor.saldo)

                if guest.name != None:
                    temp_name = guest.name

                else:
                    temp_name = ""

                if guest.vorname1 != None:
                    temp_vorname1 = guest.vorname1

                else:
                    temp_vorname1 = ""

                if guest.anredefirma != None:
                    temp_anredefirma = guest.anredefirma

                else:
                    temp_anredefirma = ""

                if guest.anrede1 != None:
                    temp_anrede1 = guest.anrede1

                else:
                    temp_anrede1 = ""
                receiver = substring(f"{temp_name}, {temp_vorname1} {temp_anredefirma}{temp_anrede1}", 0, 32)
                output_list = Output_list()
                output_list_data.append(output_list)

                output_list.bill_art = artikel.artnr
                output_list.debt_counter = debitor.counter
                output_list.famt = to_string(
                    debt.vesrdep, "->>,>>>,>>>,>>9.99")

                if show_inv:

                    bill = get_cache(Bill, {"rechnr": [(eq, debitor.rechnr)]})

                    if bill:
                        output_list.inv_no = to_string(
                            bill.rechnr2, ">>>>>>>>>")

                        if bill.billref != 0:
                            output_list.soa_inv = "INV" + \
                                to_string(bill.billref, "9999999")
                    else:

                        bdebitor = get_cache(
                            Debitor, {"rechnr": [(eq, debitor.rechnr)], "debref": [(gt, 0)]})

                        if bdebitor:
                            output_list.soa_inv = "INV" + \
                                to_string(debitor.debref, "9999999")

                output_list.pay_amt = to_decimal(debitor.saldo)
                output_list.pay_famt = to_decimal(debitor.vesrdep)

                if not long_digit:
                    output_list.str = to_string(debt.rgdatum) +\
                        to_string(debitor.rechnr, ">>>,>>>,>>9") +\
                        to_string(receiver, "x(32)") +\
                        to_string(debt.saldo, "->,>>>,>>>,>>9.99") +\
                        to_string(debitor.saldo, "->,>>>,>>>,>>9.99") +\
                        to_string(art.bezeich, "x(34)") +\
                        to_string(debitor.rgdatum)
                else:
                    output_list.str = to_string(debt.rgdatum) +\
                        to_string(debitor.rechnr, ">>>,>>>,>>9") +\
                        to_string(receiver, "x(32)") +\
                        to_string(debt.saldo, " ->>>,>>>,>>>,>>9") +\
                        to_string(debitor.saldo, " ->>>,>>>,>>>,>>9") +\
                        to_string(art.bezeich, "x(34)") +\
                        to_string(debitor.rgdatum)
                output_list.bill_num = debitor.rechnr
                output_list.art_bezeich = artikel.bezeich
                output_list.tbetrag = to_decimal(
                    output_list.tbetrag) - to_decimal(debitor.saldo)

                bguest = get_cache(
                    Guest, {"gastnr": [(eq, debitor.gastnrmember)]})

                if bguest:
                    output_list.gastname = substring(f"{bguest.name}, {bguest.vorname1}{bguest.anredefirma} {bguest.anrede1}", 0, 32)

                bediener = get_cache(
                    Bediener, {"nr": [(eq, debitor.bediener_nr)]})

                if bediener:
                    output_list.str = output_list.str + \
                        to_string(bediener.userinit, "x(3)")
                else:
                    output_list.str = output_list.str + "   "
                output_list.str = output_list.str + \
                    to_string(debitor.vesrcod, "x(34)")
                output_list.str = output_list.str + to_string(" ", "x(22)")

                t_guest = get_cache(
                    Guest, {"gastnr": [(eq, debt.gastnrmember)]})

                if t_guest:
                    tstr = substring(f"{t_guest.name}, {t_guest.vorname1}{t_guest.anrede1}", 0, 34)
                else:
                    tstr = " "
                output_list.str = output_list.str + to_string(tstr, "x(50)")
                output_list.str = output_list.str + \
                    to_string(debitor.vesrdep, "->,>>>,>>>,>>9.99")
                output_list.str = output_list.str + \
                    to_string(debitor.zahlkonto, ">>>>9")
                output_list.str = output_list.str + \
                    to_string(debitor.vesrdep, "->,>>>,>>>,>>9.99")
                output_list.str = output_list.str + \
                    to_string(artikel.bezeich, "x(40)")

                t_credit = to_decimal(t_credit) + to_decimal(debitor.saldo)
                t_famt = to_decimal(t_famt) + to_decimal(debitor.vesrdep)
                tot_credit = to_decimal(tot_credit) + to_decimal(debitor.saldo)
                tot_saldo = to_decimal(tot_saldo) + to_decimal(debitor.saldo)
                tot_foreign = to_decimal(
                    tot_foreign) + to_decimal(debitor.vesrdep)
                tot_famt = to_decimal(tot_famt) + to_decimal(debitor.vesrdep)

                s_list = query(s_list_data, filters=(
                    lambda s_list: s_list.artnr == art.artnr), first=True)

                if not s_list:
                    s_list = S_list()
                    s_list_data.append(s_list)

                    s_list.artnr = art.artnr
                    s_list.bezeich = art.bezeich
                s_list.betrag = to_decimal(
                    s_list.betrag) + to_decimal(debitor.saldo)
        output_list = Output_list()
        output_list_data.append(output_list)

        for i in range(1, 58 + 1):
            output_list.str = output_list.str + "   "
        output_list.pay_amt = to_decimal(tot_saldo)
        output_list.pay_famt = to_decimal(tot_foreign)

        if not long_digit:
            output_list.str = output_list.str + "T O T A L " +\
                to_string(tot_saldo, "->,>>>,>>>,>>9.99") +\
                fill(" ", 78) +\
                to_string(tot_foreign, " ->>,>>>,>>>,>>9.99")
        else:
            output_list.str = output_list.str + "T O T A L " +\
                to_string(tot_saldo, " ->>>,>>>,>>>,>>9") +\
                fill(" ", 78) +\
                to_string(tot_foreign, "   ->>>,>>>,>>>,>>9")
        output_list = Output_list()
        output_list_data.append(output_list)

        output_list = Output_list()
        output_list_data.append(output_list)

        for i in range(1, 58 + 1):
            output_list.str = output_list.str + "   "
        output_list.pay_amt = to_decimal(t_credit)
        output_list.pay_famt = to_decimal(t_famt)

        if not long_digit:
            output_list.str = output_list.str + "Sub-Total " +\
                to_string(t_credit, "->,>>>,>>>,>>9.99") +\
                fill(" ", 78) +\
                to_string(t_famt, "->>,>>>,>>>,>>9.99")
        else:
            output_list.str = output_list.str + "Sub-Total " +\
                to_string(t_credit, " ->>>,>>>,>>>,>>9") +\
                fill(" ", 78) +\
                to_string(t_famt, "  ->>>,>>>,>>>,>>9")
        output_list = Output_list()
        output_list_data.append(output_list)

        output_list = Output_list()
        output_list_data.append(output_list)

        for i in range(1, 56 + 1):
            output_list.str = output_list.str + " "
        output_list.pay_amt = to_decimal(tot_credit)
        output_list.pay_famt = to_decimal(tot_famt)

        if not long_digit:
            output_list.str = output_list.str + "Grand TOTAL " +\
                to_string(tot_credit, "->,>>>,>>>,>>9.99") +\
                fill(" ", 78) + \
                to_string(tot_famt, "->>,>>>,>>>,>>9.99")
        else:
            output_list.str = output_list.str + "Grand TOTAL " +\
                to_string(tot_credit, " ->>>,>>>,>>>,>>9") +\
                fill(" ", 78) + \
                to_string(tot_famt, "  ->>>,>>>,>>>,>>9")
        create_tot_payment()

    def create_list3f():

        nonlocal r_no, s_list_data, t_list_data, t_ar_paylist_data, long_digit, htparam, guest, debitor, artikel, bill, bediener, waehrung
        nonlocal comment, cledger, ccard, last_sort, from_date, to_date, from_art, to_art, mi_payment, mi_transfer, show_inv, bill_name, bill_nr
        nonlocal bguest, bdebitor

        nonlocal s_list, t_list, output_list, t_ar_paylist, bguest, bdebitor, tbuff, bq
        nonlocal s_list_data, t_list_data, output_list_data, t_ar_paylist_data

        artnr: int = 0
        i: int = 0
        curr_gastnr: int = 0
        t_credit: Decimal = to_decimal("0.0")
        tot_credit: Decimal = to_decimal("0.0")
        t_famt: Decimal = to_decimal("0.0")
        tot_famt: Decimal = to_decimal("0.0")
        tot_saldo: Decimal = to_decimal("0.0")
        tot_foreign: Decimal = to_decimal("0.0")
        receiver: string = ""
        do_it: bool = False
        temp_name: string = ""
        temp_vorname1: string = ""
        temp_anredefirma: string = ""
        temp_anrede1: string = ""
        debt = None
        art = None
        t_guest = None
        tstr: string = ""
        Debt = create_buffer("Debt", Debitor)
        Art = create_buffer("Art", Artikel)
        T_guest = create_buffer("T_guest", Guest)

        debitor_obj_list = {}
        debitor = Debitor()
        debt = Debitor()
        artikel = Artikel()
        art = Artikel()
        guest = Guest()
        for debitor.gastnr, debitor.saldo, debitor.zahlkonto, debitor.betriebsnr, debitor.counter, debitor.rechnr, debitor.debref, debitor.rgdatum, debitor.gastnrmember, debitor.bediener_nr, debitor.vesrcod, debitor.vesrdep, debitor.betrieb_gastmem, debitor._recid, debt.gastnr, debt.saldo, debt.zahlkonto, debt.betriebsnr, debt.counter, debt.rechnr, debt.debref, debt.rgdatum, debt.gastnrmember, debt.bediener_nr, debt.vesrcod, debt.vesrdep, debt.betrieb_gastmem, debt._recid, artikel.artnr, artikel.bezeich, artikel.artart, artikel._recid, art.artnr, art.bezeich, art.artart, art._recid, guest.name, guest.vorname1, guest.anredefirma, guest.anrede1, guest._recid in db_session.query(Debitor.gastnr, Debitor.saldo, Debitor.zahlkonto, Debitor.betriebsnr, Debitor.counter, Debitor.rechnr, Debitor.debref, Debitor.rgdatum, Debitor.gastnrmember, Debitor.bediener_nr, Debitor.vesrcod, Debitor.vesrdep, Debitor.betrieb_gastmem, Debitor._recid, Debt.gastnr, Debt.saldo, Debt.zahlkonto, Debt.betriebsnr, Debt.counter, Debt.rechnr, Debt.debref, Debt.rgdatum, Debt.gastnrmember, Debt.bediener_nr, Debt.vesrcod, Debt.vesrdep, Debt.betrieb_gastmem, Debt._recid, Artikel.artnr, Artikel.bezeich, Artikel.artart, Artikel._recid, Art.artnr, Art.bezeich, Art.artart, Art._recid, Guest.name, Guest.vorname1, Guest.anredefirma, Guest.anrede1, Guest._recid).join(Debt, (Debt.counter == Debitor.counter) & (Debt.zahlkonto == 0)).join(Artikel, (Artikel.artnr == Debitor.artnr) & (Artikel.departement == 0) & (Artikel.artart == 7)).join(Art, (Art.artnr == Debitor.zahlkonto) & (Art.departement == 0)).join(Guest, (Guest.gastnr == Debitor.gastnr)).filter(
                (Debitor.zahlkonto > 0) & (Debitor.artnr >= from_art) & (Debitor.artnr <= to_art) & (Debitor.counter > 0) & (Debitor.opart > 0) & (Debitor.rechnr == bill_nr)).order_by(Artikel.artnr, Debitor.name, Debitor.gastnr, Debitor.rgdatum, Debitor.zahlkonto, Debitor.betriebsnr, Debitor.rechnr).all():
            if debitor_obj_list.get(debitor._recid):
                continue
            else:
                debitor_obj_list[debitor._recid] = True

            do_it = True

            if mi_payment:

                if artikel.artart == 2 and art.artart != 4 and art.artart != 7:
                    do_it = False

                elif artikel.artart == 7 and art.artart != 4:
                    do_it = False

            elif mi_transfer:

                if artikel.artart == 2 and (art.artart == 4 or art.artart == 7):
                    do_it = False

                elif artikel.artart == 7 and art.artart == 4:
                    do_it = False

            if do_it:

                if curr_gastnr == 0:
                    curr_gastnr = debitor.gastnr

                if curr_gastnr != debitor.gastnr:
                    curr_gastnr = debitor.gastnr
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    for i in range(1, 58 + 1):
                        output_list.str = output_list.str + "   "
                    output_list.pay_amt = to_decimal(tot_saldo)
                    output_list.pay_famt = to_decimal(tot_foreign)

                    if not long_digit:
                        output_list.str = output_list.str + "T O T A L " +\
                            to_string(tot_saldo, "->,>>>,>>>,>>9.99") +\
                            fill(" ", 78) +\
                            to_string(tot_foreign, " ->>,>>>,>>>,>>9.99")
                    else:
                        output_list.str = output_list.str + "T O T A L " +\
                            to_string(tot_saldo, " ->>>,>>>,>>>,>>9") +\
                            fill(" ", 78) +\
                            to_string(tot_foreign, "   ->>>,>>>,>>>,>>9")
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    tot_saldo = to_decimal("0")
                    tot_foreign = to_decimal("0")

                if artnr != artikel.artnr:
                    t_list = T_list()
                    t_list_data.append(t_list)

                    t_list.artnr = artikel.artnr
                    t_list.bezeich = artikel.bezeich

                    if artnr != 0:

                        if tot_saldo != 0:
                            output_list = Output_list()
                            output_list_data.append(output_list)

                            for i in range(1, 58 + 1):
                                output_list.str = output_list.str + "   "
                            output_list.pay_amt = to_decimal(tot_saldo)
                            output_list.pay_famt = to_decimal(tot_foreign)

                            if not long_digit:
                                output_list.str = output_list.str + "T O T A L " +\
                                    to_string(tot_saldo, "->,>>>,>>>,>>9.99") +\
                                    fill(" ", 78) +\
                                    to_string(tot_foreign, " ->>,>>>,>>>,>>9.99")
                            else:
                                output_list.str = output_list.str + "T O T A L " +\
                                    to_string(tot_saldo, " ->>>,>>>,>>>,>>9") +\
                                    fill(" ", 78) +\
                                    to_string(tot_foreign, "   ->>>,>>>,>>>,>>9")
                            output_list = Output_list()
                            output_list_data.append(output_list)

                            tot_saldo = to_decimal("0")
                            tot_foreign = to_decimal("0")
                        output_list = Output_list()
                        output_list_data.append(output_list)

                        for i in range(1, 58 + 1):
                            output_list.str = output_list.str + "   "
                        output_list.pay_amt = to_decimal(t_credit)
                        output_list.pay_famt = to_decimal(t_famt)

                        if not long_digit:
                            output_list.str = output_list.str + "Sub-Total " +\
                                to_string(t_credit, "->,>>>,>>>,>>9.99") +\
                                fill(" ", 78) +\
                                to_string(t_famt, "->>,>>>,>>>,>>9.99")
                        else:
                            output_list.str = output_list.str + "Sub-Total " +\
                                to_string(t_credit, " ->>>,>>>,>>>,>>9") +\
                                fill(" ", 78) +\
                                to_string(t_famt, "  ->>>,>>>,>>>,>>9")
                        output_list = Output_list()
                        output_list_data.append(output_list)

                        t_credit = to_decimal("0")
                        t_famt = to_decimal("0")
                        tot_saldo = to_decimal("0")
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    for i in range(1, 19 + 1):
                        output_list.str = output_list.str + " "
                    output_list.str = output_list.str +\
                        to_string(artikel.artnr, ">>>>9") + " - " +\
                        to_string(artikel.bezeich, "x(34)")
                    artnr = artikel.artnr
                t_list.betrag = to_decimal(
                    t_list.betrag) - to_decimal(debitor.saldo)

                if guest.name != None:
                    temp_name = guest.name

                else:
                    temp_name = ""

                if guest.vorname1 != None:
                    temp_vorname1 = guest.vorname1

                else:
                    temp_vorname1 = ""

                if guest.anredefirma != None:
                    temp_anredefirma = guest.anredefirma

                else:
                    temp_anredefirma = ""

                if guest.anrede1 != None:
                    temp_anrede1 = guest.anrede1

                else:
                    temp_anrede1 = ""
                receiver = substring(f"{temp_name}, {temp_vorname1} {temp_anredefirma}{temp_anrede1}", 0, 32)
                output_list = Output_list()
                output_list_data.append(output_list)

                output_list.bill_art = artikel.artnr
                output_list.debt_counter = debitor.counter
                output_list.famt = to_string(
                    debt.vesrdep, "->>,>>>,>>>,>>9.99")

                if show_inv:

                    bill = get_cache(Bill, {"rechnr": [(eq, debitor.rechnr)]})

                    if bill:
                        output_list.inv_no = to_string(
                            bill.rechnr2, ">>>>>>>>>")

                        if bill.billref != 0:
                            output_list.soa_inv = "INV" + \
                                to_string(bill.billref, "9999999")
                    else:

                        bdebitor = get_cache(
                            Debitor, {"rechnr": [(eq, debitor.rechnr)], "debref": [(gt, 0)]})

                        if bdebitor:
                            output_list.soa_inv = "INV" + \
                                to_string(debitor.debref, "9999999")

                output_list.pay_amt = to_decimal(debitor.saldo)
                output_list.pay_famt = to_decimal(debitor.vesrdep)

                if not long_digit:
                    output_list.str = to_string(debt.rgdatum) +\
                        to_string(debitor.rechnr, ">>>,>>>,>>9") +\
                        to_string(receiver, "x(32)") +\
                        to_string(debt.saldo, "->,>>>,>>>,>>9.99") +\
                        to_string(debitor.saldo, "->,>>>,>>>,>>9.99") +\
                        to_string(art.bezeich, "x(34)") +\
                        to_string(debitor.rgdatum)
                else:
                    output_list.str = to_string(debt.rgdatum) +\
                        to_string(debitor.rechnr, ">>>,>>>,>>9") +\
                        to_string(receiver, "x(32)") +\
                        to_string(debt.saldo, " ->>>,>>>,>>>,>>9") +\
                        to_string(debitor.saldo, " ->>>,>>>,>>>,>>9") +\
                        to_string(art.bezeich, "x(34)") +\
                        to_string(debitor.rgdatum)
                output_list.bill_num = debitor.rechnr
                output_list.art_bezeich = artikel.bezeich
                output_list.tbetrag = to_decimal(
                    output_list.tbetrag) - to_decimal(debitor.saldo)

                bguest = get_cache(
                    Guest, {"gastnr": [(eq, debitor.gastnrmember)]})

                if bguest:
                    output_list.gastname = substring(f"{bguest.name}, {bguest.vorname1}{bguest.anredefirma} {bguest.anrede1}", 0, 32)

                bediener = get_cache(
                    Bediener, {"nr": [(eq, debitor.bediener_nr)]})

                if bediener:
                    output_list.str = output_list.str + \
                        to_string(bediener.userinit, "x(3)")
                else:
                    output_list.str = output_list.str + "   "
                output_list.str = output_list.str + \
                    to_string(debitor.vesrcod, "x(34)")
                output_list.str = output_list.str + to_string(" ", "x(22)")

                t_guest = get_cache(
                    Guest, {"gastnr": [(eq, debt.gastnrmember)]})

                if t_guest:
                    tstr = substring(f"{t_guest.name}, {t_guest.vorname1}{t_guest.anrede1}", 0, 34)
                else:
                    tstr = " "
                output_list.str = output_list.str + to_string(tstr, "x(50)")
                output_list.str = output_list.str + \
                    to_string(debitor.vesrdep, "->,>>>,>>>,>>9.99")
                output_list.str = output_list.str + \
                    to_string(debitor.zahlkonto, ">>>>9")
                output_list.str = output_list.str + \
                    to_string(debitor.vesrdep, "->,>>>,>>>,>>9.99")
                output_list.str = output_list.str + \
                    to_string(artikel.bezeich, "x(40)")

                t_credit = to_decimal(t_credit) + to_decimal(debitor.saldo)
                t_famt = to_decimal(t_famt) + to_decimal(debitor.vesrdep)
                tot_credit = to_decimal(tot_credit) + to_decimal(debitor.saldo)
                tot_saldo = to_decimal(tot_saldo) + to_decimal(debitor.saldo)
                tot_foreign = to_decimal(
                    tot_foreign) + to_decimal(debitor.vesrdep)
                tot_famt = to_decimal(tot_famt) + to_decimal(debitor.vesrdep)

                s_list = query(s_list_data, filters=(
                    lambda s_list: s_list.artnr == art.artnr), first=True)

                if not s_list:
                    s_list = S_list()
                    s_list_data.append(s_list)

                    s_list.artnr = art.artnr
                    s_list.bezeich = art.bezeich
                s_list.betrag = to_decimal(
                    s_list.betrag) + to_decimal(debitor.saldo)
        output_list = Output_list()
        output_list_data.append(output_list)

        for i in range(1, 58 + 1):
            output_list.str = output_list.str + "   "
        output_list.pay_amt = to_decimal(tot_saldo)
        output_list.pay_famt = to_decimal(tot_foreign)

        if not long_digit:
            output_list.str = output_list.str + "T O T A L " +\
                to_string(tot_saldo, "->,>>>,>>>,>>9.99") +\
                fill(" ", 78) +\
                to_string(tot_foreign, " ->>,>>>,>>>,>>9.99")
        else:
            output_list.str = output_list.str + "T O T A L " +\
                to_string(tot_saldo, " ->>>,>>>,>>>,>>9") +\
                fill(" ", 78) +\
                to_string(tot_foreign, "   ->>>,>>>,>>>,>>9")
        output_list = Output_list()
        output_list_data.append(output_list)

        output_list = Output_list()
        output_list_data.append(output_list)

        for i in range(1, 58 + 1):
            output_list.str = output_list.str + "   "
        output_list.pay_amt = to_decimal(t_credit)
        output_list.pay_famt = to_decimal(t_famt)

        if not long_digit:
            output_list.str = output_list.str + "Sub-Total " +\
                to_string(t_credit, "->,>>>,>>>,>>9.99") +\
                fill(" ", 78) +\
                to_string(t_famt, "->>,>>>,>>>,>>9.99")
        else:
            output_list.str = output_list.str + "Sub-Total " +\
                to_string(t_credit, " ->>>,>>>,>>>,>>9") +\
                fill(" ", 78) +\
                to_string(t_famt, "  ->>>,>>>,>>>,>>9")
        output_list = Output_list()
        output_list_data.append(output_list)

        output_list = Output_list()
        output_list_data.append(output_list)

        for i in range(1, 56 + 1):
            output_list.str = output_list.str + " "
        output_list.pay_amt = to_decimal(tot_credit)
        output_list.pay_famt = to_decimal(tot_famt)

        if not long_digit:
            output_list.str = output_list.str + "Grand TOTAL " +\
                to_string(tot_credit, "->,>>>,>>>,>>9.99") +\
                fill(" ", 78) + \
                to_string(tot_famt, "->>,>>>,>>>,>>9.99")
        else:
            output_list.str = output_list.str + "Grand TOTAL " +\
                to_string(tot_credit, " ->>>,>>>,>>>,>>9") +\
                fill(" ", 78) + \
                to_string(tot_famt, "  ->>>,>>>,>>>,>>9")
        create_tot_payment()

    def create_list3fs():

        nonlocal r_no, s_list_data, t_list_data, t_ar_paylist_data, long_digit, htparam, guest, debitor, artikel, bill, bediener, waehrung
        nonlocal comment, cledger, ccard, last_sort, from_date, to_date, from_art, to_art, mi_payment, mi_transfer, show_inv, bill_name, bill_nr
        nonlocal bguest, bdebitor

        nonlocal s_list, t_list, output_list, t_ar_paylist, bguest, bdebitor, tbuff, bq
        nonlocal s_list_data, t_list_data, output_list_data, t_ar_paylist_data

        artnr: int = 0
        i: int = 0
        curr_gastnr: int = 0
        t_credit: Decimal = to_decimal("0.0")
        tot_credit: Decimal = to_decimal("0.0")
        t_famt: Decimal = to_decimal("0.0")
        tot_famt: Decimal = to_decimal("0.0")
        tot_saldo: Decimal = to_decimal("0.0")
        tot_foreign: Decimal = to_decimal("0.0")
        receiver: string = ""
        do_it: bool = False
        temp_name: string = ""
        temp_vorname1: string = ""
        temp_anredefirma: string = ""
        temp_anrede1: string = ""
        debt = None
        art = None
        t_guest = None
        tstr: string = ""
        Debt = create_buffer("Debt", Debitor)
        Art = create_buffer("Art", Artikel)
        T_guest = create_buffer("T_guest", Guest)

        debitor_obj_list = {}
        debitor = Debitor()
        debt = Debitor()
        artikel = Artikel()
        art = Artikel()
        guest = Guest()
        for debitor.gastnr, debitor.saldo, debitor.zahlkonto, debitor.betriebsnr, debitor.counter, debitor.rechnr, debitor.debref, debitor.rgdatum, debitor.gastnrmember, debitor.bediener_nr, debitor.vesrcod, debitor.vesrdep, debitor.betrieb_gastmem, debitor._recid, debt.gastnr, debt.saldo, debt.zahlkonto, debt.betriebsnr, debt.counter, debt.rechnr, debt.debref, debt.rgdatum, debt.gastnrmember, debt.bediener_nr, debt.vesrcod, debt.vesrdep, debt.betrieb_gastmem, debt._recid, artikel.artnr, artikel.bezeich, artikel.artart, artikel._recid, art.artnr, art.bezeich, art.artart, art._recid, guest.name, guest.vorname1, guest.anredefirma, guest.anrede1, guest._recid in db_session.query(Debitor.gastnr, Debitor.saldo, Debitor.zahlkonto, Debitor.betriebsnr, Debitor.counter, Debitor.rechnr, Debitor.debref, Debitor.rgdatum, Debitor.gastnrmember, Debitor.bediener_nr, Debitor.vesrcod, Debitor.vesrdep, Debitor.betrieb_gastmem, Debitor._recid, Debt.gastnr, Debt.saldo, Debt.zahlkonto, Debt.betriebsnr, Debt.counter, Debt.rechnr, Debt.debref, Debt.rgdatum, Debt.gastnrmember, Debt.bediener_nr, Debt.vesrcod, Debt.vesrdep, Debt.betrieb_gastmem, Debt._recid, Artikel.artnr, Artikel.bezeich, Artikel.artart, Artikel._recid, Art.artnr, Art.bezeich, Art.artart, Art._recid, Guest.name, Guest.vorname1, Guest.anredefirma, Guest.anrede1, Guest._recid).join(Debt, (Debt.counter == Debitor.counter) & (Debt.zahlkonto == 0)).join(Artikel, (Artikel.artnr == Debitor.artnr) & (Artikel.departement == 0) & (Artikel.artart == 7)).join(Art, (Art.artnr == Debitor.zahlkonto) & (Art.departement == 0)).join(Guest, (Guest.gastnr == Debitor.gastnr)).filter(
                (Debitor.rgdatum >= from_date) & (Debitor.rgdatum <= to_date) & (Debitor.zahlkonto > 0) & (Debitor.artnr >= from_art) & (Debitor.artnr <= to_art) & (Debitor.counter > 0) & (Debitor.opart > 0)).order_by(Artikel.artnr, Debitor.name, Debitor.gastnr, Debitor.rgdatum, Debitor.zahlkonto, Debitor.betriebsnr, Debitor.rechnr).all():
            if debitor_obj_list.get(debitor._recid):
                continue
            else:
                debitor_obj_list[debitor._recid] = True

            do_it = True

            if mi_payment:

                if artikel.artart == 2 and art.artart != 4 and art.artart != 7:
                    do_it = False

                elif artikel.artart == 7 and art.artart != 4:
                    do_it = False

            elif mi_transfer:

                if artikel.artart == 2 and (art.artart == 4 or art.artart == 7):
                    do_it = False

                elif artikel.artart == 7 and art.artart == 4:
                    do_it = False

            if do_it:

                if curr_gastnr == 0:
                    curr_gastnr = debitor.gastnr

                if curr_gastnr != debitor.gastnr:
                    curr_gastnr = debitor.gastnr
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    for i in range(1, 58 + 1):
                        output_list.str = output_list.str + "   "
                    output_list.pay_amt = to_decimal(tot_saldo)
                    output_list.pay_famt = to_decimal(tot_foreign)

                    if not long_digit:
                        output_list.str = output_list.str + "T O T A L " +\
                            to_string(tot_saldo, "->,>>>,>>>,>>9.99") +\
                            fill(" ", 78) +\
                            to_string(tot_foreign, " ->>,>>>,>>>,>>9.99")
                    else:
                        output_list.str = output_list.str + "T O T A L " +\
                            to_string(tot_saldo, " ->>>,>>>,>>>,>>9") +\
                            fill(" ", 78) +\
                            to_string(tot_foreign, "   ->>>,>>>,>>>,>>9")
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    tot_saldo = to_decimal("0")
                    tot_foreign = to_decimal("0")

                if artnr != artikel.artnr:
                    t_list = T_list()
                    t_list_data.append(t_list)

                    t_list.artnr = artikel.artnr
                    t_list.bezeich = artikel.bezeich

                    if artnr != 0:

                        if tot_saldo != 0:
                            output_list = Output_list()
                            output_list_data.append(output_list)

                            for i in range(1, 58 + 1):
                                output_list.str = output_list.str + "   "
                            output_list.pay_amt = to_decimal(tot_saldo)
                            output_list.pay_famt = to_decimal(tot_foreign)

                            if not long_digit:
                                output_list.str = output_list.str + "T O T A L " +\
                                    to_string(tot_saldo, "->,>>>,>>>,>>9.99") +\
                                    fill(" ", 78) +\
                                    to_string(tot_foreign, " ->>,>>>,>>>,>>9.99")
                            else:
                                output_list.str = output_list.str + "T O T A L " +\
                                    to_string(tot_saldo, " ->>>,>>>,>>>,>>9") +\
                                    fill(" ", 78) +\
                                    to_string(tot_foreign, "   ->>>,>>>,>>>,>>9")
                            output_list = Output_list()
                            output_list_data.append(output_list)

                            tot_saldo = to_decimal("0")
                            tot_foreign = to_decimal("0")
                        output_list = Output_list()
                        output_list_data.append(output_list)

                        for i in range(1, 58 + 1):
                            output_list.str = output_list.str + "   "
                        output_list.pay_amt = to_decimal(t_credit)
                        output_list.pay_famt = to_decimal(t_famt)

                        if not long_digit:
                            output_list.str = output_list.str + "Sub-Total " +\
                                to_string(t_credit, "->,>>>,>>>,>>9.99") +\
                                fill(" ", 78) +\
                                to_string(t_famt, "->>,>>>,>>>,>>9.99")
                        else:
                            output_list.str = output_list.str + "Sub-Total " +\
                                to_string(t_credit, " ->>>,>>>,>>>,>>9") +\
                                fill(" ", 78) +\
                                to_string(t_famt, "  ->>>,>>>,>>>,>>9")
                        output_list = Output_list()
                        output_list_data.append(output_list)

                        t_credit = to_decimal("0")
                        t_famt = to_decimal("0")
                        tot_saldo = to_decimal("0")
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    for i in range(1, 19 + 1):
                        output_list.str = output_list.str + " "
                    output_list.str = output_list.str +\
                        to_string(artikel.artnr, ">>>>9") + " - " +\
                        to_string(artikel.bezeich, "x(34)")
                    artnr = artikel.artnr
                t_list.betrag = to_decimal(
                    t_list.betrag) - to_decimal(debitor.saldo)

                if guest.name != None:
                    temp_name = guest.name

                else:
                    temp_name = ""

                if guest.vorname1 != None:
                    temp_vorname1 = guest.vorname1

                else:
                    temp_vorname1 = ""

                if guest.anredefirma != None:
                    temp_anredefirma = guest.anredefirma

                else:
                    temp_anredefirma = ""

                if guest.anrede1 != None:
                    temp_anrede1 = guest.anrede1

                else:
                    temp_anrede1 = ""
                receiver = substring(f"{temp_name}, {temp_vorname1} {temp_anredefirma}{temp_anrede1}", 0, 32)
                output_list = Output_list()
                output_list_data.append(output_list)

                output_list.bill_art = artikel.artnr
                output_list.debt_counter = debitor.counter
                output_list.famt = to_string(
                    debt.vesrdep, "->>,>>>,>>>,>>9.99")

                if show_inv:

                    bill = get_cache(Bill, {"rechnr": [(eq, debitor.rechnr)]})

                    if bill:
                        output_list.inv_no = to_string(
                            bill.rechnr2, ">>>>>>>>>")

                        if bill.billref != 0:
                            output_list.soa_inv = "INV" + \
                                to_string(bill.billref, "9999999")
                    else:

                        bdebitor = get_cache(
                            Debitor, {"rechnr": [(eq, debitor.rechnr)], "debref": [(gt, 0)]})

                        if bdebitor:
                            output_list.soa_inv = "INV" + \
                                to_string(debitor.debref, "9999999")

                output_list.pay_amt = to_decimal(debitor.saldo)
                output_list.pay_famt = to_decimal(debitor.vesrdep)

                if not long_digit:
                    output_list.str = to_string(debt.rgdatum) +\
                        to_string(debitor.rechnr, ">>>,>>>,>>9") +\
                        to_string(receiver, "x(32)") +\
                        to_string(debt.saldo, "->,>>>,>>>,>>9.99") +\
                        to_string(debitor.saldo, "->,>>>,>>>,>>9.99") +\
                        to_string(art.bezeich, "x(34)") +\
                        to_string(debitor.rgdatum)
                else:
                    output_list.str = to_string(debt.rgdatum) +\
                        to_string(debitor.rechnr, ">>>,>>>,>>9") +\
                        to_string(receiver, "x(32)") +\
                        to_string(debt.saldo, " ->>>,>>>,>>>,>>9") +\
                        to_string(debitor.saldo, " ->>>,>>>,>>>,>>9") +\
                        to_string(art.bezeich, "x(34)") +\
                        to_string(debitor.rgdatum)
                output_list.bill_num = debitor.rechnr
                output_list.art_bezeich = artikel.bezeich
                output_list.tbetrag = to_decimal(
                    output_list.tbetrag) - to_decimal(debitor.saldo)

                bguest = get_cache(
                    Guest, {"gastnr": [(eq, debitor.gastnrmember)]})

                if bguest:
                    output_list.gastname = substring(f"{bguest.name}, {bguest.vorname1}{bguest.anredefirma} {bguest.anrede1}", 0, 32)

                bediener = get_cache(
                    Bediener, {"nr": [(eq, debitor.bediener_nr)]})

                if bediener:
                    output_list.str = output_list.str + \
                        to_string(bediener.userinit, "x(3)")
                else:
                    output_list.str = output_list.str + "   "
                output_list.str = output_list.str + \
                    to_string(debitor.vesrcod, "x(34)")
                output_list.str = output_list.str + to_string(" ", "x(22)")

                t_guest = get_cache(
                    Guest, {"gastnr": [(eq, debt.gastnrmember)]})

                if t_guest:
                    tstr = substring(f"{t_guest.name}, {t_guest.vorname1}{t_guest.anrede1}", 0, 34)
                else:
                    tstr = " "
                output_list.str = output_list.str + to_string(tstr, "x(50)")
                output_list.str = output_list.str + \
                    to_string(debitor.vesrdep, "->,>>>,>>>,>>9.99")
                output_list.str = output_list.str + \
                    to_string(debitor.zahlkonto, ">>>>9")
                output_list.str = output_list.str + \
                    to_string(debitor.vesrdep, "->,>>>,>>>,>>9.99")
                output_list.str = output_list.str + \
                    to_string(artikel.bezeich, "x(40)")

                t_credit = to_decimal(t_credit) + to_decimal(debitor.saldo)
                t_famt = to_decimal(t_famt) + to_decimal(debitor.vesrdep)
                tot_credit = to_decimal(tot_credit) + to_decimal(debitor.saldo)
                tot_saldo = to_decimal(tot_saldo) + to_decimal(debitor.saldo)
                tot_foreign = to_decimal(
                    tot_foreign) + to_decimal(debitor.vesrdep)
                tot_famt = to_decimal(tot_famt) + to_decimal(debitor.vesrdep)

                s_list = query(s_list_data, filters=(
                    lambda s_list: s_list.artnr == art.artnr), first=True)

                if not s_list:
                    s_list = S_list()
                    s_list_data.append(s_list)

                    s_list.artnr = art.artnr
                    s_list.bezeich = art.bezeich
                s_list.betrag = to_decimal(
                    s_list.betrag) + to_decimal(debitor.saldo)
        output_list = Output_list()
        output_list_data.append(output_list)

        for i in range(1, 58 + 1):
            output_list.str = output_list.str + "   "
        output_list.pay_amt = to_decimal(tot_saldo)
        output_list.pay_famt = to_decimal(tot_foreign)

        if not long_digit:
            output_list.str = output_list.str + "T O T A L " +\
                to_string(tot_saldo, "->,>>>,>>>,>>9.99") +\
                fill(" ", 78) +\
                to_string(tot_foreign, " ->>,>>>,>>>,>>9.99")
        else:
            output_list.str = output_list.str + "T O T A L " +\
                to_string(tot_saldo, " ->>>,>>>,>>>,>>9") +\
                fill(" ", 78) +\
                to_string(tot_foreign, "   ->>>,>>>,>>>,>>9")
        output_list = Output_list()
        output_list_data.append(output_list)

        output_list = Output_list()
        output_list_data.append(output_list)

        for i in range(1, 58 + 1):
            output_list.str = output_list.str + "   "
        output_list.pay_amt = to_decimal(t_credit)
        output_list.pay_famt = to_decimal(t_famt)

        if not long_digit:
            output_list.str = output_list.str + "Sub-Total " +\
                to_string(t_credit, "->,>>>,>>>,>>9.99") +\
                fill(" ", 78) +\
                to_string(t_famt, "->>,>>>,>>>,>>9.99")
        else:
            output_list.str = output_list.str + "Sub-Total " +\
                to_string(t_credit, " ->>>,>>>,>>>,>>9") +\
                fill(" ", 78) +\
                to_string(t_famt, "  ->>>,>>>,>>>,>>9")
        output_list = Output_list()
        output_list_data.append(output_list)

        output_list = Output_list()
        output_list_data.append(output_list)

        for i in range(1, 56 + 1):
            output_list.str = output_list.str + " "
        output_list.pay_amt = to_decimal(tot_credit)
        output_list.pay_famt = to_decimal(tot_famt)

        if not long_digit:
            output_list.str = output_list.str + "Grand TOTAL " +\
                to_string(tot_credit, "->,>>>,>>>,>>9.99") +\
                fill(" ", 78) + \
                to_string(tot_famt, "->>,>>>,>>>,>>9.99")
        else:
            output_list.str = output_list.str + "Grand TOTAL " +\
                to_string(tot_credit, " ->>>,>>>,>>>,>>9") +\
                fill(" ", 78) + \
                to_string(tot_famt, "  ->>>,>>>,>>>,>>9")
        create_tot_payment()

    htparam = get_cache(Htparam, {"paramnr": [(eq, 246)]})
    long_digit = htparam.flogical
    create_list()
    t_ar_paylist_data.clear()

    for output_list in query(output_list_data):
        t_ar_paylist = T_ar_paylist()
        t_ar_paylist_data.append(t_ar_paylist)
        
        log_program.write_log("LOG", f"output_str: {output_list.str}")

        t_ar_paylist.bill_date = substring(output_list.str, 0, 8)
        t_ar_paylist.bill_num = substring(output_list.str, 8, 11)
        t_ar_paylist.inv_num = output_list.inv_no
        t_ar_paylist.bill_rcv = substring(output_list.str, 19, 34)
        t_ar_paylist.debt_amt = substring(output_list.str, 51, 17)
        t_ar_paylist.curr = substring(output_list.str, 300, 3)
        # t_ar_paylist.curr =  ""
        t_ar_paylist.pay_art = substring(output_list.str, 83, 34)
        t_ar_paylist.pay_date = substring(output_list.str, 117, 8)
        t_ar_paylist.uid = substring(output_list.str, 125, 3)
        t_ar_paylist.pay_comment = substring(output_list.str, 128, 34)
        t_ar_paylist.tot_pay = output_list.sbetrag
        t_ar_paylist.artno = to_string(output_list.bill_art)
        t_ar_paylist.debt_counter = to_string(output_list.debt_counter)
        t_ar_paylist.art_bezeich = output_list.art_bezeich
        t_ar_paylist.tbetrag = to_string(
            output_list.tbetrag, "->>>,>>>,>>>,>>9.99")
        t_ar_paylist.gastname = substring(output_list.gastname, 0, 30)
        t_ar_paylist.soa_inv = output_list.soa_inv
        t_ar_paylist.famt = output_list.famt
        t_ar_paylist.bill_num2 = to_string(output_list.bill_num)

        if matches(t_ar_paylist.pay_comment, r"*?*"):
            t_ar_paylist.pay_comment = ""

        if not long_digit:
            t_ar_paylist.pay_amt = to_string(
                output_list.pay_amt, "->,>>>,>>>,>>>,>>9.99")
            t_ar_paylist.pay_famt = to_string(
                output_list.pay_famt, "->,>>>,>>>,>>>,>>>,>>9.99")

        else:
            t_ar_paylist.pay_amt = to_string(
                output_list.pay_amt, "->>>,>>>,>>>,>>>,>>9")
            t_ar_paylist.pay_famt = to_string(
                output_list.pay_famt, "->>>,>>>,>>>,>>>,>>>,>>9")

    return generate_output()
