from functions.additional_functions import *
import decimal
from functions.pos_dashboard_checksessionbl import pos_dashboard_checksessionbl
from functions.pos_dashboard_proc_sessionbl import pos_dashboard_proc_sessionbl
from functions.pos_dashboard_taken_tablebl import pos_dashboard_taken_tablebl
from functions.pos_dashboard_opened_tischbl import pos_dashboard_opened_tischbl

def pos_dashboard_showqr_webbl(asroom_service:bool, dynamic_qr:bool, outlet_number:int, table_nr:int, guest_name:str, pax:int, urlws:str, licensenr:int):
    result_msg = ""
    encodedurl = ""
    encodedsession = ""
    dataqr = ""
    pathqr = ""
    table_taken = False
    flag_rs = False
    t_list_list = []
    pick_table_list = []
    mmemptr:bytes = None
    encodedtext:str = ""
    sessionid:str = ""
    sha_sessionid:str = ""
    session_ok:bool = False
    success_taken:bool = False
    loop_session:int = 0

    t_list = pick_table = None

    t_list_list, T_list = create_model("T_list", {"dept":int, "tischnr":int, "bezeich":str, "normalbeleg":int, "name":str, "occupied":bool, "belegung":int, "balance":decimal, "zinr":str, "gname":str, "ask_bill":bool, "bill_print":bool, "platform":str, "allow_ctr":str, "bill_number":int, "pay_status":str})
    pick_table_list, Pick_table = create_model("Pick_table", {"dept":int, "tableno":int, "pax":int, "gname":str, "occupied":bool, "session_parameter":str, "gemail":str, "expired_session":bool, "dataqr":str, "date_time":})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal result_msg, encodedurl, encodedsession, dataqr, pathqr, table_taken, flag_rs, t_list_list, pick_table_list, mmemptr, encodedtext, sessionid, sha_sessionid, session_ok, success_taken, loop_session


        nonlocal t_list, pick_table
        nonlocal t_list_list, pick_table_list
        return {"result_msg": result_msg, "encodedurl": encodedurl, "encodedsession": encodedsession, "dataqr": dataqr, "pathqr": pathqr, "table_taken": table_taken, "flag_rs": flag_rs, "t-list": t_list_list, "pick-table": pick_table_list}


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
            mmemptr = FROM encodedtext            encodedtext = BASE64_ENCODE (mmemptr)
            encodedsession = to_string(encodedtext)

            if urlws != "":
                encodedtext = urlws
                mmemptr = FROM encodedtext                encodedtext = BASE64_ENCODE (mmemptr)
                encodedurl = to_string(encodedtext)
            pathqr = "C:\\e1_vhp\\Zint\\QRData"
            dataqr = "https://online_order.e1_vhp.com/selforder?endpoint == " + encodedurl + "&session == " + encodedsession
            get_output(pos_dashboard_proc_sessionbl(1, sessionid, outlet_number, table_nr, guest_name, pax, "", "", "", "", ""))
            table_taken = True
        else:
            encodedtext = to_string(licensenr) + "d271092o" + to_string(outlet_number) + "@170763t" + to_string(table_nr)
            sessionid = encodedtext
            mmemptr = FROM encodedtext            encodedtext = BASE64_ENCODE (mmemptr)
            encodedsession = to_string(encodedtext)

            if urlws != "":
                encodedtext = urlws
                mmemptr = FROM encodedtext                encodedtext = BASE64_ENCODE (mmemptr)
                encodedurl = to_string(encodedtext)
            pathqr = "C:\\e1_vhp\\Zint\\QRData"
            dataqr = "https://online_order.e1_vhp.com/selforder?endpoint == " + encodedurl + "&session == " + encodedsession
            get_output(pos_dashboard_proc_sessionbl(1, sessionid, outlet_number, table_nr, guest_name, pax, "", "", "", "", ""))
            table_taken = True

        if table_taken:
            success_taken, pick_table_list = get_output(pos_dashboard_taken_tablebl(1, sessionid, table_nr, guest_name, pax, outlet_number, dataqr, DATETIME (get_current_date(), MTIME), dynamic_qr))

            if success_taken:
                t_list_list, pick_table_list = get_output(pos_dashboard_opened_tischbl(outlet_number))
    else:

        if urlws != "":
            encodedtext = urlws
            mmemptr = FROM encodedtext            encodedtext = BASE64_ENCODE (mmemptr)
            encodedurl = to_string(encodedtext)
        pathqr = "C:\\e1_vhp\\Zint\\QRData"
        dataqr = "https://online_order.e1_vhp.com/selforder?endpoint == " + encodedurl + "&htlid == " + to_string(licensenr) + "&outlet == " + to_string(outlet_number)
        flag_rs = True

    return generate_output()