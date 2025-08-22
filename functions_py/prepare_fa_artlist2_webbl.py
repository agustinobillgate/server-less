#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.htpdate import htpdate
from sqlalchemy import func
from models import Mathis, Fa_grup, Fa_artikel, Fa_lager, Fa_kateg, Gl_acct

payload_list_data, Payload_list = create_model("Payload_list", {"from_date":date, "to_date":date, "location":int, "show_all":bool, "asset_name":string, "remark":string, "asset_number":string, "sorttype":int, "last_nr":int, "last_artname":string, "last_remark":string, "last_asset_number":string, "mode":int, "num_data":int, "rec_id":int})

def prepare_fa_artlist2_webbl(payload_list_data:[Payload_list]):

    prepare_cache ([Fa_grup, Fa_artikel, Fa_lager, Fa_kateg, Gl_acct])

    p_881 = None
    q1_list_data = []
    fibu_list_data = []
    output_list_data = []
    t_moving_data = []
    t_upgrade_data = []
    t_prepare_creatpo_data = []
    sort_loc:string = ""
    counter:int = 0
    counter_num_data:int = 0
    mathis = fa_grup = fa_artikel = fa_lager = fa_kateg = gl_acct = None

    q1_list = fibu_list = payload_list = output_list = t_moving = t_upgrade = t_prepare_creatpo = bfa_grup = None

    q1_list_data, Q1_list = create_model("Q1_list", {"name":string, "asset":string, "datum":date, "price":Decimal, "anzahl":int, "warenwert":Decimal, "depn_wert":Decimal, "book_wert":Decimal, "katnr":int, "bezeich":string, "location":string, "first_depn":date, "next_depn":date, "last_depn":date, "id":string, "created":date, "cid":string, "changed":date, "remark":string, "mathis_nr":int, "fname":string, "supplier":string, "posted":bool, "fibukonto":string, "faartikel_nr":int, "credit_fibu":string, "debit_fibu":string, "recid_fa_artikel":int, "recid_mathis":int, "avail_glacct1":bool, "avail_glacct2":bool, "avail_glacct3":bool, "subgroup":int, "model":string, "gnr":int, "flag":int, "grp_bez":string, "sgrp_bez":string, "rate":Decimal, "mark":string, "spec":string, "anz_depn":int, "category":int, "lager_nr":int, "isupgrade":string})
    fibu_list_data, Fibu_list = create_model("Fibu_list", {"flag":int, "fibukonto":string, "bezeich":string, "credit":Decimal, "debit":Decimal})
    output_list_data, Output_list = create_model("Output_list", {"curr_nr":int, "curr_loc":int, "curr_artname":string, "curr_remark":string, "curr_asset_number":string, "is_already_six_digit":bool})
    t_moving_data, T_moving = create_model_like(Mathis, {"curr_nr":int, "curr_loc":int, "curr_artname":string, "curr_remark":string, "curr_asset_number":string})
    t_upgrade_data, T_upgrade = create_model("T_upgrade", {"curr_nr":int, "curr_loc":int, "curr_artname":string, "curr_remark":string, "curr_asset_number":string})
    t_prepare_creatpo_data, T_prepare_creatpo = create_model("T_prepare_creatpo", {"curr_nr":int, "curr_loc":int, "curr_artname":string, "curr_remark":string, "curr_asset_number":string})

    Bfa_grup = create_buffer("Bfa_grup",Fa_grup)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal p_881, q1_list_data, fibu_list_data, output_list_data, t_moving_data, t_upgrade_data, t_prepare_creatpo_data, sort_loc, counter, counter_num_data, mathis, fa_grup, fa_artikel, fa_lager, fa_kateg, gl_acct
        nonlocal bfa_grup


        nonlocal q1_list, fibu_list, payload_list, output_list, t_moving, t_upgrade, t_prepare_creatpo, bfa_grup
        nonlocal q1_list_data, fibu_list_data, output_list_data, t_moving_data, t_upgrade_data, t_prepare_creatpo_data

        return {"p_881": p_881, "q1-list": q1_list_data, "fibu-list": fibu_list_data, "output-list": output_list_data, "t-moving": t_moving_data, "t-upgrade": t_upgrade_data, "t-prepare-creatPO": t_prepare_creatpo_data}

    def cr_assetname():

        nonlocal p_881, q1_list_data, fibu_list_data, output_list_data, t_moving_data, t_upgrade_data, t_prepare_creatpo_data, sort_loc, counter, counter_num_data, mathis, fa_grup, fa_artikel, fa_lager, fa_kateg, gl_acct
        nonlocal bfa_grup


        nonlocal q1_list, fibu_list, payload_list, output_list, t_moving, t_upgrade, t_prepare_creatpo, bfa_grup
        nonlocal q1_list_data, fibu_list_data, output_list_data, t_moving_data, t_upgrade_data, t_prepare_creatpo_data


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


    def cr_remark():

        nonlocal p_881, q1_list_data, fibu_list_data, output_list_data, t_moving_data, t_upgrade_data, t_prepare_creatpo_data, sort_loc, counter, counter_num_data, mathis, fa_grup, fa_artikel, fa_lager, fa_kateg, gl_acct
        nonlocal bfa_grup


        nonlocal q1_list, fibu_list, payload_list, output_list, t_moving, t_upgrade, t_prepare_creatpo, bfa_grup
        nonlocal q1_list_data, fibu_list_data, output_list_data, t_moving_data, t_upgrade_data, t_prepare_creatpo_data


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


    def cr_location():

        nonlocal p_881, q1_list_data, fibu_list_data, output_list_data, t_moving_data, t_upgrade_data, t_prepare_creatpo_data, sort_loc, counter, counter_num_data, mathis, fa_grup, fa_artikel, fa_lager, fa_kateg, gl_acct
        nonlocal bfa_grup


        nonlocal q1_list, fibu_list, payload_list, output_list, t_moving, t_upgrade, t_prepare_creatpo, bfa_grup
        nonlocal q1_list_data, fibu_list_data, output_list_data, t_moving_data, t_upgrade_data, t_prepare_creatpo_data


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


    def cr_asset_number():

        nonlocal p_881, q1_list_data, fibu_list_data, output_list_data, t_moving_data, t_upgrade_data, t_prepare_creatpo_data, sort_loc, counter, counter_num_data, mathis, fa_grup, fa_artikel, fa_lager, fa_kateg, gl_acct
        nonlocal bfa_grup


        nonlocal q1_list, fibu_list, payload_list, output_list, t_moving, t_upgrade, t_prepare_creatpo, bfa_grup
        nonlocal q1_list_data, fibu_list_data, output_list_data, t_moving_data, t_upgrade_data, t_prepare_creatpo_data


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


    def cr_asset_list():

        nonlocal p_881, q1_list_data, fibu_list_data, output_list_data, t_moving_data, t_upgrade_data, t_prepare_creatpo_data, sort_loc, counter, counter_num_data, mathis, fa_grup, fa_artikel, fa_lager, fa_kateg, gl_acct
        nonlocal bfa_grup


        nonlocal q1_list, fibu_list, payload_list, output_list, t_moving, t_upgrade, t_prepare_creatpo, bfa_grup
        nonlocal q1_list_data, fibu_list_data, output_list_data, t_moving_data, t_upgrade_data, t_prepare_creatpo_data


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

        if mathis.flag == 2:
            q1_list.isupgrade = "Yes"


        else:
            q1_list.isupgrade = "No"

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

    p_881 = get_output(htpdate(881))

    payload_list = query(payload_list_data, first=True)
    output_list = Output_list()
    output_list_data.append(output_list)


    if payload_list.num_data != None and payload_list.num_data != 0:
        counter_num_data = payload_list.num_data
    else:
        counter_num_data = 30

    if payload_list.mode == 1:

        if payload_list.show_all == False:

            if payload_list.sorttype == 1:

                if payload_list.asset_name != None and payload_list.asset_name != "":

                    mathis_obj_list = {}
                    for mathis, fa_artikel, fa_grup in db_session.query(Mathis, Fa_artikel, Fa_grup).join(Fa_artikel,(Fa_artikel.nr == Mathis.nr) & (Fa_artikel.loeschflag == 0)).join(Fa_grup,(Fa_grup.gnr == Fa_artikel.subgrp) & (Fa_grup.flag == 1)).filter(
                             (Mathis.datum >= payload_list.from_date) & (Mathis.datum <= payload_list.to_date) & (matches(Mathis.name,("*" + payload_list.asset_name + "*")))).order_by(Mathis.name).yield_per(100):
                        if mathis_obj_list.get(mathis._recid):
                            continue
                        else:
                            mathis_obj_list[mathis._recid] = True

                        if (counter >= counter_num_data) and (output_list.curr_artname != mathis.name):
                            break
                        cr_asset_list()
                        counter = counter + 1
                        output_list.curr_artname = mathis.name
                else:

                    mathis_obj_list = {}
                    for mathis, fa_artikel, fa_grup in db_session.query(Mathis, Fa_artikel, Fa_grup).join(Fa_artikel,(Fa_artikel.nr == Mathis.nr) & (Fa_artikel.loeschflag == 0)).join(Fa_grup,(Fa_grup.gnr == Fa_artikel.subgrp) & (Fa_grup.flag == 1)).filter(
                             (Mathis.datum >= payload_list.from_date) & (Mathis.datum <= payload_list.to_date) & (Mathis.name >= payload_list.asset_name)).order_by(Mathis.name).yield_per(100):
                        if mathis_obj_list.get(mathis._recid):
                            continue
                        else:
                            mathis_obj_list[mathis._recid] = True

                        if (counter >= counter_num_data) and (output_list.curr_artname != mathis.name):
                            break
                        cr_asset_list()
                        counter = counter + 1
                        output_list.curr_artname = mathis.name

            elif payload_list.sorttype == 2:

                if payload_list.remark != None and payload_list.remark != "":

                    mathis_obj_list = {}
                    for mathis, fa_artikel, fa_grup in db_session.query(Mathis, Fa_artikel, Fa_grup).join(Fa_artikel,(Fa_artikel.nr == Mathis.nr) & (Fa_artikel.loeschflag == 0)).join(Fa_grup,(Fa_grup.gnr == Fa_artikel.subgrp) & (Fa_grup.flag == 1)).filter(
                             (Mathis.datum >= payload_list.from_date) & (Mathis.datum <= payload_list.to_date) & (matches(Mathis.remark,("*" + payload_list.remark + "*")))).order_by(Mathis.remark).yield_per(100):
                        if mathis_obj_list.get(mathis._recid):
                            continue
                        else:
                            mathis_obj_list[mathis._recid] = True

                        if (counter >= counter_num_data) and (output_list.curr_remark != mathis.remark):
                            break
                        cr_asset_list()
                        counter = counter + 1
                        output_list.curr_remark = mathis.remark
                else:

                    mathis_obj_list = {}
                    for mathis, fa_artikel, fa_grup in db_session.query(Mathis, Fa_artikel, Fa_grup).join(Fa_artikel,(Fa_artikel.nr == Mathis.nr) & (Fa_artikel.loeschflag == 0)).join(Fa_grup,(Fa_grup.gnr == Fa_artikel.subgrp) & (Fa_grup.flag == 1)).filter(
                             (Mathis.datum >= payload_list.from_date) & (Mathis.datum <= payload_list.to_date) & (Mathis.remark >= payload_list.remark)).order_by(Mathis.name).yield_per(100):
                        if mathis_obj_list.get(mathis._recid):
                            continue
                        else:
                            mathis_obj_list[mathis._recid] = True

                        if (counter >= counter_num_data) and (output_list.curr_artname != mathis.name):
                            break
                        cr_asset_list()
                        counter = counter + 1
                        output_list.curr_artname = mathis.name

            elif payload_list.sorttype == 3:

                if payload_list.location != None and payload_list.location != 0:

                    mathis_obj_list = {}
                    for mathis, fa_artikel, fa_grup in db_session.query(Mathis, Fa_artikel, Fa_grup).join(Fa_artikel,(Fa_artikel.nr == Mathis.nr) & (Fa_artikel.loeschflag == 0)).join(Fa_grup,(Fa_grup.gnr == Fa_artikel.subgrp) & (Fa_grup.flag == 1)).filter(
                             (Mathis.datum >= payload_list.from_date) & (Mathis.datum <= payload_list.to_date)).order_by(Mathis.nr).yield_per(100):
                        if mathis_obj_list.get(mathis._recid):
                            continue
                        else:
                            mathis_obj_list[mathis._recid] = True

                        fa_lager = get_cache (Fa_lager, {"lager_nr": [(eq, payload_list.location)],"bezeich": [(eq, mathis.location)]})

                        if fa_lager:

                            if (counter >= counter_num_data) and (output_list.curr_nr != mathis.nr):
                                break
                            cr_asset_list()
                            counter = counter + 1
                            output_list.curr_nr = mathis.nr
                            output_list.curr_loc = fa_lager.lager_nr
                else:

                    mathis_obj_list = {}
                    for mathis, fa_artikel, fa_grup in db_session.query(Mathis, Fa_artikel, Fa_grup).join(Fa_artikel,(Fa_artikel.nr == Mathis.nr) & (Fa_artikel.loeschflag == 0)).join(Fa_grup,(Fa_grup.gnr == Fa_artikel.subgrp) & (Fa_grup.flag == 1)).filter(
                             (Mathis.datum >= payload_list.from_date) & (Mathis.datum <= payload_list.to_date)).order_by(Mathis.nr).yield_per(100):
                        if mathis_obj_list.get(mathis._recid):
                            continue
                        else:
                            mathis_obj_list[mathis._recid] = True

                        if (counter >= counter_num_data) and (output_list.curr_nr != mathis.nr):
                            break
                        cr_asset_list()
                        counter = counter + 1
                        output_list.curr_nr = mathis.nr
                        output_list.curr_loc = fa_lager.lager_nr

            elif payload_list.sorttype == 4:

                if payload_list.asset_number != None and payload_list.asset_number != "":

                    mathis_obj_list = {}
                    for mathis, fa_artikel, fa_grup in db_session.query(Mathis, Fa_artikel, Fa_grup).join(Fa_artikel,(Fa_artikel.nr == Mathis.nr) & (Fa_artikel.loeschflag == 0)).join(Fa_grup,(Fa_grup.gnr == Fa_artikel.subgrp) & (Fa_grup.flag == 1)).filter(
                             (Mathis.datum >= payload_list.from_date) & (Mathis.datum <= payload_list.to_date) & (matches(Mathis.asset,("*" + trim(payload_list.asset_number) + "*")))).order_by(Mathis.asset).yield_per(100):
                        if mathis_obj_list.get(mathis._recid):
                            continue
                        else:
                            mathis_obj_list[mathis._recid] = True

                        if (counter >= counter_num_data) and (output_list.curr_asset_number != mathis.asset):
                            break
                        cr_asset_list()
                        counter = counter + 1
                        output_list.curr_asset_number = mathis.asset
                else:

                    mathis_obj_list = {}
                    for mathis, fa_artikel, fa_grup in db_session.query(Mathis, Fa_artikel, Fa_grup).join(Fa_artikel,(Fa_artikel.nr == Mathis.nr) & (Fa_artikel.loeschflag == 0)).join(Fa_grup,(Fa_grup.gnr == Fa_artikel.subgrp) & (Fa_grup.flag == 1)).filter(
                             (Mathis.datum >= payload_list.from_date) & (Mathis.datum <= payload_list.to_date) & (Mathis.asset > trim(payload_list.asset_number))).order_by(Mathis.asset).yield_per(100):
                        if mathis_obj_list.get(mathis._recid):
                            continue
                        else:
                            mathis_obj_list[mathis._recid] = True

                        if (counter >= counter_num_data) and (output_list.curr_asset_number != mathis.asset):
                            break
                        cr_asset_list()
                        counter = counter + 1
                        output_list.curr_asset_number = mathis.asset
            else:

                if payload_list.last_artname != "" and payload_list.last_artname != None:

                    if payload_list.asset_name != None and payload_list.asset_name != "":

                        mathis_obj_list = {}
                        for mathis, fa_artikel, fa_grup in db_session.query(Mathis, Fa_artikel, Fa_grup).join(Fa_artikel,(Fa_artikel.nr == Mathis.nr) & (Fa_artikel.loeschflag == 0)).join(Fa_grup,(Fa_grup.gnr == Fa_artikel.subgrp) & (Fa_grup.flag == 1)).filter(
                                 (Mathis.datum >= payload_list.from_date) & (Mathis.datum <= payload_list.to_date) & (matches(Mathis.name,("*" + payload_list.asset_name + "*"))) & (Mathis.name > payload_list.last_artname)).order_by(Mathis.name).yield_per(100):
                            if mathis_obj_list.get(mathis._recid):
                                continue
                            else:
                                mathis_obj_list[mathis._recid] = True

                            if (counter >= counter_num_data) and (output_list.curr_artname != mathis.name):
                                break
                            cr_asset_list()
                            counter = counter + 1
                            output_list.curr_artname = mathis.name
                    else:

                        mathis_obj_list = {}
                        for mathis, fa_artikel, fa_grup in db_session.query(Mathis, Fa_artikel, Fa_grup).join(Fa_artikel,(Fa_artikel.nr == Mathis.nr) & (Fa_artikel.loeschflag == 0)).join(Fa_grup,(Fa_grup.gnr == Fa_artikel.subgrp) & (Fa_grup.flag == 1)).filter(
                                 (Mathis.datum >= payload_list.from_date) & (Mathis.datum <= payload_list.to_date) & (Mathis.name > payload_list.last_artname)).order_by(Mathis.name).yield_per(100):
                            if mathis_obj_list.get(mathis._recid):
                                continue
                            else:
                                mathis_obj_list[mathis._recid] = True

                            if (counter >= counter_num_data) and (output_list.curr_artname != mathis.name):
                                break
                            cr_asset_list()
                            counter = counter + 1
                            output_list.curr_artname = mathis.name

                if payload_list.last_remark != "" and payload_list.last_remark != None:

                    mathis_obj_list = {}
                    for mathis, fa_artikel, fa_grup in db_session.query(Mathis, Fa_artikel, Fa_grup).join(Fa_artikel,(Fa_artikel.nr == Mathis.nr) & (Fa_artikel.loeschflag == 0)).join(Fa_grup,(Fa_grup.gnr == Fa_artikel.subgrp) & (Fa_grup.flag == 1)).filter(
                             (Mathis.remark > payload_list.last_remark)).order_by(Mathis.remark).yield_per(100):
                        if mathis_obj_list.get(mathis._recid):
                            continue
                        else:
                            mathis_obj_list[mathis._recid] = True

                        if (counter >= counter_num_data) and (output_list.curr_artname != mathis.name):
                            break
                        cr_asset_list()
                        counter = counter + 1
                        output_list.curr_artname = mathis.name

                if payload_list.last_nr != None and payload_list.last_nr != 0:

                    if payload_list.location != None and payload_list.location != 0:

                        mathis_obj_list = {}
                        for mathis, fa_artikel, fa_grup in db_session.query(Mathis, Fa_artikel, Fa_grup).join(Fa_artikel,(Fa_artikel.nr == Mathis.nr) & (Fa_artikel.loeschflag == 0)).join(Fa_grup,(Fa_grup.gnr == Fa_artikel.subgrp) & (Fa_grup.flag == 1)).filter(
                                 (Mathis.datum >= payload_list.from_date) & (Mathis.datum <= payload_list.to_date) & (Mathis.nr > payload_list.last_nr)).order_by(Mathis.nr).yield_per(100):
                            if mathis_obj_list.get(mathis._recid):
                                continue
                            else:
                                mathis_obj_list[mathis._recid] = True

                            fa_lager = get_cache (Fa_lager, {"lager_nr": [(eq, payload_list.location)],"bezeich": [(eq, mathis.location)]})

                            if fa_lager:

                                if (counter >= counter_num_data) and (output_list.curr_nr != mathis.nr):
                                    break
                                cr_asset_list()
                                counter = counter + 1
                                output_list.curr_nr = mathis.nr
                                output_list.curr_loc = fa_lager.lager_nr
                    else:

                        mathis_obj_list = {}
                        for mathis, fa_artikel, fa_grup in db_session.query(Mathis, Fa_artikel, Fa_grup).join(Fa_artikel,(Fa_artikel.nr == Mathis.nr) & (Fa_artikel.loeschflag == 0)).join(Fa_grup,(Fa_grup.gnr == Fa_artikel.subgrp) & (Fa_grup.flag == 1)).filter(
                                 (Mathis.datum >= payload_list.from_date) & (Mathis.datum <= payload_list.to_date) & (Mathis.nr > payload_list.last_nr)).order_by(Mathis.nr).yield_per(100):
                            if mathis_obj_list.get(mathis._recid):
                                continue
                            else:
                                mathis_obj_list[mathis._recid] = True

                            if (counter >= counter_num_data) and (output_list.curr_nr != mathis.nr):
                                break
                            cr_asset_list()
                            counter = counter + 1
                            output_list.curr_nr = mathis.nr
                            output_list.curr_loc = fa_lager.lager_nr

                if payload_list.last_asset_number != None and payload_list.last_asset_number != "":

                    if trim(payload_list.asset_number) != None and trim(payload_list.asset_number) != "":

                        mathis_obj_list = {}
                        for mathis, fa_artikel, fa_grup in db_session.query(Mathis, Fa_artikel, Fa_grup).join(Fa_artikel,(Fa_artikel.nr == Mathis.nr) & (Fa_artikel.loeschflag == 0)).join(Fa_grup,(Fa_grup.gnr == Fa_artikel.subgrp) & (Fa_grup.flag == 1)).filter(
                                 (Mathis.datum >= payload_list.from_date) & (Mathis.datum <= payload_list.to_date) & (Mathis.asset > payload_list.last_asset_number) & (matches(Mathis.asset,("*" + trim(payload_list.asset_number) + "*")))).order_by(Mathis.asset).yield_per(100):
                            if mathis_obj_list.get(mathis._recid):
                                continue
                            else:
                                mathis_obj_list[mathis._recid] = True

                            if (counter >= counter_num_data) and (output_list.curr_asset_number != mathis.asset):
                                break
                            cr_asset_list()
                            counter = counter + 1
                            output_list.curr_asset_number = mathis.asset
                    else:

                        mathis_obj_list = {}
                        for mathis, fa_artikel, fa_grup in db_session.query(Mathis, Fa_artikel, Fa_grup).join(Fa_artikel,(Fa_artikel.nr == Mathis.nr) & (Fa_artikel.loeschflag == 0)).join(Fa_grup,(Fa_grup.gnr == Fa_artikel.subgrp) & (Fa_grup.flag == 1)).filter(
                                 (Mathis.datum >= payload_list.from_date) & (Mathis.datum <= payload_list.to_date) & (Mathis.asset > payload_list.last_asset_number)).order_by(Mathis.asset).yield_per(100):
                            if mathis_obj_list.get(mathis._recid):
                                continue
                            else:
                                mathis_obj_list[mathis._recid] = True

                            if (counter >= counter_num_data) and (output_list.curr_asset_number != mathis.asset):
                                break
                            cr_asset_list()
                            counter = counter + 1
                            output_list.curr_asset_number = mathis.asset
        else:

            if payload_list.sorttype == 1:

                if payload_list.asset_name != None and payload_list.asset_name != "":

                    mathis_obj_list = {}
                    for mathis, fa_artikel, fa_grup in db_session.query(Mathis, Fa_artikel, Fa_grup).join(Fa_artikel,(Fa_artikel.nr == Mathis.nr) & (Fa_artikel.loeschflag == 0)).join(Fa_grup,(Fa_grup.gnr == Fa_artikel.subgrp) & (Fa_grup.flag == 1)).filter(
                             (matches(Mathis.name,("*" + payload_list.asset_name + "*")))).order_by(Mathis.name).yield_per(100):
                        if mathis_obj_list.get(mathis._recid):
                            continue
                        else:
                            mathis_obj_list[mathis._recid] = True

                        if (counter >= counter_num_data) and (output_list.curr_artname != mathis.name):
                            break
                        cr_asset_list()
                        counter = counter + 1
                        output_list.curr_artname = mathis.name
                else:

                    mathis_obj_list = {}
                    for mathis, fa_artikel, fa_grup in db_session.query(Mathis, Fa_artikel, Fa_grup).join(Fa_artikel,(Fa_artikel.nr == Mathis.nr) & (Fa_artikel.loeschflag == 0)).join(Fa_grup,(Fa_grup.gnr == Fa_artikel.subgrp) & (Fa_grup.flag == 1)).filter(
                             (Mathis.name >= payload_list.asset_name)).order_by(Mathis.name).yield_per(100):
                        if mathis_obj_list.get(mathis._recid):
                            continue
                        else:
                            mathis_obj_list[mathis._recid] = True

                        if (counter >= counter_num_data) and (output_list.curr_artname != mathis.name):
                            break
                        cr_asset_list()
                        counter = counter + 1
                        output_list.curr_artname = mathis.name

            elif payload_list.sorttype == 2:

                if payload_list.remark != None and payload_list.remark != "":

                    mathis_obj_list = {}
                    for mathis, fa_artikel, fa_grup in db_session.query(Mathis, Fa_artikel, Fa_grup).join(Fa_artikel,(Fa_artikel.nr == Mathis.nr) & (Fa_artikel.loeschflag == 0)).join(Fa_grup,(Fa_grup.gnr == Fa_artikel.subgrp) & (Fa_grup.flag == 1)).filter(
                             (matches(Mathis.remark,("*" + payload_list.remark + "*")))).order_by(Mathis.remark).yield_per(100):
                        if mathis_obj_list.get(mathis._recid):
                            continue
                        else:
                            mathis_obj_list[mathis._recid] = True

                        if counter >= 100:
                            break

                        if (counter >= counter_num_data) and (output_list.curr_remark != mathis.remark):
                            break
                        cr_asset_list()
                        counter = counter + 1
                        output_list.curr_remark = mathis.remark
                else:

                    mathis_obj_list = {}
                    for mathis, fa_artikel, fa_grup in db_session.query(Mathis, Fa_artikel, Fa_grup).join(Fa_artikel,(Fa_artikel.nr == Mathis.nr) & (Fa_artikel.loeschflag == 0)).join(Fa_grup,(Fa_grup.gnr == Fa_artikel.subgrp) & (Fa_grup.flag == 1)).filter(
                             (Mathis.remark >= payload_list.remark)).order_by(Mathis.name).yield_per(100):
                        if mathis_obj_list.get(mathis._recid):
                            continue
                        else:
                            mathis_obj_list[mathis._recid] = True

                        if (counter >= counter_num_data) and (output_list.curr_artname != mathis.name):
                            break
                        cr_asset_list()
                        counter = counter + 1
                        output_list.curr_artname = mathis.name

            elif payload_list.sorttype == 3:

                if payload_list.location != None and payload_list.location != 0:

                    mathis_obj_list = {}
                    for mathis, fa_artikel, fa_grup in db_session.query(Mathis, Fa_artikel, Fa_grup).join(Fa_artikel,(Fa_artikel.nr == Mathis.nr) & (Fa_artikel.loeschflag == 0)).join(Fa_grup,(Fa_grup.gnr == Fa_artikel.subgrp) & (Fa_grup.flag == 1)).order_by(Mathis.nr).yield_per(100):
                        if mathis_obj_list.get(mathis._recid):
                            continue
                        else:
                            mathis_obj_list[mathis._recid] = True

                        fa_lager = get_cache (Fa_lager, {"lager_nr": [(eq, payload_list.location)],"bezeich": [(eq, mathis.location)]})

                        if fa_lager:

                            if (counter >= counter_num_data) and (output_list.curr_nr != mathis.nr):
                                break
                            cr_asset_list()
                            counter = counter + 1
                            output_list.curr_nr = mathis.nr
                            output_list.curr_loc = fa_lager.lager_nr
                else:

                    mathis_obj_list = {}
                    for mathis, fa_artikel, fa_grup in db_session.query(Mathis, Fa_artikel, Fa_grup).join(Fa_artikel,(Fa_artikel.nr == Mathis.nr) & (Fa_artikel.loeschflag == 0)).join(Fa_grup,(Fa_grup.gnr == Fa_artikel.subgrp) & (Fa_grup.flag == 1)).order_by(Mathis.nr).yield_per(100):
                        if mathis_obj_list.get(mathis._recid):
                            continue
                        else:
                            mathis_obj_list[mathis._recid] = True

                        if (counter >= counter_num_data) and (output_list.curr_nr != mathis.nr):
                            break
                        cr_asset_list()
                        counter = counter + 1
                        output_list.curr_nr = mathis.nr
                        output_list.curr_loc = fa_lager.lager_nr

            elif payload_list.sorttype == 4:

                if payload_list.asset_number != None and payload_list.asset_number != "":

                    mathis_obj_list = {}
                    for mathis, fa_artikel, fa_grup in db_session.query(Mathis, Fa_artikel, Fa_grup).join(Fa_artikel,(Fa_artikel.nr == Mathis.nr) & (Fa_artikel.loeschflag == 0)).join(Fa_grup,(Fa_grup.gnr == Fa_artikel.subgrp) & (Fa_grup.flag == 1)).filter(
                             (matches(Mathis.asset,("*" + trim(payload_list.asset_number) + "*")))).order_by(Mathis.asset).yield_per(100):
                        if mathis_obj_list.get(mathis._recid):
                            continue
                        else:
                            mathis_obj_list[mathis._recid] = True

                        if (counter >= counter_num_data) and (output_list.curr_asset_number != mathis.asset):
                            break
                        cr_asset_list()
                        counter = counter + 1
                        output_list.curr_asset_number = mathis.asset
                else:

                    mathis_obj_list = {}
                    for mathis, fa_artikel, fa_grup in db_session.query(Mathis, Fa_artikel, Fa_grup).join(Fa_artikel,(Fa_artikel.nr == Mathis.nr) & (Fa_artikel.loeschflag == 0)).join(Fa_grup,(Fa_grup.gnr == Fa_artikel.subgrp) & (Fa_grup.flag == 1)).filter(
                             (Mathis.asset > trim(payload_list.asset_number))).order_by(Mathis.asset).yield_per(100):
                        if mathis_obj_list.get(mathis._recid):
                            continue
                        else:
                            mathis_obj_list[mathis._recid] = True

                        if (counter >= counter_num_data) and (output_list.curr_asset_number != mathis.asset):
                            break
                        cr_asset_list()
                        counter = counter + 1
                        output_list.curr_asset_number = mathis.asset

            elif payload_list.sorttype == 6:

                mathis_obj_list = {}
                for mathis, fa_artikel, fa_grup in db_session.query(Mathis, Fa_artikel, Fa_grup).join(Fa_artikel,(Fa_artikel.nr == Mathis.nr) & (Fa_artikel.loeschflag == 0)).join(Fa_grup,(Fa_grup.gnr == Fa_artikel.subgrp) & (Fa_grup.flag == 1)).order_by(Mathis.name).all():
                    if mathis_obj_list.get(mathis._recid):
                        continue
                    else:
                        mathis_obj_list[mathis._recid] = True


                    cr_asset_list()
            else:

                if payload_list.last_artname != "" and payload_list.last_artname != None:

                    if payload_list.asset_name != None and payload_list.asset_name != "":

                        mathis_obj_list = {}
                        for mathis, fa_artikel, fa_grup in db_session.query(Mathis, Fa_artikel, Fa_grup).join(Fa_artikel,(Fa_artikel.nr == Mathis.nr) & (Fa_artikel.loeschflag == 0)).join(Fa_grup,(Fa_grup.gnr == Fa_artikel.subgrp) & (Fa_grup.flag == 1)).filter(
                                 (matches(Mathis.name,("*" + payload_list.asset_name + "*"))) & (Mathis.name > payload_list.last_artname)).order_by(Mathis.name).yield_per(100):
                            if mathis_obj_list.get(mathis._recid):
                                continue
                            else:
                                mathis_obj_list[mathis._recid] = True

                            if (counter >= counter_num_data) and (output_list.curr_artname != mathis.name):
                                break
                            cr_asset_list()
                            counter = counter + 1
                            output_list.curr_artname = mathis.name
                    else:

                        mathis_obj_list = {}
                        for mathis, fa_artikel, fa_grup in db_session.query(Mathis, Fa_artikel, Fa_grup).join(Fa_artikel,(Fa_artikel.nr == Mathis.nr) & (Fa_artikel.loeschflag == 0)).join(Fa_grup,(Fa_grup.gnr == Fa_artikel.subgrp) & (Fa_grup.flag == 1)).filter(
                                 (Mathis.name > payload_list.last_artname)).order_by(Mathis.name).yield_per(100):
                            if mathis_obj_list.get(mathis._recid):
                                continue
                            else:
                                mathis_obj_list[mathis._recid] = True

                            if (counter >= counter_num_data) and (output_list.curr_artname != mathis.name):
                                break
                            cr_asset_list()
                            counter = counter + 1
                            output_list.curr_artname = mathis.name

                if payload_list.last_remark != "" and payload_list.last_remark != None:

                    mathis_obj_list = {}
                    for mathis, fa_artikel, fa_grup in db_session.query(Mathis, Fa_artikel, Fa_grup).join(Fa_artikel,(Fa_artikel.nr == Mathis.nr) & (Fa_artikel.loeschflag == 0)).join(Fa_grup,(Fa_grup.gnr == Fa_artikel.subgrp) & (Fa_grup.flag == 1)).filter(
                             (Mathis.remark > payload_list.last_remark)).order_by(Mathis.remark).yield_per(100):
                        if mathis_obj_list.get(mathis._recid):
                            continue
                        else:
                            mathis_obj_list[mathis._recid] = True

                        if (counter >= counter_num_data) and (output_list.curr_artname != mathis.name):
                            break
                        cr_asset_list()
                        counter = counter + 1
                        output_list.curr_artname = mathis.name

                if payload_list.last_nr != None and payload_list.last_nr != 0:

                    if payload_list.location != None and payload_list.location != 0:

                        mathis_obj_list = {}
                        for mathis, fa_artikel, fa_grup in db_session.query(Mathis, Fa_artikel, Fa_grup).join(Fa_artikel,(Fa_artikel.nr == Mathis.nr) & (Fa_artikel.loeschflag == 0)).join(Fa_grup,(Fa_grup.gnr == Fa_artikel.subgrp) & (Fa_grup.flag == 1)).filter(
                                 (Mathis.nr > payload_list.last_nr)).order_by(Mathis.nr).yield_per(100):
                            if mathis_obj_list.get(mathis._recid):
                                continue
                            else:
                                mathis_obj_list[mathis._recid] = True

                            fa_lager = get_cache (Fa_lager, {"lager_nr": [(eq, payload_list.location)],"bezeich": [(eq, mathis.location)]})

                            if fa_lager:

                                if (counter >= counter_num_data) and (output_list.curr_nr != mathis.nr):
                                    break
                                cr_asset_list()
                                counter = counter + 1
                                output_list.curr_nr = mathis.nr
                                output_list.curr_loc = fa_lager.lager_nr
                    else:

                        mathis_obj_list = {}
                        for mathis, fa_artikel, fa_grup in db_session.query(Mathis, Fa_artikel, Fa_grup).join(Fa_artikel,(Fa_artikel.nr == Mathis.nr) & (Fa_artikel.loeschflag == 0)).join(Fa_grup,(Fa_grup.gnr == Fa_artikel.subgrp) & (Fa_grup.flag == 1)).filter(
                                 (Mathis.nr > payload_list.last_nr)).order_by(Mathis.nr).yield_per(100):
                            if mathis_obj_list.get(mathis._recid):
                                continue
                            else:
                                mathis_obj_list[mathis._recid] = True

                            if (counter >= counter_num_data) and (output_list.curr_nr != mathis.nr):
                                break
                            cr_asset_list()
                            counter = counter + 1
                            output_list.curr_nr = mathis.nr
                            output_list.curr_loc = fa_lager.lager_nr

                if payload_list.last_asset_number != None and payload_list.last_asset_number != "":

                    if trim(payload_list.asset_number) != None and trim(payload_list.asset_number) != "":

                        mathis_obj_list = {}
                        for mathis, fa_artikel, fa_grup in db_session.query(Mathis, Fa_artikel, Fa_grup).join(Fa_artikel,(Fa_artikel.nr == Mathis.nr) & (Fa_artikel.loeschflag == 0)).join(Fa_grup,(Fa_grup.gnr == Fa_artikel.subgrp) & (Fa_grup.flag == 1)).filter(
                                 (Mathis.asset > payload_list.last_asset_number) & (matches(Mathis.asset,("*" + trim(payload_list.asset_number) + "*")))).order_by(Mathis.asset).yield_per(100):
                            if mathis_obj_list.get(mathis._recid):
                                continue
                            else:
                                mathis_obj_list[mathis._recid] = True

                            if (counter >= counter_num_data) and (output_list.curr_asset_number != mathis.asset):
                                break
                            cr_asset_list()
                            counter = counter + 1
                            output_list.curr_asset_number = mathis.asset
                    else:

                        mathis_obj_list = {}
                        for mathis, fa_artikel, fa_grup in db_session.query(Mathis, Fa_artikel, Fa_grup).join(Fa_artikel,(Fa_artikel.nr == Mathis.nr) & (Fa_artikel.loeschflag == 0)).join(Fa_grup,(Fa_grup.gnr == Fa_artikel.subgrp) & (Fa_grup.flag == 1)).filter(
                                 (Mathis.asset > payload_list.last_asset_number)).order_by(Mathis.asset).yield_per(100):
                            if mathis_obj_list.get(mathis._recid):
                                continue
                            else:
                                mathis_obj_list[mathis._recid] = True

                            if (counter >= counter_num_data) and (output_list.curr_asset_number != mathis.asset):
                                break
                            cr_asset_list()
                            counter = counter + 1
                            output_list.curr_asset_number = mathis.asset

    elif payload_list.mode == 2:

        if payload_list.sorttype == 1:

            if payload_list.asset_name != None and payload_list.asset_name != "":

                mathis_obj_list = {}
                for mathis, fa_artikel, fa_grup in db_session.query(Mathis, Fa_artikel, Fa_grup).join(Fa_artikel,(Fa_artikel.nr == Mathis.nr) & (Fa_artikel.loeschflag == 0)).join(Fa_grup,(Fa_grup.gnr == Fa_artikel.subgrp) & (Fa_grup.flag == 1)).filter(
                         (matches(Mathis.name,("*" + payload_list.asset_name + "*")))).order_by(Mathis.name).yield_per(100):
                    if mathis_obj_list.get(mathis._recid):
                        continue
                    else:
                        mathis_obj_list[mathis._recid] = True

                    if (counter >= counter_num_data) and (output_list.curr_artname != mathis.name):
                        break
                    cr_asset_list()
                    counter = counter + 1
                    output_list.curr_artname = mathis.name
            else:

                mathis_obj_list = {}
                for mathis, fa_artikel, fa_grup in db_session.query(Mathis, Fa_artikel, Fa_grup).join(Fa_artikel,(Fa_artikel.nr == Mathis.nr) & (Fa_artikel.loeschflag == 0)).join(Fa_grup,(Fa_grup.gnr == Fa_artikel.subgrp) & (Fa_grup.flag == 1)).filter(
                         (Mathis.name >= payload_list.asset_name)).order_by(Mathis.name).yield_per(100):
                    if mathis_obj_list.get(mathis._recid):
                        continue
                    else:
                        mathis_obj_list[mathis._recid] = True

                    if (counter >= counter_num_data) and (output_list.curr_artname != mathis.name):
                        break
                    cr_asset_list()
                    counter = counter + 1
                    output_list.curr_artname = mathis.name
        else:

            if payload_list.last_artname != "" and payload_list.last_artname != None:

                if payload_list.asset_name != None and payload_list.asset_name != "":

                    mathis_obj_list = {}
                    for mathis, fa_artikel, fa_grup in db_session.query(Mathis, Fa_artikel, Fa_grup).join(Fa_artikel,(Fa_artikel.nr == Mathis.nr) & (Fa_artikel.loeschflag == 0)).join(Fa_grup,(Fa_grup.gnr == Fa_artikel.subgrp) & (Fa_grup.flag == 1)).filter(
                             (matches(Mathis.name,("*" + payload_list.asset_name + "*"))) & (Mathis.name > payload_list.last_artname)).order_by(Mathis.name).yield_per(100):
                        if mathis_obj_list.get(mathis._recid):
                            continue
                        else:
                            mathis_obj_list[mathis._recid] = True

                        if (counter >= counter_num_data) and (output_list.curr_artname != mathis.name):
                            break
                        cr_asset_list()
                        counter = counter + 1
                        output_list.curr_artname = mathis.name
                else:

                    mathis_obj_list = {}
                    for mathis, fa_artikel, fa_grup in db_session.query(Mathis, Fa_artikel, Fa_grup).join(Fa_artikel,(Fa_artikel.nr == Mathis.nr) & (Fa_artikel.loeschflag == 0)).join(Fa_grup,(Fa_grup.gnr == Fa_artikel.subgrp) & (Fa_grup.flag == 1)).filter(
                             (Mathis.name > payload_list.last_artname)).order_by(Mathis.name).yield_per(100):
                        if mathis_obj_list.get(mathis._recid):
                            continue
                        else:
                            mathis_obj_list[mathis._recid] = True

                        if (counter >= counter_num_data) and (output_list.curr_artname != mathis.name):
                            break
                        cr_asset_list()
                        counter = counter + 1
                        output_list.curr_artname = mathis.name

    elif payload_list.mode == 3:

        if payload_list.sorttype == 1:

            if payload_list.asset_name != None and payload_list.asset_name != "":

                for mathis in db_session.query(Mathis).filter(
                         (matches(Mathis.name,("*" + payload_list.asset_name + "*")))).order_by(Mathis.name).yield_per(100):

                    if (counter >= counter_num_data) and (output_list.curr_artname != mathis.name):
                        break
                    t_moving = T_moving()
                    t_moving_data.append(t_moving)

                    buffer_copy(mathis, t_moving)
                    counter = counter + 1
                    output_list.curr_artname = mathis.name
            else:

                for mathis in db_session.query(Mathis).filter(
                         (Mathis.name >= payload_list.asset_name)).order_by(Mathis.name).yield_per(100):

                    if (counter >= counter_num_data) and (output_list.curr_artname != mathis.name):
                        break
                    t_moving = T_moving()
                    t_moving_data.append(t_moving)

                    buffer_copy(mathis, t_moving)
                    counter = counter + 1
                    output_list.curr_artname = mathis.name
        else:

            if payload_list.last_artname != "" and payload_list.last_artname != None:

                if payload_list.asset_name != None and payload_list.asset_name != "":

                    for mathis in db_session.query(Mathis).filter(
                             (matches(Mathis.name,("*" + payload_list.asset_name + "*"))) & (Mathis.name > payload_list.last_artname)).order_by(Mathis.name).yield_per(100):

                        if (counter >= counter_num_data) and (output_list.curr_artname != mathis.name):
                            break
                        t_moving = T_moving()
                        t_moving_data.append(t_moving)

                        buffer_copy(mathis, t_moving)
                        counter = counter + 1
                        output_list.curr_artname = mathis.name
                else:

                    for mathis in db_session.query(Mathis).filter(
                             (Mathis.name > payload_list.last_artname)).order_by(Mathis.name).yield_per(100):

                        if (counter >= counter_num_data) and (output_list.curr_artname != mathis.name):
                            break
                        t_moving = T_moving()
                        t_moving_data.append(t_moving)

                        buffer_copy(mathis, t_moving)
                        counter = counter + 1
                        output_list.curr_artname = mathis.name

    elif payload_list.mode == 4:

        mathis = db_session.query(Mathis).filter(
                 (Mathis.flag != 0) & (length(trim(Mathis.asset)) > 10)).first()

        if mathis:
            output_list.is_already_six_digit = True

    elif payload_list.mode == 5:

        if payload_list.show_all == False:

            if payload_list.sorttype == 1:

                if payload_list.asset_name != None and payload_list.asset_name != "":

                    mathis_obj_list = {}
                    for mathis, fa_artikel, fa_grup in db_session.query(Mathis, Fa_artikel, Fa_grup).join(Fa_artikel,(Fa_artikel.nr == Mathis.nr) & (Fa_artikel.loeschflag == 0)).join(Fa_grup,(Fa_grup.gnr == Fa_artikel.subgrp) & (Fa_grup.flag == 1)).filter(
                             (Mathis.datum >= payload_list.from_date) & (Mathis.datum <= payload_list.to_date) & (matches(Mathis.name,("*" + payload_list.asset_name + "*")))).order_by(Mathis.name).yield_per(100):
                        if mathis_obj_list.get(mathis._recid):
                            continue
                        else:
                            mathis_obj_list[mathis._recid] = True


                        cr_asset_list()
                else:

                    mathis_obj_list = {}
                    for mathis, fa_artikel, fa_grup in db_session.query(Mathis, Fa_artikel, Fa_grup).join(Fa_artikel,(Fa_artikel.nr == Mathis.nr) & (Fa_artikel.loeschflag == 0)).join(Fa_grup,(Fa_grup.gnr == Fa_artikel.subgrp) & (Fa_grup.flag == 1)).filter(
                             (Mathis.datum >= payload_list.from_date) & (Mathis.datum <= payload_list.to_date) & (Mathis.name >= payload_list.asset_name)).order_by(Mathis.name).yield_per(100):
                        if mathis_obj_list.get(mathis._recid):
                            continue
                        else:
                            mathis_obj_list[mathis._recid] = True


                        cr_asset_list()

            elif payload_list.sorttype == 2:

                if payload_list.remark != None and payload_list.remark != "":

                    mathis_obj_list = {}
                    for mathis, fa_artikel, fa_grup in db_session.query(Mathis, Fa_artikel, Fa_grup).join(Fa_artikel,(Fa_artikel.nr == Mathis.nr) & (Fa_artikel.loeschflag == 0)).join(Fa_grup,(Fa_grup.gnr == Fa_artikel.subgrp) & (Fa_grup.flag == 1)).filter(
                             (Mathis.datum >= payload_list.from_date) & (Mathis.datum <= payload_list.to_date) & (matches(Mathis.remark,("*" + payload_list.remark + "*")))).order_by(Mathis.remark).yield_per(100):
                        if mathis_obj_list.get(mathis._recid):
                            continue
                        else:
                            mathis_obj_list[mathis._recid] = True


                        cr_asset_list()
                else:

                    mathis_obj_list = {}
                    for mathis, fa_artikel, fa_grup in db_session.query(Mathis, Fa_artikel, Fa_grup).join(Fa_artikel,(Fa_artikel.nr == Mathis.nr) & (Fa_artikel.loeschflag == 0)).join(Fa_grup,(Fa_grup.gnr == Fa_artikel.subgrp) & (Fa_grup.flag == 1)).filter(
                             (Mathis.datum >= payload_list.from_date) & (Mathis.datum <= payload_list.to_date) & (Mathis.remark >= payload_list.remark)).order_by(Mathis.name).yield_per(100):
                        if mathis_obj_list.get(mathis._recid):
                            continue
                        else:
                            mathis_obj_list[mathis._recid] = True


                        cr_asset_list()

            elif payload_list.sorttype == 3:

                if payload_list.location != None and payload_list.location != 0:

                    mathis_obj_list = {}
                    for mathis, fa_artikel, fa_grup in db_session.query(Mathis, Fa_artikel, Fa_grup).join(Fa_artikel,(Fa_artikel.nr == Mathis.nr) & (Fa_artikel.loeschflag == 0)).join(Fa_grup,(Fa_grup.gnr == Fa_artikel.subgrp) & (Fa_grup.flag == 1)).filter(
                             (Mathis.datum >= payload_list.from_date) & (Mathis.datum <= payload_list.to_date)).order_by(Mathis.nr).yield_per(100):
                        if mathis_obj_list.get(mathis._recid):
                            continue
                        else:
                            mathis_obj_list[mathis._recid] = True

                        fa_lager = get_cache (Fa_lager, {"lager_nr": [(eq, payload_list.location)],"bezeich": [(eq, mathis.location)]})

                        if fa_lager:
                            cr_asset_list()
                else:

                    mathis_obj_list = {}
                    for mathis, fa_artikel, fa_grup in db_session.query(Mathis, Fa_artikel, Fa_grup).join(Fa_artikel,(Fa_artikel.nr == Mathis.nr) & (Fa_artikel.loeschflag == 0)).join(Fa_grup,(Fa_grup.gnr == Fa_artikel.subgrp) & (Fa_grup.flag == 1)).filter(
                             (Mathis.datum >= payload_list.from_date) & (Mathis.datum <= payload_list.to_date)).order_by(Mathis.nr).yield_per(100):
                        if mathis_obj_list.get(mathis._recid):
                            continue
                        else:
                            mathis_obj_list[mathis._recid] = True


                        cr_asset_list()

            elif payload_list.sorttype == 4:

                if payload_list.asset_number != None and payload_list.asset_number != "":

                    mathis_obj_list = {}
                    for mathis, fa_artikel, fa_grup in db_session.query(Mathis, Fa_artikel, Fa_grup).join(Fa_artikel,(Fa_artikel.nr == Mathis.nr) & (Fa_artikel.loeschflag == 0)).join(Fa_grup,(Fa_grup.gnr == Fa_artikel.subgrp) & (Fa_grup.flag == 1)).filter(
                             (Mathis.datum >= payload_list.from_date) & (Mathis.datum <= payload_list.to_date) & (matches(Mathis.asset,("*" + trim(payload_list.asset_number) + "*")))).order_by(Mathis.asset).yield_per(100):
                        if mathis_obj_list.get(mathis._recid):
                            continue
                        else:
                            mathis_obj_list[mathis._recid] = True


                        cr_asset_list()
                else:

                    mathis_obj_list = {}
                    for mathis, fa_artikel, fa_grup in db_session.query(Mathis, Fa_artikel, Fa_grup).join(Fa_artikel,(Fa_artikel.nr == Mathis.nr) & (Fa_artikel.loeschflag == 0)).join(Fa_grup,(Fa_grup.gnr == Fa_artikel.subgrp) & (Fa_grup.flag == 1)).filter(
                             (Mathis.datum >= payload_list.from_date) & (Mathis.datum <= payload_list.to_date) & (Mathis.asset > trim(payload_list.asset_number))).order_by(Mathis.asset).yield_per(100):
                        if mathis_obj_list.get(mathis._recid):
                            continue
                        else:
                            mathis_obj_list[mathis._recid] = True


                        cr_asset_list()
        else:

            if payload_list.sorttype == 1:

                if payload_list.asset_name != None and payload_list.asset_name != "":

                    mathis_obj_list = {}
                    for mathis, fa_artikel, fa_grup in db_session.query(Mathis, Fa_artikel, Fa_grup).join(Fa_artikel,(Fa_artikel.nr == Mathis.nr) & (Fa_artikel.loeschflag == 0)).join(Fa_grup,(Fa_grup.gnr == Fa_artikel.subgrp) & (Fa_grup.flag == 1)).filter(
                             (matches(Mathis.name,("*" + payload_list.asset_name + "*")))).order_by(Mathis.name).yield_per(100):
                        if mathis_obj_list.get(mathis._recid):
                            continue
                        else:
                            mathis_obj_list[mathis._recid] = True


                        cr_asset_list()
                else:

                    mathis_obj_list = {}
                    for mathis, fa_artikel, fa_grup in db_session.query(Mathis, Fa_artikel, Fa_grup).join(Fa_artikel,(Fa_artikel.nr == Mathis.nr) & (Fa_artikel.loeschflag == 0)).join(Fa_grup,(Fa_grup.gnr == Fa_artikel.subgrp) & (Fa_grup.flag == 1)).filter(
                             (Mathis.name >= payload_list.asset_name)).order_by(Mathis.name).yield_per(100):
                        if mathis_obj_list.get(mathis._recid):
                            continue
                        else:
                            mathis_obj_list[mathis._recid] = True


                        cr_asset_list()

            elif payload_list.sorttype == 2:

                if payload_list.remark != None and payload_list.remark != "":

                    mathis_obj_list = {}
                    for mathis, fa_artikel, fa_grup in db_session.query(Mathis, Fa_artikel, Fa_grup).join(Fa_artikel,(Fa_artikel.nr == Mathis.nr) & (Fa_artikel.loeschflag == 0)).join(Fa_grup,(Fa_grup.gnr == Fa_artikel.subgrp) & (Fa_grup.flag == 1)).filter(
                             (matches(Mathis.remark,("*" + payload_list.remark + "*")))).order_by(Mathis.remark).yield_per(100):
                        if mathis_obj_list.get(mathis._recid):
                            continue
                        else:
                            mathis_obj_list[mathis._recid] = True


                        cr_asset_list()
                else:

                    mathis_obj_list = {}
                    for mathis, fa_artikel, fa_grup in db_session.query(Mathis, Fa_artikel, Fa_grup).join(Fa_artikel,(Fa_artikel.nr == Mathis.nr) & (Fa_artikel.loeschflag == 0)).join(Fa_grup,(Fa_grup.gnr == Fa_artikel.subgrp) & (Fa_grup.flag == 1)).filter(
                             (Mathis.remark >= payload_list.remark)).order_by(Mathis.name).yield_per(100):
                        if mathis_obj_list.get(mathis._recid):
                            continue
                        else:
                            mathis_obj_list[mathis._recid] = True


                        cr_asset_list()

            elif payload_list.sorttype == 3:

                if payload_list.location != None and payload_list.location != 0:

                    mathis_obj_list = {}
                    for mathis, fa_artikel, fa_grup in db_session.query(Mathis, Fa_artikel, Fa_grup).join(Fa_artikel,(Fa_artikel.nr == Mathis.nr) & (Fa_artikel.loeschflag == 0)).join(Fa_grup,(Fa_grup.gnr == Fa_artikel.subgrp) & (Fa_grup.flag == 1)).order_by(Mathis.nr).yield_per(100):
                        if mathis_obj_list.get(mathis._recid):
                            continue
                        else:
                            mathis_obj_list[mathis._recid] = True

                        fa_lager = get_cache (Fa_lager, {"lager_nr": [(eq, payload_list.location)],"bezeich": [(eq, mathis.location)]})

                        if fa_lager:
                            cr_asset_list()
                else:

                    mathis_obj_list = {}
                    for mathis, fa_artikel, fa_grup in db_session.query(Mathis, Fa_artikel, Fa_grup).join(Fa_artikel,(Fa_artikel.nr == Mathis.nr) & (Fa_artikel.loeschflag == 0)).join(Fa_grup,(Fa_grup.gnr == Fa_artikel.subgrp) & (Fa_grup.flag == 1)).order_by(Mathis.nr).yield_per(100):
                        if mathis_obj_list.get(mathis._recid):
                            continue
                        else:
                            mathis_obj_list[mathis._recid] = True


                        cr_asset_list()

            elif payload_list.sorttype == 4:

                if payload_list.asset_number != None and payload_list.asset_number != "":

                    mathis_obj_list = {}
                    for mathis, fa_artikel, fa_grup in db_session.query(Mathis, Fa_artikel, Fa_grup).join(Fa_artikel,(Fa_artikel.nr == Mathis.nr) & (Fa_artikel.loeschflag == 0)).join(Fa_grup,(Fa_grup.gnr == Fa_artikel.subgrp) & (Fa_grup.flag == 1)).filter(
                             (matches(Mathis.asset,("*" + trim(payload_list.asset_number) + "*")))).order_by(Mathis.asset).yield_per(100):
                        if mathis_obj_list.get(mathis._recid):
                            continue
                        else:
                            mathis_obj_list[mathis._recid] = True


                        cr_asset_list()
                else:

                    mathis_obj_list = {}
                    for mathis, fa_artikel, fa_grup in db_session.query(Mathis, Fa_artikel, Fa_grup).join(Fa_artikel,(Fa_artikel.nr == Mathis.nr) & (Fa_artikel.loeschflag == 0)).join(Fa_grup,(Fa_grup.gnr == Fa_artikel.subgrp) & (Fa_grup.flag == 1)).filter(
                             (Mathis.asset > trim(payload_list.asset_number))).order_by(Mathis.asset).yield_per(100):
                        if mathis_obj_list.get(mathis._recid):
                            continue
                        else:
                            mathis_obj_list[mathis._recid] = True


                        cr_asset_list()

            elif payload_list.sorttype == 5:

                mathis_obj_list = {}
                for mathis, fa_artikel, fa_grup in db_session.query(Mathis, Fa_artikel, Fa_grup).join(Fa_artikel,(Fa_artikel.nr == Mathis.nr) & (Fa_artikel.loeschflag == 0)).join(Fa_grup,(Fa_grup.gnr == Fa_artikel.subgrp) & (Fa_grup.flag == 1)).order_by(Mathis.name).all():
                    if mathis_obj_list.get(mathis._recid):
                        continue
                    else:
                        mathis_obj_list[mathis._recid] = True


                    cr_asset_list()

    elif payload_list.mode == 6:
        for mathis, fa_artikel, fa_grup in db_session.query(Mathis, Fa_artikel, Fa_grup).join(Fa_artikel,(Fa_artikel.nr == Mathis.nr)).join(Fa_grup,(Fa_grup.gnr == Fa_artikel.subgrp) & (Fa_grup.flag == 1)).filter(
            (Fa_artikel._recid == payload_list.rec_id)).order_by(Mathis.name):
            
            cr_asset_list()            

    return generate_output()