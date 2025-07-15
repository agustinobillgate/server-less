#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Fa_artikel, Fa_order, Fa_grup, Mathis

def prepare_fa_selartlistbl():

    prepare_cache ([Fa_grup, Mathis])

    tmp_faartikel_data = []
    fa_artikel = fa_order = fa_grup = mathis = None

    tmp_faartikel = t_faartikel = None

    tmp_faartikel_data, Tmp_faartikel = create_model_like(Fa_artikel, {"name":string, "asset":string, "datum":date, "price":Decimal, "bezeich":string, "location":string, "remark":string})
    t_faartikel_data, T_faartikel = create_model_like(Fa_artikel)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal tmp_faartikel_data, fa_artikel, fa_order, fa_grup, mathis


        nonlocal tmp_faartikel, t_faartikel
        nonlocal tmp_faartikel_data, t_faartikel_data

        return {"tmp-faartikel": tmp_faartikel_data}

    def create_artikel():

        nonlocal tmp_faartikel_data, fa_artikel, fa_order, fa_grup, mathis


        nonlocal tmp_faartikel, t_faartikel
        nonlocal tmp_faartikel_data, t_faartikel_data

        for fa_artikel in db_session.query(Fa_artikel).filter(
                 not_ (Fa_artikel.posted) & (Fa_artikel.loeschflag == 0) & (Fa_artikel.next_depn == None)).order_by(Fa_artikel._recid).all():

            fa_order = get_cache (Fa_order, {"activeflag": [(eq, 0)],"fa_nr": [(eq, fa_artikel.nr)]})

            if fa_order:
                pass
            else:
                t_faartikel = T_faartikel()
                t_faartikel_data.append(t_faartikel)

                buffer_copy(fa_artikel, t_faartikel)

    mathis_obj_list = {}
    for mathis, fa_artikel, fa_order, fa_grup in db_session.query(Mathis, Fa_artikel, Fa_order, Fa_grup).join(Fa_artikel,(Fa_artikel.nr == Mathis.nr) & not_ (Fa_artikel.posted) & (Fa_artikel.loeschflag == 0) & (Fa_artikel.next_depn == None)).join(Fa_order,(Fa_order.activeflag == 0) & (Fa_order.fa_nr == Fa_artikel.nr)).join(Fa_grup,(Fa_grup.gnr == Fa_artikel.subgrp) & (Fa_grup.flag == 1)).order_by(Mathis.name).all():
        if mathis_obj_list.get(mathis._recid):
            continue
        else:
            mathis_obj_list[mathis._recid] = True


        tmp_faartikel = Tmp_faartikel()
        tmp_faartikel_data.append(tmp_faartikel)

        buffer_copy(fa_artikel, tmp_faartikel)
        tmp_faartikel.name = mathis.name
        tmp_faartikel.asset = mathis.asset
        tmp_faartikel.datum = mathis.datum
        tmp_faartikel.price =  to_decimal(mathis.price)
        tmp_faartikel.location = mathis.location
        tmp_faartikel.remark = mathis.remark
        tmp_faartikel.bezeich = fa_grup.bezeich

    return generate_output()