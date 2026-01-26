# using conversion tools version: 1.0.0.117
"""_yusufwijasena_14/01/2026

        remark: - update from #Malik Serverless 920 comment
                - fix & optimize query for mathis, fa_grup, fa_artikel
                - fix wrong position query for fa_order
                - deleted func create_artikel()
"""
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Fa_artikel, Fa_order, Fa_grup, Mathis


def prepare_fa_selartlistbl():

    prepare_cache([Fa_grup, Mathis])

    tmp_faartikel_data = []
    fa_artikel = fa_order = fa_grup = mathis = None

    tmp_faartikel = t_faartikel = None

    tmp_faartikel_data, Tmp_faartikel = create_model_like(
        Fa_artikel,
        {
            "name": string,
            "asset": string,
            "datum": date,
            "price": Decimal,
            "bezeich": string,
            "location": string,
            "remark": string
        })
    t_faartikel_data, T_faartikel = create_model_like(Fa_artikel)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal tmp_faartikel_data, fa_artikel, fa_order, fa_grup, mathis
        nonlocal tmp_faartikel, t_faartikel
        nonlocal tmp_faartikel_data, t_faartikel_data

        return {
            "tmp-faartikel": tmp_faartikel_data
        }


    mathis_obj_list = {}

    query_mathis = (
        db_session.query(Mathis, Fa_grup, Fa_artikel)
        .join(Fa_artikel, Fa_artikel.nr == Mathis.nr)
        .join(Fa_grup, Fa_grup.gnr == Fa_artikel.subgrp)
        .filter(
            not_(Fa_artikel.posted),
            Fa_artikel.loeschflag == 0,
            Fa_artikel.next_depn.is_(None),
            Fa_grup.flag == 1
        )
        .order_by(Mathis.name)
    )
    for mathis, fa_grup, fa_artikel in query_mathis.yield_per(100):
        # print(f"[DEBUG] mathis: {mathis.nr} - {mathis.name}")
        # print(f"[DEBUG] fa grup: {fa_grup.bezeich}")
        
        if mathis_obj_list.get(mathis._recid):
            continue
        else:
            mathis_obj_list[mathis._recid] = True
            
        fa_order = db_session.query(Fa_order).filter(
            Fa_order.activeflag == 0,
            Fa_order.fa_nr == fa_artikel.nr
        ).first()
        
        # print(f"[DEBUG] fa artikel: {fa_artikel.nr}")
        
        if not fa_order:    
            tmp_faartikel = Tmp_faartikel()
            tmp_faartikel_data.append(tmp_faartikel)

            buffer_copy(fa_artikel, tmp_faartikel)
            tmp_faartikel.name = mathis.name
            tmp_faartikel.asset = mathis.asset
            tmp_faartikel.datum = mathis.datum
            tmp_faartikel.price = to_decimal(mathis.price)
            tmp_faartikel.location = mathis.location
            tmp_faartikel.remark = mathis.remark
            tmp_faartikel.bezeich = fa_grup.bezeich

        else:
            pass
            # print("[LOG] has fa_order")

    return generate_output()
