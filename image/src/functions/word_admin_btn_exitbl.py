from functions.additional_functions import *
import decimal
from models import Brief

def word_admin_btn_exitbl(b_list:[B_list], case_type:int, kateg:int, rec_id:int):
    brief = None

    b_list = None

    b_list_list, B_list = create_model_like(Brief, {"fname2":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal brief


        nonlocal b_list
        nonlocal b_list_list
        return {}

    def fill_brief():

        nonlocal brief


        nonlocal b_list
        nonlocal b_list_list


        briefnr = b_list.briefnr
        briefbezeich = b_list.briefbezeich
        brief.fname = b_list.fname
        briefkateg = kateg

        if b_list.fname != "":
            brief.fname = brief.fname + ";" + b_list.fname2 + ";"

    b_list = query(b_list_list, first=True)

    if case_type == 1:
        brief = Brief()
        db_session.add(brief)

        fill_brief()

    elif case_type == 2:

        brief = db_session.query(Brief).filter(
                (Brief._recid == rec_id)).first()
        fill_brief()

        brief = db_session.query(Brief).first()

    return generate_output()