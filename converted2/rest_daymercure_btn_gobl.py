#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, Kellner, H_bill_line, H_bill, Bill, Res_line, H_artikel, Artikel

bline_list_data, Bline_list = create_model("Bline_list", {"selected":bool, "name":string, "depart":string, "dept":int, "knr":int, "bl_recid":int})

def rest_daymercure_btn_gobl(bline_list_data:[Bline_list], shift:int, from_date:date, exchg_rate:Decimal):

    prepare_cache ([Htparam, Kellner, H_bill_line, Bill, Res_line, H_artikel, Artikel])

    tot_debit:Decimal = to_decimal("0.0")
    tot_cover:int = 0
    nt_debit:Decimal = to_decimal("0.0")
    nt_cover:int = 0
    t_debit:Decimal = to_decimal("0.0")
    t_cash:Decimal = to_decimal("0.0")
    t_cash1:Decimal = to_decimal("0.0")
    t_trans:Decimal = to_decimal("0.0")
    t_ledger:Decimal = to_decimal("0.0")
    t_coupon:Decimal = to_decimal("0.0")
    t_compli:Decimal = to_decimal("0.0")
    t_cover:int = 0
    anz_comp:int = 0
    val_comp:Decimal = to_decimal("0.0")
    anz_coup:int = 0
    val_coup:Decimal = to_decimal("0.0")
    serv_taxable:bool = False
    tot_cash = to_decimal("0.0")
    tot_cash1 = to_decimal("0.0")
    tot_ledger = to_decimal("0.0")
    tot_trans = to_decimal("0.0")
    tot_compli = to_decimal("0.0")
    tot_coupon = to_decimal("0.0")
    nt_cash = to_decimal("0.0")
    nt_cash1 = to_decimal("0.0")
    nt_ledger = to_decimal("0.0")
    nt_trans = to_decimal("0.0")
    nt_compli = to_decimal("0.0")
    nt_coupon = to_decimal("0.0")
    t_betrag = to_decimal("0.0")
    t_foreign = to_decimal("0.0")
    turnover_data = []
    htparam = kellner = h_bill_line = h_bill = bill = res_line = h_artikel = artikel = None

    cash_art = bline_list = outstand_list = pay_list = turnover = bufparam = tlist = None

    cash_art_data, Cash_art = create_model("Cash_art", {"sortnr":int, "usrnr":int, "usrnm":string, "artnr":int, "bezeich":string, "amount":Decimal})
    outstand_list_data, Outstand_list = create_model("Outstand_list", {"name":string, "rechnr":int, "foreign":Decimal, "saldo":Decimal})
    pay_list_data, Pay_list = create_model("Pay_list", {"compli":bool, "person":int, "flag":int, "bezeich":string, "artnr":int, "rechnr":int, "foreign":Decimal, "saldo":Decimal})
    turnover_data, Turnover = create_model("Turnover", {"departement":int, "deptname":string, "kellner_nr":int, "name":string, "tischnr":int, "rechnr":string, "belegung":int, "artnr":int, "info":string, "t_debit":Decimal, "t_credit":Decimal, "p_cash":Decimal, "p_cash1":Decimal, "r_transfer":Decimal, "c_ledger":Decimal, "compli":bool, "flag":int, "coupon":Decimal, "comp":Decimal, "gname":string})

    Bufparam = create_buffer("Bufparam",Htparam)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal tot_debit, tot_cover, nt_debit, nt_cover, t_debit, t_cash, t_cash1, t_trans, t_ledger, t_coupon, t_compli, t_cover, anz_comp, val_comp, anz_coup, val_coup, serv_taxable, tot_cash, tot_cash1, tot_ledger, tot_trans, tot_compli, tot_coupon, nt_cash, nt_cash1, nt_ledger, nt_trans, nt_compli, nt_coupon, t_betrag, t_foreign, turnover_data, htparam, kellner, h_bill_line, h_bill, bill, res_line, h_artikel, artikel
        nonlocal shift, from_date, exchg_rate
        nonlocal bufparam


        nonlocal cash_art, bline_list, outstand_list, pay_list, turnover, bufparam, tlist
        nonlocal cash_art_data, outstand_list_data, pay_list_data, turnover_data

        return {"tot_cash": tot_cash, "tot_cash1": tot_cash1, "tot_ledger": tot_ledger, "tot_trans": tot_trans, "tot_compli": tot_compli, "tot_coupon": tot_coupon, "nt_cash": nt_cash, "nt_cash1": nt_cash1, "nt_ledger": nt_ledger, "nt_trans": nt_trans, "nt_compli": nt_compli, "nt_coupon": nt_coupon, "t_betrag": t_betrag, "t_foreign": t_foreign, "turnover": turnover_data}

    def daysale_list():

        nonlocal tot_debit, tot_cover, nt_debit, nt_cover, t_debit, t_cash, t_cash1, t_trans, t_ledger, t_coupon, t_compli, t_cover, anz_comp, val_comp, anz_coup, val_coup, serv_taxable, tot_cash, tot_cash1, tot_ledger, tot_trans, tot_compli, tot_coupon, nt_cash, nt_cash1, nt_ledger, nt_trans, nt_compli, nt_coupon, t_betrag, t_foreign, turnover_data, htparam, kellner, h_bill_line, h_bill, bill, res_line, h_artikel, artikel
        nonlocal shift, from_date, exchg_rate
        nonlocal bufparam


        nonlocal cash_art, bline_list, outstand_list, pay_list, turnover, bufparam, tlist
        nonlocal cash_art_data, outstand_list_data, pay_list_data, turnover_data

        curr_s:int = 0
        billnr:int = 0
        dept:int = 1
        d_name:string = ""
        usr_nr:int = 0
        d_found:bool = False
        c_found:bool = False
        vat:Decimal = to_decimal("0.0")
        service:Decimal = to_decimal("0.0")
        netto:Decimal = to_decimal("0.0")
        i:int = 0
        found:bool = False
        compli:bool = False
        guestname:string = ""
        bill_no:int = 0
        pos:int = 0
        kellner1 = None
        h_bline = None
        Kellner1 =  create_buffer("Kellner1",Kellner)
        Tlist = Turnover
        tlist_data = turnover_data
        H_bline =  create_buffer("H_bline",H_bill_line)
        turnover_data.clear()
        pay_list_data.clear()
        outstand_list_data.clear()
        t_betrag =  to_decimal("0")
        t_foreign =  to_decimal("0")
        tot_cover = 0
        tot_debit =  to_decimal("0")
        tot_cash1 =  to_decimal("0")
        tot_cash =  to_decimal("0")
        tot_trans =  to_decimal("0")
        tot_ledger =  to_decimal("0")
        tot_compli =  to_decimal("0")
        tot_coupon =  to_decimal("0")
        nt_cover = 0
        nt_debit =  to_decimal("0")
        nt_cash1 =  to_decimal("0")
        nt_cash =  to_decimal("0")
        nt_trans =  to_decimal("0")
        nt_compli =  to_decimal("0")
        nt_coupon =  to_decimal("0")

        kellner_obj_list = {}
        for kellner in db_session.query(Kellner).filter(
                 (Kellner._recid.in_(list(set([bline_list.bl_recid for bline_list in bline_list_data if bline_list.selected]))))).order_by(Kellner.departement, Kellner.kellnername).all():
            if kellner_obj_list.get(kellner._recid):
                continue
            else:
                kellner_obj_list[kellner._recid] = True

            bline_list = query(bline_list_data, (lambda bline_list: (kellner._recid == bline_list.bl_recid)), first=True)
            t_cover = 0
            t_debit =  to_decimal("0")
            t_cash1 =  to_decimal("0")
            t_cash =  to_decimal("0")
            t_trans =  to_decimal("0")
            t_ledger =  to_decimal("0")
            t_compli =  to_decimal("0")
            t_coupon =  to_decimal("0")

            for h_bill in db_session.query(H_bill).filter(
                     (H_bill.flag == 0) & (H_bill.saldo != 0) & (H_bill.departement == bline_list.dept)).order_by(H_bill._recid).all():
                outstand_list = Outstand_list()
                outstand_list_data.append(outstand_list)


                kellner1 = get_cache (Kellner, {"kellner_nr": [(eq, h_bill.kellner_nr)],"departement": [(eq, h_bill.departement)]})
                outstand_list.rechnr = h_bill.rechnr

                if kellner1:
                    outstand_list.name = kellner1.kellnername
                else:
                    outstand_list.name = to_string(h_bill.kellner_nr)

                for h_bill_line in db_session.query(H_bill_line).filter(
                         (H_bill_line.rechnr == h_bill.rechnr) & (H_bill_line.departement == bline_list.dept)).order_by(H_bill_line._recid).all():
                    outstand_list.saldo =  to_decimal(outstand_list.saldo) + to_decimal(h_bill_line.betrag)
                    outstand_list.foreign =  to_decimal(outstand_list.foreign) + to_decimal(h_bill_line.fremdwbetrag)

            for h_bill in db_session.query(H_bill).filter(
                     (H_bill.flag == 1) & (H_bill.departement == bline_list.dept) & (H_bill.kellner_nr == kellner.kellner_nr)).order_by(H_bill._recid).all():

                if shift == 0:

                    h_bill_line = get_cache (H_bill_line, {"rechnr": [(eq, h_bill.rechnr)],"bill_datum": [(eq, from_date)],"departement": [(eq, bline_list.dept)]})
                else:

                    h_bill_line = get_cache (H_bill_line, {"rechnr": [(eq, h_bill.rechnr)],"bill_datum": [(eq, from_date)],"departement": [(eq, bline_list.dept)],"betriebsnr": [(eq, shift)]})

                if not h_bill_line:
                    found = False
                else:
                    found = True
                while None != h_bill_line:
                    found = True

                    turnover = query(turnover_data, filters=(lambda turnover: turnover.departement == bline_list.dept and turnover.kellner_nr == kellner.kellner_nr and turnover.rechnr == to_string(h_bill.rechnr)), first=True)

                    if not turnover:
                        pos = 0
                        bill_no = 0
                        guestname = ""

                        if shift == 0:

                            h_bline = get_cache (H_bill_line, {"rechnr": [(eq, h_bill.rechnr)],"bill_datum": [(eq, from_date)],"departement": [(eq, bline_list.dept)],"artnr": [(eq, 0)]})
                        else:

                            h_bline = get_cache (H_bill_line, {"rechnr": [(eq, h_bill.rechnr)],"bill_datum": [(eq, from_date)],"departement": [(eq, bline_list.dept)],"betriebsnr": [(eq, shift)],"artnr": [(eq, 0)]})

                        if h_bline:
                            pos = get_index(h_bline.bezeich, "*")

                            if pos != 0:
                                bill_no = to_int(substring(h_bline.bezeich, pos - 1, (length(h_bline.bezeich) - pos + 1)))

                            if bill_no != 0:

                                bill = get_cache (Bill, {"rechnr": [(eq, bill_no)]})

                                if bill:

                                    res_line = get_cache (Res_line, {"resnr": [(eq, bill.resnr)],"reslinnr": [(eq, bill.parent_nr)]})

                                    if res_line:
                                        guestname = res_line.name
                        turnover = Turnover()
                        turnover_data.append(turnover)

                        turnover.departement = kellner.departement
                        turnover.deptname = bline_list.depart
                        turnover.kellner_nr = kellner.kellner_nr
                        turnover.name = kellner.kellnername
                        turnover.tischnr = h_bill.tischnr
                        turnover.belegung = h_bill.belegung
                        turnover.rechnr = to_string(h_bill.rechnr)
                        turnover.gname = guestname
                        tot_cover = tot_cover + h_bill.belegung
                        t_cover = t_cover + h_bill.belegung

                    if h_bill_line.artnr == 0:
                        turnover.r_transfer =  to_decimal(turnover.r_transfer) - to_decimal(h_bill_line.betrag)
                        turnover.compli = False

                        pay_list = query(pay_list_data, filters=(lambda pay_list: pay_list.flag == 2), first=True)

                        if not pay_list:
                            pay_list = Pay_list()
                            pay_list_data.append(pay_list)

                            pay_list.flag = 2
                            pay_list.bezeich = "Room / Bill Transfer"
                        pay_list.saldo =  to_decimal(pay_list.saldo) - to_decimal(h_bill_line.betrag)
                        t_betrag =  to_decimal(t_betrag) - to_decimal(h_bill_line.betrag)
                        i = 0

                        if matches(h_bill_line.bezeich,r"*RmNo*"):

                            if num_entries(h_bill_line.bezeich, "*") > 1:
                                billnr = to_int(entry(1, h_bill_line.bezeich, "*"))

                        bill = get_cache (Bill, {"rechnr": [(eq, billnr)]})

                        if bill:
                            turnover.info = bill.zinr
                        turnover.t_credit =  to_decimal(turnover.t_credit) - to_decimal(h_bill_line.betrag)
                        t_trans =  to_decimal(t_trans) - to_decimal(h_bill_line.betrag)
                        tot_trans =  to_decimal(tot_trans) - to_decimal(h_bill_line.betrag)
                    else:

                        h_artikel = get_cache (H_artikel, {"artnr": [(eq, h_bill_line.artnr)],"departement": [(eq, bline_list.dept)]})

                        if h_artikel:

                            if h_artikel.artart == 11 or h_artikel.artart == 12:

                                if h_artikel.artart == 11:

                                    pay_list = query(pay_list_data, filters=(lambda pay_list: pay_list.flag == 6), first=True)

                                    if not pay_list:
                                        pay_list = Pay_list()
                                        pay_list_data.append(pay_list)

                                        pay_list.flag = 6
                                        pay_list.compli = True
                                        pay_list.bezeich = "Compliment"
                                    pay_list.saldo =  to_decimal(pay_list.saldo) - to_decimal(h_bill_line.betrag)

                                    if h_bill_line.betrag < 0:
                                        pay_list.person = pay_list.person + h_bill.belegung

                                    elif h_bill_line.betrag > 0:

                                        if h_bill.belegung > 0:
                                            pay_list.person = pay_list.person - h_bill.belegung
                                        else:
                                            pay_list.person = pay_list.person + h_bill.belegung
                                    t_betrag =  to_decimal(t_betrag) - to_decimal(h_bill_line.betrag)
                                    t_compli =  to_decimal(t_compli) - to_decimal(h_bill_line.betrag)
                                    tot_compli =  to_decimal(tot_compli) - to_decimal(h_bill_line.betrag)
                                    anz_comp = anz_comp + 1
                                    val_comp =  to_decimal(val_comp) - to_decimal(h_bill_line.betrag)
                                    turnover.comp = turnover.comp - h_bill_line.betrag

                                elif h_artikel.artart == 12:

                                    pay_list = query(pay_list_data, filters=(lambda pay_list: pay_list.flag == 7 and pay_list.bezeich == h_artikel.bezeich), first=True)

                                    if not pay_list:
                                        pay_list = Pay_list()
                                        pay_list_data.append(pay_list)

                                        pay_list.flag = 7
                                        pay_list.compli = True
                                        pay_list.bezeich = h_artikel.bezeich
                                    pay_list.saldo =  to_decimal(pay_list.saldo) - to_decimal(h_bill_line.betrag)

                                    if h_bill_line.betrag < 0:
                                        pay_list.person = pay_list.person + h_bill.belegung

                                    elif h_bill_line.betrag > 0:

                                        if h_bill.belegung > 0:
                                            pay_list.person = pay_list.person - h_bill.belegung
                                        else:
                                            pay_list.person = pay_list.person + h_bill.belegung
                                    t_betrag =  to_decimal(t_betrag) - to_decimal(h_bill_line.betrag)
                                    t_coupon =  to_decimal(t_coupon) - to_decimal(h_bill_line.betrag)
                                    tot_coupon =  to_decimal(tot_coupon) - to_decimal(h_bill_line.betrag)
                                    anz_coup = anz_coup + 1
                                    val_coup =  to_decimal(val_coup) - to_decimal(h_bill_line.betrag)
                                    turnover.coupon =  to_decimal(turnover.coupon) - to_decimal(h_bill_line.betrag)
                                turnover.compli = not turnover.compli
                                turnover.info = h_bill.bilname

                            elif h_artikel.artart == 0:
                                service =  to_decimal("0")
                                vat =  to_decimal("0")

                                artikel = get_cache (Artikel, {"departement": [(eq, bline_list.dept)],"artnr": [(eq, h_artikel.artnrfront)]})

                                if artikel:

                                    htparam = get_cache (Htparam, {"paramnr": [(eq, artikel.service_code)]})

                                    if htparam:
                                        service =  to_decimal(0.01) * to_decimal(htparam.fDECIMAL)

                                    htparam = get_cache (Htparam, {"paramnr": [(eq, artikel.mwst_code)]})

                                    if htparam:

                                        if serv_taxable:
                                            vat =  to_decimal(0.01) * to_decimal(htparam.fDECIMAL) * to_decimal((1) + to_decimal(service))
                                        else:
                                            vat =  to_decimal(0.01) * to_decimal(htparam.fDECIMAL)
                                netto =  to_decimal(h_bill_line.betrag) / to_decimal((1) + to_decimal(vat) + to_decimal(service))

                                if h_bill_line.fremdwbetrag != 0:
                                    exchg_rate =  to_decimal(h_bill_line.betrag) / to_decimal(h_bill_line.fremdwbetrag)

                            if h_artikel.artart == 6:

                                artikel = get_cache (Artikel, {"artnr": [(eq, h_artikel.artnrfront)],"departement": [(eq, 0)]})

                                if artikel:

                                    pay_list = query(pay_list_data, filters=(lambda pay_list: pay_list.flag == 1 and pay_list.bezeich == artikel.bezeich), first=True)

                                    if not pay_list:
                                        pay_list = Pay_list()
                                        pay_list_data.append(pay_list)

                                        pay_list.flag = 1
                                        pay_list.bezeich = artikel.bezeich

                                    if artikel.pricetab:
                                        pay_list.foreign =  to_decimal(pay_list.foreign) - to_decimal(h_bill_line.fremdwbetrag)
                                        t_foreign =  to_decimal(t_foreign) - to_decimal(h_bill_line.fremdwbetrag)
                                    else:
                                        pay_list.saldo =  to_decimal(pay_list.saldo) - to_decimal(h_bill_line.betrag)
                                        t_betrag =  to_decimal(t_betrag) - to_decimal(h_bill_line.betrag)

                                    if h_artikel.artnr == bufparam.finteger:
                                        turnover.p_cash1 =  to_decimal(turnover.p_cash1) - to_decimal(h_bill_line.betrag)
                                        t_cash1 =  to_decimal(t_cash1) - to_decimal(h_bill_line.betrag)
                                        tot_cash1 =  to_decimal(tot_cash1) - to_decimal(h_bill_line.betrag)
                                    else:
                                        turnover.p_cash =  to_decimal(turnover.p_cash) - to_decimal(h_bill_line.betrag)
                                        t_cash =  to_decimal(t_cash) - to_decimal(h_bill_line.betrag)
                                        tot_cash =  to_decimal(tot_cash) - to_decimal(h_bill_line.betrag)
                                    turnover.t_credit =  to_decimal(turnover.t_credit) - to_decimal(h_bill_line.betrag)

                                    cash_art = query(cash_art_data, filters=(lambda cash_art: cash_art.artnr == artikel.artnr and cash_art.usrnr == kellner.kellner_nr), first=True)

                                    if not cash_art:
                                        cash_art = Cash_art()
                                        cash_art_data.append(cash_art)

                                        cash_art.artnr = artikel.artnr
                                        cash_art.usrnr = kellner.kellner_nr
                                        cash_art.usrnm = kellner.kellnername
                                        cash_art.bezeich = artikel.bezeich


                                    cash_art.amount =  to_decimal(cash_art.amount) - to_decimal(h_bill_line.betrag)

                            if h_artikel.artart == 6 and h_artikel.artart == 7:

                                artikel = get_cache (Artikel, {"artnr": [(eq, h_artikel.artnrfront)],"departement": [(eq, 0)]})

                                if artikel:

                                    pay_list = query(pay_list_data, filters=(lambda pay_list: pay_list.flag == 1 and pay_list.bezeich == artikel.bezeich), first=True)

                                    if not pay_list:
                                        pay_list = Pay_list()
                                        pay_list_data.append(pay_list)

                                        pay_list.flag = 1
                                        pay_list.bezeich = artikel.bezeich

                                    if artikel.pricetab:
                                        pay_list.foreign =  to_decimal(pay_list.foreign) - to_decimal(h_bill_line.fremdwbetrag)
                                        t_foreign =  to_decimal(t_foreign) - to_decimal(h_bill_line.fremdwbetrag)
                                    else:
                                        pay_list.saldo =  to_decimal(pay_list.saldo) - to_decimal(h_bill_line.betrag)
                                        t_betrag =  to_decimal(t_betrag) - to_decimal(h_bill_line.betrag)

                                    if h_artikel.artnr == bufparam.finteger:
                                        turnover.p_cash1 =  to_decimal(turnover.p_cash1) - to_decimal(h_bill_line.betrag)
                                        t_cash1 =  to_decimal(t_cash1) - to_decimal(h_bill_line.betrag)
                                        tot_cash1 =  to_decimal(tot_cash1) - to_decimal(h_bill_line.betrag)
                                    else:
                                        turnover.p_cash =  to_decimal(turnover.p_cash) - to_decimal(h_bill_line.betrag)
                                        t_cash =  to_decimal(t_cash) - to_decimal(h_bill_line.betrag)
                                        tot_cash =  to_decimal(tot_cash) - to_decimal(h_bill_line.betrag)
                                    turnover.t_credit =  to_decimal(turnover.t_credit) - to_decimal(h_bill_line.betrag)

                                    cash_art = query(cash_art_data, filters=(lambda cash_art: cash_art.artnr == artikel.artnr and cash_art.usrnr == kellner.kellner_nr), first=True)

                                    if not cash_art:
                                        cash_art = Cash_art()
                                        cash_art_data.append(cash_art)

                                        cash_art.artnr = artikel.artnr
                                        cash_art.usrnr = kellner.kellner_nr
                                        cash_art.usrnm = kellner.kellnername
                                        cash_art.bezeich = artikel.bezeich


                                    cash_art.amount =  to_decimal(cash_art.amount) - to_decimal(h_bill_line.betrag)

                            elif h_artikel.artart == 7 or h_artikel.artart == 2:

                                artikel = get_cache (Artikel, {"artnr": [(eq, h_artikel.artnrfront)],"departement": [(eq, 0)]})

                                if artikel:

                                    if h_artikel.artart == 7:

                                        pay_list = query(pay_list_data, filters=(lambda pay_list: pay_list.flag == 3), first=True)

                                        if not pay_list:
                                            pay_list = Pay_list()
                                            pay_list_data.append(pay_list)

                                            pay_list.flag = 3
                                            pay_list.bezeich = "Credit Card"

                                    elif h_artikel.artart == 2:

                                        pay_list = query(pay_list_data, filters=(lambda pay_list: pay_list.flag == 5), first=True)

                                        if not pay_list:
                                            pay_list = Pay_list()
                                            pay_list_data.append(pay_list)

                                            pay_list.flag = 5
                                            pay_list.bezeich = "City- & Employee Ledger"
                                    pay_list.saldo =  to_decimal(pay_list.saldo) - to_decimal(h_bill_line.betrag)
                                    t_betrag =  to_decimal(t_betrag) - to_decimal(h_bill_line.betrag)

                                    if length(h_bill_line.bezeich) > length(h_artikel.bezeich):
                                        turnover.info = substring(h_bill_line.bezeich, (length(h_artikel.bezeich) + 1) - 1, (length(h_bill_line.bezeich) - length(h_artikel.bezeich)))
                                    else:
                                        turnover.info = h_bill.bilname
                                    turnover.artnr = artikel.artnr
                                    turnover.c_ledger =  to_decimal(turnover.c_ledger) - to_decimal(h_bill_line.betrag)
                                    turnover.t_credit =  to_decimal(turnover.t_credit) - to_decimal(h_bill_line.betrag)
                                    t_ledger =  to_decimal(t_ledger) - to_decimal(h_bill_line.betrag)
                                    tot_ledger =  to_decimal(tot_ledger) - to_decimal(h_bill_line.betrag)

                    if shift == 0:

                        curr_recid = h_bill_line._recid
                        h_bill_line = db_session.query(H_bill_line).filter(
                                 (H_bill_line.rechnr == h_bill.rechnr) & (H_bill_line.bill_datum == from_date) & (H_bill_line.departement == bline_list.dept) & (H_bill_line._recid > curr_recid)).first()
                    else:

                        curr_recid = h_bill_line._recid
                        h_bill_line = db_session.query(H_bill_line).filter(
                                 (H_bill_line.rechnr == h_bill.rechnr) & (H_bill_line.bill_datum == from_date) & (H_bill_line.departement == bline_list.dept) & (H_bill_line.betriebsnr == shift) & (H_bill_line._recid > curr_recid)).first()

            tlist = query(tlist_data, filters=(lambda tlist: tlist.name == kellner.kellnername and tlist.departement == bline_list.dept), first=True)

            if tlist:
                turnover = Turnover()
                turnover_data.append(turnover)

                turnover.departement = bline_list.dept
                turnover.deptname = bline_list.depart
                turnover.name = kellner.kellnername
                turnover.rechnr = kellner.kellnername + " TOTAL"
                turnover.belegung = t_cover
                turnover.t_debit =  to_decimal(t_debit)
                turnover.p_cash =  to_decimal(t_cash)
                turnover.p_cash1 =  to_decimal(t_cash1)
                turnover.r_transfer =  to_decimal(t_trans)
                turnover.c_ledger =  to_decimal(t_ledger)
                turnover.comp = t_compli
                turnover.coupon =  to_decimal(t_coupon)
                turnover.flag = 1
        turnover = Turnover()
        turnover_data.append(turnover)

        turnover.rechnr = "G-TOTAL"
        turnover.name = "ZZZ"
        turnover.belegung = tot_cover
        turnover.t_debit =  to_decimal(tot_debit)
        turnover.p_cash =  to_decimal(tot_cash)
        turnover.p_cash1 =  to_decimal(tot_cash1)
        turnover.r_transfer =  to_decimal(tot_trans)
        turnover.c_ledger =  to_decimal(tot_ledger)
        turnover.comp = tot_compli
        turnover.coupon =  to_decimal(tot_coupon)
        turnover.flag = 2
        turnover = Turnover()
        turnover_data.append(turnover)

        turnover.name = "ZZZ"
        turnover.rechnr = "R-TOTAL"
        turnover.flag = 3

        for tlist in query(tlist_data, filters=(lambda tlist: tlist.flag == 0)):
            turnover.belegung = turnover.belegung + tlist.belegung
            turnover.comp = turnover.comp + tlist.comp
            turnover.coupon =  to_decimal(turnover.coupon) + to_decimal(tlist.coupon)
            turnover.t_debit =  to_decimal(turnover.t_debit) + to_decimal(tlist.t_debit)
            turnover.p_cash =  to_decimal(turnover.p_cash) + to_decimal(tlist.p_cash)
            turnover.p_cash1 =  to_decimal(turnover.p_cash1) + to_decimal(tlist.p_cash1)
            turnover.r_transfer =  to_decimal(turnover.r_transfer) + to_decimal(tlist.r_transfer)
            turnover.c_ledger =  to_decimal(turnover.c_ledger) + to_decimal(tlist.c_ledger)
        nt_cover = turnover.belegung
        nt_compli =  to_decimal(turnover.comp)
        nt_coupon =  to_decimal(turnover.coupon)
        nt_debit =  to_decimal(turnover.t_debit)
        nt_cash =  to_decimal(turnover.p_cash)
        nt_cash1 =  to_decimal(turnover.p_cash1)
        nt_trans =  to_decimal(turnover.r_transfer)
        nt_ledger =  to_decimal(turnover.c_ledger)


    bufparam = get_cache (Htparam, {"paramnr": [(eq, 1001)]})
    daysale_list()

    return generate_output()