from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import L_order, L_quote, L_lieferant

def prepare_chg_pr_enter_suppbl(s_list:[S_list], docu_nr:str, flag_oe:int, artno:int, lieferdatum:date):
    pr_no = ""
    mainno = 0
    mainsupp = ""
    mainprice = 0
    maincurr = ""
    qsupp_list_list = []
    rsupp_list_list = []
    supp_list_list = []
    t_buff_order_list = []
    l_order = l_quote = l_lieferant = None

    s_list = supp_list = qsupp_list = rsupp_list = t_buff_order = b_order = buff_order = None

    s_list_list, S_list = create_model_like(L_order, {"curr":str, "exrate":decimal, "s_recid":int, "amount":decimal, "supp1":int, "supp2":int, "supp3":int, "suppn1":str, "suppn2":str, "suppn3":str, "supps":str, "du_price1":decimal, "du_price2":decimal, "du_price3":decimal, "curr1":str, "curr2":str, "curr3":str, "fdate1":date, "fdate2":date, "fdate3":date, "tdate1":date, "tdate2":date, "tdate3":date, "desc_coa":str, "last_pprice":decimal, "avg_pprice":decimal, "lprice":decimal, "lief_fax2":str, "ek_letzter":decimal, "lief_einheit":int, "supplier":str, "lief_fax_2":str, "vk_preis":decimal, "soh":decimal, "last_pdate":date, "a_firma":str, "last_pbook":decimal, "avg_cons":decimal})
    supp_list_list, Supp_list = create_model("Supp_list", {"sno":int, "sname":str, "sprice":decimal, "scurr":str, "fdate":date, "tdate":date, "flag":int, "sr":int})
    qsupp_list_list, Qsupp_list = create_model_like(Supp_list)
    rsupp_list_list, Rsupp_list = create_model_like(Supp_list)
    t_buff_order_list, T_buff_order = create_model_like(L_order)

    B_order = L_order
    Buff_order = L_order

    db_session = local_storage.db_session

    def generate_output():
        nonlocal pr_no, mainno, mainsupp, mainprice, maincurr, qsupp_list_list, rsupp_list_list, supp_list_list, t_buff_order_list, l_order, l_quote, l_lieferant
        nonlocal b_order, buff_order


        nonlocal s_list, supp_list, qsupp_list, rsupp_list, t_buff_order, b_order, buff_order
        nonlocal s_list_list, supp_list_list, qsupp_list_list, rsupp_list_list, t_buff_order_list
        return {"pr_no": pr_no, "mainno": mainno, "mainsupp": mainsupp, "mainprice": mainprice, "maincurr": maincurr, "qsupp-list": qsupp_list_list, "rsupp-list": rsupp_list_list, "supp-list": supp_list_list, "t-buff-order": t_buff_order_list}


    supp_list_list.clear()
    qsupp_list_list.clear()
    rsupp_list_list.clear()

    if flag_oe == 1:

        for l_quote in db_session.query(L_quote).filter(
                (L_quote.artnr == artno) &  (L_quote.from_date <= lieferdatum) &  (L_quote.to_date >= lieferdatum)).all():

            l_lieferant = db_session.query(L_lieferant).filter(
                    (L_lieferant.lief_nr == l_quote.lief_nr)).first()

            if l_lieferant:
                qsupp_list = Qsupp_list()
                qsupp_list_list.append(qsupp_list)

                qsupp_list.scurr = l_quote.reserve_char[0]
                qsupp_list.sno = l_quote.lief_nr
                qsupp_list.sname = l_lieferant.firma
                qsupp_list.sprice = l_quote.unitprice
                qsupp_list.fdate = l_quote.from_date
                qsupp_list.tdate = l_quote.to_date
                qsupp_list.flag = 0

        for l_quote in db_session.query(L_quote).filter(
                (L_quote.artnr == artno) &  (L_quote.lieferdatum > L_quote.to_date) &  ((lieferdatum - L_quote.to_date) <= 30)).all():

            l_lieferant = db_session.query(L_lieferant).filter(
                    (L_lieferant.lief_nr == l_quote.lief_nr)).first()

            if l_lieferant:
                qsupp_list = Qsupp_list()
                qsupp_list_list.append(qsupp_list)

                qsupp_list.scurr = l_quote.reserve_char[0]
                qsupp_list.sno = l_quote.lief_nr
                qsupp_list.sname = l_lieferant.firma
                qsupp_list.sprice = l_quote.unitprice
                qsupp_list.fdate = l_quote.from_date
                qsupp_list.tdate = l_quote.to_date
                qsupp_list.flag = 1

    b_order = db_session.query(B_order).filter(
            (B_order.artnr == artno) &  (B_order.lief_nr == 0) &  (func.lower(B_order.(docu_nr).lower()) == (docu_nr).lower())).first()

    if b_order:

        b_order = db_session.query(B_order).filter(
                (B_order.artnr == artno) &  (B_order.lief_nr == 0) &  (B_order.bestellart != "") &  (B_order.bestellart != None)).first()

        if b_order:
            pr_no = b_order.docu_nr

            if to_int(entry(1, entry(0, b_order.bestellart, "-") , ";")) != 0:

                l_lieferant = db_session.query(L_lieferant).filter(
                        (L_lieferant.lief_nr == to_int(entry(0, entry(0, b_order.bestellart, "-") , ";")))).first()

                if l_lieferant:
                    rsupp_list = Rsupp_list()
                    rsupp_list_list.append(rsupp_list)

                    rsupp_list.scurr = entry(2, entry(0, b_order.bestellart, "-") , ";")
                    rsupp_list.sno = to_int(entry(0, entry(0, b_order.bestellart, "-") , ";"))
                    rsupp_list.sname = l_lieferant.firma
                    rsupp_list.sprice = to_int(entry(1, entry(0, b_order.bestellart, "-") , ";")) / 100
                    rsupp_list.fdate = date_mdy(entry(3, entry(0, b_order.bestellart, "-") , ";"))
                    rsupp_list.tdate = date_mdy(entry(4, entry(0, b_order.bestellart, "-") , ";"))

                    if rsupp_list.tdate < lieferdatum:
                        rsupp_list.flag = 1
                    else:
                        rsupp_list.flag = 0

            if to_int(entry(1, entry(1, b_order.bestellart, "-") , ";")) != 0:

                l_lieferant = db_session.query(L_lieferant).filter(
                        (L_lieferant.lief_nr == to_int(entry(0, entry(1, b_order.bestellart, "-") , ";")))).first()

                if l_lieferant:
                    rsupp_list = Rsupp_list()
                    rsupp_list_list.append(rsupp_list)

                    rsupp_list.scurr = entry(2, entry(1, b_order.bestellart, "-") , ";")
                    rsupp_list.sno = to_int(entry(0, entry(1, b_order.bestellart, "-") , ";"))
                    rsupp_list.sname = l_lieferant.firma
                    rsupp_list.sprice = to_int(entry(1, entry(1, b_order.bestellart, "-") , ";")) / 100
                    rsupp_list.fdate = date_mdy(entry(3, entry(1, b_order.bestellart, "-") , ";"))
                    rsupp_list.tdate = date_mdy(entry(4, entry(1, b_order.bestellart, "-") , ";"))

                    if rsupp_list.tdate < lieferdatum:
                        rsupp_list.flag = 1
                    else:
                        rsupp_list.flag = 0

            if to_int(entry(1, entry(2, b_order.bestellart, "-") , ";")) != 0:

                l_lieferant = db_session.query(L_lieferant).filter(
                        (L_lieferant.lief_nr == to_int(entry(0, entry(2, b_order.bestellart, "-") , ";")))).first()

                if l_lieferant:
                    rsupp_list = Rsupp_list()
                    rsupp_list_list.append(rsupp_list)

                    rsupp_list.scurr = entry(2, entry(2, b_order.bestellart, "-") , ";")
                    rsupp_list.sno = to_int(entry(0, entry(2, b_order.bestellart, "-") , ";"))
                    rsupp_list.sname = l_lieferant.firma
                    rsupp_list.sprice = to_int(entry(1, entry(2, b_order.bestellart, "-") , ";")) / 100
                    rsupp_list.fdate = date_mdy(entry(3, entry(2, b_order.bestellart, "-") , ";"))
                    rsupp_list.tdate = date_mdy(entry(4, entry(2, b_order.bestellart, "-") , ";"))

                    if rsupp_list.tdate < lieferdatum:
                        rsupp_list.flag = 1
                    else:
                        rsupp_list.flag = 0

    s_list = query(s_list_list, filters=(lambda s_list :s_list.artnr == artno), first=True)

    if s_list:

        if s_list.du_price1 != 0:

            l_lieferant = db_session.query(L_lieferant).filter(
                    (L_lieferant.lief_nr == s_list.supp1)).first()

            if l_lieferant:
                supp_list = Supp_list()
                supp_list_list.append(supp_list)

                supp_list.scurr = s_list.curr1
                supp_list.sno = s_list.supp1
                supp_list.sname = l_lieferant.firma
                supp_list.sprice = s_list.du_price1
                supp_list.fdate = s_list.fdate1
                supp_list.tdate = s_list.tdate1

                if supp_list.tdate < lieferdatum:
                    supp_list.flag = 1
                else:
                    supp_list.flag = 0

        if s_list.du_price2 != 0:

            l_lieferant = db_session.query(L_lieferant).filter(
                    (L_lieferant.lief_nr == s_list.supp2)).first()

            if l_lieferant:
                supp_list = Supp_list()
                supp_list_list.append(supp_list)

                supp_list.sno = s_list.supp2
                supp_list.sname = l_lieferant.firma
                supp_list.sprice = s_list.du_price2
                supp_list.scurr = s_list.curr2
                supp_list.fdate = s_list.fdate2
                supp_list.tdate = s_list.tdate2

                if supp_list.tdate < lieferdatum:
                    supp_list.flag = 1
                else:
                    supp_list.flag = 0

        if s_list.du_price3 != 0:

            l_lieferant = db_session.query(L_lieferant).filter(
                    (L_lieferant.lief_nr == s_list.supp3)).first()

            if l_lieferant:
                supp_list = Supp_list()
                supp_list_list.append(supp_list)

                supp_list.sno = s_list.supp3
                supp_list.sname = l_lieferant.firma
                supp_list.sprice = s_list.du_price3
                supp_list.scurr = s_list.curr3
                supp_list.fdate = s_list.fdate3
                supp_list.tdate = s_list.tdate3

                if supp_list.tdate < lieferdatum:
                    supp_list.flag = 1
                else:
                    supp_list.flag = 0

    for rsupp_list in query(rsupp_list_list):

        qsupp_list = query(qsupp_list_list, filters=(lambda qsupp_list :qsupp_list.sno == rsupp_list.sno and qsupp_list.sprice == rsupp_list.sprice and qsupp_list.flag == rsupp_list.flag), first=True)

        if qsupp_list:
            qsupp_list_list.remove(qsupp_list)

    for supp_list in query(supp_list_list):

        qsupp_list = query(qsupp_list_list, filters=(lambda qsupp_list :qsupp_list.sno == supp_list.sno and qsupp_list.sprice == supp_list.sprice and qsupp_list.flag == supp_list.flag), first=True)

        if qsupp_list:
            qsupp_list_list.remove(qsupp_list)

    for supp_list in query(supp_list_list):

        rsupp_list = query(rsupp_list_list, filters=(lambda rsupp_list :rsupp_list.sno == supp_list.sno and rsupp_list.sprice == supp_list.sprice and rsupp_list.flag == supp_list.flag), first=True)

        if rsupp_list:
            rsupp_list_list.remove(rsupp_list)

    l_lieferant = db_session.query(L_lieferant).filter(
            (L_lieferant.lief_nr == s_list.angebot_lief[1])).first()

    if l_lieferant:
        mainno = s_list.angebot_lief[1]
        mainsupp = l_lieferant.firma
        mainprice = s_list.einzelpreis
        maincurr = s_list.curr

    buff_order = db_session.query(Buff_order).filter(
            (Buff_order.docu_nr == pr_no) &  (Buff_order.artnr == artno)).first()

    if buff_order:
        t_buff_order = T_buff_order()
        t_buff_order_list.append(t_buff_order)

        buffer_copy(buff_order, t_buff_order)

    return generate_output()