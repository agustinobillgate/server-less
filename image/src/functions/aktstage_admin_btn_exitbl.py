from functions.additional_functions import *
import decimal
from models import Akt_code

def aktstage_admin_btn_exitbl(case_type:int, rec_id:int, stage_list:[Stage_list]):
    akt_code = None

    stage_list = None

    stage_list_list, Stage_list = create_model_like(Akt_code)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal akt_code


        nonlocal stage_list
        nonlocal stage_list_list
        return {}

    def fill_stage_code():

        nonlocal akt_code


        nonlocal stage_list
        nonlocal stage_list_list


        akt_code.aktiongrup = 2
        akt_code.aktionscode = stage_list.aktionscode
        akt_code.bezeich = stage_list.bezeich
        akt_code.bemerkung = stage_list.bemerkung
        akt_code.wertigkeit = stage_list.wertigkeit

    stage_list = query(stage_list_list, first=True)

    if case_type == 1:
        akt_code = Akt_code()
        db_session.add(akt_code)

        fill_stage_code()

    elif case_type == 2:

        akt_code = db_session.query(Akt_code).filter(
                (Akt_code._recid == rec_id)).first()

        akt_code = db_session.query(Akt_code).first()
        fill_stage_code()

        akt_code = db_session.query(Akt_code).first()

    return generate_output()