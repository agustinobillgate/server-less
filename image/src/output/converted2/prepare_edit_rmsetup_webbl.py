#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Bk_rset, Bk_raum, Bk_setup

def prepare_edit_rmsetup_webbl(raum:string, curr_select:string, setup_id:int, record_id:int):

    prepare_cache ([Bk_rset])

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
        nonlocal raum, curr_select, setup_id, record_id


        nonlocal bk_list, t_bk_raum, t_bk_setup
        nonlocal bk_list_list, t_bk_raum_list, t_bk_setup_list

        return {"raum_bez": raum_bez, "setup_bez": setup_bez, "bk-list": bk_list_list, "t-bk-raum": t_bk_raum_list, "t-bk-setup": t_bk_setup_list}

    def fill_bk_list():

        nonlocal raum_bez, setup_bez, bk_list_list, t_bk_raum_list, t_bk_setup_list, bk_rset, bk_raum, bk_setup
        nonlocal raum, curr_select, setup_id, record_id


        nonlocal bk_list, t_bk_raum, t_bk_setup
        nonlocal bk_list_list, t_bk_raum_list, t_bk_setup_list

        bk_rset = get_cache (Bk_rset, {"_recid": [(eq, record_id)]})

        bk_raum = get_cache (Bk_raum, {"raum": [(eq, raum)]})

        if bk_raum:

            bk_setup = get_cache (Bk_setup, {"setup_id": [(eq, setup_id)]})
            raum_bez = bk_raum.bezeich
            setup_bez = bk_setup.bezeich
            bk_list.raum = bk_rset.raum
            bk_list.bezeich = bk_rset.bezeich
            bk_list.groesse = bk_rset.groesse
            bk_list.nebenstelle = bk_rset.nebenstelle
            bk_list.personen = bk_rset.personen
            bk_list.preis =  to_decimal(bk_rset.preis)
            bk_list.vorbereit = bk_rset.vorbereit
            bk_list.vname = bk_rset.vname
            bk_list.rec_id = bk_rset._recid

    bk_list = Bk_list()
    bk_list_list.append(bk_list)


    if curr_select.lower()  == ("chg").lower() :
        fill_bk_list()

    for bk_raum in db_session.query(Bk_raum).order_by(Bk_raum._recid).all():
        t_bk_raum = T_bk_raum()
        t_bk_raum_list.append(t_bk_raum)

        buffer_copy(bk_raum, t_bk_raum)

    for bk_setup in db_session.query(Bk_setup).order_by(Bk_setup._recid).all():
        t_bk_setup = T_bk_setup()
        t_bk_setup_list.append(t_bk_setup)

        buffer_copy(bk_setup, t_bk_setup)

    return generate_output()