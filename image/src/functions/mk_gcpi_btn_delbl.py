from functions.additional_functions import *
import decimal
from models import Gc_pibline

def mk_gcpi_btn_delbl(s_recid:int):
    gc_pibline = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal gc_pibline


        return {}


    gc_pibline = db_session.query(Gc_pibline).filter(
            (gc_PIbline._recid == s_recid)).first()
    db_session.delete(gc_pibline)

    return generate_output()