#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Fa_artikel, Fa_grup, Mathis, Fa_order

def prepare_fa_selartlistbl():

    prepare_cache ([Fa_grup, Mathis])

    tmp_faartikel_list = []
    fa_artikel = fa_grup = mathis = fa_order = None

    tmp_faartikel = t_faartikel = None

    tmp_faartikel_list, Tmp_faartikel = create_model_like(Fa_artikel, {"name":string, "asset":string, "datum":date, "price":Decimal, "bezeich":string, "location":string, "remark":string})
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
                 not_ (Fa_artikel.posted) & (Fa_artikel.loeschflag == 0) & (Fa_artikel.next_depn == None)).order_by(Fa_artikel._recid).all():

            fa_order = get_cache (Fa_order, {"activeflag": [(eq, 0)],"fa_nr": [(eq, fa_artikel.nr)]})

            if fa_order:
                pass
            else:
                t_faartikel = T_faartikel()
                t_faartikel_list.append(t_faartikel)

                buffer_copy(fa_artikel, t_faartikel)


    create_artikel()

    mathis_obj_list = {}
    for mathis, fa_grup in db_session.query(Mathis, Fa_grup).join(Fa_grup,(Fa_grup.gnr == t_faartikel.subgrp) & (Fa_grup.flag == 1)).order_by(Mathis.name).all():
        t_faartikel = query(t_faartikel_list, (lambda t_faartikel: t_faartikel.nr == mathis.nr and not t_faartikel.posted and t_faartikel.loeschflag == 0 and t_faartikel.next_depn == None), first=True)
        if not t_faartikel:
            continue

        if mathis_obj_list.get(mathis._recid):
            continue
        else:
            mathis_obj_list[mathis._recid] = True


        tmp_faartikel = Tmp_faartikel()
        tmp_faartikel_list.append(tmp_faartikel)

        buffer_copy(t_faartikel, tmp_faartikel)
        tmp_faartikel.name = mathis.name
        tmp_faartikel.asset = mathis.asset
        tmp_faartikel.datum = mathis.datum
        tmp_faartikel.price =  to_decimal(mathis.price)
        tmp_faartikel.location = mathis.location
        tmp_faartikel.remark = mathis.remark
        tmp_faartikel.bezeich = fa_grup.bezeich

    return generate_output()