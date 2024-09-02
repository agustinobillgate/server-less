from functions.additional_functions import *
import decimal
from datetime import date
from models import L_artikel, Eg_request, Eg_subtask, Eg_queasy, Eg_vperform

def eg_rephistoryprop_disp_webbl(prop_nr:int, fdate:date, tdate:date):
    grand_total = ""
    tbrowse_list = []
    atotal:int = 0
    btotal:decimal = 0
    tot:decimal = 0
    int_str:[str] = ["", "", "", "", "", ""]
    l_artikel = eg_request = eg_subtask = eg_queasy = eg_vperform = None

    tbrowse = tbuff = None

    tbrowse_list, Tbrowse = create_model("Tbrowse", {"reqno":str, "opend":str, "processd":str, "doned":str, "subtask":str, "reqstat":str, "tflag":str})

    Tbuff = L_artikel

    db_session = local_storage.db_session

    def generate_output():
        nonlocal grand_total, tbrowse_list, atotal, btotal, tot, int_str, l_artikel, eg_request, eg_subtask, eg_queasy, eg_vperform
        nonlocal tbuff


        nonlocal tbrowse, tbuff
        nonlocal tbrowse_list
        return {"grand_total": grand_total, "tbrowse": tbrowse_list}

    def create_history():

        nonlocal grand_total, tbrowse_list, atotal, btotal, tot, int_str, l_artikel, eg_request, eg_subtask, eg_queasy, eg_vperform
        nonlocal tbuff


        nonlocal tbrowse, tbuff
        nonlocal tbrowse_list

        char1:str = ""
        str_op:str = ""
        str_cd:str = ""
        str_dd:str = ""
        itotal:decimal = 0
        tbrowse_list.clear()
        atotal = 0
        btotal = 0

        for eg_request in db_session.query(Eg_request).filter(
                ((Eg_request.propertynr == prop_nr) &  (Eg_request.opened_date >= fdate) &  (Eg_request.opened_date <= tdate)) |  ((Eg_request.propertynr == prop_nr) &  (Eg_request.closed_date >= fdate) &  (Eg_request.closed_date <= tdate)) |  ((Eg_request.propertynr == prop_nr) &  (Eg_request.process_date >= fdate) &  (Eg_request.process_date <= tdate))).all():

            if eg_request.opened_date == None:
                str_op = "-"
            else:
                str_op = to_string(eg_request.opened_date , "99/99/99")

            if eg_request.closed_date == None:
                str_cd = "-"
            else:
                str_cd = to_string(eg_request.closed_date , "99/99/99")

            if eg_request.done_date == None:
                str_dd = "-"
            else:
                str_dd = to_string(eg_request.done_date , "99/99/99")

            eg_subtask = db_session.query(Eg_subtask).filter(
                    (Eg_subtask.sub_CODE == eg_request.sub_task)).first()

            if eg_subtask:
                char1 = eg_subtask.bezeich
            else:
                char1 = ""
            tbrowse = Tbrowse()
            tbrowse_list.append(tbrowse)

            tbrowse.tflag = "1"
            tbrowse.reqno = to_string(eg_request.reqnr , "->>>>>>>>9")
            tbrowse.opend = str_op
            tbrowse.processd = str_cd
            tbrowse.doned = str_dd
            tbrowse.subtask = char1
            tbrowse.reqstat = to_string(int_str[eg_request.reqstatus - 1])

            eg_queasy = db_session.query(Eg_queasy).filter(
                    (Eg_queasy.key == 1) &  (Eg_queasy.reqnr == eg_request.reqnr)).first()

            if eg_queasy:

                for eg_queasy in db_session.query(Eg_queasy).filter(
                        (Eg_queasy.key == 1) &  (Eg_queasy.reqnr == eg_request.reqnr)).all():

                    tbuff = db_session.query(Tbuff).filter(
                            (Tbuff.artnr == eg_queasy.stock_nr)).first()

                    if tbuff:
                        itotal = eg_queasy.deci1 * eg_queasy.price
                    tot = tot + itotal

            eg_vperform = db_session.query(Eg_vperform).filter(
                    (Eg_vperform.reqnr == eg_request.reqnr)).first()

            if eg_vperform:

                for eg_vperform in db_session.query(Eg_vperform).filter(
                        (Eg_vperform.reqnr == eg_request.reqnr)).all():
                    tot = tot + eg_vperform.price

            if tot != 0:
                btotal = btotal + tot
                tot = 0

        if btotal != 0:
            grand_total = to_string(btotal, "->>>,>>>,>>>,>>9.99")


    create_history()

    return generate_output()