#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Bk_rset

def edit_rmsetup_bezeichbl(bk_list_bezeich:string, bk_list_raum:string):
    avail_bk_rset1 = False
    bk_rset = None

    bk_rset1 = None

    Bk_rset1 = create_buffer("Bk_rset1",Bk_rset)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal avail_bk_rset1, bk_rset
        nonlocal bk_list_bezeich, bk_list_raum
        nonlocal bk_rset1


        nonlocal bk_rset1

        return {"avail_bk_rset1": avail_bk_rset1}


    bk_rset1 = db_session.query(Bk_rset1).filter(
             (Bk_rset1.bezeich == (bk_list_bezeich).lower()) & (Bk_rset1.raum == (bk_list_raum).lower())).first()

    if bk_rset1:
        avail_bk_rset1 = True

    return generate_output()