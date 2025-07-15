#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Bk_reser

def main_fs_btn_rechnr_chkbl(bk_veran_veran_nr:int):
    avail_reser_buff = False
    bk_reser = None

    reser_buff = None

    Reser_buff = create_buffer("Reser_buff",Bk_reser)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal avail_reser_buff, bk_reser
        nonlocal bk_veran_veran_nr
        nonlocal reser_buff


        nonlocal reser_buff

        return {"avail_reser_buff": avail_reser_buff}


    reser_buff = db_session.query(Reser_buff).filter(
             (Reser_buff.veran_nr == bk_veran_veran_nr) & (Reser_buff.resstatus == 1)).first()

    if not reser_buff:
        avail_reser_buff = True

        return generate_output()

    return generate_output()