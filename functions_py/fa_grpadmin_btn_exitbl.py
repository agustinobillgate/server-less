#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 28/11/2025, with_for_update added
#-------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import Fa_grup

l_list_data, L_list = create_model_like(Fa_grup)

def fa_grpadmin_btn_exitbl(l_list_data:[L_list], case_type:int, rec_id:int):

    prepare_cache ([Fa_grup])

    fa_grup = None

    l_list = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal fa_grup
        nonlocal case_type, rec_id


        nonlocal l_list

        return {}

    def fill_new_fa_grup():

        nonlocal fa_grup
        nonlocal case_type, rec_id


        nonlocal l_list


        fa_grup.gnr = l_list.gnr
        fa_grup.bezeich = l_list.bezeich
        fa_grup.flag = 0


    l_list = query(l_list_data, first=True)

    if case_type == 1:
        fa_grup = Fa_grup()
        db_session.add(fa_grup)

        fill_new_fa_grup()
    else:

        # fa_grup = get_cache (Fa_grup, {"_recid": [(eq, rec_id)]})
        fa_grup = db_session.query(Fa_grup).filter(Fa_grup._recid == rec_id).with_for_update().first()
        fa_grup.bezeich = l_list.bezeich

    return generate_output()