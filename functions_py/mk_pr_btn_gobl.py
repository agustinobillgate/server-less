from functions.additional_functions import *
import decimal
from datetime import date
from models import L_order, L_orderhdr, Dml_art, L_artikel
from sqlalchemy.orm.attributes import flag_modified

s_list_list, S_list = create_model_like(L_order, {"s_recid":int})

def mk_pr_btn_gobl(s_list_list:[S_list], docu_nr:str, rec_id:int, dml_created:bool, t_l_orderhdr_lieferdatum:date, t_l_orderhdr_angebot_lief:int, comments_screen_value:str, dml_grp:int, dml_datum:date):
    created = False
    pr_nr = ""
    l_order = l_orderhdr = dml_art = l_artikel = None

    s_list = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal created, pr_nr, l_order, l_orderhdr, dml_art, l_artikel
        nonlocal docu_nr, rec_id, dml_created, t_l_orderhdr_lieferdatum, t_l_orderhdr_angebot_lief, comments_screen_value, dml_grp, dml_datum


        nonlocal s_list
        nonlocal s_list_list
        return {"created": created, "pr_nr": pr_nr}

    def del_dml_art():

        nonlocal created, pr_nr, l_order, l_orderhdr, dml_art, l_artikel
        nonlocal docu_nr, rec_id, dml_created, t_l_orderhdr_lieferdatum, t_l_orderhdr_angebot_lief, comments_screen_value, dml_grp, dml_datum


        nonlocal s_list
        nonlocal s_list_list

        dml_art1 = None
        Dml_art1 =  create_buffer("Dml_art1",Dml_art)

        if dml_grp == 0:

            for dml_art in db_session.query(Dml_art).filter(
                     (Dml_art.datum == dml_datum) & (Dml_art.anzahl != 0)).with_for_update().order_by(Dml_art._recid).all():
                
                db_session.delete(dml_art)

        else:

            dml_art_obj_list = []
            for dml_art, l_artikel in db_session.query(Dml_art, L_artikel).join(L_artikel,(L_artikel.artnr == Dml_art.artnr) & (L_artikel.zwkum == dml_grp)).filter(
                     (Dml_art.datum == dml_datum) & (Dml_art.anzahl != 0)).order_by(Dml_art._recid).all():
                if dml_art._recid in dml_art_obj_list:
                    continue
                else:
                    dml_art_obj_list.append(dml_art._recid)

                dml_art1 = db_session.query(Dml_art1).filter(
                         (Dml_art1._recid == dml_art._recid)).with_for_update().first()
                
                db_session.delete(dml_art1)

    for s_list in query(s_list_list):
        l_order = L_order()
        db_session.add(l_order)

        buffer_copy(s_list, l_order)

    l_orderhdr = db_session.query(L_orderhdr).filter(
             (L_orderhdr._recid == rec_id)).with_for_update().first()
    
    l_orderhdr.lieferdatum = t_l_orderhdr_lieferdatum
    l_orderhdr.lief_fax[2] = comments_screen_value
    l_orderhdr.lief_fax[1] = " ; ; ; "
    l_orderhdr.angebot_lief[0] = t_l_orderhdr_angebot_lief

    flag_modified(l_orderhdr, "lief_fax")
    flag_modified(l_orderhdr, "angebot_lief")

    created = True
    pr_nr = docu_nr

    if dml_created:
        del_dml_art()

    return generate_output()