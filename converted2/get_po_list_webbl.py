#using conversion tools version: 1.0.0.117
#-----------------------------------------
# Rd, 30/7/2025
# geser 'else' di: po_list_btn_go2_1cldbl
# pakai: check_ast.py
#-----------------------------------------

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.po_list_btn_go_1cldbl import po_list_btn_go_1cldbl
from functions.po_list_btn_go2_1cldbl import po_list_btn_go2_1cldbl
from models import L_order, Gl_acct, L_artikel

def get_po_list_webbl(usrname:string, po_number:string, last_doc_nr:string, app_sort:string, dml_only:bool, t_liefno:int, deptnr:int, all_supp:bool, stattype:int, sorttype:int, from_date:date, to_date:date, billdate:date, pr_only:bool, excl_dml_pr:bool):

    prepare_cache ([Gl_acct, L_artikel])

    p_267 = 0
    first_docu_nr = ""
    curr_docu_nr = ""
    last_docu_nr = ""
    q2_list_data = []
    param267:bool = False
    loeschflag:int = 0
    l_order = gl_acct = l_artikel = None

    q2_list = t_list = None

    q2_list_data, Q2_list = create_model("Q2_list", {"bestelldatum":date, "bezeich":string, "firma":string, "docu_nr":string, "l_orderhdr_lieferdatum":date, "wabkurz":string, "bestellart":string, "gedruckt":date, "l_orderhdr_besteller":string, "l_order_gedruckt":date, "zeit":int, "lief_fax_2":string, "l_order_lieferdatum":date, "lief_fax_3":string, "lieferdatum_eff":date, "lief_fax_1":string, "lief_nr":int, "username":string, "del_reason":string, "tot_amount":Decimal, "art_number":int, "art_desc":string, "content":Decimal, "order_qty":Decimal, "unit_price":Decimal, "gross_amount":Decimal, "deliv_unit":string, "nett_price":Decimal, "nett_amount":Decimal, "arrival_date":string, "s_unit":int, "d_unit":Decimal, "art_unit":string, "last_user":string, "account_number":string, "account_name":string, "remark":string, "flag_line":bool})
    t_list_data, T_list = create_model("T_list", {"bestelldatum":date, "bezeich":string, "firma":string, "docu_nr":string, "l_orderhdr_lieferdatum":date, "wabkurz":string, "bestellart":string, "gedruckt":date, "l_orderhdr_besteller":string, "l_order_gedruckt":date, "zeit":int, "lief_fax_2":string, "l_order_lieferdatum":date, "lief_fax_3":string, "lieferdatum_eff":date, "lief_fax_1":string, "lief_nr":int, "username":string, "del_reason":string, "tot_amount":Decimal})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal p_267, first_docu_nr, curr_docu_nr, last_docu_nr, q2_list_data, param267, loeschflag, l_order, gl_acct, l_artikel
        nonlocal usrname, po_number, last_doc_nr, app_sort, dml_only, t_liefno, deptnr, all_supp, stattype, sorttype, from_date, to_date, billdate, pr_only, excl_dml_pr


        nonlocal q2_list, t_list
        nonlocal q2_list_data, t_list_data

        return {"p_267": p_267, "first_docu_nr": first_docu_nr, "curr_docu_nr": curr_docu_nr, "last_docu_nr": last_docu_nr, "q2-list": q2_list_data}


    if usrname == None:
        usrname = ""

    if po_number == None:
        po_number = ""

    if dml_only == None:
        dml_only = False

    if t_liefno == None:
        t_liefno = 0

    if sorttype == None:
        sorttype = 1

    if deptnr == None:
        deptnr = -1

    if all_supp == None:
        all_supp = True

    if stattype == None:
        stattype = 0

    if usrname == None:
        usrname = ""

    if po_number != "":
        param267, t_list_data = get_output(po_list_btn_go_1cldbl(usrname, po_number, dml_only, pr_only, excl_dml_pr))
    else:
        first_docu_nr, curr_docu_nr, param267, last_docu_nr, t_list_data = get_output(po_list_btn_go2_1cldbl(t_liefno, last_doc_nr, sorttype, deptnr, all_supp, stattype, usrname, from_date, to_date, billdate, dml_only, app_sort, pr_only, excl_dml_pr))
    p_267 = to_int(param267)

    if stattype == 0 or stattype == 2:
        loeschflag = 0

    elif stattype == 1:
        loeschflag = 1

    elif stattype == 3:
        loeschflag = 2

    for t_list in query(t_list_data, sort_by=[("docu_nr",False)]):
        q2_list = Q2_list()
        q2_list_data.append(q2_list)

        buffer_copy(t_list, q2_list)

        l_order = get_cache (L_order, {"docu_nr": [(eq, t_list.docu_nr)],"loeschflag": [(eq, loeschflag)],"pos": [(gt, 0)]})
        while None != l_order:
            q2_list = Q2_list()
            q2_list_data.append(q2_list)

            q2_list.flag_line = True
            q2_list.docu_nr = l_order.docu_nr
            q2_list.art_number = l_order.artnr
            q2_list.order_qty =  to_decimal(l_order.anzahl)
            q2_list.nett_price =  to_decimal(l_order.einzelpreis)
            q2_list.nett_amount =  to_decimal(l_order.warenwert)
            q2_list.account_number = l_order.stornogrund
            q2_list.remark = l_order.besteller
            q2_list.deliv_unit = l_order.lief_fax[2]
            q2_list.d_unit =  to_decimal(l_order.geliefert)
            q2_list.s_unit = l_order.angebot_lief[0]
            q2_list.last_user = l_order.lief_fax[1]

            if l_order.lieferdatum_eff != None:
                q2_list.arrival_date = to_string(l_order.lieferdatum_eff)
            else:
                q2_list.arrival_date = ""

            gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, l_order.stornogrund)]})

            if gl_acct:
                q2_list.account_name = gl_acct.bezeich

            l_artikel = get_cache (L_artikel, {"artnr": [(eq, l_order.artnr)]})

            if l_artikel:
                q2_list.art_desc = l_artikel.bezeich
                q2_list.content =  to_decimal(l_artikel.lief_einheit)
                q2_list.art_unit = l_artikel.masseinheit

            curr_recid = l_order._recid
            l_order = db_session.query(L_order).filter(
                     (L_order.docu_nr == t_list.docu_nr) & (L_order.loeschflag == loeschflag) & (L_order.pos > 0) & (L_order._recid > curr_recid)).first()

    return generate_output()