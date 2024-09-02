from functions.additional_functions import *
import decimal
from models import Ba_typ

def batype_admin_btn_delartbl(rec_id:int):
    ba_typ = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal ba_typ


        return {}


    ba_typ = db_session.query(Ba_typ).filter(
            (Ba_typ._recid == rec_id)).first()

    if ba_typ:
        db_session.delete(ba_typ)

    return generate_output()