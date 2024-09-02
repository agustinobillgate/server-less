from functions.additional_functions import *
import decimal
from models import Artikel, Wgrpgen

def rmaingrp_admin_btn_delbl(wgrpgen_eknr:int):
    flag = 0
    artikel = wgrpgen = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal flag, artikel, wgrpgen


        return {"flag": flag}


    artikel = db_session.query(Artikel).filter(
            (Artikel.endkum == wgrpgen_eknr)).first()

    if artikel:
        flag = 1
    else:

        wgrpgen = db_session.query(Wgrpgen).filter(
                (Wgrpgen.eknr == wgrpgen_eknr)).first()

        wgrpgen = db_session.query(Wgrpgen).first()
        db_session.delete(wgrpgen)

    return generate_output()