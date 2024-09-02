from functions.additional_functions import *
import decimal
from datetime import date
from functions.prepare_mn_startbl import prepare_mn_startbl
from functions.mn_chg_sysdatesbl import mn_chg_sysdatesbl
from functions.na_startbl import na_startbl
from functions.delete_nitestorbl import delete_nitestorbl
import re
from functions.delete_nitehistbl import delete_nitehistbl
from functions.mn_noshowbl import mn_noshowbl
from functions.mn_extend_departurebl import mn_extend_departurebl
from functions.mn_crm_checkoutbl import mn_crm_checkoutbl
from functions.mn_early_checkoutbl import mn_early_checkoutbl
from functions.mn_update_zistatusbl import mn_update_zistatusbl
from functions.mn_fix_bill_datumbl import mn_fix_bill_datumbl
from functions.mn_del_old_billsbl import mn_del_old_billsbl
from functions.mn_del_old_billjournalbl import mn_del_old_billjournalbl
from functions.mn_del_old_resbl import mn_del_old_resbl
from functions.mn_del_old_roomplanbl import mn_del_old_roomplanbl
from functions.mn_del_old_debtbl import mn_del_old_debtbl
from functions.mn_del_old_apbl import mn_del_old_apbl
from functions.mn_del_old_rbillbl import mn_del_old_rbillbl
from functions.mn_del_old_rjournalbl import mn_del_old_rjournalbl
from functions.mn_del_old_bonsbl import mn_del_old_bonsbl
from functions.mn_del_old_outlet_umsatzbl import mn_del_old_outlet_umsatzbl
from functions.mn_del_old_callsbl import mn_del_old_callsbl
from functions.mn_del_old_pobl import mn_del_old_pobl
from functions.mn_del_old_l_opbl import mn_del_old_l_opbl
from functions.mn_del_old_statbl import mn_del_old_statbl
from functions.mn_del_interfacebl import mn_del_interfacebl
from functions.mn_del_nitehistbl import mn_del_nitehistbl
from functions.mn_del_old_baresbl import mn_del_old_baresbl
from functions.mn_update_logfile_recordsbl import mn_update_logfile_recordsbl
from functions.mn_del_oldbl import mn_del_oldbl
from functions.mn_club_softwarebl import mn_club_softwarebl
from sqlalchemy import func
from models import Paramtext, Queasy

def na_start_web2bl(language_code:int, htparam_recid:int, user_init:str, ans_arrguest:bool):
    printer_nr = 0
    success_flag = False
    mn_stopped:bool = False
    stop_it:bool = False
    arrival_guest:bool = False
    msg_str:str = ""
    mess_str:str = ""
    crm_license:bool = False
    banquet_license:bool = False
    na_date1:date = None
    na_time1:int = 0
    na_name1:str = ""
    mnstart_flag:bool = False
    store_flag:bool = False
    billdate:date = None
    na_date:date = None
    na_time:int = 0
    na_name:str = ""
    lic_nr:str = ""
    paramtext = queasy = None

    na_list = t_nightaudit = None

    na_list_list, Na_list = create_model("Na_list", {"reihenfolge":int, "flag":int, "anz":int, "bezeich":str})
    t_nightaudit_list, T_nightaudit = create_model("T_nightaudit", {"bezeichnung":str, "hogarest":int, "reihenfolge":int, "programm":str, "abschlussart":bool})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal printer_nr, success_flag, mn_stopped, stop_it, arrival_guest, msg_str, mess_str, crm_license, banquet_license, na_date1, na_time1, na_name1, mnstart_flag, store_flag, billdate, na_date, na_time, na_name, lic_nr, paramtext, queasy


        nonlocal na_list, t_nightaudit
        nonlocal na_list_list, t_nightaudit_list
        return {"printer_nr": printer_nr, "success_flag": success_flag}

    def na_prog():

        nonlocal printer_nr, success_flag, mn_stopped, stop_it, arrival_guest, msg_str, mess_str, crm_license, banquet_license, na_date1, na_time1, na_name1, mnstart_flag, store_flag, billdate, na_date, na_time, na_name, lic_nr, paramtext, queasy


        nonlocal na_list, t_nightaudit
        nonlocal na_list_list, t_nightaudit_list

        night_type:int = 0
        mn_stopped:bool = False
        a:int = 0
        session_parameter:str = ""
        i:int = 0
        success_flag:bool = False
        i = 0

        for t_nightaudit in query(t_nightaudit_list):
            i = i + 1
            cqueasy(to_string(t_nightaudit.bezeichnung, "x(40)"), "PROCESS")

            if store_flag:

                if t_nightaudit.hogarest == 0:
                    night_type = 0
                else:
                    night_type = 2
                success_flag = get_output(delete_nitestorbl(1, night_type, t_nightaudit.reihenfolge))

            if re.match(".*bl.p.*",t_nightaudit.programm):
                value(t_nightaudit.programm.lower())
            else:

                if to_int(t_nightaudit.abschlussart) == 1:
                    value(t_nightaudit.programm.lower())
                else:
                    a = R_INDEX (t_nightaudit.programm, ".p")
                    value(substring(t_nightaudit.programm.lower(), 0, a - 1) + "bl.p")

            if store_flag:
                success_flag = get_output(delete_nitehistbl(1, billdate, t_nightaudit.reihenfolge))
            cqueasy(to_string(t_nightaudit.bezeichnung, "x(40)"), "DONE")

    def midnite_prog():

        nonlocal printer_nr, success_flag, mn_stopped, stop_it, arrival_guest, msg_str, mess_str, crm_license, banquet_license, na_date1, na_time1, na_name1, mnstart_flag, store_flag, billdate, na_date, na_time, na_name, lic_nr, paramtext, queasy


        nonlocal na_list, t_nightaudit
        nonlocal na_list_list, t_nightaudit_list

        i:int = 0
        j:int = 0
        k:int = 0
        cqueasy("No Show List", "PROCESS")
        i, msg_str = get_output(mn_noshowbl(language_code))
        cqueasy("No Show List", "DONE")
        cqueasy("Extending Departure Date", "PROCESS")
        i = get_output(mn_extend_departurebl())
        cqueasy("Extending Departure Date", "DONE")

        if crm_license:
            cqueasy("CRM questionnair - C/O Guests", "PROCESS")
            get_output(mn_crm_checkoutbl())
            cqueasy("CRM questionnair - C/O Guests", "DONE")
        cqueasy("Early Checkout", "PROCESS")
        i = get_output(mn_early_checkoutbl())
        cqueasy("Early Checkout", "DONE")
        cqueasy("Updating Room Status", "PROCESS")
        i, msg_str = get_output(mn_update_zistatusbl(language_code))
        cqueasy("Updating Room Status", "DONE")
        cqueasy("Correcting bill date", "PROCESS")
        get_output(mn_fix_bill_datumbl())
        cqueasy("Correcting bill date", "DONE")
        cqueasy("Deleting old bills", "PROCESS")
        i = get_output(mn_del_old_billsbl())
        cqueasy("Deleting old bills", "DONE")
        cqueasy("Deleting old bill journals", "PROCESS")
        i = get_output(mn_del_old_billjournalbl())
        cqueasy("Deleting old bill journals", "DONE")
        cqueasy("Deleting old reservations", "PROCESS")
        i, j, k = get_output(mn_del_old_resbl())
        cqueasy("Deleting old reservations", "DONE")
        cqueasy("Deleting old roomplans", "PROCESS")
        i = get_output(mn_del_old_roomplanbl())
        cqueasy("Deleting old roomplans", "DONE")
        cqueasy("Deleting old paid debts", "PROCESS")
        i = get_output(mn_del_old_debtbl())
        cqueasy("Deleting old paid debts", "DONE")
        cqueasy("Deleting old paid a/P", "PROCESS")
        i = get_output(mn_del_old_apbl())
        cqueasy("Deleting old paid a/P", "DONE")
        cqueasy("Deleting old restaurant bills", "PROCESS")
        i = get_output(mn_del_old_rbillbl())
        cqueasy("Deleting old restaurant bills", "DONE")
        cqueasy("Deleting old rest.journals", "PROCESS")
        i, j = get_output(mn_del_old_rjournalbl())
        cqueasy("Deleting old rest.journals", "DONE")
        cqueasy("Deleting old rest.journals", "PROCESS")
        get_output(mn_del_old_bonsbl())
        cqueasy("Deleting old rest.journals", "DONE")
        cqueasy("Deleting old outlet turnovers", "PROCESS")
        i = get_output(mn_del_old_outlet_umsatzbl())
        cqueasy("Deleting old outlet turnovers", "DONE")
        cqueasy("Deleting old calls", "PROCESS")
        i = get_output(mn_del_old_callsbl())
        cqueasy("Deleting old calls", "DONE")
        cqueasy("Deleting old purchase orders", "PROCESS")
        i = get_output(mn_del_old_pobl())
        cqueasy("Deleting old purchase orders", "DONE")
        cqueasy("Deleted old stock moving journals", "PROCESS")
        i, j = get_output(mn_del_old_l_opbl())
        cqueasy("Deleted old stock moving journals", "DONE")
        cqueasy("Deleting old room number statistics", "PROCESS")
        i, j = get_output(mn_del_old_statbl(1))
        cqueasy("Deleting old room number statistics", "DONE")
        cqueasy("Deleting old room catagory statistics", "PROCESS")
        i, j = get_output(mn_del_old_statbl(2))
        cqueasy("Deleting old room catagory statistics", "DONE")
        cqueasy("Deleting old room catagory statistics", "PROCESS")
        i, j = get_output(mn_del_old_statbl(3))
        cqueasy("Deleting old source statistics", "DONE")
        cqueasy("Deleting old segment statistics", "PROCESS")
        i, j = get_output(mn_del_old_statbl(4))
        cqueasy("Deleting old segment statistics", "DONE")
        cqueasy("Deleting old market segment statistics", "PROCESS")
        i, j = get_output(mn_del_old_statbl(41))
        cqueasy("Deleting old market segment statistics", "DONE")
        cqueasy("Deleting old nation statistics", "PROCESS")
        i, j = get_output(mn_del_old_statbl(5))
        cqueasy("Deleting old nation statistics", "DONE")
        cqueasy("Deleting old turnover statistics", "PROCESS")
        i, j = get_output(mn_del_old_statbl(6))
        cqueasy("Deleting old turnover statistics", "DONE")
        cqueasy("Deleting old restaurant turnover statistics", "PROCESS")
        i, j = get_output(mn_del_old_statbl(7))
        cqueasy("Deleting old restaurant turnover statistics", "DONE")
        cqueasy("Deleting old F&B Costs", "PROCESS")
        i, j = get_output(mn_del_old_statbl(8))
        cqueasy("Deleting old F&B Costs", "DONE")
        cqueasy("Deleting old Exchange Rates", "PROCESS")
        i, j = get_output(mn_del_old_statbl(9))
        cqueasy("Deleting old Exchange Rates", "DONE")
        cqueasy("Deleting expired allotments", "PROCESS")
        del_allotment()
        cqueasy("Deleting expired allotments", "DONE")
        cqueasy("Deleting old DML_Articles", "PROCESS")
        i, j = get_output(mn_del_old_statbl(999))
        cqueasy("Deleting old DML_Articles", "DONE")
        cqueasy("Deleting old Interface Records", "PROCESS")
        get_output(mn_del_interfacebl(1))
        cqueasy("Deleting old Interface Records", "DONE")
        cqueasy("Deleting old nithist Records", "PROCESS")
        get_output(mn_del_nitehistbl())
        cqueasy("Deleting old nithist Records", "DONE")

        if banquet_license:
            cqueasy("Deleted old Banquet Reservations", "PROCESS")
            i = get_output(mn_del_old_baresbl())
            cqueasy("Deleted old Banquet Reservations", "DONE")
        cqueasy("Updating logfile records", "PROCESS")
        get_output(mn_update_logfile_recordsbl())
        cqueasy("Updating logfile records", "DONE")
        cqueasy("Deleting old F&B Compliments", "PROCESS")
        i = get_output(mn_del_oldbl(1))
        cqueasy("Deleting old F&B Compliments", "DONE")
        cqueasy("Deleting old Work Order Records", "PROCESS")
        i = get_output(mn_del_oldbl(2))
        cqueasy("Deleting old Work Order Records", "DONE")
        get_output(mn_club_softwarebl())

    def del_allotment():

        nonlocal printer_nr, success_flag, mn_stopped, stop_it, arrival_guest, msg_str, mess_str, crm_license, banquet_license, na_date1, na_time1, na_name1, mnstart_flag, store_flag, billdate, na_date, na_time, na_name, lic_nr, paramtext, queasy


        nonlocal na_list, t_nightaudit
        nonlocal na_list_list, t_nightaudit_list

    def decode_string(in_str:str):

        nonlocal printer_nr, success_flag, mn_stopped, stop_it, arrival_guest, msg_str, mess_str, crm_license, banquet_license, na_date1, na_time1, na_name1, mnstart_flag, store_flag, billdate, na_date, na_time, na_name, lic_nr, paramtext, queasy


        nonlocal na_list, t_nightaudit
        nonlocal na_list_list, t_nightaudit_list

        out_str = ""
        s:str = ""
        j:int = 0
        len_:int = 0

        def generate_inner_output():
            return out_str
        s = in_str
        j = ord(substring(s, 0, 1)) - 70
        len_ = len(in_str) - 1
        s = substring(in_str, 1, len_)
        for len_ in range(1,len(s)  + 1) :
            out_str = out_str + chr (ord(substring(s, len_ - 1, 1)) - j)


        return generate_inner_output()

    def cqueasy(bezeich:str, str_process:str):

        nonlocal printer_nr, success_flag, mn_stopped, stop_it, arrival_guest, msg_str, mess_str, crm_license, banquet_license, na_date1, na_time1, na_name1, mnstart_flag, store_flag, billdate, na_date, na_time, na_name, lic_nr, paramtext, queasy


        nonlocal na_list, t_nightaudit
        nonlocal na_list_list, t_nightaudit_list

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == 232) &  (func.lower(Queasy.char2) == (bezeich).lower()) &  (Queasy.date1 == get_current_date())).first()

        if not queasy:
            queasy = Queasy()
            db_session.add(queasy)

            queasy.key = 232
            queasy.char1 = "LOG NIGHT AUDIT"
            queasy.char2 = bezeich
            queasy.char3 = str_process
            queasy.date1 = get_current_date()
            queasy.number1 = get_current_time_in_seconds()


        else:

            queasy = db_session.query(Queasy).first()
            queasy.char3 = str_process

            queasy = db_session.query(Queasy).first()

    paramtext = db_session.query(Paramtext).filter(
            (Paramtext.txtnr == 243)).first()

    if paramtext:
        lic_nr = decode_string(paramtext.ptexte)

    for queasy in db_session.query(Queasy).filter(
            (Queasy.key == 232)).all():
        db_session.delete(queasy)

    if ans_arrguest:
        mn_stopped, stop_it, arrival_guest, msg_str, mess_str, crm_license, banquet_license, na_list_list = get_output(prepare_mn_startbl(2, language_code))

    if mn_stopped:
        pass
    else:
        midnite_prog()
        get_output(mn_chg_sysdatesbl())
        mnstart_flag, store_flag, printer_nr, t_nightaudit_list, na_date1, na_time1, na_name1 = get_output(na_startbl(2, user_init, htparam_recid))
    na_prog()
    mnstart_flag, store_flag, printer_nr, t_nightaudit_list, na_date, na_time, na_name = get_output(na_startbl(3, user_init, htparam_recid))
    success_flag = True

    for queasy in db_session.query(Queasy).filter(
            (Queasy.key == 232) &  (Queasy.date1 == TODAY)).all():
        db_session.delete(queasy)

    return generate_output()