#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import H_artikel, Artikel, Hoteldpt, H_compli, Exrate, H_bill, H_cost

def ldry_compli_btn_gobl(foreign_nr:int, sorttype:int, from_dept:int, to_dept:int, from_date:date, to_date:date, billdate:date, exchg_rate:Decimal, double_currency:bool):

    prepare_cache ([H_artikel, Hoteldpt, H_compli, Exrate, H_bill, H_cost])

    c_list_list = []
    it_exist:bool = False
    n:int = 0
    h_artikel = artikel = hoteldpt = h_compli = exrate = h_bill = h_cost = None

    c_list = c1_list = None

    c_list_list, C_list = create_model("C_list", {"nr":int, "datum":date, "dept":int, "rechnr":int, "name":string, "p_artnr":int, "bezeich":string, "betrag":Decimal, "t_cost":Decimal, "deptname":string})
    c1_list_list, C1_list = create_model_like(C_list)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal c_list_list, it_exist, n, h_artikel, artikel, hoteldpt, h_compli, exrate, h_bill, h_cost
        nonlocal foreign_nr, sorttype, from_dept, to_dept, from_date, to_date, billdate, exchg_rate, double_currency


        nonlocal c_list, c1_list
        nonlocal c_list_list, c1_list_list

        return {"c-list": c_list_list}

    def journal_list1():

        nonlocal c_list_list, it_exist, n, h_artikel, artikel, hoteldpt, h_compli, exrate, h_bill, h_cost
        nonlocal foreign_nr, sorttype, from_dept, to_dept, from_date, to_date, billdate, exchg_rate, double_currency


        nonlocal c_list, c1_list
        nonlocal c_list_list, c1_list_list

        amount:Decimal = to_decimal("0.0")
        t_amount:Decimal = to_decimal("0.0")
        tot_amount:Decimal = to_decimal("0.0")
        rechnr:int = 0
        dept:int = -1
        p_artnr:int = 0
        depart:string = ""
        bezeich:string = ""
        i:int = 0
        artnr:int = 0
        datum:date = None
        curr_datum:date = None
        rate:Decimal = 1
        h_art = None
        fr_art = None
        cost:Decimal = to_decimal("0.0")
        t_cost:Decimal = to_decimal("0.0")
        t_betrag:Decimal = to_decimal("0.0")
        tt_cost:Decimal = to_decimal("0.0")
        tt_betrag:Decimal = to_decimal("0.0")
        curr_artnr:int = 0
        nr:int = 0
        H_art =  create_buffer("H_art",H_artikel)
        Fr_art =  create_buffer("Fr_art",Artikel)
        c_list_list.clear()
        c1_list_list.clear()
        it_exist = False

        for hoteldpt in db_session.query(Hoteldpt).filter(
                 (Hoteldpt.num >= from_dept) & (Hoteldpt.num <= to_dept)).order_by(Hoteldpt.num).all():

            h_compli_obj_list = {}
            h_compli = H_compli()
            h_art = H_artikel()
            for h_compli.datum, h_compli.departement, h_compli.rechnr, h_compli.p_artnr, h_compli.artnr, h_compli.anzahl, h_compli.epreis, h_compli._recid, h_art.artnrfront, h_art.prozent, h_art._recid, h_art.bezeich in db_session.query(H_compli.datum, H_compli.departement, H_compli.rechnr, H_compli.p_artnr, H_compli.artnr, H_compli.anzahl, H_compli.epreis, H_compli._recid, H_art.artnrfront, H_art.prozent, H_art._recid, H_art.bezeich).join(H_art,(H_art.departement == H_compli.departement) & (H_art.artnr == H_compli.p_artnr) & (H_art.artart == 11)).filter(
                     (H_compli.datum >= from_date) & (H_compli.datum <= to_date) & (H_compli.departement == hoteldpt.num) & (H_compli.betriebsnr == 0)).order_by(H_compli.rechnr).all():
                if h_compli_obj_list.get(h_compli._recid):
                    continue
                else:
                    h_compli_obj_list[h_compli._recid] = True

                if double_currency and curr_datum != h_compli.datum:
                    curr_datum = h_compli.datum

                    if foreign_nr != 0:

                        exrate = get_cache (Exrate, {"artnr": [(eq, foreign_nr)],"datum": [(eq, curr_datum)]})
                    else:

                        exrate = get_cache (Exrate, {"datum": [(eq, curr_datum)]})

                    if exrate:
                        rate =  to_decimal(exrate.betrag)
                    else:
                        rate =  to_decimal(exchg_rate)

                c1_list = query(c1_list_list, filters=(lambda c1_list: c1_list.datum == h_compli.datum and c1_list.dept == h_compli.departement and c1_list.rechnr == h_compli.rechnr and c1_list.p_artnr == h_compli.p_artnr), first=True)

                if not c1_list:
                    c1_list = C1_list()
                    c1_list_list.append(c1_list)

                    c1_list.datum = h_compli.datum
                    c1_list.dept = h_compli.departement
                    c1_list.deptname = hoteldpt.depart
                    c1_list.rechnr = h_compli.rechnr
                    c1_list.p_artnr = h_compli.p_artnr

                    h_bill = get_cache (H_bill, {"rechnr": [(eq, h_compli.rechnr)],"departement": [(eq, h_compli.departement)]})

                    if h_bill:
                        c1_list.name = h_bill.bilname
                    c1_list.bezeich = h_art.bezeich

                h_artikel = get_cache (H_artikel, {"artnr": [(eq, h_compli.artnr)],"departement": [(eq, h_compli.departement)]})

                artikel = get_cache (Artikel, {"artnr": [(eq, h_artikel.artnrfront)],"departement": [(eq, h_compli.departement)]})
                cost =  to_decimal("0")

                h_cost = get_cache (H_cost, {"artnr": [(eq, h_compli.artnr)],"departement": [(eq, h_compli.departement)],"datum": [(eq, h_compli.datum)],"flag": [(eq, 1)]})

                if h_cost and h_cost.betrag != 0:
                    cost =  to_decimal(h_compli.anzahl) * to_decimal(h_cost.betrag)
                    tt_cost =  to_decimal(tt_cost) + to_decimal(cost)
                    c1_list.t_cost =  to_decimal(c1_list.t_cost) + to_decimal(cost)

                if (not h_cost and h_compli.datum < billdate) or (h_cost and h_cost.betrag == 0):
                    cost =  to_decimal(h_compli.anzahl) * to_decimal(h_compli.epreis) * to_decimal(h_artikel.prozent) / to_decimal("100") * to_decimal(rate)
                    tt_cost =  to_decimal(tt_cost) + to_decimal(cost)
                    c1_list.t_cost =  to_decimal(c1_list.t_cost) + to_decimal(cost)
                c1_list.betrag =  to_decimal(c1_list.betrag) + to_decimal(h_compli.anzahl) * to_decimal(h_compli.epreis) * to_decimal(rate)
                tt_betrag =  to_decimal(tt_betrag) + to_decimal(h_compli.anzahl) * to_decimal(h_compli.epreis) * to_decimal(rate)
        curr_artnr = 0

        for c1_list in query(c1_list_list, filters=(lambda c1_list: c1_list.betrag != 0), sort_by=[("p_artnr",False),("dept",False)]):

            if curr_artnr == 0:
                curr_artnr = c1_list.p_artnr

            if curr_artnr != c1_list.p_artnr:
                c_list = C_list()
                c_list_list.append(c_list)

                nr = nr + 1
                c_list.nr = nr
                c_list.bezeich = "T O T A L"
                c_list.t_cost =  to_decimal(t_cost)
                c_list.betrag =  to_decimal(t_betrag)
                curr_artnr = c1_list.p_artnr
                t_cost =  to_decimal("0")
                t_betrag =  to_decimal("0")
            t_cost =  to_decimal(t_cost) + to_decimal(c1_list.t_cost)
            t_betrag =  to_decimal(t_betrag) + to_decimal(c1_list.betrag)
            c_list = C_list()
            c_list_list.append(c_list)

            nr = nr + 1
            c_list.nr = nr
            c_list.datum = c1_list.datum
            c_list.dept = c1_list.dept
            c_list.deptname = c1_list.deptname
            c_list.rechnr = c1_list.rechnr
            c_list.p_artnr = c1_list.p_artnr
            c_list.bezeich = c1_list.bezeich
            c_list.betrag =  to_decimal(c1_list.betrag)
            c_list.t_cost =  to_decimal(c1_list.t_cost)
            c_list.name = c1_list.name
        c_list = C_list()
        c_list_list.append(c_list)

        nr = nr + 1
        c_list.nr = nr
        c_list.bezeich = "T O T A L"
        c_list.t_cost =  to_decimal(t_cost)
        c_list.betrag =  to_decimal(t_betrag)
        c_list = C_list()
        c_list_list.append(c_list)

        nr = nr + 1
        c_list.nr = nr
        c_list.bezeich = "GRAND TOTAL"
        c_list.t_cost =  to_decimal(tt_cost)
        c_list.betrag =  to_decimal(tt_betrag)


    def journal_list2():

        nonlocal c_list_list, it_exist, n, h_artikel, artikel, hoteldpt, h_compli, exrate, h_bill, h_cost
        nonlocal foreign_nr, sorttype, from_dept, to_dept, from_date, to_date, billdate, exchg_rate, double_currency


        nonlocal c_list, c1_list
        nonlocal c_list_list, c1_list_list

        amount:Decimal = to_decimal("0.0")
        t_amount:Decimal = to_decimal("0.0")
        tot_amount:Decimal = to_decimal("0.0")
        rechnr:int = 0
        dept:int = -1
        p_artnr:int = 0
        depart:string = ""
        bezeich:string = ""
        i:int = 0
        artnr:int = 0
        datum:date = None
        curr_datum:date = None
        rate:Decimal = 1
        h_art = None
        fr_art = None
        cost:Decimal = to_decimal("0.0")
        t_cost:Decimal = to_decimal("0.0")
        t_betrag:Decimal = to_decimal("0.0")
        tt_cost:Decimal = to_decimal("0.0")
        tt_betrag:Decimal = to_decimal("0.0")
        curr_name:string = ""
        nr:int = 0
        H_art =  create_buffer("H_art",H_artikel)
        Fr_art =  create_buffer("Fr_art",Artikel)
        c_list_list.clear()
        c1_list_list.clear()
        it_exist = False

        for hoteldpt in db_session.query(Hoteldpt).filter(
                 (Hoteldpt.num >= from_dept) & (Hoteldpt.num <= to_dept)).order_by(Hoteldpt.num).all():

            h_compli_obj_list = {}
            h_compli = H_compli()
            h_art = H_artikel()
            for h_compli.datum, h_compli.departement, h_compli.rechnr, h_compli.p_artnr, h_compli.artnr, h_compli.anzahl, h_compli.epreis, h_compli._recid, h_art.artnrfront, h_art.prozent, h_art._recid, h_art.bezeich in db_session.query(H_compli.datum, H_compli.departement, H_compli.rechnr, H_compli.p_artnr, H_compli.artnr, H_compli.anzahl, H_compli.epreis, H_compli._recid, H_art.artnrfront, H_art.prozent, H_art._recid, H_art.bezeich).join(H_art,(H_art.departement == H_compli.departement) & (H_art.artnr == H_compli.p_artnr) & (H_art.artart == 11)).filter(
                     (H_compli.datum >= from_date) & (H_compli.datum <= to_date) & (H_compli.departement == hoteldpt.num) & (H_compli.betriebsnr == 0)).order_by(H_compli.rechnr).all():
                if h_compli_obj_list.get(h_compli._recid):
                    continue
                else:
                    h_compli_obj_list[h_compli._recid] = True

                if double_currency and curr_datum != h_compli.datum:
                    curr_datum = h_compli.datum

                    if foreign_nr != 0:

                        exrate = get_cache (Exrate, {"artnr": [(eq, foreign_nr)],"datum": [(eq, curr_datum)]})
                    else:

                        exrate = get_cache (Exrate, {"datum": [(eq, curr_datum)]})

                    if exrate:
                        rate =  to_decimal(exrate.betrag)
                    else:
                        rate =  to_decimal(exchg_rate)

                c1_list = query(c1_list_list, filters=(lambda c1_list: c1_list.datum == h_compli.datum and c1_list.dept == h_compli.departement and c1_list.rechnr == h_compli.rechnr and c1_list.p_artnr == h_compli.p_artnr), first=True)

                if not c1_list:
                    c1_list = C1_list()
                    c1_list_list.append(c1_list)

                    c1_list.datum = h_compli.datum
                    c1_list.dept = h_compli.departement
                    c1_list.deptname = hoteldpt.depart
                    c1_list.rechnr = h_compli.rechnr
                    c1_list.p_artnr = h_compli.p_artnr

                    h_bill = get_cache (H_bill, {"rechnr": [(eq, h_compli.rechnr)],"departement": [(eq, h_compli.departement)]})

                    if h_bill:
                        c1_list.name = h_bill.bilname
                    c1_list.bezeich = h_art.bezeich

                h_artikel = get_cache (H_artikel, {"artnr": [(eq, h_compli.artnr)],"departement": [(eq, h_compli.departement)]})

                artikel = get_cache (Artikel, {"artnr": [(eq, h_artikel.artnrfront)],"departement": [(eq, h_compli.departement)]})
                cost =  to_decimal("0")

                h_cost = get_cache (H_cost, {"artnr": [(eq, h_compli.artnr)],"departement": [(eq, h_compli.departement)],"datum": [(eq, h_compli.datum)],"flag": [(eq, 1)]})

                if h_cost and h_cost.betrag != 0:
                    cost =  to_decimal(h_compli.anzahl) * to_decimal(h_cost.betrag)
                    tt_cost =  to_decimal(tt_cost) + to_decimal(cost)
                    c1_list.t_cost =  to_decimal(c1_list.t_cost) + to_decimal(cost)

                if (not h_cost and h_compli.datum < billdate) or (h_cost and h_cost.betrag == 0):
                    cost =  to_decimal(h_compli.anzahl) * to_decimal(h_compli.epreis) * to_decimal(h_artikel.prozent) / to_decimal("100") * to_decimal(rate)
                    tt_cost =  to_decimal(tt_cost) + to_decimal(cost)
                    c1_list.t_cost =  to_decimal(c1_list.t_cost) + to_decimal(cost)
                c1_list.betrag =  to_decimal(c1_list.betrag) + to_decimal(h_compli.anzahl) * to_decimal(h_compli.epreis) * to_decimal(rate)
                tt_betrag =  to_decimal(tt_betrag) + to_decimal(h_compli.anzahl) * to_decimal(h_compli.epreis) * to_decimal(rate)
        curr_name = ""

        for c1_list in query(c1_list_list, filters=(lambda c1_list: c1_list.betrag != 0), sort_by=[("name",False)]):

            if curr_name == "":
                curr_name = c1_list.name

            if curr_name != c1_list.name:
                c_list = C_list()
                c_list_list.append(c_list)

                nr = nr + 1
                c_list.nr = nr
                c_list.bezeich = "T O T A L"
                c_list.t_cost =  to_decimal(t_cost)
                c_list.betrag =  to_decimal(t_betrag)
                curr_name = c1_list.name
                t_cost =  to_decimal("0")
                t_betrag =  to_decimal("0")
            t_cost =  to_decimal(t_cost) + to_decimal(c1_list.t_cost)
            t_betrag =  to_decimal(t_betrag) + to_decimal(c1_list.betrag)
            c_list = C_list()
            c_list_list.append(c_list)

            nr = nr + 1
            c_list.nr = nr
            c_list.datum = c1_list.datum
            c_list.dept = c1_list.dept
            c_list.deptname = c1_list.deptname
            c_list.rechnr = c1_list.rechnr
            c_list.p_artnr = c1_list.p_artnr
            c_list.bezeich = c1_list.bezeich
            c_list.betrag =  to_decimal(c1_list.betrag)
            c_list.t_cost =  to_decimal(c1_list.t_cost)
            c_list.name = c1_list.name
        c_list = C_list()
        c_list_list.append(c_list)

        nr = nr + 1
        c_list.nr = nr
        c_list.bezeich = "T O T A L"
        c_list.t_cost =  to_decimal(t_cost)
        c_list.betrag =  to_decimal(t_betrag)
        c_list = C_list()
        c_list_list.append(c_list)

        nr = nr + 1
        c_list.nr = nr
        c_list.bezeich = "GRAND TOTAL"
        c_list.t_cost =  to_decimal(tt_cost)
        c_list.betrag =  to_decimal(tt_betrag)

    if sorttype == 2:
        journal_list1()

    elif sorttype == 3:
        journal_list2()

    return generate_output()