#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Ba_typ

ba_list_list, Ba_list = create_model_like(Ba_typ)

def batype_admin_btn_exitbl(icase:int, rec_id:int, ba_list_list:[Ba_list]):

    prepare_cache ([Ba_typ])

    ba_typ = None

    ba_list = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal ba_typ
        nonlocal icase, rec_id


        nonlocal ba_list

        return {}

    def fill_new_ba_typ():

        nonlocal ba_typ
        nonlocal icase, rec_id


        nonlocal ba_list


        ba_typ.typ_id = ba_list.typ_id
        ba_typ.bezeichnung = ba_list.bezeich


    ba_list = query(ba_list_list, first=True)

    if icase == 1:
        ba_typ = Ba_typ()
        db_session.add(ba_typ)

        fill_new_ba_typ()
    else:

        ba_typ = get_cache (Ba_typ, {"_recid": [(eq, rec_id)]})
        ba_typ.bezeichnung = ba_list.bezeich
        pass

    return generate_output()