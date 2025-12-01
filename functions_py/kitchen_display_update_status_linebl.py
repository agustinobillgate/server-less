#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 01/12/2025, with_for_update added
#-------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import Queasy

def kitchen_display_update_status_linebl(line_recid:int, status_nr:int):

    prepare_cache ([Queasy])

    ok_flag = False
    save_time1:string = ""
    save_time2:string = ""
    save_time3:string = ""
    orig_char:string = ""
    queasy = None

    q_kds_line = None

    Q_kds_line = create_buffer("Q_kds_line",Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal ok_flag, save_time1, save_time2, save_time3, orig_char, queasy
        nonlocal line_recid, status_nr
        nonlocal q_kds_line


        nonlocal q_kds_line

        return {"ok_flag": ok_flag}


    if status_nr < 0:
        ok_flag = False

        return generate_output()

    if status_nr > 3:
        ok_flag = False

        return generate_output()

    q_kds_line = get_cache (Queasy, {"_recid": [(eq, line_recid)]})

    if q_kds_line:
        q_kds_line.char3 = to_string(status_nr)
        ok_flag = True

        if status_nr == 1:
            save_time1 = to_string(get_current_datetime(), "99/99/9999 HH:MM:SS")

        elif status_nr == 2:
            save_time2 = to_string(get_current_datetime(), "99/99/9999 HH:MM:SS")

        elif status_nr == 3:
            save_time3 = to_string(get_current_datetime(), "99/99/9999 HH:MM:SS")

        # queasy = get_cache (Queasy, {"key": [(eq, 302)],"betriebsnr": [(eq, line_recid)]})
        queasy = db_session.query(Queasy).filter(
                     (Queasy.key == 302) &
                     (Queasy.betriebsnr == line_recid)).with_for_update().first()

        if not queasy:
            queasy = Queasy()
            db_session.add(queasy)

            queasy.key = 302
            queasy.betriebsnr = line_recid
            queasy.char1 = save_time1 + "|" + save_time2 + "|" + save_time3


        else:
            orig_char = queasy.char1

            if save_time1 != "":
                queasy.char1 = save_time1 + "|" + entry(1, orig_char, "|") + "|" + entry(2, orig_char, "|")

            if save_time2 != "":
                queasy.char1 = entry(0, orig_char, "|") + "|" + save_time2 + "|" + entry(2, orig_char, "|")

            if save_time3 != "":
                queasy.char1 = entry(0, orig_char, "|") + "|" + entry(1, orig_char, "|") + "|" + save_time3
    else:
        ok_flag = False

    return generate_output()