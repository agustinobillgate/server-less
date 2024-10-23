from functions.additional_functions import *
import decimal
from models import Fa_lager, Mathis

fa_list_list, Fa_list = create_model_like(Fa_lager)

def fa_storadmin_btn_exitbl(fa_list_list:[Fa_list], case_type:int, rec_id:int):
    fa_lager = mathis = None

    fa_list = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal fa_lager, mathis
        nonlocal case_type, rec_id


        nonlocal fa_list
        nonlocal fa_list_list
        return {}

    def fill_new_fa_lager():

        nonlocal fa_lager, mathis
        nonlocal case_type, rec_id


        nonlocal fa_list
        nonlocal fa_list_list


        fa_lager.lager_nr = fa_list.lager_nr
        fa_lager.bezeich = fa_list.bezeich


    def update_name():

        nonlocal fa_lager, mathis
        nonlocal case_type, rec_id


        nonlocal fa_list
        nonlocal fa_list_list

        mbuff = None
        Mbuff =  create_buffer("Mbuff",Mathis)

        if fa_lager.bezeich == fa_list.bezeich:

            return

        mathis = db_session.query(Mathis).filter(
                     (Mathis.location == fa_lager.bezeich)).first()
        while None != mathis:

            mbuff = db_session.query(Mbuff).filter(
                         (Mbuff._recid == mathis._recid)).first()
            mbuff.location = fa_list.bezeich

            curr_recid = mathis._recid
            mathis = db_session.query(Mathis).filter(
                         (Mathis.location == fa_lager.bezeich)).filter(Mathis._recid > curr_recid).first()
        fa_lager.bezeich = fa_list.bezeich

    fa_list = query(fa_list_list, first=True)

    if case_type == 1:
        fa_lager = Fa_lager()
        db_session.add(fa_lager)

        fill_new_fa_lager()
    else:

        fa_lager = db_session.query(Fa_lager).filter(
                 (Fa_lager._recid == rec_id)).first()
        update_name()

    return generate_output()