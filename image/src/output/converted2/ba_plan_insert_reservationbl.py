from functions.additional_functions import *
import decimal
from functions.ba_plan_read_mainresbl import ba_plan_read_mainresbl
from functions.ba_plan_get_guestbl import ba_plan_get_guestbl

def ba_plan_insert_reservationbl(rml_resnr:int):
    mess_result = ""
    insert_flag = False
    main_exist = False
    curr_resnr = 0
    reslinnr = 0
    guest_gastnr = 0
    recid_guest = 0
    guest_full_name = ""
    mainres_gastnr:int = 0
    mainres_veran_nr:int = 0
    mainres_resnr:int = 0
    avail_mainres:bool = False
    avail_guest:bool = False
    gast_karteityp:int = 0


    db_session = local_storage.db_session

    def generate_output():
        nonlocal mess_result, insert_flag, main_exist, curr_resnr, reslinnr, guest_gastnr, recid_guest, guest_full_name, mainres_gastnr, mainres_veran_nr, mainres_resnr, avail_mainres, avail_guest, gast_karteityp
        nonlocal rml_resnr


        return {"mess_result": mess_result, "insert_flag": insert_flag, "main_exist": main_exist, "curr_resnr": curr_resnr, "reslinnr": reslinnr, "guest_gastnr": guest_gastnr, "recid_guest": recid_guest, "guest_full_name": guest_full_name}

    mainres_gastnr, mainres_veran_nr, mainres_resnr, gast_karteityp, avail_mainres = get_output(ba_plan_read_mainresbl(rml_resnr))

    if avail_mainres:
        avail_guest, guest_gastnr, recid_guest, guest_full_name = get_output(ba_plan_get_guestbl(mainres_gastnr))
        insert_flag = True
        main_exist = True
        curr_resnr = mainres_veran_nr
        reslinnr = mainres_resnr
        mess_result = "Get Main Reservation Success"
    else:
        mess_result = "Get Main Reservation Failed"

    return generate_output()