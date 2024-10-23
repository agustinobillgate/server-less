from functions.additional_functions import *
import decimal
from models import Res_line

def arl_list_add_keycard1bl(recid_rline:int):
    res_line = None

    rline = None

    Rline = create_buffer("Rline",Res_line)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal res_line
        nonlocal recid_rline
        nonlocal rline


        nonlocal rline
        return {}


    rline = db_session.query(Rline).filter(
             (Rline._recid == recid_rline)).first()

    if rline:
        rline.betrieb_gast = rline.betrieb_gast + 1
        pass

    return generate_output()