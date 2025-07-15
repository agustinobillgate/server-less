#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import L_artikel, Eg_request, Eg_subtask, Eg_queasy, Eg_vperform

def eg_rephistoryprop_disp_webbl(prop_nr:int, fdate:date, tdate:date):

    prepare_cache ([Eg_request, Eg_subtask, Eg_queasy, Eg_vperform])

    grand_total = ""
    tbrowse_data = []
    atotal:int = 0
    btotal:Decimal = to_decimal("0.0")
    tot:Decimal = to_decimal("0.0")
    int_str:List[string] = ["New", "Processed", "Done", "Postponed", "Closed"]
    l_artikel = eg_request = eg_subtask = eg_queasy = eg_vperform = None

    tbrowse = tbuff = None

    tbrowse_data, Tbrowse = create_model("Tbrowse", {"reqno":string, "opend":string, "processd":string, "doned":string, "subtask":string, "reqstat":string, "tflag":string})

    Tbuff = create_buffer("Tbuff",L_artikel)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal grand_total, tbrowse_data, atotal, btotal, tot, int_str, l_artikel, eg_request, eg_subtask, eg_queasy, eg_vperform
        nonlocal prop_nr, fdate, tdate
        nonlocal tbuff


        nonlocal tbrowse, tbuff
        nonlocal tbrowse_data

        return {"grand_total": grand_total, "tbrowse": tbrowse_data}

    def create_history():

        nonlocal grand_total, tbrowse_data, atotal, btotal, tot, int_str, l_artikel, eg_request, eg_subtask, eg_queasy, eg_vperform
        nonlocal prop_nr, fdate, tdate
        nonlocal tbuff


        nonlocal tbrowse, tbuff
        nonlocal tbrowse_data

        char1:string = ""
        str_op:string = ""
        str_cd:string = ""
        str_dd:string = ""
        itotal:Decimal = to_decimal("0.0")
        tbrowse_data.clear()
        atotal = 0
        btotal =  to_decimal("0")

        for eg_request in db_session.query(Eg_request).filter(
                 ((Eg_request.propertynr == prop_nr) & (Eg_request.opened_date >= fdate) & (Eg_request.opened_date <= tdate)) | ((Eg_request.propertynr == prop_nr) & (Eg_request.closed_date >= fdate) & (Eg_request.closed_date <= tdate)) | ((Eg_request.propertynr == prop_nr) & (Eg_request.process_date >= fdate) & (Eg_request.process_date <= tdate))).order_by(Eg_request._recid).all():

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

            eg_subtask = get_cache (Eg_subtask, {"sub_code": [(eq, eg_request.sub_task)]})

            if eg_subtask:
                char1 = eg_subtask.bezeich
            else:
                char1 = ""
            tbrowse = Tbrowse()
            tbrowse_data.append(tbrowse)

            tbrowse.tflag = "1"
            tbrowse.reqno = to_string(eg_request.reqnr , "->>>>>>>>9")
            tbrowse.opend = str_op
            tbrowse.processd = str_cd
            tbrowse.doned = str_dd
            tbrowse.subtask = char1
            tbrowse.reqstat = to_string(int_str[eg_request.reqstatus - 1])

            eg_queasy = get_cache (Eg_queasy, {"key": [(eq, 1)],"reqnr": [(eq, eg_request.reqnr)]})

            if eg_queasy:

                for eg_queasy in db_session.query(Eg_queasy).filter(
                         (Eg_queasy.key == 1) & (Eg_queasy.reqnr == eg_request.reqnr)).order_by(Eg_queasy._recid).all():

                    tbuff = db_session.query(Tbuff).filter(
                             (Tbuff.artnr == eg_queasy.stock_nr)).first()

                    if tbuff:
                        itotal =  to_decimal(eg_queasy.deci1) * to_decimal(eg_queasy.price)
                    tot =  to_decimal(tot) + to_decimal(itotal)

            eg_vperform = get_cache (Eg_vperform, {"reqnr": [(eq, eg_request.reqnr)]})

            if eg_vperform:

                for eg_vperform in db_session.query(Eg_vperform).filter(
                         (Eg_vperform.reqnr == eg_request.reqnr)).order_by(Eg_vperform._recid).all():
                    tot =  to_decimal(tot) + to_decimal(eg_vperform.price)

            if tot != 0:
                btotal =  to_decimal(btotal) + to_decimal(tot)
                tot =  to_decimal("0")

        if btotal != 0:
            grand_total = to_string(btotal, "->>>,>>>,>>>,>>9.99")

    create_history()

    return generate_output()