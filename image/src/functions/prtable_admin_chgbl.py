from functions.additional_functions import *
import decimal
from models import Prmarket, Queasy, Prtable

def prtable_admin_chgbl(margt_list:[Margt_list], mrmcat_list:[Mrmcat_list], market_bezeich:str, fix_rate:bool, curr_sen:bool, s:str, rec_id:int, nr:int):
    prmarket = queasy = prtable = None

    margt_list = mrmcat_list = None

    margt_list_list, Margt_list = create_model_like(Prmarket)
    mrmcat_list_list, Mrmcat_list = create_model_like(Prmarket)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal prmarket, queasy, prtable


        nonlocal margt_list, mrmcat_list
        nonlocal margt_list_list, mrmcat_list_list
        return {}

    def update_array():

        nonlocal prmarket, queasy, prtable


        nonlocal margt_list, mrmcat_list
        nonlocal margt_list_list, mrmcat_list_list

        i:int = 0

        prtable = db_session.query(Prtable).filter(
                (Prtable._recid == rec_id)).first()
        for i in range(1,99 + 1) :
            prtable.zikatnr[i - 1] = 0
            prtable.argtnr[i - 1] = 0
        i = 0

        for mrmcat_list in query(mrmcat_list_list):
            i = i + 1
            prtable.zikatnr[i - 1] = mrmcat_list.nr
        i = 0

        for margt_list in query(margt_list_list):
            i = i + 1
            prtable.argtnr[i - 1] = margt_list.nr

        prtable = db_session.query(Prtable).first()


    prmarket = db_session.query(Prmarket).filter(
            (Prmarket.nr == nr)).first()
    prmarket.bezeich = market_bezeich

    prmarket = db_session.query(Prmarket).first()

    queasy = db_session.query(Queasy).filter(
                (Queasy.key == 18) &  (Queasy.number1 == nr)).first()
    queasy.logi3 = fix_rate

    if curr_sen:
        queasy.char3 = s

    queasy = db_session.query(Queasy).first()
    update_array()

    return generate_output()