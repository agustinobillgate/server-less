#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import H_artikel, Htparam, Hoteldpt, H_compli, H_bill, H_journal, Artikel, H_cost, Queasy, Exrate, H_bill_line

def hcompli_list_2bl(pvilanguage:int, gname:string, sorttype:int, from_dept:int, to_dept:int, from_date:date, to_date:date, double_currency:bool, exchg_rate:Decimal, billdate:date, mi_detail1:bool, sm_disp1:bool, foreign_nr:int, artnr:int):

    prepare_cache ([H_artikel, Htparam, Hoteldpt, H_compli, H_bill, Artikel, H_cost, Queasy, Exrate, H_bill_line])

    c_list_data = []
    it_exist:bool = False
    curr_name:string = ""
    guestname:string = ""
    lvcarea:string = "hcompli-list"
    h_artikel = htparam = hoteldpt = h_compli = h_bill = h_journal = artikel = h_cost = queasy = exrate = h_bill_line = None

    c_list = c1_list = c2_list = s_list = s_list = s_list = s_list = None

    c_list_data, C_list = create_model("C_list", {"flag":int, "nr":int, "datum":date, "dept":int, "deptname":string, "rechnr":int, "name":string, "artnr":int, "p_artnr":int, "bezeich":string, "qty":int, "betrag":Decimal, "f_betrag":Decimal, "f_cost":Decimal, "b_betrag":Decimal, "b_cost":Decimal, "o_betrag":Decimal, "o_cost":Decimal, "t_cost":Decimal, "creditlimit":Decimal, "officer":string, "detailed":bool})
    c1_list_data, C1_list = create_model_like(C_list)

    C2_list = C1_list
    c2_list_data = c1_list_data

    db_session = local_storage.db_session

    def generate_output():
        nonlocal c_list_data, it_exist, curr_name, guestname, lvcarea, h_artikel, htparam, hoteldpt, h_compli, h_bill, h_journal, artikel, h_cost, queasy, exrate, h_bill_line
        nonlocal pvilanguage, gname, sorttype, from_dept, to_dept, from_date, to_date, double_currency, exchg_rate, billdate, mi_detail1, sm_disp1, foreign_nr, artnr
        nonlocal c2_list


        nonlocal c_list, c1_list, c2_list, s_list, s_list, s_list, s_list
        nonlocal c_list_data, c1_list_data

        return {"c-list": c_list_data}

    def journal_list():

        nonlocal c_list_data, guestname, lvcarea, h_artikel, htparam, hoteldpt, h_compli, h_bill, h_journal, artikel, h_cost, queasy, exrate, h_bill_line
        nonlocal pvilanguage, gname, sorttype, from_dept, to_dept, from_date, to_date, double_currency, exchg_rate, billdate, mi_detail1, sm_disp1, foreign_nr, c2_list


        nonlocal c_list, c1_list, c2_list, s_list, s_list, s_list, s_list
        nonlocal c_list_data, c1_list_data

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
        qty:int = 0
        t_qty:int = 0
        tt_qty:int = 0
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
        to_betrag:Decimal = to_decimal("0.0")
        tt_cost:Decimal = to_decimal("0.0")
        ttf_cost:Decimal = to_decimal("0.0")
        ttb_cost:Decimal = to_decimal("0.0")
        tto_cost:Decimal = to_decimal("0.0")
        tt_betrag:Decimal = to_decimal("0.0")
        ttf_betrag:Decimal = to_decimal("0.0")
        ttb_betrag:Decimal = to_decimal("0.0")
        tto_betrag:Decimal = to_decimal("0.0")
        f_endkum:int = 0
        b_endkum:int = 0
        curr_name:string = ""
        nr:int = 0
        it_exist:bool = False
        flag_artnr:string = ""
        h_art = None
        S_list = C_list
        s_list_data = c_list_data
        H_art =  create_buffer("H_art",H_artikel)

        if gname != "":
            journal_gname()

            return

        if sorttype == 2:
            journal_list1()

            return

        if sorttype == 3:
            journal_list2()

            return
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
            tf_betrag =  to_decimal("0")
            tb_betrag =  to_decimal("0")
            to_betrag =  to_decimal("0")
            t_qty = 0

            h_compli_obj_list = {}
            h_compli = H_compli()
            h_art = H_artikel()
            for h_compli.artnr, h_compli.datum, h_compli.departement, h_compli.rechnr, h_compli.p_artnr, h_compli.anzahl, h_compli.epreis, h_compli._recid, h_art.artnrfront, h_art.prozent, h_art.artnr, h_art.bezeich, h_art.epreis1, h_art.artart, h_art._recid in db_session.query(H_compli.artnr, H_compli.datum, H_compli.departement, H_compli.rechnr, H_compli.p_artnr, H_compli.anzahl, H_compli.epreis, H_compli._recid, H_art.artnrfront, H_art.prozent, H_art.artnr, H_art.bezeich, H_art.epreis1, H_art.artart, H_art._recid).join(H_art,(H_art.departement == H_compli.departement) & (H_art.artnr == H_compli.p_artnr) & (H_art.artart == 11)).filter(
                     (H_compli.datum >= from_date) & (H_compli.datum <= to_date) & (H_compli.departement == hoteldpt.num) & (H_compli.betriebsnr == 0)).order_by(H_compli.rechnr).all():
                if h_compli_obj_list.get(h_compli._recid):
                    continue
                else:
                    h_compli_obj_list[h_compli._recid] = True


                flag_artnr = flag_artnr + "," + to_string(h_compli.artnr)

                if double_currency and curr_datum != h_compli.datum:
                    curr_datum = h_compli.datum
                    find_exrate(curr_datum)

                    if exrate:
                        rate =  to_decimal(exrate.betrag)
                    else:
                        rate =  to_decimal(exchg_rate)

                c1_list = query(c1_list_data, filters=(lambda c1_list: c1_list.datum == h_compli.datum and c1_list.dept == h_compli.departement and c1_list.rechnr == h_compli.rechnr and c1_list.p_artnr == h_compli.p_artnr), first=True)

                if not c1_list:
                    c1_list = C1_list()
                    c1_list_data.append(c1_list)

                    c1_list.datum = h_compli.datum
                    c1_list.dept = h_compli.departement
                    c1_list.deptname = hoteldpt.depart
                    c1_list.rechnr = h_compli.rechnr
                    c1_list.p_artnr = h_compli.p_artnr

                    h_bill = get_cache (H_bill, {"rechnr": [(eq, h_compli.rechnr)],"departement": [(eq, h_compli.departement)]})

                    if h_bill:
                        c1_list.name = h_bill.bilname
                    else:

                        h_journal = get_cache (H_journal, {"bill_datum": [(eq, h_compli.datum)],"departement": [(eq, h_compli.departement)],"segmentcode": [(eq, h_compli.p_artnr)],"zeit": [(ge, 0)]})

                        if h_journal and h_journal.aendertext != "":
                            c1_list.name = h_journal.aendertext
                    c1_list.bezeich = h_art.bezeich

                h_artikel = get_cache (H_artikel, {"artnr": [(eq, h_compli.artnr)],"departement": [(eq, h_compli.departement)]})

                artikel = get_cache (Artikel, {"artnr": [(eq, h_artikel.artnrfront)],"departement": [(eq, h_compli.departement)]})
                cost =  to_decimal("0")
                f_cost =  to_decimal("0")
                b_cost =  to_decimal("0")
                o_cost =  to_decimal("0")

                h_cost = get_cache (H_cost, {"artnr": [(eq, h_compli.artnr)],"departement": [(eq, h_compli.departement)],"datum": [(eq, h_compli.datum)],"flag": [(eq, 1)]})

                if h_cost and h_cost.betrag != 0:
                    cost =  to_decimal(h_compli.anzahl) * to_decimal(h_cost.betrag)
                    cost = cost_correction(cost)
                    cost = to_decimal(round(cost , 2))
                    tt_cost =  to_decimal(tt_cost) + to_decimal(cost)

                    if artikel.umsatzart == 3 or artikel.umsatzart == 5:
                        f_cost =  to_decimal(cost)
                        ttf_cost =  to_decimal(ttf_cost) + to_decimal(cost)

                    elif artikel.umsatzart == 6:
                        b_cost =  to_decimal(cost)
                        ttb_cost =  to_decimal(ttb_cost) + to_decimal(cost)
                    else:
                        o_cost =  to_decimal(cost)
                        tto_cost =  to_decimal(tto_cost) + to_decimal(cost)
                    c1_list.f_cost =  to_decimal(c1_list.f_cost) + to_decimal(f_cost)
                    c1_list.b_cost =  to_decimal(c1_list.b_cost) + to_decimal(b_cost)
                    c1_list.o_cost =  to_decimal(c1_list.o_cost) + to_decimal(o_cost)
                    c1_list.t_cost =  to_decimal(c1_list.t_cost) + to_decimal(cost)

                elif (not h_cost and h_compli.datum < billdate) or (h_cost and h_cost.betrag == 0):
                    cost =  to_decimal(h_compli.anzahl) * to_decimal(h_compli.epreis) * to_decimal(h_artikel.prozent) / to_decimal("100") * to_decimal(rate)
                    cost = to_decimal(round(cost , 2))
                    tt_cost =  to_decimal(tt_cost) + to_decimal(cost)

                    if artikel.umsatzart == 3 or artikel.umsatzart == 5:
                        f_cost =  to_decimal(cost)
                        ttf_cost =  to_decimal(ttf_cost) + to_decimal(cost)

                    elif artikel.umsatzart == 6:
                        b_cost =  to_decimal(cost)
                        ttb_cost =  to_decimal(ttb_cost) + to_decimal(cost)
                    else:
                        o_cost =  to_decimal(cost)
                        tto_cost =  to_decimal(tto_cost) + to_decimal(cost)
                    c1_list.f_cost =  to_decimal(c1_list.f_cost) + to_decimal(f_cost)
                    c1_list.b_cost =  to_decimal(c1_list.b_cost) + to_decimal(b_cost)
                    c1_list.o_cost =  to_decimal(c1_list.o_cost) + to_decimal(o_cost)
                    c1_list.t_cost =  to_decimal(c1_list.t_cost) + to_decimal(cost)
                c1_list.betrag =  to_decimal(c1_list.betrag) + to_decimal(h_compli.anzahl) * to_decimal(h_compli.epreis) * to_decimal(rate)
                tt_betrag =  to_decimal(tt_betrag) + to_decimal(h_compli.anzahl) * to_decimal(h_compli.epreis) * to_decimal(rate)

                if artikel.umsatzart == 3 or artikel.umsatzart == 5:
                    c1_list.f_betrag =  to_decimal(c1_list.f_betrag) + to_decimal(h_compli.anzahl) * to_decimal(h_compli.epreis) * to_decimal(rate)
                    ttf_betrag =  to_decimal(ttf_betrag) + to_decimal(h_compli.anzahl) * to_decimal(h_compli.epreis) * to_decimal(rate)

                elif artikel.umsatzart == 6:
                    c1_list.b_betrag =  to_decimal(c1_list.b_betrag) + to_decimal(h_compli.anzahl) * to_decimal(h_compli.epreis) * to_decimal(rate)
                    ttb_betrag =  to_decimal(ttb_betrag) + to_decimal(h_compli.anzahl) * to_decimal(h_compli.epreis) * to_decimal(rate)
                else:
                    c1_list.o_betrag =  to_decimal(c1_list.o_betrag) + to_decimal(h_compli.anzahl) * to_decimal(h_compli.epreis) * to_decimal(rate)
                    tto_betrag =  to_decimal(tto_betrag) + to_decimal(h_compli.anzahl) * to_decimal(h_compli.epreis) * to_decimal(rate)

                if mi_detail1:

                    c2_list = query(c2_list_data, filters=(lambda c2_list: c2_list.datum == h_compli.datum and c2_list.dept == h_compli.departement and c2_list.rechnr == h_compli.rechnr and c2_list.artnr == h_compli.artnr), first=True)

                    if not c2_list:

                        h_artikel = get_cache (H_artikel, {"artnr": [(eq, h_compli.artnr)],"departement": [(eq, h_compli.departement)]})
                        c2_list = C2_list()
                        c2_list_data.append(c2_list)

                        c2_list.detailed = True
                        c2_list.datum = h_compli.datum
                        c2_list.dept = h_compli.departement
                        c2_list.deptname = hoteldpt.depart
                        c2_list.rechnr = h_compli.rechnr
                        c2_list.artnr = h_artikel.artnr
                        c2_list.bezeich = h_artikel.bezeich
                        c2_list.name = c1_list.name


                    c2_list.qty = c2_list.qty + h_compli.anzahl
                    c2_list.f_cost =  to_decimal(c2_list.f_cost) + to_decimal(f_cost)
                    c2_list.b_cost =  to_decimal(c2_list.b_cost) + to_decimal(b_cost)
                    c2_list.o_cost =  to_decimal(c2_list.o_cost) + to_decimal(o_cost)
                    c2_list.t_cost =  to_decimal(c2_list.t_cost) + to_decimal(cost)
                    c2_list.betrag =  to_decimal(c2_list.betrag) + to_decimal(h_compli.anzahl) * to_decimal(h_compli.epreis) * to_decimal(rate)

                    if artikel.umsatzart == 3 or artikel.umsatzart == 5:
                        c2_list.f_betrag =  to_decimal(c2_list.f_betrag) + to_decimal(h_compli.anzahl) * to_decimal(h_compli.epreis) * to_decimal(rate)

                    elif artikel.umsatzart == 6:
                        c2_list.b_betrag =  to_decimal(c2_list.b_betrag) + to_decimal(h_compli.anzahl) * to_decimal(h_compli.epreis) * to_decimal(rate)
                    else:
                        c2_list.o_betrag =  to_decimal(c2_list.o_betrag) + to_decimal(h_compli.anzahl) * to_decimal(h_compli.epreis) * to_decimal(rate)

        if mi_detail1 == False:
            curr_name = "???"
            b_cost =  to_decimal("0")
            o_cost =  to_decimal("0")

            for c1_list in query(c1_list_data, filters=(lambda c1_list: c1_list.betrag != 0), sort_by=[("rechnr",False),("name",False),("datum",False),("dept",True)]):

                if not c1_list.detailed:
                    t_cost =  to_decimal(t_cost) + to_decimal(c1_list.t_cost)
                    tf_cost =  to_decimal(tf_cost) + to_decimal(c1_list.f_cost)
                    tb_cost =  to_decimal(tb_cost) + to_decimal(c1_list.b_cost)
                    to_cost =  to_decimal(to_cost) + to_decimal(c1_list.o_cost)
                    t_betrag =  to_decimal(t_betrag) + to_decimal(c1_list.betrag)
                    tf_betrag =  to_decimal(tf_betrag) + to_decimal(c1_list.f_betrag)
                    tb_betrag =  to_decimal(tb_betrag) + to_decimal(c1_list.b_betrag)
                    to_betrag =  to_decimal(to_betrag) + to_decimal(c1_list.o_betrag)
                c_list = C_list()
                c_list_data.append(c_list)

                nr = nr + 1
                c_list.nr = nr
                c_list.datum = c1_list.datum
                c_list.dept = c1_list.dept
                c_list.deptname = c1_list.deptname
                c_list.rechnr = c1_list.rechnr
                c_list.artnr = c1_list.artnr
                c_list.p_artnr = c1_list.p_artnr
                c_list.bezeich = c1_list.bezeich
                c_list.betrag =  to_decimal(c1_list.betrag)
                c_list.f_betrag =  to_decimal(c1_list.f_betrag)
                c_list.b_betrag =  to_decimal(c1_list.b_betrag)
                c_list.o_betrag =  to_decimal(c1_list.o_betrag)
                c_list.f_cost =  to_decimal(c1_list.f_cost)
                c_list.b_cost =  to_decimal(c1_list.b_cost)
                c_list.o_cost =  to_decimal(c1_list.o_cost)
                c_list.t_cost =  to_decimal(c1_list.t_cost)
                c_list.name = c1_list.name

        if mi_detail1 :
            curr_name = "???"
            b_cost =  to_decimal("0")
            o_cost =  to_decimal("0")

            for c1_list in query(c1_list_data, filters=(lambda c1_list: c1_list.betrag != 0), sort_by=[("rechnr",False),("p_artnr",False),("name",False),("datum",False),("dept",False),("artnr",True)]):

                if curr_name.lower()  == ("???").lower() :
                    curr_name = c1_list.name

                if curr_name != c1_list.name:
                    c_list = C_list()
                    c_list_data.append(c_list)

                    nr = nr + 1
                    c_list.nr = nr
                    c_list.bezeich = "T O T A L"
                    c_list.qty = t_qty
                    c_list.f_cost =  to_decimal(tf_cost)
                    c_list.b_cost =  to_decimal(tb_cost)
                    c_list.o_cost =  to_decimal(to_cost)
                    c_list.t_cost =  to_decimal(t_cost)
                    c_list.betrag =  to_decimal(t_betrag)
                    c_list.f_betrag =  to_decimal(tf_betrag)
                    c_list.b_betrag =  to_decimal(tb_betrag)
                    c_list.o_betrag =  to_decimal(to_betrag)
                    tt_qty = tt_qty + t_qty
                    t_qty = 0

                    if sm_disp1:

                        queasy = get_cache (Queasy, {"key": [(eq, 105)],"char1": [(eq, curr_name)]})

                        if queasy:
                            it_exist = True
                            c_list.creditlimit =  to_decimal(queasy.deci3)
                            c_list.officer = curr_name
                    curr_name = c1_list.name
                    t_cost =  to_decimal("0")
                    tf_cost =  to_decimal("0")
                    tb_cost =  to_decimal("0")
                    to_cost =  to_decimal("0")
                    t_betrag =  to_decimal("0")
                    tf_betrag =  to_decimal("0")
                    tb_betrag =  to_decimal("0")
                    to_betrag =  to_decimal("0")

                if not c1_list.detailed:
                    t_cost =  to_decimal(t_cost) + to_decimal(c1_list.t_cost)
                    tf_cost =  to_decimal(tf_cost) + to_decimal(c1_list.f_cost)
                    tb_cost =  to_decimal(tb_cost) + to_decimal(c1_list.b_cost)
                    to_cost =  to_decimal(to_cost) + to_decimal(c1_list.o_cost)
                    t_betrag =  to_decimal(t_betrag) + to_decimal(c1_list.betrag)
                    tf_betrag =  to_decimal(tf_betrag) + to_decimal(c1_list.f_betrag)
                    tb_betrag =  to_decimal(tb_betrag) + to_decimal(c1_list.b_betrag)
                    to_betrag =  to_decimal(to_betrag) + to_decimal(c1_list.o_betrag)
                c_list = C_list()
                c_list_data.append(c_list)

                nr = nr + 1
                c_list.nr = nr
                c_list.datum = c1_list.datum
                c_list.dept = c1_list.dept
                c_list.deptname = c1_list.deptname
                c_list.rechnr = c1_list.rechnr
                c_list.artnr = c1_list.artnr
                c_list.p_artnr = c1_list.p_artnr
                c_list.bezeich = c1_list.bezeich
                c_list.betrag =  to_decimal(c1_list.betrag)
                c_list.f_betrag =  to_decimal(c1_list.f_betrag)
                c_list.b_betrag =  to_decimal(c1_list.b_betrag)
                c_list.o_betrag =  to_decimal(c1_list.o_betrag)
                c_list.f_cost =  to_decimal(c1_list.f_cost)
                c_list.b_cost =  to_decimal(c1_list.b_cost)
                c_list.o_cost =  to_decimal(c1_list.o_cost)
                c_list.t_cost =  to_decimal(c1_list.t_cost)
                c_list.name = c1_list.name

                if p_artnr == 0:
                    qty = c1_list.qty
                    c_list.qty = c1_list.qty
                    t_qty = t_qty + qty
        c_list = C_list()
        c_list_data.append(c_list)

        nr = nr + 1
        c_list.nr = nr
        c_list.bezeich = "T O T A L"
        c_list.qty = t_qty
        c_list.f_cost =  to_decimal(tf_cost)
        c_list.b_cost =  to_decimal(tb_cost)
        c_list.o_cost =  to_decimal(to_cost)
        c_list.t_cost =  to_decimal(t_cost)
        c_list.betrag =  to_decimal(t_betrag)
        c_list.f_betrag =  to_decimal(tf_betrag)
        c_list.b_betrag =  to_decimal(tb_betrag)
        c_list.o_betrag =  to_decimal(to_betrag)
        tt_qty = tt_qty + t_qty
        t_qty = 0

        if sm_disp1:

            queasy = get_cache (Queasy, {"key": [(eq, 105)],"char1": [(eq, curr_name)]})

            if queasy:
                it_exist = True
                c_list.creditlimit =  to_decimal(queasy.deci3)
                c_list.officer = curr_name
        c_list = C_list()
        c_list_data.append(c_list)

        nr = nr + 1
        c_list.nr = nr
        c_list.bezeich = "GRAND TOTAL"
        c_list.qty = tt_qty
        c_list.f_cost =  to_decimal(ttf_cost)
        c_list.b_cost =  to_decimal(ttb_cost)
        c_list.o_cost =  to_decimal(tto_cost)
        c_list.t_cost =  to_decimal(tt_cost)
        c_list.betrag =  to_decimal(tt_betrag)
        c_list.f_betrag =  to_decimal(ttf_betrag)
        c_list.b_betrag =  to_decimal(ttb_betrag)
        c_list.o_betrag =  to_decimal(tto_betrag)
        tt_qty = 0

        if it_exist:

            for s_list in query(s_list_data, filters=(lambda s_list: s_list.creditlimit != 0 and s_list.creditlimit < s_list.betrag and s_list.flag == 0)):
                c_list = C_list()
                c_list_data.append(c_list)

                nr = nr + 1
                c_list.nr = nr
                c_list.flag = 1
                c_list.deptname = translateExtended ("Over CreditLimit", lvcarea, "")
                c_list.name = s_list.officer
                c_list.creditlimit =  to_decimal(s_list.creditlimit)
                c_list.bezeich = to_string(s_list.creditlimit, " ->>>,>>>,>>>,>>9.99")
                c_list.betrag =  to_decimal(s_list.betrag)
                c_list.f_betrag =  to_decimal(s_list.betrag) - to_decimal(s_list.creditlimit)


    def journal_list1():

        nonlocal c_list_data, it_exist, curr_name, guestname, lvcarea, h_artikel, htparam, hoteldpt, h_compli, h_bill, h_journal, artikel, h_cost, queasy, exrate, h_bill_line
        nonlocal pvilanguage, gname, sorttype, from_dept, to_dept, from_date, to_date, double_currency, exchg_rate, billdate, mi_detail1, sm_disp1, foreign_nr, c2_list


        nonlocal c_list, c1_list, c2_list, s_list, s_list, s_list, s_list
        nonlocal c_list_data, c1_list_data

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
        qty:int = 0
        t_qty:int = 0
        tt_qty:int = 0
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
        to_betrag:Decimal = to_decimal("0.0")
        tt_cost:Decimal = to_decimal("0.0")
        ttf_cost:Decimal = to_decimal("0.0")
        ttb_cost:Decimal = to_decimal("0.0")
        tto_cost:Decimal = to_decimal("0.0")
        tt_betrag:Decimal = to_decimal("0.0")
        ttf_betrag:Decimal = to_decimal("0.0")
        ttb_betrag:Decimal = to_decimal("0.0")
        tto_betrag:Decimal = to_decimal("0.0")
        f_endkum:int = 0
        b_endkum:int = 0
        curr_artnr:int = 0
        nr:int = 0
        h_art = None
        fr_art = None
        S_list = C_list
        s_list_data = c_list_data
        H_art =  create_buffer("H_art",H_artikel)
        Fr_art =  create_buffer("Fr_art",Artikel)
        c_list_data.clear()
        c1_list_data.clear()
        it_exist = False

        htparam = get_cache (Htparam, {"paramnr": [(eq, 862)]})
        f_endkum = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 892)]})
        b_endkum = htparam.finteger

        for hoteldpt in db_session.query(Hoteldpt).filter(
                 (Hoteldpt.num >= from_dept) & (Hoteldpt.num <= to_dept)).order_by(Hoteldpt.num).all():

            for h_compli in db_session.query(H_compli).filter(
                     (H_compli.datum >= from_date) & (H_compli.datum <= to_date) & (H_compli.departement == hoteldpt.num) & (H_compli.betriebsnr == 0)).order_by(H_compli.rechnr).all():

                h_art = get_cache (H_artikel, {"departement": [(eq, h_compli.departement)],"artnr": [(eq, h_compli.p_artnr)],"artart": [(eq, 11)]})

                if double_currency and curr_datum != h_compli.datum:
                    curr_datum = h_compli.datum
                    find_exrate(curr_datum)

                    if exrate:
                        rate =  to_decimal(exrate.betrag)
                    else:
                        rate =  to_decimal(exchg_rate)

                c1_list = query(c1_list_data, filters=(lambda c1_list: c1_list.datum == h_compli.datum and c1_list.dept == h_compli.departement and c1_list.rechnr == h_compli.rechnr and c1_list.p_artnr == h_compli.p_artnr), first=True)

                if not c1_list:
                    c1_list = C1_list()
                    c1_list_data.append(c1_list)

                    c1_list.datum = h_compli.datum
                    c1_list.dept = h_compli.departement
                    c1_list.deptname = hoteldpt.depart
                    c1_list.rechnr = h_compli.rechnr
                    c1_list.p_artnr = h_compli.p_artnr

                    h_bill = get_cache (H_bill, {"rechnr": [(eq, h_compli.rechnr)],"departement": [(eq, h_compli.departement)]})

                    if h_bill:
                        c1_list.name = h_bill.bilname
                    else:

                        h_journal = get_cache (H_journal, {"bill_datum": [(eq, h_compli.datum)],"departement": [(eq, h_compli.departement)],"segmentcode": [(eq, h_compli.p_artnr)],"zeit": [(ge, 0)]})

                        if h_journal and h_journal.aendertext != "":
                            c1_list.name = h_journal.aendertext
                    c1_list.bezeich = h_art.bezeich

                h_artikel = get_cache (H_artikel, {"artnr": [(eq, h_compli.artnr)],"departement": [(eq, h_compli.departement)]})

                artikel = get_cache (Artikel, {"artnr": [(eq, h_artikel.artnrfront)],"departement": [(eq, h_compli.departement)]})
                cost =  to_decimal("0")
                f_cost =  to_decimal("0")
                b_cost =  to_decimal("0")
                o_cost =  to_decimal("0")

                h_cost = get_cache (H_cost, {"artnr": [(eq, h_compli.artnr)],"departement": [(eq, h_compli.departement)],"datum": [(eq, h_compli.datum)],"flag": [(eq, 1)]})

                if h_cost and h_cost.betrag != 0:
                    cost =  to_decimal(h_compli.anzahl) * to_decimal(h_cost.betrag)
                    cost = cost_correction(cost)
                    cost = to_decimal(round(cost , 2))
                    tt_cost =  to_decimal(tt_cost) + to_decimal(cost)

                    if artikel.umsatzart == 3 or artikel.umsatzart == 5:
                        f_cost =  to_decimal(cost)
                        ttf_cost =  to_decimal(ttf_cost) + to_decimal(cost)

                    elif artikel.umsatzart == 6:
                        b_cost =  to_decimal(cost)
                        ttb_cost =  to_decimal(ttb_cost) + to_decimal(cost)
                    else:
                        o_cost =  to_decimal(cost)
                        tto_cost =  to_decimal(tto_cost) + to_decimal(cost)
                    c1_list.f_cost =  to_decimal(c1_list.f_cost) + to_decimal(f_cost)
                    c1_list.b_cost =  to_decimal(c1_list.b_cost) + to_decimal(b_cost)
                    c1_list.o_cost =  to_decimal(c1_list.o_cost) + to_decimal(o_cost)
                    c1_list.t_cost =  to_decimal(c1_list.t_cost) + to_decimal(cost)

                elif not h_cost or (h_cost and h_cost.betrag == 0):
                    cost =  to_decimal(h_compli.anzahl) * to_decimal(h_compli.epreis) * to_decimal(h_artikel.prozent) / to_decimal("100") * to_decimal(rate)
                    cost = to_decimal(round(cost , 2))
                    tt_cost =  to_decimal(tt_cost) + to_decimal(cost)

                    if artikel.umsatzart == 3 or artikel.umsatzart == 5:
                        f_cost =  to_decimal(cost)
                        ttf_cost =  to_decimal(ttf_cost) + to_decimal(cost)

                    elif artikel.umsatzart == 6:
                        b_cost =  to_decimal(cost)
                        ttb_cost =  to_decimal(ttb_cost) + to_decimal(cost)
                    else:
                        o_cost =  to_decimal(cost)
                        tto_cost =  to_decimal(tto_cost) + to_decimal(cost)
                    c1_list.f_cost =  to_decimal(c1_list.f_cost) + to_decimal(f_cost)
                    c1_list.b_cost =  to_decimal(c1_list.b_cost) + to_decimal(b_cost)
                    c1_list.o_cost =  to_decimal(c1_list.o_cost) + to_decimal(o_cost)
                    c1_list.t_cost =  to_decimal(c1_list.t_cost) + to_decimal(cost)
                c1_list.betrag =  to_decimal(c1_list.betrag) + to_decimal(h_compli.anzahl) * to_decimal(h_compli.epreis) * to_decimal(rate)
                tt_betrag =  to_decimal(tt_betrag) + to_decimal(h_compli.anzahl) * to_decimal(h_compli.epreis) * to_decimal(rate)

                if artikel.umsatzart == 3 or artikel.umsatzart == 5:
                    c1_list.f_betrag =  to_decimal(c1_list.f_betrag) + to_decimal(h_compli.anzahl) * to_decimal(h_compli.epreis) * to_decimal(rate)
                    ttf_betrag =  to_decimal(ttf_betrag) + to_decimal(h_compli.anzahl) * to_decimal(h_compli.epreis) * to_decimal(rate)

                elif artikel.umsatzart == 6:
                    c1_list.b_betrag =  to_decimal(c1_list.b_betrag) + to_decimal(h_compli.anzahl) * to_decimal(h_compli.epreis) * to_decimal(rate)
                    ttb_betrag =  to_decimal(ttb_betrag) + to_decimal(h_compli.anzahl) * to_decimal(h_compli.epreis) * to_decimal(rate)
                else:
                    c1_list.o_betrag =  to_decimal(c1_list.o_betrag) + to_decimal(h_compli.anzahl) * to_decimal(h_compli.epreis) * to_decimal(rate)
                    tto_betrag =  to_decimal(tto_betrag) + to_decimal(h_compli.anzahl) * to_decimal(h_compli.epreis) * to_decimal(rate)

                if mi_detail1:

                    c2_list = query(c2_list_data, filters=(lambda c2_list: c2_list.datum == h_compli.datum and c2_list.dept == h_compli.departement and c2_list.rechnr == h_compli.rechnr and c2_list.artnr == h_compli.artnr), first=True)

                    if not c2_list:

                        h_artikel = get_cache (H_artikel, {"artnr": [(eq, h_compli.artnr)],"departement": [(eq, h_compli.departement)]})
                        c2_list = C2_list()
                        c2_list_data.append(c2_list)

                        c2_list.detailed = True
                        c2_list.datum = h_compli.datum
                        c2_list.dept = h_compli.departement
                        c2_list.deptname = hoteldpt.depart
                        c2_list.rechnr = h_compli.rechnr
                        c2_list.artnr = h_artikel.artnr
                        c2_list.bezeich = h_artikel.bezeich
                        c2_list.name = c1_list.name


                    c2_list.qty = c2_list.qty + h_compli.anzahl
                    c2_list.f_cost =  to_decimal(c2_list.f_cost) + to_decimal(f_cost)
                    c2_list.b_cost =  to_decimal(c2_list.b_cost) + to_decimal(b_cost)
                    c2_list.o_cost =  to_decimal(c2_list.o_cost) + to_decimal(o_cost)
                    c2_list.t_cost =  to_decimal(c2_list.t_cost) + to_decimal(cost)
                    c2_list.betrag =  to_decimal(c2_list.betrag) + to_decimal(h_compli.anzahl) * to_decimal(h_compli.epreis) * to_decimal(rate)

                    if artikel.umsatzart == 3 or artikel.umsatzart == 5:
                        c2_list.f_betrag =  to_decimal(c2_list.f_betrag) + to_decimal(h_compli.anzahl) * to_decimal(h_compli.epreis) * to_decimal(rate)

                    elif artikel.umsatzart == 6:
                        c2_list.b_betrag =  to_decimal(c2_list.b_betrag) + to_decimal(h_compli.anzahl) * to_decimal(h_compli.epreis) * to_decimal(rate)
                    else:
                        c2_list.o_betrag =  to_decimal(c2_list.o_betrag) + to_decimal(h_compli.anzahl) * to_decimal(h_compli.epreis) * to_decimal(rate)

        if mi_detail1 == False:
            curr_artnr = 0
            f_cost =  to_decimal("0")
            b_cost =  to_decimal("0")
            o_cost =  to_decimal("0")

            for c1_list in query(c1_list_data, filters=(lambda c1_list: c1_list.betrag != 0), sort_by=[("p_artnr",False),("dept",False),("datum",False),("dept",False),("rechnr",False),("artnr",True)]):

                if curr_artnr == 0:
                    curr_artnr = c1_list.p_artnr

                if curr_artnr != c1_list.p_artnr:
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
                    c_list.o_betrag =  to_decimal(to_betrag)

                    if sm_disp1:

                        queasy = get_cache (Queasy, {"key": [(eq, 105)],"char1": [(eq, curr_name)]})

                        if queasy:
                            it_exist = True
                            c_list.creditlimit =  to_decimal(queasy.deci3)
                            c_list.officer = curr_name
                    curr_artnr = c1_list.p_artnr
                    t_cost =  to_decimal("0")
                    tf_cost =  to_decimal("0")
                    tb_cost =  to_decimal("0")
                    to_cost =  to_decimal("0")
                    t_betrag =  to_decimal("0")
                    tf_betrag =  to_decimal("0")
                    tb_betrag =  to_decimal("0")
                    to_betrag =  to_decimal("0")

                if not c1_list.detailed:
                    t_cost =  to_decimal(t_cost) + to_decimal(c1_list.t_cost)
                    tf_cost =  to_decimal(tf_cost) + to_decimal(c1_list.f_cost)
                    tb_cost =  to_decimal(tb_cost) + to_decimal(c1_list.b_cost)
                    to_cost =  to_decimal(to_cost) + to_decimal(c1_list.o_cost)
                    t_betrag =  to_decimal(t_betrag) + to_decimal(c1_list.betrag)
                    tf_betrag =  to_decimal(tf_betrag) + to_decimal(c1_list.f_betrag)
                    tb_betrag =  to_decimal(tb_betrag) + to_decimal(c1_list.b_betrag)
                    to_betrag =  to_decimal(to_betrag) + to_decimal(c1_list.o_betrag)
                c_list = C_list()
                c_list_data.append(c_list)

                nr = nr + 1
                c_list.nr = nr
                c_list.datum = c1_list.datum
                c_list.dept = c1_list.dept
                c_list.deptname = c1_list.deptname
                c_list.rechnr = c1_list.rechnr
                c_list.p_artnr = c1_list.p_artnr
                c_list.bezeich = c1_list.bezeich
                c_list.betrag =  to_decimal(c1_list.betrag)
                c_list.f_betrag =  to_decimal(c1_list.f_betrag)
                c_list.b_betrag =  to_decimal(c1_list.b_betrag)
                c_list.o_betrag =  to_decimal(c1_list.o_betrag)
                c_list.f_cost =  to_decimal(c1_list.f_cost)
                c_list.b_cost =  to_decimal(c1_list.b_cost)
                c_list.o_cost =  to_decimal(c1_list.o_cost)
                c_list.t_cost =  to_decimal(c1_list.t_cost)
                c_list.name = c1_list.name

        if mi_detail1 :
            curr_artnr = 0
            f_cost =  to_decimal("0")
            b_cost =  to_decimal("0")
            o_cost =  to_decimal("0")

            for c1_list in query(c1_list_data, filters=(lambda c1_list: c1_list.betrag != 0), sort_by=[("rechnr",False),("p_artnr",False),("dept",False),("datum",False),("dept",False),("artnr",True)]):

                if curr_artnr == 0:
                    curr_artnr = c1_list.p_artnr

                if curr_artnr != c1_list.p_artnr:
                    c_list = C_list()
                    c_list_data.append(c_list)

                    nr = nr + 1
                    c_list.nr = nr
                    c_list.bezeich = "T O T A L"
                    c_list.qty = t_qty
                    c_list.f_cost =  to_decimal(tf_cost)
                    c_list.b_cost =  to_decimal(tb_cost)
                    c_list.o_cost =  to_decimal(to_cost)
                    c_list.t_cost =  to_decimal(t_cost)
                    c_list.betrag =  to_decimal(t_betrag)
                    c_list.f_betrag =  to_decimal(tf_betrag)
                    c_list.b_betrag =  to_decimal(tb_betrag)
                    c_list.o_betrag =  to_decimal(to_betrag)
                    tt_qty = tt_qty + t_qty
                    t_qty = 0

                    if sm_disp1:

                        queasy = get_cache (Queasy, {"key": [(eq, 105)],"char1": [(eq, curr_name)]})

                        if queasy:
                            it_exist = True
                            c_list.creditlimit =  to_decimal(queasy.deci3)
                            c_list.officer = curr_name
                    curr_name = c1_list.name
                    t_cost =  to_decimal("0")
                    tf_cost =  to_decimal("0")
                    tb_cost =  to_decimal("0")
                    to_cost =  to_decimal("0")
                    t_betrag =  to_decimal("0")
                    tf_betrag =  to_decimal("0")
                    tb_betrag =  to_decimal("0")
                    to_betrag =  to_decimal("0")

                if not c1_list.detailed:
                    t_cost =  to_decimal(t_cost) + to_decimal(c1_list.t_cost)
                    tf_cost =  to_decimal(tf_cost) + to_decimal(c1_list.f_cost)
                    tb_cost =  to_decimal(tb_cost) + to_decimal(c1_list.b_cost)
                    to_cost =  to_decimal(to_cost) + to_decimal(c1_list.o_cost)
                    t_betrag =  to_decimal(t_betrag) + to_decimal(c1_list.betrag)
                    tf_betrag =  to_decimal(tf_betrag) + to_decimal(c1_list.f_betrag)
                    tb_betrag =  to_decimal(tb_betrag) + to_decimal(c1_list.b_betrag)
                    to_betrag =  to_decimal(to_betrag) + to_decimal(c1_list.o_betrag)
                c_list = C_list()
                c_list_data.append(c_list)

                nr = nr + 1
                c_list.nr = nr
                c_list.datum = c1_list.datum
                c_list.dept = c1_list.dept
                c_list.deptname = c1_list.deptname
                c_list.rechnr = c1_list.rechnr
                c_list.artnr = c1_list.artnr
                c_list.p_artnr = c1_list.p_artnr
                c_list.bezeich = c1_list.bezeich
                c_list.betrag =  to_decimal(c1_list.betrag)
                c_list.f_betrag =  to_decimal(c1_list.f_betrag)
                c_list.b_betrag =  to_decimal(c1_list.b_betrag)
                c_list.o_betrag =  to_decimal(c1_list.o_betrag)
                c_list.f_cost =  to_decimal(c1_list.f_cost)
                c_list.b_cost =  to_decimal(c1_list.b_cost)
                c_list.o_cost =  to_decimal(c1_list.o_cost)
                c_list.t_cost =  to_decimal(c1_list.t_cost)
                c_list.name = c1_list.name

                if p_artnr == 0:
                    qty = c1_list.qty
                    c_list.qty = c1_list.qty
                    t_qty = t_qty + qty
        c_list = C_list()
        c_list_data.append(c_list)

        nr = nr + 1
        c_list.nr = nr
        c_list.bezeich = "T O T A L"
        c_list.qty = t_qty
        c_list.f_cost =  to_decimal(tf_cost)
        c_list.b_cost =  to_decimal(tb_cost)
        c_list.o_cost =  to_decimal(to_cost)
        c_list.t_cost =  to_decimal(t_cost)
        c_list.betrag =  to_decimal(t_betrag)
        c_list.f_betrag =  to_decimal(tf_betrag)
        c_list.b_betrag =  to_decimal(tb_betrag)
        c_list.o_betrag =  to_decimal(to_betrag)
        tt_qty = tt_qty + t_qty
        t_qty = 0

        if sm_disp1:

            queasy = get_cache (Queasy, {"key": [(eq, 105)],"char1": [(eq, curr_name)]})

            if queasy:
                it_exist = True
                c_list.creditlimit =  to_decimal(queasy.deci3)
                c_list.officer = curr_name
        c_list = C_list()
        c_list_data.append(c_list)

        nr = nr + 1
        c_list.nr = nr
        c_list.bezeich = "GRAND TOTAL"
        c_list.qty = tt_qty
        c_list.f_cost =  to_decimal(ttf_cost)
        c_list.b_cost =  to_decimal(ttb_cost)
        c_list.o_cost =  to_decimal(tto_cost)
        c_list.t_cost =  to_decimal(tt_cost)
        c_list.betrag =  to_decimal(tt_betrag)
        c_list.f_betrag =  to_decimal(ttf_betrag)
        c_list.b_betrag =  to_decimal(ttb_betrag)
        c_list.o_betrag =  to_decimal(tto_betrag)

        if it_exist:

            for s_list in query(s_list_data, filters=(lambda s_list: s_list.creditlimit != 0 and s_list.creditlimit < s_list.betrag and s_list.flag == 0)):
                c_list = C_list()
                c_list_data.append(c_list)

                nr = nr + 1
                c_list.nr = nr
                c_list.flag = 1
                c_list.deptname = translateExtended ("Over CreditLimit", lvcarea, "")
                c_list.name = s_list.officer
                c_list.creditlimit =  to_decimal(s_list.creditlimit)
                c_list.bezeich = to_string(s_list.creditlimit, " ->>>,>>>,>>>,>>9.99")
                c_list.betrag =  to_decimal(s_list.betrag)
                c_list.f_betrag =  to_decimal(s_list.betrag) - to_decimal(s_list.creditlimit)


    def journal_list2():

        nonlocal c_list_data, guestname, lvcarea, h_artikel, htparam, hoteldpt, h_compli, h_bill, h_journal, artikel, h_cost, queasy, exrate, h_bill_line
        nonlocal pvilanguage, gname, sorttype, from_dept, to_dept, from_date, to_date, double_currency, exchg_rate, billdate, mi_detail1, sm_disp1, foreign_nr, c2_list


        nonlocal c_list, c1_list, c2_list, s_list, s_list, s_list, s_list
        nonlocal c_list_data, c1_list_data

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
        qty:int = 0
        t_qty:int = 0
        tt_qty:int = 0
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
        to_betrag:Decimal = to_decimal("0.0")
        tt_cost:Decimal = to_decimal("0.0")
        ttf_cost:Decimal = to_decimal("0.0")
        ttb_cost:Decimal = to_decimal("0.0")
        tto_cost:Decimal = to_decimal("0.0")
        tt_betrag:Decimal = to_decimal("0.0")
        ttf_betrag:Decimal = to_decimal("0.0")
        ttb_betrag:Decimal = to_decimal("0.0")
        tto_betrag:Decimal = to_decimal("0.0")
        f_endkum:int = 0
        b_endkum:int = 0
        curr_name:string = ""
        nr:int = 0
        it_exist:bool = False
        h_art = None
        fr_art = None
        S_list = C_list
        s_list_data = c_list_data
        H_art =  create_buffer("H_art",H_artikel)
        Fr_art =  create_buffer("Fr_art",Artikel)
        c_list_data.clear()
        c1_list_data.clear()
        it_exist = False

        htparam = get_cache (Htparam, {"paramnr": [(eq, 862)]})
        f_endkum = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 892)]})
        b_endkum = htparam.finteger

        for hoteldpt in db_session.query(Hoteldpt).filter(
                 (Hoteldpt.num >= from_dept) & (Hoteldpt.num <= to_dept)).order_by(Hoteldpt.num).all():

            h_compli_obj_list = {}
            h_compli = H_compli()
            h_art = H_artikel()
            for h_compli.artnr, h_compli.datum, h_compli.departement, h_compli.rechnr, h_compli.p_artnr, h_compli.anzahl, h_compli.epreis, h_compli._recid, h_art.artnrfront, h_art.prozent, h_art.artnr, h_art.bezeich, h_art.epreis1, h_art.artart, h_art._recid in db_session.query(H_compli.artnr, H_compli.datum, H_compli.departement, H_compli.rechnr, H_compli.p_artnr, H_compli.anzahl, H_compli.epreis, H_compli._recid, H_art.artnrfront, H_art.prozent, H_art.artnr, H_art.bezeich, H_art.epreis1, H_art.artart, H_art._recid).join(H_art,(H_art.departement == H_compli.departement) & (H_art.artnr == H_compli.p_artnr) & (H_art.artart == 11)).filter(
                     (H_compli.datum >= from_date) & (H_compli.datum <= to_date) & (H_compli.departement == hoteldpt.num) & (H_compli.betriebsnr == 0)).order_by(H_compli.rechnr).all():
                if h_compli_obj_list.get(h_compli._recid):
                    continue
                else:
                    h_compli_obj_list[h_compli._recid] = True

                if double_currency and curr_datum != h_compli.datum:
                    curr_datum = h_compli.datum
                    find_exrate(curr_datum)

                    if exrate:
                        rate =  to_decimal(exrate.betrag)
                    else:
                        rate =  to_decimal(exchg_rate)

                c1_list = query(c1_list_data, filters=(lambda c1_list: c1_list.datum == h_compli.datum and c1_list.dept == h_compli.departement and c1_list.rechnr == h_compli.rechnr and c1_list.p_artnr == h_compli.p_artnr), first=True)

                if not c1_list:
                    c1_list = C1_list()
                    c1_list_data.append(c1_list)

                    c1_list.datum = h_compli.datum
                    c1_list.dept = h_compli.departement
                    c1_list.deptname = hoteldpt.depart
                    c1_list.rechnr = h_compli.rechnr
                    c1_list.p_artnr = h_compli.p_artnr

                    h_bill = get_cache (H_bill, {"rechnr": [(eq, h_compli.rechnr)],"departement": [(eq, h_compli.departement)]})

                    if h_bill:
                        c1_list.name = h_bill.bilname
                    else:

                        h_journal = get_cache (H_journal, {"bill_datum": [(eq, h_compli.datum)],"departement": [(eq, h_compli.departement)],"segmentcode": [(eq, h_compli.p_artnr)],"zeit": [(ge, 0)]})

                        if h_journal and h_journal.aendertext != "":
                            c1_list.name = h_journal.aendertext
                    c1_list.bezeich = h_art.bezeich

                h_artikel = get_cache (H_artikel, {"artnr": [(eq, h_compli.artnr)],"departement": [(eq, h_compli.departement)]})

                artikel = get_cache (Artikel, {"artnr": [(eq, h_artikel.artnrfront)],"departement": [(eq, h_compli.departement)]})
                cost =  to_decimal("0")
                f_cost =  to_decimal("0")
                b_cost =  to_decimal("0")
                o_cost =  to_decimal("0")

                h_cost = get_cache (H_cost, {"artnr": [(eq, h_compli.artnr)],"departement": [(eq, h_compli.departement)],"datum": [(eq, h_compli.datum)],"flag": [(eq, 1)]})

                if h_cost and h_cost.betrag != 0:
                    cost =  to_decimal(h_compli.anzahl) * to_decimal(h_cost.betrag)
                    cost = cost_correction(cost)
                    cost = to_decimal(round(cost , 2))
                    tt_cost =  to_decimal(tt_cost) + to_decimal(cost)

                    if artikel.umsatzart == 3 or artikel.umsatzart == 5:
                        f_cost =  to_decimal(cost)
                        ttf_cost =  to_decimal(ttf_cost) + to_decimal(cost)

                    elif artikel.umsatzart == 6:
                        b_cost =  to_decimal(cost)
                        ttb_cost =  to_decimal(ttb_cost) + to_decimal(cost)
                    else:
                        o_cost =  to_decimal(cost)
                        tto_cost =  to_decimal(tto_cost) + to_decimal(cost)
                    c1_list.f_cost =  to_decimal(c1_list.f_cost) + to_decimal(f_cost)
                    c1_list.b_cost =  to_decimal(c1_list.b_cost) + to_decimal(b_cost)
                    c1_list.o_cost =  to_decimal(c1_list.o_cost) + to_decimal(o_cost)
                    c1_list.t_cost =  to_decimal(c1_list.t_cost) + to_decimal(cost)

                elif (not h_cost and h_compli.datum < billdate) or (h_cost and h_cost.betrag == 0):
                    cost =  to_decimal(h_compli.anzahl) * to_decimal(h_compli.epreis) * to_decimal(h_artikel.prozent) / to_decimal("100") * to_decimal(rate)
                    cost = to_decimal(round(cost , 2))
                    tt_cost =  to_decimal(tt_cost) + to_decimal(cost)

                    if artikel.umsatzart == 3 or artikel.umsatzart == 5:
                        f_cost =  to_decimal(cost)
                        ttf_cost =  to_decimal(ttf_cost) + to_decimal(cost)

                    elif artikel.umsatzart == 6:
                        b_cost =  to_decimal(cost)
                        ttb_cost =  to_decimal(ttb_cost) + to_decimal(cost)
                    else:
                        o_cost =  to_decimal(cost)
                        tto_cost =  to_decimal(tto_cost) + to_decimal(cost)
                    c1_list.f_cost =  to_decimal(c1_list.f_cost) + to_decimal(f_cost)
                    c1_list.b_cost =  to_decimal(c1_list.b_cost) + to_decimal(b_cost)
                    c1_list.o_cost =  to_decimal(c1_list.o_cost) + to_decimal(o_cost)
                    c1_list.t_cost =  to_decimal(c1_list.t_cost) + to_decimal(cost)
                c1_list.betrag =  to_decimal(c1_list.betrag) + to_decimal(h_compli.anzahl) * to_decimal(h_compli.epreis) * to_decimal(rate)
                tt_betrag =  to_decimal(tt_betrag) + to_decimal(h_compli.anzahl) * to_decimal(h_compli.epreis) * to_decimal(rate)

                if artikel.umsatzart == 3 or artikel.umsatzart == 5:
                    c1_list.f_betrag =  to_decimal(c1_list.f_betrag) + to_decimal(h_compli.anzahl) * to_decimal(h_compli.epreis) * to_decimal(rate)
                    ttf_betrag =  to_decimal(ttf_betrag) + to_decimal(h_compli.anzahl) * to_decimal(h_compli.epreis) * to_decimal(rate)

                elif artikel.umsatzart == 6:
                    c1_list.b_betrag =  to_decimal(c1_list.b_betrag) + to_decimal(h_compli.anzahl) * to_decimal(h_compli.epreis) * to_decimal(rate)
                    ttb_betrag =  to_decimal(ttb_betrag) + to_decimal(h_compli.anzahl) * to_decimal(h_compli.epreis) * to_decimal(rate)
                else:
                    c1_list.o_betrag =  to_decimal(c1_list.o_betrag) + to_decimal(h_compli.anzahl) * to_decimal(h_compli.epreis) * to_decimal(rate)
                    tto_betrag =  to_decimal(tto_betrag) + to_decimal(h_compli.anzahl) * to_decimal(h_compli.epreis) * to_decimal(rate)

                if mi_detail1:

                    c2_list = query(c2_list_data, filters=(lambda c2_list: c2_list.datum == h_compli.datum and c2_list.dept == h_compli.departement and c2_list.rechnr == h_compli.rechnr and c2_list.artnr == h_compli.artnr), first=True)

                    if not c2_list:

                        h_artikel = get_cache (H_artikel, {"artnr": [(eq, h_compli.artnr)],"departement": [(eq, h_compli.departement)]})
                        c2_list = C2_list()
                        c2_list_data.append(c2_list)

                        c2_list.detailed = True
                        c2_list.datum = h_compli.datum
                        c2_list.dept = h_compli.departement
                        c2_list.deptname = hoteldpt.depart
                        c2_list.rechnr = h_compli.rechnr
                        c2_list.artnr = h_artikel.artnr
                        c2_list.bezeich = h_artikel.bezeich
                        c2_list.name = c1_list.name


                    c2_list.qty = c2_list.qty + h_compli.anzahl
                    c2_list.f_cost =  to_decimal(c2_list.f_cost) + to_decimal(f_cost)
                    c2_list.b_cost =  to_decimal(c2_list.b_cost) + to_decimal(b_cost)
                    c2_list.o_cost =  to_decimal(c2_list.o_cost) + to_decimal(o_cost)
                    c2_list.t_cost =  to_decimal(c2_list.t_cost) + to_decimal(cost)
                    c2_list.betrag =  to_decimal(c2_list.betrag) + to_decimal(h_compli.anzahl) * to_decimal(h_compli.epreis) * to_decimal(rate)

                    if artikel.umsatzart == 3 or artikel.umsatzart == 5:
                        c2_list.f_betrag =  to_decimal(c2_list.f_betrag) + to_decimal(h_compli.anzahl) * to_decimal(h_compli.epreis) * to_decimal(rate)

                    elif artikel.umsatzart == 6:
                        c2_list.b_betrag =  to_decimal(c2_list.b_betrag) + to_decimal(h_compli.anzahl) * to_decimal(h_compli.epreis) * to_decimal(rate)
                    else:
                        c2_list.o_betrag =  to_decimal(c2_list.o_betrag) + to_decimal(h_compli.anzahl) * to_decimal(h_compli.epreis) * to_decimal(rate)
        curr_name = "???"
        f_cost =  to_decimal("0")
        b_cost =  to_decimal("0")
        o_cost =  to_decimal("0")

        for c1_list in query(c1_list_data, filters=(lambda c1_list: c1_list.betrag != 0), sort_by=[("name",False),("datum",False),("dept",False),("rechnr",False),("artnr",True)]):

            if curr_name.lower()  == ("???").lower() :
                curr_name = c1_list.name

            if curr_name != c1_list.name:
                c_list = C_list()
                c_list_data.append(c_list)

                nr = nr + 1
                c_list.nr = nr
                c_list.bezeich = "T O T A L"
                c_list.qty = t_qty
                c_list.f_cost =  to_decimal(tf_cost)
                c_list.b_cost =  to_decimal(tb_cost)
                c_list.o_cost =  to_decimal(to_cost)
                c_list.t_cost =  to_decimal(t_cost)
                c_list.betrag =  to_decimal(t_betrag)
                c_list.f_betrag =  to_decimal(tf_betrag)
                c_list.b_betrag =  to_decimal(tb_betrag)
                c_list.o_betrag =  to_decimal(to_betrag)
                tt_qty = tt_qty + t_qty
                t_qty = 0

                if sm_disp1:

                    queasy = get_cache (Queasy, {"key": [(eq, 105)],"char1": [(eq, curr_name)]})

                    if queasy:
                        it_exist = True
                        c_list.creditlimit =  to_decimal(queasy.deci3)
                        c_list.officer = curr_name
                curr_name = c1_list.name
                t_cost =  to_decimal("0")
                tf_cost =  to_decimal("0")
                tb_cost =  to_decimal("0")
                to_cost =  to_decimal("0")
                t_betrag =  to_decimal("0")
                tf_betrag =  to_decimal("0")
                tb_betrag =  to_decimal("0")
                to_betrag =  to_decimal("0")

            if not c1_list.detailed:
                t_cost =  to_decimal(t_cost) + to_decimal(c1_list.t_cost)
                tf_cost =  to_decimal(tf_cost) + to_decimal(c1_list.f_cost)
                tb_cost =  to_decimal(tb_cost) + to_decimal(c1_list.b_cost)
                to_cost =  to_decimal(to_cost) + to_decimal(c1_list.o_cost)
                t_betrag =  to_decimal(t_betrag) + to_decimal(c1_list.betrag)
                tf_betrag =  to_decimal(tf_betrag) + to_decimal(c1_list.f_betrag)
                tb_betrag =  to_decimal(tb_betrag) + to_decimal(c1_list.b_betrag)
                to_betrag =  to_decimal(to_betrag) + to_decimal(c1_list.o_betrag)
            c_list = C_list()
            c_list_data.append(c_list)

            nr = nr + 1
            c_list.nr = nr
            c_list.datum = c1_list.datum
            c_list.dept = c1_list.dept
            c_list.deptname = c1_list.deptname
            c_list.rechnr = c1_list.rechnr
            c_list.artnr = c1_list.artnr
            c_list.p_artnr = c1_list.p_artnr
            c_list.bezeich = c1_list.bezeich
            c_list.betrag =  to_decimal(c1_list.betrag)
            c_list.f_betrag =  to_decimal(c1_list.f_betrag)
            c_list.b_betrag =  to_decimal(c1_list.b_betrag)
            c_list.o_betrag =  to_decimal(c1_list.o_betrag)
            c_list.f_cost =  to_decimal(c1_list.f_cost)
            c_list.b_cost =  to_decimal(c1_list.b_cost)
            c_list.o_cost =  to_decimal(c1_list.o_cost)
            c_list.t_cost =  to_decimal(c1_list.t_cost)
            c_list.name = c1_list.name

            if p_artnr == 0:
                qty = c1_list.qty
                c_list.qty = c1_list.qty
                t_qty = t_qty + qty
        c_list = C_list()
        c_list_data.append(c_list)

        nr = nr + 1
        c_list.nr = nr
        c_list.bezeich = "T O T A L"
        c_list.qty = t_qty
        c_list.f_cost =  to_decimal(tf_cost)
        c_list.b_cost =  to_decimal(tb_cost)
        c_list.o_cost =  to_decimal(to_cost)
        c_list.t_cost =  to_decimal(t_cost)
        c_list.betrag =  to_decimal(t_betrag)
        c_list.f_betrag =  to_decimal(tf_betrag)
        c_list.b_betrag =  to_decimal(tb_betrag)
        c_list.o_betrag =  to_decimal(to_betrag)
        tt_qty = tt_qty + t_qty
        t_qty = 0

        if sm_disp1:

            queasy = get_cache (Queasy, {"key": [(eq, 105)],"char1": [(eq, curr_name)]})

            if queasy:
                it_exist = True
                c_list.creditlimit =  to_decimal(queasy.deci3)
                c_list.officer = curr_name
        c_list = C_list()
        c_list_data.append(c_list)

        nr = nr + 1
        c_list.nr = nr
        c_list.bezeich = "GRAND TOTAL"
        c_list.qty = tt_qty
        c_list.f_cost =  to_decimal(ttf_cost)
        c_list.b_cost =  to_decimal(ttb_cost)
        c_list.o_cost =  to_decimal(tto_cost)
        c_list.t_cost =  to_decimal(tt_cost)
        c_list.betrag =  to_decimal(tt_betrag)
        c_list.f_betrag =  to_decimal(ttf_betrag)
        c_list.b_betrag =  to_decimal(ttb_betrag)
        c_list.o_betrag =  to_decimal(tto_betrag)

        if it_exist:

            for s_list in query(s_list_data, filters=(lambda s_list: s_list.creditlimit != 0 and s_list.creditlimit < s_list.betrag and s_list.flag == 0)):
                c_list = C_list()
                c_list_data.append(c_list)

                nr = nr + 1
                c_list.nr = nr
                c_list.flag = 1
                c_list.deptname = translateExtended ("Over CreditLimit", lvcarea, "")
                c_list.name = s_list.officer
                c_list.creditlimit =  to_decimal(s_list.creditlimit)
                c_list.bezeich = to_string(s_list.creditlimit, " ->>>,>>>,>>>,>>9.99")
                c_list.betrag =  to_decimal(s_list.betrag)
                c_list.f_betrag =  to_decimal(s_list.betrag) - to_decimal(s_list.creditlimit)


    def journal_gname():

        nonlocal c_list_data, it_exist, guestname, lvcarea, h_artikel, htparam, hoteldpt, h_compli, h_bill, h_journal, artikel, h_cost, queasy, exrate, h_bill_line
        nonlocal pvilanguage, gname, sorttype, from_dept, to_dept, from_date, to_date, double_currency, exchg_rate, billdate, mi_detail1, sm_disp1, foreign_nr, c2_list


        nonlocal c_list, c1_list, c2_list, s_list, s_list, s_list, s_list
        nonlocal c_list_data, c1_list_data

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
        to_betrag:Decimal = to_decimal("0.0")
        tt_cost:Decimal = to_decimal("0.0")
        ttf_cost:Decimal = to_decimal("0.0")
        ttb_cost:Decimal = to_decimal("0.0")
        tto_cost:Decimal = to_decimal("0.0")
        tt_betrag:Decimal = to_decimal("0.0")
        ttf_betrag:Decimal = to_decimal("0.0")
        ttb_betrag:Decimal = to_decimal("0.0")
        tto_betrag:Decimal = to_decimal("0.0")
        f_endkum:int = 0
        b_endkum:int = 0
        curr_name:string = ""
        nr:int = 0
        name:string = ""
        h_art = None
        fr_art = None
        H_art =  create_buffer("H_art",H_artikel)
        Fr_art =  create_buffer("Fr_art",Artikel)
        S_list = C_list
        s_list_data = c_list_data
        c_list_data.clear()
        c1_list_data.clear()
        it_exist = False

        htparam = get_cache (Htparam, {"paramnr": [(eq, 862)]})
        f_endkum = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 892)]})
        b_endkum = htparam.finteger

        for hoteldpt in db_session.query(Hoteldpt).filter(
                 (Hoteldpt.num >= from_dept) & (Hoteldpt.num <= to_dept)).order_by(Hoteldpt.num).all():

            h_compli_obj_list = {}
            h_compli = H_compli()
            h_art = H_artikel()
            for h_compli.artnr, h_compli.datum, h_compli.departement, h_compli.rechnr, h_compli.p_artnr, h_compli.anzahl, h_compli.epreis, h_compli._recid, h_art.artnrfront, h_art.prozent, h_art.artnr, h_art.bezeich, h_art.epreis1, h_art.artart, h_art._recid in db_session.query(H_compli.artnr, H_compli.datum, H_compli.departement, H_compli.rechnr, H_compli.p_artnr, H_compli.anzahl, H_compli.epreis, H_compli._recid, H_art.artnrfront, H_art.prozent, H_art.artnr, H_art.bezeich, H_art.epreis1, H_art.artart, H_art._recid).join(H_art,(H_art.departement == H_compli.departement) & (H_art.artnr == H_compli.p_artnr) & (H_art.artart == 11)).filter(
                     (H_compli.datum >= from_date) & (H_compli.datum <= to_date) & (H_compli.departement == hoteldpt.num) & (H_compli.betriebsnr == 0)).order_by(H_compli.departement, H_compli.rechnr).all():
                if h_compli_obj_list.get(h_compli._recid):
                    continue
                else:
                    h_compli_obj_list[h_compli._recid] = True

                h_bill = get_cache (H_bill, {"rechnr": [(eq, h_compli.rechnr)],"departement": [(eq, h_compli.departement)]})

                if h_bill:
                    name = h_bill.bilname
                else:

                    h_journal = get_cache (H_journal, {"bill_datum": [(eq, h_compli.datum)],"departement": [(eq, h_compli.departement)],"segmentcode": [(eq, h_compli.p_artnr)],"zeit": [(ge, 0)]})

                    if h_journal and h_journal.aendertext != "":
                        name = h_journal.aendertext

                if name.lower()  == (gname).lower() :

                    if double_currency and curr_datum != h_compli.datum:
                        curr_datum = h_compli.datum
                        find_exrate(curr_datum)

                        if exrate:
                            rate =  to_decimal(exrate.betrag)
                        else:
                            rate =  to_decimal(exchg_rate)

                    c1_list = query(c1_list_data, filters=(lambda c1_list: c1_list.datum == h_compli.datum and c1_list.dept == h_compli.departement and c1_list.rechnr == h_compli.rechnr and c1_list.p_artnr == h_compli.p_artnr), first=True)

                    if not c1_list:
                        c1_list = C1_list()
                        c1_list_data.append(c1_list)

                        c1_list.datum = h_compli.datum
                        c1_list.dept = h_compli.departement
                        c1_list.deptname = hoteldpt.depart
                        c1_list.rechnr = h_compli.rechnr
                        c1_list.p_artnr = h_compli.p_artnr

                        h_bill = get_cache (H_bill, {"rechnr": [(eq, h_compli.rechnr)],"departement": [(eq, h_compli.departement)]})

                        if h_bill:
                            c1_list.name = h_bill.bilname
                        else:

                            h_journal = get_cache (H_journal, {"bill_datum": [(eq, h_compli.datum)],"departement": [(eq, h_compli.departement)],"segmentcode": [(eq, h_compli.p_artnr)],"zeit": [(ge, 0)]})

                            if h_journal and h_journal.aendertext != "":
                                c_list.name = h_journal.aendertext
                        c1_list.bezeich = h_art.bezeich

                    h_artikel = get_cache (H_artikel, {"artnr": [(eq, h_compli.artnr)],"departement": [(eq, h_compli.departement)]})

                    artikel = get_cache (Artikel, {"artnr": [(eq, h_artikel.artnrfront)],"departement": [(eq, h_compli.departement)]})
                    cost =  to_decimal("0")
                    f_cost =  to_decimal("0")
                    b_cost =  to_decimal("0")
                    o_cost =  to_decimal("0")

                    h_cost = get_cache (H_cost, {"artnr": [(eq, h_compli.artnr)],"departement": [(eq, h_compli.departement)],"datum": [(eq, h_compli.datum)],"flag": [(eq, 1)]})

                    if h_cost and h_cost.betrag != 0:
                        cost =  to_decimal(h_compli.anzahl) * to_decimal(h_cost.betrag)
                        cost = cost_correction(cost)
                        cost = to_decimal(round(cost , 2))
                        tt_cost =  to_decimal(tt_cost) + to_decimal(cost)

                        if artikel.umsatzart == 3 or artikel.umsatzart == 5:
                            f_cost =  to_decimal(cost)
                            ttf_cost =  to_decimal(ttf_cost) + to_decimal(cost)

                        elif artikel.umsatzart == 6:
                            b_cost =  to_decimal(cost)
                            ttb_cost =  to_decimal(ttb_cost) + to_decimal(cost)
                        else:
                            o_cost =  to_decimal(cost)
                            tto_cost =  to_decimal(tto_cost) + to_decimal(cost)
                        c1_list.f_cost =  to_decimal(c1_list.f_cost) + to_decimal(f_cost)
                        c1_list.b_cost =  to_decimal(c1_list.b_cost) + to_decimal(b_cost)
                        c1_list.o_cost =  to_decimal(c1_list.o_cost) + to_decimal(o_cost)
                        c1_list.t_cost =  to_decimal(c1_list.t_cost) + to_decimal(cost)

                    if (not h_cost and h_compli.datum < billdate) or (h_cost and h_cost.betrag == 0):
                        cost =  to_decimal(h_compli.anzahl) * to_decimal(h_compli.epreis) * to_decimal(h_artikel.prozent) / to_decimal("100") * to_decimal(rate)
                        cost = to_decimal(round(cost , 2))
                        tt_cost =  to_decimal(tt_cost) + to_decimal(cost)

                        if artikel.umsatzart == 3 or artikel.umsatzart == 5:
                            f_cost =  to_decimal(cost)
                            ttf_cost =  to_decimal(ttf_cost) + to_decimal(cost)

                        elif artikel.umsatzart == 6:
                            b_cost =  to_decimal(cost)
                            ttb_cost =  to_decimal(ttb_cost) + to_decimal(cost)
                        else:
                            o_cost =  to_decimal(cost)
                            tto_cost =  to_decimal(tto_cost) + to_decimal(cost)
                        c1_list.f_cost =  to_decimal(c1_list.f_cost) + to_decimal(f_cost)
                        c1_list.b_cost =  to_decimal(c1_list.b_cost) + to_decimal(b_cost)
                        c1_list.o_cost =  to_decimal(c1_list.o_cost) + to_decimal(o_cost)
                        c1_list.t_cost =  to_decimal(c1_list.t_cost) + to_decimal(cost)
                    c1_list.betrag =  to_decimal(c1_list.betrag) + to_decimal(h_compli.anzahl) * to_decimal(h_compli.epreis) * to_decimal(rate)
                    tt_betrag =  to_decimal(tt_betrag) + to_decimal(h_compli.anzahl) * to_decimal(h_compli.epreis) * to_decimal(rate)

                    if artikel.umsatzart == 3 or artikel.umsatzart == 5:
                        c1_list.f_betrag =  to_decimal(c1_list.f_betrag) + to_decimal(h_compli.anzahl) * to_decimal(h_compli.epreis) * to_decimal(rate)
                        ttf_betrag =  to_decimal(ttf_betrag) + to_decimal(h_compli.anzahl) * to_decimal(h_compli.epreis) * to_decimal(rate)

                    elif artikel.umsatzart == 6:
                        c1_list.b_betrag =  to_decimal(c1_list.b_betrag) + to_decimal(h_compli.anzahl) * to_decimal(h_compli.epreis) * to_decimal(rate)
                        ttb_betrag =  to_decimal(ttb_betrag) + to_decimal(h_compli.anzahl) * to_decimal(h_compli.epreis) * to_decimal(rate)
                    else:
                        c1_list.o_betrag =  to_decimal(c1_list.o_betrag) + to_decimal(h_compli.anzahl) * to_decimal(h_compli.epreis) * to_decimal(rate)
                        tto_betrag =  to_decimal(tto_betrag) + to_decimal(h_compli.anzahl) * to_decimal(h_compli.epreis) * to_decimal(rate)
        curr_name = ""
        f_cost =  to_decimal("0")
        b_cost =  to_decimal("0")
        o_cost =  to_decimal("0")

        for c1_list in query(c1_list_data, filters=(lambda c1_list: c1_list.betrag != 0), sort_by=[("name",False),("datum",False),("dept",False)]):

            if curr_name == "":
                curr_name = c1_list.name

            if curr_name != c1_list.name:
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
                c_list.o_betrag =  to_decimal(to_betrag)
                curr_name = c1_list.name
                t_cost =  to_decimal("0")
                tf_cost =  to_decimal("0")
                tb_cost =  to_decimal("0")
                to_cost =  to_decimal("0")
                t_betrag =  to_decimal("0")
                tf_betrag =  to_decimal("0")
                tb_betrag =  to_decimal("0")
                to_betrag =  to_decimal("0")
            t_cost =  to_decimal(t_cost) + to_decimal(c1_list.t_cost)
            tf_cost =  to_decimal(tf_cost) + to_decimal(c1_list.f_cost)
            tb_cost =  to_decimal(tb_cost) + to_decimal(c1_list.b_cost)
            to_cost =  to_decimal(to_cost) + to_decimal(c1_list.o_cost)
            t_betrag =  to_decimal(t_betrag) + to_decimal(c1_list.betrag)
            tf_betrag =  to_decimal(tf_betrag) + to_decimal(c1_list.f_betrag)
            tb_betrag =  to_decimal(tb_betrag) + to_decimal(c1_list.b_betrag)
            to_betrag =  to_decimal(to_betrag) + to_decimal(c1_list.o_betrag)
            c_list = C_list()
            c_list_data.append(c_list)

            nr = nr + 1
            c_list.nr = nr
            c_list.datum = c1_list.datum
            c_list.dept = c1_list.dept
            c_list.deptname = c1_list.deptname
            c_list.rechnr = c1_list.rechnr
            c_list.p_artnr = c1_list.p_artnr
            c_list.bezeich = c1_list.bezeich
            c_list.betrag =  to_decimal(c1_list.betrag)
            c_list.f_betrag =  to_decimal(c1_list.f_betrag)
            c_list.b_betrag =  to_decimal(c1_list.b_betrag)
            c_list.o_betrag =  to_decimal(c1_list.o_betrag)
            c_list.f_cost =  to_decimal(c1_list.f_cost)
            c_list.b_cost =  to_decimal(c1_list.b_cost)
            c_list.o_cost =  to_decimal(c1_list.o_cost)
            c_list.t_cost =  to_decimal(c1_list.t_cost)
            c_list.name = c1_list.name
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
        c_list.o_betrag =  to_decimal(to_betrag)

        if sm_disp1:

            queasy = get_cache (Queasy, {"key": [(eq, 105)],"char1": [(eq, curr_name)]})

            if queasy:
                it_exist = True
                c_list.creditlimit =  to_decimal(queasy.deci3)
                c_list.officer = curr_name

                if c_list.creditlimit != 0 and c_list.creditlimit < c_list.betrag:

                    s_list = query(s_list_data, filters=(lambda s_list: s_list._recid == c_list._recid), first=True)
                    c_list = C_list()
                    c_list_data.append(c_list)

                    nr = nr + 1
                    c_list.nr = nr
                    c_list.flag = 1
                    c_list.deptname = translateExtended ("Over CreditLimit", lvcarea, "")
                    c_list.name = s_list.officer
                    c_list.creditlimit =  to_decimal(s_list.creditlimit)
                    c_list.bezeich = to_string(s_list.creditlimit, " ->>>,>>>,>>>,>>9.99")
                    c_list.betrag =  to_decimal(s_list.betrag)
                    c_list.f_betrag =  to_decimal(s_list.betrag) - to_decimal(s_list.creditlimit)


    def find_exrate(curr_date:date):

        nonlocal c_list_data, it_exist, curr_name, guestname, lvcarea, h_artikel, htparam, hoteldpt, h_compli, h_bill, h_journal, artikel, h_cost, queasy, exrate, h_bill_line
        nonlocal pvilanguage, gname, sorttype, from_dept, to_dept, from_date, to_date, double_currency, exchg_rate, billdate, mi_detail1, sm_disp1, foreign_nr, artnr
        nonlocal c2_list


        nonlocal c_list, c1_list, c2_list, s_list, s_list, s_list, s_list
        nonlocal c_list_data, c1_list_data

        if foreign_nr != 0:

            exrate = get_cache (Exrate, {"artnr": [(eq, foreign_nr)],"datum": [(eq, curr_date)]})
        else:

            exrate = get_cache (Exrate, {"datum": [(eq, curr_date)]})


    def cost_correction(cost:Decimal):

        nonlocal c_list_data, it_exist, curr_name, guestname, lvcarea, h_artikel, htparam, hoteldpt, h_compli, h_bill, h_journal, artikel, h_cost, queasy, exrate, h_bill_line
        nonlocal pvilanguage, gname, sorttype, from_dept, to_dept, from_date, to_date, double_currency, exchg_rate, billdate, mi_detail1, sm_disp1, foreign_nr, artnr
        nonlocal c2_list


        nonlocal c_list, c1_list, c2_list, s_list, s_list, s_list, s_list
        nonlocal c_list_data, c1_list_data

        def generate_inner_output():
            return (cost)


        h_bill_line = get_cache (H_bill_line, {"rechnr": [(eq, h_compli.rechnr)],"bill_datum": [(eq, h_compli.datum)],"departement": [(eq, h_compli.departement)],"artnr": [(eq, h_compli.artnr)],"epreis": [(eq, h_compli.epreis)]})

        if h_bill_line and substring(h_bill_line.bezeich, length(h_bill_line.bezeich) - 1, 1) == ("*").lower()  and h_bill_line.epreis != 0:

            h_artikel = get_cache (H_artikel, {"artnr": [(eq, h_bill_line.artnr)],"departement": [(eq, h_bill_line.departement)]})

            if h_artikel and h_artikel.artart == 0 and h_artikel.epreis1 > h_bill_line.epreis:
                cost =  to_decimal(cost) * to_decimal(h_bill_line.epreis) / to_decimal(h_artikel.epreis1)

        return generate_inner_output()


    def coba():

        nonlocal c_list_data, it_exist, curr_name, guestname, lvcarea, h_artikel, htparam, hoteldpt, h_compli, h_bill, h_journal, artikel, h_cost, queasy, exrate, h_bill_line
        nonlocal pvilanguage, gname, sorttype, from_dept, to_dept, from_date, to_date, double_currency, exchg_rate, billdate, mi_detail1, sm_disp1, foreign_nr, artnr
        nonlocal c2_list


        nonlocal c_list, c1_list, c2_list, s_list, s_list, s_list, s_list
        nonlocal c_list_data, c1_list_data

        h_artikel = get_cache (H_artikel, {"artnr": [(eq, artnr)],"departement": [(eq, c_list.dept)]})

        if h_artikel:
            c_list.p_artnr = artnr
            c_list.bezeich = h_artikel.bezeich

            for h_compli in db_session.query(H_compli).filter(
                     (H_compli.datum == c_list.datum) & (c_list.dept == H_compli.departement) & (c_list.rechnr == H_compli.rechnr) & (H_compli.betriebsnr == 0)).order_by(H_compli._recid).all():
                h_compli.p_artnr = artnr
        curr_name = c_list.name
        guestname = c_list.name

        if (guestname).lower()  != "" and (guestname).lower()  != None and curr_name.lower()  != (guestname).lower() :

            h_bill = get_cache (H_bill, {"rechnr": [(eq, c_list.rechnr)],"departement": [(eq, c_list.dept)]})

            if h_bill:
                pass
                h_bill.bilname = guestname
                pass

                h_journal = get_cache (H_journal, {"bill_datum": [(eq, c_list.datum)],"departement": [(eq, c_list.dept)],"segmentcode": [(eq, c_list.p_artnr)],"rechnr": [(eq, c_list.rechnr)],"zeit": [(ge, 0)]})
                while None != h_journal:
                    pass
                    h_journal.aendertext = guestname
                    pass

                    curr_recid = h_journal._recid
                    h_journal = db_session.query(H_journal).filter(
                             (H_journal.bill_datum == c_list.datum) & (H_journal.departement == c_list.dept) & (H_journal.segmentcode == c_list.p_artnr) & (H_journal.rechnr == c_list.rechnr) & (H_journal.zeit >= 0) & (H_journal._recid > curr_recid)).first()


    journal_list()

    return generate_output()