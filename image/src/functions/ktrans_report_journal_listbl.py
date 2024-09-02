from functions.additional_functions import *
import decimal
from datetime import date
from models import Hoteldpt, Htparam, H_compli, H_artikel

def ktrans_report_journal_listbl(sorttype:int, from_dept:int, to_dept:int, from_date:date, to_date:date):
    it_exist = False
    c_list_list = []
    hoteldpt = htparam = h_compli = h_artikel = None

    c_list = h_dept = None

    c_list_list, C_list = create_model("C_list", {"nr":int, "s_recid":int, "datum":date, "dept":int, "p_artnr":int, "dept1":str, "dept2":str, "artnr":int, "bezeich":str, "f_cost":decimal, "b_cost":decimal})

    H_dept = Hoteldpt

    db_session = local_storage.db_session

    def generate_output():
        nonlocal it_exist, c_list_list, hoteldpt, htparam, h_compli, h_artikel
        nonlocal h_dept


        nonlocal c_list, h_dept
        nonlocal c_list_list
        return {"it_exist": it_exist, "c-list": c_list_list}

    def journal_list():

        nonlocal it_exist, c_list_list, hoteldpt, htparam, h_compli, h_artikel
        nonlocal h_dept


        nonlocal c_list, h_dept
        nonlocal c_list_list

        amount:decimal = 0
        t_amount:decimal = 0
        tot_amount:decimal = 0
        rechnr:int = 0
        dept:int = -1
        p_artnr:int = 0
        depart:str = ""
        bezeich:str = ""
        i:int = 0
        artnr:int = 0
        datum:date = None
        curr_datum:date = None
        rate:decimal = 1
        f_cost:decimal = 0
        b_cost:decimal = 0
        o_cost:decimal = 0
        cost:decimal = 0
        t_cost:decimal = 0
        tf_cost:decimal = 0
        tb_cost:decimal = 0
        to_cost:decimal = 0
        t_betrag:decimal = 0
        tf_betrag:decimal = 0
        tb_betrag:decimal = 0
        tt_cost:decimal = 0
        ttf_cost:decimal = 0
        ttb_cost:decimal = 0
        tto_cost:decimal = 0
        tt_betrag:decimal = 0
        ttf_betrag:decimal = 0
        ttb_betrag:decimal = 0
        f_endkum:int = 0
        b_endkum:int = 0
        nr:int = 0
        H_dept = Hoteldpt

        if sorttype == 2:
            journal_list1()

            return
        c_list_list.clear()
        it_exist = False

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 862)).first()
        f_endkum = finteger

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 892)).first()
        b_endkum = finteger

        for hoteldpt in db_session.query(Hoteldpt).filter(
                (Hoteldpt.num >= from_dept) &  (Hoteldpt.num <= to_dept)).all():
            tf_cost = 0
            tb_cost = 0

            h_compli_obj_list = []
            for h_compli, h_dept in db_session.query(H_compli, H_dept).join(H_dept,(H_dept.num == H_compli.betriebsnr)).filter(
                    (H_compli.datum >= from_date) &  (H_compli.datum <= to_date) &  (H_compli.departement == hoteldpt.num) &  (H_compli.betriebsnr > 0)).all():
                if h_compli._recid in h_compli_obj_list:
                    continue
                else:
                    h_compli_obj_list.append(h_compli._recid)

                h_artikel = db_session.query(H_artikel).filter(
                        (H_artikel.artnr == h_compli.artnr) &  (H_artikel.departement == h_compli.departement)).first()
                c_list = C_list()
                c_list_list.append(c_list)

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


                f_cost = 0
                b_cost = 0

                if h_compli.p_artnr == 1:
                    c_list.f_cost = h_compli.epreis
                    tf_cost = tf_cost + c_list.f_cost
                    ttf_cost = ttf_cost + c_list.f_cost

                elif h_compli.p_artnr == 2:
                    c_list.b_cost = h_compli.epreis
                    tb_cost = tb_cost + c_list.b_cost
                    ttb_cost = ttb_cost + c_list.b_cost

            if tf_cost != 0 or tb_cost != 0:
                c_list = C_list()
                c_list_list.append(c_list)

                nr = nr + 1
                c_list.nr = nr
                c_list.bezeich = "T O T A L"
                c_list.f_cost = tf_cost
                c_list.b_cost = tb_cost
        c_list = C_list()
        c_list_list.append(c_list)

        nr = nr + 1
        c_list.nr = nr
        c_list.bezeich = "GRAND TOTAL"
        c_list.f_cost = ttf_cost
        c_list.b_cost = ttb_cost

    def journal_list1():

        nonlocal it_exist, c_list_list, hoteldpt, htparam, h_compli, h_artikel
        nonlocal h_dept


        nonlocal c_list, h_dept
        nonlocal c_list_list

        amount:decimal = 0
        t_amount:decimal = 0
        tot_amount:decimal = 0
        rechnr:int = 0
        dept:int = -1
        p_artnr:int = 0
        depart:str = ""
        bezeich:str = ""
        i:int = 0
        artnr:int = 0
        datum:date = None
        curr_datum:date = None
        rate:decimal = 1
        f_cost:decimal = 0
        b_cost:decimal = 0
        o_cost:decimal = 0
        cost:decimal = 0
        t_cost:decimal = 0
        tf_cost:decimal = 0
        tb_cost:decimal = 0
        to_cost:decimal = 0
        t_betrag:decimal = 0
        tf_betrag:decimal = 0
        tb_betrag:decimal = 0
        tt_cost:decimal = 0
        ttf_cost:decimal = 0
        ttb_cost:decimal = 0
        tto_cost:decimal = 0
        tt_betrag:decimal = 0
        ttf_betrag:decimal = 0
        ttb_betrag:decimal = 0
        f_endkum:int = 0
        b_endkum:int = 0
        nr:int = 0
        H_dept = Hoteldpt
        c_list_list.clear()
        it_exist = False

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 862)).first()
        f_endkum = finteger

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 892)).first()
        b_endkum = finteger

        for hoteldpt in db_session.query(Hoteldpt).filter(
                (Hoteldpt.num >= from_dept) &  (Hoteldpt.num <= to_dept)).all():
            tf_cost = 0
            tb_cost = 0

            h_compli_obj_list = []
            for h_compli, h_dept in db_session.query(H_compli, H_dept).join(H_dept,(H_dept.num == H_compli.departement)).filter(
                    (H_compli.datum >= from_date) &  (H_compli.datum <= to_date) &  (H_compli.betriebsnr == hoteldpt.num) &  (H_compli.betriebsnr > 0)).all():
                if h_compli._recid in h_compli_obj_list:
                    continue
                else:
                    h_compli_obj_list.append(h_compli._recid)

                h_artikel = db_session.query(H_artikel).filter(
                        (H_artikel.artnr == h_compli.artnr) &  (H_artikel.departement == h_compli.departement)).first()
                c_list = C_list()
                c_list_list.append(c_list)

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


                f_cost = 0
                b_cost = 0

                if h_compli.p_artnr == 1:
                    c_list.f_cost = h_compli.epreis
                    tf_cost = tf_cost + c_list.f_cost
                    ttf_cost = ttf_cost + c_list.f_cost

                elif h_compli.p_artnr == 2:
                    c_list.b_cost = h_compli.epreis
                    tb_cost = tb_cost + c_list.b_cost
                    ttb_cost = ttb_cost + c_list.b_cost

            if tf_cost != 0 or tb_cost != 0:
                c_list = C_list()
                c_list_list.append(c_list)

                nr = nr + 1
                c_list.nr = nr
                c_list.bezeich = "T O T A L"
                c_list.f_cost = tf_cost
                c_list.b_cost = tb_cost
        c_list = C_list()
        c_list_list.append(c_list)

        nr = nr + 1
        c_list.nr = nr
        c_list.bezeich = "GRAND TOTAL"
        c_list.f_cost = ttf_cost
        c_list.b_cost = ttb_cost


    journal_list()

    return generate_output()