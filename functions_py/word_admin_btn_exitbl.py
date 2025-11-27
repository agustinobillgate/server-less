#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 27/11/2025, with_for_update added
#-------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import Brief

b_list_data, B_list = create_model_like(Brief, {"fname2":string})

def word_admin_btn_exitbl(b_list_data:[B_list], case_type:int, kateg:int, rec_id:int):

    prepare_cache ([Brief])

    brief = None

    b_list = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal brief
        nonlocal case_type, kateg, rec_id


        nonlocal b_list

        return {}

    def fill_brief():

        nonlocal brief
        nonlocal case_type, kateg, rec_id


        nonlocal b_list


        brief.briefnr = b_list.briefnr
        brief.briefbezeich = b_list.briefbezeich
        brief.fname = b_list.fname
        brief.briefkateg = kateg

        if b_list.fname != "":
            brief.fname = brief.fname + ";" + b_list.fname2 + ";"


    b_list = query(b_list_data, first=True)

    if case_type == 1:
        brief = Brief()
        db_session.add(brief)

        fill_brief()

    elif case_type == 2:

        # brief = get_cache (Brief, {"_recid": [(eq, rec_id)]})
        brief = db_session.query(Brief).filter(
                 (Brief._recid == rec_id)).with_for_update().first()

        if brief:
            fill_brief()
            pass

    return generate_output()