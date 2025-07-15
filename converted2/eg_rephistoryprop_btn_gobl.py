#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import L_artikel, Eg_request, Eg_subtask, Eg_queasy, Eg_vperform, Eg_vendor

def eg_rephistoryprop_btn_gobl(prop_nr:int, fdate:date, tdate:date):

    prepare_cache ([L_artikel, Eg_request, Eg_subtask, Eg_queasy, Eg_vperform, Eg_vendor])

    tbrowse_data = []
    atotal:int = 0
    btotal:int = 0
    tot:int = 0
    int_str:List[string] = ["New", "Processed", "Done", "Postponed", "Closed"]
    l_artikel = eg_request = eg_subtask = eg_queasy = eg_vperform = eg_vendor = None

    tbrowse = tbuff = None

    tbrowse_data, Tbrowse = create_model("Tbrowse", {"desc1":string, "desc2":string, "reqno":string, "opend":string, "processd":string, "doned":string, "subtask":string, "reqstat":string, "tflag":string})

    Tbuff = create_buffer("Tbuff",L_artikel)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal tbrowse_data, atotal, btotal, tot, int_str, l_artikel, eg_request, eg_subtask, eg_queasy, eg_vperform, eg_vendor
        nonlocal prop_nr, fdate, tdate
        nonlocal tbuff


        nonlocal tbrowse, tbuff
        nonlocal tbrowse_data

        return {"tbrowse": tbrowse_data}

    def create_history():

        nonlocal tbrowse_data, atotal, btotal, tot, int_str, l_artikel, eg_request, eg_subtask, eg_queasy, eg_vperform, eg_vendor
        nonlocal prop_nr, fdate, tdate
        nonlocal tbuff


        nonlocal tbrowse, tbuff
        nonlocal tbrowse_data

        char1:string = ""
        char2:string = ""
        char3:string = ""
        char4:string = ""
        a:string = ""
        b:string = ""
        c:string = ""
        vendo_nm:string = ""
        itotal:Decimal = to_decimal("0.0")
        char1 = " Req No. Open Process Done Object Task "
        char2 = "Status "
        tbrowse_data.clear()
        tbrowse = Tbrowse()
        tbrowse_data.append(tbrowse)

        tbrowse.desc1 = char1
        tbrowse.desc2 = char2
        tbrowse.tflag = "0"


        tbrowse = Tbrowse()
        tbrowse_data.append(tbrowse)

        tbrowse.desc1 = "================================================================================"
        tbrowse.desc2 = "=================================================="
        tbrowse.tflag = "0"


        atotal = 0
        btotal = 0

        for eg_request in db_session.query(Eg_request).filter(
                 (Eg_request.propertynr == prop_nr) & (Eg_request.opened_date >= fdate) & (Eg_request.opened_date <= tdate) | (Eg_request.propertynr == prop_nr) & (Eg_request.closed_date >= fdate) & (Eg_request.closed_date <= tdate) | (Eg_request.propertynr == prop_nr) & (Eg_request.process_date >= fdate) & (Eg_request.process_date <= tdate)).order_by(Eg_request._recid).all():

            if eg_request.opened_date == None:
                a = " - "
            else:
                a = to_string(eg_request.opened_date , "99/99/99")

            if eg_request.closed_date == None:
                b = " - "
            else:
                b = to_string(eg_request.closed_date , "99/99/99")

            if eg_request.done_date == None:
                c = " - "
            else:
                c = to_string(eg_request.done_date , "99/99/99")

            eg_subtask = get_cache (Eg_subtask, {"sub_code": [(eq, eg_request.sub_task)]})

            if eg_subtask:
                char4 = to_string(eg_subtask.bezeich , "x(36)")
            else:
                char4 = ""
            char1 = to_string(eg_request.reqnr , "->>>>>>9") + " " + to_string(a, "x(9)") + " " + to_string(b, "x(9)") + " " + to_string(c, "x(9)") + " " + to_string(char4, "x(30)") + " "
            char2 = to_string(int_str[eg_request.reqstatus - 1], "x(10)") + " "
            tbrowse = Tbrowse()
            tbrowse_data.append(tbrowse)

            tbrowse.desc1 = char1
            tbrowse.desc2 = char2
            tbrowse.tflag = "1"
            tbrowse.reqno = to_string(eg_request.reqnr , "->>>>>>9")
            tbrowse.opend = to_string(a, "x(9)")
            tbrowse.processd = to_string(b, "x(9)")
            tbrowse.doned = to_string(c, "x(9)")
            tbrowse.subtask = to_string(char4, "x(30)")
            tbrowse.reqstat = to_string(int_str[eg_request.reqstatus - 1], "x(10)")

            eg_queasy = get_cache (Eg_queasy, {"key": [(eq, 1)],"reqnr": [(eq, eg_request.reqnr)]})

            if eg_queasy:
                tbrowse = Tbrowse()
                tbrowse_data.append(tbrowse)

                tbrowse.desc1 = ""
                tbrowse.desc2 = ""
                tbrowse.tflag = "0"


                tbrowse = Tbrowse()
                tbrowse_data.append(tbrowse)

                tbrowse.desc1 = " Art No. Article "
                tbrowse.desc2 = " QTY Price TOTAL "
                tbrowse.tflag = "0"

                tbrowse = Tbrowse()
                tbrowse_data.append(tbrowse)

                tbrowse.desc1 = " -----------------------------------------------------------------------"
                tbrowse.desc2 = "--------------------------------------------------"
                tbrowse.tflag = "0"


                char2 = ""
                char3 = ""

                for eg_queasy in db_session.query(Eg_queasy).filter(
                         (Eg_queasy.key == 1) & (Eg_queasy.reqnr == eg_request.reqnr)).order_by(Eg_queasy._recid).all():

                    tbuff = get_cache (L_artikel, {"artnr": [(eq, eg_queasy.stock_nr)]})

                    if tbuff:
                        itotal =  to_decimal(eg_queasy.deci1) * to_decimal(eg_queasy.price)
                        char2 = " " + to_string(eg_queasy.stock_nr, "9999999") + " " + to_string(tbuff.bezeich , "x(36)") + " "
                        char3 = to_string(eg_queasy.deci1 , "->>>>>>9") + " " + to_string(eg_queasy.price, ">>>,>>>,>>9") + " " + to_string(itotal , ">>>,>>>,>>>,>>9") + " "
                        tbrowse = Tbrowse()
                        tbrowse_data.append(tbrowse)

                        tbrowse.desc1 = char2
                        tbrowse.desc2 = char3
                        tbrowse.tflag = "1"


                        char2 = ""
                        char3 = ""
                    tot = tot + itotal

            eg_vperform = get_cache (Eg_vperform, {"reqnr": [(eq, eg_request.reqnr)]})

            if eg_vperform:
                tbrowse = Tbrowse()
                tbrowse_data.append(tbrowse)

                tbrowse.desc1 = ""
                tbrowse.desc2 = ""
                tbrowse.tflag = "0"


                tbrowse = Tbrowse()
                tbrowse_data.append(tbrowse)

                tbrowse.desc1 = " Outsource Vendor "
                tbrowse.desc2 = "Start Date Finish Date Price "
                tbrowse.tflag = "0"


                tbrowse = Tbrowse()
                tbrowse_data.append(tbrowse)

                tbrowse.desc1 = " -----------------------------------------------------------------------"
                tbrowse.desc2 = "--------------------------------------------------"
                tbrowse.tflag = "0"


                char2 = ""
                char3 = ""

                for eg_vperform in db_session.query(Eg_vperform).filter(
                         (Eg_vperform.reqnr == eg_request.reqnr)).order_by(Eg_vperform._recid).all():

                    eg_vendor = get_cache (Eg_vendor, {"vendor_nr": [(eq, eg_vperform.vendor_nr)]})

                    if eg_vendor:
                        vendo_nm = eg_vendor.bezeich
                    else:
                        vendo_nm = "Undefine"

                    if eg_vperform.startdate == None:
                        a = " - "
                    else:
                        a = " " + to_string(eg_vperform.startdate , "99/99/99")

                    if eg_vperform.finishdate == None:
                        b = " - "
                    else:
                        b = " " + to_string(eg_vperform.finishdate , "99/99/99")
                    char2 = " " + to_string(eg_vperform.perform_nr, "9999999") + " " + to_string(vendo_nm , "x(36)") + " "
                    char3 = a + " " + b + " " + to_string(eg_vperform.price , ">>>,>>>,>>>,>>9") + " "
                    tbrowse = Tbrowse()
                    tbrowse_data.append(tbrowse)

                    tbrowse.desc1 = char2
                    tbrowse.desc2 = char3
                    tbrowse.tflag = "0"


                    char2 = ""
                    char3 = ""
                    tot = tot + eg_vperform.price

            if tot != 0:
                tbrowse = Tbrowse()
                tbrowse_data.append(tbrowse)

                tbrowse.desc1 = " "
                tbrowse.desc2 = " TOTAL " + to_string(tot , ">>,>>>,>>>,>>9")


                btotal = btotal + tot
                tot = 0
        tbrowse = Tbrowse()
        tbrowse_data.append(tbrowse)

        tbrowse.desc1 = "=================================================================================="
        tbrowse.desc2 = "=================================================="
        tbrowse.tflag = "0"


        tbrowse = Tbrowse()
        tbrowse_data.append(tbrowse)

        tbrowse.desc1 = " "
        tbrowse.desc2 = " GRAND TOTAL " + to_string(btotal , ">,>>>,>>>,>>>,>>9")

    create_history()

    return generate_output()