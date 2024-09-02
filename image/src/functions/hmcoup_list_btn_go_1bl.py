from functions.additional_functions import *
import decimal
from datetime import date
from models import Hoteldpt, H_artikel, H_journal, Htparam, Exrate, H_bill, Kellner, Artikel, H_bill_line, H_cost

def hmcoup_list_btn_go_1bl(double_currency:bool, foreign_nr:int, exchg_rate:decimal, billdate:date, from_dept:int, to_dept:int, from_date:date, to_date:date):
    c_list_list = []
    it_exist:bool = False
    hoteldpt = h_artikel = h_journal = htparam = exrate = h_bill = kellner = artikel = h_bill_line = h_cost = None

    h_list = c_list = h_art = None

    h_list_list, H_list = create_model("H_list", {"rechnr":int, "departement":int, "datum":date, "betrag":decimal})
    c_list_list, C_list = create_model("C_list", {"nr":int, "datum":date, "dept":int, "deptname":str, "rechnr":int, "pax":int, "bezeich":str, "f_betrag":decimal, "f_cost":decimal, "b_betrag":decimal, "b_cost":decimal, "betrag":decimal, "t_cost":decimal, "o_cost":decimal, "usr_id":str})

    H_art = H_artikel

    db_session = local_storage.db_session

    def generate_output():
        nonlocal c_list_list, it_exist, hoteldpt, h_artikel, h_journal, htparam, exrate, h_bill, kellner, artikel, h_bill_line, h_cost
        nonlocal h_art


        nonlocal h_list, c_list, h_art
        nonlocal h_list_list, c_list_list
        return {"c-list": c_list_list}

    def create_mplist():

        nonlocal c_list_list, it_exist, hoteldpt, h_artikel, h_journal, htparam, exrate, h_bill, kellner, artikel, h_bill_line, h_cost
        nonlocal h_art


        nonlocal h_list, c_list, h_art
        nonlocal h_list_list, c_list_list


        h_list_list.clear()

        for hoteldpt in db_session.query(Hoteldpt).filter(
                (Hoteldpt.num >= from_dept) &  (Hoteldpt.num <= to_dept)).all():

            h_journal_obj_list = []
            for h_journal, h_artikel in db_session.query(H_journal, H_artikel).join(H_artikel,(H_artikel.artnr == H_journal.artnr) &  (H_artikel.departement == hoteldpt.num) &  (H_artikel.artart == 12)).filter(
                    (H_journal.bill_datum >= from_date) &  (H_journal.bill_datum <= to_date) &  (H_journal.departement == hoteldpt.num)).all():
                if h_journal._recid in h_journal_obj_list:
                    continue
                else:
                    h_journal_obj_list.append(h_journal._recid)

                h_list = query(h_list_list, filters=(lambda h_list :h_list.rechnr == h_journal.rechnr and h_list.departement == h_journal.departement and h_list.datum == h_journal.bill_datum), first=True)

                if not h_list:
                    h_list = H_list()
                    h_list_list.append(h_list)

                    h_list.rechnr = h_journal.rechnr
                    h_list.departement = h_journal.departement
                    h_list.datum = h_journal.bill_datum
                h_list.betrag = h_list.betrag + h_journal.betrag

        for h_list in query(h_list_list, filters=(lambda h_list :h_list.betrag == 0)):
            h_list_list.remove(h_list)

    def journal_list():

        nonlocal c_list_list, it_exist, hoteldpt, h_artikel, h_journal, htparam, exrate, h_bill, kellner, artikel, h_bill_line, h_cost
        nonlocal h_art


        nonlocal h_list, c_list, h_art
        nonlocal h_list_list, c_list_list

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

            for h_list in query(h_list_list, filters=(lambda h_list :h_list.datum >= from_date and h_list.datum <= to_date and h_list.departement == hoteldpt.num)):

                if double_currency and curr_datum != h_list.datum:
                    curr_datum = h_list.datum

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

                h_bill = db_session.query(H_bill).filter(
                        (H_bill.rechnr == h_list.rechnr) &  (H_bill.departement == h_list.departement)).first()

                c_list = query(c_list_list, filters=(lambda c_list :c_list.datum == h_list.datum and c_list.dept == h_list.departement and c_list.rechnr == h_list.rechnr), first=True)

                if not c_list:
                    c_list = C_list()
                    c_list_list.append(c_list)

                    nr = nr + 1
                    c_list.nr = nr
                    c_list.datum = h_list.datum
                    c_list.dept = h_list.departement
                    c_list.deptname = hoteldpt.depart
                    c_list.rechnr = h_list.rechnr

                    if h_bill:

                        kellner = db_session.query(Kellner).filter(
                                (Kellner_nr == h_bill.kellner_nr)).first()

                        if kellner:
                            c_list.usr_id = kellnername
                        else:
                            c_list.usr_id = ""
                        c_list.pax = h_bill.belegung

                h_bill_line_obj_list = []
                for h_bill_line, h_artikel, artikel in db_session.query(H_bill_line, H_artikel, Artikel).join(H_artikel,(H_artikel.artnr == H_bill_line.artnr) &  (H_artikel.departement == h_list.departement) &  (H_artikel.artart == 0)).join(Artikel,(Artikel.artnr == h_Artikel.artnrfront) &  (Artikel.departement == h_Artikel.departement)).filter(
                        (H_bill_line.rechnr == h_list.rechnr) &  (H_bill_line.departement == h_list.departement) &  (H_bill_line.bill_datum == h_list.datum)).all():
                    if h_bill_line._recid in h_bill_line_obj_list:
                        continue
                    else:
                        h_bill_line_obj_list.append(h_bill_line._recid)


                    cost = 0
                    f_cost = 0
                    b_cost = 0
                    o_cost = 0

                    h_cost = db_session.query(H_cost).filter(
                            (H_cost.artnr == h_artikel.artnr) &  (H_cost.departement == h_artikel.departement) &  (H_cost.datum == h_list.datum) &  (H_cost.flag == 1)).first()

                    if h_cost and h_cost.betrag != 0:
                        cost = h_bill_line.anzahl * h_cost.betrag
                        t_cost = t_cost + cost
                        tt_cost = tt_cost + cost

                        if artikel.endkum == f_endkum:
                            f_cost = cost
                            tf_cost = tf_cost + f_cost
                            ttf_cost = ttf_cost + f_cost

                        elif artikel.endkum == b_endkum:
                            b_cost = cost
                            tb_cost = tb_cost + b_cost
                            ttb_cost = ttb_cost + b_cost
                        c_list.f_cost = c_list.f_cost + f_cost
                        c_list.b_cost = c_list.b_cost + b_cost
                        c_list.o_cost = c_list.o_cost + o_cost
                        c_list.t_cost = c_list.t_cost + cost

                    if (not h_cost and h_list.datum <= billdate) or (h_cost and h_cost.betrag == 0):
                        cost = h_bill_line.anzahl * h_bill_line.epreis * h_artikel.prozent / 100 * rate
                        t_cost = t_cost + cost
                        tt_cost = tt_cost + cost

                        if artikel.endkum == f_endkum:
                            f_cost = cost
                            tf_cost = tf_cost + cost
                            ttf_cost = ttf_cost + cost

                        elif artikel.endkum == b_endkum:
                            b_cost = cost
                            tb_cost = tb_cost + cost
                            ttb_cost = ttb_cost + cost
                        c_list.f_cost = c_list.f_cost + f_cost
                        c_list.b_cost = c_list.b_cost + b_cost
                        c_list.o_cost = c_list.o_cost + o_cost
                        c_list.t_cost = c_list.t_cost + cost
                    c_list.betrag = c_list.betrag + h_bill_line.anzahl * h_bill_line.epreis * rate
                    t_betrag = t_betrag + h_bill_line.anzahl * h_bill_line.epreis * rate
                    tt_betrag = tt_betrag + h_bill_line.anzahl * h_bill_line.epreis * rate

                    if artikel.endkum == f_endkum:
                        c_list.f_betrag = c_list.f_betrag + h_bill_line.anzahl * h_bill_line.epreis * rate
                        tf_betrag = tf_betrag + h_bill_line.anzahl * h_bill_line.epreis * rate
                        ttf_betrag = ttf_betrag + h_bill_line.anzahl * h_bill_line.epreis * rate

                    elif artikel.endkum == b_endkum:
                        c_list.b_betrag = c_list.b_betrag + h_bill_line.anzahl * h_bill_line.epreis * rate
                        tb_betrag = tb_betrag + h_bill_line.anzahl * h_bill_line.epreis * rate
                        ttb_betrag = ttb_betrag + h_bill_line.anzahl * h_bill_line.epreis * rate

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

    create_mplist()
    journal_list()

    return generate_output()