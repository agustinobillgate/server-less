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
from functions.mn_club_softwarebl import mn_club_softwarebl
from models import Paramtext, Queasy

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

    db_session = local_storage.

    def clear_log(key: int):    
        sql = f"DELETE FROM queasy WHERE key = {key}"
        db_session.execute(text(sql))
        db_session.commit()

    def log_process(key: int, message:string):
        queasy = Queasy()
        db_session.add(queasy)
        queasy.key = key
        queasy.char1 = "Log NA"
        queasy.char2 = message

    def run_program(program_name:string):
        log_process(270001, f"Running program: {program_name}")
        # Placeholder for actual program execution logic

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
            log_process(270001, f"Processing night audit task: {t_nightaudit.bezeichnung}")
            if store_flag:

                if t_nightaudit.hogarest == 0:
                    night_type = 0
                else:
                    night_type = 2

                log_process(270001, f"Deleting nitestor records for night_type {night_type} and reihenfolge {t_nightaudit.reihenfolge}")
                success_flag = get_output(delete_nitestorbl(1, night_type, t_nightaudit.reihenfolge))

            # if matches(t_nightaudit.programm,r"*bl.p*"):
            #     run_program(t_nightaudit.programm.lower())
            # else:

            #     if to_int(t_nightaudit.abschlussart) == 1:
            #         run_program(t_nightaudit.programm.lower())
            #     else:
            #         a = R_INDEX (t_nightaudit.programm, ".p")
            #         run_program(substring(t_nightaudit.programm.lower() , 0, a - 1) + "bl")

            programm = t_nightaudit.programm.lower()
            abschlussart = int(t_nightaudit.abschlussart)

            if "bl.p" in programm:
                log_process(270001, f"Running program bl.p: {programm}")
                # run_program(programm)
            else:
                if abschlussart == 1:
                    log_process(270001, f"Running program, abschlussart=1: {programm}")
                    # run_program(programm)
                else:
                    a = programm.rfind(".p")
                    new_programm = (programm[:a] + "bl.p") if a != -1 else (programm + "bl.p")
                    log_process(270001, f"Running new program .p: {new_programm}")
                    # run_program(new_programm)

            if store_flag:
                log_process(270001, f"Deleting nitehist records for billdate {billdate} and reihenfolge {t_nightaudit.reihenfolge}")
                success_flag = get_output(delete_nitehistbl(1, billdate, t_nightaudit.reihenfolge))
            cqueasy(to_string(t_nightaudit.bezeichnung, "x(40)"), "DONE")
            log_process(270001, f"Completed night audit task: {t_nightaudit.bezeichnung}")


    def midnite_prog():

        nonlocal printer_nr, success_flag, mn_stopped, stop_it, arrival_guest, msg_str, mess_str, crm_license, banquet_license, na_date1, na_time1, na_name1, mnstart_flag, store_flag, billdate, na_date, na_time, na_name, lic_nr, paramtext, queasy
        nonlocal language_code, htparam_recid, user_init, ans_arrguest


        nonlocal na_list, t_nightaudit
        nonlocal na_list_data, t_nightaudit_data

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
        cqueasy("Deleting old DML-Articles", "PROCESS")
        i, j = get_output(mn_del_old_statbl(999))
        cqueasy("Deleting old DML-Articles", "DONE")
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
        cqueasy("Deleting old Quotation Attachment Records", "PROCESS")
        i = get_output(mn_del_oldbl(4))
        cqueasy("Deleting old Quotation Attachment Records", "DONE")
        get_output(mn_club_softwarebl())


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

        queasy = get_cache (Queasy, {"key": [(eq, 232)],"char2": [(eq, bezeich)],"date1": [(eq, get_current_date())]})

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
            pass
            queasy.char3 = str_process


            pass
            pass


    paramtext = get_cache (Paramtext, {"txtnr": [(eq, 243)]})
    log_process(270001,"Retrieving license number from Paramtext record 243")
    if paramtext:
        lic_nr = decode_string(paramtext.ptexte)

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 232)).order_by(Queasy._recid).all():
        log_process(270001, f"Deleting Queasy record: {queasy.char2} - {queasy.char3}")
        db_session.delete(queasy)

    if ans_arrguest:
        log_process(270001, "Retrieving arrival guest information")
        mn_stopped, stop_it, arrival_guest, msg_str, mess_str, crm_license, banquet_license, na_list_data = get_output(prepare_mn_startbl(2, language_code))

    if mn_stopped:
        pass
    else:
        log_process(270001, "Starting midnight programs")
        # midnite_prog()
        log_process(270001, "Changing system dates")
        # get_output(mn_chg_sysdatesbl())
        log_process(270001, "Running NA Programs:na_startbl")
        # mnstart_flag, store_flag, printer_nr, t_nightaudit_data, na_date1, na_time1, na_name1 = get_output(na_startbl(2, user_init, htparam_recid))

    log_process(270001, "Running NA Programs")
    na_prog()
    # mnstart_flag, store_flag, printer_nr, t_nightaudit_data, na_date, na_time, na_name = get_output(na_startbl(3, user_init, htparam_recid))
    success_flag = True

    # for queasy in db_session.query(Queasy).filter(
    #          (Queasy.key == 232) & (Queasy.date1 == TODAY)).order_by(Queasy._recid).all():


    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 232) & (Queasy.date1 == date.today())).order_by(Queasy._recid).all():
        log_process(270001, f"Deleting Queasy record: {queasy.char2} - {queasy.char3}")
        db_session.delete(queasy)

    return generate_output()