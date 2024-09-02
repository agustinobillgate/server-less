from functions.additional_functions import *
import decimal
from models import Fa_kateg

def fa_kategadmin_btn_exitbl(l_list:[L_list], case_type:int, rec_id:int):
    fa_kateg = None

    l_list = None

    l_list_list, L_list = create_model_like(Fa_kateg)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal fa_kateg


        nonlocal l_list
        nonlocal l_list_list
        return {}

    def fill_new_fa_kateg():

        nonlocal fa_kateg


        nonlocal l_list
        nonlocal l_list_list


        fa_kateg.katnr = l_list.katnr
        fa_kateg.bezeich = l_list.bezeich
        fa_kateg.nutzjahr = l_list.nutzjahr
        fa_kateg.rate = l_list.rate

    l_list = query(l_list_list, first=True)

    if case_type == 1:
        fa_kateg = Fa_kateg()
        db_session.add(fa_kateg)

        fill_new_fa_kateg()
    else:

        fa_kateg = db_session.query(Fa_kateg).filter(
                (Fa_kateg._recid == rec_id)).first()

        fa_kateg = db_session.query(Fa_kateg).first()
        fa_kateg.bezeich = l_list.bezeich
        fa_kateg.nutzjahr = l_list.nutzjahr
        fa_kateg.rate = l_list.rate

        fa_kateg = db_session.query(Fa_kateg).first()

    return generate_output()