from functions.additional_functions import *
import decimal
from models import Argt_line

def nsargt_admin_btn_cancartbl(rec_id:int):
    argt_line = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal argt_line


        return {}


    argt_line = db_session.query(Argt_line).filter(
            (Argt_line._recid == rec_id)).first()

    argt_line = db_session.query(Argt_line).first()
    db_session.delete(argt_line)

    return generate_output()