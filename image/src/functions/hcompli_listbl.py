from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import H_artikel, Htparam, Hoteldpt, H_compli, H_bill, H_journal, Artikel, H_cost, Queasy, Exrate, H_bill_line

def hcompli_listbl(pvilanguage:int, gname:str, sorttype:int, from_dept:int, to_dept:int, from_date:date, to_date:date, double_currency:bool, exchg_rate:decimal, billdate:date, mi_detail1:bool, sm_disp1:bool, foreign_nr:int, artnr:int):
    c_list_list = []
    it_exist:bool = False
    curr_name:str = ""
    guestname:str = ""
    lvcarea:str = "hcompli_list"
    h_artikel = htparam = hoteldpt = h_compli = h_bill = h_journal = artikel = h_cost = queasy = exrate = h_bill_line = None

    c_list = c1_list = c2_list = h_art = fr_art = s_list = None

    c_list_list, C_list = create_model("C_list", {"flag":int, "nr":int, "datum":date, "dept":int, "deptname":str, "rechnr":int, "name":str, "artnr":int, "p_artnr":int, "bezeich":str, "betrag":decimal, "f_betrag":decimal, "f_cost":decimal, "b_betrag":decimal, "b_cost":decimal, "t_cost":decimal, "o_cost":decimal, "creditlimit":decimal, "officer":str, "detailed":bool})
    c1_list_list, C1_list = create_model_like(C_list)

    C2_list = C1_list
    c2_list_list = c1_list_list

    H_art = H_artikel
    Fr_art = Artikel
    S_list = C_list
    s_list_list = c_list_list


    db_session = local_storage.db_session

    def generate_output():
        nonlocal c_list_list, it_exist, curr_name, guestname, lvcarea, h_artikel, htparam, hoteldpt, h_compli, h_bill, h_journal, artikel, h_cost, queasy, exrate, h_bill_line
        nonlocal c2_list, h_art, fr_art, s_list


        nonlocal c_list, c1_list, c2_list, h_art, fr_art, s_list
        nonlocal c_list_list, c1_list_list
        return {"c-list": c_list_list}

    def journal_list():

        nonlocal c_list_list, it_exist, curr_name, guestname, lvcarea, h_artikel, htparam, hoteldpt, h_compli, h_bill, h_journal, artikel, h_cost, queasy, exrate, h_bill_line
        nonlocal c2_list, h_art, fr_art, s_list


        nonlocal c_list, c1_list, c2_list, h_art, fr_art, s_list
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
        H_art = H_artikel

        if gname != "":
            journal_gname()

            return

        if sorttype == 2:
            journal_list1()

            return

        if sorttype == 3:
            journal_list2()

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
            t_cost = 0
            tf_cost = 0
            tb_cost = 0
            to_cost = 0
            t_betrag = 0
            tf_betrag = 0
            tb_betrag = 0

            h_compli_obj_list = []
            for h_compli, h_art in db_session.query(H_compli, H_art).join(H_art,(H_art.departement == H_compli.departement) &  (H_art.artnr == H_compli.p_artnr) &  (H_art.artart == 11)).filter(
                    (H_compli.datum >= from_date) &  (H_compli.datum <= to_date) &  (H_compli.departement == hoteldpt.num) &  (H_compli.betriebsnr == 0)).all():
                if h_compli._recid in h_compli_obj_list:
                    continue
                else:
                    h_compli_obj_list.append(h_compli._recid)

                if double_currency and curr_datum != h_compli.datum:
                    curr_datum = h_compli.datum
                    find_exrate(curr_datum)

                    if exrate:
                        rate = exrate.betrag
                    else:
                        rate = exchg_rate

                c_list = query(c_list_list, filters=(lambda c_list :c_list.datum == h_compli.datum and c_list.dept == h_compli.departement and c_list.rechnr == h_compli.rechnr and c_list.p_artnr == h_compli.p_artnr), first=True)

                if not c_list:
                    c_list = C_list()
                    c_list_list.append(c_list)

                    nr = nr + 1
                    c_list.nr = nr
                    c_list.datum = h_compli.datum
                    c_list.dept = h_compli.departement
                    c_list.deptname = hoteldpt.depart
                    c_list.rechnr = h_compli.rechnr
                    c_list.p_artnr = h_compli.p_artnr

                    h_bill = db_session.query(H_bill).filter(
                            (H_bill.rechnr == h_compli.rechnr) &  (H_bill.departement == h_compli.departement)).first()

                    if h_bill:
                        c_list.name = h_bill.bilname
                    else:

                        h_journal = db_session.query(H_journal).filter(
                                (H_journal.bill_datum == h_compli.datum) &  (H_journal.departement == h_compli.departement) &  (H_journal.segmentcode == h_compli.p_artnr) &  (H_journal.zeit >= 0)).first()

                        if h_journal and h_journal.aendertext != "":
                            c_list.name = h_journal.aendertext
                    c_list.bezeich = h_art.bezeich

                h_artikel = db_session.query(H_artikel).filter(
                        (H_artikel.artnr == h_compli.artnr) &  (H_artikel.departement == h_compli.departement)).first()

                artikel = db_session.query(Artikel).filter(
                        (Artikel.artnr == h_Artikel.artnrfront) &  (Artikel.departement == h_Artikel.departement)).first()
                cost = 0
                f_cost = 0
                b_cost = 0
                o_cost = 0

                h_cost = db_session.query(H_cost).filter(
                        (H_cost.artnr == h_compli.artnr) &  (H_cost.departement == h_compli.departement) &  (H_cost.datum == h_compli.datum) &  (H_cost.flag == 1)).first()

                if h_cost and h_cost.betrag != 0:
                    cost = h_compli.anzahl * h_cost.betrag
                    cost = cost_correction(cost)
                    t_cost = t_cost + cost
                    tt_cost = tt_cost + cost

                    if artikel.umsatzart == 3 or artikel.umsatzart == 5:
                        f_cost = cost
                        tf_cost = tf_cost + f_cost
                        ttf_cost = ttf_cost + f_cost

                    elif artikel.umsatzart == 6:
                        b_cost = cost
                        tb_cost = tb_cost + b_cost
                        ttb_cost = ttb_cost + b_cost
                    c_list.f_cost = c_list.f_cost + f_cost
                    c_list.b_cost = c_list.b_cost + b_cost
                    c_list.o_cost = c_list.o_cost + o_cost
                    c_list.t_cost = c_list.t_cost + cost

                if (not h_cost and h_compli.datum < billdate) or (h_cost and h_cost.betrag == 0):
                    cost = h_compli.anzahl * h_compli.epreis * h_artikel.prozent / 100 * rate
                    t_cost = t_cost + cost
                    tt_cost = tt_cost + cost

                    if artikel.umsatzart == 3 or artikel.umsatzart == 5:
                        f_cost = cost
                        tf_cost = tf_cost + cost
                        ttf_cost = ttf_cost + cost

                    elif artikel.umsatzart == 6:
                        b_cost = cost
                        tb_cost = tb_cost + cost
                        ttb_cost = ttb_cost + cost
                    c_list.f_cost = c_list.f_cost + f_cost
                    c_list.b_cost = c_list.b_cost + b_cost
                    c_list.o_cost = c_list.o_cost + o_cost
                    c_list.t_cost = c_list.t_cost + cost
                c_list.betrag = c_list.betrag + h_compli.anzahl * h_compli.epreis * rate
                t_betrag = t_betrag + h_compli.anzahl * h_compli.epreis * rate
                tt_betrag = tt_betrag + h_compli.anzahl * h_compli.epreis * rate

                if artikel.umsatzart == 3 or artikel.umsatzart == 5:
                    c_list.f_betrag = c_list.f_betrag + h_compli.anzahl * h_compli.epreis * rate
                    tf_betrag = tf_betrag + h_compli.anzahl * h_compli.epreis * rate
                    ttf_betrag = ttf_betrag + h_compli.anzahl * h_compli.epreis * rate

                elif artikel.umsatzart == 6:
                    c_list.b_betrag = c_list.b_betrag + h_compli.anzahl * h_compli.epreis * rate
                    tb_betrag = tb_betrag + h_compli.anzahl * h_compli.epreis * rate
                    ttb_betrag = ttb_betrag + h_compli.anzahl * h_compli.epreis * rate

            if t_betrag != 0:
                c_list = C_list()
                c_list_list.append(c_list)

                nr = nr + 1
                c_list.nr = nr
                c_list.bezeich = "T O T A L"
                c_list.f_cost = tf_cost
                c_list.b_cost = tb_cost
                c_list.o_cost = to_cost
                c_list.t_cost = t_cost
                c_list.betrag = t_betrag
                c_list.f_betrag = tf_betrag
                c_list.b_betrag = tb_betrag
        c_list = C_list()
        c_list_list.append(c_list)

        nr = nr + 1
        c_list.nr = nr
        c_list.bezeich = "GRAND TOTAL"
        c_list.f_cost = ttf_cost
        c_list.b_cost = ttb_cost
        c_list.o_cost = tto_cost
        c_list.t_cost = tt_cost
        c_list.betrag = tt_betrag
        c_list.f_betrag = ttf_betrag
        c_list.b_betrag = ttb_betrag

        for c_list in query(c_list_list):

            if c_list.betrag == 0:
                c_list_list.remove(c_list)

    def journal_list1():

        nonlocal c_list_list, it_exist, curr_name, guestname, lvcarea, h_artikel, htparam, hoteldpt, h_compli, h_bill, h_journal, artikel, h_cost, queasy, exrate, h_bill_line
        nonlocal c2_list, h_art, fr_art, s_list


        nonlocal c_list, c1_list, c2_list, h_art, fr_art, s_list
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
        curr_artnr:int = 0
        nr:int = 0
        H_art = H_artikel
        Fr_art = Artikel
        c_list_list.clear()
        c1_list_list.clear()
        it_exist = False

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 862)).first()
        f_endkum = finteger

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 892)).first()
        b_endkum = finteger

        for hoteldpt in db_session.query(Hoteldpt).filter(
                (Hoteldpt.num >= from_dept) &  (Hoteldpt.num <= to_dept)).all():

            for h_compli in db_session.query(H_compli).filter(
                    (H_compli.datum >= from_date) &  (H_compli.datum <= to_date) &  (H_compli.departement == hoteldpt.num) &  (H_compli.betriebsnr == 0)).all():

                h_art = db_session.query(H_art).filter(
                        (H_art.departement == h_compli.departement) &  (H_art.artnr == h_compli.p_artnr) &  (H_art.artart == 11)).first()

                if double_currency and curr_datum != h_compli.datum:
                    curr_datum = h_compli.datum
                    find_exrate(curr_datum)

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
                    else:

                        h_journal = db_session.query(H_journal).filter(
                                (H_journal.bill_datum == h_compli.datum) &  (H_journal.departement == h_compli.departement) &  (H_journal.segmentcode == h_compli.p_artnr) &  (H_journal.zeit >= 0)).first()

                        if h_journal and h_journal.aendertext != "":
                            c1_list.name = h_journal.aendertext
                    c1_list.bezeich = h_art.bezeich

                h_artikel = db_session.query(H_artikel).filter(
                        (H_artikel.artnr == h_compli.artnr) &  (H_artikel.departement == h_compli.departement)).first()

                artikel = db_session.query(Artikel).filter(
                        (Artikel.artnr == h_Artikel.artnrfront) &  (Artikel.departement == h_compli.departement)).first()
                cost = 0
                f_cost = 0
                b_cost = 0
                o_cost = 0

                h_cost = db_session.query(H_cost).filter(
                        (H_cost.artnr == h_compli.artnr) &  (H_cost.departement == h_compli.departement) &  (H_cost.datum == h_compli.datum) &  (H_cost.flag == 1)).first()

                if h_cost and h_cost.betrag != 0:
                    cost = h_compli.anzahl * h_cost.betrag
                    cost = cost_correction(cost)
                    tt_cost = tt_cost + cost

                    if artikel.umsatzart == 3 or artikel.umsatzart == 5:
                        f_cost = cost
                        ttf_cost = ttf_cost + cost

                    elif artikel.umsatzart == 6:
                        b_cost = cost
                        ttb_cost = ttb_cost + cost
                    else:
                        o_cost = cost
                        tto_cost = tto_cost + cost
                    c1_list.f_cost = c1_list.f_cost + f_cost
                    c1_list.b_cost = c1_list.b_cost + b_cost
                    c1_list.o_cost = c1_list.o_cost + o_cost
                    c1_list.t_cost = c1_list.t_cost + cost

                elif not h_cost or (h_cost and h_cost.betrag == 0):
                    cost = h_compli.anzahl * h_compli.epreis * h_artikel.prozent / 100 * rate
                    tt_cost = tt_cost + cost

                    if artikel.umsatzart == 3 or artikel.umsatzart == 5:
                        f_cost = cost
                        ttf_cost = ttf_cost + cost

                    elif artikel.umsatzart == 6:
                        b_cost = cost
                        ttb_cost = ttb_cost + cost
                    else:
                        o_cost = cost
                        tto_cost = tto_cost + cost
                    c1_list.f_cost = c1_list.f_cost + f_cost
                    c1_list.b_cost = c1_list.b_cost + b_cost
                    c1_list.o_cost = c1_list.o_cost + o_cost
                    c1_list.t_cost = c1_list.t_cost + cost
                c1_list.betrag = c1_list.betrag + h_compli.anzahl * h_compli.epreis * rate
                tt_betrag = tt_betrag + h_compli.anzahl * h_compli.epreis * rate

                if artikel.umsatzart == 3 or artikel.umsatzart == 5:
                    c1_list.f_betrag = c1_list.f_betrag + h_compli.anzahl * h_compli.epreis * rate
                    ttf_betrag = ttf_betrag + h_compli.anzahl * h_compli.epreis * rate

                elif artikel.umsatzart == 6:
                    c1_list.b_betrag = c1_list.b_betrag + h_compli.anzahl * h_compli.epreis * rate
                    ttb_betrag = ttb_betrag + h_compli.anzahl * h_compli.epreis * rate
        curr_artnr = 0
        f_cost = 0
        b_cost = 0
        o_cost = 0

        for c1_list in query(c1_list_list, filters=(lambda c1_list :c1_list.betrag != 0)):

            if curr_artnr == 0:
                curr_artnr = c1_list.p_artnr

            if curr_artnr != c1_list.p_artnr:
                c_list = C_list()
                c_list_list.append(c_list)

                nr = nr + 1
                c_list.nr = nr
                c_list.bezeich = "T O T A L"
                c_list.f_cost = tf_cost
                c_list.b_cost = tb_cost
                c_list.o_cost = to_cost
                c_list.t_cost = t_cost
                c_list.betrag = t_betrag
                c_list.f_betrag = tf_betrag
                c_list.b_betrag = tb_betrag
                curr_artnr = c1_list.p_artnr
                t_cost = 0
                tf_cost = 0
                tb_cost = 0
                to_cost = 0
                t_betrag = 0
                tf_betrag = 0
                tb_betrag = 0
            t_cost = t_cost + c1_list.t_cost
            tf_cost = tf_cost + c1_list.f_cost
            tb_cost = tb_cost + c1_list.b_cost
            to_cost = to_cost + c1_list.o_cost
            t_betrag = t_betrag + c1_list.betrag
            tf_betrag = tf_betrag + c1_list.f_betrag
            tb_betrag = tb_betrag + c1_list.b_betrag
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
            c_list.f_betrag = c1_list.f_betrag
            c_list.b_betrag = c1_list.b_betrag
            c_list.f_cost = c1_list.f_cost
            c_list.b_cost = c1_list.b_cost
            c_list.o_cost = c1_list.o_cost
            c_list.t_cost = c1_list.t_cost
            c_list.name = c1_list.name
        c_list = C_list()
        c_list_list.append(c_list)

        nr = nr + 1
        c_list.nr = nr
        c_list.bezeich = "T O T A L"
        c_list.f_cost = tf_cost
        c_list.b_cost = tb_cost
        c_list.o_cost = to_cost
        c_list.t_cost = t_cost
        c_list.betrag = t_betrag
        c_list.f_betrag = tf_betrag
        c_list.b_betrag = tb_betrag
        c_list = C_list()
        c_list_list.append(c_list)

        nr = nr + 1
        c_list.nr = nr
        c_list.bezeich = "GRAND TOTAL"
        c_list.f_cost = ttf_cost
        c_list.b_cost = ttb_cost
        c_list.o_cost = tto_cost
        c_list.t_cost = tt_cost
        c_list.betrag = tt_betrag
        c_list.f_betrag = ttf_betrag
        c_list.b_betrag = ttb_betrag

    def journal_list2():

        nonlocal c_list_list, it_exist, curr_name, guestname, lvcarea, h_artikel, htparam, hoteldpt, h_compli, h_bill, h_journal, artikel, h_cost, queasy, exrate, h_bill_line
        nonlocal c2_list, h_art, fr_art, s_list


        nonlocal c_list, c1_list, c2_list, h_art, fr_art, s_list
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
        curr_name:str = ""
        nr:int = 0
        it_exist:bool = False
        H_art = H_artikel
        Fr_art = Artikel
        S_list = C_list
        c_list_list.clear()
        c1_list_list.clear()
        it_exist = False

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 862)).first()
        f_endkum = finteger

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 892)).first()
        b_endkum = finteger

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
                    find_exrate(curr_datum)

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
                    else:

                        h_journal = db_session.query(H_journal).filter(
                                (H_journal.bill_datum == h_compli.datum) &  (H_journal.departement == h_compli.departement) &  (H_journal.segmentcode == h_compli.p_artnr) &  (H_journal.zeit >= 0)).first()

                        if h_journal and h_journal.aendertext != "":
                            c1_list.name = h_journal.aendertext
                    c1_list.bezeich = h_art.bezeich

                h_artikel = db_session.query(H_artikel).filter(
                        (H_artikel.artnr == h_compli.artnr) &  (H_artikel.departement == h_compli.departement)).first()

                artikel = db_session.query(Artikel).filter(
                        (Artikel.artnr == h_Artikel.artnrfront) &  (Artikel.departement == h_compli.departement)).first()
                cost = 0
                f_cost = 0
                b_cost = 0
                o_cost = 0

                h_cost = db_session.query(H_cost).filter(
                        (H_cost.artnr == h_compli.artnr) &  (H_cost.departement == h_compli.departement) &  (H_cost.datum == h_compli.datum) &  (H_cost.flag == 1)).first()

                if h_cost and h_cost.betrag != 0:
                    cost = h_compli.anzahl * h_cost.betrag
                    cost = cost_correction(cost)
                    tt_cost = tt_cost + cost

                    if artikel.umsatzart == 3 or artikel.umsatzart == 5:
                        f_cost = cost
                        ttf_cost = ttf_cost + cost

                    elif artikel.umsatzart == 6:
                        b_cost = cost
                        ttb_cost = ttb_cost + cost
                    else:
                        o_cost = cost
                        tto_cost = tto_cost + cost
                    c1_list.f_cost = c1_list.f_cost + f_cost
                    c1_list.b_cost = c1_list.b_cost + b_cost
                    c1_list.o_cost = c1_list.o_cost + o_cost
                    c1_list.t_cost = c1_list.t_cost + cost

                elif (not h_cost and h_compli.datum < billdate) or (h_cost and h_cost.betrag == 0):
                    cost = h_compli.anzahl * h_compli.epreis * h_artikel.prozent / 100 * rate
                    tt_cost = tt_cost + cost

                    if artikel.umsatzart == 3 or artikel.umsatzart == 5:
                        f_cost = cost
                        ttf_cost = ttf_cost + cost

                    elif artikel.umsatzart == 6:
                        b_cost = cost
                        ttb_cost = ttb_cost + cost
                    else:
                        o_cost = cost
                        tto_cost = tto_cost + cost
                    c1_list.f_cost = c1_list.f_cost + f_cost
                    c1_list.b_cost = c1_list.b_cost + b_cost
                    c1_list.o_cost = c1_list.o_cost + o_cost
                    c1_list.t_cost = c1_list.t_cost + cost
                c1_list.betrag = c1_list.betrag + h_compli.anzahl * h_compli.epreis * rate
                tt_betrag = tt_betrag + h_compli.anzahl * h_compli.epreis * rate

                if artikel.umsatzart == 3 or artikel.umsatzart == 5:
                    c1_list.f_betrag = c1_list.f_betrag + h_compli.anzahl * h_compli.epreis * rate
                    ttf_betrag = ttf_betrag + h_compli.anzahl * h_compli.epreis * rate

                elif artikel.umsatzart == 6:
                    c1_list.b_betrag = c1_list.b_betrag + h_compli.anzahl * h_compli.epreis * rate
                    ttb_betrag = ttb_betrag + h_compli.anzahl * h_compli.epreis * rate

                if mi_detail1:

                    c2_list = query(c2_list_list, filters=(lambda c2_list :c2_list.datum == h_compli.datum and c2_list.dept == h_compli.departement and c2_list.rechnr == h_compli.rechnr and c2_list.artnr == h_compli.artnr), first=True)

                    if not c2_list:

                        h_artikel = db_session.query(H_artikel).filter(
                                (H_artikel.artnr == h_compli.artnr) &  (H_artikel.departement == h_compli.departement)).first()
                        c2_list = C2_list()
                        c2_list_list.append(c2_list)

                        c2_list.detailed = True
                        c2_list.datum = h_compli.datum
                        c2_list.dept = h_compli.departement
                        c2_list.deptname = hoteldpt.depart
                        c2_list.rechnr = h_compli.rechnr
                        c2_list.artnr = h_artikel.artnr
                        c2_list.bezeich = h_artikel.bezeich
                        c2_list.name = c1_list.name


                    c2_list.f_cost = c2_list.f_cost + f_cost
                    c2_list.b_cost = c2_list.b_cost + b_cost
                    c2_list.o_cost = c2_list.o_cost + o_cost
                    c2_list.t_cost = c2_list.t_cost + cost
                    c2_list.betrag = c2_list.betrag + h_compli.anzahl * h_compli.epreis * rate

                    if artikel.umsatzart == 3 or artikel.umsatzart == 5:
                        c2_list.f_betrag = c2_list.f_betrag + h_compli.anzahl * h_compli.epreis * rate

                    elif artikel.umsatzart == 6:
                        c2_list.b_betrag = c2_list.b_betrag + h_compli.anzahl * h_compli.epreis * rate
        curr_name = "???"
        f_cost = 0
        b_cost = 0
        o_cost = 0

        for c1_list in query(c1_list_list, filters=(lambda c1_list :c1_list.betrag != 0)):

            if curr_name.lower()  == "???":
                curr_name = c1_list.name

            if curr_name != c1_list.name:
                c_list = C_list()
                c_list_list.append(c_list)

                nr = nr + 1
                c_list.nr = nr
                c_list.bezeich = "T O T A L"
                c_list.f_cost = tf_cost
                c_list.b_cost = tb_cost
                c_list.o_cost = to_cost
                c_list.t_cost = t_cost
                c_list.betrag = t_betrag
                c_list.f_betrag = tf_betrag
                c_list.b_betrag = tb_betrag

                if sm_disp1:

                    queasy = db_session.query(Queasy).filter(
                            (Queasy.key == 105) &  (func.lower(Queasy.char1) == (curr_name).lower())).first()

                    if queasy:
                        it_exist = True
                        c_list.creditlimit = queasy.deci3
                        c_list.officer = curr_name
                curr_name = c1_list.name
                t_cost = 0
                tf_cost = 0
                tb_cost = 0
                to_cost = 0
                t_betrag = 0
                tf_betrag = 0
                tb_betrag = 0

            if not c1_list.detailed:
                t_cost = t_cost + c1_list.t_cost
                tf_cost = tf_cost + c1_list.f_cost
                tb_cost = tb_cost + c1_list.b_cost
                to_cost = to_cost + c1_list.o_cost
                t_betrag = t_betrag + c1_list.betrag
                tf_betrag = tf_betrag + c1_list.f_betrag
                tb_betrag = tb_betrag + c1_list.b_betrag
            c_list = C_list()
            c_list_list.append(c_list)

            nr = nr + 1
            c_list.nr = nr
            c_list.datum = c1_list.datum
            c_list.dept = c1_list.dept
            c_list.deptname = c1_list.deptname
            c_list.rechnr = c1_list.rechnr
            c_list.artnr = c1_list.artnr
            c_list.p_artnr = c1_list.p_artnr
            c_list.bezeich = c1_list.bezeich
            c_list.betrag = c1_list.betrag
            c_list.f_betrag = c1_list.f_betrag
            c_list.b_betrag = c1_list.b_betrag
            c_list.f_cost = c1_list.f_cost
            c_list.b_cost = c1_list.b_cost
            c_list.o_cost = c1_list.o_cost
            c_list.t_cost = c1_list.t_cost
            c_list.name = c1_list.name
        c_list = C_list()
        c_list_list.append(c_list)

        nr = nr + 1
        c_list.nr = nr
        c_list.bezeich = "T O T A L"
        c_list.f_cost = tf_cost
        c_list.b_cost = tb_cost
        c_list.o_cost = to_cost
        c_list.t_cost = t_cost
        c_list.betrag = t_betrag
        c_list.f_betrag = tf_betrag
        c_list.b_betrag = tb_betrag

        if sm_disp1:

            queasy = db_session.query(Queasy).filter(
                    (Queasy.key == 105) &  (func.lower(Queasy.char1) == (curr_name).lower())).first()

            if queasy:
                it_exist = True
                c_list.creditlimit = queasy.deci3
                c_list.officer = curr_name
        c_list = C_list()
        c_list_list.append(c_list)

        nr = nr + 1
        c_list.nr = nr
        c_list.bezeich = "GRAND TOTAL"
        c_list.f_cost = ttf_cost
        c_list.b_cost = ttb_cost
        c_list.o_cost = tto_cost
        c_list.t_cost = tt_cost
        c_list.betrag = tt_betrag
        c_list.f_betrag = ttf_betrag
        c_list.b_betrag = ttb_betrag

        if it_exist:

            for s_list in query(s_list_list, filters=(lambda s_list :s_list.creditlimit != 0 and s_list.creditlimit < s_list.betrag and s_list.flag == 0)):
                c_list = C_list()
                c_list_list.append(c_list)

                nr = nr + 1
                c_list.nr = nr
                c_list.flag = 1
                c_list.deptname = translateExtended ("Over CreditLimit", lvcarea, "")
                c_list.name = s_list.officer
                c_list.creditlimit = s_list.creditlimit
                c_list.bezeich = to_string(s_list.creditlimit, " ->>>,>>>,>>>,>>9.99")
                c_list.betrag = s_list.betrag
                c_list.f_betrag = s_list.betrag - s_list.creditlimit

    def journal_gname():

        nonlocal c_list_list, it_exist, curr_name, guestname, lvcarea, h_artikel, htparam, hoteldpt, h_compli, h_bill, h_journal, artikel, h_cost, queasy, exrate, h_bill_line
        nonlocal c2_list, h_art, fr_art, s_list


        nonlocal c_list, c1_list, c2_list, h_art, fr_art, s_list
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
        curr_name:str = ""
        nr:int = 0
        name:str = ""
        H_art = H_artikel
        Fr_art = Artikel
        S_list = C_list
        c_list_list.clear()
        c1_list_list.clear()
        it_exist = False

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 862)).first()
        f_endkum = finteger

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 892)).first()
        b_endkum = finteger

        for hoteldpt in db_session.query(Hoteldpt).filter(
                (Hoteldpt.num >= from_dept) &  (Hoteldpt.num <= to_dept)).all():

            h_compli_obj_list = []
            for h_compli, h_art in db_session.query(H_compli, H_art).join(H_art,(H_art.departement == H_compli.departement) &  (H_art.artnr == H_compli.p_artnr) &  (H_art.artart == 11)).filter(
                    (H_compli.datum >= from_date) &  (H_compli.datum <= to_date) &  (H_compli.departement == hoteldpt.num) &  (H_compli.betriebsnr == 0)).all():
                if h_compli._recid in h_compli_obj_list:
                    continue
                else:
                    h_compli_obj_list.append(h_compli._recid)

                h_bill = db_session.query(H_bill).filter(
                        (H_bill.rechnr == h_compli.rechnr) &  (H_bill.departement == h_compli.departement)).first()

                if h_bill:
                    name = h_bill.bilname
                else:

                    h_journal = db_session.query(H_journal).filter(
                            (H_journal.bill_datum == h_compli.datum) &  (H_journal.departement == h_compli.departement) &  (H_journal.segmentcode == h_compli.p_artnr) &  (H_journal.zeit >= 0)).first()

                    if h_journal and h_journal.aendertext != "":
                        name = h_journal.aendertext

                if name.lower()  == (gname).lower() :

                    if double_currency and curr_datum != h_compli.datum:
                        curr_datum = h_compli.datum
                        find_exrate(curr_datum)

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
                        else:

                            h_journal = db_session.query(H_journal).filter(
                                    (H_journal.bill_datum == h_compli.datum) &  (H_journal.departement == h_compli.departement) &  (H_journal.segmentcode == h_compli.p_artnr) &  (H_journal.zeit >= 0)).first()

                            if h_journal and h_journal.aendertext != "":
                                c_list.name = h_journal.aendertext
                        c1_list.bezeich = h_art.bezeich

                    h_artikel = db_session.query(H_artikel).filter(
                            (H_artikel.artnr == h_compli.artnr) &  (H_artikel.departement == h_compli.departement)).first()

                    artikel = db_session.query(Artikel).filter(
                            (Artikel.artnr == h_Artikel.artnrfront) &  (Artikel.departement == h_compli.departement)).first()
                    cost = 0
                    f_cost = 0
                    b_cost = 0
                    o_cost = 0

                    h_cost = db_session.query(H_cost).filter(
                            (H_cost.artnr == h_compli.artnr) &  (H_cost.departement == h_compli.departement) &  (H_cost.datum == h_compli.datum) &  (H_cost.flag == 1)).first()

                    if h_cost and h_cost.betrag != 0:
                        cost = h_compli.anzahl * h_cost.betrag
                        cost = cost_correction(cost)
                        tt_cost = tt_cost + cost

                        if artikel.umsatzart == 3 or artikel.umsatzart == 5:
                            f_cost = cost
                            ttf_cost = ttf_cost + cost

                        elif artikel.umsatzart == 6:
                            b_cost = cost
                            ttb_cost = ttb_cost + cost
                        else:
                            f_cost = cost
                            ttf_cost = ttf_cost + cost
                        c1_list.f_cost = c1_list.f_cost + f_cost
                        c1_list.b_cost = c1_list.b_cost + b_cost
                        c1_list.o_cost = c1_list.o_cost + o_cost
                        c1_list.t_cost = c1_list.t_cost + cost

                    if (not h_cost and h_compli.datum < billdate) or (h_cost and h_cost.betrag == 0):
                        cost = h_compli.anzahl * h_compli.epreis * h_artikel.prozent / 100 * rate
                        tt_cost = tt_cost + cost

                        if artikel.umsatzart == 3 or artikel.umsatzart == 5:
                            f_cost = cost
                            ttf_cost = ttf_cost + cost

                        elif artikel.umsatzart == 6:
                            b_cost = cost
                            ttb_cost = ttb_cost + cost
                        else:
                            f_cost = cost
                            ttf_cost = ttf_cost + cost
                        c1_list.f_cost = c1_list.f_cost + f_cost
                        c1_list.b_cost = c1_list.b_cost + b_cost
                        c1_list.o_cost = c1_list.o_cost + o_cost
                        c1_list.t_cost = c1_list.t_cost + cost
                    c1_list.betrag = c1_list.betrag + h_compli.anzahl * h_compli.epreis * rate
                    tt_betrag = tt_betrag + h_compli.anzahl * h_compli.epreis * rate

                    if artikel.umsatzart == 3 or artikel.umsatzart == 5:
                        c1_list.f_betrag = c1_list.f_betrag + h_compli.anzahl * h_compli.epreis * rate
                        ttf_betrag = ttf_betrag + h_compli.anzahl * h_compli.epreis * rate

                    elif artikel.umsatzart == 6:
                        c1_list.b_betrag = c1_list.b_betrag + h_compli.anzahl * h_compli.epreis * rate
                        ttb_betrag = ttb_betrag + h_compli.anzahl * h_compli.epreis * rate
        curr_name = ""
        f_cost = 0
        b_cost = 0
        o_cost = 0

        for c1_list in query(c1_list_list, filters=(lambda c1_list :c1_list.betrag != 0)):

            if curr_name == "":
                curr_name = c1_list.name

            if curr_name != c1_list.name:
                c_list = C_list()
                c_list_list.append(c_list)

                nr = nr + 1
                c_list.nr = nr
                c_list.bezeich = "T O T A L"
                c_list.f_cost = tf_cost
                c_list.b_cost = tb_cost
                c_list.o_cost = to_cost
                c_list.t_cost = t_cost
                c_list.betrag = t_betrag
                c_list.f_betrag = tf_betrag
                c_list.b_betrag = tb_betrag
                curr_name = c1_list.name
                t_cost = 0
                tf_cost = 0
                tb_cost = 0
                to_cost = 0
                t_betrag = 0
                tf_betrag = 0
                tb_betrag = 0
            t_cost = t_cost + c1_list.t_cost
            tf_cost = tf_cost + c1_list.f_cost
            tb_cost = tb_cost + c1_list.b_cost
            to_cost = to_cost + c1_list.o_cost
            t_betrag = t_betrag + c1_list.betrag
            tf_betrag = tf_betrag + c1_list.f_betrag
            tb_betrag = tb_betrag + c1_list.b_betrag
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
            c_list.f_betrag = c1_list.f_betrag
            c_list.b_betrag = c1_list.b_betrag
            c_list.f_cost = c1_list.f_cost
            c_list.b_cost = c1_list.b_cost
            c_list.o_cost = c1_list.o_cost
            c_list.t_cost = c1_list.t_cost
            c_list.name = c1_list.name
        c_list = C_list()
        c_list_list.append(c_list)

        nr = nr + 1
        c_list.nr = nr
        c_list.bezeich = "T O T A L"
        c_list.f_cost = tf_cost
        c_list.b_cost = tb_cost
        c_list.o_cost = to_cost
        c_list.t_cost = t_cost
        c_list.betrag = t_betrag
        c_list.f_betrag = tf_betrag
        c_list.b_betrag = tb_betrag

        if sm_disp1:

            queasy = db_session.query(Queasy).filter(
                    (Queasy.key == 105) &  (func.lower(Queasy.char1) == (curr_name).lower())).first()

            if queasy:
                it_exist = True
                c_list.creditlimit = queasy.deci3
                c_list.officer = curr_name

                if c_list.creditlimit != 0 and c_list.creditlimit < c_list.betrag:

                    s_list = query(s_list_list, filters=(lambda s_list :s_list._recid == c_list._recid), first=True)
                    c_list = C_list()
                    c_list_list.append(c_list)

                    nr = nr + 1
                    c_list.nr = nr
                    c_list.flag = 1
                    c_list.deptname = translateExtended ("Over CreditLimit", lvcarea, "")
                    c_list.name = s_list.officer
                    c_list.creditlimit = s_list.creditlimit
                    c_list.bezeich = to_string(s_list.creditlimit, " ->>>,>>>,>>>,>>9.99")
                    c_list.betrag = s_list.betrag
                    c_list.f_betrag = s_list.betrag - s_list.creditlimit

    def find_exrate(curr_date:date):

        nonlocal c_list_list, it_exist, curr_name, guestname, lvcarea, h_artikel, htparam, hoteldpt, h_compli, h_bill, h_journal, artikel, h_cost, queasy, exrate, h_bill_line
        nonlocal c2_list, h_art, fr_art, s_list


        nonlocal c_list, c1_list, c2_list, h_art, fr_art, s_list
        nonlocal c_list_list, c1_list_list

        if foreign_nr != 0:

            exrate = db_session.query(Exrate).filter(
                    (Exrate.artnr == foreign_nr) &  (Exrate.datum == curr_date)).first()
        else:

            exrate = db_session.query(Exrate).filter(
                    (Exrate.datum == curr_date)).first()

    def cost_correction(cost:decimal):

        nonlocal c_list_list, it_exist, curr_name, guestname, lvcarea, h_artikel, htparam, hoteldpt, h_compli, h_bill, h_journal, artikel, h_cost, queasy, exrate, h_bill_line
        nonlocal c2_list, h_art, fr_art, s_list


        nonlocal c_list, c1_list, c2_list, h_art, fr_art, s_list
        nonlocal c_list_list, c1_list_list

        h_bill_line = db_session.query(H_bill_line).filter(
                (H_bill_line.rechnr == h_compli.rechnr) &  (H_bill_line.bill_datum == h_compli.datum) &  (H_bill_line.departement == h_compli.departement) &  (H_bill_line.artnr == h_compli.artnr) &  (H_bill_line.epreis == h_compli.epreis)).first()

        if h_bill_line and substring(h_bill_line.bezeich, len(h_bill_line.bezeich) - 1, 1) == "*" and h_bill_line.epreis != 0:

            h_artikel = db_session.query(H_artikel).filter(
                    (H_artikel.artnr == h_bill_line.artnr) &  (H_artikel.departement == h_bill_line.departement)).first()

            if h_artikel and h_artikel.artart == 0 and h_artikel.epreis1 > h_bill_line.epreis:
                cost = cost * h_bill_line.epreis / h_artikel.epreis1

    def coba():

        nonlocal c_list_list, it_exist, curr_name, guestname, lvcarea, h_artikel, htparam, hoteldpt, h_compli, h_bill, h_journal, artikel, h_cost, queasy, exrate, h_bill_line
        nonlocal c2_list, h_art, fr_art, s_list


        nonlocal c_list, c1_list, c2_list, h_art, fr_art, s_list
        nonlocal c_list_list, c1_list_list

        h_artikel = db_session.query(H_artikel).filter(
                (H_artikel.artnr == artnr) &  (H_artikel.departement == c_list.dept)).first()

        if h_artikel:
            c_list.p_artnr = artnr
            c_list.bezeich = h_artikel.bezeich

            for h_compli in db_session.query(H_compli).filter(
                    (H_compli.datum == c_list.datum) &  (c_list.dept == H_compli.departement) &  (c_list.rechnr == H_compli.rechnr) &  (H_compli.betriebsnr == 0)).all():
                h_compli.p_artnr = artnr
        curr_name = c_list.name
        guestname = c_list.name

        if (guestname).lower()  != "" and (guestname).lower()  != None and curr_name.lower()  != (guestname).lower() :

            h_bill = db_session.query(H_bill).filter(
                    (H_bill.rechnr == c_list.rechnr) &  (H_bill.departement == c_list.dept)).first()

            if h_bill:

                h_bill = db_session.query(H_bill).first()
                h_bill.bilname = guestname

                h_bill = db_session.query(H_bill).first()

                h_journal = db_session.query(H_journal).filter(
                        (H_journal.bill_datum == c_list.datum) &  (H_journal.departement == c_list.dept) &  (H_journal.segmentcode == c_list.p_artnr) &  (H_journal.rechnr == c_list.rechnr) &  (H_journal.zeit >= 0)).first()
                while None != h_journal:

                    h_journal = db_session.query(H_journal).first()
                    h_journal.aendertext = guestname

                    h_journal = db_session.query(H_journal).first()

                    h_journal = db_session.query(H_journal).filter(
                            (H_journal.bill_datum == c_list.datum) &  (H_journal.departement == c_list.dept) &  (H_journal.segmentcode == c_list.p_artnr) &  (H_journal.rechnr == c_list.rechnr) &  (H_journal.zeit >= 0)).first()

    journal_list()

    return generate_output()