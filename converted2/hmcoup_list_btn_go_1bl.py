#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Hoteldpt, H_artikel, H_journal, Htparam, Exrate, H_bill, Kellner, Artikel, H_bill_line, H_cost

def hmcoup_list_btn_go_1bl(double_currency:bool, foreign_nr:int, exchg_rate:Decimal, billdate:date, from_dept:int, to_dept:int, from_date:date, to_date:date):

    prepare_cache ([Hoteldpt, H_artikel, H_journal, Htparam, Exrate, H_bill, Kellner, Artikel, H_bill_line, H_cost])

    c_list_data = []
    it_exist:bool = False
    hoteldpt = h_artikel = h_journal = htparam = exrate = h_bill = kellner = artikel = h_bill_line = h_cost = None

    h_list = c_list = None

    h_list_data, H_list = create_model("H_list", {"rechnr":int, "departement":int, "datum":date, "betrag":Decimal, "bezeich":string})
    c_list_data, C_list = create_model("C_list", {"nr":int, "datum":date, "dept":int, "deptname":string, "rechnr":int, "pax":int, "bezeich":string, "f_betrag":Decimal, "f_cost":Decimal, "b_betrag":Decimal, "b_cost":Decimal, "betrag":Decimal, "t_cost":Decimal, "o_cost":Decimal, "usr_id":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal c_list_data, it_exist, hoteldpt, h_artikel, h_journal, htparam, exrate, h_bill, kellner, artikel, h_bill_line, h_cost
        nonlocal double_currency, foreign_nr, exchg_rate, billdate, from_dept, to_dept, from_date, to_date


        nonlocal h_list, c_list
        nonlocal h_list_data, c_list_data

        return {"c-list": c_list_data}

    def create_mplist():

        nonlocal c_list_data, it_exist, hoteldpt, h_artikel, h_journal, htparam, exrate, h_bill, kellner, artikel, h_bill_line, h_cost
        nonlocal double_currency, foreign_nr, exchg_rate, billdate, from_dept, to_dept, from_date, to_date


        nonlocal h_list, c_list
        nonlocal h_list_data, c_list_data


        h_list_data.clear()

        for hoteldpt in db_session.query(Hoteldpt).filter(
                 (Hoteldpt.num >= from_dept) & (Hoteldpt.num <= to_dept)).order_by(Hoteldpt.num).all():

            h_journal_obj_list = {}
            h_journal = H_journal()
            h_artikel = H_artikel()
            for h_journal.rechnr, h_journal.departement, h_journal.bill_datum, h_journal.bezeich, h_journal.betrag, h_journal._recid, h_artikel.artnr, h_artikel.departement, h_artikel.prozent, h_artikel._recid in db_session.query(H_journal.rechnr, H_journal.departement, H_journal.bill_datum, H_journal.bezeich, H_journal.betrag, H_journal._recid, H_artikel.artnr, H_artikel.departement, H_artikel.prozent, H_artikel._recid).join(H_artikel,(H_artikel.artnr == H_journal.artnr) & (H_artikel.departement == hoteldpt.num) & (H_artikel.artart == 12)).filter(
                     (H_journal.bill_datum >= from_date) & (H_journal.bill_datum <= to_date) & (H_journal.departement == hoteldpt.num)).order_by(H_journal.rechnr).all():
                if h_journal_obj_list.get(h_journal._recid):
                    continue
                else:
                    h_journal_obj_list[h_journal._recid] = True

                h_list = query(h_list_data, filters=(lambda h_list: h_list.rechnr == h_journal.rechnr and h_list.departement == h_journal.departement and h_list.datum == h_journal.bill_datum and h_list.bezeich == h_journal.bezeich), first=True)

                if not h_list:
                    h_list = H_list()
                    h_list_data.append(h_list)

                    h_list.rechnr = h_journal.rechnr
                    h_list.departement = h_journal.departement
                    h_list.datum = h_journal.bill_datum
                    h_list.bezeich = h_journal.bezeich
                h_list.betrag =  to_decimal(h_list.betrag) + to_decimal(h_journal.betrag)

        for h_list in query(h_list_data, filters=(lambda h_list: h_list.betrag == 0)):
            h_list_data.remove(h_list)


    def journal_list():

        nonlocal c_list_data, it_exist, hoteldpt, h_artikel, h_journal, htparam, exrate, h_bill, kellner, artikel, h_bill_line, h_cost
        nonlocal double_currency, foreign_nr, exchg_rate, billdate, from_dept, to_dept, from_date, to_date


        nonlocal h_list, c_list
        nonlocal h_list_data, c_list_data

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
        f_cost:Decimal = to_decimal("0.0")
        b_cost:Decimal = to_decimal("0.0")
        o_cost:Decimal = to_decimal("0.0")
        cost:Decimal = to_decimal("0.0")
        t_cost:Decimal = to_decimal("0.0")
        tf_cost:Decimal = to_decimal("0.0")
        tb_cost:Decimal = to_decimal("0.0")
        to_cost:Decimal = to_decimal("0.0")
        t_betrag:Decimal = to_decimal("0.0")
        tf_betrag:Decimal = to_decimal("0.0")
        tb_betrag:Decimal = to_decimal("0.0")
        tt_cost:Decimal = to_decimal("0.0")
        ttf_cost:Decimal = to_decimal("0.0")
        ttb_cost:Decimal = to_decimal("0.0")
        tto_cost:Decimal = to_decimal("0.0")
        tt_betrag:Decimal = to_decimal("0.0")
        ttf_betrag:Decimal = to_decimal("0.0")
        ttb_betrag:Decimal = to_decimal("0.0")
        f_endkum:int = 0
        b_endkum:int = 0
        nr:int = 0
        H_art =  create_buffer("H_art",H_artikel)
        c_list_data.clear()
        it_exist = False

        htparam = get_cache (Htparam, {"paramnr": [(eq, 862)]})
        f_endkum = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 892)]})
        b_endkum = htparam.finteger

        for hoteldpt in db_session.query(Hoteldpt).filter(
                 (Hoteldpt.num >= from_dept) & (Hoteldpt.num <= to_dept)).order_by(Hoteldpt.num).all():
            t_cost =  to_decimal("0")
            tf_cost =  to_decimal("0")
            tb_cost =  to_decimal("0")
            to_cost =  to_decimal("0")
            t_betrag =  to_decimal("0")

            for h_list in query(h_list_data, filters=(lambda h_list: h_list.datum >= from_date and h_list.datum <= to_date and h_list.departement == hoteldpt.num), sort_by=[("rechnr",False)]):

                if double_currency and curr_datum != h_list.datum:
                    curr_datum = h_list.datum

                    if foreign_nr != 0:

                        exrate = get_cache (Exrate, {"artnr": [(eq, foreign_nr)],"datum": [(eq, curr_datum)]})
                    else:

                        exrate = get_cache (Exrate, {"datum": [(eq, curr_datum)]})

                    if exrate:
                        rate =  to_decimal(exrate.betrag)
                    else:
                        rate =  to_decimal(exchg_rate)

                h_bill = get_cache (H_bill, {"rechnr": [(eq, h_list.rechnr)],"departement": [(eq, h_list.departement)]})

                c_list = query(c_list_data, filters=(lambda c_list: c_list.datum == h_list.datum and c_list.dept == h_list.departement and c_list.rechnr == h_list.rechnr), first=True)

                if not c_list:
                    c_list = C_list()
                    c_list_data.append(c_list)

                    nr = nr + 1
                    c_list.nr = nr
                    c_list.datum = h_list.datum
                    c_list.dept = h_list.departement
                    c_list.deptname = hoteldpt.depart
                    c_list.rechnr = h_list.rechnr
                    c_list.bezeich = h_list.bezeich

                    if h_bill:

                        kellner = get_cache (Kellner, {"kellner_nr": [(eq, h_bill.kellner_nr)]})

                        if kellner:
                            c_list.usr_id = kellner.kellnername
                        else:
                            c_list.usr_id = ""
                        c_list.pax = h_bill.belegung

                h_bill_line_obj_list = {}
                h_bill_line = H_bill_line()
                h_artikel = H_artikel()
                artikel = Artikel()
                for h_bill_line.anzahl, h_bill_line.epreis, h_bill_line._recid, h_artikel.artnr, h_artikel.departement, h_artikel.prozent, h_artikel._recid, artikel.endkum, artikel._recid in db_session.query(H_bill_line.anzahl, H_bill_line.epreis, H_bill_line._recid, H_artikel.artnr, H_artikel.departement, H_artikel.prozent, H_artikel._recid, Artikel.endkum, Artikel._recid).join(H_artikel,(H_artikel.artnr == H_bill_line.artnr) & (H_artikel.departement == h_list.departement) & (H_artikel.artart == 0)).join(Artikel,(Artikel.artnr == H_artikel.artnrfront) & (Artikel.departement == H_artikel.departement)).filter(
                         (H_bill_line.rechnr == h_list.rechnr) & (H_bill_line.departement == h_list.departement) & (H_bill_line.bill_datum == h_list.datum)).order_by(H_bill_line._recid).all():
                    if h_bill_line_obj_list.get(h_bill_line._recid):
                        continue
                    else:
                        h_bill_line_obj_list[h_bill_line._recid] = True


                    cost =  to_decimal("0")
                    f_cost =  to_decimal("0")
                    b_cost =  to_decimal("0")
                    o_cost =  to_decimal("0")

                    h_cost = get_cache (H_cost, {"artnr": [(eq, h_artikel.artnr)],"departement": [(eq, h_artikel.departement)],"datum": [(eq, h_list.datum)],"flag": [(eq, 1)]})

                    if h_cost and h_cost.betrag != 0:
                        cost =  to_decimal(h_bill_line.anzahl) * to_decimal(h_cost.betrag)
                        t_cost =  to_decimal(t_cost) + to_decimal(cost)
                        tt_cost =  to_decimal(tt_cost) + to_decimal(cost)

                        if artikel.endkum == f_endkum:
                            f_cost =  to_decimal(cost)
                            tf_cost =  to_decimal(tf_cost) + to_decimal(f_cost)
                            ttf_cost =  to_decimal(ttf_cost) + to_decimal(f_cost)

                        elif artikel.endkum == b_endkum:
                            b_cost =  to_decimal(cost)
                            tb_cost =  to_decimal(tb_cost) + to_decimal(b_cost)
                            ttb_cost =  to_decimal(ttb_cost) + to_decimal(b_cost)
                        c_list.f_cost =  to_decimal(c_list.f_cost) + to_decimal(f_cost)
                        c_list.b_cost =  to_decimal(c_list.b_cost) + to_decimal(b_cost)
                        c_list.o_cost =  to_decimal(c_list.o_cost) + to_decimal(o_cost)
                        c_list.t_cost =  to_decimal(c_list.t_cost) + to_decimal(cost)

                    if (not h_cost and h_list.datum <= billdate) or (h_cost and h_cost.betrag == 0):
                        cost =  to_decimal(h_bill_line.anzahl) * to_decimal(h_bill_line.epreis) * to_decimal(h_artikel.prozent) / to_decimal("100") * to_decimal(rate)
                        t_cost =  to_decimal(t_cost) + to_decimal(cost)
                        tt_cost =  to_decimal(tt_cost) + to_decimal(cost)

                        if artikel.endkum == f_endkum:
                            f_cost =  to_decimal(cost)
                            tf_cost =  to_decimal(tf_cost) + to_decimal(cost)
                            ttf_cost =  to_decimal(ttf_cost) + to_decimal(cost)

                        elif artikel.endkum == b_endkum:
                            b_cost =  to_decimal(cost)
                            tb_cost =  to_decimal(tb_cost) + to_decimal(cost)
                            ttb_cost =  to_decimal(ttb_cost) + to_decimal(cost)
                        c_list.f_cost =  to_decimal(c_list.f_cost) + to_decimal(f_cost)
                        c_list.b_cost =  to_decimal(c_list.b_cost) + to_decimal(b_cost)
                        c_list.o_cost =  to_decimal(c_list.o_cost) + to_decimal(o_cost)
                        c_list.t_cost =  to_decimal(c_list.t_cost) + to_decimal(cost)
                    c_list.betrag =  to_decimal(c_list.betrag) + to_decimal(h_bill_line.anzahl) * to_decimal(h_bill_line.epreis) * to_decimal(rate)
                    t_betrag =  to_decimal(t_betrag) + to_decimal(h_bill_line.anzahl) * to_decimal(h_bill_line.epreis) * to_decimal(rate)
                    tt_betrag =  to_decimal(tt_betrag) + to_decimal(h_bill_line.anzahl) * to_decimal(h_bill_line.epreis) * to_decimal(rate)

                    if artikel.endkum == f_endkum:
                        c_list.f_betrag =  to_decimal(c_list.f_betrag) + to_decimal(h_bill_line.anzahl) * to_decimal(h_bill_line.epreis) * to_decimal(rate)
                        tf_betrag =  to_decimal(tf_betrag) + to_decimal(h_bill_line.anzahl) * to_decimal(h_bill_line.epreis) * to_decimal(rate)
                        ttf_betrag =  to_decimal(ttf_betrag) + to_decimal(h_bill_line.anzahl) * to_decimal(h_bill_line.epreis) * to_decimal(rate)

                    elif artikel.endkum == b_endkum:
                        c_list.b_betrag =  to_decimal(c_list.b_betrag) + to_decimal(h_bill_line.anzahl) * to_decimal(h_bill_line.epreis) * to_decimal(rate)
                        tb_betrag =  to_decimal(tb_betrag) + to_decimal(h_bill_line.anzahl) * to_decimal(h_bill_line.epreis) * to_decimal(rate)
                        ttb_betrag =  to_decimal(ttb_betrag) + to_decimal(h_bill_line.anzahl) * to_decimal(h_bill_line.epreis) * to_decimal(rate)

            if t_betrag != 0:
                c_list = C_list()
                c_list_data.append(c_list)

                nr = nr + 1
                c_list.nr = nr
                c_list.bezeich = "T O T A L"
                c_list.f_cost =  to_decimal(tf_cost)
                c_list.b_cost =  to_decimal(tb_cost)
                c_list.o_cost =  to_decimal(to_cost)
                c_list.t_cost =  to_decimal(t_cost)
                c_list.betrag =  to_decimal(t_betrag)
                c_list.f_betrag =  to_decimal(tf_betrag)
                c_list.b_betrag =  to_decimal(tb_betrag)
        c_list = C_list()
        c_list_data.append(c_list)

        nr = nr + 1
        c_list.nr = nr
        c_list.bezeich = "GRAND TOTAL"
        c_list.f_cost =  to_decimal(ttf_cost)
        c_list.b_cost =  to_decimal(ttb_cost)
        c_list.o_cost =  to_decimal(tto_cost)
        c_list.t_cost =  to_decimal(tt_cost)
        c_list.betrag =  to_decimal(tt_betrag)
        c_list.f_betrag =  to_decimal(ttf_betrag)
        c_list.b_betrag =  to_decimal(ttb_betrag)

        for c_list in query(c_list_data):

            if c_list.betrag == 0:
                c_list_data.remove(c_list)


    create_mplist()
    journal_list()

    return generate_output()