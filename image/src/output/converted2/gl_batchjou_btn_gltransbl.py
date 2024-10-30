from functions.additional_functions import *
import decimal
from models import Gl_jouhdr

def gl_batchjou_btn_gltransbl(rec_id:int):
    gl_jouhdr = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal gl_jouhdr
        nonlocal rec_id

        return {}


    gl_jouhdr = db_session.query(Gl_jouhdr).filter(
             (Gl_jouhdr._recid == rec_id)).first()
    gl_jouhdr.batch = False

    return generate_output()