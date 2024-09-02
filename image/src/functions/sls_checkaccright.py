from functions.additional_functions import *
import decimal
from models import Htparam, Guest, Bediener

def sls_checkaccright(gastno:int):
    restriction = False
    gcf_restrict:bool = False
    shared: = None
    htparam = guest = bediener = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal restriction, gcf_restrict, shared, htparam, guest, bediener


        return {"restriction": restriction}


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1202)).first()
    gcf_restrict = htparam.flogical

    if not gcf_restrict:

        return generate_output()

    guest = db_session.query(Guest).filter(
            (Guest.gastnr == gastno)).first()

    if not guest:

        return generate_output()

    if guest.phonetik3 == user_init or guest.phonetik3 == "":

        return generate_output()
    else:

        bediener = db_session.query(Bediener).filter(
                (Bediener.userinit == user_init)).first()

        if substring(bediener.permission, 31, 1) < "2":
            restriction = True

    return generate_output()