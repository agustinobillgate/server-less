#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy, H_artikel, Wgrpgen

def ts_get_request_text_webbl(article_num:int, dept_num:int):

    prepare_cache ([H_artikel])

    t_queasy_data = []
    art_mgroup:int = 0
    count_i:int = 0
    count_k:int = 0
    param978:string = ""
    str_tmp:string = ""
    curr_tmp:string = ""
    curr_tmp2:string = ""
    queasy = h_artikel = wgrpgen = None

    t_queasy = rest_maingroup = b_queasy = None

    t_queasy_data, T_queasy = create_model_like(Queasy)
    rest_maingroup_data, Rest_maingroup = create_model("Rest_maingroup", {"mg_number":int})

    B_queasy = create_buffer("B_queasy",Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_queasy_data, art_mgroup, count_i, count_k, param978, str_tmp, curr_tmp, curr_tmp2, queasy, h_artikel, wgrpgen
        nonlocal article_num, dept_num
        nonlocal b_queasy


        nonlocal t_queasy, rest_maingroup, b_queasy
        nonlocal t_queasy_data, rest_maingroup_data

        return {"t-queasy": t_queasy_data}


    h_artikel = get_cache (H_artikel, {"artnr": [(eq, article_num)],"departement": [(eq, dept_num)]})

    if h_artikel:

        wgrpgen = get_cache (Wgrpgen, {"eknr": [(eq, h_artikel.endkum)]})

        if wgrpgen:
            art_mgroup = h_artikel.endkum

    queasy = get_cache (Queasy, {"key": [(eq, 12)],"number2": [(eq, art_mgroup)]})

    if queasy:

        for b_queasy in db_session.query(B_queasy).filter(
                 (B_queasy.key == 12) & ((B_queasy.number2 == art_mgroup) | (B_queasy.number2 == 0))).order_by(B_queasy._recid).all():
            t_queasy = T_queasy()
            t_queasy_data.append(t_queasy)

            buffer_copy(b_queasy, t_queasy)
    else:

        for b_queasy in db_session.query(B_queasy).filter(
                 (B_queasy.key == 12) & (B_queasy.number2 == 0)).order_by(B_queasy._recid).all():
            t_queasy = T_queasy()
            t_queasy_data.append(t_queasy)

            buffer_copy(b_queasy, t_queasy)

    return generate_output()