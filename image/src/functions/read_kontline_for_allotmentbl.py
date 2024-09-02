from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Kontline

def read_kontline_for_allotmentbl(case_type:int, gastno:int, kontignr:int, kontcode:str, katnr:int, argt:str, erwachs:int, abreise:date, ankunft:date):
    t_kontline_list = []
    kontline = None

    t_kontline = None

    t_kontline_list, T_kontline = create_model_like(Kontline)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_kontline_list, kontline


        nonlocal t_kontline
        nonlocal t_kontline_list
        return {"t-kontline": t_kontline_list}

    if case_type == 1:

        kontline = db_session.query(Kontline).filter(
                (Kontline.gastnr == gastno) &  (Kontline.kontignr != kontignr) &  (func.lower(Kontline.(kontcode).lower()) == (kontcode).lower()) &  (Kontline.kontstat == 1) &  (((Kontline.zikatnr != katnr)) |  ((Kontline.arrangement != argt)) |  ((Kontline.erwachs != erwachs)))).first()

        if kontline:
            t_kontline = T_kontline()
            t_kontline_list.append(t_kontline)

            buffer_copy(kontline, t_kontline)
    elif case_type == 2:

        kontline = db_session.query(Kontline).filter(
                (Kontline.gastnr == gastno) &  (Kontline.kontignr != kontignr) &  (func.lower(Kontline.(kontcode).lower()) == (kontcode).lower()) &  (Kontline.kontstat == 1) &  (not Kontline.ankunft >= abreise) &  (not Kontline.abreise <= ankunft)).first()

        if kontline:
            t_kontline = T_kontline()
            t_kontline_list.append(t_kontline)

            buffer_copy(kontline, t_kontline)

    return generate_output()