#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Kontline

def read_kontline_for_allotmentbl(case_type:int, gastno:int, kontignr:int, kontcode:string, katnr:int, argt:string, erwachs:int, abreise:date, ankunft:date):
    t_kontline_data = []
    kontline = None

    t_kontline = None

    t_kontline_data, T_kontline = create_model_like(Kontline)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_kontline_data, kontline
        nonlocal case_type, gastno, kontignr, kontcode, katnr, argt, erwachs, abreise, ankunft


        nonlocal t_kontline
        nonlocal t_kontline_data

        return {"t-kontline": t_kontline_data}

    if case_type == 1:

        kontline = db_session.query(Kontline).filter(
                 (Kontline.gastnr == gastno) & (Kontline.kontignr != kontignr) & (Kontline.kontcode == (kontcode).lower()) & (Kontline.kontstatus == 1) & (((Kontline.zikatnr != katnr)) | ((Kontline.arrangement != (argt).lower())) | ((Kontline.erwachs != erwachs)))).first()

        if kontline:
            t_kontline = T_kontline()
            t_kontline_data.append(t_kontline)

            buffer_copy(kontline, t_kontline)
    elif case_type == 2:

        kontline = get_cache (Kontline, {"gastnr": [(eq, gastno)],"kontignr": [(ne, kontignr)],"kontcode": [(eq, kontcode)],"kontstatus": [(eq, 1)],"ankunft": [(ge, abreise)],"abreise": [(le, ankunft)]})

        if kontline:
            t_kontline = T_kontline()
            t_kontline_data.append(t_kontline)

            buffer_copy(kontline, t_kontline)

    return generate_output()