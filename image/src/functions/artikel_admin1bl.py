from functions.additional_functions import *
import decimal
from models import Argt_line, Umsatz, Artikel

def artikel_admin1bl(pvilanguage:int, artno:int, deptno:int, rec_id:int):
    msg_str = ""
    lvcarea:str = "artikel_admin"
    argt_line = umsatz = artikel = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, lvcarea, argt_line, umsatz, artikel


        return {"msg_str": msg_str}


    argt_line = db_session.query(Argt_line).filter(
            (Argt_line.argt_artnr == artno) &  (Argt_line.departement == deptno)).first()

    if argt_line:
        msg_str = msg_str + chr(2) + translateExtended ("Arrangement Line exists, deleting not possible.", lvcarea, "")

        return generate_output()

    umsatz = db_session.query(Umsatz).filter(
            (Umsatz.artnr == artno) &  (Umsatz.departement == deptno)).first()

    if umsatz:
        msg_str = msg_str + chr(2) + translateExtended ("Turnover exists, deleting not possible.", lvcarea, "")

        return generate_output()

    artikel = db_session.query(Artikel).filter(
                (Artikel._recid == rec_id)).first()
    db_session.delete(artikel)

    return generate_output()