from functions.additional_functions import *
import decimal
from datetime import date
from models import Bediener, Artikel, Billjournal, Bill, Res_line, Waehrung

bline_list_list, Bline_list = create_model("Bline_list", {"flag":int, "userinit":str, "selected":bool, "name":str, "bl_recid":int})

def fo_daysale_daysale_list1bl(bline_list_list:[Bline_list], pvilanguage:int, shift:int, from_date:date, to_date:date):
    curr_shift = None
    nt_cash = None
    nt_fcash = None
    nt_ledger = to_decimal("0.0")
    nt_credit = None
    turnover_list = []
    summary1_list = []
    cash_art_list = []
    tot_cash:decimal = to_decimal("0.0")
    tot_fcash:decimal = to_decimal("0.0")
    tot_ledger:decimal = to_decimal("0.0")
    tot_credit:decimal = to_decimal("0.0")
    tot_amount:List[decimal] = create_empty_list(6,to_decimal("0"))
    nt_amount:List[decimal] = create_empty_list(6,to_decimal("0"))
    lvcarea:str = "FO-daysale"
    bediener = artikel = billjournal = bill = res_line = waehrung = None

    bline_list = summary1 = cash_art = turnover = cbuff = tlist = None

    summary1_list, Summary1 = create_model("Summary1", {"usrinit":str, "username":str, "artnr":int, "amount":decimal})
    cash_art_list, Cash_art = create_model("Cash_art", {"pos_nr":int, "artnr":int, "bezeich":str, "amount":decimal, "tamount":decimal})
    turnover_list, Turnover = create_model("Turnover", {"departement":int, "usr_nr":int, "name":str, "rechnr":str, "zinr":str, "info":str, "curr":str, "p_cash":decimal, "f_cash":decimal, "c_ledger":decimal, "creditcard":decimal, "flag":int, "gname":str}, {"zinr": ""})

    Cbuff = Cash_art
    cbuff_list = cash_art_list


    db_session = local_storage.db_session

    def generate_output():
        nonlocal curr_shift, nt_cash, nt_fcash, nt_ledger, nt_credit, turnover_list, summary1_list, cash_art_list, tot_cash, tot_fcash, tot_ledger, tot_credit, tot_amount, nt_amount, lvcarea, bediener, artikel, billjournal, bill, res_line, waehrung
        nonlocal pvilanguage, shift, from_date, to_date
        nonlocal cbuff


        nonlocal bline_list, summary1, cash_art, turnover, cbuff, tlist
        nonlocal bline_list_list, summary1_list, cash_art_list, turnover_list
        return {"curr_shift": curr_shift, "nt_cash": nt_cash, "nt_fcash": nt_fcash, "nt_ledger": nt_ledger, "nt_credit": nt_credit, "turnover": turnover_list, "summary1": summary1_list, "cash-art": cash_art_list}

    def daysale_list1():

        nonlocal curr_shift, nt_cash, nt_fcash, nt_ledger, nt_credit, turnover_list, summary1_list, cash_art_list, tot_cash, tot_fcash, tot_ledger, tot_credit, tot_amount, nt_amount, lvcarea, bediener, artikel, billjournal, bill, res_line, waehrung
        nonlocal pvilanguage, shift, from_date, to_date
        nonlocal cbuff


        nonlocal bline_list, summary1, cash_art, turnover, cbuff, tlist
        nonlocal bline_list_list, summary1_list, cash_art_list, turnover_list

        curr_s:int = 0
        billnr:int = 0
        dept:int = 0
        d_name:str = ""
        usr_nr:int = 0
        d_found:bool = False
        c_found:bool = False
        vat:decimal = to_decimal("0.0")
        service:decimal = to_decimal("0.0")
        netto:decimal = to_decimal("0.0")
        i:int = 0
        pos:int = 0
        bill_no:int = 0
        guestname:str = ""
        found:bool = False
        do_it:bool = False
        t_resnr:str = ""
        Tlist = Turnover
        tlist_list = turnover_list

        for turnover in query(turnover_list):
            turnover_list.remove(turnover)
        cash_art_list.clear()
        summary1_list.clear()
        tot_cash =  to_decimal("0")
        tot_ledger =  to_decimal("0")
        tot_credit =  to_decimal("0")
        tot_fcash =  to_decimal("0")
        nt_cash = 0
        nt_ledger =  to_decimal("0")
        nt_credit = 0
        nt_fcash = 0

        if shift == 0:
            curr_shift = translateExtended ("shift : ALL", lvcarea, "")

        elif shift == 1:
            curr_shift = translateExtended ("shift : MORNING", lvcarea, "")

        elif shift == 2:
            curr_shift = translateExtended ("shift : NOON", lvcarea, "")

        elif shift == 1:
            curr_shift = translateExtended ("shift : DINNER", lvcarea, "")

        elif shift == 1:
            curr_shift = translateExtended ("shift : SUPPER", lvcarea, "")

        for bline_list in query(bline_list_list, filters=(lambda bline_list: bline_list.selected), sort_by=[("name",False)]):

            bediener = db_session.query(Bediener).filter(
                     (Bediener._recid == bline_list.bl_recid)).first()
            tot_cash =  to_decimal("0")
            tot_ledger =  to_decimal("0")
            tot_credit =  to_decimal("0")
            tot_fcash =  to_decimal("0")
            found = False

            billjournal_obj_list = []
            for billjournal, artikel in db_session.query(Billjournal, Artikel).join(Artikel,(Artikel.artnr == Billjournal.artnr) & (Artikel.departement == 0) & ((Artikel.artart == 2) | (Artikel.artart == 6) | (Artikel.artart == 7))).filter(
                     (Billjournal.bill_datum == from_date) & (Billjournal.departement == 0) & (Billjournal.anzahl != 0) & (Billjournal.userinit == bediener.userinit)).order_by(Billjournal.rechnr).all():
                if billjournal._recid in billjournal_obj_list:
                    continue
                else:
                    billjournal_obj_list.append(billjournal._recid)

                if shift == 0:
                    do_it = True
                else:
                    do_it = billjournal.betriebsnr == shift

                if do_it:
                    found = True

                    bill = db_session.query(Bill).filter(
                             (Bill.rechnr == billjournal.rechnr) & (Bill.rechnr != 0)).first()

                    turnover = query(turnover_list, filters=(lambda turnover: turnover.rechnr == to_string(billjournal.rechnr) and turnover.usr_nr == bediener.nr), first=True)

                    if not turnover:
                        turnover = Turnover()
                        turnover_list.append(turnover)

                        turnover.rechnr = to_string(billjournal.rechnr)
                        turnover.usr_nr = bediener.nr
                        turnover.name = bediener.username

                        if bill:

                            res_line = db_session.query(Res_line).filter(
                                     (Res_line.resnr == bill.resnr) & (Res_line.reslinnr == bill.parent_nr)).first()

                            if res_line:
                                turnover.gname = res_line.name
                            turnover.zinr = bill.zinr


                        else:

                            if re.match(r".*#.*",billjournal.bezeich, re.IGNORECASE):
                                t_resnr = entry(1, billjournal.bezeich, "#")


                            else:
                                t_resnr = billjournal.bezeich


                            t_resnr = entry(0, t_resnr, "]")

                            res_line = db_session.query(Res_line).filter(
                                     (Res_line.resnr == to_int(t_resnr))).first()

                            if res_line:
                                turnover.gname = res_line.name

                    if artikel.artart == 2:
                        turnover.c_ledger =  to_decimal(turnover.c_ledger) - to_decimal(billjournal.betrag)
                        tot_ledger =  to_decimal(tot_ledger) - to_decimal(billjournal.betrag)

                    elif artikel.artart == 6:

                        if artikel.pricetab:

                            waehrung = db_session.query(Waehrung).filter(
                                     (Waehrung.waehrungsnr == artikel.betriebsnr)).first()

                            if waehrung:
                                turnover.curr = waehrung.wabkurz
                            turnover.f_cash =  to_decimal(turnover.f_cash) - to_decimal(billjournal.fremdwaehrng)
                            tot_fcash =  to_decimal(tot_fcash) - to_decimal(billjournal.fremdwaehrng)


                        else:
                            turnover.p_cash =  to_decimal(turnover.p_cash) - to_decimal(billjournal.betrag)
                            tot_cash =  to_decimal(tot_cash) - to_decimal(billjournal.betrag)

                        cash_art = query(cash_art_list, filters=(lambda cash_art: cash_art.artnr == artikel.artnr), first=True)

                        if not cash_art:
                            cash_art = Cash_art()
                            cash_art_list.append(cash_art)

                            cash_art.artnr = artikel.artnr
                            cash_art.bezeich = artikel.bezeich

                            cbuff = query(cbuff_list, last=True)

                            if cbuff:
                                cash_art.pos_nr = cbuff.pos_nr + 1


                            else:
                                cash_art.pos_nr = 1

                        summary1 = query(summary1_list, filters=(lambda summary1: summary1.usrinit == billjournal.userinit and summary1.artnr == artikel.artnr), first=True)

                        if not summary1:
                            summary1 = Summary1()
                            summary1_list.append(summary1)

                            summary1.artnr = artikel.artnr
                            summary1.usrinit = bediener.userinit


                        summary1.amount =  to_decimal(summary1.amount) - to_decimal(billjournal.betrag)

                    elif artikel.artart == 7:
                        turnover.creditcard =  to_decimal(turnover.creditcard) - to_decimal(billjournal.betrag)
                        tot_credit =  to_decimal(tot_credit) - to_decimal(billjournal.betrag)
                        turnover.info = entry(1, billjournal.bezeich, "/")

            if found:
                turnover = Turnover()
                turnover_list.append(turnover)

                turnover.rechnr = "TOTAL"
                turnover.flag = 1
                turnover.p_cash =  to_decimal(tot_cash)
                turnover.c_ledger =  to_decimal(tot_ledger)
                turnover.creditcard =  to_decimal(tot_credit)
                turnover.f_cash =  to_decimal(tot_fcash)


        turnover = Turnover()
        turnover_list.append(turnover)

        turnover.rechnr = "G-TOTAL"
        turnover.flag = 3

        for tlist in query(tlist_list, filters=(lambda tlist: tlist.flag == 0)):
            turnover.p_cash =  to_decimal(turnover.p_cash) + to_decimal(tlist.p_cash)
            turnover.c_ledger =  to_decimal(turnover.c_ledger) + to_decimal(tlist.c_ledger)
            turnover.creditcard =  to_decimal(turnover.creditcard) + to_decimal(tlist.creditcard)
            turnover.f_cash =  to_decimal(turnover.f_cash) + to_decimal(tlist.f_cash)
        nt_cash = turnover.p_cash
        nt_ledger =  to_decimal(turnover.c_ledger)
        nt_credit = turnover.credit
        nt_fcash = turnover.f_cash


    daysale_list1()

    return generate_output()