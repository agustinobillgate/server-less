from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Bk_rset, Bk_raum, Bk_setup

def prepare_select_setupbl(raum:str):
    t_setup_list = []
    bk_rset = bk_raum = bk_setup = None

    t_setup = None

    t_setup_list, T_setup = create_model("T_setup", {"room":str, "setup":str, "maxperson":int, "roomspace":int, "preptime":int, "extention":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_setup_list, bk_rset, bk_raum, bk_setup


        nonlocal t_setup
        nonlocal t_setup_list
        return {"t-setup": t_setup_list}

    for bk_rset in db_session.query(Bk_rset).filter(
            (func.lower(Bk_rset.(raum).lower()) == (raum).lower())).all():

        bk_raum = db_session.query(Bk_raum).filter(
                (Bk_raum.raum == bk_rset.raum)).first()

        if bk_raum:

            bk_setup = db_session.query(Bk_setup).filter(
                    (Bk_setup.setup_id == bk_rset.setup_id)).first()

            if bk_setup:
                t_setup = T_setup()
                t_setup_list.append(t_setup)

                t_setup.room = bk_raum.bezeich
                t_setup.setup = bk_setup.bezeich
                t_setup.maxPerson = bk_rset.personen
                t_setup.roomSpace = bk_rset.groesse
                t_setup.prepTime = bk_rset.vorbereit
                t_setup.extention = bk_rset.nebenstelle

    return generate_output()