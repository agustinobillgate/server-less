from functions.additional_functions import *
import decimal
from models import Paramtext

def footnote_admin_update_it_webbl(foot1:str, foot2:str, foot3:str):
    paramtext = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal paramtext
        nonlocal foot1, foot2, foot3


        return {}

    def update_it():

        nonlocal paramtext
        nonlocal foot1, foot2, foot3

        paramtext = db_session.query(Paramtext).filter(
                 (Paramtext.txtnr == 711)).first()

        if paramtext:
            paramtext.ptexte = foot1
            pass

        paramtext = db_session.query(Paramtext).filter(
                 (Paramtext.txtnr == 712)).first()

        if paramtext:
            paramtext.ptexte = foot2
            pass

        paramtext = db_session.query(Paramtext).filter(
                 (Paramtext.txtnr == 713)).first()

        if not paramtext:
            paramtext = Paramtext()
            db_session.add(paramtext)

            paramtext.txtnr = 713
            paramtext.ptexte = foot3
        else:
            paramtext.ptexte = foot3
            pass


    update_it()

    return generate_output()