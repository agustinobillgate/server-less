from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Gl_acct, Htparam, Waehrung, Exrate, H_artikel, Artikel, H_journal, Kellner, H_bill, H_cost

def prepare_gl_detailcomplibl(fibu:str, bemerk:str, from_date:date):
    t_gl_acct_list = []
    s_list_list = []
    gl_acct = htparam = waehrung = exrate = h_artikel = artikel = h_journal = kellner = h_bill = h_cost = None

    t_gl_acct = s_list = None

    t_gl_acct_list, T_gl_acct = create_model_like(Gl_acct)
    s_list_list, S_list = create_model("S_list", {"bill_datum":date, "departement":int, "artart":int, "rechnr":int, "artnr":int, "bezeich":str, "anzahl":int, "betrag":decimal, "cost":decimal, "tischnr":int, "sysdate":date, "zeit":int, "gname":str, "fibu":str, "kellner_nr":int, "waiter":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_gl_acct_list, s_list_list, gl_acct, htparam, waehrung, exrate, h_artikel, artikel, h_journal, kellner, h_bill, h_cost


        nonlocal t_gl_acct, s_list
        nonlocal t_gl_acct_list, s_list_list
        return {"t-gl-acct": t_gl_acct_list, "s-list": s_list_list}

    def disp_it():

        nonlocal t_gl_acct_list, s_list_list, gl_acct, htparam, waehrung, exrate, h_artikel, artikel, h_journal, kellner, h_bill, h_cost


        nonlocal t_gl_acct, s_list
        nonlocal t_gl_acct_list, s_list_list

        dept:int = 0
        billno:int = 0
        cost:decimal = 0
        rate:decimal = 1
        double_currency:bool = False
        dept = to_int(entry(2, bemerk, ";"))
        billno = to_int(entry(3, bemerk, ";"))

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 240)).first()
        double_currency = htparam.flogical

        if double_currency:

            htparam = db_session.query(Htparam).filter(
                    (Htparam.paramnr == 144)).first()

            if htparam.fchar != "":

                waehrung = db_session.query(Waehrung).filter(
                        (Waehrung.wabkurz == htparam.fchar)).first()

                if waehrung:

                    exrate = db_session.query(Exrate).filter(
                            (Exrate.artnr == waehrungsnr)).first()

                    if exrate:
                        rate = exrate.betrag
                    else:
                        rate = waehrung.ankauf / waehrung.einheit

        h_journal_obj_list = []
        for h_journal, h_artikel, artikel in db_session.query(H_journal, H_artikel, Artikel).join(H_artikel,(H_artikel.artnr == H_journal.artnr) &  (H_artikel.departement == H_journal.departement)).join(Artikel,((Artikel.artart == 0) &  (Artikel.artnr == h_Artikel.artnrfront) &  (Artikel.departement == h_Artikel.departement)) |  ((Artikel.artnr == h_Artikel.artnrfront) &  (Artikel.departement == 0))).filter(
                (H_journal.bill_datum == from_date) &  (H_journal.departement == dept) &  (H_journal.rechnr == billno)).all():
            if h_journal._recid in h_journal_obj_list:
                continue
            else:
                h_journal_obj_list.append(h_journal._recid)


            s_list = S_list()
            s_list_list.append(s_list)

            buffer_copy(h_journal, s_list)

            kellner = db_session.query(Kellner).filter(
                    (Kellner_nr == s_list.kellner) &  (Kellner.departement == dept)).first()

            if kellner:
                s_list.waiter = kellnername

            h_bill = db_session.query(H_bill).filter(
                    (H_bill.rechnr == s_list.rechnr) &  (H_bill.departement == dept)).first()

            if h_bill:
                s_list.gname = h_bill.bilname
            s_list.artart = artikel.artart
            s_list.fibu = artikel.fibukonto

            if s_list.artart == 0:

                h_cost = db_session.query(H_cost).filter(
                        (H_cost.artnr == s_list.artnr) &  (H_cost.departement == dept) &  (H_cost.datum == from_date) &  (H_cost.flag == 1)).first()

                if h_cost and h_cost.betrag != 0:
                    s_list.cost = s_list.anzahl * h_cost.betrag
                else:
                    s_list.cost = h_journal.epreis * h_journal.anzahl * h_artikel.prozent / 100
                cost = cost + s_list.cost

        for s_list in query(s_list_list, filters=(lambda s_list :s_list.artart == 11)):

            if s_list.betrag < 0:
                s_list.cost = cost

            elif s_list.betrag > 0:
                s_list.cost = - cost
        OPEN QUERY q1 FOR EACH s_list


    gl_acct = db_session.query(Gl_acct).filter(
            (func.lower(Gl_acct.fibukonto) == (fibu).lower())).first()
    t_gl_acct = T_gl_acct()
    t_gl_acct_list.append(t_gl_acct)

    buffer_copy(gl_acct, t_gl_acct)
    disp_it()

    return generate_output()