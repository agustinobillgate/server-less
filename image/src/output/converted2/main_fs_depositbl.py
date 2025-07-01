#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Bk_veran

def main_fs_depositbl(bk_veran_recid:int):
    buf_bkveran_list = []
    bk_veran = None

    buf_bkveran = None

    buf_bkveran_list, Buf_bkveran = create_model_like(Bk_veran)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal buf_bkveran_list, bk_veran
        nonlocal bk_veran_recid


        nonlocal buf_bkveran
        nonlocal buf_bkveran_list

        return {"buf-bkveran": buf_bkveran_list}

    bk_veran = get_cache (Bk_veran, {"_recid": [(eq, bk_veran_recid)]})

    if bk_veran:
        buf_bkveran = Buf_bkveran()
        buf_bkveran_list.append(buf_bkveran)

        buffer_copy(bk_veran, buf_bkveran)

    return generate_output()