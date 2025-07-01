#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.calc_servtaxesbl import calc_servtaxesbl
from models import H_bill_line, H_artikel, Hoteldpt, Kellner, H_bill, Artikel

tt_artnr_list, Tt_artnr = create_model("Tt_artnr", {"curr_i":int, "artnr":int})

def rest_sumsale_btn_gobl(curr_dept:int, dept_name:string, exchg_rate:Decimal, tt_artnr_list:[Tt_artnr], ldry:int, dstore:int, clb:int, zeit2:int, zeit1:int, from_date:date):

    prepare_cache ([H_bill_line, H_artikel, Hoteldpt, Kellner, H_bill, Artikel])

    t_betrag = to_decimal("0.0")
    t_foreign = to_decimal("0.0")
    turnover_list = []
    outstand_list_list = []
    pay_list_list = []
    artnr_list:List[int] = create_empty_list(5,0)
    curr_rechnr:int = -1
    new_dept:int = -1
    tot_food:Decimal = to_decimal("0.0")
    tot_beverage:Decimal = to_decimal("0.0")
    tot_misc:Decimal = to_decimal("0.0")
    tot_cigar:Decimal = to_decimal("0.0")
    tot_disc:Decimal = to_decimal("0.0")
    tot_serv:Decimal = to_decimal("0.0")
    tot_tax:Decimal = to_decimal("0.0")
    tot_debit:Decimal = to_decimal("0.0")
    tot_cash:Decimal = to_decimal("0.0")
    tot_cash1:Decimal = to_decimal("0.0")
    tot_trans:Decimal = to_decimal("0.0")
    tot_ledger:Decimal = to_decimal("0.0")
    tot_cover:int = 0
    t_food:Decimal = to_decimal("0.0")
    t_beverage:Decimal = to_decimal("0.0")
    t_misc:Decimal = to_decimal("0.0")
    t_cigar:Decimal = to_decimal("0.0")
    t_disc:Decimal = to_decimal("0.0")
    t_serv:Decimal = to_decimal("0.0")
    t_tax:Decimal = to_decimal("0.0")
    t_debit:Decimal = to_decimal("0.0")
    t_cash:Decimal = to_decimal("0.0")
    t_cash1:Decimal = to_decimal("0.0")
    t_trans:Decimal = to_decimal("0.0")
    t_ledger:Decimal = to_decimal("0.0")
    t_cover:int = 0
    anz_comp:int = 0
    val_comp:Decimal = to_decimal("0.0")
    anz_coup:int = 0
    val_coup:Decimal = to_decimal("0.0")
    return_debit:Decimal = to_decimal("0.0")
    return_cash1:Decimal = to_decimal("0.0")
    return_cash:Decimal = to_decimal("0.0")
    return_trans:Decimal = to_decimal("0.0")
    return_ledger:Decimal = to_decimal("0.0")
    compli_flag:bool = False
    h_bill_line = h_artikel = hoteldpt = kellner = h_bill = artikel = None

    outstand_list = pay_list = comp_list = turnover = tt_artnr = bh_bill_line = bh_artikel = None

    outstand_list_list, Outstand_list = create_model("Outstand_list", {"deptname":string, "name":string, "rechnr":int, "foreign":Decimal, "saldo":Decimal})
    pay_list_list, Pay_list = create_model("Pay_list", {"flag":int, "bezeich":string, "artnr":int, "rechnr":int, "foreign":Decimal, "saldo":Decimal})
    comp_list_list, Comp_list = create_model("Comp_list", {"rechnr":int})
    turnover_list, Turnover = create_model("Turnover", {"compli":bool, "compli_amt":Decimal, "departement":int, "kellner_nr":int, "name":string, "tischnr":int, "rechnr":string, "belegung":int, "artnr":int, "info":string, "food":Decimal, "beverage":Decimal, "misc":Decimal, "cigarette":Decimal, "discount":Decimal, "t_service":Decimal, "t_tax":Decimal, "t_debit":Decimal, "t_credit":Decimal, "p_cash":Decimal, "p_cash1":Decimal, "r_transfer":Decimal, "c_ledger":Decimal})

    Bh_bill_line = create_buffer("Bh_bill_line",H_bill_line)
    Bh_artikel = create_buffer("Bh_artikel",H_artikel)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_betrag, t_foreign, turnover_list, outstand_list_list, pay_list_list, artnr_list, curr_rechnr, new_dept, tot_food, tot_beverage, tot_misc, tot_cigar, tot_disc, tot_serv, tot_tax, tot_debit, tot_cash, tot_cash1, tot_trans, tot_ledger, tot_cover, t_food, t_beverage, t_misc, t_cigar, t_disc, t_serv, t_tax, t_debit, t_cash, t_cash1, t_trans, t_ledger, t_cover, anz_comp, val_comp, anz_coup, val_coup, return_debit, return_cash1, return_cash, return_trans, return_ledger, compli_flag, h_bill_line, h_artikel, hoteldpt, kellner, h_bill, artikel
        nonlocal curr_dept, dept_name, exchg_rate, ldry, dstore, clb, zeit2, zeit1, from_date
        nonlocal bh_bill_line, bh_artikel


        nonlocal outstand_list, pay_list, comp_list, turnover, tt_artnr, bh_bill_line, bh_artikel
        nonlocal outstand_list_list, pay_list_list, comp_list_list, turnover_list

        return {"curr_dept": curr_dept, "dept_name": dept_name, "exchg_rate": exchg_rate, "t_betrag": t_betrag, "t_foreign": t_foreign, "turnover": turnover_list, "outstand-list": outstand_list_list, "pay-list": pay_list_list}

    def daysale_list():

        nonlocal t_betrag, t_foreign, turnover_list, outstand_list_list, pay_list_list, artnr_list, curr_rechnr, new_dept, tot_food, tot_beverage, tot_misc, tot_cigar, tot_disc, tot_serv, tot_tax, tot_debit, tot_cash, tot_cash1, tot_trans, tot_ledger, tot_cover, t_food, t_beverage, t_misc, t_cigar, t_disc, t_serv, t_tax, t_debit, t_cash, t_cash1, t_trans, t_ledger, t_cover, anz_comp, val_comp, anz_coup, val_coup, return_debit, return_cash1, return_cash, return_trans, return_ledger, compli_flag, h_bill_line, h_artikel, hoteldpt, kellner, h_bill, artikel
        nonlocal curr_dept, dept_name, exchg_rate, ldry, dstore, clb, zeit2, zeit1, from_date
        nonlocal bh_bill_line, bh_artikel


        nonlocal outstand_list, pay_list, comp_list, turnover, tt_artnr, bh_bill_line, bh_artikel
        nonlocal outstand_list_list, pay_list_list, comp_list_list, turnover_list

        from_dept:int = 0
        to_dept:int = 0
        ft_dept:int = 0

        for tt_artnr in query(tt_artnr_list):
            artnr_list[tt_artnr.curr_i - 1] = tt_artnr.artnr


        t_betrag =  to_decimal("0")
        t_foreign =  to_decimal("0")


        turnover_list.clear()
        pay_list_list.clear()
        outstand_list_list.clear()
        tot_cover = 0
        tot_food =  to_decimal("0")
        tot_beverage =  to_decimal("0")
        tot_misc =  to_decimal("0")
        tot_disc =  to_decimal("0")
        tot_serv =  to_decimal("0")
        tot_tax =  to_decimal("0")
        tot_debit =  to_decimal("0")
        tot_cash1 =  to_decimal("0")
        tot_cash =  to_decimal("0")
        tot_trans =  to_decimal("0")
        tot_ledger =  to_decimal("0")

        for hoteldpt in db_session.query(Hoteldpt).filter(
                 (Hoteldpt.num >= 1) & (Hoteldpt.num != ldry) & (Hoteldpt.num != dstore) & (Hoteldpt.num != clb)).order_by(Hoteldpt.num.desc()).all():
            curr_dept = hoteldpt.num
            dept_name = hoteldpt.depart

            h_bill_obj_list = {}
            h_bill = H_bill()
            kellner = Kellner()
            for h_bill.rechnr, h_bill.belegung, h_bill._recid, kellner.kellnername, kellner._recid in db_session.query(H_bill.rechnr, H_bill.belegung, H_bill._recid, Kellner.kellnername, Kellner._recid).join(Kellner,(Kellner.kellner_nr == H_bill.kellner_nr)).filter(
                     (H_bill.flag == 0) & (H_bill.saldo != 0) & (H_bill.departement == curr_dept)).order_by(H_bill.rechnr).all():
                if h_bill_obj_list.get(h_bill._recid):
                    continue
                else:
                    h_bill_obj_list[h_bill._recid] = True


                outstand_list = Outstand_list()
                outstand_list_list.append(outstand_list)

                outstand_list.deptname = to_string(curr_dept, "99") + " - " + dept_name
                outstand_list.rechnr = h_bill.rechnr
                outstand_list.name = kellner.kellnername

                for h_bill_line in db_session.query(H_bill_line).filter(
                         (H_bill_line.rechnr == h_bill.rechnr) & (H_bill_line.departement == curr_dept)).order_by(H_bill_line._recid).all():
                    outstand_list.saldo =  to_decimal(outstand_list.saldo) + to_decimal(h_bill_line.betrag)
                    outstand_list.foreign =  to_decimal(outstand_list.foreign) + to_decimal(h_bill_line.fremdwbetrag)

        for hoteldpt in db_session.query(Hoteldpt).filter(
                 (Hoteldpt.num >= 1) & (Hoteldpt.num != ldry) & (Hoteldpt.num != dstore) & (Hoteldpt.num != clb)).order_by(Hoteldpt._recid).all():
            curr_dept = hoteldpt.num
            dept_name = hoteldpt.depart
            turnover = Turnover()
            turnover_list.append(turnover)

            turnover.departement = curr_dept
            turnover.name = to_string(curr_dept, "99") + " - " + dept_name

            if (zeit2 - zeit1) >= (24 * 3600 - 60):

                h_bill_line_obj_list = {}
                h_bill_line = H_bill_line()
                h_bill = H_bill()
                for h_bill_line.betrag, h_bill_line.fremdwbetrag, h_bill_line.rechnr, h_bill_line.departement, h_bill_line.artnr, h_bill_line.bill_datum, h_bill_line._recid, h_bill.rechnr, h_bill.belegung, h_bill._recid in db_session.query(H_bill_line.betrag, H_bill_line.fremdwbetrag, H_bill_line.rechnr, H_bill_line.departement, H_bill_line.artnr, H_bill_line.bill_datum, H_bill_line._recid, H_bill.rechnr, H_bill.belegung, H_bill._recid).join(H_bill,(H_bill.rechnr == H_bill_line.rechnr) & (H_bill.departement == H_bill_line.departement) & (H_bill.flag == 1)).filter(
                         (H_bill_line.bill_datum == from_date) & (H_bill_line.departement == curr_dept)).order_by(H_bill_line.rechnr).all():
                    if h_bill_line_obj_list.get(h_bill_line._recid):
                        continue
                    else:
                        h_bill_line_obj_list[h_bill_line._recid] = True


                    create_turnover()

            elif zeit1 > zeit2:

                h_bill_line_obj_list = {}
                h_bill_line = H_bill_line()
                h_bill = H_bill()
                for h_bill_line.betrag, h_bill_line.fremdwbetrag, h_bill_line.rechnr, h_bill_line.departement, h_bill_line.artnr, h_bill_line.bill_datum, h_bill_line._recid, h_bill.rechnr, h_bill.belegung, h_bill._recid in db_session.query(H_bill_line.betrag, H_bill_line.fremdwbetrag, H_bill_line.rechnr, H_bill_line.departement, H_bill_line.artnr, H_bill_line.bill_datum, H_bill_line._recid, H_bill.rechnr, H_bill.belegung, H_bill._recid).join(H_bill,(H_bill.rechnr == H_bill_line.rechnr) & (H_bill.departement == H_bill_line.departement) & (H_bill.flag == 1)).filter(
                         (H_bill_line.bill_datum == from_date) & (H_bill_line.departement == curr_dept) & (H_bill_line.zeit >= zeit1)).order_by(H_bill_line.rechnr).all():
                    if h_bill_line_obj_list.get(h_bill_line._recid):
                        continue
                    else:
                        h_bill_line_obj_list[h_bill_line._recid] = True


                    create_turnover()
            else:

                h_bill_line_obj_list = {}
                h_bill_line = H_bill_line()
                h_bill = H_bill()
                for h_bill_line.betrag, h_bill_line.fremdwbetrag, h_bill_line.rechnr, h_bill_line.departement, h_bill_line.artnr, h_bill_line.bill_datum, h_bill_line._recid, h_bill.rechnr, h_bill.belegung, h_bill._recid in db_session.query(H_bill_line.betrag, H_bill_line.fremdwbetrag, H_bill_line.rechnr, H_bill_line.departement, H_bill_line.artnr, H_bill_line.bill_datum, H_bill_line._recid, H_bill.rechnr, H_bill.belegung, H_bill._recid).join(H_bill,(H_bill.rechnr == H_bill_line.rechnr) & (H_bill.departement == H_bill_line.departement) & (H_bill.flag == 1)).filter(
                         (H_bill_line.bill_datum == from_date) & (H_bill_line.departement == curr_dept) & (H_bill_line.zeit >= zeit1) & (H_bill_line.zeit <= zeit2)).order_by(H_bill_line.rechnr).all():
                    if h_bill_line_obj_list.get(h_bill_line._recid):
                        continue
                    else:
                        h_bill_line_obj_list[h_bill_line._recid] = True


                    create_turnover()

        for turnover in query(turnover_list, filters=(lambda turnover: turnover.compli_amt != 0)):
            turnover.compli = True
        turnover = Turnover()
        turnover_list.append(turnover)

        turnover.name = "TOTAL"
        turnover.belegung = tot_cover
        turnover.food =  to_decimal(tot_food)
        turnover.beverage =  to_decimal(tot_beverage)
        turnover.misc =  to_decimal(tot_misc)
        turnover.discount =  to_decimal(tot_disc)
        turnover.t_service =  to_decimal(tot_serv)
        turnover.t_tax =  to_decimal(tot_tax)
        turnover.t_debit =  to_decimal(tot_debit) - to_decimal(return_debit)
        turnover.p_cash =  to_decimal(tot_cash) - to_decimal(return_cash)
        turnover.p_cash1 =  to_decimal(tot_cash1) - to_decimal(return_cash1)
        turnover.r_transfer =  to_decimal(tot_trans) - to_decimal(return_trans)
        turnover.c_ledger =  to_decimal(tot_ledger) - to_decimal(return_ledger)


    def create_turnover():

        nonlocal t_betrag, t_foreign, turnover_list, outstand_list_list, pay_list_list, artnr_list, curr_rechnr, new_dept, tot_food, tot_beverage, tot_misc, tot_cigar, tot_disc, tot_serv, tot_tax, tot_debit, tot_cash, tot_cash1, tot_trans, tot_ledger, tot_cover, t_food, t_beverage, t_misc, t_cigar, t_disc, t_serv, t_tax, t_debit, t_cash, t_cash1, t_trans, t_ledger, t_cover, anz_comp, val_comp, anz_coup, val_coup, return_debit, return_cash1, return_cash, return_trans, return_ledger, compli_flag, h_bill_line, h_artikel, hoteldpt, kellner, h_bill, artikel
        nonlocal curr_dept, dept_name, exchg_rate, ldry, dstore, clb, zeit2, zeit1, from_date
        nonlocal bh_bill_line, bh_artikel


        nonlocal outstand_list, pay_list, comp_list, turnover, tt_artnr, bh_bill_line, bh_artikel
        nonlocal outstand_list_list, pay_list_list, comp_list_list, turnover_list

        dept:int = 1
        i:int = 0
        curr_s:int = 0
        billnr:int = 0
        d_name:string = ""
        usr_nr:int = 0
        d_found:bool = False
        c_found:bool = False
        vat:Decimal = to_decimal("0.0")
        service:Decimal = to_decimal("0.0")
        netto:Decimal = to_decimal("0.0")
        found:bool = False
        vat2:Decimal = to_decimal("0.0")
        fact:Decimal = to_decimal("0.0")

        if curr_rechnr != h_bill.rechnr:
            turnover.belegung = turnover.belegung + h_bill.belegung


            tot_cover = tot_cover + h_bill.belegung
            curr_rechnr = h_bill.rechnr

        if h_bill_line.artnr == 0:

            pay_list = query(pay_list_list, filters=(lambda pay_list: pay_list.flag == 2), first=True)

            if not pay_list:
                pay_list = Pay_list()
                pay_list_list.append(pay_list)

                pay_list.flag = 2
                pay_list.bezeich = "Room / Bill Transfer"
            pay_list.saldo =  to_decimal(pay_list.saldo) - to_decimal(h_bill_line.betrag)
            t_betrag =  to_decimal(t_betrag) - to_decimal(h_bill_line.betrag)
            turnover.r_transfer =  to_decimal(turnover.r_transfer) - to_decimal(h_bill_line.betrag)
            i = 0
            found = False
            turnover.t_credit =  to_decimal(turnover.t_credit) - to_decimal(h_bill_line.betrag)
            tot_trans =  to_decimal(tot_trans) - to_decimal(h_bill_line.betrag)
        else:
            compli_flag = False

            bh_bill_line_obj_list = {}
            bh_bill_line = H_bill_line()
            bh_artikel = H_artikel()
            for bh_bill_line.betrag, bh_bill_line.fremdwbetrag, bh_bill_line.rechnr, bh_bill_line.departement, bh_bill_line.artnr, bh_bill_line.bill_datum, bh_bill_line._recid, bh_artikel.artart, bh_artikel.bezeich, bh_artikel.artnrfront, bh_artikel._recid in db_session.query(Bh_bill_line.betrag, Bh_bill_line.fremdwbetrag, Bh_bill_line.rechnr, Bh_bill_line.departement, Bh_bill_line.artnr, Bh_bill_line.bill_datum, Bh_bill_line._recid, Bh_artikel.artart, Bh_artikel.bezeich, Bh_artikel.artnrfront, Bh_artikel._recid).join(Bh_artikel,(Bh_artikel.artnr == Bh_bill_line.artnr) & (Bh_artikel.departement == Bh_bill_line.departement) & (Bh_artikel.artart >= 11) & (Bh_artikel.artart <= 12)).filter(
                     (Bh_bill_line.rechnr == h_bill_line.rechnr) & (Bh_bill_line.departement == h_bill_line.departement)).order_by(Bh_artikel.artart.desc()).yield_per(100):
                if bh_bill_line_obj_list.get(bh_bill_line._recid):
                    continue
                else:
                    bh_bill_line_obj_list[bh_bill_line._recid] = True


                compli_flag = True


                break

            h_artikel = get_cache (H_artikel, {"artnr": [(eq, h_bill_line.artnr)],"departement": [(eq, h_bill_line.departement)]})

            if h_artikel:

                if h_artikel.artart == 11 or h_artikel.artart == 12:

                    if h_artikel.artart == 11:

                        pay_list = query(pay_list_list, filters=(lambda pay_list: pay_list.flag == 6 and pay_list.bezeich == h_artikel.bezeich), first=True)

                        if not pay_list:
                            pay_list = Pay_list()
                            pay_list_list.append(pay_list)

                            pay_list.flag = 6
                            pay_list.bezeich = h_artikel.bezeich
                        pay_list.saldo =  to_decimal(pay_list.saldo) - to_decimal(h_bill_line.betrag)

                        if h_bill_line.betrag < 0:
                            anz_comp = anz_comp + 1

                        elif h_bill_line.betrag > 0:
                            anz_comp = anz_comp - 1
                        turnover.compli_amt =  to_decimal(turnover.compli_amt) - to_decimal(h_bill_line.betrag)
                        val_comp =  to_decimal(val_comp) - to_decimal(h_bill_line.betrag)

                    elif h_artikel.artart == 12:

                        pay_list = query(pay_list_list, filters=(lambda pay_list: pay_list.flag == 7), first=True)

                        if not pay_list:
                            pay_list = Pay_list()
                            pay_list_list.append(pay_list)

                            pay_list.flag = 7
                            pay_list.bezeich = "Meal Coupon"
                        pay_list.saldo =  to_decimal(pay_list.saldo) - to_decimal(h_bill_line.betrag)

                        if h_bill_line.betrag < 0:
                            anz_coup = anz_coup + 1

                        elif h_bill_line.betrag > 0:
                            anz_coup = anz_coup - 1
                        turnover.compli_amt =  to_decimal(turnover.compli_amt) - to_decimal(h_bill_line.betrag)
                        val_coup =  to_decimal(val_coup) - to_decimal(h_bill_line.betrag)
                    turnover.r_transfer =  to_decimal(turnover.r_transfer) - to_decimal(h_bill_line.betrag)

                    if h_artikel.artart == 11:
                        turnover.info = "Comp"

                    elif h_artikel.artart == 12:
                        turnover.info = "Cpon"
                    tot_trans =  to_decimal(tot_trans) - to_decimal(h_bill_line.betrag)
                else:

                    if h_artikel.artart == 0:

                        artikel = get_cache (Artikel, {"departement": [(eq, curr_dept)],"artnr": [(eq, h_artikel.artnrfront)]})
                    else:

                        artikel = get_cache (Artikel, {"departement": [(eq, 0)],"artnr": [(eq, h_artikel.artnrfront)]})

                    if h_artikel.artart == 0:
                        service =  to_decimal("0")
                        vat =  to_decimal("0")
                        vat2 =  to_decimal("0")
                        service, vat, vat2, fact = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, h_bill_line.bill_datum))
                        netto =  to_decimal(h_bill_line.betrag) / to_decimal((1) + to_decimal(vat) + to_decimal(vat2) + to_decimal(service))

                        if not compli_flag:
                            turnover.t_service =  to_decimal(turnover.t_service) + to_decimal(netto) * to_decimal(service)
                            turnover.t_tax =  to_decimal(turnover.t_tax) + to_decimal(netto) * to_decimal(vat)
                            turnover.t_debit =  to_decimal(turnover.t_debit) + to_decimal(h_bill_line.betrag)
                            tot_serv =  to_decimal(tot_serv) + to_decimal(netto) * to_decimal(service)
                            tot_tax =  to_decimal(tot_tax) + to_decimal(netto) * to_decimal(vat)
                            tot_debit =  to_decimal(tot_debit) + to_decimal(h_bill_line.betrag)
                        else:
                            turnover.r_transfer =  to_decimal(turnover.r_transfer) - to_decimal(netto) * to_decimal(service) - to_decimal(netto) * to_decimal(vat)
                            tot_trans =  to_decimal(tot_trans) - to_decimal(netto) * to_decimal(service) - to_decimal(netto) * to_decimal(vat)
                            turnover.t_debit =  to_decimal(turnover.t_debit) + to_decimal(netto)
                            tot_debit =  to_decimal(tot_debit) + to_decimal(netto)

                        if h_bill_line.fremdwbetrag != 0:
                            exchg_rate =  to_decimal(h_bill_line.betrag) / to_decimal(h_bill_line.fremdwbetrag)

                        if artikel.artnr == artnr_list[0]:
                            turnover.food =  to_decimal(turnover.food) + to_decimal(netto)
                            tot_food =  to_decimal(tot_food) + to_decimal(netto)

                        elif artikel.artnr == artnr_list[1]:
                            turnover.beverage =  to_decimal(turnover.beverage) + to_decimal(netto)
                            tot_beverage =  to_decimal(tot_beverage) + to_decimal(netto)

                        elif artikel.artnr == artnr_list[2]:
                            turnover.misc =  to_decimal(turnover.misc) + to_decimal(netto)
                            tot_misc =  to_decimal(tot_misc) + to_decimal(netto)

                        elif artikel.artnr == artnr_list[3]:
                            turnover.cigarette =  to_decimal(turnover.cigarette) + to_decimal(netto)
                            tot_cigar =  to_decimal(tot_cigar) + to_decimal(netto)

                        elif artikel.artnr == artnr_list[4]:
                            turnover.discount =  to_decimal(turnover.discount) + to_decimal(netto)
                            tot_disc =  to_decimal(tot_disc) + to_decimal(netto)

                    elif h_artikel.artart == 6:

                        artikel = get_cache (Artikel, {"artnr": [(eq, h_artikel.artnrfront)],"departement": [(eq, 0)]})

                        pay_list = query(pay_list_list, filters=(lambda pay_list: pay_list.flag == 1), first=True)

                        if not pay_list:
                            pay_list = Pay_list()
                            pay_list_list.append(pay_list)

                            pay_list.flag = 1
                            pay_list.bezeich = "Cash"

                        if artikel.pricetab:
                            pay_list.foreign =  to_decimal(pay_list.foreign) - to_decimal(h_bill_line.fremdwbetrag)
                            t_foreign =  to_decimal(t_foreign) - to_decimal(h_bill_line.fremdwbetrag)
                        else:
                            pay_list.saldo =  to_decimal(pay_list.saldo) - to_decimal(h_bill_line.betrag)
                            t_betrag =  to_decimal(t_betrag) - to_decimal(h_bill_line.betrag)

                        if artikel.pricetab:
                            turnover.p_cash1 =  to_decimal(turnover.p_cash1) - to_decimal(h_bill_line.fremdwbetrag)
                            tot_cash1 =  to_decimal(tot_cash1) - to_decimal(h_bill_line.fremdwbetrag)
                        else:
                            turnover.p_cash =  to_decimal(turnover.p_cash) - to_decimal(h_bill_line.betrag)
                            tot_cash =  to_decimal(tot_cash) - to_decimal(h_bill_line.betrag)
                        turnover.t_credit =  to_decimal(turnover.t_credit) - to_decimal(h_bill_line.betrag)

                    elif h_artikel.artart == 7 or h_artikel.artart == 2:

                        if h_artikel.artart == 7:

                            pay_list = query(pay_list_list, filters=(lambda pay_list: pay_list.flag == 3), first=True)

                            if not pay_list:
                                pay_list = Pay_list()
                                pay_list_list.append(pay_list)

                                pay_list.flag = 3
                                pay_list.bezeich = "Credit Card"

                        elif h_artikel.artart == 2:

                            pay_list = query(pay_list_list, filters=(lambda pay_list: pay_list.flag == 5), first=True)

                            if not pay_list:
                                pay_list = Pay_list()
                                pay_list_list.append(pay_list)

                                pay_list.flag = 5
                                pay_list.bezeich = "City- & Employee Ledger"
                        pay_list.saldo =  to_decimal(pay_list.saldo) - to_decimal(h_bill_line.betrag)
                        t_betrag =  to_decimal(t_betrag) - to_decimal(h_bill_line.betrag)
                        turnover.c_ledger =  to_decimal(turnover.c_ledger) - to_decimal(h_bill_line.betrag)
                        turnover.t_credit =  to_decimal(turnover.t_credit) - to_decimal(h_bill_line.betrag)
                        tot_ledger =  to_decimal(tot_ledger) - to_decimal(h_bill_line.betrag)

    daysale_list()

    return generate_output()