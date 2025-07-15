#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Bk_rart

def main_fs_proc_btn_help6_2bl(fsl_veran_nr:int, fsl_veran_seite:int, zwkum_zknr:int):

    prepare_cache ([Bk_rart])

    str = ""
    bk_rart = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal str, bk_rart
        nonlocal fsl_veran_nr, fsl_veran_seite, zwkum_zknr

        return {"str": str}

    def create_p2_str(str:string):

        nonlocal bk_rart
        nonlocal fsl_veran_nr, fsl_veran_seite, zwkum_zknr

        def generate_inner_output():
            return (str)


        if str == "":

            if bk_rart.preis == 0:
                str = to_string(bk_rart.anzahl) + " " + bk_rart.bezeich
            else:
                str = to_string(bk_rart.anzahl) + " " + bk_rart.bezeich + " " + to_string(bk_rart.preis, ">,>>>,>>>")
        else:

            if bk_rart.preis == 0:
                str = str + ", " + to_string(bk_rart.anzahl) + " " + bk_rart.bezeich
            else:
                str = str + ", " + to_string(bk_rart.anzahl) + " " + bk_rart.bezeich + " " + to_string(bk_rart.preis, ">,>>>,>>>")

        return generate_inner_output()

    for bk_rart in db_session.query(Bk_rart).filter(
             (Bk_rart.veran_nr == fsl_veran_nr) & (Bk_rart.veran_seite == fsl_veran_seite) & (Bk_rart.zwkum == zwkum_zknr)).order_by(Bk_rart._recid).all():
        str = create_p2_str(str)

    return generate_output()