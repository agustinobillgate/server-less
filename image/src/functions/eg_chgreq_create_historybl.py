from functions.additional_functions import *
import decimal
from datetime import date
from models import Eg_queasy, Eg_staff, History, L_artikel

def eg_chgreq_create_historybl(reqno:int):
    history_list = []
    stock_list = []
    attchment_list = []
    att_ctr:int = 0
    eg_queasy = eg_staff = history = l_artikel = None

    attchment = stock = history = qbuff = usr = None

    attchment_list, Attchment = create_model("Attchment", {"nr":int, "att_file":str, "bezeich":str})
    stock_list, Stock = create_model("Stock", {"nr":int, "stock_nr":int, "stock_nm":str, "stock_qty":decimal, "stock_price":int, "stock_total":int})
    history_list, History = create_model("History", {"nr":int, "fdate":date, "stime":str, "usrid":str, "username":str})

    Qbuff = Eg_queasy
    Usr = Eg_staff

    db_session = local_storage.db_session

    def generate_output():
        nonlocal history_list, stock_list, attchment_list, att_ctr, eg_queasy, eg_staff, history, l_artikel
        nonlocal qbuff, usr


        nonlocal attchment, stock, history, qbuff, usr
        nonlocal attchment_list, stock_list, history_list
        return {"history": history_list, "stock": stock_list, "attchment": attchment_list}

    def create_stock():

        nonlocal history_list, stock_list, attchment_list, att_ctr, eg_queasy, eg_staff, history, l_artikel
        nonlocal qbuff, usr


        nonlocal attchment, stock, history, qbuff, usr
        nonlocal attchment_list, stock_list, history_list

        counter:int = 0
        Qbuff = Eg_queasy
        stock_list.clear()

        for qbuff in db_session.query(Qbuff).filter(
                (Qbuff.key == 1) &  (Qbuff.reqnr == reqno)).all():
            counter = counter + 1
            stock = Stock()
            stock_list.append(stock)

            stock.nr = counter
            stock.stock_nr = qbuff.stock_nr
            stock.stock_qty = qbuff.deci1
            stock.stock_price = qbuff.price
            stock.stock_total = qbuff.deci1 * qbuff.price

            l_artikel = db_session.query(L_artikel).filter(
                    (L_artikel.artnr == stock.stock_nr)).first()

            if l_artikel:
                stock.stock_nm = l_artikel.bezeich
            else:
                stock.stock_nm = "Unknown"

    def create_attchment():

        nonlocal history_list, stock_list, attchment_list, att_ctr, eg_queasy, eg_staff, history, l_artikel
        nonlocal qbuff, usr


        nonlocal attchment, stock, history, qbuff, usr
        nonlocal attchment_list, stock_list, history_list


        Qbuff = Eg_queasy
        attchment_list.clear()

        for qbuff in db_session.query(Qbuff).filter(
                (Qbuff.key == 2) &  (Qbuff.reqnr == reqno)).all():
            att_ctr = att_ctr + 1
            attchment = Attchment()
            attchment_list.append(attchment)

            attchment.nr = att_ctr
            attchment.att_file = qbuff.ATTACHMENT
            attchment.bezeich = qbuff.att_desc


    history_list.clear()

    for qbuff in db_session.query(Qbuff).filter(
            (Qbuff.key == 3) &  (Qbuff.reqnr == reqno) &  (Qbuff.usr_nr != 0)).all():

        usr = db_session.query(Usr).filter(
                (Usr.nr == qbuff.usr_nr)).first()

        if usr:
            history = History()
            db_session.add(history)

            history.nr = qbuff.hist_nr
            history.fdate = qbuff.hist_fdate
            history.stime = to_string(qbuff.hist_time, "HH:MM:SS")
            history.usrid = to_string(usr.nr)
            history.username = usr.name


        else:
            history = History()
            db_session.add(history)

            history.nr = qbuff.hist_nr
            history.fdate = qbuff.hist_fdate
            history.stime = to_string(qbuff.hist_time, "HH:MM:SS")
            history.usrid = to_string(qbuff.usr_nr)
            history.username = "PIC not found"


    create_stock()
    create_attchment()

    return generate_output()