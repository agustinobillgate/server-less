from functions.additional_functions import *
import decimal
from datetime import date
from models import Fa_artikel, Fa_grup, Mathis, Fa_order

def prepare_fa_selartlistbl():
    tmp_faartikel_list = []
    fa_artikel = fa_grup = mathis = fa_order = None

    tmp_faartikel = t_faartikel = None

    tmp_faartikel_list, Tmp_faartikel = create_model_like(Fa_artikel, {"name":str, "asset":str, "datum":date, "price":decimal, "bezeich":str, "location":str, "remark":str})
    t_faartikel_list, T_faartikel = create_model_like(Fa_artikel)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal tmp_faartikel_list, fa_artikel, fa_grup, mathis, fa_order


        nonlocal tmp_faartikel, t_faartikel
        nonlocal tmp_faartikel_list, t_faartikel_list
        return {"tmp-faartikel": tmp_faartikel_list}

    def create_artikel():

        nonlocal tmp_faartikel_list, fa_artikel, fa_grup, mathis, fa_order


        nonlocal tmp_faartikel, t_faartikel
        nonlocal tmp_faartikel_list, t_faartikel_list

        for fa_artikel in db_session.query(Fa_artikel).filter(
                (not Fa_artikel.posted) &  (Fa_artikel.loeschflag == 0) &  (Fa_artikel.next_depn == None)).all():

            fa_order = db_session.query(Fa_order).filter(
                    (Fa_order.activeflag == 0) &  (Fa_order.fa_nr == fa_artikel.nr)).first()

            if fa_order:
                pass
            else:
                t_faartikel = T_faartikel()
                t_faartikel_list.append(t_faartikel)

                buffer_copy(fa_artikel, t_faartikel)

    create_artikel()

    mathis_obj_list = []
    for mathis, t_faartikel, fa_grup in db_session.query(Mathis, T_faartikel, Fa_grup).join(T_faartikel,(T_faartikel.nr == Mathis.nr) &  (not T_faartikel.posted) &  (T_faartikel.loeschflag == 0) &  (T_faartikel.next_depn == None)).join(Fa_grup,(Fa_grup.gnr == t_faartikel.subgrp) &  (Fa_grup.flag == 1)).all():
        if mathis._recid in mathis_obj_list:
            continue
        else:
            mathis_obj_list.append(mathis._recid)


        tmp_faartikel = Tmp_faartikel()
        tmp_faartikel_list.append(tmp_faartikel)

        buffer_copy(t_faartikel, tmp_faartikel)
        tmp_faartikel.name = mathis.name
        tmp_faartikel.asset = mathis.asset
        tmp_faartikel.datum = mathis.datum
        tmp_faartikel.price = mathis.price
        tmp_faartikel.location = mathis.location
        tmp_faartikel.remark = mathis.remark
        tmp_faartikel.bezeich = fa_grup.bezeich

    return generate_output()