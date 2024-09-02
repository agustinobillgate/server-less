from functions.additional_functions import *
import decimal
from models import Mhis_line

def mhis_line_btn_delbl(rec_id:int):
    mhis_line = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal mhis_line


        return {}


    mhis_line = db_session.query(Mhis_line).filter(
            (Mhis_line._recid == rec_id)).first()
    db_session.delete(mhis_line)

    return generate_output()