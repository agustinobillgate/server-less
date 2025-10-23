#using conversion tools version: 1.0.0.117
# pyright: reportAttributeAccessIssue=false

"""_yusufwijasena_

    TICKET ID:
    ISSUE:  - fix python indentation
            - add type ignore to avoid warning
""" 

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy

email_setup_data, Email_setup = create_model(
    "Email_setup", {
        "from_email":string, 
        "to_email":string, 
        "cc_email":string
        }
    )

def tbase_email_setupbl(email_setup_data:Email_setup):
    prepare_cache ([Queasy])

    queasy = None

    email_setup = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal queasy
        nonlocal email_setup

        return {}

    email_setup = query(email_setup_data, first=True)  # type: ignore email_setup_data masih belum terisi

    if email_setup:
        queasy = get_cache (Queasy, {
            "key": [(eq, 369)],
            "char1": [(eq, "tbase-email")]})

        if not queasy:
            queasy = Queasy()

            queasy.key = 369
            queasy.char1 = "tbase-email"
            queasy.char2 = email_setup.from_email
            
            db_session.add(queasy)

            # if email_setup.to_email != "":
            if email_setup.to_email:
                queasy.char3 = email_setup.to_email

            if email_setup.cc_email:
                queasy.char3 = queasy.char3 + "|" + email_setup.cc_email

        else:
            queasy.char2 = email_setup.from_email

            if email_setup.to_email:
                queasy.char3 = email_setup.to_email

            if email_setup.cc_email:
                queasy.char3 = queasy.char3 + "|" + email_setup.cc_email

    return generate_output()