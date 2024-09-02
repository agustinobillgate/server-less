from functions.additional_functions import *
import decimal
from models import Argt_line, Arrangement, Artikel

def prepare_argtline_admin_webbl(argtno:int):
    t_argt_line_list = []
    t_arrangement_list = []
    argt_line = arrangement = artikel = None

    t_argt_line = t_arrangement = None

    t_argt_line_list, T_argt_line = create_model_like(Argt_line, {"bezeich":str})
    t_arrangement_list, T_arrangement = create_model_like(Arrangement)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_argt_line_list, t_arrangement_list, argt_line, arrangement, artikel


        nonlocal t_argt_line, t_arrangement
        nonlocal t_argt_line_list, t_arrangement_list
        return {"t-argt-line": t_argt_line_list, "t-arrangement": t_arrangement_list}


    arrangement = db_session.query(Arrangement).filter(
            (Arrangement.argtnr == argtno)).first()

    if arrangement:
        t_arrangement = T_arrangement()
        t_arrangement_list.append(t_arrangement)

        buffer_copy(arrangement, t_arrangement)

    for argt_line in db_session.query(Argt_line).filter(
            (Argt_line.argtnr == argtno)).all():
        t_argt_line = T_argt_line()
        t_argt_line_list.append(t_argt_line)

        buffer_copy(argt_line, t_argt_line)

        artikel = db_session.query(Artikel).filter(
                (Artikel.artnr == argt_line.argt_artnr) &  (Artikel.departement == argt_line.departement)).first()

        if artikel:
            t_argt_line.bezeich = artikel.bezeich

    return generate_output()