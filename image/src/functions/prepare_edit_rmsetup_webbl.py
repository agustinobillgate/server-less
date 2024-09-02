from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Bk_rset, Bk_raum, Bk_setup

def prepare_edit_rmsetup_webbl(raum:str, curr_select:str, setup_id:int, record_id:int):
    raum_bez = ""
    setup_bez = ""
    bk_list_list = []
    t_bk_raum_list = []
    t_bk_setup_list = []
    bk_rset = bk_raum = bk_setup = None

    bk_list = t_bk_raum = t_bk_setup = None

    bk_list_list, Bk_list = create_model_like(Bk_rset, {"rec_id":int})
    t_bk_raum_list, T_bk_raum = create_model_like(Bk_raum)
    t_bk_setup_list, T_bk_setup = create_model_like(Bk_setup)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal raum_bez, setup_bez, bk_list_list, t_bk_raum_list, t_bk_setup_list, bk_rset, bk_raum, bk_setup


        nonlocal bk_list, t_bk_raum, t_bk_setup
        nonlocal bk_list_list, t_bk_raum_list, t_bk_setup_list
        return {"raum_bez": raum_bez, "setup_bez": setup_bez, "bk-list": bk_list_list, "t-bk-raum": t_bk_raum_list, "t-bk-setup": t_bk_setup_list}

    def fill_bk_list():

        nonlocal raum_bez, setup_bez, bk_list_list, t_bk_raum_list, t_bk_setup_list, bk_rset, bk_raum, bk_setup


        nonlocal bk_list, t_bk_raum, t_bk_setup
        nonlocal bk_list_list, t_bk_raum_list, t_bk_setup_list

        bk_rset = db_session.query(Bk_rset).filter(
                (Bk_rset._recid == record_id)).first()

        bk_raum = db_session.query(Bk_raum).filter(
                (func.lower(Bk_raum.(raum).lower()) == (raum).lower())).first()

        bk_setup = db_session.query(Bk_setup).filter(
                (Bk_setup.setup_id == setup_id)).first()
        raum_bez = bk_raum.bezeich
        setup_bez = bk_setup.bezeich
        bk_list.raum = bk_rset.raum
        bk_list.bezeich = bk_rset.bezeich
        bk_list.groesse = bk_rset.groesse
        bk_list.nebenstelle = bk_rset.nebenstelle
        bk_list.personen = bk_rset.personen
        bk_list.preis = bk_rset.preis
        bk_list.vorbereit = bk_rset.vorbereit
        bk_list.vname = bk_rset.vname
        bk_list.rec_id = bk_rset._recid


    bk_list = Bk_list()
    bk_list_list.append(bk_list)


    if curr_select.lower()  == "chg":
        fill_bk_list()

    for bk_raum in db_session.query(Bk_raum).all():
        t_bk_raum = T_bk_raum()
        t_bk_raum_list.append(t_bk_raum)

        buffer_copy(bk_raum, t_bk_raum)

    for bk_setup in db_session.query(Bk_setup).all():
        t_bk_setup = T_bk_setup()
        t_bk_setup_list.append(t_bk_setup)

        buffer_copy(bk_setup, t_bk_setup)

    return generate_output()