from functions.additional_functions import *
import decimal
from functions.clclosingbl import clclosingbl
from models import Htparam

def mn_club_softwarebl():
    htparam = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal htparam


        return {}


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1114)).first()

    if htparam.flogical:
        get_output(clclosingbl())

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 592)).first()

    if htparam.flogical:

        return generate_output()

    htparam = db_session.query(Htparam).first()
    htparam.flogical = True

    htparam = db_session.query(Htparam).first()

    htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 592)).first()
    htparam.fchar = "Midnight Program"
    htparam.fdate = get_current_date()
    htparam.finteger = get_current_time_in_seconds()
    htparam.flogical = False

    htparam = db_session.query(Htparam).first()


    return generate_output()