#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Argt_line, Umsatz, Artikel

def artikel_admin1bl(pvilanguage:int, artno:int, deptno:int, rec_id:int):
    msg_str = ""
    lvcarea:string = "artikel-admin"
    argt_line = umsatz = artikel = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, lvcarea, argt_line, umsatz, artikel
        nonlocal pvilanguage, artno, deptno, rec_id

        return {"msg_str": msg_str}


    argt_line = get_cache (Argt_line, {"argt_artnr": [(eq, artno)],"departement": [(eq, deptno)]})

    if argt_line:
        msg_str = msg_str + chr_unicode(2) + translateExtended ("Arrangement Line exists, deleting not possible.", lvcarea, "")

        return generate_output()

    umsatz = get_cache (Umsatz, {"artnr": [(eq, artno)],"departement": [(eq, deptno)]})

    if umsatz:
        msg_str = msg_str + chr_unicode(2) + translateExtended ("Turnover exists, deleting not possible.", lvcarea, "")

        return generate_output()

    artikel = get_cache (Artikel, {"_recid": [(eq, rec_id)]})
    db_session.delete(artikel)

    return generate_output()