#using conversion tools version: 1.0.0.117

# ==================================
# Rulita, 27-11-2025
# - Added with_for_update all query 
# ==================================

from functions.additional_functions import *
from decimal import Decimal
from models import Mathis, Fa_artikel

fa_article_list_data, Fa_article_list = create_model("Fa_article_list", {"mathis_number":int, "fa_art_name":string, "fa_art_group":int, "fa_art_subgroup":int, "fa_art_category":int, "fa_art_mark":string, "fa_art_model":string, "fa_art_spec":string, "fa_art_remark":string})

def fa_artlist_mobileview_savebl(v_key:int, fa_article_list_data:[Fa_article_list]):

    prepare_cache ([Mathis, Fa_artikel])

    v_success = False
    v_result = ""
    mathis = fa_artikel = None

    fa_article_list = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal v_success, v_result, mathis, fa_artikel
        nonlocal v_key


        nonlocal fa_article_list

        return {"v_success": v_success, "v_result": v_result}

    fa_article_list = query(fa_article_list_data, first=True)

    if not fa_article_list:
        v_result = "Asset List not found."

        return generate_output()

    mathis = get_cache (Mathis, {"nr": [(eq, fa_article_list.mathis_number)]})

    if not mathis:
        v_result = "Asset not found."

        return generate_output()

    fa_artikel = get_cache (Fa_artikel, {"nr": [(eq, fa_article_list.mathis_number)]})

    if not fa_artikel:
        v_result = "Asset not found."

        return generate_output()

    if v_key == 1:

        # mathis = get_cache (Mathis, {"nr": [(eq, fa_article_list.mathis_number)]})
        mathis = db_session.query(Mathis).filter(
                 (Mathis.nr == fa_article_list.mathis_number)).with_for_update().first()

        if mathis:
            # pass
            mathis.name = fa_article_list.fa_art_name
            mathis.mark = fa_article_list.fa_art_mark
            mathis.model = fa_article_list.fa_art_model
            mathis.spec = fa_article_list.fa_art_spec
            mathis.remark = fa_article_list.fa_art_remark

            db_session.refresh(mathis,with_for_update=True)
            # pass
            # pass

        # fa_artikel = get_cache (Fa_artikel, {"nr": [(eq, fa_article_list.mathis_number)]})
        fa_artikel = db_session.query(Fa_artikel).filter(
                 (Fa_artikel.nr == fa_article_list.mathis_number)).with_for_update().first()

        if fa_artikel:
            # pass
            fa_artikel.gnr = fa_article_list.fa_art_group
            fa_artikel.subgrp = fa_article_list.fa_art_subgroup
            fa_artikel.katnr = fa_article_list.fa_art_category

            db_session.refresh(fa_artikel,with_for_update=True)
            # pass
            # pass
    v_success = True

    return generate_output()
