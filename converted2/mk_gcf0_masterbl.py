from functions.additional_functions import *
import decimal
from models import Guest

def mk_gcf0_masterbl(master_gastnr:int):
    mastername = ""
    guest = None

    guest0 = None

    Guest0 = create_buffer("Guest0",Guest)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal mastername, guest
        nonlocal master_gastnr
        nonlocal guest0


        nonlocal guest0
        return {"mastername": mastername}


    guest0 = db_session.query(Guest0).filter(
             (Guest0.gastnr == master_gastnr)).first()
    mastername = guest0.name + ", " + guest0.vorname1 + guest0.anredefirma + " " + guest0.anrede1

    return generate_output()