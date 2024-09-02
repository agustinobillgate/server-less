from functions.additional_functions import *
import decimal
from models import Akt_line

def akt_sales1_btn_del2bl(recid_aktline:int):
    akt_line = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal akt_line


        return {}


    akt_line = db_session.query(Akt_line).filter(
            (Akt_line._recid == recid_aktline)).first()

    akt_line = db_session.query(Akt_line).first()
    db_session.delete(akt_line)

    return generate_output()