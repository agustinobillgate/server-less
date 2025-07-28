#using conversion tools version: 1.0.0.117
#-------------------------------------------
# Rd 28/7/2025
# gitlab: 950 
# payload:
# {
#     "request": {
#         "caseType": 3,
#         "tWaehrung": {
#             "t-waehrung": [
#                 {
#                     "waehrungsnr": 17,
#                     "wabkurz": "RRP",
#                     "bezeich": "asd",
#                     "ankauf": "1.000",
#                     "verkauf": "1.000",
#                     "einheit": 1,
#                     "geaendert": "2025-07-28"
#                 }
#             ]
#         },
#         "inputUserkey": "95EE44CBF839764A7690C157AC66C9C902905E01",
#         "inputUsername": "it",
#         "hotel_schema": "qcserverless3"
#     }
# }
# {
#     "request": {
#         "caseType": 1,
#         "tWaehrung": {
#             "t-waehrung": [
#                 {
#                     "waehrungsnr": 17,
#                     "wabkurz": "asd",
#                     "bezeich": "asd",
#                     "ankauf": 1,
#                     "verkauf": 1,
#                     "einheit": 1,
#                     "geaendert": "2025-07-28"
#                 }
#             ]
#         },
#         "inputUserkey": "95EE44CBF839764A7690C157AC66C9C902905E01",
#         "inputUsername": "it",
#         "hotel_schema": "qcserverless3"
#     }
# }
#-------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import Waehrung, Res_line, Artikel, Htparam

t_waehrung_data, T_waehrung = create_model_like(Waehrung)

def write_waehrungbl(case_type:int, t_waehrung_data:[T_waehrung]):

    prepare_cache ([Htparam])

    successflag = False
    useflag:bool = False
    waehrung = res_line = artikel = htparam = None

    t_waehrung = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal successflag, useflag, waehrung, res_line, artikel, htparam
        nonlocal case_type


        nonlocal t_waehrung

        return {"successflag": successflag}

    t_waehrung = query(t_waehrung_data, first=True)

    if not t_waehrung:

        return generate_output()

    if case_type == 1:
        waehrung = Waehrung()
        db_session.add(waehrung)

        buffer_copy(t_waehrung, waehrung)
        pass
        successflag = True
    elif case_type == 2:

        waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, t_waehrung.waehrungsnr)]})

        if waehrung:
            buffer_copy(t_waehrung, waehrung)
            pass
            successflag = True
    elif case_type == 3:

        waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, t_waehrung.waehrungsnr)]})

        if waehrung:

            res_line = get_cache (Res_line, {"betriebsnr": [(eq, waehrung.waehrungsnr)]})
            useflag = None != res_line

            if not useflag:

                artikel = get_cache (Artikel, {"departement": [(lt, 90)],"betriebsnr": [(eq, waehrung.waehrungsnr)]})
                useflag = None != artikel

            if not useflag:

                htparam = get_cache (Htparam, {"paramnr": [(eq, 152)]})

                if htparam.fchar == waehrung.wabkurz:
                    pass
                    htparam.fchar = ""


                    pass
                    pass
                pass
                db_session.delete(waehrung)
                pass
                successflag = True

    return generate_output()