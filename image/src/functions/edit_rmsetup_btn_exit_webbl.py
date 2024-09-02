from functions.additional_functions import *
import decimal
from models import Bk_rset

def edit_rmsetup_btn_exit_webbl(bk_list:[Bk_list], case_type:int, t_bk_raum_raum:str, t_bk_setup_setup_id:int):
    recid_rset = 0
    bk_rset = None

    bk_list = None

    bk_list_list, Bk_list = create_model_like(Bk_rset, {"rec_id":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal recid_rset, bk_rset


        nonlocal bk_list
        nonlocal bk_list_list
        return {"recid_rset": recid_rset}

    def fill_bk_rset():

        nonlocal recid_rset, bk_rset


        nonlocal bk_list
        nonlocal bk_list_list

        bk_list = query(bk_list_list, first=True)
        bk_rset = Bk_rset()
        db_session.add(bk_rset)

        bk_rset.raum = t_bk_raum_raum
        bk_rset.setup_id = t_bk_setup_setup_id
        bk_rset.bezeich = bk_list.bezeich
        bk_rset.groesse = bk_list.groesse
        bk_rset.nebenstelle = bk_list.nebenstelle
        bk_rset.personen = bk_list.personen
        bk_rset.preis = bk_list.preis
        bk_rset.vorbereit = bk_list.vorbereit
        bk_rset.vname = bk_list.vname

        for bk_rset in db_session.query(Bk_rset).all():
            recid_rset = bk_rset._recid
            break

    def update_bk_rset():

        nonlocal recid_rset, bk_rset


        nonlocal bk_list
        nonlocal bk_list_list

        bk_rset = db_session.query(Bk_rset).filter(
                (Bk_rset._recid == bk_list.rec_id)).first()

        if bk_rset:

            bk_rset = db_session.query(Bk_rset).first()
            bk_rset.raum = t_bk_raum_raum
            bk_rset.setup_id = t_bk_setup_setup_id
            bk_rset.bezeich = bk_list.bezeich
            bk_rset.groesse = bk_list.groesse
            bk_rset.nebenstelle = bk_list.nebenstelle
            bk_rset.personen = bk_list.personen
            bk_rset.preis = bk_list.preis
            bk_rset.vorbereit = bk_list.vorbereit
            bk_rset.vname = bk_list.vname

            bk_rset = db_session.query(Bk_rset).first()

    bk_list = query(bk_list_list, first=True)

    if case_type == 1:
        fill_bk_rset()
    else:
        update_bk_rset()

    return generate_output()