from functions.additional_functions import *
import decimal
from datetime import date
import re
from models import Htparam, Kellner, H_bill_line, H_bill, Bill, Res_line, H_artikel, Artikel

def rest_daymercure_btn_gobl(bline_list:[Bline_list], shift:int, from_date:date, exchg_rate:decimal):
    tot_debit:decimal = 0
    tot_cover:int = 0
    nt_debit:decimal = 0
    nt_cover:int = 0
    t_debit:decimal = 0
    t_cash:decimal = 0
    t_cash1:decimal = 0
    t_trans:decimal = 0
    t_ledger:decimal = 0
    t_coupon:decimal = 0
    t_compli:decimal = 0
    t_cover:int = 0
    anz_comp:int = 0
    val_comp:decimal = 0
    anz_coup:int = 0
    val_coup:decimal = 0
    serv_taxable:bool = False
    tot_cash = 0
    tot_cash1 = 0
    tot_ledger = 0
    tot_trans = 0
    tot_compli = 0
    tot_coupon = 0
    nt_cash = 0
    nt_cash1 = 0
    nt_ledger = 0
    nt_trans = 0
    nt_compli = 0
    nt_coupon = 0
    t_betrag = 0
    t_foreign = 0
    turnover_list = []
    htparam = kellner = h_bill_line = h_bill = bill = res_line = h_artikel = artikel = None

    cash_art = bline_list = outstand_list = pay_list = turnover = bufparam = kellner1 = tlist = h_bline = None

    cash_art_list, Cash_art = create_model("Cash_art", {"sortnr":int, "usrnr":int, "usrnm":str, "artnr":int, "bezeich":str, "amount":decimal})
    bline_list_list, Bline_list = create_model("Bline_list", {"selected":bool, "name":str, "depart":str, "dept":int, "knr":int, "bl_recid":int})
    outstand_list_list, Outstand_list = create_model("Outstand_list", {"name":str, "rechnr":int, "foreign":decimal, "saldo":decimal})
    pay_list_list, Pay_list = create_model("Pay_list", {"compli":bool, "person":int, "flag":int, "bezeich":str, "artnr":int, "rechnr":int, "foreign":decimal, "saldo":decimal}, {"compli": no})
    turnover_list, Turnover = create_model("Turnover", {"departement":int, "deptname":str, "kellner_nr":int, "name":str, "tischnr":int, "rechnr":str, "belegung":int, "artnr":int, "info":str, "t_debit":decimal, "t_credit":decimal, "p_cash":decimal, "p_cash1":decimal, "r_transfer":decimal, "c_ledger":decimal, "compli":bool, "flag":int, "coupon":decimal, "comp":decimal, "gname":str})

    Bufparam = Htparam
    Kellner1 = Kellner
    Tlist = Turnover
    tlist_list = turnover_list

    H_bline = H_bill_line

    db_session = local_storage.db_session

    def generate_output():
        nonlocal tot_debit, tot_cover, nt_debit, nt_cover, t_debit, t_cash, t_cash1, t_trans, t_ledger, t_coupon, t_compli, t_cover, anz_comp, val_comp, anz_coup, val_coup, serv_taxable, tot_cash, tot_cash1, tot_ledger, tot_trans, tot_compli, tot_coupon, nt_cash, nt_cash1, nt_ledger, nt_trans, nt_compli, nt_coupon, t_betrag, t_foreign, turnover_list, htparam, kellner, h_bill_line, h_bill, bill, res_line, h_artikel, artikel
        nonlocal bufparam, kellner1, tlist, h_bline


        nonlocal cash_art, bline_list, outstand_list, pay_list, turnover, bufparam, kellner1, tlist, h_bline
        nonlocal cash_art_list, bline_list_list, outstand_list_list, pay_list_list, turnover_list
        return {"tot_cash": tot_cash, "tot_cash1": tot_cash1, "tot_ledger": tot_ledger, "tot_trans": tot_trans, "tot_compli": tot_compli, "tot_coupon": tot_coupon, "nt_cash": nt_cash, "nt_cash1": nt_cash1, "nt_ledger": nt_ledger, "nt_trans": nt_trans, "nt_compli": nt_compli, "nt_coupon": nt_coupon, "t_betrag": t_betrag, "t_foreign": t_foreign, "turnover": turnover_list}

    def daysale_list():

        nonlocal tot_debit, tot_cover, nt_debit, nt_cover, t_debit, t_cash, t_cash1, t_trans, t_ledger, t_coupon, t_compli, t_cover, anz_comp, val_comp, anz_coup, val_coup, serv_taxable, tot_cash, tot_cash1, tot_ledger, tot_trans, tot_compli, tot_coupon, nt_cash, nt_cash1, nt_ledger, nt_trans, nt_compli, nt_coupon, t_betrag, t_foreign, turnover_list, htparam, kellner, h_bill_line, h_bill, bill, res_line, h_artikel, artikel
        nonlocal bufparam, kellner1, tlist, h_bline


        nonlocal cash_art, bline_list, outstand_list, pay_list, turnover, bufparam, kellner1, tlist, h_bline
        nonlocal cash_art_list, bline_list_list, outstand_list_list, pay_list_list, turnover_list

        curr_s:int = 0
        billnr:int = 0
        dept:int = 0
        d_name:str = ""
        usr_nr:int = 0
        d_found:bool = "no"
        c_found:bool = "no"
        vat:decimal = 0
        service:decimal = 0
        netto:decimal = 0
        i:int = 0
        found:bool = no
        compli:bool = False
        guestname:str = ""
        bill_no:int = 0
        pos:int = 0
        Kellner1 = Kellner
        Tlist = Turnover
        H_bline = H_bill_line
        turnover_list.clear()
        pay_list_list.clear()
        outstand_list_list.clear()
        t_betrag = 0
        t_foreign = 0
        tot_cover = 0
        tot_debit = 0
        tot_cash1 = 0
        tot_cash = 0
        tot_trans = 0
        tot_ledger = 0
        tot_compli = 0
        tot_coupon = 0
        nt_cover = 0
        nt_debit = 0
        nt_cash1 = 0
        nt_cash = 0
        nt_trans = 0
        nt_compli = 0
        nt_coupon = 0

        for bline_list in query(bline_list_list, filters=(lambda bline_list :recid (kellner) == bline_list.bl_recid)):
            t_cover = 0
            t_debit = 0
            t_cash1 = 0
            t_cash = 0
            t_trans = 0
            t_ledger = 0
            t_compli = 0
            t_coupon = 0

            for h_bill in db_session.query(H_bill).filter(
                    (H_bill.flag == 0 and H_bill.saldo != 0 and H_bill.departement == bline_list.dept use_index dept1__ix)).all():
                outstand_list = Outstand_list()
                outstand_list_list.append(outstand_list)


                kellner1 = db_session.query(Kellner1).filter(
                        (Kellner1.kellner_nr == h_bill.kellner_nr and Kellner1.departement == h_bill.departement)).first()
                outstand_list.rechnr = h_bill.rechnr

                if kellner1:
                    outstand_list.name = kellner1.kellnername
                else:
                    outstand_list.name = to_string(h_bill.kellner_nr)

                for h_bill_line in db_session.query(H_bill_line).filter(
                        (H_bill_line.rechnr == h_bill.rechnr and H_bill_line.departement == bline_list.dept)).all():
                    outstand_list.saldo = outstand_list.saldo + h_bill_line.betrag
                    outstand_list.foreign = outstand_list.foreign + h_bill_line.fremdwbetrag

            for h_bill in db_session.query(H_bill).filter(
                    (H_bill.flag == 1 and H_bill.departement == bline_list.dept and H_bill.kellner_nr == kellner_nr use_index dept1__ix)).all():

                if shift == 0:

                    h_bill_line = db_session.query(H_bill_line).filter(
                            (H_bill_line.rechnr == h_bill.rechnr) &  (H_bill_line.bill_datum == from_date) &  (H_bill_line.departement == bline_list.dept)).first()
                else:

                    h_bill_line = db_session.query(H_bill_line).filter(
                            (H_bill_line.rechnr == h_bill.rechnr) &  (H_bill_line.bill_datum == from_date) &  (H_bill_line.departement == bline_list.dept) &  (H_bill_line.betriebsnr == shift)).first()

                if not h_bill_line:
                    found = False
                else:
                    found = True
                while None != h_bill_line:
                    found = True

                    turnover = query(turnover_list, filters=(lambda turnover :turnover.departement == bline_list.dept and turnover.kellner_nr == kellner_nr and turnover.rechnr == to_string(h_bill.rechnr)), first=True)

                    if not turnover:
                        pos = 0
                        bill_no = 0
                        guestname = ""

                        if shift == 0:

                            h_bline = db_session.query(H_bline).filter(
                                    (H_bline.rechnr == h_bill.rechnr) &  (H_bline.bill_datum == from_date) &  (H_bline.departement == bline_list.dept) &  (H_bline.artnr == 0)).first()
                        else:

                            h_bline = db_session.query(H_bline).filter(
                                    (H_bline.rechnr == h_bill.rechnr) &  (H_bline.bill_datum == from_date) &  (H_bline.departement == bline_list.dept) &  (H_bline.betriebsnr == shift) &  (H_bline.artnr == 0)).first()

                        if h_bline:
                            pos = 1 + get_index(h_bline.bezeich, "*")

                            if pos != 0:
                                bill_no = to_int(substring(h_bline.bezeich, pos - 1, (len(h_bline.bezeich) - pos + 1)))

                            if bill_no != 0:

                                bill = db_session.query(Bill).filter(
                                        (Bill.rechnr == bill_no)).first()

                                if bill:

                                    res_line = db_session.query(Res_line).filter(
                                            (Res_line.resnr == bill.resnr) &  (Res_line.reslinnr == bill.parent_nr)).first()

                                    if res_line:
                                        guestname = res_line.name
                        turnover = Turnover()
                        turnover_list.append(turnover)

                        turnover.departement = kellner.departement
                        turnover.deptname = bline_list.depart
                        turnover.kellner_nr = kellner_nr
                        turnover.name = kellnername
                        turnover.tischnr = h_bill.tischnr
                        turnover.belegung = h_bill.belegung
                        turnover.rechnr = to_string(h_bill.rechnr)
                        turnover.gname = guestname
                        tot_cover = tot_cover + h_bill.belegung
                        t_cover = t_cover + h_bill.belegung

                    if h_bill_line.artnr == 0:
                        turnover.r_transfer = turnover.r_transfer - h_bill_line.betrag
                        turnover.compli = False

                        pay_list = query(pay_list_list, filters=(lambda pay_list :pay_list.flag == 2), first=True)

                        if not pay_list:
                            pay_list = Pay_list()
                            pay_list_list.append(pay_list)

                            pay_list.flag = 2
                            pay_list.bezeich = "Room / Bill Transfer"
                        pay_list.saldo = pay_list.saldo - h_bill_line.betrag
                        t_betrag = t_betrag - h_bill_line.betrag
                        i = 0

                        if re.match(".*RmNo.*",h_bill_line.bezeich):

                            if num_entries(h_bill_line.bezeich, "*") > 1:
                                billnr = to_int(entry(1, h_bill_line.bezeich, "*"))

                        bill = db_session.query(Bill).filter(
                                (Bill.rechnr == billnr)).first()

                        if bill:
                            turnover.info = bill.zinr
                        turnover.t_credit = turnover.t_credit - h_bill_line.betrag
                        t_trans = t_trans - h_bill_line.betrag
                        tot_trans = tot_trans - h_bill_line.betrag
                    else:

                        h_artikel = db_session.query(H_artikel).filter(
                                (H_artikel.artnr == h_bill_line.artnr) &  (H_artikel.departement == bline_list.dept)).first()

                        if h_artikel:

                            if h_artikel.artart == 11 or h_artikel.artart == 12:

                                if h_artikel.artart == 11:

                                    pay_list = query(pay_list_list, filters=(lambda pay_list :pay_list.flag == 6), first=True)

                                    if not pay_list:
                                        pay_list = Pay_list()
                                        pay_list_list.append(pay_list)

                                        pay_list.flag = 6
                                        pay_list.compli = True
                                        pay_list.bezeich = "Compliment"
                                    pay_list.saldo = pay_list.saldo - h_bill_line.betrag

                                    if h_bill_line.betrag < 0:
                                        pay_list.person = pay_list.person + h_bill.belegung

                                    elif h_bill_line.betrag > 0:

                                        if h_bill.belegung > 0:
                                            pay_list.person = pay_list.person - h_bill.belegung
                                        else:
                                            pay_list.person = pay_list.person + h_bill.belegung
                                    t_betrag = t_betrag - h_bill_line.betrag
                                    t_compli = t_compli - h_bill_line.betrag
                                    tot_compli = tot_compli - h_bill_line.betrag
                                    anz_comp = anz_comp + 1
                                    val_comp = val_comp - h_bill_line.betrag
                                    turnover.comp = turnover.comp - h_bill_line.betrag

                                elif h_artikel.artart == 12:

                                    pay_list = query(pay_list_list, filters=(lambda pay_list :pay_list.flag == 7 and pay_list.bezeich == h_artikel.bezeich), first=True)

                                    if not pay_list:
                                        pay_list = Pay_list()
                                        pay_list_list.append(pay_list)

                                        pay_list.flag = 7
                                        pay_list.compli = True
                                        pay_list.bezeich = h_artikel.bezeich
                                    pay_list.saldo = pay_list.saldo - h_bill_line.betrag

                                    if h_bill_line.betrag < 0:
                                        pay_list.person = pay_list.person + h_bill.belegung

                                    elif h_bill_line.betrag > 0:

                                        if h_bill.belegung > 0:
                                            pay_list.person = pay_list.person - h_bill.belegung
                                        else:
                                            pay_list.person = pay_list.person + h_bill.belegung
                                    t_betrag = t_betrag - h_bill_line.betrag
                                    t_coupon = t_coupon - h_bill_line.betrag
                                    tot_coupon = tot_coupon - h_bill_line.betrag
                                    anz_coup = anz_coup + 1
                                    val_coup = val_coup - h_bill_line.betrag
                                    turnover.coupon = turnover.coupon - h_bill_line.betrag
                                turnover.compli = not turnover.compli
                                turnover.info = h_bill.bilname

                            elif h_artikel.artart == 0:
                                service = 0
                                vat = 0

                                artikel = db_session.query(Artikel).filter(
                                        (Artikel.departement == bline_list.dept) &  (Artikel.artnr == h_Artikel.artnrfront)).first()

                                if artikel:

                                    htparam = db_session.query(Htparam).filter(
                                            (Htparam.paramnr == artikel.service_code)).first()

                                    if htparam:
                                        service = 0.01 * htparam.fDECIMAL

                                    htparam = db_session.query(Htparam).filter(
                                            (Htparam.paramnr == artikel.mwst_code)).first()

                                    if htparam:

                                        if serv_taxable:
                                            vat = 0.01 * htparam.fDECIMAL * (1 + service)
                                        else:
                                            vat = 0.01 * htparam.fDECIMAL
                                netto = h_bill_line.betrag / (1 + vat + service)

                                if h_bill_line.fremdwbetrag != 0:
                                    exchg_rate = h_bill_line.betrag / h_bill_line.fremdwbetrag

                            if h_artikel.artart == 6:

                                artikel = db_session.query(Artikel).filter(
                                        (Artikel.artnr == h_Artikel.artnrfront and Artikel.departement == 0)).first()

                                if artikel:

                                    pay_list = query(pay_list_list, filters=(lambda pay_list :pay_list.flag == 1 and pay_list.bezeich == artikel.bezeich), first=True)

                                    if not pay_list:
                                        pay_list = Pay_list()
                                        pay_list_list.append(pay_list)

                                        pay_list.flag = 1
                                        pay_list.bezeich = artikel.bezeich

                                    if artikel.pricetab:
                                        pay_list.foreign = pay_list.foreign - h_bill_line.fremdwbetrag
                                        t_foreign = t_foreign - h_bill_line.fremdwbetrag
                                    else:
                                        pay_list.saldo = pay_list.saldo - h_bill_line.betrag
                                        t_betrag = t_betrag - h_bill_line.betrag

                                    if h_artikel.artnr == bufparam.finteger:
                                        turnover.p_cash1 = turnover.p_cash1 - h_bill_line.fremdwbetrag
                                        t_cash1 = t_cash1 - h_bill_line.fremdwbetrag
                                        tot_cash1 = tot_cash1 - h_bill_line.fremdwbetrag
                                    else:
                                        turnover.p_cash = turnover.p_cash - h_bill_line.betrag
                                        t_cash = t_cash - h_bill_line.betrag
                                        tot_cash = tot_cash - h_bill_line.betrag
                                    turnover.t_credit = turnover.t_credit - h_bill_line.betrag

                                    cash_art = query(cash_art_list, filters=(lambda cash_art :cash_art.artnr == artikel.artnr and cash_art.usrnr == kellner_nr), first=True)

                                    if not cash_art:
                                        cash_art = Cash_art()
                                        cash_art_list.append(cash_art)

                                        cash_art.artnr = artikel.artnr
                                        cash_art.usrnr = kellner_nr
                                        cash_art.usrnm = kellnername
                                        cash_art.bezeich = artikel.bezeich


                                    cash_art.amount = cash_art.amount - h_bill_line.betrag

                            if h_artikel.artart == 6 and h_artikel.artart == 7:

                                artikel = db_session.query(Artikel).filter(
                                        (Artikel.artnr == h_Artikel.artnrfront and Artikel.departement == 0)).first()

                                if artikel:

                                    pay_list = query(pay_list_list, filters=(lambda pay_list :pay_list.flag == 1 and pay_list.bezeich == artikel.bezeich), first=True)

                                    if not pay_list:
                                        pay_list = Pay_list()
                                        pay_list_list.append(pay_list)

                                        pay_list.flag = 1
                                        pay_list.bezeich = artikel.bezeich

                                    if artikel.pricetab:
                                        pay_list.foreign = pay_list.foreign - h_bill_line.fremdwbetrag
                                        t_foreign = t_foreign - h_bill_line.fremdwbetrag
                                    else:
                                        pay_list.saldo = pay_list.saldo - h_bill_line.betrag
                                        t_betrag = t_betrag - h_bill_line.betrag

                                    if h_artikel.artnr == bufparam.finteger:
                                        turnover.p_cash1 = turnover.p_cash1 - h_bill_line.fremdwbetrag
                                        t_cash1 = t_cash1 - h_bill_line.fremdwbetrag
                                        tot_cash1 = tot_cash1 - h_bill_line.fremdwbetrag
                                    else:
                                        turnover.p_cash = turnover.p_cash - h_bill_line.betrag
                                        t_cash = t_cash - h_bill_line.betrag
                                        tot_cash = tot_cash - h_bill_line.betrag
                                    turnover.t_credit = turnover.t_credit - h_bill_line.betrag

                                    cash_art = query(cash_art_list, filters=(lambda cash_art :cash_art.artnr == artikel.artnr and cash_art.usrnr == kellner_nr), first=True)

                                    if not cash_art:
                                        cash_art = Cash_art()
                                        cash_art_list.append(cash_art)

                                        cash_art.artnr = artikel.artnr
                                        cash_art.usrnr = kellner_nr
                                        cash_art.usrnm = kellnername
                                        cash_art.bezeich = artikel.bezeich


                                    cash_art.amount = cash_art.amount - h_bill_line.betrag

                            elif h_artikel.artart == 7 or h_artikel.artart == 2:

                                artikel = db_session.query(Artikel).filter(
                                        (Artikel.artnr == h_Artikel.artnrfront and Artikel.departement == 0)).first()

                                if artikel:

                                    if h_artikel.artart == 7:

                                        pay_list = query(pay_list_list, filters=(lambda pay_list :pay_list.flag == 3), first=True)

                                        if not pay_list:
                                            pay_list = Pay_list()
                                            pay_list_list.append(pay_list)

                                            pay_list.flag = 3
                                            pay_list.bezeich = "Credit Card"

                                    elif h_artikel.artart == 2:

                                        pay_list = query(pay_list_list, filters=(lambda pay_list :pay_list.flag == 5), first=True)

                                        if not pay_list:
                                            pay_list = Pay_list()
                                            pay_list_list.append(pay_list)

                                            pay_list.flag = 5
                                            pay_list.bezeich = "City- & Employee Ledger"
                                    pay_list.saldo = pay_list.saldo - h_bill_line.betrag
                                    t_betrag = t_betrag - h_bill_line.betrag

                                    if len(h_bill_line.bezeich) > len(h_artikel.bezeich):
                                        turnover.info = substring(h_bill_line.bezeich, (len(h_artikel.bezeich) + 1) - 1, (len(h_bill_line.bezeich) - len(h_artikel.bezeich)))
                                    else:
                                        turnover.INFO = h_bill.bilname
                                    turnover.artnr = artikel.artnr
                                    turnover.c_ledger = turnover.c_ledger - h_bill_line.betrag
                                    turnover.t_credit = turnover.t_credit - h_bill_line.betrag
                                    t_ledger = t_ledger - h_bill_line.betrag
                                    tot_ledger = tot_ledger - h_bill_line.betrag

                    if shift == 0:

                        h_bill_line = db_session.query(H_bill_line).filter(
                                (H_bill_line.rechnr == h_bill.rechnr) &  (H_bill_line.bill_datum == from_date) &  (H_bill_line.departement == bline_list.dept)).first()
                    else:

                        h_bill_line = db_session.query(H_bill_line).filter(
                                (H_bill_line.rechnr == h_bill.rechnr) &  (H_bill_line.bill_datum == from_date) &  (H_bill_line.departement == bline_list.dept) &  (H_bill_line.betriebsnr == shift)).first()

            tlist = query(tlist_list, filters=(lambda tlist :tlist.name == kellnername and tlist.departement == bline_list.dept), first=True)

            if tlist:
                turnover = Turnover()
                turnover_list.append(turnover)

                turnover.departement = bline_list.dept
                turnover.deptname = bline_list.depart
                turnover.name = kellnername
                turnover.rechnr = kellnername + " TOTAL"
                turnover.belegung = t_cover
                turnover.t_debit = t_debit
                turnover.p_cash = t_cash
                turnover.p_cash1 = t_cash1
                turnover.r_transfer = t_trans
                turnover.c_ledger = t_ledger
                turnover.comp = t_compli
                turnover.coupon = t_coupon
                turnover.flag = 1
        turnover = Turnover()
        turnover_list.append(turnover)

        turnover.rechnr = "G_TOTAL"
        turnover.name = "ZZZ"
        turnover.belegung = tot_cover
        turnover.t_debit = tot_debit
        turnover.p_cash = tot_cash
        turnover.p_cash1 = tot_cash1
        turnover.r_transfer = tot_trans
        turnover.c_ledger = tot_ledger
        turnover.comp = tot_compli
        turnover.coupon = tot_coupon
        turnover.flag = 2
        turnover = Turnover()
        turnover_list.append(turnover)

        turnover.name = "ZZZ"
        turnover.rechnr = "R_TOTAL"
        turnover.flag = 3

        for tlist in query(tlist_list, filters=(lambda tlist :tlist.flag == 0)):
            turnover.belegung = turnover.belegung + tlist.belegung
            turnover.comp = turnover.comp + tlist.comp
            turnover.coupon = turnover.coupon + tlist.coupon
            turnover.t_debit = turnover.t_debit + tlist.t_debit
            turnover.p_cash = turnover.p_cash + tlist.p_cash
            turnover.p_cash1 = turnover.p_cash1 + tlist.p_cash1
            turnover.r_transfer = turnover.r_transfer + tlist.r_transfer
            turnover.c_ledger = turnover.c_ledger + tlist.c_ledger
        nt_cover = turnover.belegung
        nt_compli = turnover.comp
        nt_coupon = turnover.coupon
        nt_debit = turnover.t_debit
        nt_cash = turnover.p_cash
        nt_cash1 = turnover.p_cash1
        nt_trans = turnover.r_transfer
        nt_ledger = turnover.c_ledger

    bufparam = db_session.query(Bufparam).filter(
            (Bufparam.paramnr == 1001)).first()
    daysale_list()

    return generate_output()