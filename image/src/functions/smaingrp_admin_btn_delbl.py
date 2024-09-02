from functions.additional_functions import *
import decimal
from models import L_hauptgrp, L_artikel

def smaingrp_admin_btn_delbl(l_hauptgrp_endkum:int):
    flag = 0
    l_hauptgrp = l_artikel = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal flag, l_hauptgrp, l_artikel


        return {"flag": flag}


    l_hauptgrp = db_session.query(L_hauptgrp).filter(
            (L_hauptgrp.endkum == l_hauptgrp_endkum)).first()

    l_artikel = db_session.query(L_artikel).filter(
            (L_artikel.endkum == l_hauptgrp_endkum)).first()

    if l_artikel:
        flag = 1
    else:

        l_hauptgrp = db_session.query(L_hauptgrp).first()
        db_session.delete(l_hauptgrp)

    return generate_output()