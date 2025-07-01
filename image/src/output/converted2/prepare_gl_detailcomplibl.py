#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Gl_acct, Htparam, Waehrung, Exrate, H_artikel, Artikel, H_journal, Kellner, H_bill, H_cost

def prepare_gl_detailcomplibl(fibu:string, bemerk:string, from_date:date):

    prepare_cache ([Htparam, Waehrung, Exrate, H_artikel, Artikel, Kellner, H_bill, H_cost])

    t_gl_acct_list = []
    s_list_list = []
    gl_acct = htparam = waehrung = exrate = h_artikel = artikel = h_journal = kellner = h_bill = h_cost = None

    t_gl_acct = s_list = None

    t_gl_acct_list, T_gl_acct = create_model_like(Gl_acct)
    s_list_list, S_list = create_model("S_list", {"bill_datum":date, "departement":int, "artart":int, "rechnr":int, "artnr":int, "bezeich":string, "anzahl":int, "betrag":Decimal, "cost":Decimal, "tischnr":int, "sysdate":date, "zeit":int, "gname":string, "fibu":string, "kellner_nr":int, "waiter":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_gl_acct_list, s_list_list, gl_acct, htparam, waehrung, exrate, h_artikel, artikel, h_journal, kellner, h_bill, h_cost
        nonlocal fibu, bemerk, from_date


        nonlocal t_gl_acct, s_list
        nonlocal t_gl_acct_list, s_list_list

        return {"t-gl-acct": t_gl_acct_list, "s-list": s_list_list}

    def disp_it():

        nonlocal t_gl_acct_list, s_list_list, gl_acct, htparam, waehrung, exrate, h_artikel, artikel, h_journal, kellner, h_bill, h_cost
        nonlocal fibu, bemerk, from_date


        nonlocal t_gl_acct, s_list
        nonlocal t_gl_acct_list, s_list_list

        dept:int = 0
        billno:int = 0
        cost:Decimal = to_decimal("0.0")
        rate:Decimal = 1
        double_currency:bool = False
        dept = to_int(entry(2, bemerk, ";"))
        billno = to_int(entry(3, bemerk, ";"))

        htparam = get_cache (Htparam, {"paramnr": [(eq, 240)]})
        double_currency = htparam.flogical

        if double_currency:

            htparam = get_cache (Htparam, {"paramnr": [(eq, 144)]})

            if htparam.fchar != "":

                waehrung = get_cache (Waehrung, {"wabkurz": [(eq, htparam.fchar)]})

                if waehrung:

                    exrate = get_cache (Exrate, {"artnr": [(eq, waehrung.waehrungsnr)]})

                    if exrate:
                        rate =  to_decimal(exrate.betrag)
                    else:
                        rate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)

        h_journal_obj_list = {}
        for h_journal, h_artikel, artikel in db_session.query(H_journal, H_artikel, Artikel).join(H_artikel,(H_artikel.artnr == H_journal.artnr) & (H_artikel.departement == H_journal.departement)).join(Artikel,((Artikel.artart == 0) & (Artikel.artnr == H_artikel.artnrfront) & (Artikel.departement == H_artikel.departement)) | ((Artikel.artnr == H_artikel.artnrfront) & (Artikel.departement == 0))).filter(
                 (H_journal.bill_datum == from_date) & (H_journal.departement == dept) & (H_journal.rechnr == billno)).order_by(H_journal.sysdate, H_journal.zeit).all():
            if h_journal_obj_list.get(h_journal._recid):
                continue
            else:
                h_journal_obj_list[h_journal._recid] = True


            s_list = S_list()
            s_list_list.append(s_list)

            buffer_copy(h_journal, s_list)

            kellner = get_cache (Kellner, {"kellner_nr": [(eq, s_list.kellner)],"departement": [(eq, dept)]})

            if kellner:
                s_list.waiter = kellner.kellnername

            h_bill = get_cache (H_bill, {"rechnr": [(eq, s_list.rechnr)],"departement": [(eq, dept)]})

            if h_bill:
                s_list.gname = h_bill.bilname
            s_list.artart = artikel.artart
            s_list.fibu = artikel.fibukonto

            if s_list.artart == 0:

                h_cost = get_cache (H_cost, {"artnr": [(eq, s_list.artnr)],"departement": [(eq, dept)],"datum": [(eq, from_date)],"flag": [(eq, 1)]})

                if h_cost and h_cost.betrag != 0:
                    s_list.cost =  to_decimal(s_list.anzahl) * to_decimal(h_cost.betrag)
                else:
                    s_list.cost =  to_decimal(h_journal.epreis) * to_decimal(h_journal.anzahl) * to_decimal(h_artikel.prozent) / to_decimal("100")
                cost =  to_decimal(cost) + to_decimal(s_list.cost)

        for s_list in query(s_list_list, filters=(lambda s_list: s_list.artart == 11)):

            if s_list.betrag < 0:
                s_list.cost =  to_decimal(cost)

            elif s_list.betrag > 0:
                s_list.cost =  - to_decimal(cost)

    gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, fibu)]})
    t_gl_acct = T_gl_acct()
    t_gl_acct_list.append(t_gl_acct)

    buffer_copy(gl_acct, t_gl_acct)
    disp_it()

    return generate_output()