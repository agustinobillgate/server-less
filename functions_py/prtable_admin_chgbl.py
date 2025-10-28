#using conversion tools version: 1.0.0.117
#------------------------------------------
# Rd, 28/10/2025
# update roomtype, arrangement, tidak masuk
#------------------------------------------

from functions.additional_functions import *
from decimal import Decimal
from models import Prmarket, Queasy, Prtable

margt_list_data, Margt_list = create_model_like(Prmarket)
mrmcat_list_data, Mrmcat_list = create_model_like(Prmarket)

def prtable_admin_chgbl(margt_list_data:[Margt_list], mrmcat_list_data:[Mrmcat_list], market_bezeich:string, fix_rate:bool, curr_sen:bool, s:string, rec_id:int, nr:int):

    prepare_cache ([Prmarket, Queasy, Prtable])

    prmarket = queasy = prtable = None

    margt_list = mrmcat_list = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal prmarket, queasy, prtable
        nonlocal market_bezeich, fix_rate, curr_sen, s, rec_id, nr


        nonlocal margt_list, mrmcat_list

        return {}

    def update_array():

        nonlocal prmarket, queasy, prtable
        nonlocal market_bezeich, fix_rate, curr_sen, s, rec_id, nr
        nonlocal margt_list, mrmcat_list

        i:int = 0

        # prtable = get_cache (Prtable, {"_recid": [(eq, rec_id)]})
        prtable = db_session.query(Prtable).filter(Prtable._recid == rec_id).first()

        if prtable:
            # pass
            # for i in range(1,99 + 1) :
            #     prtable.zikatnr[i - 1] = 0
            #     prtable.argtnr[i - 1] = 0

            # i = 0
            # for mrmcat_list in query(mrmcat_list_data):
            #     print("mrmcat_list.nr=",mrmcat_list.nr)
            #     i = i + 1
            #     prtable.zikatnr[i - 1] = mrmcat_list.nr
            
            # i = 0
            # for margt_list in query(margt_list_data):
            #     print("margt_list.nr=",margt_list.nr)
            #     i = i + 1
            #     prtable.argtnr[i - 1] = margt_list.nr
            # pass
            # pass
            zikat = [0] * 99
            argt = [0] * 99

            for i, mrmcat_list in enumerate(query(mrmcat_list_data)):
                zikat[i] = mrmcat_list.nr

            for i, margt_list in enumerate(query(margt_list_data)):
                argt[i] = margt_list.nr

            prtable.zikatnr = zikat
            prtable.argtnr = argt

            db_session.commit()
        else:
            print("Prtable not found for rec_id=",rec_id)
        
        db_session.commit()

    prmarket = get_cache (Prmarket, {"nr": [(eq, nr)]})

    # print(margt_list_data)
    # print(mrmcat_list_data)


    if prmarket:
        pass
        prmarket.bezeich = market_bezeich
        pass
        pass

        queasy = get_cache (Queasy, {"key": [(eq, 18)],"number1": [(eq, nr)]})

        if queasy:
            pass
            queasy.logi3 = fix_rate

            if curr_sen:
                queasy.char3 = s
            pass
            pass
        update_array()

    return generate_output()