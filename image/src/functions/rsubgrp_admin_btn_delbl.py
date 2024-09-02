from functions.additional_functions import *
import decimal
from models import H_artikel, Wgrpdep

def rsubgrp_admin_btn_delbl(departement:int, zknr:int):
    flag = 0
    h_artikel = wgrpdep = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal flag, h_artikel, wgrpdep


        return {"flag": flag}


    h_artikel = db_session.query(H_artikel).filter(
            (H_artikel.departement == departement) &  (H_artikel.zwkum == zknr)).first()

    if h_artikel:
        flag = 1
    else:

        wgrpdep = db_session.query(Wgrpdep).filter(
                (Wgrpdep.departement == departement) &  (Wgrpdep.zknr == zknr)).first()
        db_session.delete(wgrpdep)


    return generate_output()