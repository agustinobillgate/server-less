from functions.additional_functions import *
import decimal
from datetime import date
from models import Hoteldpt, Kellner, H_bill, H_bill_line, H_artikel, Artikel, Htparam

def rest_sumsale_btn_gobl(curr_dept:int, dept_name:str, exchg_rate:decimal, tt_artnr:[Tt_artnr], ldry:int, dstore:int, clb:int, zeit2:int, zeit1:int, from_date:date):
    t_betrag = 0
    t_foreign = 0
    turnover_list = []
    outstand_list_list = []
    pay_list_list = []
    artnr_list:[int] = [0, 0, 0, 0, 0, 0]
    curr_rechnr:int = -1
    new_dept:int = -1
    tot_food:decimal = 0
    tot_beverage:decimal = 0
    tot_misc:decimal = 0
    tot_cigar:decimal = 0
    tot_disc:decimal = 0
    tot_serv:decimal = 0
    tot_tax:decimal = 0
    tot_debit:decimal = 0
    tot_cash:decimal = 0
    tot_cash1:decimal = 0
    tot_trans:decimal = 0
    tot_ledger:decimal = 0
    tot_cover:int = 0
    t_food:decimal = 0
    t_beverage:decimal = 0
    t_misc:decimal = 0
    t_cigar:decimal = 0
    t_disc:decimal = 0
    t_serv:decimal = 0
    t_tax:decimal = 0
    t_debit:decimal = 0
    t_cash:decimal = 0
    t_cash1:decimal = 0
    t_trans:decimal = 0
    t_ledger:decimal = 0
    t_cover:int = 0
    anz_comp:int = 0
    val_comp:decimal = 0
    anz_coup:int = 0
    val_coup:decimal = 0
    return_debit:decimal = 0
    return_cash1:decimal = 0
    return_cash:decimal = 0
    return_trans:decimal = 0
    return_ledger:decimal = 0
    hoteldpt = kellner = h_bill = h_bill_line = h_artikel = artikel = htparam = None

    outstand_list = pay_list = turnover = tt_artnr = None

    outstand_list_list, Outstand_list = create_model("Outstand_list", {"deptname":str, "name":str, "rechnr":int, "foreign":decimal, "saldo":decimal})
    pay_list_list, Pay_list = create_model("Pay_list", {"flag":int, "bezeich":str, "artnr":int, "rechnr":int, "foreign":decimal, "saldo":decimal})
    turnover_list, Turnover = create_model("Turnover", {"compli":bool, "compli_amt":decimal, "departement":int, "kellner_nr":int, "name":str, "tischnr":int, "rechnr":str, "belegung":int, "artnr":int, "info":str, "food":decimal, "beverage":decimal, "misc":decimal, "cigarette":decimal, "discount":decimal, "t_service":decimal, "t_tax":decimal, "t_debit":decimal, "t_credit":decimal, "p_cash":decimal, "p_cash1":decimal, "r_transfer":decimal, "c_ledger":decimal})
    tt_artnr_list, Tt_artnr = create_model("Tt_artnr", {"curr_i":int, "artnr":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_betrag, t_foreign, turnover_list, outstand_list_list, pay_list_list, artnr_list, curr_rechnr, new_dept, tot_food, tot_beverage, tot_misc, tot_cigar, tot_disc, tot_serv, tot_tax, tot_debit, tot_cash, tot_cash1, tot_trans, tot_ledger, tot_cover, t_food, t_beverage, t_misc, t_cigar, t_disc, t_serv, t_tax, t_debit, t_cash, t_cash1, t_trans, t_ledger, t_cover, anz_comp, val_comp, anz_coup, val_coup, return_debit, return_cash1, return_cash, return_trans, return_ledger, hoteldpt, kellner, h_bill, h_bill_line, h_artikel, artikel, htparam


        nonlocal outstand_list, pay_list, turnover, tt_artnr
        nonlocal outstand_list_list, pay_list_list, turnover_list, tt_artnr_list
        return {"t_betrag": t_betrag, "t_foreign": t_foreign, "turnover": turnover_list, "outstand-list": outstand_list_list, "pay-list": pay_list_list}

    def daysale_list():

        nonlocal t_betrag, t_foreign, turnover_list, outstand_list_list, pay_list_list, artnr_list, curr_rechnr, new_dept, tot_food, tot_beverage, tot_misc, tot_cigar, tot_disc, tot_serv, tot_tax, tot_debit, tot_cash, tot_cash1, tot_trans, tot_ledger, tot_cover, t_food, t_beverage, t_misc, t_cigar, t_disc, t_serv, t_tax, t_debit, t_cash, t_cash1, t_trans, t_ledger, t_cover, anz_comp, val_comp, anz_coup, val_coup, return_debit, return_cash1, return_cash, return_trans, return_ledger, hoteldpt, kellner, h_bill, h_bill_line, h_artikel, artikel, htparam


        nonlocal outstand_list, pay_list, turnover, tt_artnr
        nonlocal outstand_list_list, pay_list_list, turnover_list, tt_artnr_list

        from_dept:int = 0
        to_dept:int = 0
        ft_dept:int = 0

        for tt_artnr in query(tt_artnr_list):
            artnr_list[tt_artnr.curr_i - 1] = tt_artnr.artnr


        t_betrag = 0
        t_foreign = 0


        turnover_list.clear()
        pay_list_list.clear()
        outstand_list_list.clear()
        tot_cover = 0
        tot_food = 0
        tot_beverage = 0
        tot_misc = 0
        tot_disc = 0
        tot_serv = 0
        tot_tax = 0
        tot_debit = 0
        tot_cash1 = 0
        tot_cash = 0
        tot_trans = 0
        tot_ledger = 0

        for hoteldpt in db_session.query(Hoteldpt).filter(
                (Hoteldpt.num >= 1) &  (Hoteldpt.num != ldry) &  (Hoteldpt.num != dstore) &  (Hoteldpt.num != clb)).all():
            curr_dept = hoteldpt.num
            dept_name = hoteldpt.depart

            h_bill_obj_list = []
            for h_bill, kellner in db_session.query(H_bill, Kellner).join(Kellner,(Kellner_nr == H_bill.kellner_nr)).filter(
                    (H_bill.flag == 0) &  (H_bill.saldo != 0) &  (H_bill.departement == curr_dept)).all():
                if h_bill._recid in h_bill_obj_list:
                    continue
                else:
                    h_bill_obj_list.append(h_bill._recid)


                outstand_list = Outstand_list()
                outstand_list_list.append(outstand_list)

                outstand_list.deptname = to_string(curr_dept, "99") + " - " + dept_name
                outstand_list.rechnr = h_bill.rechnr
                outstand_list.name = kellnername

                for h_bill_line in db_session.query(H_bill_line).filter(
                        (H_bill_line.rechnr == h_bill.rechnr) &  (H_bill_line.departement == curr_dept)).all():
                    outstand_list.saldo = outstand_list.saldo + h_bill_line.betrag
                    outstand_list.foreign = outstand_list.foreign + h_bill_line.fremdwbetrag

        for hoteldpt in db_session.query(Hoteldpt).filter(
                (Hoteldpt.num >= 1) &  (Hoteldpt.num != ldry) &  (Hoteldpt.num != dstore) &  (Hoteldpt.num != clb)).all():
            curr_dept = hoteldpt.num
            dept_name = hoteldpt.depart
            turnover = Turnover()
            turnover_list.append(turnover)

            turnover.departement = curr_dept
            turnover.name = to_string(curr_dept, "99") + " - " + dept_name

            if (zeit2 - zeit1) >= (24 * 3600 - 60):

                h_bill_line_obj_list = []
                for h_bill_line, h_bill in db_session.query(H_bill_line, H_bill).join(H_bill,(H_bill.rechnr == H_bill_line.rechnr) &  (H_bill.departement == H_bill_line.departement) &  (H_bill.flag == 1)).filter(
                        (H_bill_line.bill_datum == from_date) &  (H_bill_line.departement == curr_dept)).all():
                    if h_bill_line._recid in h_bill_line_obj_list:
                        continue
                    else:
                        h_bill_line_obj_list.append(h_bill_line._recid)


                    create_turnover()

            elif zeit1 > zeit2:

                h_bill_line_obj_list = []
                for h_bill_line, h_bill in db_session.query(H_bill_line, H_bill).join(H_bill,(H_bill.rechnr == H_bill_line.rechnr) &  (H_bill.departement == H_bill_line.departement) &  (H_bill.flag == 1)).filter(
                        (H_bill_line.bill_datum == from_date) &  (H_bill_line.departement == curr_dept) &  (H_bill_line.zeit >= zeit1)).all():
                    if h_bill_line._recid in h_bill_line_obj_list:
                        continue
                    else:
                        h_bill_line_obj_list.append(h_bill_line._recid)


                    create_turnover()
            else:

                h_bill_line_obj_list = []
                for h_bill_line, h_bill in db_session.query(H_bill_line, H_bill).join(H_bill,(H_bill.rechnr == H_bill_line.rechnr) &  (H_bill.departement == H_bill_line.departement) &  (H_bill.flag == 1)).filter(
                        (H_bill_line.bill_datum == from_date) &  (H_bill_line.departement == curr_dept) &  (H_bill_line.zeit >= zeit1) &  (H_bill_line.zeit <= zeit2)).all():
                    if h_bill_line._recid in h_bill_line_obj_list:
                        continue
                    else:
                        h_bill_line_obj_list.append(h_bill_line._recid)


                    create_turnover()

        for turnover in query(turnover_list, filters=(lambda turnover :turnover.compli_amt != 0)):
            turnover.compli = True
            tot_food = tot_food - turnover.food
            tot_beverage = tot_beverage - turnover.beverage
            tot_misc = tot_misc - turnover.misc
            tot_disc = tot_disc - turnover.discount
            tot_serv = tot_serv - turnover.t_service
            tot_tax = tot_tax - turnover.t_tax
            tot_cover = tot_cover - turnover.belegung
            return_debit = return_debit + turnover.t_debit
            return_cash1 = return_cash1 + turnover.p_cash1
            return_cash = return_cash + turnover.p_cash
            return_trans = return_trans + turnover.r_transfer
            return_ledger = return_ledger + turnover.c_ledger
        turnover = Turnover()
        turnover_list.append(turnover)

        turnover.name = "TOTAL"
        turnover.belegung = tot_cover
        turnover.food = tot_food
        turnover.beverage = tot_beverage
        turnover.misc = tot_misc
        turnover.discount = tot_disc
        turnover.t_service = tot_serv
        turnover.t_tax = tot_tax
        turnover.t_debit = tot_debit - return_debit
        turnover.p_cash = tot_cash - return_cash
        turnover.p_cash1 = tot_cash1 - return_cash1
        turnover.r_transfer = tot_trans - return_trans
        turnover.c_ledger = tot_ledger - return_ledger

    def create_turnover():

        nonlocal t_betrag, t_foreign, turnover_list, outstand_list_list, pay_list_list, artnr_list, curr_rechnr, new_dept, tot_food, tot_beverage, tot_misc, tot_cigar, tot_disc, tot_serv, tot_tax, tot_debit, tot_cash, tot_cash1, tot_trans, tot_ledger, tot_cover, t_food, t_beverage, t_misc, t_cigar, t_disc, t_serv, t_tax, t_debit, t_cash, t_cash1, t_trans, t_ledger, t_cover, anz_comp, val_comp, anz_coup, val_coup, return_debit, return_cash1, return_cash, return_trans, return_ledger, hoteldpt, kellner, h_bill, h_bill_line, h_artikel, artikel, htparam


        nonlocal outstand_list, pay_list, turnover, tt_artnr
        nonlocal outstand_list_list, pay_list_list, turnover_list, tt_artnr_list

        dept:int = 0
        i:int = 0
        curr_s:int = 0
        billnr:int = 0
        d_name:str = ""
        usr_nr:int = 0
        d_found:bool = "no"
        c_found:bool = "no"
        vat:decimal = 0
        service:decimal = 0
        netto:decimal = 0
        found:bool = False

        if curr_rechnr != h_bill.rechnr:
            turnover.belegung = turnover.belegung + h_bill.belegung


            tot_cover = tot_cover + h_bill.belegung
            curr_rechnr = h_bill.rechnr

        if h_bill_line.artnr == 0:

            pay_list = query(pay_list_list, filters=(lambda pay_list :pay_list.flag == 2), first=True)

            if not pay_list:
                pay_list = Pay_list()
                pay_list_list.append(pay_list)

                pay_list.flag = 2
                pay_list.bezeich = "Room / Bill Transfer"
            pay_list.saldo = pay_list.saldo - h_bill_line.betrag
            t_betrag = t_betrag - h_bill_line.betrag
            turnover.r_transfer = turnover.r_transfer - h_bill_line.betrag
            i = 0
            found = False
            turnover.t_credit = turnover.t_credit - h_bill_line.betrag
            tot_trans = tot_trans - h_bill_line.betrag
        else:

            h_artikel = db_session.query(H_artikel).filter(
                    (H_artikel.artnr == h_bill_line.artnr) &  (H_artikel.departement == h_bill_line.departement)).first()

            if h_artikel:

                if h_artikel.artart == 11 or h_artikel.artart == 12:

                    if h_artikel.artart == 11:

                        pay_list = query(pay_list_list, filters=(lambda pay_list :pay_list.flag == 6 and pay_list.bezeich == h_artikel.bezeich), first=True)

                        if not pay_list:
                            pay_list = Pay_list()
                            pay_list_list.append(pay_list)

                            pay_list.flag = 6
                            pay_list.bezeich = h_artikel.bezeich
                        pay_list.saldo = pay_list.saldo - h_bill_line.betrag

                        if h_bill_line.betrag < 0:
                            anz_comp = anz_comp + 1

                        elif h_bill_line.betrag > 0:
                            anz_comp = anz_comp - 1
                        turnover.compli_amt = turnover.compli_amt - h_bill_line.betrag
                        val_comp = val_comp - h_bill_line.betrag

                    elif h_artikel.artart == 12:

                        pay_list = query(pay_list_list, filters=(lambda pay_list :pay_list.flag == 7), first=True)

                        if not pay_list:
                            pay_list = Pay_list()
                            pay_list_list.append(pay_list)

                            pay_list.flag = 7
                            pay_list.bezeich = "Meal Coupon"
                        pay_list.saldo = pay_list.saldo - h_bill_line.betrag

                        if h_bill_line.betrag < 0:
                            anz_coup = anz_coup + 1

                        elif h_bill_line.betrag > 0:
                            anz_coup = anz_coup - 1
                        turnover.compli_amt = turnover.compli_amt - h_bill_line.betrag
                        val_coup = val_coup - h_bill_line.betrag
                    turnover.r_transfer = turnover.r_transfer - h_bill_line.betrag

                    if h_artikel.artart == 11:
                        turnover.info = "Comp"

                    elif h_artikel.artart == 12:
                        turnover.info = "Cpon"
                    tot_trans = tot_trans - h_bill_line.betrag
                else:

                    if h_artikel.artart == 0:

                        artikel = db_session.query(Artikel).filter(
                                (Artikel.departement == curr_dept) &  (Artikel.artnr == h_Artikel.artnrfront)).first()
                    else:

                        artikel = db_session.query(Artikel).filter(
                                (Artikel.departement == 0) &  (Artikel.artnr == h_Artikel.artnrfront)).first()

                    if h_artikel.artart == 0:
                        service = 0
                        vat = 0

                        htparam = db_session.query(Htparam).filter(
                                (Htparam.paramnr == h_artikel.service_code)).first()

                        if htparam:
                            service = 0.01 * htparam.fdecimal

                        htparam = db_session.query(Htparam).filter(
                                (Htparam.paramnr == h_artikel.mwst_code)).first()

                        if htparam:
                            vat = 0.01 * htparam.fdecimal * (1 + service)
                        netto = h_bill_line.betrag / (1 + vat + service)
                        turnover.t_service = turnover.t_service + netto * service
                        turnover.t_tax = turnover.t_tax + netto * vat
                        turnover.t_debit = turnover.t_debit + h_bill_line.betrag
                        tot_serv = tot_serv + netto * service
                        tot_tax = tot_tax + netto * vat
                        tot_debit = tot_debit + h_bill_line.betrag

                        if h_bill_line.fremdwbetrag != 0:
                            exchg_rate = h_bill_line.betrag / h_bill_line.fremdwbetrag

                        if artikel.artnr == artnr_list[0]:
                            turnover.food = turnover.food + netto
                            tot_food = tot_food + netto

                        elif artikel.artnr == artnr_list[1]:
                            turnover.beverage = turnover.beverage + netto
                            tot_beverage = tot_beverage + netto

                        elif artikel.artnr == artnr_list[2]:
                            turnover.misc = turnover.misc + netto
                            tot_misc = tot_misc + netto

                        elif artikel.artnr == artnr_list[3]:
                            turnover.cigarette = turnover.cigarette + netto
                            tot_cigar = tot_cigar + netto

                        elif artikel.artnr == artnr_list[4]:
                            turnover.discount = turnover.discount + netto
                            tot_disc = tot_disc + netto

                    elif h_artikel.artart == 6:

                        artikel = db_session.query(Artikel).filter(
                                (Artikel.artnr == h_Artikel.artnrfront) &  (Artikel.departement == 0)).first()

                        pay_list = query(pay_list_list, filters=(lambda pay_list :pay_list.flag == 1), first=True)

                        if not pay_list:
                            pay_list = Pay_list()
                            pay_list_list.append(pay_list)

                            pay_list.flag = 1
                            pay_list.bezeich = "Cash"

                        if artikel.pricetab:
                            pay_list.foreign = pay_list.foreign - h_bill_line.fremdwbetrag
                            t_foreign = t_foreign - h_bill_line.fremdwbetrag
                        else:
                            pay_list.saldo = pay_list.saldo - h_bill_line.betrag
                            t_betrag = t_betrag - h_bill_line.betrag

                        if artikel.pricetab:
                            turnover.p_cash1 = turnover.p_cash1 - h_bill_line.fremdwbetrag
                            tot_cash1 = tot_cash1 - h_bill_line.fremdwbetrag
                        else:
                            turnover.p_cash = turnover.p_cash - h_bill_line.betrag
                            tot_cash = tot_cash - h_bill_line.betrag
                        turnover.t_credit = turnover.t_credit - h_bill_line.betrag

                    elif h_artikel.artart == 7 or h_artikel.artart == 2:

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
                        turnover.c_ledger = turnover.c_ledger - h_bill_line.betrag
                        turnover.t_credit = turnover.t_credit - h_bill_line.betrag
                        tot_ledger = tot_ledger - h_bill_line.betrag

    daysale_list()

    return generate_output()