#using conversion tools version: 1.0.0.117
#------------------------------------------
# Rd, 20/10/2025

# vhpNA/reprintNaPrepare -> prepare_reprint_nabl
# vhpFOC/naStartPrepare -> prepare_na_startbl
# vhpFOC/naCheck1 -> na_check1bl
# vhpFOC/naStart -> na_start_webbl
# vhpFOC/naStart2 -> na_start_web2bl
# vhpFOC/naStartGetInfo -> na_start_get_info_webbl
#------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.prepare_mn_startbl import prepare_mn_startbl
from functions.mn_chg_sysdatesbl import mn_chg_sysdatesbl
from functions.na_startbl import na_startbl
from functions.delete_nitestorbl import delete_nitestorbl
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
from functions.mn_del_lockrecord_queasybl import mn_del_lockrecord_queasybl
from functions.mn_add_notused_htparambl import mn_add_notused_htparambl
from functions.mn_club_softwarebl import mn_club_softwarebl

from models import Paramtext, Queasy
print("starting na_start_web2bl,1")

def na_run_program(function_name:string, input_data=()):
    function_name = function_name.replace(".py","")
    module_name = "functions." + function_name
    module = importlib.import_module(module_name)

    obj = getattr(module, function_name)
    return  obj(*input_data)

def na_start_web2bl(language_code:int, htparam_recid:int, user_init:string, ans_arrguest:bool):

    prepare_cache ([Paramtext])

    printer_nr = 0
    success_flag = False
    mn_stopped:bool = False
    stop_it:bool = False
    arrival_guest:bool = False
    msg_str:string = ""
    mess_str:string = ""
    crm_license:bool = False
    banquet_license:bool = False
    na_date1:date = None
    na_time1:int = 0
    na_name1:string = ""
    mnstart_flag:bool = False
    store_flag:bool = False
    billdate:date = None
    na_date:date = None
    na_time:int = 0
    na_name:string = ""
    lic_nr:string = ""
    paramtext = queasy = None

    na_list = t_nightaudit = None

    na_list_data, Na_list = create_model("Na_list", {"reihenfolge":int, "flag":int, "anz":int, "bezeich":string})
    t_nightaudit_data, T_nightaudit = create_model("T_nightaudit", {"bezeichnung":string, "hogarest":int, "reihenfolge":int, "programm":string, "abschlussart":bool})

    db_session = local_storage.db_session

    # def clear_log(key: int):    
    #     sql = f"DELETE FROM queasy WHERE key = {key}"
    #     db_session.execute(text(sql))
    #     db_session.commit()
    
    def log_process(key: int, message:string):
        queasy = Queasy()
        db_session.add(queasy)
        queasy.key = key
        queasy.char1 = "na_start_web2bl"
        queasy.char2 = message
        db_session.commit()
        print(f"Log Process [{key}]: {message}")

    # clear_log(270001)
    # # log_process(270001,"Starting na_start_web2bl")
    

    # def run_program(program_name:string):
    #     # log_process(270001, f"Running program: {program_name}")
    #     # Placeholder for actual program execution logic

    def generate_output():
        nonlocal printer_nr, success_flag, mn_stopped, stop_it, arrival_guest, msg_str, mess_str, crm_license, banquet_license, na_date1, na_time1, na_name1, mnstart_flag, store_flag, billdate, na_date, na_time, na_name, lic_nr, paramtext, queasy
        nonlocal language_code, htparam_recid, user_init, ans_arrguest


        nonlocal na_list, t_nightaudit
        nonlocal na_list_data, t_nightaudit_data

        return {"printer_nr": printer_nr, "success_flag": success_flag}

    def na_prog():

        nonlocal printer_nr, stop_it, arrival_guest, msg_str, mess_str, crm_license, banquet_license, na_date1, na_time1, na_name1, mnstart_flag, store_flag, billdate, na_date, na_time, na_name, lic_nr, paramtext, queasy
        nonlocal language_code, htparam_recid, user_init, ans_arrguest


        nonlocal na_list, t_nightaudit
        nonlocal na_list_data, t_nightaudit_data

        night_type:int = 0
        mn_stopped:bool = False
        a:int = 0
        session_parameter:string = ""
        i:int = 0
        success_flag:bool = False
        i = 0

        # for t_nightaudit in query(t_nightaudit_data, sort_by=[("(",False),("reihenfolge",False))]:
        t_nightaudit_sorted_list = sorted(
            t_nightaudit_data,
            key=lambda x: (-x.hogarest, x.reihenfolge)
        )
        for t_nightaudit in t_nightaudit_sorted_list:
            i = i + 1
            cqueasy(to_string(t_nightaudit.bezeichnung, "x(40)"), "PROCESS")
            log_process(270001, f"Processing: {t_nightaudit.bezeichnung}")
            if store_flag:

                if t_nightaudit.hogarest == 0:
                    night_type = 0
                else:
                    night_type = 2

                success_flag = get_output(delete_nitestorbl(1, night_type, t_nightaudit.reihenfolge))

            # if matches(t_nightaudit.programm,r"*bl.p*"):
            #     run_program(t_nightaudit.programm.lower())
            # else:

            #     if to_int(t_nightaudit.abschlussart) == 1:
            #         run_program(t_nightaudit.programm.lower())
            #     else:
            #         a = R_INDEX (t_nightaudit.programm, ".p")
            #         run_program(substring(t_nightaudit.programm.lower() , 0, a - 1) + "bl")

            programm = t_nightaudit.programm
            programm = programm.replace(".p",".py").replace(".r",".py").replace("-","_").lower()
            
            abschlussart = int(t_nightaudit.abschlussart)
            # print("LogfilProcessed program name:", programm)
            try:
                if abschlussart == 1:
                    log_process(270001, f"Run2: {programm}")
                    print("Running program 2:", programm)
                    na_run_program(programm)
                else:
                    programm = programm.replace(".py","bl.py")
                    log_process(270001, f"Run3 .p: {programm}")
                    print("Running program 3:", programm)
                    na_run_program(programm)
            except Exception as e:
                log_process(270001, f"Error running program {programm}: {str(e)}")
                print(f"Error running program {programm}: {str(e)}")

            if store_flag:
                success_flag = get_output(delete_nitehistbl(1, billdate, t_nightaudit.reihenfolge))

            cqueasy(to_string(t_nightaudit.bezeichnung, "x(40)"), "DONE")
            log_process(270001, f"Completed: {t_nightaudit.bezeichnung}")


    def midnite_prog():

        nonlocal printer_nr, success_flag, mn_stopped, stop_it, arrival_guest, msg_str, mess_str, crm_license, banquet_license, na_date1, na_time1, na_name1, mnstart_flag, store_flag, billdate, na_date, na_time, na_name, lic_nr, paramtext, queasy
        nonlocal language_code, htparam_recid, user_init, ans_arrguest


        nonlocal na_list, t_nightaudit
        nonlocal na_list_data, t_nightaudit_data

        i:int = 0
        j:int = 0
        k:int = 0

        na_steps:int = 0
        na_steps += 1
        log_process(270001, f"{na_steps}- midnite_prog, mn_noshowbl")
        cqueasy("No Show List", "PROCESS")
        i, msg_str = get_output(mn_noshowbl(language_code))
        log_process(270001, f"- midnite_prog, mn_noshowbl, DONE {i},{msg_str}")
        cqueasy("No Show List", "DONE")

        na_steps += 1
        log_process(270001, f"{na_steps}- midnite_prog, mn_extend_departurebl")
        cqueasy("Extending Departure Date", "PROCESS")
        i = get_output(mn_extend_departurebl())
        log_process(270001, f"- midnite_prog, mn_extend_departurebl, DONE {i}")
        cqueasy("Extending Departure Date", "DONE")

        if crm_license:
            log_process
            cqueasy("CRM questionnair - C/O Guests", "PROCESS")
            get_output(mn_crm_checkoutbl())
            cqueasy("CRM questionnair - C/O Guests", "DONE")

        na_steps += 1
        cqueasy("Early Checkout", "PROCESS")
        i = get_output(mn_early_checkoutbl())
        log_process(270001, f"- midnite_prog, mn_early_checkoutbl, DONE {i}")
        cqueasy("Early Checkout", "DONE")

        na_steps += 1
        log_process(270001, f"{na_steps}- midnite_prog, mn_update_zistatusbl")
        cqueasy("Updating Room Status", "PROCESS")
        i, msg_str = get_output(mn_update_zistatusbl(language_code))
        log_process(270001, f"- midnite_prog, mn_update_zistatusbl, DONE {i},{msg_str}")
        cqueasy("Updating Room Status", "DONE")

        na_steps += 1
        log_process(270001, f"{na_steps}- midnite_prog, mn_fix_bill_datumbl")
        cqueasy("Correcting bill date", "PROCESS")
        get_output(mn_fix_bill_datumbl())
        na_steps += 1
        log_process(270001, f"{na_steps}- midnite_prog, mn_fix_bill_datumbl, DONE")
        cqueasy("Correcting bill date", "DONE")

        na_steps += 1
        log_process(270001, f"{na_steps}- midnite_prog, deleting old records")
        cqueasy("Deleting old bills", "PROCESS")
        i = get_output(mn_del_old_billsbl())
        log_process(270001, f"- midnite_prog, mn_del_old_billsbl, DONE {i}")
        cqueasy("Deleting old bills", "DONE")

        na_steps += 1
        log_process(270001, f"{na_steps}- midnite_prog, deleting old bill journals")
        cqueasy("Deleting old bill journals", "PROCESS")
        i = get_output(mn_del_old_billjournalbl())
        log_process(270001, f"- midnite_prog, mn_del_old_billjournalbl, DONE {i}")
        cqueasy("Deleting old bill journals", "DONE")

        na_steps += 1
        log_process(270001, f"{na_steps}- midnite_prog, deleting old reservations")
        cqueasy("Deleting old reservations", "PROCESS")
        i, j, k = get_output(mn_del_old_resbl())
        log_process(270001, f"- midnite_prog, mn_del_old_resbl, DONE {i},{j},{k}")
        cqueasy("Deleting old reservations", "DONE")

        na_steps += 1
        log_process(270001, f"{na_steps}- midnite_prog, deleting old roomplans")
        cqueasy("Deleting old roomplans", "PROCESS")
        i = get_output(mn_del_old_roomplanbl())
        log_process(270001, f"- midnite_prog, mn_del_old_roomplanbl, DONE {i}")
        cqueasy("Deleting old roomplans", "DONE")

        na_steps += 1
        log_process(270001, f"{na_steps}- midnite_prog, deleting old paid debts")
        cqueasy("Deleting old paid debts", "PROCESS")
        i = get_output(mn_del_old_debtbl())
        log_process(270001, f"- midnite_prog, mn_del_old_debtbl, DONE {i}")
        cqueasy("Deleting old paid debts", "DONE")

        na_steps += 1
        log_process(270001, f"{na_steps}- midnite_prog, deleting old paid a/P")
        cqueasy("Deleting old paid a/P", "PROCESS")
        i = get_output(mn_del_old_apbl())
        log_process(270001, f"- midnite_prog, mn_del_old_apbl, DONE {i}")
        cqueasy("Deleting old paid a/P", "DONE")

        na_steps += 1
        log_process(270001, f"{na_steps}- midnite_prog, deleting old restaurant bills")
        cqueasy("Deleting old restaurant bills", "PROCESS")
        i = get_output(mn_del_old_rbillbl())
        log_process(270001, f"- midnite_prog, mn_del_old_rbillbl, DONE {i}")
        cqueasy("Deleting old restaurant bills", "DONE")

        na_steps += 1
        log_process(270001, f"{na_steps}- midnite_prog, deleting old restaurant journals")
        cqueasy("Deleting old rest.journals", "PROCESS")
        i, j = get_output(mn_del_old_rjournalbl())
        log_process(270001, f"- midnite_prog, mn_del_old_rjournalbl, DONE {i},{j}")
        cqueasy("Deleting old rest.journals", "DONE")

        na_steps += 1
        log_process(270001, f"{na_steps}- midnite_prog, deleting old bon journals")
        cqueasy("Deleting old rest.journals", "PROCESS")
        get_output(mn_del_old_bonsbl())
        na_steps += 1
        log_process(270001, f"{na_steps}- midnite_prog, mn_del_old_bonsbl, DONE")
        cqueasy("Deleting old rest.journals", "DONE")

        na_steps += 1
        log_process(270001, f"{na_steps}- midnite_prog, deleting old outlet turnovers")
        cqueasy("Deleting old outlet turnovers", "PROCESS")
        i = get_output(mn_del_old_outlet_umsatzbl())
        na_steps += 1
        log_process(270001, f"{na_steps}- midnite_prog, mn_del_old_outlet_umsatzbl, DONE {i}")
        cqueasy("Deleting old outlet turnovers", "DONE")

        na_steps += 1
        log_process(270001, f"{na_steps}- midnite_prog, deleting old calls")
        cqueasy("Deleting old calls", "PROCESS")
        i = get_output(mn_del_old_callsbl())
        log_process(270001, f"- midnite_prog, mn_del_old_callsbl, DONE {i}")
        cqueasy("Deleting old calls", "DONE")

        na_steps += 1
        log_process(270001, f"{na_steps}- midnite_prog, deleting old purchase orders")
        cqueasy("Deleting old purchase orders", "PROCESS")
        i = get_output(mn_del_old_pobl())
        log_process(270001, f"- midnite_prog, mn_del_old_pobl, DONE {i}")
        cqueasy("Deleting old purchase orders", "DONE")

        na_steps += 1
        log_process(270001, f"{na_steps}- midnite_prog, deleting old stock moving journals")
        cqueasy("Deleted old stock moving journals", "PROCESS")
        i, j = get_output(mn_del_old_l_opbl())
        log_process(270001, f"- midnite_prog, mn_del_old_l_opbl, DONE {i},{j}")
        cqueasy("Deleted old stock moving journals", "DONE")

        na_steps += 1
        log_process(270001, f"{na_steps}- midnite_prog, deleting old statistics")
        cqueasy("Deleting old room number statistics", "PROCESS")
        i, j = get_output(mn_del_old_statbl(1))
        log_process(270001, f"- midnite_prog, mn_del_old_statbl(1), DONE {i},{j}")
        cqueasy("Deleting old room number statistics", "DONE")

        na_steps += 1
        log_process(270001, f"{na_steps}- midnite_prog, deleting old statistics")
        cqueasy("Deleting old room catagory statistics", "PROCESS")
        i, j = get_output(mn_del_old_statbl(2))
        log_process(270001, f"- midnite_prog, mn_del_old_statbl(2), DONE {i},{j}")
        cqueasy("Deleting old room catagory statistics", "DONE")

        na_steps += 1
        log_process(270001, f"{na_steps}- midnite_prog, deleting old statistics")
        cqueasy("Deleting old room catagory statistics", "PROCESS")
        i, j = get_output(mn_del_old_statbl(3))
        log_process(270001, f"- midnite_prog, mn_del_old_statbl(3), DONE {i},{j}")
        cqueasy("Deleting old source statistics", "DONE")

        na_steps += 1
        log_process(270001, f"{na_steps}- midnite_prog, deleting old statistics")
        cqueasy("Deleting old segment statistics", "PROCESS")
        i, j = get_output(mn_del_old_statbl(4))
        log_process(270001, f"- midnite_prog, mn_del_old_statbl(4), DONE {i},{j}")
        cqueasy("Deleting old segment statistics", "DONE")

        na_steps += 1
        log_process(270001, f"{na_steps}- midnite_prog, deleting old statistics")
        cqueasy("Deleting old market segment statistics", "PROCESS")
        i, j = get_output(mn_del_old_statbl(41))
        log_process(270001, f"- midnite_prog, mn_del_old_statbl(41), DONE {i},{j}")
        cqueasy("Deleting old market segment statistics", "DONE")

        na_steps += 1
        log_process(270001, f"{na_steps}- midnite_prog, deleting old statistics")
        cqueasy("Deleting old nation statistics", "PROCESS")
        i, j = get_output(mn_del_old_statbl(5))
        log_process(270001, f"- midnite_prog, mn_del_old_statbl(5), DONE {i},{j}")
        cqueasy("Deleting old nation statistics", "DONE")

        na_steps += 1
        log_process(270001, f"{na_steps}- midnite_prog, deleting old statistics")    
        cqueasy("Deleting old turnover statistics", "PROCESS")
        i, j = get_output(mn_del_old_statbl(6))
        log_process(270001, f"- midnite_prog, mn_del_old_statbl(6), DONE {i},{j}")
        cqueasy("Deleting old turnover statistics", "DONE")

        na_steps += 1
        log_process(270001, f"{na_steps}- midnite_prog, deleting old statistics")
        cqueasy("Deleting old restaurant turnover statistics", "PROCESS")
        i, j = get_output(mn_del_old_statbl(7))
        log_process(270001, f"- midnite_prog, mn_del_old_statbl(7), DONE {i},{j}")
        cqueasy("Deleting old restaurant turnover statistics", "DONE")


        na_steps += 1
        log_process(270001, f"{na_steps}- midnite_prog, deleting old statistics")
        cqueasy("Deleting old F&B Costs", "PROCESS")
        i, j = get_output(mn_del_old_statbl(8))
        log_process(270001, f"- midnite_prog, mn_del_old_statbl(8), DONE {i},{j}")
        cqueasy("Deleting old F&B Costs", "DONE")

        na_steps += 1
        log_process(270001, f"{na_steps}- midnite_prog, deleting old statistics")
        cqueasy("Deleting old Exchange Rates", "PROCESS")
        i, j = get_output(mn_del_old_statbl(9))
        log_process(270001, f"- midnite_prog, mn_del_old_statbl(9), DONE {i},{j}")
        cqueasy("Deleting old Exchange Rates", "DONE")

        na_steps += 1
        log_process(270001, f"{na_steps}- midnite_prog, deleting expired allotments")
        cqueasy("Deleting expired allotments", "PROCESS")
        del_allotment()
        na_steps += 1
        log_process(270001, f"{na_steps}- midnite_prog, deleting expired allotments, DONE")
        cqueasy("Deleting expired allotments", "DONE")

        na_steps += 1
        log_process(270001, f"{na_steps}- midnite_prog, deleting old statistics")
        cqueasy("Deleting old DML-Articles", "PROCESS")
        i, j = get_output(mn_del_old_statbl(999))
        log_process(270001, f"- midnite_prog, mn_del_old_statbl(999), DONE {i},{j}")
        cqueasy("Deleting old DML-Articles", "DONE")

        na_steps += 1
        log_process(270001, f"{na_steps}- midnite_prog, deleting old interface records")
        cqueasy("Deleting old Interface Records", "PROCESS")
        get_output(mn_del_interfacebl(1))
        na_steps += 1
        log_process(270001, f"{na_steps}- midnite_prog, mn_del_interfacebl, DONE")
        cqueasy("Deleting old Interface Records", "DONE")

        na_steps += 1
        log_process(270001, f"{na_steps}- midnite_prog, deleting old nite store records")
        cqueasy("Deleting old nithist Records", "PROCESS")
        get_output(mn_del_nitehistbl())
        na_steps += 1
        log_process(270001, f"{na_steps}- midnite_prog, mn_del_nitehistbl, DONE")
        cqueasy("Deleting old nithist Records", "DONE")

        if banquet_license:
            na_steps += 1
            log_process(270001, f"{na_steps}- midnite_prog, deleting old banquet reservations")
            cqueasy("Deleted old Banquet Reservations", "PROCESS")
            i = get_output(mn_del_old_baresbl())
            log_process(270001, f"- midnite_prog, mn_del_old_baresbl, DONE {i}")
            cqueasy("Deleted old Banquet Reservations", "DONE")

        na_steps += 1
        log_process(270001, f"{na_steps}- midnite_prog, updating logfile records")
        cqueasy("Updating logfile records", "PROCESS")
        get_output(mn_update_logfile_recordsbl())
        na_steps += 1
        log_process(270001, f"{na_steps}- midnite_prog, mn_update_logfile_recordsbl, DONE")
        cqueasy("Updating logfile records", "DONE")

        na_steps += 1
        log_process(270001, f"{na_steps}- midnite_prog, deleting old F&B compliments")
        cqueasy("Deleting old F&B Compliments", "PROCESS")
        i = get_output(mn_del_oldbl(1))
        log_process(270001, f"- midnite_prog, deleting old F&B compliments, DONE {i}")
        cqueasy("Deleting old F&B Compliments", "DONE")

        na_steps += 1
        log_process(270001, f"{na_steps}- midnite_prog, deleting old work order records")
        cqueasy("Deleting old Work Order Records", "PROCESS")
        i = get_output(mn_del_oldbl(2))
        log_process(270001, f"- midnite_prog, deleting old work order records, DONE {i}")
        cqueasy("Deleting old Work Order Records", "DONE")

        na_steps += 1
        log_process(270001, f"{na_steps}- midnite_prog, deleting old Housekeeping records")
        cqueasy("Deleting old Quotation Attachment Records", "PROCESS")
        i = get_output(mn_del_oldbl(4))
        log_process(270001, f"- midnite_prog, deleting old Housekeeping records, DONE {i}")
        cqueasy("Deleting old Quotation Attachment Records", "DONE")

        na_steps += 1
        log_process(270001, f"{na_steps}- midnite_prog, deleting old mn_club_softwarebl records")
        get_output(mn_club_softwarebl())
        na_steps += 1
        log_process(270001, f"{na_steps}- midnite_prog, club software updates done")    

    def del_allotment():

        nonlocal printer_nr, success_flag, mn_stopped, stop_it, arrival_guest, msg_str, mess_str, crm_license, banquet_license, na_date1, na_time1, na_name1, mnstart_flag, store_flag, billdate, na_date, na_time, na_name, lic_nr, paramtext, queasy
        nonlocal language_code, htparam_recid, user_init, ans_arrguest


        nonlocal na_list, t_nightaudit
        nonlocal na_list_data, t_nightaudit_data


    def decode_string(in_str:string):

        nonlocal printer_nr, success_flag, mn_stopped, stop_it, arrival_guest, msg_str, mess_str, crm_license, banquet_license, na_date1, na_time1, na_name1, mnstart_flag, store_flag, billdate, na_date, na_time, na_name, lic_nr, paramtext, queasy
        nonlocal language_code, htparam_recid, user_init, ans_arrguest


        nonlocal na_list, t_nightaudit
        nonlocal na_list_data, t_nightaudit_data

        out_str = ""
        s:string = ""
        j:int = 0
        len_:int = 0

        def generate_inner_output():
            return (out_str)

        s = in_str
        j = asc(substring(s, 0, 1)) - 70
        len_ = length(in_str) - 1
        s = substring(in_str, 1, len_)
        for len_ in range(1,length(s)  + 1) :
            out_str = out_str + chr_unicode(asc(substring(s, len_ - 1, 1)) - j)

        return generate_inner_output()


    def cqueasy(bezeich:string, str_process:string):

        nonlocal printer_nr, success_flag, mn_stopped, stop_it, arrival_guest, msg_str, mess_str, crm_license, banquet_license, na_date1, na_time1, na_name1, mnstart_flag, store_flag, billdate, na_date, na_time, na_name, lic_nr, paramtext, queasy
        nonlocal language_code, htparam_recid, user_init, ans_arrguest


        nonlocal na_list, t_nightaudit
        nonlocal na_list_data, t_nightaudit_data
        # print(f"cqueasy called with bezeich: {bezeich}, str_process: {str_process}")
        # queasy = get_cache (Queasy, {"key": [(eq, 232)],"char2": [(eq, bezeich)],"date1": [(eq, get_current_date())]})
        queasy = db_session.query(Queasy).filter(
            (Queasy.key == 232) &
            (Queasy.char2 == bezeich) &
            (Queasy.date1 == date.today())
        ).with_for_update().first()

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
            queasy.char3 = str_process

    # paramtext = get_cache (Paramtext, {"txtnr": [(eq, 243)]})
    paramtext = db_session.query(Paramtext).filter(
             (Paramtext.txtnr == 243)).first()
    log_process(270001,"Retrieving license number from Paramtext record 243")
    if paramtext:
        lic_nr = decode_string(paramtext.ptexte)

    # start awal , 232 dikosongkan
    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 232)).order_by(Queasy._recid).all():
        db_session.delete(queasy)

    if ans_arrguest:
        log_process(270001, "Retrieving arrival guest information")
        mn_stopped, stop_it, arrival_guest, msg_str, mess_str, crm_license, banquet_license, na_list_data = get_output(prepare_mn_startbl(2, language_code))

    print("Starting na_start_web2bl,2", mn_stopped)
    log_process(270001, "Starting na_start_web2bl,2")
    if mn_stopped:
        print("MN stopped, exiting NA start")
        log_process(270001, "Stop -> Retrieving arrival guest information")
        pass
    else:
        print("MN continuing NA start")
        log_process(270001, "Starting midnight programs")
        midnite_prog()
        log_process(270001, "Changing system dates")
        get_output(mn_chg_sysdatesbl())
        mnstart_flag, store_flag, printer_nr, t_nightaudit_data, na_date1, na_time1, na_name1 = get_output(na_startbl(2, user_init, htparam_recid))

    print("->NA Programs")
    # for t_nightaudit in t_nightaudit_data:
    #     # log_process(270001, f"List Nightaudit Program: {t_nightaudit.bezeichnung}")
    #     print("Nightaudit Program:", t_nightaudit.bezeichnung)

    log_process(270001, "Starting NA programs")
    na_prog()
    print("<-NA Programs")
    log_process(270001, "Completed NA programs")
    mnstart_flag, store_flag, printer_nr, t_nightaudit_data, na_date, na_time, na_name = get_output(na_startbl(3, user_init, htparam_recid))
    success_flag = True

    # for queasy in db_session.query(Queasy).filter(
    #          (Queasy.key == 232) & (Queasy.date1 == TODAY)).order_by(Queasy._recid).all():


    # for queasy in db_session.query(Queasy).filter(
    #          (Queasy.key == 232) & (Queasy.date1 == date.today())).order_by(Queasy._recid).all():
    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 232) & (Queasy.date1 == get_current_date())).order_by(Queasy._recid).all():
        db_session.delete(queasy)

    log_process(270001, "NA Process: na_start_web2bl, completed successfully")
    return generate_output()