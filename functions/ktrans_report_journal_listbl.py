#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Hoteldpt, Htparam, H_compli, H_artikel

def ktrans_report_journal_listbl(sorttype:int, from_dept:int, to_dept:int, from_date:date, to_date:date):

    prepare_cache ([Hoteldpt, Htparam, H_compli, H_artikel])

    it_exist = False
    c_list_data = []
    hoteldpt = htparam = h_compli = h_artikel = None

    c_list = None

    c_list_data, C_list = create_model("C_list", {"nr":int, "s_recid":int, "datum":date, "dept":int, "p_artnr":int, "dept1":string, "dept2":string, "artnr":int, "bezeich":string, "f_cost":Decimal, "b_cost":Decimal})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal it_exist, c_list_data, hoteldpt, htparam, h_compli, h_artikel
        nonlocal sorttype, from_dept, to_dept, from_date, to_date


        nonlocal c_list
        nonlocal c_list_data

        return {"it_exist": it_exist, "c-list": c_list_data}

    def journal_list():

        nonlocal it_exist, c_list_data, hoteldpt, htparam, h_compli, h_artikel
        nonlocal sorttype, from_dept, to_dept, from_date, to_date


        nonlocal c_list
        nonlocal c_list_data

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
        h_dept = None
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
        H_dept =  create_buffer("H_dept",Hoteldpt)

        if sorttype == 2:
            journal_list1()

            return
        c_list_data.clear()
        it_exist = False

        htparam = get_cache (Htparam, {"paramnr": [(eq, 862)]})
        f_endkum = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 892)]})
        b_endkum = htparam.finteger

        for hoteldpt in db_session.query(Hoteldpt).filter(
                 (Hoteldpt.num >= from_dept) & (Hoteldpt.num <= to_dept)).order_by(Hoteldpt.num).all():
            tf_cost =  to_decimal("0")
            tb_cost =  to_decimal("0")

            h_compli_obj_list = {}
            h_compli = H_compli()
            h_dept = Hoteldpt()
            for h_compli.artnr, h_compli.departement, h_compli._recid, h_compli.datum, h_compli.p_artnr, h_compli.epreis, h_dept.num, h_dept.depart, h_dept._recid in db_session.query(H_compli.artnr, H_compli.departement, H_compli._recid, H_compli.datum, H_compli.p_artnr, H_compli.epreis, H_dept.num, H_dept.depart, H_dept._recid).join(H_dept,(H_dept.num == H_compli.betriebsnr)).filter(
                     (H_compli.datum >= from_date) & (H_compli.datum <= to_date) & (H_compli.departement == hoteldpt.num) & (H_compli.betriebsnr > 0)).order_by(H_compli.datum, H_compli.betriebsnr).all():
                if h_compli_obj_list.get(h_compli._recid):
                    continue
                else:
                    h_compli_obj_list[h_compli._recid] = True

                h_artikel = get_cache (H_artikel, {"artnr": [(eq, h_compli.artnr)],"departement": [(eq, h_compli.departement)]})
                c_list = C_list()
                c_list_data.append(c_list)

                nr = nr + 1
                c_list.nr = nr
                c_list.s_recid = h_compli._recid
                c_list.datum = h_compli.datum
                c_list.dept = h_compli.departement
                c_list.dept1 = hoteldpt.depart
                c_list.dept2 = h_dept.depart
                c_list.p_artnr = h_compli.p_artnr
                c_list.artnr = h_artikel.artnr
                c_list.bezeich = h_artikel.bezeich


                f_cost =  to_decimal("0")
                b_cost =  to_decimal("0")

                if h_compli.p_artnr == 1:
                    c_list.f_cost =  to_decimal(h_compli.epreis)
                    tf_cost =  to_decimal(tf_cost) + to_decimal(c_list.f_cost)
                    ttf_cost =  to_decimal(ttf_cost) + to_decimal(c_list.f_cost)

                elif h_compli.p_artnr == 2:
                    c_list.b_cost =  to_decimal(h_compli.epreis)
                    tb_cost =  to_decimal(tb_cost) + to_decimal(c_list.b_cost)
                    ttb_cost =  to_decimal(ttb_cost) + to_decimal(c_list.b_cost)

            if tf_cost != 0 or tb_cost != 0:
                c_list = C_list()
                c_list_data.append(c_list)

                nr = nr + 1
                c_list.nr = nr
                c_list.bezeich = "T O T A L"
                c_list.f_cost =  to_decimal(tf_cost)
                c_list.b_cost =  to_decimal(tb_cost)
        c_list = C_list()
        c_list_data.append(c_list)

        nr = nr + 1
        c_list.nr = nr
        c_list.bezeich = "GRAND TOTAL"
        c_list.f_cost =  to_decimal(ttf_cost)
        c_list.b_cost =  to_decimal(ttb_cost)


    def journal_list1():

        nonlocal it_exist, c_list_data, hoteldpt, htparam, h_compli, h_artikel
        nonlocal sorttype, from_dept, to_dept, from_date, to_date


        nonlocal c_list
        nonlocal c_list_data

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
        h_dept = None
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
        H_dept =  create_buffer("H_dept",Hoteldpt)
        c_list_data.clear()
        it_exist = False

        htparam = get_cache (Htparam, {"paramnr": [(eq, 862)]})
        f_endkum = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 892)]})
        b_endkum = htparam.finteger

        for hoteldpt in db_session.query(Hoteldpt).filter(
                 (Hoteldpt.num >= from_dept) & (Hoteldpt.num <= to_dept)).order_by(Hoteldpt.num).all():
            tf_cost =  to_decimal("0")
            tb_cost =  to_decimal("0")

            h_compli_obj_list = {}
            h_compli = H_compli()
            h_dept = Hoteldpt()
            for h_compli.artnr, h_compli.departement, h_compli._recid, h_compli.datum, h_compli.p_artnr, h_compli.epreis, h_dept.num, h_dept.depart, h_dept._recid in db_session.query(H_compli.artnr, H_compli.departement, H_compli._recid, H_compli.datum, H_compli.p_artnr, H_compli.epreis, H_dept.num, H_dept.depart, H_dept._recid).join(H_dept,(H_dept.num == H_compli.departement)).filter(
                     (H_compli.datum >= from_date) & (H_compli.datum <= to_date) & (H_compli.betriebsnr == hoteldpt.num) & (H_compli.betriebsnr > 0)).order_by(H_compli.datum, H_compli.departement).all():
                if h_compli_obj_list.get(h_compli._recid):
                    continue
                else:
                    h_compli_obj_list[h_compli._recid] = True

                h_artikel = get_cache (H_artikel, {"artnr": [(eq, h_compli.artnr)],"departement": [(eq, h_compli.departement)]})
                c_list = C_list()
                c_list_data.append(c_list)

                nr = nr + 1
                c_list.s_recid = h_compli._recid
                c_list.nr = nr
                c_list.datum = h_compli.datum
                c_list.dept = h_compli.departement
                c_list.dept2 = hoteldpt.depart
                c_list.dept1 = h_dept.depart
                c_list.p_artnr = h_compli.p_artnr
                c_list.artnr = h_artikel.artnr
                c_list.bezeich = h_artikel.bezeich


                f_cost =  to_decimal("0")
                b_cost =  to_decimal("0")

                if h_compli.p_artnr == 1:
                    c_list.f_cost =  to_decimal(h_compli.epreis)
                    tf_cost =  to_decimal(tf_cost) + to_decimal(c_list.f_cost)
                    ttf_cost =  to_decimal(ttf_cost) + to_decimal(c_list.f_cost)

                elif h_compli.p_artnr == 2:
                    c_list.b_cost =  to_decimal(h_compli.epreis)
                    tb_cost =  to_decimal(tb_cost) + to_decimal(c_list.b_cost)
                    ttb_cost =  to_decimal(ttb_cost) + to_decimal(c_list.b_cost)

            if tf_cost != 0 or tb_cost != 0:
                c_list = C_list()
                c_list_data.append(c_list)

                nr = nr + 1
                c_list.nr = nr
                c_list.bezeich = "T O T A L"
                c_list.f_cost =  to_decimal(tf_cost)
                c_list.b_cost =  to_decimal(tb_cost)
        c_list = C_list()
        c_list_data.append(c_list)

        nr = nr + 1
        c_list.nr = nr
        c_list.bezeich = "GRAND TOTAL"
        c_list.f_cost =  to_decimal(ttf_cost)
        c_list.b_cost =  to_decimal(ttb_cost)

    journal_list()

    return generate_output()