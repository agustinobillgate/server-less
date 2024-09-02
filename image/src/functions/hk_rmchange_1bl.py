from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import History, Res_line, Bediener

def hk_rmchange_1bl(from_date:date, to_date:date):
    local_storage.debugging = local_storage.debugging + ",FD:" + str(from_date) + ",TD2:" + str(to_date)
    h_list_list = []
    s1:str = ""
    s2:str = ""
    s3:str = ""
    user_init:str = ""
    history = res_line = bediener = None

    h_list = None

    h_list_list, H_list = create_model_like(History, {"chgdate":str, "tzinr":str, "reason":str, "usr_id":str, "res_name":str, "abreisezeit1":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal h_list_list, s1, s2, s3, user_init, history, res_line, bediener
        nonlocal h_list
        nonlocal h_list_list
        return {"h-list": h_list_list}


    h_list_list.clear()
    
    # recs = (
    #     db_session.query(History).filter(
    #         (History.ankunft <= to_date) &  
    #         (History.abreise >= from_date) &  
    #         (History.zi_wechsel) &  
    #         (substring(History.bemerk, 0, 8) >= to_string(from_date)) &  
    #         (substring(History.bemerk, 0, 8) <= to_string(to_date))
    #         ).all()
    # )
    recs = (
        db_session.query(History).filter(
            (History.ankunft <= to_date) &  
            (History.abreise >= from_date) &  
            (History.zi_wechsel) 
            ).all()
    )
    local_storage.debugging = local_storage.debugging + ",Len:" + str(len(recs)) 
    for history in recs:
        if (
                (substring(history.bemerk, 0, 8) >= to_string(from_date)) &  
                (substring(history.bemerk, 0, 8) <= to_string(to_date))
            ):
            
            local_storage.debugging = local_storage.debugging + ",Bm:" + substring(history.bemerk, 0, 8) 
            res_line = db_session.query(Res_line).filter(
                    (Res_line.resnr == history.resnr)).first()

            bediener = db_session.query(Bediener).filter(
                    (func.lower(Bediener.userinit) == (user_init).lower())).first()
            s1 = entry(0, history.bemerk, chr(10))
            
            if get_index(history.bemerk, chr(10)) > 0:
                s2 = entry(0, entry(1, history.bemerk, chr(10)) , chr(2))
            else:
                s2 = ""

            h_list = H_list()
            h_list_list.append(h_list)

            buffer_copy(history, h_list)
            h_list.reason = s2
            h_list.tzinr = trim(substring(s1, 19))
            h_list.chgdate = substring(history.bemerk, 0, 8)
            h_list.resnr = res_line.resnr
            h_list.reslinnr = res_line.reslinnr
            h_list.abreisezeit1 = res_line.ankzeit
            h_list.res_name = res_line.resname
            usr_id = ""

            if num_entries(history.bemerk, chr(2)) > 1:
                usr_id = entry(1, history.bemerk, chr(2))
        else:
            pass
            # print("Else.")
            # local_storage.debugging = local_storage.debugging + ",ElseBm:" + str(history.bemerk) 

    return generate_output()