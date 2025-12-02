#using conversion tools version: 1.0.0.117
#------------------------------------------
# Rd, 22/8/2025
# validate fname, gname is ? -> ""
#------------------------------------------
# Rd, 26/11/2025, with_for_update, tidak ada exclusive lock
#-------------------------------------------
from functions.additional_functions import *
from sqlalchemy import func, or_
from decimal import Decimal
from models import Guest, Bill

def read_guestbl(case_type:int, gastno:int, gname:string, fname:string):

    prepare_cache ([Bill])

    t_guest_data = []
    guest = bill = None

    t_guest = None
    
    # Rd, 22/8/2025
    if gname is None:
        gname = ""
    if fname is None:
        fname = ""

    t_guest_data, T_guest = create_model_like(Guest)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_guest_data, guest, bill
        nonlocal case_type, gastno, gname, fname


        nonlocal t_guest
        nonlocal t_guest_data

        return {"t-guest": t_guest_data}

    def delete_procedure():

        nonlocal t_guest_data, guest, bill
        nonlocal case_type, gastno, gname, fname


        nonlocal t_guest
        nonlocal t_guest_data

    if case_type == 1:

        if gastno > 0:

            guest = get_cache (Guest, {"gastnr": [(eq, gastno)]})

        elif gname != "":

            guest = db_session.query(Guest).filter(
                     (Guest.name == (gname).lower()) & (Guest.gastnr > 0)).first()
    elif case_type == 2:

        guest = db_session.query(Guest).filter(
                 (func.lower(Guest.name) == (gname).lower()) & (func.lower(Guest.vorname1 + Guest.anredefirma) == (fname).lower()) & (Guest.gastnr > 0)).first()
    elif case_type == 3:

        if gastno > 0:

            guest = get_cache (Guest, {"gastnr": [(eq, gastno)]})

        elif gname != "":

            guest = db_session.query(Guest).filter(
                     (Guest.name == (gname).lower()) & (Guest.gastnr > 0)).first()
    elif case_type == 4:

        guest = get_cache (Guest, {"name": [(eq, gname)],"vorname1": [(eq, fname)],"gastnr": [(ne, gastno)]})
    elif case_type == 5:

        if fname != "":

            guest = db_session.query(Guest).filter(
                     (func.lower(Guest.name) == (gname).lower()) & (func.lower(Guest.vorname1 + Guest.anredefirma) == (fname).lower()) & (Guest.gastnr > 0)).first()
        else:

            guest = get_cache (Guest, {"name": [(eq, gname)],"gastnr": [(gt, 0)]})
    elif case_type == 6:

        guest = db_session.query(Guest).filter(
                 (func.lower(Guest.name) == (gname).lower()) & (func.lower(Guest.vorname1 + Guest.anredefirma) == (fname).lower()) & (Guest.karteityp == gastno) & (Guest.gastnr > 0)).first()
    elif case_type == 7:

        guest = get_cache (Guest, {"karteityp": [(ge, 1)],"gastnr": [(gt, gastno)],"firmen_nr": [(gt, 0)]})
    elif case_type == 8:

        guest = get_cache (Guest, {"karteityp": [(ge, 1)],"gastnr": [(gt, gastno)],"steuernr": [(ne, "")]})
    elif case_type == 9:

        guest = db_session.query(Guest).filter(
                 (func.lower(Guest.name) == (gname).lower()) | ((func.lower(Guest.name) + ", " + func.lower(Guest.anredefirma)  ) == (gname).lower())).first()
    elif case_type == 10:

        guest = db_session.query(Guest).order_by(Guest._recid.desc()).first()
    elif case_type == 11:

        guest = get_cache (Guest, {"ausweis_nr1": [(eq, gname)],"karteityp": [(eq, 0)],"gastnr": [(gt, 0)]})
    elif case_type == 12:

        guest = get_cache (Guest, {"master_gastnr": [(eq, gastno)],"karteityp": [(eq, 0)],"gastnr": [(gt, 0)]})
    elif case_type == 13:

        guest = get_cache (Guest, {"karteityp": [(eq, 0)]})
    elif case_type == 14:

        guest = get_cache (Guest, {"nation1": [(eq, gname)]})
    elif case_type == 15:

        guest = get_cache (Guest, {"gastnr": [(eq, gastno)],"karteityp": [(gt, 0)]})
    elif case_type == 16:

        bill = get_cache (Bill, {"rechnr": [(eq, gastno)]})

        if not bill:

            return generate_output()

        guest = get_cache (Guest, {"gastnr": [(eq, bill.gastnr)]})
    elif case_type == 17:

        guest = get_cache (Guest, {"karteityp": [(eq, 1)],"name": [(eq, gname)],"gastnr": [(ne, gastno),(gt, 0)]})
    elif case_type == 18:

        guest = get_cache (Guest, {"karteityp": [(eq, 2)],"name": [(eq, gname)],"gastnr": [(ne, gastno),(gt, 0)]})

    if guest:
        t_guest = T_guest()
        t_guest_data.append(t_guest)

        buffer_copy(guest, t_guest)

    return generate_output()