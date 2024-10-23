from functions.additional_functions import *
import decimal
from models import Guest, Htparam

def chg_gcf_btn_searchbl(case_type:int, master_gastnr:int):
    progname = ""
    mastername = ""
    gbuff_gastnr = 0
    ext_char:str = ""
    guest = htparam = None

    gbuff = None

    Gbuff = create_buffer("Gbuff",Guest)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal progname, mastername, gbuff_gastnr, ext_char, guest, htparam
        nonlocal case_type, master_gastnr
        nonlocal gbuff


        nonlocal gbuff
        return {"progname": progname, "mastername": mastername, "gbuff_gastnr": gbuff_gastnr}


    if case_type == 0:

        gbuff = db_session.query(Gbuff).filter(
                 (Gbuff.gastnr == master_gastnr)).first()
        mastername = gbuff.name + ", " + gbuff.vorname1 + gbuff.anredefirma + " " + gbuff.anrede1

        return generate_output()

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 148)).first()
    ext_char = htparam.fchar

    gbuff = db_session.query(Gbuff).filter(
             (Gbuff.gastnr == master_gastnr)).first()

    if gbuff:
        gbuff_gastnr = gbuff.gastnr
        progname = "chg-gcf" + ext_char + to_string(gbuff.karteityp) + "UI.p"
        mastername = gbuff.name + ", " + gbuff.vorname1 + gbuff.anredefirma + " " + gbuff.anrede1

    return generate_output()