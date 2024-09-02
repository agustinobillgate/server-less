from functions.additional_functions import *
import decimal
from models import Paramtext

def footnote_admin_fill_list_webbl():
    foot1 = ""
    foot2 = ""
    foot3 = ""
    paramtext = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal foot1, foot2, foot3, paramtext


        return {"foot1": foot1, "foot2": foot2, "foot3": foot3}

    def fill_list():

        nonlocal foot1, foot2, foot3, paramtext

        paramtext = db_session.query(Paramtext).filter(
                (Paramtext.txtnr == 711)).first()
        if paramtext is not None:
              foot1 = paramtext.ptexte

        paramtext = db_session.query(Paramtext).filter(
                (Paramtext.txtnr == 712)).first()
        if paramtext is not None:
                foot2 = paramtext.ptexte

        paramtext = db_session.query(Paramtext).filter(
                (Paramtext.txtnr == 713)).first()
        if paramtext is not None:
                foot3 = paramtext.ptexte

    fill_list()

    return generate_output()