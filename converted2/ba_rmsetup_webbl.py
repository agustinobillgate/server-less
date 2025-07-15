#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Bk_raum, Bk_setup, Bk_rset

def ba_rmsetup_webbl():

    prepare_cache ([Bk_raum, Bk_setup, Bk_rset])

    bk_list_data = []
    bk_raum = bk_setup = bk_rset = None

    bk_list = None

    bk_list_data, Bk_list = create_model("Bk_list", {"raum":string, "rset_bezeich":string, "raum_bezeich":string, "setup_bezeich":string, "personen":int, "preis":Decimal, "nebenstelle":string, "vorbereit":int, "vname":string, "setup_id":int, "rec_id":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal bk_list_data, bk_raum, bk_setup, bk_rset


        nonlocal bk_list
        nonlocal bk_list_data

        return {"bk-list": bk_list_data}

    bk_rset_obj_list = {}
    bk_rset = Bk_rset()
    bk_raum = Bk_raum()
    bk_setup = Bk_setup()
    for bk_rset.raum, bk_rset.bezeichnung, bk_rset.personen, bk_rset.preis, bk_rset.nebenstelle, bk_rset.vorbereit, bk_rset.vname, bk_rset.setup_id, bk_rset._recid, bk_raum.bezeich, bk_raum._recid, bk_setup.bezeichnung, bk_setup._recid in db_session.query(Bk_rset.raum, Bk_rset.bezeichnung, Bk_rset.personen, Bk_rset.preis, Bk_rset.nebenstelle, Bk_rset.vorbereit, Bk_rset.vname, Bk_rset.setup_id, Bk_rset._recid, Bk_raum.bezeich, Bk_raum._recid, Bk_setup.bezeichnung, Bk_setup._recid).join(Bk_raum,(Bk_raum.raum == Bk_rset.raum)).join(Bk_setup,(Bk_setup.setup_id == Bk_rset.setup_id)).order_by(Bk_rset.raum).all():
        if bk_rset_obj_list.get(bk_rset._recid):
            continue
        else:
            bk_rset_obj_list[bk_rset._recid] = True


        bk_list = Bk_list()
        bk_list_data.append(bk_list)

        bk_list.raum = bk_rset.raum
        bk_list.rset_bezeich = bk_rset.bezeichnung
        bk_list.raum_bezeich = bk_raum.bezeich
        bk_list.setup_bezeich = bk_setup.bezeichnung
        bk_list.personen = bk_rset.personen
        bk_list.preis =  to_decimal(bk_rset.preis)
        bk_list.nebenstelle = bk_rset.nebenstelle
        bk_list.vorbereit = bk_rset.vorbereit
        bk_list.vname = bk_rset.vname
        bk_list.setup_id = bk_rset.setup_id
        bk_list.rec_id = bk_rset._recid

    return generate_output()