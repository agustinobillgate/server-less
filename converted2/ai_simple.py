#using conversion tools version: 1.0.0.109

from functions.additional_functions import *


def ai_simple():
    db_session = local_storage.db_session

    def generate_output():
        return {"message": "hello world"}


    return generate_output()