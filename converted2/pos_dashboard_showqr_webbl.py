#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from functions.pos_dashboard_checksessionbl import pos_dashboard_checksessionbl
from functions.pos_dashboard_proc_sessionbl import pos_dashboard_proc_sessionbl
from functions.pos_dashboard_taken_tablebl import pos_dashboard_taken_tablebl
from functions.pos_dashboard_opened_tischbl import pos_dashboard_opened_tischbl

def pos_dashboard_showqr_webbl(asroom_service:bool, dynamic_qr:bool, outlet_number:int, table_nr:int, guest_name:string, pax:int, urlws:string, licensenr:int):
    result_msg = ""
    encodedurl = ""
    encodedsession = ""
    dataqr = ""
    pathqr = ""
    table_taken = False
    flag_rs = False
    t_list_data = []
    pick_table_data = []
    mmemptr:bytes = None
    encodedtext:string = ""
    sessionid:string = ""
    sha_sessionid:string = ""
    session_ok:bool = False
    success_taken:bool = False
    loop_session:int = 0

    t_list = pick_table = None

    t_list_data, T_list = create_model("T_list", {"dept":int, "tischnr":int, "bezeich":string, "normalbeleg":int, "name":string, "occupied":bool, "belegung":int, "balance":Decimal, "zinr":string, "gname":string, "ask_bill":bool, "bill_print":bool, "platform":string, "allow_ctr":string, "bill_number":int, "pay_status":string})
    pick_table_data, Pick_table = create_model("Pick_table", {"dept":int, "tableno":int, "pax":int, "gname":string, "occupied":bool, "session_parameter":string, "gemail":string, "expired_session":bool, "dataqr":string, "date_time":datetime})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal result_msg, encodedurl, encodedsession, dataqr, pathqr, table_taken, flag_rs, t_list_data, pick_table_data, mmemptr, encodedtext, sessionid, sha_sessionid, session_ok, success_taken, loop_session
        nonlocal asroom_service, dynamic_qr, outlet_number, table_nr, guest_name, pax, urlws, licensenr


        nonlocal t_list, pick_table
        nonlocal t_list_data, pick_table_data

        return {"result_msg": result_msg, "encodedurl": encodedurl, "encodedsession": encodedsession, "dataqr": dataqr, "pathqr": pathqr, "table_taken": table_taken, "flag_rs": flag_rs, "t-list": t_list_data, "pick-table": pick_table_data}


    if guest_name == None:
        guest_name = ""

    if urlws == None:
        urlws = ""

    if urlws == "":
        result_msg = "UrlWebServices Not Available In Configuration Setup."

        return generate_output()

    if not asroom_service:

        if dynamic_qr:
            for loop_session in range(1,10 + 1) :
                sessionid = to_string(get_current_date()) + to_string(get_current_time_in_seconds()) + to_string(outlet_number) + to_string(table_nr) + guest_name
                sha_sessionid = sha1(sessionid).hexdigest()
                encodedtext = substring(sha_sessionid, 0, 20)
                sessionid = encodedtext
                session_ok = get_output(pos_dashboard_checksessionbl(sessionid))

                if session_ok:
                    break
            mmemptr =  encodedtext
            encodedtext = base64_encode(mmemptr)
            encodedsession = to_string(encodedtext)

            if urlws != "":
                encodedtext = urlws
                mmemptr =  encodedtext
                encodedtext = base64_encode(mmemptr)
                encodedurl = to_string(encodedtext)
            pathqr = "C:\\e1-vhp\\Zint\\QRData"
            dataqr = "https://online-order.e1-vhp.com/selforder?endpoint=" + encodedurl + "&session=" + encodedsession
            get_output(pos_dashboard_proc_sessionbl(1, sessionid, outlet_number, table_nr, guest_name, pax, "", "", "", "", ""))
            table_taken = True
        else:
            encodedtext = to_string(licensenr) + "d271092o" + to_string(outlet_number) + "@170763t" + to_string(table_nr)
            sessionid = encodedtext
            mmemptr =  encodedtext
            encodedtext = base64_encode(mmemptr)
            encodedsession = to_string(encodedtext)

            if urlws != "":
                encodedtext = urlws
                mmemptr =  encodedtext
                encodedtext = base64_encode(mmemptr)
                encodedurl = to_string(encodedtext)
            pathqr = "C:\\e1-vhp\\Zint\\QRData"
            dataqr = "https://online-order.e1-vhp.com/selforder?endpoint=" + encodedurl + "&session=" + encodedsession
            get_output(pos_dashboard_proc_sessionbl(1, sessionid, outlet_number, table_nr, guest_name, pax, "", "", "", "", ""))
            table_taken = True

        if table_taken:
            success_taken, pick_table_data = get_output(pos_dashboard_taken_tablebl(1, sessionid, table_nr, guest_name, pax, outlet_number, dataqr, to_datetime(get_current_date(), MTIME), dynamic_qr))

            if success_taken:
                t_list_data, pick_table_data = get_output(pos_dashboard_opened_tischbl(outlet_number))
    else:

        if urlws != "":
            encodedtext = urlws
            mmemptr =  encodedtext
            encodedtext = base64_encode(mmemptr)
            encodedurl = to_string(encodedtext)
        pathqr = "C:\\e1-vhp\\Zint\\QRData"
        dataqr = "https://online-order.e1-vhp.com/selforder?endpoint=" + encodedurl + "&htlid=" + to_string(licensenr) + "&outlet=" + to_string(outlet_number)
        flag_rs = True

    return generate_output()