from functions.additional_functions import *
import decimal
from models import Guest

def init_gcf(gastnr:int):
    guest = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal guest
        nonlocal gastnr

        return {}


    guest = db_session.query(Guest).filter(
             (Guest.gastnr == gastnr)).first()
    guest.gastnr = - gastnr
    guest.karteityp = 0
    guest.name = ""
    guest.vorname1 = ""
    guest.anredefirma = ""
    guest.master_gastnr = 0
    guest.nation1 = ""
    guest.land = ""
    guest.char1 = ""
    guest.anlage_datum = get_current_date()
    guest.bemerkung = ""
    guest.anredefirma = ""
    guest.zahlungsart = 0
    guest.adresse1 = ""
    guest.adresse2 = ""
    guest.adresse3 = ""
    guest.anrede1 = ""
    guest.wohnort = ""
    guest.plz = ""
    guest.geburtdatum1 = None
    guest.ausweis_nr1 = ""
    guest.kreditlimit =  to_decimal("0")
    guest.telefon = ""
    guest.fax = ""
    guest.email_adr = ""

    return generate_output()