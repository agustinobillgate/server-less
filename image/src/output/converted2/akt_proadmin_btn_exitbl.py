from functions.additional_functions import *
import decimal
from models import Akt_code

akt_code_list_list, Akt_code_list = create_model_like(Akt_code)

def akt_proadmin_btn_exitbl(case_type:int, rec_id:int, akt_code_list_list:[Akt_code_list]):
    akt_code = None

    akt_code_list = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal akt_code
        nonlocal case_type, rec_id


        nonlocal akt_code_list
        nonlocal akt_code_list_list
        return {}

    def fill_akt_code():

        nonlocal akt_code
        nonlocal case_type, rec_id


        nonlocal akt_code_list
        nonlocal akt_code_list_list


        akt_code.aktiongrup = 3
        akt_code.aktionscode = akt_code_list.aktionscode
        akt_code.bezeich = akt_code_list.bezeich
        akt_code.bemerkung = akt_code_list.bemerkung


    akt_code_list = query(akt_code_list_list, first=True)

    if case_type == 1:
        akt_code = Akt_code()
        db_session.add(akt_code)

        fill_akt_code()

    elif case_type == 2:

        akt_code = db_session.query(Akt_code).filter(
                 (Akt_code._recid == rec_id)).first()
        fill_akt_code()

    return generate_output()