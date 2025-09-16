#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.stock_outlist_btn_go_cldbl import stock_outlist_btn_go_cldbl

import re

def stock_outlist_btn_go1bl(trans_code:string, from_grp:int, mi_alloc:bool, mi_article:bool, mi_docu:bool, mi_date:bool, mattype:int, from_lager:int, to_lager:int, from_date:date, to_date:date, from_art:int, to_art:int, show_price:bool, cost_acct:string, deptno:int):
    it_exist = False
    tot_anz = to_decimal("0.0")
    tot_amount = to_decimal("0.0")
    stock_outlist_data = []

    str_list = stock_outlist = None

    str_list_data, Str_list = create_model("Str_list", {"billdate":date, "fibu":string, "other_fibu":bool, "op_recid":int, "lscheinnr":string, "s":string, "id":string, "masseinheit":string, "gldept":string, "amount":Decimal, "avrg_price":Decimal, "remark_artikel":string, "bezeich":string})
    stock_outlist_data, Stock_outlist = create_model("Stock_outlist", {"datum":date, "lager":string, "lscheinnr":string, "docu_nr":string, "art_nr":int, "art_bez":string, "out_qty":Decimal, "avrg_price":Decimal, "amount":Decimal, "id":string, "billdate":date, "fibu":string, "other_fibu":bool, "op_recid":int, "strpanjang":string, "masseinheit":string, "gldept":string, "remark_artikel":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal it_exist, tot_anz, tot_amount, stock_outlist_data
        nonlocal trans_code, from_grp, mi_alloc, mi_article, mi_docu, mi_date, mattype, from_lager, to_lager, from_date, to_date, from_art, to_art, show_price, cost_acct, deptno


        nonlocal str_list, stock_outlist
        nonlocal str_list_data, stock_outlist_data

        return {"it_exist": it_exist, "tot_anz": tot_anz, "tot_amount": tot_amount, "stock-outlist": stock_outlist_data}

    it_exist, tot_anz, tot_amount, str_list_data = get_output(stock_outlist_btn_go_cldbl(trans_code, from_grp, mi_alloc, mi_article, mi_docu, mi_date, mattype, from_lager, to_lager, from_date, to_date, from_art, to_art, show_price, cost_acct, deptno))
    stock_outlist_data.clear()

    for str_list in query(str_list_data):
        stock_outlist = Stock_outlist()
        stock_outlist_data.append(stock_outlist)

        stock_outlist.datum = date_mdy(substring(str_list.s, 0, 8))
        stock_outlist.lager = str_list.bezeich
        stock_outlist.docu_nr = substring(str_list.s, 109, 12)
        stock_outlist.art_nr = to_int(substring(str_list.s, 38, 7))
        stock_outlist.art_bez = substring(str_list.s, 45, 50)
        stock_outlist.out_qty = to_decimal(substring(str_list.s, 95, 14))
        stock_outlist.avrg_price =  to_decimal(str_list.avrg_price)
        stock_outlist.amount =  to_decimal(str_list.amount)
        stock_outlist.id = str_list.id
        stock_outlist.billdate = str_list.billdate
        stock_outlist.fibu = str_list.fibu
        stock_outlist.other_fibu = str_list.other_fibu
        stock_outlist.op_recid = str_list.op_recid
        stock_outlist.strpanjang = str_list.s
        stock_outlist.masseinheit = str_list.masseinheit
        stock_outlist.gldept = str_list.gldept
        stock_outlist.remark_artikel = str_list.remark_artikel

        if re.search(r".Subtotal.", stock_outlist.strpanjang):
            stock_outlist.docu_nr = ""
        if re.search(r".T O T A L.", stock_outlist.strpanjang):
            stock_outlist.docu_nr = ""

    return generate_output()