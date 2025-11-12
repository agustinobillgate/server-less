#using conversion tools version: 1.0.0.117
"""_yusufwijasena_29/10/2025

    Ticket ID: 882DCF
        _remark_:   - fix python indentation
                    - fix var declaration
                    - add import from functions_py
                    - change string to str
"""
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Eg_queasy, Eg_staff, L_artikel

def eg_chgreq_create_history_webbl(reqno:int):

    prepare_cache ([Eg_queasy, Eg_staff, L_artikel])

    t_history_data = []
    stock_data = []
    attchment_data = []
    att_ctr:int = 0
    eg_queasy = eg_staff = l_artikel = None

    attchment = stock = t_history = qbuff = usr = None

    attchment_data, Attchment = create_model(
        "Attchment", {
            "nr":int, 
            "att_file":str, 
            "bezeich":str
            }
        )
    stock_data, Stock = create_model(
        "Stock", {
            "nr":int, 
            "stock_nr":int, 
            "stock_nm":str, 
            "stock_qty":Decimal, 
            "stock_price":int, 
            "stock_total":int
            }
        )
    t_history_data, T_history = create_model(
        "T_history", {
            "nr":int, 
            "fdate":date, 
            "stime":str, 
            "usrid":str, 
            "username":str
            }
        )

    Qbuff = create_buffer("Qbuff",Eg_queasy)
    Usr = create_buffer("Usr",Eg_staff)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_history_data, stock_data, attchment_data, att_ctr, eg_queasy, eg_staff, l_artikel
        nonlocal reqno
        nonlocal qbuff, usr
        nonlocal attchment, stock, t_history, qbuff, usr
        nonlocal attchment_data, stock_data, t_history_data

        return {
            "t-history": t_history_data, 
            "stock": stock_data, 
            "attchment": attchment_data
            }

    def create_stock():
        nonlocal t_history_data, stock_data, attchment_data, att_ctr, eg_queasy, eg_staff, l_artikel
        nonlocal reqno
        nonlocal qbuff, usr
        nonlocal attchment, stock, t_history, qbuff, usr
        nonlocal attchment_data, stock_data, t_history_data

        counter:int = 0
        qbuff = None
        Qbuff =  create_buffer("Qbuff",Eg_queasy)
        stock_data.clear()

        for qbuff in db_session.query(Qbuff).filter(
                (Qbuff.key == 1) & (Qbuff.reqnr == reqno)).order_by(Qbuff._recid).all():
            counter = counter + 1
            stock = Stock()
            stock_data.append(stock)

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
        nonlocal t_history_data, stock_data, attchment_data, att_ctr, eg_queasy, eg_staff, l_artikel
        nonlocal reqno
        nonlocal qbuff, usr
        nonlocal attchment, stock, t_history, qbuff, usr
        nonlocal attchment_data, stock_data, t_history_data

        qbuff = None
        Qbuff =  create_buffer("Qbuff",Eg_queasy)
        attchment_data.clear()

        for qbuff in db_session.query(Qbuff).filter(
                (Qbuff.key == 2) & (Qbuff.reqnr == reqno)).order_by(Qbuff._recid).all():
            att_ctr = att_ctr + 1
            attchment = Attchment()
            attchment_data.append(attchment)

            attchment.nr = att_ctr
            attchment.att_file = qbuff.ATTACHMENT
            attchment.bezeich = qbuff.att_desc

    t_history_data.clear()

    for qbuff in db_session.query(Qbuff).filter(
            (Qbuff.key == 3) & (Qbuff.reqnr == reqno) & (Qbuff.usr_nr != 0)).order_by(Qbuff._recid).all():

        usr = get_cache (Eg_staff, {"nr": [(eq, qbuff.usr_nr)]})

        if usr:
            t_history = T_history()
            t_history_data.append(t_history)

            t_history.nr = qbuff.hist_nr
            t_history.fdate = qbuff.hist_fdate
            t_history.stime = to_string(qbuff.hist_time, "HH:MM:SS")
            t_history.usrid = to_string(usr.nr)
            t_history.username = usr.name

        else:
            t_history = T_history()
            t_history_data.append(t_history)

            t_history.nr = qbuff.hist_nr
            t_history.fdate = qbuff.hist_fdate
            t_history.stime = to_string(qbuff.hist_time, "HH:MM:SS")
            t_history.usrid = to_string(qbuff.usr_nr)
            t_history.username = "PIC not found"

    create_stock()
    create_attchment()

    return generate_output()