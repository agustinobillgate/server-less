from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Bk_setup, Bk_rset

def select_basetup_create_listbl(room:str):
    bk_list_list = []
    bk_setup = bk_rset = None

    bk_list = None

    bk_list_list, Bk_list = create_model("Bk_list", {"setup_id":int, "bezeich":str, "pax":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal bk_list_list, bk_setup, bk_rset


        nonlocal bk_list
        nonlocal bk_list_list
        return {"bk-list": bk_list_list}

    for bk_setup in db_session.query(Bk_setup).all():
        bk_list = Bk_list()
        bk_list_list.append(bk_list)

        bk_list.setup_id = bk_setup.setup_id
        bk_list.bezeich = bk_setup.bezeichnung

        if room != "":

            bk_rset = db_session.query(Bk_rset).filter(
                    (func.lower(Bk_rset.raum) == (room).lower()) &  (Bk_rset.setup_id == bk_setup.setup_id)).first()

            if bk_rset:
                bk_list.pax = bk_rset.personen

    return generate_output()