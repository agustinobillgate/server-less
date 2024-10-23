from functions.additional_functions import *
import decimal
from models import Ba_typ

ba_list_list, Ba_list = create_model_like(Ba_typ)

def batype_admin_btn_exitbl(icase:int, rec_id:int, ba_list_list:[Ba_list]):
    ba_typ = None

    ba_list = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal ba_typ
        nonlocal icase, rec_id


        nonlocal ba_list
        nonlocal ba_list_list
        return {}

    def fill_new_ba_typ():

        nonlocal ba_typ
        nonlocal icase, rec_id


        nonlocal ba_list
        nonlocal ba_list_list


        ba_typ.typ_id = ba_list.typ_id
        ba_typ.bezeichnung = ba_list.bezeich


    ba_list = query(ba_list_list, first=True)

    if icase == 1:
        ba_typ = Ba_typ()
        db_session.add(ba_typ)

        fill_new_ba_typ()
    else:

        ba_typ = db_session.query(Ba_typ).filter(
                 (Ba_typ._recid == rec_id)).first()
        ba_typ.bezeichnung = ba_list.bezeich

    return generate_output()