#using conversion tools version: 1.0.0.117
#--------------------------------------------
# Rd, 26/11/2025, with_for_update
#--------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from sqlalchemy import func
from models import Interface

def if_fcs0bl_resend_api(p_resend:int, p_irecid:int):

    prepare_cache ([Interface])

    p_status = ""
    v_count:int = 0
    interface = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal p_status, v_count, interface
        nonlocal p_resend, p_irecid

        return {"p_status": p_status}


    if p_resend == 1:

        # interface = get_cache (Interface, {"_recid": [(eq, p_irecid)]})
        interface = db_session.query(Interface).filter(
            (Interface._recid == p_irecid)).with_for_update().first()

        if interface:

            if interface.key == 38 or matches(interface.nebenstelle,r"*$FCS0$*") and (interface.parameters.lower()  != ("modify").lower()  or (interface.parameters.lower()  == ("modify").lower()  and interface.zinr != "")):
                interface.nebenstelle = ""
                interface.intdate = get_current_date()
                v_count = 1
                p_status = "SUCCESS: Data berhasil di resend"


            else:
                p_status = "ERROR: Data tidak ditemukan"

    elif p_resend == 2:

        for interface in db_session.query(Interface).filter(
                 (Interface.key == 38) & (matches(Interface.nebenstelle,"*$FCS0$*")) & 
                 ((Interface.parameters != ("modify").lower()) | (Interface.parameters == ("modify").lower()) & 
                  (Interface.zinr != ""))).order_by(Interface._recid).with_for_update().all():
            
            interface.nebenstelle = ""
            interface.intdate = get_current_date()
            v_count = v_count + 1

        if v_count > 0:
            p_status = "SUCCESS: " + to_string(v_count) + " data berhasil di resend"
        else:
            p_status = "INFO: Tidak ada data yang perlu di resend"
        return to_string(v_count)

    return generate_output()