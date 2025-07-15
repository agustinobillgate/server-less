#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Bk_veran

def main_fs_display_depositbl(veran_nr:int):
    buf_bkveran_data = []
    bk_veran = None

    buf_bkveran = None

    buf_bkveran_data, Buf_bkveran = create_model_like(Bk_veran)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal buf_bkveran_data, bk_veran
        nonlocal veran_nr


        nonlocal buf_bkveran
        nonlocal buf_bkveran_data

        return {"buf-bkveran": buf_bkveran_data}


    buf_bkveran_data.clear()

    bk_veran = get_cache (Bk_veran, {"veran_nr": [(eq, veran_nr)]})

    if bk_veran:
        buf_bkveran = Buf_bkveran()
        buf_bkveran_data.append(buf_bkveran)

        buffer_copy(bk_veran, buf_bkveran)

    return generate_output()