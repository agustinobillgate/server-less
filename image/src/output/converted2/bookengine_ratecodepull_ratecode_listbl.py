from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Prtable, Queasy, Ratecode, Prmarket, Zimkateg, Arrangement

def bookengine_ratecodepull_ratecode_listbl(prcode:str):
    ratecode_detail_list_list = []
    i:int = 0
    j:int = 0
    k:int = 0
    zikatnr:int = 0
    argtnr:int = 0
    found1:bool = False
    pr_str:str = ""
    curr_id:int = 0
    iftask:str = ""
    tokcounter:int = 0
    mestoken:str = ""
    mesvalue:str = ""
    dyna_flag:bool = False
    prev_prcode:str = ""
    cat_flag:bool = False
    roomtype:str = ""
    prtable = queasy = ratecode = prmarket = zimkateg = arrangement = None

    ratecode_detail_list = prtable0 = qsy = None

    ratecode_detail_list_list, Ratecode_detail_list = create_model("Ratecode_detail_list", {"id":int, "marknr":int, "rcode":str, "rmtype":str, "argmt":str, "cstr":[str,2], "flag":int})

    Prtable0 = create_buffer("Prtable0",Prtable)
    Qsy = create_buffer("Qsy",Queasy)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal ratecode_detail_list_list, i, j, k, zikatnr, argtnr, found1, pr_str, curr_id, iftask, tokcounter, mestoken, mesvalue, dyna_flag, prev_prcode, cat_flag, roomtype, prtable, queasy, ratecode, prmarket, zimkateg, arrangement
        nonlocal prcode
        nonlocal prtable0, qsy


        nonlocal ratecode_detail_list, prtable0, qsy
        nonlocal ratecode_detail_list_list
        return {"ratecode-detail-list": ratecode_detail_list_list}


    prev_prcode = prcode

    queasy = db_session.query(Queasy).filter(
             (Queasy.key == 152)).first()

    if queasy:
        cat_flag = True

    queasy = db_session.query(Queasy).filter(
             (Queasy.key == 2) & (func.lower(Queasy.char1) == (prcode).lower())).first()

    if queasy.logi2:
        dyna_flag = True

        ratecode = db_session.query(Ratecode).filter(
                 (func.lower(Ratecode.code) == (prcode).lower())).first()
        iftask = ratecode.char1[4]
        for tokcounter in range(1,num_entries(iftask, ";") - 1 + 1) :
            mestoken = substring(entry(tokcounter - 1, iftask, ";") , 0, 2)
            mesvalue = substring(entry(tokcounter - 1, iftask, ";") , 2)

            if mestoken == "RC":
                prcode = mesvalue

    prtable_obj_list = []
    for prtable, prmarket, prtable0 in db_session.query(Prtable, Prmarket, Prtable0).join(Prmarket,(Prmarket.nr == Prtable.marknr)).join(Prtable0,(Prtable0.marknr == Prtable.marknr) & (Prtable0.prcode == "")).filter(
             (func.lower(Prtable.prcode) == (prcode).lower())).order_by(Prtable._recid).all():
        if prtable._recid in prtable_obj_list:
            continue
        else:
            prtable_obj_list.append(prtable._recid)


        for i in range(1,99 + 1) :

            zimkateg = db_session.query(Zimkateg).filter(
                     (Zimkateg.zikatnr == prtable0.zikatnr[i - 1)]).first()

            if zimkateg:
                for j in range(1,99 + 1) :

                    if prtable0.argtnr[j - 1] != 0:

                        arrangement = db_session.query(Arrangement).filter(
                                 (Arrangement.argtnr == prtable0.argtnr[j - 1)]).first()
                        found1 = False
                        k = 1

                        if arrangement:
                            while k <= 99 and not found1 and prtable:

                                if prtable.product[k - 1] > 10000:
                                    pr_str = to_string(prtable.product[k - 1])
                                    zikatnr = to_int(substring(pr_str, 0, 2))
                                    argtnr = to_int(substring(pr_str, 2))

                                    if zikatnr >= 91:
                                        zikatnr = zikatnr - 90

                                elif prtable.product[k - 1] > 0 and prtable0.argtnr[j - 1] <= 99:
                                    zikatnr = round((prtable.product[k - 1] / 100 - 0.5) , 0)
                                    argtnr = prtable.product[k - 1] - zikatnr * 100

                                elif prtable.product[k - 1] > 0 and prtable0.argtnr[j - 1] >= 100:
                                    zikatnr = round((prtable.product[k - 1] / 1000 - 0.5) , 0)
                                    argtnr = prtable.product[k - 1] - zikatnr * 1000

                                if zikatnr == prtable0.zikatnr[i - 1] and argtnr == prtable0.argtnr[j - 1]:
                                    found1 = True
                                k = k + 1
                        curr_id = curr_id + 1

                        if cat_flag:

                            qsy = db_session.query(Qsy).filter(
                                     (Qsy.key == 152) & (Qsy.number1 == zimkateg.typ)).first()

                            if qsy:
                                roomtype = qsy.char1
                        else:
                            roomtype = zimkateg.kurzbez

                        ratecode_detail_list = query(ratecode_detail_list_list, filters=(lambda ratecode_detail_list: ratecode_detail_list.rmType.lower()  == (roomtype).lower()  and ratecode_detail_list.argmt == arrangement.arrangement and ratecode_detail_list.flag == 1), first=True)

                        if not ratecode_detail_list:
                            ratecode_detail_list = Ratecode_detail_list()
                            ratecode_detail_list_list.append(ratecode_detail_list)

                            ratecode_detail_list.id = curr_id
                            ratecode_detail_list.marknr = prmarket.nr
                            ratecode_detail_list.rcode = prcode
                            ratecode_detail_list.rmtype = roomtype
                            ratecode_detail_list.argmt = arrangement.arrangement
                            ratecode_detail_list.flag = to_int(found1)

                            if dyna_flag:
                                ratecode_detail_list.rcode = prev_prcode

    for ratecode_detail_list in query(ratecode_detail_list_list, filters=(lambda ratecode_detail_list: ratecode_detail_list.cstr[ratecode_detail_list.flag + 1 - 1] == "")):
        ratecode_detail_list_list.remove(ratecode_detail_list)

    return generate_output()