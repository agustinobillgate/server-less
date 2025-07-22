#using conversion tools version: 1.0.0.117
#-----------------------------------------
# Rd, 22/7/2025
# gitlab: 
# 
#-----------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import Bk_raum

def prepare_bartikel_listbl():
    t_bk_raum_data, T_bk_raum = create_model_like(Bk_raum)
    db_session = local_storage.db_session

    def generate_output():
        return {"t-bk-raum": t_bk_raum_data}

    for bk_raum in db_session.query(Bk_raum).order_by(Bk_raum._recid).all():
        t_bk_raum = T_bk_raum()  # Instantiate the buffer before copying
        buffer_copy(bk_raum, t_bk_raum)
        t_bk_raum_data.append(t_bk_raum)

    return generate_output()

# def prepare_bartikel_listbl():
#     t_bk_raum_data = []
#     bk_raum = None

#     # t_bk_raum = None
#     t_bk_raum = T_bk_raum()

#     t_bk_raum_data, T_bk_raum = create_model_like(Bk_raum)

#     db_session = local_storage.db_session

#     def generate_output():
#         nonlocal t_bk_raum_data, bk_raum


#         nonlocal t_bk_raum
#         nonlocal t_bk_raum_data

#         return {"t-bk-raum": t_bk_raum_data}

#     for bk_raum in db_session.query(Bk_raum).order_by(Bk_raum._recid).all():
#         buffer_copy(bk_raum, t_bk_raum)

#     return generate_output()