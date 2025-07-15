#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.htpdate import htpdate
from models import Fa_grup, Fa_artikel, Mathis, Fa_kateg, Gl_acct

def prepare_fa_artlistbl():

    prepare_cache ([Fa_grup, Fa_artikel, Mathis, Fa_kateg, Gl_acct])

    p_881 = None
    q1_list_data = []
    fibu_list_data = []
    fa_grup = fa_artikel = mathis = fa_kateg = gl_acct = None

    q1_list = fibu_list = bfa_grup = None

    q1_list_data, Q1_list = create_model("Q1_list", {"name":string, "asset":string, "datum":date, "price":Decimal, "anzahl":int, "warenwert":Decimal, "depn_wert":Decimal, "book_wert":Decimal, "katnr":int, "bezeich":string, "location":string, "first_depn":date, "next_depn":date, "last_depn":date, "id":string, "created":date, "cid":string, "changed":date, "remark":string, "mathis_nr":int, "fname":string, "supplier":string, "posted":bool, "fibukonto":string, "faartikel_nr":int, "credit_fibu":string, "debit_fibu":string, "recid_fa_artikel":int, "recid_mathis":int, "avail_glacct1":bool, "avail_glacct2":bool, "avail_glacct3":bool, "subgroup":int, "model":string, "gnr":int, "flag":int, "grp_bez":string, "sgrp_bez":string, "rate":Decimal, "mark":string, "spec":string, "anz_depn":int, "category":int})
    fibu_list_data, Fibu_list = create_model("Fibu_list", {"flag":int, "fibukonto":string, "bezeich":string, "credit":Decimal, "debit":Decimal})

    Bfa_grup = create_buffer("Bfa_grup",Fa_grup)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal p_881, q1_list_data, fibu_list_data, fa_grup, fa_artikel, mathis, fa_kateg, gl_acct
        nonlocal bfa_grup


        nonlocal q1_list, fibu_list, bfa_grup
        nonlocal q1_list_data, fibu_list_data

        return {"p_881": p_881, "q1-list": q1_list_data, "fibu-list": fibu_list_data}

    p_881 = get_output(htpdate(881))

    mathis_obj_list = {}
    mathis = Mathis()
    fa_artikel = Fa_artikel()
    fa_grup = Fa_grup()
    for mathis.name, mathis.asset, mathis.datum, mathis.price, mathis.location, mathis.remark, mathis.nr, mathis.fname, mathis.supplier, mathis._recid, mathis.model, mathis.flag, mathis.mark, mathis.spec, fa_artikel.anzahl, fa_artikel.warenwert, fa_artikel.depn_wert, fa_artikel.book_wert, fa_artikel.katnr, fa_artikel.first_depn, fa_artikel.next_depn, fa_artikel.last_depn, fa_artikel.id, fa_artikel.created, fa_artikel.cid, fa_artikel.changed, fa_artikel.posted, fa_artikel.fibukonto, fa_artikel.nr, fa_artikel.credit_fibu, fa_artikel.debit_fibu, fa_artikel._recid, fa_artikel.subgrp, fa_artikel.gnr, fa_artikel.anz_depn, fa_grup.bezeich, fa_grup.fibukonto, fa_grup.credit_fibu, fa_grup.debit_fibu, fa_grup._recid in db_session.query(Mathis.name, Mathis.asset, Mathis.datum, Mathis.price, Mathis.location, Mathis.remark, Mathis.nr, Mathis.fname, Mathis.supplier, Mathis._recid, Mathis.model, Mathis.flag, Mathis.mark, Mathis.spec, Fa_artikel.anzahl, Fa_artikel.warenwert, Fa_artikel.depn_wert, Fa_artikel.book_wert, Fa_artikel.katnr, Fa_artikel.first_depn, Fa_artikel.next_depn, Fa_artikel.last_depn, Fa_artikel.id, Fa_artikel.created, Fa_artikel.cid, Fa_artikel.changed, Fa_artikel.posted, Fa_artikel.fibukonto, Fa_artikel.nr, Fa_artikel.credit_fibu, Fa_artikel.debit_fibu, Fa_artikel._recid, Fa_artikel.subgrp, Fa_artikel.gnr, Fa_artikel.anz_depn, Fa_grup.bezeich, Fa_grup.fibukonto, Fa_grup.credit_fibu, Fa_grup.debit_fibu, Fa_grup._recid).join(Fa_artikel,(Fa_artikel.nr == Mathis.nr) & (Fa_artikel.loeschflag == 0)).join(Fa_grup,(Fa_grup.gnr == Fa_artikel.subgrp) & (Fa_grup.flag == 1)).order_by(Mathis.name).all():
        if mathis_obj_list.get(mathis._recid):
            continue
        else:
            mathis_obj_list[mathis._recid] = True


        q1_list = Q1_list()
        q1_list_data.append(q1_list)

        q1_list.name = mathis.name
        q1_list.asset = mathis.asset
        q1_list.datum = mathis.datum
        q1_list.price =  to_decimal(mathis.price)
        q1_list.anzahl = fa_artikel.anzahl
        q1_list.warenwert =  to_decimal(fa_artikel.warenwert)
        q1_list.depn_wert =  to_decimal(fa_artikel.depn_wert)
        q1_list.book_wert =  to_decimal(fa_artikel.book_wert)
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
        q1_list.gnr = fa_artikel.gnr
        q1_list.model = mathis.model
        q1_list.flag = mathis.flag
        q1_list.mark = mathis.mark
        q1_list.spec = mathis.spec
        q1_list.anz_depn = fa_artikel.anz_depn
        q1_list.category = fa_artikel.katnr

        bfa_grup = get_cache (Fa_grup, {"gnr": [(eq, fa_artikel.gnr)],"flag": [(eq, 0)]})

        if bfa_grup:
            q1_list.grp_bez = bfa_grup.bezeich

        bfa_grup = get_cache (Fa_grup, {"gnr": [(eq, fa_artikel.subgrp)],"flag": [(gt, 0)]})

        if bfa_grup:
            q1_list.sgrp_bez = bfa_grup.bezeich

        fa_kateg = get_cache (Fa_kateg, {"katnr": [(eq, fa_artikel.katnr)]})

        if fa_kateg:
            q1_list.rate =  to_decimal(fa_kateg.rate)

        fibu_list = query(fibu_list_data, filters=(lambda fibu_list: fibu_list.fibukonto == fa_grup.fibukonto), first=True)

        if not fibu_list:

            gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, fa_grup.fibukonto)]})

            if not gl_acct:
                q1_list.avail_glacct1 = True


            else:
                fibu_list = Fibu_list()
                fibu_list_data.append(fibu_list)

                fibu_list.fibukonto = fa_grup.fibukonto
                fibu_list.bezeich = gl_acct.bezeich
                fibu_list.flag = 1

        if q1_list.avail_glacct1 == False:
            fibu_list.debit =  to_decimal(fibu_list.debit) + to_decimal(fa_artikel.warenwert)

        fibu_list = query(fibu_list_data, filters=(lambda fibu_list: fibu_list.fibukonto == fa_grup.credit_fibu), first=True)

        if not fibu_list:

            gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, fa_grup.credit_fibu)]})

            if not gl_acct:
                q1_list.avail_glacct2 = True


            else:
                fibu_list = Fibu_list()
                fibu_list_data.append(fibu_list)

                fibu_list.fibukonto = fa_grup.credit_fibu
                fibu_list.bezeich = gl_acct.bezeich
                fibu_list.flag = 2

        if q1_list.avail_glacct2 == False:
            fibu_list.credit =  to_decimal(fibu_list.credit) + to_decimal(fa_artikel.depn_wert)

        fibu_list = query(fibu_list_data, filters=(lambda fibu_list: fibu_list.fibukonto == fa_grup.debit_fibu), first=True)

        if not fibu_list:

            gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, fa_grup.debit_fibu)]})

            if not gl_acct:
                q1_list.avail_glacct3 = True


            else:
                fibu_list = Fibu_list()
                fibu_list_data.append(fibu_list)

                fibu_list.fibukonto = fa_grup.debit_fibu
                fibu_list.bezeich = gl_acct.bezeich
                fibu_list.flag = 3

        if q1_list.avail_glacct3 == False:
            fibu_list.debit =  to_decimal(fibu_list.debit) + to_decimal(fa_artikel.depn_wert)

    return generate_output()