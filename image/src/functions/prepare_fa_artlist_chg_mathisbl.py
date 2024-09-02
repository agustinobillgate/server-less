from functions.additional_functions import *
import decimal
from models import Mathis, Fa_artikel, Fa_grup, Fa_kateg

def prepare_fa_artlist_chg_mathisbl(recid_mathis:int, recid_fa_artikel:int):
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
    rate = 0
    rate_bez = ""
    fa_grup_fibukonto = ""
    fa_grup_credit_fibu = ""
    fa_grup_debit_fibu = ""
    m_list_list = []
    fa_art_list = []
    mathis = fa_artikel = fa_grup = fa_kateg = None

    m_list = fa_art = None

    m_list_list, M_list = create_model_like(Mathis)
    fa_art_list, Fa_art = create_model_like(Fa_artikel)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal spec, locate, curr_location, curr_gnr, curr_subgrp, curr_asset, fibukonto, credit_fibu, debit_fibu, upgrade_part, grp_bez, sgrp_bez, rate, rate_bez, fa_grup_fibukonto, fa_grup_credit_fibu, fa_grup_debit_fibu, m_list_list, fa_art_list, mathis, fa_artikel, fa_grup, fa_kateg


        nonlocal m_list, fa_art
        nonlocal m_list_list, fa_art_list
        return {"spec": spec, "locate": locate, "curr_location": curr_location, "curr_gnr": curr_gnr, "curr_subgrp": curr_subgrp, "curr_asset": curr_asset, "fibukonto": fibukonto, "credit_fibu": credit_fibu, "debit_fibu": debit_fibu, "upgrade_part": upgrade_part, "grp_bez": grp_bez, "sgrp_bez": sgrp_bez, "rate": rate, "rate_bez": rate_bez, "fa_grup_fibukonto": fa_grup_fibukonto, "fa_grup_credit_fibu": fa_grup_credit_fibu, "fa_grup_debit_fibu": fa_grup_debit_fibu, "m-list": m_list_list, "fa-art": fa_art_list}

    m_list = M_list()
    m_list_list.append(m_list)

    fa_art = Fa_art()
    fa_art_list.append(fa_art)


    mathis = db_session.query(Mathis).filter(
            (Mathis._recid == recid_mathis)).first()

    fa_artikel = db_session.query(Fa_artikel).filter(
            (Fa_artikel._recid == recid_fa_artikel)).first()
    m_list.datum = mathis.datum
    m_list.name = mathis.name
    m_list.supplier = mathis.supplier
    m_list.model = mathis.model
    m_list.mark = mathis.mark
    m_list.asset = mathis.asset
    m_list.price = mathis.price
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
    fa_art.warenwert = fa_artikel.warenwert
    fa_art.depn_wert = fa_artikel.depn_wert
    fa_art.book_wert = fa_artikel.book_wert
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

    fa_grup = db_session.query(Fa_grup).filter(
            (Fa_grup.flag == 1) &  (Fa_grup.gnr == fa_artikel.subgrp)).first()
    fa_grup_fibukonto = fa_grup.fibukonto
    fa_grup_credit_fibu = fa_grup.credit_fibu
    fa_grup_debit_fibu = fa_grup.debit_fibu

    fa_kateg = db_session.query(Fa_kateg).filter(
            (Fa_kateg.katnr == fa_artikel.katnr)).first()

    fa_grup = db_session.query(Fa_grup).filter(
            (Fa_grup.gnr == fa_artikel.gnr) &  (Fa_grup.flag == 0)).first()
    grp_bez = fa_grup.bezeich

    fa_grup = db_session.query(Fa_grup).filter(
            (Fa_grup.gnr == fa_artikel.subgrp) &  (Fa_grup.flag == 1)).first()

    if fa_grup:
        sgrp_bez = fa_grup.bezeich
    rate = fa_kateg.rate
    rate_bez = to_string(rate) + " %"

    return generate_output()