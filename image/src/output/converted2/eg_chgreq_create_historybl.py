#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Eg_queasy, Eg_staff, History, L_artikel

def eg_chgreq_create_historybl(reqno:int):

    prepare_cache ([Eg_queasy, Eg_staff, History, L_artikel])

    history_list = []
    stock_list = []
    attchment_list = []
    att_ctr:int = 0
    eg_queasy = eg_staff = history = l_artikel = None

    attchment = stock = history = qbuff = usr = None

    attchment_list, Attchment = create_model("Attchment", {"nr":int, "att_file":string, "bezeich":string})
    stock_list, Stock = create_model("Stock", {"nr":int, "stock_nr":int, "stock_nm":string, "stock_qty":Decimal, "stock_price":int, "stock_total":int})
    history_list, History = create_model("History", {"nr":int, "fdate":date, "stime":string, "usrid":string, "username":string})

    Qbuff = create_buffer("Qbuff",Eg_queasy)
    Usr = create_buffer("Usr",Eg_staff)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal history_list, stock_list, attchment_list, att_ctr, eg_queasy, eg_staff, history, l_artikel
        nonlocal reqno
        nonlocal qbuff, usr


        nonlocal attchment, stock, history, qbuff, usr
        nonlocal attchment_list, stock_list, history_list

        return {"history": history_list, "stock": stock_list, "attchment": attchment_list}

    def create_stock():

        nonlocal history_list, stock_list, attchment_list, att_ctr, eg_queasy, eg_staff, history, l_artikel
        nonlocal reqno
        nonlocal qbuff, usr


        nonlocal attchment, stock, history, qbuff, usr
        nonlocal attchment_list, stock_list, history_list

        counter:int = 0
        qbuff = None
        Qbuff =  create_buffer("Qbuff",Eg_queasy)
        stock_list.clear()

        for qbuff in db_session.query(Qbuff).filter(
                 (Qbuff.key == 1) & (Qbuff.reqnr == reqno)).order_by(Qbuff._recid).all():
            counter = counter + 1
            stock = Stock()
            stock_list.append(stock)

            stock.nr = counter
            stock.stock_nr = qbuff.stock_nr
            stock.stock_qty =  to_decimal(qbuff.deci1)
            stock.stock_price = qbuff.price
            stock.stock_total = qbuff.deci1 * qbuff.price

            l_artikel = get_cache (L_artikel, {"artnr": [(eq, stock.stock_nr)]})

            if l_artikel:
                stock.stock_nm = l_artikel.bezeich
            else:
                stock.stock_nm = "Unknown"


    def create_attchment():

        nonlocal history_list, stock_list, attchment_list, att_ctr, eg_queasy, eg_staff, history, l_artikel
        nonlocal reqno
        nonlocal qbuff, usr


        nonlocal attchment, stock, history, qbuff, usr
        nonlocal attchment_list, stock_list, history_list

        qbuff = None
        Qbuff =  create_buffer("Qbuff",Eg_queasy)
        attchment_list.clear()

        for qbuff in db_session.query(Qbuff).filter(
                 (Qbuff.key == 2) & (Qbuff.reqnr == reqno)).order_by(Qbuff._recid).all():
            att_ctr = att_ctr + 1
            attchment = Attchment()
            attchment_list.append(attchment)

            attchment.nr = att_ctr
            attchment.att_file = qbuff.ATTACHMENT
            attchment.bezeich = qbuff.att_desc

    history_list.clear()

    for qbuff in db_session.query(Qbuff).filter(
             (Qbuff.key == 3) & (Qbuff.reqnr == reqno) & (Qbuff.usr_nr != 0)).order_by(Qbuff._recid).all():

        usr = get_cache (Eg_staff, {"nr": [(eq, qbuff.usr_nr)]})

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