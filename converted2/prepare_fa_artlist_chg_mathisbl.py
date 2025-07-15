#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Mathis, Fa_artikel, Fa_grup, Fa_kateg

def prepare_fa_artlist_chg_mathisbl(recid_mathis:int, recid_fa_artikel:int):

    prepare_cache ([Mathis, Fa_artikel, Fa_grup, Fa_kateg])

    spec = ""
    locate = ""
    curr_location = ""
    curr_gnr = 0
    curr_subgrp = 0
    curr_asset = ""
    fibukonto = ""
    credit_fibu = ""
    debit_fibu = ""
    upgrade_part = False
    grp_bez = ""
    sgrp_bez = ""
    rate = to_decimal("0.0")
    rate_bez = ""
    fa_grup_fibukonto = ""
    fa_grup_credit_fibu = ""
    fa_grup_debit_fibu = ""
    m_list_data = []
    fa_art_data = []
    mathis = fa_artikel = fa_grup = fa_kateg = None

    m_list = fa_art = None

    m_list_data, M_list = create_model_like(Mathis)
    fa_art_data, Fa_art = create_model_like(Fa_artikel)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal spec, locate, curr_location, curr_gnr, curr_subgrp, curr_asset, fibukonto, credit_fibu, debit_fibu, upgrade_part, grp_bez, sgrp_bez, rate, rate_bez, fa_grup_fibukonto, fa_grup_credit_fibu, fa_grup_debit_fibu, m_list_data, fa_art_data, mathis, fa_artikel, fa_grup, fa_kateg
        nonlocal recid_mathis, recid_fa_artikel


        nonlocal m_list, fa_art
        nonlocal m_list_data, fa_art_data

        return {"spec": spec, "locate": locate, "curr_location": curr_location, "curr_gnr": curr_gnr, "curr_subgrp": curr_subgrp, "curr_asset": curr_asset, "fibukonto": fibukonto, "credit_fibu": credit_fibu, "debit_fibu": debit_fibu, "upgrade_part": upgrade_part, "grp_bez": grp_bez, "sgrp_bez": sgrp_bez, "rate": rate, "rate_bez": rate_bez, "fa_grup_fibukonto": fa_grup_fibukonto, "fa_grup_credit_fibu": fa_grup_credit_fibu, "fa_grup_debit_fibu": fa_grup_debit_fibu, "m-list": m_list_data, "fa-art": fa_art_data}

    m_list = M_list()
    m_list_data.append(m_list)

    fa_art = Fa_art()
    fa_art_data.append(fa_art)


    mathis = get_cache (Mathis, {"_recid": [(eq, recid_mathis)]})

    fa_artikel = get_cache (Fa_artikel, {"_recid": [(eq, recid_fa_artikel)]})
    m_list.datum = mathis.datum
    m_list.name = mathis.name
    m_list.supplier = mathis.supplier
    m_list.model = mathis.model
    m_list.mark = mathis.mark
    m_list.asset = mathis.asset
    m_list.price =  to_decimal(mathis.price)
    m_list.remark = mathis.remark
    spec = mathis.spec
    locate = mathis.location
    curr_location = locate
    fa_art.lief_nr = fa_artikel.lief_nr
    fa_art.gnr = fa_artikel.gnr
    fa_art.subgrp = fa_artikel.subgrp
    curr_gnr = fa_artikel.gnr
    curr_subgrp = fa_artikel.subgrp
    curr_asset = mathis.asset
    fa_art.katnr = fa_artikel.katnr
    fa_art.anzahl = fa_artikel.anzahl
    fa_art.warenwert =  to_decimal(fa_artikel.warenwert)
    fa_art.depn_wert =  to_decimal(fa_artikel.depn_wert)
    fa_art.book_wert =  to_decimal(fa_artikel.book_wert)
    fa_art.anz_depn = fa_artikel.anz_depn
    fa_art.next_depn = fa_artikel.next_depn
    fa_art.first_depn = fa_artikel.first_depn
    fa_art.last_depn = fa_artikel.last_depn

    if fa_artikel.fibukonto != "":
        fibukonto = fa_artikel.fibukonto

    if fa_artikel.credit_fibu != "":
        credit_fibu = fa_artikel.credit_fibu

    if fa_artikel.debit_fibu != "":
        debit_fibu = fa_artikel.debit_fibu

    if mathis.flag == 2:
        upgrade_part = True
    else:
        upgrade_part = False

    fa_grup = get_cache (Fa_grup, {"flag": [(eq, 1)],"gnr": [(eq, fa_artikel.subgrp)]})
    fa_grup_fibukonto = fa_grup.fibukonto
    fa_grup_credit_fibu = fa_grup.credit_fibu
    fa_grup_debit_fibu = fa_grup.debit_fibu

    fa_kateg = get_cache (Fa_kateg, {"katnr": [(eq, fa_artikel.katnr)]})

    fa_grup = get_cache (Fa_grup, {"gnr": [(eq, fa_artikel.gnr)],"flag": [(eq, 0)]})
    grp_bez = fa_grup.bezeich

    fa_grup = get_cache (Fa_grup, {"gnr": [(eq, fa_artikel.subgrp)],"flag": [(eq, 1)]})

    if fa_grup:
        sgrp_bez = fa_grup.bezeich
    rate =  to_decimal(fa_kateg.rate)
    rate_bez = to_string(rate) + " %"

    return generate_output()