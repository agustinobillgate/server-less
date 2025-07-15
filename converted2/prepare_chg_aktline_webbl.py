#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from functions.read_guestbl import read_guestbl
from functions.read_akt_codebl import read_akt_codebl
from models import Akt_line, Akt_code, Guest

def prepare_chg_aktline_webbl(akt_line_gastnr:int, akt_line_aktionscode:int, akt_line_prioritaet:int, akt_line_zeit:int, akt_line_dauer:int, akt_line_bemerk:string):
    lname = ""
    aktion = ""
    prior = ""
    zeit = ""
    dauer = ""
    comment = ""
    t_akt_code_data = []
    akt_line = akt_code = guest = None

    akt_line1 = t_akt_code = t_guest = None

    akt_line1_data, Akt_line1 = create_model_like(Akt_line)
    t_akt_code_data, T_akt_code = create_model_like(Akt_code)
    t_guest_data, T_guest = create_model_like(Guest)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal lname, aktion, prior, zeit, dauer, comment, t_akt_code_data, akt_line, akt_code, guest
        nonlocal akt_line_gastnr, akt_line_aktionscode, akt_line_prioritaet, akt_line_zeit, akt_line_dauer, akt_line_bemerk


        nonlocal akt_line1, t_akt_code, t_guest
        nonlocal akt_line1_data, t_akt_code_data, t_guest_data

        return {"akt_line_gastnr": akt_line_gastnr, "lname": lname, "aktion": aktion, "prior": prior, "zeit": zeit, "dauer": dauer, "comment": comment, "t-akt-code": t_akt_code_data}

    if akt_line_gastnr > 0:
        t_guest_data = get_output(read_guestbl(1, akt_line_gastnr, "", ""))

        t_guest = query(t_guest_data, first=True)

        if t_guest:
            lname = t_guest.name + ", " + t_guest.anredefirma
            akt_line_gastnr = t_guest.gastnr
    t_akt_code_data = get_output(read_akt_codebl(1, "", None))

    t_akt_code = query(t_akt_code_data, filters=(lambda t_akt_code: t_akt_code.aktiongrup == 1 and t_akt_code.aktionscode == akt_line_aktionscode), first=True)

    if t_akt_code:
        aktion = t_akt_code.bezeich

    if akt_line_prioritaet == 1:
        prior = "Low"

    elif akt_line_prioritaet == 2:
        prior = "Medium"

    elif akt_line_prioritaet == 3:
        prior = "High"
    zeit = substring(to_string(akt_line_zeit, "HH:MM") , 0, 2) + substring(to_string(akt_line_zeit, "HH:MM") , 3, 2)
    dauer = substring(to_string(akt_line_dauer, "HH:MM") , 0, 2) + substring(to_string(akt_line_dauer, "HH:MM") , 3, 2)
    comment = akt_line_bemerk

    return generate_output()