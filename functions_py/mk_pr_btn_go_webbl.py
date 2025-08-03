#using conversion tools version: 1.0.0.117
#----------------------------------------
# Rd 3/8/2025
# if not availble -> return
#----------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import L_order, L_orderhdr, Dml_art, L_artikel

s_list_data, S_list = create_model_like(L_order, {"s_recid":int})

def mk_pr_btn_go_webbl(s_list_data:[S_list], docu_nr:string, rec_id:int, dml_created:bool, t_l_orderhdr_lieferdatum:date, t_l_orderhdr_angebot_lief:int, comments_screen_value:string, dml_grp:int, dml_datum:date):

    prepare_cache ([L_order, L_orderhdr])

    created = False
    pr_nr = ""
    l_order = l_orderhdr = dml_art = l_artikel = None

    s_list = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal created, pr_nr, l_order, l_orderhdr, dml_art, l_artikel
        nonlocal docu_nr, rec_id, dml_created, t_l_orderhdr_lieferdatum, t_l_orderhdr_angebot_lief, comments_screen_value, dml_grp, dml_datum


        nonlocal s_list

        return {"created": created, "pr_nr": pr_nr}

    def del_dml_art():

        nonlocal created, pr_nr, l_order, l_orderhdr, dml_art, l_artikel
        nonlocal docu_nr, rec_id, dml_created, t_l_orderhdr_lieferdatum, t_l_orderhdr_angebot_lief, comments_screen_value, dml_grp, dml_datum


        nonlocal s_list

        dml_art1 = None
        Dml_art1 =  create_buffer("Dml_art1",Dml_art)

        if dml_grp == 0:

            for dml_art in db_session.query(Dml_art).filter(
                     (Dml_art.datum == dml_datum) & (Dml_art.anzahl != 0)).order_by(Dml_art._recid).all():
                db_session.delete(dml_art)

        else:

            dml_art_obj_list = {}
            for dml_art, l_artikel in db_session.query(Dml_art, L_artikel).join(L_artikel,(L_artikel.artnr == Dml_art.artnr) & (L_artikel.zwkum == dml_grp)).filter(
                     (Dml_art.datum == dml_datum) & (Dml_art.anzahl != 0)).order_by(Dml_art._recid).all():
                if dml_art_obj_list.get(dml_art._recid):
                    continue
                else:
                    dml_art_obj_list[dml_art._recid] = True

                dml_art1 = db_session.query(Dml_art1).filter(
                         (Dml_art1._recid == dml_art._recid)).first()
                db_session.delete(dml_art1)

    for s_list in query(s_list_data):
        l_order = L_order()
        db_session.add(l_order)

        l_order.zeit = s_list.zeit
        buffer_copy(s_list, l_order)
        l_order.zeit = get_current_time_in_seconds()


        pass

    l_orderhdr = get_cache (L_orderhdr, {"_recid": [(eq, rec_id)]})
    # Rd 3/8/2025
    # if not avail return
    if l_orderhdr is None:
        return generate_output()
    
    l_orderhdr.lieferdatum = t_l_orderhdr_lieferdatum
    l_orderhdr.lief_fax[2] = comments_screen_value
    l_orderhdr.lief_fax[1] = " ; ; ; "
    l_orderhdr.angebot_lief[0] = t_l_orderhdr_angebot_lief
    created = True
    pr_nr = docu_nr

    if dml_created:
        del_dml_art()

    return generate_output()