from functions.additional_functions import *
import decimal
from models import History, Blinehis, Bill_line

def view_history3bl(rechnr:int, t_history:[T_history]):
    bline_list_list = []
    history = blinehis = bill_line = None

    t_history = bline_list = None

    t_history_list, T_history = create_model_like(History)
    bline_list_list, Bline_list = create_model_like(Blinehis, {"transflag":bool})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal bline_list_list, history, blinehis, bill_line


        nonlocal t_history, bline_list
        nonlocal t_history_list, bline_list_list
        return {"bline-list": bline_list_list}


    t_history = query(t_history_list, first=True)

    for bill_line in db_session.query(Bill_line).filter(
            (Bill_line.rechnr == rechnr)).all():
        bline_list = Bline_list()
        bline_list_list.append(bline_list)

        buffer_copy(bill_line, bline_list)

    for bill_line in db_session.query(Bill_line).filter(
            (Bill_line.rechnr != rechnr) &  (Bill_line.bill_datum >= t_history.ankunft) &  (Bill_line.bill_datum <= t_history.abreise) &  (Bill_line.massnr == t_history.resnr) &  (Bill_line.billin_nr == t_history.reslinnr)).all():
        bline_list = Bline_list()
        bline_list_list.append(bline_list)

        buffer_copy(bill_line, bline_list)
        bline_list.transflag = True

    if not bline_list:

        for blinehis in db_session.query(Blinehis).filter(
                (Blinehis.rechnr == rechnr)).all():
            bline_list = Bline_list()
            bline_list_list.append(bline_list)

            buffer_copy(blinehis, bline_list)


    return generate_output()