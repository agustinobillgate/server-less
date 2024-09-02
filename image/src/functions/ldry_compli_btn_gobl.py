from functions.additional_functions import *
import decimal
from datetime import date
from models import H_artikel, Artikel, Hoteldpt, H_compli, Exrate, H_bill, H_cost

def ldry_compli_btn_gobl(foreign_nr:int, sorttype:int, from_dept:int, to_dept:int, from_date:date, to_date:date, billdate:date, exchg_rate:decimal, double_currency:bool):
    c_list_list = []
    it_exist:bool = False
    n:int = 0
    h_artikel = artikel = hoteldpt = h_compli = exrate = h_bill = h_cost = None

    c_list = c1_list = h_art = fr_art = None

    c_list_list, C_list = create_model("C_list", {"nr":int, "datum":date, "dept":int, "rechnr":int, "name":str, "p_artnr":int, "bezeich":str, "betrag":decimal, "t_cost":decimal, "deptname":str})
    c1_list_list, C1_list = create_model_like(C_list)

    H_art = H_artikel
    Fr_art = Artikel

    db_session = local_storage.db_session

    def generate_output():
        nonlocal c_list_list, it_exist, n, h_artikel, artikel, hoteldpt, h_compli, exrate, h_bill, h_cost
        nonlocal h_art, fr_art


        nonlocal c_list, c1_list, h_art, fr_art
        nonlocal c_list_list, c1_list_list
        return {"c-list": c_list_list}

    def journal_list1():

        nonlocal c_list_list, it_exist, n, h_artikel, artikel, hoteldpt, h_compli, exrate, h_bill, h_cost
        nonlocal h_art, fr_art


        nonlocal c_list, c1_list, h_art, fr_art
        nonlocal c_list_list, c1_list_list

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
        cost:decimal = 0
        t_cost:decimal = 0
        t_betrag:decimal = 0
        tt_cost:decimal = 0
        tt_betrag:decimal = 0
        curr_artnr:int = 0
        nr:int = 0
        H_art = H_artikel
        Fr_art = Artikel
        c_list_list.clear()
        c1_list_list.clear()
        it_exist = False

        for hoteldpt in db_session.query(Hoteldpt).filter(
                (Hoteldpt.num >= from_dept) &  (Hoteldpt.num <= to_dept)).all():

            h_compli_obj_list = []
            for h_compli, h_art in db_session.query(H_compli, H_art).join(H_art,(H_art.departement == H_compli.departement) &  (H_art.artnr == H_compli.p_artnr) &  (H_art.artart == 11)).filter(
                    (H_compli.datum >= from_date) &  (H_compli.datum <= to_date) &  (H_compli.departement == hoteldpt.num) &  (H_compli.betriebsnr == 0)).all():
                if h_compli._recid in h_compli_obj_list:
                    continue
                else:
                    h_compli_obj_list.append(h_compli._recid)

                if double_currency and curr_datum != h_compli.datum:
                    curr_datum = h_compli.datum

                    if foreign_nr != 0:

                        exrate = db_session.query(Exrate).filter(
                                (Exrate.artnr == foreign_nr) &  (Exrate.datum == curr_datum)).first()
                    else:

                        exrate = db_session.query(Exrate).filter(
                                (Exrate.datum == curr_datum)).first()

                    if exrate:
                        rate = exrate.betrag
                    else:
                        rate = exchg_rate

                c1_list = query(c1_list_list, filters=(lambda c1_list :c1_list.datum == h_compli.datum and c1_list.dept == h_compli.departement and c1_list.rechnr == h_compli.rechnr and c1_list.p_artnr == h_compli.p_artnr), first=True)

                if not c1_list:
                    c1_list = C1_list()
                    c1_list_list.append(c1_list)

                    c1_list.datum = h_compli.datum
                    c1_list.dept = h_compli.departement
                    c1_list.deptname = hoteldpt.depart
                    c1_list.rechnr = h_compli.rechnr
                    c1_list.p_artnr = h_compli.p_artnr

                    h_bill = db_session.query(H_bill).filter(
                            (H_bill.rechnr == h_compli.rechnr) &  (H_bill.departement == h_compli.departement)).first()

                    if h_bill:
                        c1_list.name = h_bill.bilname
                    c1_list.bezeich = h_art.bezeich

                h_artikel = db_session.query(H_artikel).filter(
                        (H_artikel.artnr == h_compli.artnr) &  (H_artikel.departement == h_compli.departement)).first()

                artikel = db_session.query(Artikel).filter(
                        (Artikel.artnr == h_Artikel.artnrfront) &  (Artikel.departement == h_compli.departement)).first()
                cost = 0

                h_cost = db_session.query(H_cost).filter(
                        (H_cost.artnr == h_compli.artnr) &  (H_cost.departement == h_compli.departement) &  (H_cost.datum == h_compli.datum) &  (H_cost.flag == 1)).first()

                if h_cost and h_cost.betrag != 0:
                    cost = h_compli.anzahl * h_cost.betrag
                    tt_cost = tt_cost + cost
                    c1_list.t_cost = c1_list.t_cost + cost

                if (not h_cost and h_compli.datum < billdate) or (h_cost and h_cost.betrag == 0):
                    cost = h_compli.anzahl * h_compli.epreis * h_artikel.prozent / 100 * rate
                    tt_cost = tt_cost + cost
                    c1_list.t_cost = c1_list.t_cost + cost
                c1_list.betrag = c1_list.betrag + h_compli.anzahl * h_compli.epreis * rate
                tt_betrag = tt_betrag + h_compli.anzahl * h_compli.epreis * rate
        curr_artnr = 0

        for c1_list in query(c1_list_list, filters=(lambda c1_list :c1_list.betrag != 0)):

            if curr_artnr == 0:
                curr_artnr = c1_list.p_artnr

            if curr_artnr != c1_list.p_artnr:
                c_list = C_list()
                c_list_list.append(c_list)

                nr = nr + 1
                c_list.nr = nr
                c_list.bezeich = "T O T A L"
                c_list.t_cost = t_cost
                c_list.betrag = t_betrag
                curr_artnr = c1_list.p_artnr
                t_cost = 0
                t_betrag = 0
            t_cost = t_cost + c1_list.t_cost
            t_betrag = t_betrag + c1_list.betrag
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
            c_list.betrag = c1_list.betrag
            c_list.t_cost = c1_list.t_cost
            c_list.name = c1_list.name
        c_list = C_list()
        c_list_list.append(c_list)

        nr = nr + 1
        c_list.nr = nr
        c_list.bezeich = "T O T A L"
        c_list.t_cost = t_cost
        c_list.betrag = t_betrag
        c_list = C_list()
        c_list_list.append(c_list)

        nr = nr + 1
        c_list.nr = nr
        c_list.bezeich = "GRAND TOTAL"
        c_list.t_cost = tt_cost
        c_list.betrag = tt_betrag

    def journal_list2():

        nonlocal c_list_list, it_exist, n, h_artikel, artikel, hoteldpt, h_compli, exrate, h_bill, h_cost
        nonlocal h_art, fr_art


        nonlocal c_list, c1_list, h_art, fr_art
        nonlocal c_list_list, c1_list_list

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
        cost:decimal = 0
        t_cost:decimal = 0
        t_betrag:decimal = 0
        tt_cost:decimal = 0
        tt_betrag:decimal = 0
        curr_name:str = ""
        nr:int = 0
        H_art = H_artikel
        Fr_art = Artikel
        c_list_list.clear()
        c1_list_list.clear()
        it_exist = False

        for hoteldpt in db_session.query(Hoteldpt).filter(
                (Hoteldpt.num >= from_dept) &  (Hoteldpt.num <= to_dept)).all():

            h_compli_obj_list = []
            for h_compli, h_art in db_session.query(H_compli, H_art).join(H_art,(H_art.departement == H_compli.departement) &  (H_art.artnr == H_compli.p_artnr) &  (H_art.artart == 11)).filter(
                    (H_compli.datum >= from_date) &  (H_compli.datum <= to_date) &  (H_compli.departement == hoteldpt.num) &  (H_compli.betriebsnr == 0)).all():
                if h_compli._recid in h_compli_obj_list:
                    continue
                else:
                    h_compli_obj_list.append(h_compli._recid)

                if double_currency and curr_datum != h_compli.datum:
                    curr_datum = h_compli.datum

                    if foreign_nr != 0:

                        exrate = db_session.query(Exrate).filter(
                                (Exrate.artnr == foreign_nr) &  (Exrate.datum == curr_datum)).first()
                    else:

                        exrate = db_session.query(Exrate).filter(
                                (Exrate.datum == curr_datum)).first()

                    if exrate:
                        rate = exrate.betrag
                    else:
                        rate = exchg_rate

                c1_list = query(c1_list_list, filters=(lambda c1_list :c1_list.datum == h_compli.datum and c1_list.dept == h_compli.departement and c1_list.rechnr == h_compli.rechnr and c1_list.p_artnr == h_compli.p_artnr), first=True)

                if not c1_list:
                    c1_list = C1_list()
                    c1_list_list.append(c1_list)

                    c1_list.datum = h_compli.datum
                    c1_list.dept = h_compli.departement
                    c1_list.deptname = hoteldpt.depart
                    c1_list.rechnr = h_compli.rechnr
                    c1_list.p_artnr = h_compli.p_artnr

                    h_bill = db_session.query(H_bill).filter(
                            (H_bill.rechnr == h_compli.rechnr) &  (H_bill.departement == h_compli.departement)).first()

                    if h_bill:
                        c1_list.name = h_bill.bilname
                    c1_list.bezeich = h_art.bezeich

                h_artikel = db_session.query(H_artikel).filter(
                        (H_artikel.artnr == h_compli.artnr) &  (H_artikel.departement == h_compli.departement)).first()

                artikel = db_session.query(Artikel).filter(
                        (Artikel.artnr == h_Artikel.artnrfront) &  (Artikel.departement == h_compli.departement)).first()
                cost = 0

                h_cost = db_session.query(H_cost).filter(
                        (H_cost.artnr == h_compli.artnr) &  (H_cost.departement == h_compli.departement) &  (H_cost.datum == h_compli.datum) &  (H_cost.flag == 1)).first()

                if h_cost and h_cost.betrag != 0:
                    cost = h_compli.anzahl * h_cost.betrag
                    tt_cost = tt_cost + cost
                    c1_list.t_cost = c1_list.t_cost + cost

                if (not h_cost and h_compli.datum < billdate) or (h_cost and h_cost.betrag == 0):
                    cost = h_compli.anzahl * h_compli.epreis * h_artikel.prozent / 100 * rate
                    tt_cost = tt_cost + cost
                    c1_list.t_cost = c1_list.t_cost + cost
                c1_list.betrag = c1_list.betrag + h_compli.anzahl * h_compli.epreis * rate
                tt_betrag = tt_betrag + h_compli.anzahl * h_compli.epreis * rate
        curr_name = ""

        for c1_list in query(c1_list_list, filters=(lambda c1_list :c1_list.betrag != 0)):

            if curr_name == "":
                curr_name = c1_list.name

            if curr_name != c1_list.name:
                c_list = C_list()
                c_list_list.append(c_list)

                nr = nr + 1
                c_list.nr = nr
                c_list.bezeich = "T O T A L"
                c_list.t_cost = t_cost
                c_list.betrag = t_betrag
                curr_name = c1_list.name
                t_cost = 0
                t_betrag = 0
            t_cost = t_cost + c1_list.t_cost
            t_betrag = t_betrag + c1_list.betrag
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
            c_list.betrag = c1_list.betrag
            c_list.t_cost = c1_list.t_cost
            c_list.name = c1_list.name
        c_list = C_list()
        c_list_list.append(c_list)

        nr = nr + 1
        c_list.nr = nr
        c_list.bezeich = "T O T A L"
        c_list.t_cost = t_cost
        c_list.betrag = t_betrag
        c_list = C_list()
        c_list_list.append(c_list)

        nr = nr + 1
        c_list.nr = nr
        c_list.bezeich = "GRAND TOTAL"
        c_list.t_cost = tt_cost
        c_list.betrag = tt_betrag


    if sorttype == 2:
        journal_list1()

    elif sorttype == 3:
        journal_list2()

    return generate_output()