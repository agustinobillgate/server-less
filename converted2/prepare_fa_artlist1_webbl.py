#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.prepare_fa_artlist_cldbl import prepare_fa_artlist_cldbl
from models import Fa_grup, Queasy

sortir_list_data, Sortir_list = create_model("Sortir_list", {"from_date":date, "to_date":date, "location":int, "show_all":bool, "asset_name":string, "remark":string})

def prepare_fa_artlist1_webbl(sortir_list_data:[Sortir_list], idflag:string):

    prepare_cache ([Queasy])

    p_881 = None
    q1_list_data = []
    fibu_list_data = []
    sort_loc:string = ""
    mark:string = ""
    htl_no:string = ""
    counter:int = 0
    q1_list_datum:string = ""
    q1_list_first_depn:string = ""
    q1_list_next_depn:string = ""
    q1_list_last_depn:string = ""
    q1_list_created:string = ""
    q1_list_changed:string = ""
    q1_list_supplier:string = ""
    q1_list_price:string = ""
    q1_list_mark:string = ""
    q1_list_model:string = ""
    q1_list_spec:string = ""
    q1_list_remark:string = ""
    fa_grup = queasy = None

    q1_list = fibu_list = sortir_list = bfa_grup = bqueasy = tqueasy = None

    q1_list_data, Q1_list = create_model("Q1_list", {"name":string, "asset":string, "datum":date, "price":Decimal, "anzahl":int, "warenwert":Decimal, "depn_wert":Decimal, "book_wert":Decimal, "katnr":int, "bezeich":string, "location":string, "first_depn":date, "next_depn":date, "last_depn":date, "id":string, "created":date, "cid":string, "changed":date, "remark":string, "mathis_nr":int, "fname":string, "supplier":string, "posted":bool, "fibukonto":string, "faartikel_nr":int, "credit_fibu":string, "debit_fibu":string, "recid_fa_artikel":int, "recid_mathis":int, "avail_glacct1":bool, "avail_glacct2":bool, "avail_glacct3":bool, "subgroup":int, "model":string, "gnr":int, "flag":int, "grp_bez":string, "sgrp_bez":string, "rate":Decimal, "mark":string, "spec":string, "anz_depn":int, "category":int, "lager_nr":int})
    fibu_list_data, Fibu_list = create_model("Fibu_list", {"flag":int, "fibukonto":string, "bezeich":string, "credit":Decimal, "debit":Decimal})

    Bfa_grup = create_buffer("Bfa_grup",Fa_grup)
    Bqueasy = create_buffer("Bqueasy",Queasy)
    Tqueasy = create_buffer("Tqueasy",Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal p_881, q1_list_data, fibu_list_data, sort_loc, mark, htl_no, counter, q1_list_datum, q1_list_first_depn, q1_list_next_depn, q1_list_last_depn, q1_list_created, q1_list_changed, q1_list_supplier, q1_list_price, q1_list_mark, q1_list_model, q1_list_spec, q1_list_remark, fa_grup, queasy
        nonlocal idflag
        nonlocal bfa_grup, bqueasy, tqueasy


        nonlocal q1_list, fibu_list, sortir_list, bfa_grup, bqueasy, tqueasy
        nonlocal q1_list_data, fibu_list_data

        return {"p_881": p_881, "q1-list": q1_list_data, "fibu-list": fibu_list_data}


    queasy = Queasy()
    db_session.add(queasy)

    queasy.key = 285
    queasy.char1 = "Fixed Asset List Report"
    queasy.number1 = 1
    queasy.char2 = idflag


    pass
    p_881, q1_list_data, fibu_list_data = get_output(prepare_fa_artlist_cldbl(sortir_list_data))

    q1_list = query(q1_list_data, first=True)
    while None != q1_list:

        if q1_list.datum == None:
            q1_list_datum = ""
        else:
            q1_list_datum = to_string(q1_list.datum)

        if q1_list.first_depn == None:
            q1_list_first_depn = ""
        else:
            q1_list_first_depn = to_string(q1_list.first_depn)

        if q1_list.next_depn == None:
            q1_list_next_depn = ""
        else:
            q1_list_next_depn = to_string(q1_list.next_depn)

        if q1_list.last_depn == None:
            q1_list_last_depn = ""
        else:
            q1_list_last_depn = to_string(q1_list.last_depn)

        if q1_list.created == None:
            q1_list_created = ""
        else:
            q1_list_created = to_string(q1_list.created)

        if q1_list.changed == None:
            q1_list_changed = ""
        else:
            q1_list_changed = to_string(q1_list.changed)

        if q1_list.supplier == None:
            q1_list_supplier = ""
        else:
            q1_list_supplier = to_string(q1_list.supplier)

        if q1_list.mark == None:
            q1_list_mark = ""
        else:
            q1_list_mark = to_string(q1_list.mark)

        if q1_list.model == None:
            q1_list_model = ""
        else:
            q1_list_model = to_string(q1_list.model)

        if q1_list.spec == None:
            q1_list_spec = ""
        else:
            q1_list_spec = to_string(q1_list.spec)

        if q1_list.remark == None:
            q1_list_remark = ""
        else:
            q1_list_remark = to_string(q1_list.remark)

        if q1_list.price == None:
            q1_list_price = ""
        else:
            q1_list_price = to_string(q1_list.price)

        if q1_list.fname == None:
            q1_list.fname = ""

        if q1_list.id == None:
            q1_list.id = ""

        if q1_list.cid == None:
            q1_list.cid = ""

        if matches(q1_list.name,r"*|*"):
            q1_list.name = replace_str(q1_list.name, "|", " ")

        if matches(q1_list.bezeich,r"*|*"):
            q1_list.bezeich = replace_str(q1_list.bezeich, "|", " ")

        if matches(q1_list.location,r"*|*"):
            q1_list.location = replace_str(q1_list.location, "|", " ")

        if matches(q1_list.id,r"*|*"):
            q1_list.id = replace_str(q1_list.id, "|", " ")

        if matches(q1_list_remark,r"*|*"):
            q1_list_remark = replace_str(q1_list_remark, "|", " ")

        if matches(q1_list_supplier,r"*|*"):
            q1_list_supplier = replace_str(q1_list_supplier, "|", " ")

        if matches(q1_list.grp_bez,r"*|*"):
            q1_list.grp_bez = replace_str(q1_list.grp_bez, "|", " ")

        if matches(q1_list.sgrp_bez,r"*|*"):
            q1_list.sgrp_bez = replace_str(q1_list.sgrp_bez, "|", " ")

        if matches(q1_list_mark,r"*|*"):
            q1_list_mark = replace_str(q1_list_mark, "|", " ")

        if matches(q1_list_spec,r"*|*"):
            q1_list_spec = replace_str(q1_list_spec, "|", " ")
        mark = "article"
        queasy = Queasy()
        db_session.add(queasy)

        counter = counter + 1
        queasy.key = 280
        queasy.char1 = "Fixed Asset List Report"
        queasy.char3 = idflag
        queasy.char2 = to_string(mark) + "|" +\
                to_string(q1_list.name) + "|" +\
                to_string(q1_list.asset) + "|" +\
                to_string(q1_list_datum) + "|" +\
                to_string(q1_list_price) + "|" +\
                to_string(q1_list.anzahl) + "|" +\
                to_string(q1_list.warenwert) + "|" +\
                to_string(q1_list.depn_wert) + "|" +\
                to_string(q1_list.book_wert) + "|" +\
                to_string(q1_list.katnr) + "|" +\
                to_string(q1_list.bezeich) + "|" +\
                to_string(q1_list.location) + "|" +\
                to_string(q1_list_first_depn) + "|" +\
                to_string(q1_list_next_depn) + "|" +\
                to_string(q1_list_last_depn) + "|" +\
                to_string(q1_list.id) + "|" +\
                to_string(q1_list_created) + "|" +\
                to_string(q1_list.cid) + "|" +\
                to_string(q1_list_changed) + "|" +\
                to_string(q1_list_remark) + "|" +\
                to_string(q1_list.mathis_nr) + "|" +\
                to_string(q1_list.fname) + "|" +\
                to_string(q1_list_supplier) + "|" +\
                to_string(q1_list.posted) + "|" +\
                to_string(q1_list.fibukonto) + "|" +\
                to_string(q1_list.faartikel_nr) + "|" +\
                to_string(q1_list.credit_fibu) + "|" +\
                to_string(q1_list.debit_fibu) + "|" +\
                to_string(q1_list.recid_fa_artikel) + "|" +\
                to_string(q1_list.recid_mathis) + "|" +\
                to_string(q1_list.avail_glacct1) + "|" +\
                to_string(q1_list.avail_glacct2) + "|" +\
                to_string(q1_list.avail_glacct3) + "|" +\
                to_string(q1_list.subgroup) + "|" +\
                to_string(q1_list_model) + "|" +\
                to_string(q1_list.gnr) + "|" +\
                to_string(q1_list.flag) + "|" +\
                to_string(q1_list.grp_bez) + "|" +\
                to_string(q1_list.sgrp_bez) + "|" +\
                to_string(q1_list.rate) + "|" +\
                to_string(q1_list_mark) + "|" +\
                to_string(q1_list_spec) + "|" +\
                to_string(q1_list.anz_depn) + "|" +\
                to_string(q1_list.category) + "|" +\
                to_string(q1_list.lager_nr)
        queasy.number1 = counter


        q1_list_data.remove(q1_list)

        q1_list = query(q1_list_data, next=True)

    fibu_list = query(fibu_list_data, first=True)
    while None != fibu_list:

        if matches(fibu_list.bezeich,r"*|*"):
            fibu_list.bezeich = replace_str(fibu_list.bezeich, "|", " ")
        mark = "fibu"
        queasy = Queasy()
        db_session.add(queasy)

        counter = counter + 1
        queasy.key = 280
        queasy.char1 = "Fixed Asset List Report"
        queasy.char3 = idflag
        queasy.char2 = to_string(mark) + "|" +\
                to_string(fibu_list.flag) + "|" +\
                to_string(fibu_list.fibukonto) + "|" +\
                to_string(fibu_list.bezeich) + "|" +\
                to_string(fibu_list.credit) + "|" +\
                to_string(fibu_list.debit)
        queasy.number1 = counter


        fibu_list_data.remove(fibu_list)

        fibu_list = query(fibu_list_data, next=True)

    bqueasy = get_cache (Queasy, {"key": [(eq, 285)],"char1": [(eq, "fixed asset list report")],"char2": [(eq, idflag)]})

    if bqueasy:
        pass
        bqueasy.number1 = 0


        pass
        pass

    return generate_output()