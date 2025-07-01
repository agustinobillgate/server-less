#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Fa_lager, Mathis

fa_list_list, Fa_list = create_model_like(Fa_lager)

def fa_storadmin_btn_exitbl(fa_list_list:[Fa_list], case_type:int, rec_id:int):

    prepare_cache ([Fa_lager, Mathis])

    fa_lager = mathis = None

    fa_list = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal fa_lager, mathis
        nonlocal case_type, rec_id


        nonlocal fa_list

        return {}

    def fill_new_fa_lager():

        nonlocal fa_lager, mathis
        nonlocal case_type, rec_id


        nonlocal fa_list


        fa_lager.lager_nr = fa_list.lager_nr
        fa_lager.bezeich = fa_list.bezeich


    def update_name():

        nonlocal fa_lager, mathis
        nonlocal case_type, rec_id


        nonlocal fa_list

        mbuff = None
        Mbuff =  create_buffer("Mbuff",Mathis)

        if fa_lager.bezeich == fa_list.bezeich:

            return

        mathis = get_cache (Mathis, {"location": [(eq, fa_lager.bezeich)]})
        while None != mathis:

            mbuff = get_cache (Mathis, {"_recid": [(eq, mathis._recid)]})
            mbuff.location = fa_list.bezeich


            pass

            curr_recid = mathis._recid
            mathis = db_session.query(Mathis).filter(
                         (Mathis.location == fa_lager.bezeich) & (Mathis._recid > curr_recid)).first()
        pass
        fa_lager.bezeich = fa_list.bezeich


    fa_list = query(fa_list_list, first=True)

    if case_type == 1:
        fa_lager = Fa_lager()
        db_session.add(fa_lager)

        fill_new_fa_lager()
    else:

        fa_lager = get_cache (Fa_lager, {"_recid": [(eq, rec_id)]})
        update_name()
        pass

    return generate_output()