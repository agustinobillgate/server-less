#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Argt_line, Arrangement, Artikel

def prepare_argtline_admin_webbl(argtno:int):

    prepare_cache ([Artikel])

    t_argt_line_list = []
    t_arrangement_list = []
    argt_line = arrangement = artikel = None

    t_argt_line = t_arrangement = None

    t_argt_line_list, T_argt_line = create_model_like(Argt_line, {"bezeich":string})
    t_arrangement_list, T_arrangement = create_model_like(Arrangement)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_argt_line_list, t_arrangement_list, argt_line, arrangement, artikel
        nonlocal argtno


        nonlocal t_argt_line, t_arrangement
        nonlocal t_argt_line_list, t_arrangement_list

        return {"t-argt-line": t_argt_line_list, "t-arrangement": t_arrangement_list}


    arrangement = get_cache (Arrangement, {"argtnr": [(eq, argtno)]})

    if arrangement:
        t_arrangement = T_arrangement()
        t_arrangement_list.append(t_arrangement)

        buffer_copy(arrangement, t_arrangement)

    for argt_line in db_session.query(Argt_line).filter(
             (Argt_line.argtnr == argtno)).order_by(Argt_line._recid).all():
        t_argt_line = T_argt_line()
        t_argt_line_list.append(t_argt_line)

        buffer_copy(argt_line, t_argt_line)

        artikel = get_cache (Artikel, {"artnr": [(eq, argt_line.argt_artnr)],"departement": [(eq, argt_line.departement)]})

        if artikel:
            t_argt_line.bezeich = artikel.bezeich

    return generate_output()