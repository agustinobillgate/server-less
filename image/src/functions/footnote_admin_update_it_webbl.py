from functions.additional_functions import *
import decimal
from models import Paramtext

def footnote_admin_update_it_webbl(foot1:str, foot2:str, foot3:str):
    paramtext = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal paramtext


        return {}

    def update_it():

        nonlocal paramtext

        paramtext = db_session.query(Paramtext).filter(
                (Paramtext.txtnr == 711)).first()
        paramtext.ptexte = foot1

        paramtext = db_session.query(Paramtext).filter(
                (Paramtext.txtnr == 712)).first()
        paramtext.ptexte = foot2

        paramtext = db_session.query(Paramtext).filter(
                (Paramtext.txtnr == 713)).first()
        paramtext.ptexte = foot3

    update_it()

    return generate_output()