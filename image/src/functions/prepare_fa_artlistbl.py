from functions.additional_functions import *
import decimal
from datetime import date
from functions.htpdate import htpdate
from models import Fa_artikel, Fa_grup, Mathis, Gl_acct

def prepare_fa_artlistbl():
    p_881 = None
    q1_list_list = []
    fibu_list_list = []
    fa_artikel = fa_grup = mathis = gl_acct = None

    q1_list = fibu_list = None

    q1_list_list, Q1_list = create_model("Q1_list", {"name":str, "asset":str, "datum":date, "price":decimal, "anzahl":int, "warenwert":decimal, "depn_wert":decimal, "book_wert":decimal, "katnr":int, "bezeich":str, "location":str, "first_depn":date, "next_depn":date, "last_depn":date, "id":str, "created":date, "cid":str, "changed":date, "remark":str, "mathis_nr":int, "fname":str, "supplier":str, "posted":bool, "fibukonto":str, "faartikel_nr":int, "credit_fibu":str, "debit_fibu":str, "recid_fa_artikel":int, "recid_mathis":int, "avail_glacct1":bool, "avail_glacct2":bool, "avail_glacct3":bool, "subgroup":int})
    fibu_list_list, Fibu_list = create_model("Fibu_list", {"flag":int, "fibukonto":str, "bezeich":str, "credit":decimal, "debit":decimal})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal p_881, q1_list_list, fibu_list_list, fa_artikel, fa_grup, mathis, gl_acct


        nonlocal q1_list, fibu_list
        nonlocal q1_list_list, fibu_list_list
        return {"p_881": p_881, "q1-list": q1_list_list, "fibu-list": fibu_list_list}

    p_881 = get_output(htpdate(881))

    mathis_obj_list = []
    for mathis, fa_artikel, fa_grup in db_session.query(Mathis, Fa_artikel, Fa_grup).join(Fa_artikel,(Fa_artikel.nr == Mathis.nr) &  (Fa_artikel.loeschflag == 0)).join(Fa_grup,(Fa_grup.gnr == fa_artikel.subgrp) &  (Fa_grup.flag == 1)).all():
        if mathis._recid in mathis_obj_list:
            continue
        else:
            mathis_obj_list.append(mathis._recid)


        q1_list = Q1_list()
        q1_list_list.append(q1_list)

        q1_list.name = mathis.name
        q1_list.asset = mathis.asset
        q1_list.datum = mathis.datum
        q1_list.price = mathis.price
        q1_list.anzahl = fa_artikel.anzahl
        q1_list.warenwert = fa_artikel.warenwert
        q1_list.depn_wert = fa_artikel.depn_wert
        q1_list.book_wert = fa_artikel.book_wert
        q1_list.katnr = fa_artikel.katnr
        q1_list.bezeich = fa_grup.bezeich
        q1_list.location = mathis.location
        q1_list.first_depn = fa_artikel.first_depn
        q1_list.next_depn = fa_artikel.next_depn
        q1_list.last_depn = fa_artikel.last_depn
        q1_list.id = fa_artikel.id
        q1_list.created = fa_artikel.created
        q1_list.cid = fa_artikel.cid
        q1_list.changed = fa_artikel.changed
        q1_list.remark = mathis.remark
        q1_list.mathis_nr = mathis.nr
        q1_list.fname = mathis.fname
        q1_list.supplier = mathis.supplier
        q1_list.posted = fa_artikel.posted
        q1_list.fibukonto = fa_artikel.fibukonto
        q1_list.faartikel_nr = fa_artikel.nr
        q1_list.credit_fibu = fa_artikel.credit_fibu
        q1_list.debit_fibu = fa_artikel.debit_fibu
        q1_list.recid_fa_artikel = fa_artikel._recid
        q1_list.recid_mathis = mathis._recid
        q1_list.subgroup = fa_artikel.subgrp

        fibu_list = query(fibu_list_list, filters=(lambda fibu_list :fibu_list.fibukonto == fa_grup.fibukonto), first=True)

        if not fibu_list:

            gl_acct = db_session.query(Gl_acct).filter(
                    (Gl_acct.fibukonto == fa_grup.fibukonto)).first()

            if not gl_acct:
                q1_list.avail_glacct1 = True


            else:
                fibu_list = Fibu_list()
                fibu_list_list.append(fibu_list)

                fibu_list.fibukonto = fa_grup.fibukonto
                fibu_list.bezeich = gl_acct.bezeich
                fibu_list.flag = 1

        if q1_list.avail_glacct1 == False:
            fibu_list.debit = fibu_list.debit + fa_artikel.warenwert

        fibu_list = query(fibu_list_list, filters=(lambda fibu_list :fibu_list.fibukonto == fa_grup.credit_fibu), first=True)

        if not fibu_list:

            gl_acct = db_session.query(Gl_acct).filter(
                    (Gl_acct.fibukonto == fa_grup.credit_fibu)).first()

            if not gl_acct:
                q1_list.avail_glacct2 = True


            else:
                fibu_list = Fibu_list()
                fibu_list_list.append(fibu_list)

                fibu_list.fibukonto = fa_grup.credit_fibu
                fibu_list.bezeich = gl_acct.bezeich
                fibu_list.flag = 2

        if q1_list.avail_glacct2 == False:
            fibu_list.credit = fibu_list.credit + fa_artikel.depn_wert

        fibu_list = query(fibu_list_list, filters=(lambda fibu_list :fibu_list.fibukonto == fa_grup.debit_fibu), first=True)

        if not fibu_list:

            gl_acct = db_session.query(Gl_acct).filter(
                    (Gl_acct.fibukonto == fa_grup.debit_fibu)).first()

            if not gl_acct:
                q1_list.avail_glacct3 = True


            else:
                fibu_list = Fibu_list()
                fibu_list_list.append(fibu_list)

                fibu_list.fibukonto = fa_grup.debit_fibu
                fibu_list.bezeich = gl_acct.bezeich
                fibu_list.flag = 3

        if q1_list.avail_glacct3 == False:
            fibu_list.debit = fibu_list.debit + fa_artikel.depn_wert

    return generate_output()