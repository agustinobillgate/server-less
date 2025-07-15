#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import History, Blinehis, Bill_line

t_history_data, T_history = create_model_like(History)

def view_history3bl(rechnr:int, t_history_data:[T_history]):
    bline_list_data = []
    history = blinehis = bill_line = None

    t_history = bline_list = None

    bline_list_data, Bline_list = create_model_like(Blinehis, {"transflag":bool})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal bline_list_data, history, blinehis, bill_line
        nonlocal rechnr


        nonlocal t_history, bline_list
        nonlocal bline_list_data

        return {"bline-list": bline_list_data}


    t_history = query(t_history_data, first=True)

    for bill_line in db_session.query(Bill_line).filter(
             (Bill_line.rechnr == rechnr)).order_by(Bill_line.sysdate.desc(), Bill_line.zeit.desc()).all():
        bline_list = Bline_list()
        bline_list_data.append(bline_list)

        buffer_copy(bill_line, bline_list)

    for bill_line in db_session.query(Bill_line).filter(
             (Bill_line.rechnr != rechnr) & (Bill_line.bill_datum >= t_history.ankunft) & (Bill_line.bill_datum <= t_history.abreise) & (Bill_line.massnr == t_history.resnr) & (Bill_line.billin_nr == t_history.reslinnr)).order_by(Bill_line._recid).all():
        bline_list = Bline_list()
        bline_list_data.append(bline_list)

        buffer_copy(bill_line, bline_list)
        bline_list.transflag = True

    if not bline_list:

        for blinehis in db_session.query(Blinehis).filter(
                 (Blinehis.rechnr == rechnr)).order_by(Blinehis.sysdate.desc(), Blinehis.zeit.desc()).all():
            bline_list = Bline_list()
            bline_list_data.append(bline_list)

            buffer_copy(blinehis, bline_list)


    return generate_output()