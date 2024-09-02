from functions.additional_functions import *
import decimal
from datetime import date
from functions.stock_outlist_btn_gobl import stock_outlist_btn_gobl

def stock_outlist_btn_go1bl(trans_code:str, from_grp:int, mi_alloc:bool, mi_article:bool, mi_docu:bool, mi_date:bool, mattype:int, from_lager:int, to_lager:int, from_date:date, to_date:date, from_art:int, to_art:int, show_price:bool, cost_acct:str, deptno:int):
    it_exist = False
    tot_anz = 0
    tot_amount = 0
    stock_outlist_list = []

    str_list = stock_outlist = None

    str_list_list, Str_list = create_model("Str_list", {"billdate":date, "fibu":str, "other_fibu":bool, "op_recid":int, "lscheinnr":str, "s":str, "id":str})
    stock_outlist_list, Stock_outlist = create_model("Stock_outlist", {"datum":date, "lager":str, "lscheinnr":str, "docu_nr":str, "art_nr":int, "art_bez":str, "out_qty":decimal, "avrg_price":decimal, "amount":decimal, "id":str, "billdate":date, "fibu":str, "other_fibu":bool, "op_recid":int, "strpanjang":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal it_exist, tot_anz, tot_amount, stock_outlist_list


        nonlocal str_list, stock_outlist
        nonlocal str_list_list, stock_outlist_list
        return {"it_exist": it_exist, "tot_anz": tot_anz, "tot_amount": tot_amount, "stock-outlist": stock_outlist_list}

    it_exist, tot_anz, tot_amount, str_list_list = get_output(stock_outlist_btn_gobl(trans_code, from_grp, mi_alloc, mi_article, mi_docu, mi_date, mattype, from_lager, to_lager, from_date, to_date, from_art, to_art, show_price, cost_acct, deptno))
    stock_outlist_list.clear()

    for str_list in query(str_list_list):
        stock_outlist = Stock_outlist()
        stock_outlist_list.append(stock_outlist)

        stock_outlist.datum = date_mdy(substring(str_list.s, 0, 8))
        stock_outlist.lager = substring(str_list.s, 8, 30)
        stock_outlist.docu_nr = substring(str_list.s, 140, 12)
        stock_outlist.art_nr = to_int(substring(str_list.s, 38, 7))
        stock_outlist.art_bez = substring(str_list.s, 45, 50)
        stock_outlist.out_qty = decimal.Decimal(substring(str_list.s, 93, 14))
        stock_outlist.avrg_price = decimal.Decimal(substring(str_list.s, 109, 14))
        stock_outlist.amount = decimal.Decimal(substring(str_list.s, 123, 17))
        stock_outlist.id = str_list.id
        stock_outlist.billdate = str_list.billdate
        stock_outlist.fibu = str_list.fibu
        stock_outlist.other_fibu = str_list.other_fibu
        stock_outlist.op_recid = str_list.op_recid
        stock_outlist.strPanjang = str_list.s

    return generate_output()