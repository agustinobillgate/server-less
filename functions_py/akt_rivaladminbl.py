#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 27/11/2025, with_for_update added
#-------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import Akt_code

t_akt_code_data, T_akt_code = create_model_like(Akt_code)

def akt_rivaladminbl(pvilanguage:int, case_type:int, t_akt_code_data:[T_akt_code], aktionscode:int, aktiongrup:int, bezeich:string):

    prepare_cache ([Akt_code])

    msg_str = ""
    success_flag = False
    lvcarea:string = "akt-rivaladmin"
    akt_code = None

    t_akt_code = akt_code1 = None

    Akt_code1 = create_buffer("Akt_code1",Akt_code)


    db_session = local_storage.db_session
    bezeich = bezeich.strip()

    def generate_output():
        nonlocal msg_str, success_flag, lvcarea, akt_code
        nonlocal pvilanguage, case_type, aktionscode, aktiongrup, bezeich
        nonlocal akt_code1


        nonlocal t_akt_code, akt_code1

        return {"msg_str": msg_str, "success_flag": success_flag}

    def fill_akt_code():

        nonlocal msg_str, success_flag, lvcarea, akt_code
        nonlocal pvilanguage, case_type, aktionscode, aktiongrup, bezeich
        nonlocal akt_code1


        nonlocal t_akt_code, akt_code1


        akt_code.aktiongrup = 4
        akt_code.aktionscode = t_akt_code.aktionscode
        akt_code.bezeich = t_akt_code.bezeich
        akt_code.bemerkung = t_akt_code.bemerkung


    def validate_it():

        nonlocal msg_str, success_flag, lvcarea, akt_code
        nonlocal pvilanguage, case_type, aktionscode, aktiongrup, bezeich
        nonlocal akt_code1


        nonlocal t_akt_code, akt_code1

        akt_code1 = get_cache (Akt_code, {"bezeich": [(eq, t_akt_code.bezeich)],"aktionscode": [(ne, t_akt_code.aktionscode)]})

        if akt_code1:
            msg_str = msg_str + chr_unicode(2) + "&W" + translateExtended ("Other Competitor Name exists with the same description.", lvcarea, "")

        akt_code1 = get_cache (Akt_code, {"bezeich": [(eq, t_akt_code.bezeich)],"aktionscode": [(ne, t_akt_code.aktionscode)]})

        if akt_code1:
            msg_str = msg_str + chr_unicode(2) + "&W" + translateExtended ("Other Competitor Name exists with the same description.", lvcarea, "")


    t_akt_code = query(t_akt_code_data, first=True)
    validate_it()

    if case_type == 1:
        akt_code = Akt_code()
        db_session.add(akt_code)

        fill_akt_code()
        success_flag = True

    elif case_type == 2:

        # akt_code = get_cache (Akt_code, {"aktiongrup": [(eq, aktiongrup)],"aktionscode": [(eq, aktionscode)],"bezeich": [(eq, bezeich)]})
        akt_code = db_session.query(Akt_code).filter(
                 (Akt_code.aktiongrup == aktiongrup) &
                 (Akt_code.aktionscode == aktionscode) &
                 (Akt_code.bezeich == bezeich)).with_for_update().first()

        if akt_code:
            fill_akt_code()
            success_flag = True
            pass

    return generate_output()