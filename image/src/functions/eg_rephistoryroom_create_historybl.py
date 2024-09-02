from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import L_artikel, Eg_request, Eg_property, Eg_subtask, Eg_queasy, Eg_vperform, Eg_vendor

def eg_rephistoryroom_create_historybl(room_nr:str, fdate:date, tdate:date, prop_nr:int):
    tbrowse_list = []
    tprop_list = []
    tot:int = 0
    atotal:int = 0
    btotal:int = 0
    int_str:[str] = ["", "", "", "", "", ""]
    l_artikel = eg_request = eg_property = eg_subtask = eg_queasy = eg_vperform = eg_vendor = None

    tprop = tbrowse = tbuff = None

    tprop_list, Tprop = create_model("Tprop", {"nr":int, "nm":str})
    tbrowse_list, Tbrowse = create_model("Tbrowse", {"desc1":str, "desc2":str, "reqno":str, "opend":str, "processd":str, "doned":str, "subtask":str, "reqstat":str, "tflag":str})

    Tbuff = L_artikel

    db_session = local_storage.db_session

    def generate_output():
        nonlocal tbrowse_list, tprop_list, tot, atotal, btotal, int_str, l_artikel, eg_request, eg_property, eg_subtask, eg_queasy, eg_vperform, eg_vendor
        nonlocal tbuff


        nonlocal tprop, tbrowse, tbuff
        nonlocal tprop_list, tbrowse_list
        return {"tbrowse": tbrowse_list, "tprop": tprop_list}

    def create_history():

        nonlocal tbrowse_list, tprop_list, tot, atotal, btotal, int_str, l_artikel, eg_request, eg_property, eg_subtask, eg_queasy, eg_vperform, eg_vendor
        nonlocal tbuff


        nonlocal tprop, tbrowse, tbuff
        nonlocal tprop_list, tbrowse_list

        char1:str = ""
        char2:str = ""
        char3:str = ""
        char4:str = ""
        a:str = ""
        b:str = ""
        c:str = ""
        vendo_nm:str = ""
        itotal:decimal = 0
        nm_prop:str = ""
        char1 = " Art No.      Article                                  "
        char2 = ""
        tbrowse_list.clear()
        tprop_list.clear()
        tbrowse = Tbrowse()
        tbrowse_list.append(tbrowse)

        tbrowse.desc1 = char1
        tbrowse.desc2 = char2
        tbrowse.tflag = "0"


        tbrowse = Tbrowse()
        tbrowse_list.append(tbrowse)

        tbrowse.desc1 = "================================================================================"
        tbrowse.desc2 = "=================================================="
        tbrowse.tflag = "0"


        atotal = 0
        btotal = 0

        for eg_request in db_session.query(Eg_request).filter(
                (func.lower(Eg_request.zinr) == (room_nr).lower()) &  (Eg_request.opened_date >= fdate) &  (Eg_request.opened_date <= tdate) |  (Eg_request.propertynr == prop_nr) &  (Eg_request.closed_date >= fdate) &  (Eg_request.closed_date <= tdate) |  (Eg_request.propertynr == prop_nr) &  (Eg_request.process_date >= fdate) &  (Eg_request.process_date <= tdate)).all():

            tprop = query(tprop_list, filters=(lambda tprop :tprop.nr == eg_request.propertynr), first=True)

            if not tprop:

                eg_property = db_session.query(Eg_property).filter(
                        (Eg_property.nr == eg_request.propertynr)).first()

                if eg_property:
                    nm_prop = eg_property.bezeich
                else:
                    nm_prop = ""
                tprop = Tprop()
                tprop_list.append(tprop)

                tprop.nr = eg_request.propertynr
                tprop.nm = nm_prop


                char1 = to_string(eg_request.propertynr , "->>>>>>9") + "  " + to_string(nm_prop, "x(30)") + "  "
                char2 = "   "
                tbrowse = Tbrowse()
                tbrowse_list.append(tbrowse)

                tbrowse.desc1 = char1
                tbrowse.desc2 = char2
                tbrowse.tflag = "0"


                tbrowse = Tbrowse()
                tbrowse_list.append(tbrowse)

                tbrowse.desc1 = "--------------------------------------------------------------------------------"
                tbrowse.desc2 = "--------------------------------------------------"
                tbrowse.tflag = "0"

            if eg_request.opened_date == None:
                a = "    -     "
            else:
                a = to_string(eg_request.opened_date , "99/99/99")

            if eg_request.closed_date == None:
                b = "   -     "
            else:
                b = to_string(eg_request.closed_date , "99/99/99")

            if eg_request.done_date == None:
                c = "    -    "
            else:
                c = to_string(eg_request.done_date , "99/99/99")

            eg_subtask = db_session.query(Eg_subtask).filter(
                    (Eg_subtask.sub_CODE == eg_request.sub_task)).first()

            if eg_subtask:
                char4 = to_string(eg_subtask.bezeich , "x(36)")
            else:
                char4 = ""
            char1 = "          Req No.  Open       Process    Done       Task                          "
            char2 = "Status "
            tbrowse = Tbrowse()
            tbrowse_list.append(tbrowse)

            tbrowse.desc1 = char1
            tbrowse.desc2 = char2
            tbrowse.tflag = "0"


            tbrowse = Tbrowse()
            tbrowse_list.append(tbrowse)

            tbrowse.desc1 = "         -----------------------------------------------------------------------"
            tbrowse.desc2 = "--------------------------------------------------"
            tbrowse.tflag = "0"


            tbrowse.desc1 = "         -----------------------------------------------------------------------"
            tbrowse.desc2 = "--------------------------------------------------"
            tbrowse.tflag = "0"


            char1 = "         " + to_string(eg_request.reqnr , "->>>>>>9") + "  " + to_string(a, "x(9)") + "  " + to_string(b, "x(9)") + "  " + to_string(c, "x(9)") + "  " + to_string(char4, "x(20)") + "   "
            char2 = to_string(int_str[eg_request.reqstatus - 1], "x(10)") + "   "
            tbrowse = Tbrowse()
            tbrowse_list.append(tbrowse)

            tbrowse.desc1 = char1
            tbrowse.desc2 = char2
            tbrowse.tflag = "1"
            tbrowse.reqno = to_string(eg_request.reqnr , "->>>>>>9")
            tbrowse.opend = to_string(a, "x(9)")
            tbrowse.processd = to_string(b, "x(9)")
            tbrowse.doned = to_string(c, "x(9)")
            tbrowse.subtask = to_string(char4, "x(30)")
            tbrowse.reqstat = to_string(int_str[eg_request.reqstatus - 1], "x(10)")

            eg_queasy = db_session.query(Eg_queasy).filter(
                    (Eg_queasy.key == 1) &  (Eg_queasy.reqnr == eg_request.reqnr)).first()

            if eg_queasy:
                tbrowse = Tbrowse()
                tbrowse_list.append(tbrowse)

                tbrowse.desc1 = ""
                tbrowse.desc2 = ""
                tbrowse.tflag = "0"


                tbrowse = Tbrowse()
                tbrowse_list.append(tbrowse)

                tbrowse.desc1 = "        " + "           Art No.    Stock Article                  "
                tbrowse.desc2 = "     QTY        Price              TOTAL          "
                tbrowse.tflag = "0"


                tbrowse = Tbrowse()
                tbrowse_list.append(tbrowse)

                tbrowse.desc1 = "        " + "           -----------------------------------------------------------------------"
                tbrowse.desc2 = "--------------------------------------------------"
                tbrowse.tflag = "0"


                char2 = ""
                char3 = ""

                for eg_queasy in db_session.query(Eg_queasy).filter(
                        (Eg_queasy.key == 1) &  (Eg_queasy.reqnr == eg_request.reqnr)).all():

                    tbuff = db_session.query(Tbuff).filter(
                            (Tbuff.artnr == eg_queasy.stock_nr)).first()

                    if tbuff:
                        itotal = eg_queasy.deci1 * eg_queasy.price
                        char2 = "         " + "           " + to_string(eg_queasy.stock_nr, "9999999") + "    " + to_string(tbuff.bezeich , "x(26)") + "   "
                        char3 = to_string(eg_queasy.deci1 , "->>>>>>9") + "   " + to_string(eg_queasy.price, ">>>,>>>,>>9") + "   " + to_string(itotal , ">>>,>>>,>>>,>>9") + "   "
                        tbrowse = Tbrowse()
                        tbrowse_list.append(tbrowse)

                        tbrowse.desc1 = char2
                        tbrowse.desc2 = char3
                        tbrowse.tflag = "1"


                        char2 = ""
                        char3 = ""
                    tot = tot + itotal

            eg_vperform = db_session.query(Eg_vperform).filter(
                    (Eg_vperform.reqnr == eg_request.reqnr)).first()

            if eg_vperform:
                tbrowse = Tbrowse()
                tbrowse_list.append(tbrowse)

                tbrowse.desc1 = ""
                tbrowse.desc2 = ""
                tbrowse.tflag = "0"


                tbrowse = Tbrowse()
                tbrowse_list.append(tbrowse)

                tbrowse.desc1 = "        " + "           Outsource  Vendor                        "
                tbrowse.desc2 = "Start Date      Finish Date        Price  "
                tbrowse.tflag = "0"


                tbrowse = Tbrowse()
                tbrowse_list.append(tbrowse)

                tbrowse.desc1 = "        " + "           -----------------------------------------------------------------------"
                tbrowse.desc2 = "--------------------------------------------------"
                tbrowse.tflag = "0"


                char2 = ""
                char3 = ""

                for eg_vperform in db_session.query(Eg_vperform).filter(
                        (Eg_vperform.reqnr == eg_request.reqnr)).all():

                    eg_vendor = db_session.query(Eg_vendor).filter(
                            (Eg_vendor.vendor_nr == eg_vperform.vendor_nr)).first()

                    if eg_vendor:
                        vendo_nm = eg_vendor.bezeich
                    else:
                        vendo_nm = "Undefine"

                    if eg_vperform.startdate == None:
                        a = "    -    "
                    else:
                        a = " " + to_string(eg_vperform.startdate , "99/99/99")

                    if eg_vperform.finishdate == None:
                        b = "      -     "
                    else:
                        b = "    " + to_string(eg_vperform.finishdate , "99/99/99")
                    char2 = "         " + "           " + to_string(eg_vperform.perform_nr, "9999999") + "    " + to_string(vendo_nm , "x(26)") + "  "
                    char3 = a + "  " + b + "  " + to_string(eg_vperform.price , ">>>,>>>,>>>,>>9") + "  "
                    tbrowse = Tbrowse()
                    tbrowse_list.append(tbrowse)

                    tbrowse.desc1 = char2
                    tbrowse.desc2 = char3
                    tbrowse.tflag = "0"


                    char2 = ""
                    char3 = ""
                    tot = tot + eg_vperform.price

            if tot != 0:
                tbrowse = Tbrowse()
                tbrowse_list.append(tbrowse)

                tbrowse.desc1 = "         -----------------------------------------------------------------------"
                tbrowse.desc2 = "--------------------------------------------------"
                tbrowse.tflag = "0"


                tbrowse = Tbrowse()
                tbrowse_list.append(tbrowse)

                tbrowse.desc1 = "                                                                "
                tbrowse.desc2 = "                TOTAL     " + to_string(tot , ">>,>>>,>>>,>>9")


                tbrowse = Tbrowse()
                tbrowse_list.append(tbrowse)

                tbrowse.desc1 = "                                                                "
                tbrowse.desc2 = "  "


                btotal = btotal + tot
                tot = 0
        tbrowse = Tbrowse()
        tbrowse_list.append(tbrowse)

        tbrowse.desc1 = "=================================================================================="
        tbrowse.desc2 = "=================================================="
        tbrowse.tflag = "0"


        tbrowse = Tbrowse()
        tbrowse_list.append(tbrowse)

        tbrowse.desc1 = "                                                                "
        tbrowse.desc2 = "          GRAND TOTAL  " + to_string(btotal , ">,>>>,>>>,>>>,>>9")


        OPEN QUERY q3 FOR EACH tbrowse

    create_history()

    return generate_output()