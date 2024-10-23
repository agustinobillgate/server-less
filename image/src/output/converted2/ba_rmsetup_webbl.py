from functions.additional_functions import *
import decimal
from models import Bk_raum, Bk_setup, Bk_rset

def ba_rmsetup_webbl():
    bk_list_list = []
    bk_raum = bk_setup = bk_rset = None

    bk_list = None

    bk_list_list, Bk_list = create_model("Bk_list", {"raum":str, "rset_bezeich":str, "raum_bezeich":str, "setup_bezeich":str, "personen":int, "preis":decimal, "nebenstelle":str, "vorbereit":int, "vname":str, "setup_id":int, "rec_id":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal bk_list_list, bk_raum, bk_setup, bk_rset


        nonlocal bk_list
        nonlocal bk_list_list
        return {"bk-list": bk_list_list}

    bk_rset_obj_list = []
    for bk_rset, bk_raum, bk_setup in db_session.query(Bk_rset, Bk_raum, Bk_setup).join(Bk_raum,(Bk_raum.raum == Bk_rset.raum)).join(Bk_setup,(Bk_setup.setup_id == Bk_rset.setup_id)).order_by(Bk_rset.raum).all():
        if bk_rset._recid in bk_rset_obj_list:
            continue
        else:
            bk_rset_obj_list.append(bk_rset._recid)


        bk_list = Bk_list()
        bk_list_list.append(bk_list)

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