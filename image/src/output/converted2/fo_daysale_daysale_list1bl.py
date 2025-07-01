#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Bediener, Artikel, Billjournal, Bill, Res_line, Waehrung

bline_list_list, Bline_list = create_model("Bline_list", {"flag":int, "userinit":string, "selected":bool, "name":string, "bl_recid":int})

def fo_daysale_daysale_list1bl(bline_list_list:[Bline_list], pvilanguage:int, shift:int, from_date:date, to_date:date):

    prepare_cache ([Bediener, Artikel, Billjournal, Bill, Res_line, Waehrung])

    curr_shift = ""
    nt_cash = to_decimal("0.0")
    nt_fcash = to_decimal("0.0")
    nt_ledger = to_decimal("0.0")
    nt_credit = to_decimal("0.0")
    turnover_list = []
    summary1_list = []
    cash_art_list = []
    tot_cash:Decimal = to_decimal("0.0")
    tot_fcash:Decimal = to_decimal("0.0")
    tot_ledger:Decimal = to_decimal("0.0")
    tot_credit:Decimal = to_decimal("0.0")
    tot_amount:List[Decimal] = create_empty_list(6,to_decimal("0"))
    nt_amount:List[Decimal] = create_empty_list(6,to_decimal("0"))
    lvcarea:string = "FO-daysale"
    bediener = artikel = billjournal = bill = res_line = waehrung = None

    bline_list = summary1 = cash_art = turnover = cbuff = tlist = None

    summary1_list, Summary1 = create_model("Summary1", {"usrinit":string, "username":string, "artnr":int, "amount":Decimal})
    cash_art_list, Cash_art = create_model("Cash_art", {"pos_nr":int, "artnr":int, "bezeich":string, "amount":Decimal, "tamount":Decimal})
    turnover_list, Turnover = create_model("Turnover", {"departement":int, "usr_nr":int, "name":string, "rechnr":string, "zinr":string, "info":string, "curr":string, "p_cash":Decimal, "f_cash":Decimal, "c_ledger":Decimal, "creditcard":Decimal, "flag":int, "gname":string}, {"zinr": ""})

    Cbuff = Cash_art
    cbuff_list = cash_art_list

    db_session = local_storage.db_session

    def generate_output():
        nonlocal curr_shift, nt_cash, nt_fcash, nt_ledger, nt_credit, turnover_list, summary1_list, cash_art_list, tot_cash, tot_fcash, tot_ledger, tot_credit, tot_amount, nt_amount, lvcarea, bediener, artikel, billjournal, bill, res_line, waehrung
        nonlocal pvilanguage, shift, from_date, to_date
        nonlocal cbuff


        nonlocal bline_list, summary1, cash_art, turnover, cbuff, tlist
        nonlocal summary1_list, cash_art_list, turnover_list

        return {"curr_shift": curr_shift, "nt_cash": nt_cash, "nt_fcash": nt_fcash, "nt_ledger": nt_ledger, "nt_credit": nt_credit, "turnover": turnover_list, "summary1": summary1_list, "cash-art": cash_art_list}

    def daysale_list1():

        nonlocal curr_shift, nt_cash, nt_fcash, nt_ledger, nt_credit, turnover_list, summary1_list, cash_art_list, tot_cash, tot_fcash, tot_ledger, tot_credit, tot_amount, nt_amount, lvcarea, bediener, artikel, billjournal, bill, res_line, waehrung
        nonlocal pvilanguage, shift, from_date, to_date
        nonlocal cbuff


        nonlocal bline_list, summary1, cash_art, turnover, cbuff, tlist
        nonlocal summary1_list, cash_art_list, turnover_list

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
        pos:int = 0
        bill_no:int = 0
        guestname:string = ""
        found:bool = False
        do_it:bool = False
        t_resnr:string = ""
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
        nt_cash =  to_decimal("0")
        nt_ledger =  to_decimal("0")
        nt_credit =  to_decimal("0")
        nt_fcash =  to_decimal("0")

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

            bediener = get_cache (Bediener, {"_recid": [(eq, bline_list.bl_recid)]})

            if bediener:
                tot_cash =  to_decimal("0")
                tot_ledger =  to_decimal("0")
                tot_credit =  to_decimal("0")
                tot_fcash =  to_decimal("0")
                found = False

                billjournal_obj_list = {}
                billjournal = Billjournal()
                artikel = Artikel()
                for billjournal.betriebsnr, billjournal.rechnr, billjournal.bezeich, billjournal.betrag, billjournal.fremdwaehrng, billjournal.userinit, billjournal._recid, artikel.betriebsnr, artikel.artnr, artikel.bezeich, artikel.artart, artikel._recid in db_session.query(Billjournal.betriebsnr, Billjournal.rechnr, Billjournal.bezeich, Billjournal.betrag, Billjournal.fremdwaehrng, Billjournal.userinit, Billjournal._recid, Artikel.betriebsnr, Artikel.artnr, Artikel.bezeich, Artikel.artart, Artikel._recid).join(Artikel,(Artikel.artnr == Billjournal.artnr) & (Artikel.departement == 0) & ((Artikel.artart == 2) | (Artikel.artart == 6) | (Artikel.artart == 7))).filter(
                         (Billjournal.bill_datum == from_date) & (Billjournal.departement == 0) & (Billjournal.anzahl != 0) & (Billjournal.userinit == bediener.userinit)).order_by(Billjournal.rechnr).all():
                    if billjournal_obj_list.get(billjournal._recid):
                        continue
                    else:
                        billjournal_obj_list[billjournal._recid] = True

                    if shift == 0:
                        do_it = True
                    else:
                        do_it = billjournal.betriebsnr == shift

                    if do_it:
                        found = True

                        bill = get_cache (Bill, {"rechnr": [(eq, billjournal.rechnr),(ne, 0)]})

                        turnover = query(turnover_list, filters=(lambda turnover: turnover.rechnr == to_string(billjournal.rechnr) and turnover.usr_nr == bediener.nr), first=True)

                        if not turnover:
                            turnover = Turnover()
                            turnover_list.append(turnover)

                            turnover.rechnr = to_string(billjournal.rechnr)
                            turnover.usr_nr = bediener.nr
                            turnover.name = bediener.username

                            if bill:

                                res_line = get_cache (Res_line, {"resnr": [(eq, bill.resnr)],"reslinnr": [(eq, bill.parent_nr)]})

                                if res_line:
                                    turnover.gname = res_line.name
                                turnover.zinr = bill.zinr


                            else:

                                if matches(billjournal.bezeich,r"*#*"):
                                    t_resnr = entry(1, billjournal.bezeich, "#")


                                else:
                                    t_resnr = billjournal.bezeich


                                t_resnr = entry(0, t_resnr, "]")

                                res_line = get_cache (Res_line, {"resnr": [(eq, to_int(t_resnr))]})

                                if res_line:
                                    turnover.gname = res_line.name

                        if artikel.artart == 2:
                            turnover.c_ledger =  to_decimal(turnover.c_ledger) - to_decimal(billjournal.betrag)
                            tot_ledger =  to_decimal(tot_ledger) - to_decimal(billjournal.betrag)

                        elif artikel.artart == 6:

                            if artikel.pricetab:

                                waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, artikel.betriebsnr)]})

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
        nt_cash =  to_decimal(turnover.p_cash)
        nt_ledger =  to_decimal(turnover.c_ledger)
        nt_credit =  to_decimal(turnover.creditcard)
        nt_fcash =  to_decimal(turnover.f_cash)


    daysale_list1()

    return generate_output()