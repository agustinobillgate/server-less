# using conversion tools version: 1.0.0.117
"""_yusufwijasena_30/01/2026

        remark: - fix python indentation
                - optimize query

"""
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Mathis, L_lieferant, Htparam, Fa_artikel, Fa_grup


def prepare_fa_stinbl(a_bezeich: string):

    prepare_cache([Htparam, Fa_grup])

    billdate = None
    fa_list_data = []
    lief_list_data = []
    mathis = l_lieferant = htparam = fa_artikel = fa_grup = None

    fa_list = lief_list = None

    fa_list_data, Fa_list = create_model_like(
        Mathis, {
            "bezeich": string
        })
    lief_list_data, Lief_list = create_model_like(L_lieferant)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal billdate, fa_list_data, lief_list_data, mathis, l_lieferant, htparam, fa_artikel, fa_grup
        nonlocal a_bezeich
        nonlocal fa_list, lief_list
        nonlocal fa_list_data, lief_list_data

        return {
            "billdate": billdate,
            "fa-list": fa_list_data,
            "lief-list": lief_list_data
        }

    htparam = get_cache(Htparam, {"paramnr": [(eq, 474)]})
    billdate = htparam.fdate

    mathis_obj_list = {}
    mathis_data = (
        db_session.query(Mathis, Fa_artikel, Fa_grup)
        .join(Fa_artikel, (Fa_artikel.nr == Mathis.nr) & not_(Fa_artikel.posted) & (Fa_artikel.loeschflag == 0) & (Fa_artikel.next_depn == None))
        .join(Fa_grup, (Fa_grup.gnr == Fa_artikel.gnr) & (Fa_grup.flag == 0))
        .filter(Mathis.name >= (a_bezeich).lower())
        .order_by(Mathis._recid)
    )
    for mathis, fa_artikel, fa_grup in mathis_data.yield_per(100):
        if mathis_obj_list.get(mathis._recid):
            continue
        else:
            mathis_obj_list[mathis._recid] = True

        fa_list = Fa_list()
        fa_list_data.append(fa_list)

        buffer_copy(mathis, fa_list)
        fa_list.bezeich = fa_grup.bezeich

    for l_lieferant in db_session.query(L_lieferant).order_by(L_lieferant._recid).yield_per(100):
        lief_list = Lief_list()
        lief_list_data.append(lief_list)

        buffer_copy(l_lieferant, lief_list)

    return generate_output()
