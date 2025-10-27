#using conversion tools version: 1.0.0.117
# pyright: reportAttributeAccessIssue=false

"""_yusufwijasena_

    TICKET ID:
    ISSUE:  - recompile only
            - fix python indentation
            - add type ignore to avoid warning
""" 

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy

def prepare_tbase_email_setupbl():

    prepare_cache ([Queasy])

    email_setup_data = []
    queasy = None

    email_setup = None

    email_setup_data, Email_setup = create_model(
        "Email_setup", {
            "from_email":string, 
            "to_email":string, 
            "cc_email":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal email_setup_data, queasy


        nonlocal email_setup
        nonlocal email_setup_data

        return {
            "email-setup": email_setup_data
        }

    queasy = get_cache (Queasy, {
        "key": [(eq, 369)],
        "char1": [(eq, "tbase-email")]})

    if queasy:
        email_setup = Email_setup()
        email_setup_data.append(email_setup)

        email_setup.from_email = queasy.char2

        # if num_entries(queasy.char3, "|") > 1:
        if int(str(num_entries(queasy.char3, "|"))) > 1:
            email_setup.to_email = entry(0, queasy.char3, "|")
            email_setup.cc_email = entry(1, queasy.char3, "|")


        else:
            email_setup.to_email = queasy.char3

    return generate_output()