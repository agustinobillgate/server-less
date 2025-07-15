#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Prtable, Queasy, Ratecode, Prmarket, Zimkateg, Arrangement

def bookengine_ratecodepull_ratecode_listbl(prcode:string):

    prepare_cache ([Prtable, Queasy, Ratecode, Prmarket, Zimkateg, Arrangement])

    ratecode_detail_list_data = []
    i:int = 0
    j:int = 0
    k:int = 0
    zikatnr:int = 0
    argtnr:int = 0
    found1:bool = False
    pr_str:string = ""
    curr_id:int = 0
    iftask:string = ""
    tokcounter:int = 0
    mestoken:string = ""
    mesvalue:string = ""
    dyna_flag:bool = False
    prev_prcode:string = ""
    has_contract_rate:bool = False
    cat_flag:bool = False
    roomtype:string = ""
    prtable = queasy = ratecode = prmarket = zimkateg = arrangement = None

    ratecode_detail_list = prtable0 = qsy = rc_check = None

    ratecode_detail_list_data, Ratecode_detail_list = create_model("Ratecode_detail_list", {"id":int, "marknr":int, "rcode":string, "rmtype":string, "argmt":string, "cstr":[string,2], "flag":int})

    Prtable0 = create_buffer("Prtable0",Prtable)
    Qsy = create_buffer("Qsy",Queasy)
    Rc_check = create_buffer("Rc_check",Ratecode)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal ratecode_detail_list_data, i, j, k, zikatnr, argtnr, found1, pr_str, curr_id, iftask, tokcounter, mestoken, mesvalue, dyna_flag, prev_prcode, has_contract_rate, cat_flag, roomtype, prtable, queasy, ratecode, prmarket, zimkateg, arrangement
        nonlocal prcode
        nonlocal prtable0, qsy, rc_check


        nonlocal ratecode_detail_list, prtable0, qsy, rc_check
        nonlocal ratecode_detail_list_data

        return {"ratecode-detail-list": ratecode_detail_list_data}


    prev_prcode = prcode

    queasy = get_cache (Queasy, {"key": [(eq, 152)]})

    if queasy:
        cat_flag = True

    queasy = get_cache (Queasy, {"key": [(eq, 2)],"char1": [(eq, prcode)]})

    if queasy.logi2:
        dyna_flag = True

        ratecode = get_cache (Ratecode, {"code": [(eq, prcode)]})
        iftask = ratecode.char1[4]
        for tokcounter in range(1,num_entries(iftask, ";") - 1 + 1) :
            mestoken = substring(entry(tokcounter - 1, iftask, ";") , 0, 2)
            mesvalue = substring(entry(tokcounter - 1, iftask, ";") , 2)

            if mestoken == "RC":
                prcode = mesvalue

    prtable_obj_list = {}
    prtable = Prtable()
    prmarket = Prmarket()
    prtable0 = Prtable()
    for prtable.product, prtable._recid, prtable.zikatnr, prtable.argtnr, prmarket.nr, prmarket._recid, prtable0.product, prtable0._recid, prtable0.zikatnr, prtable0.argtnr in db_session.query(Prtable.product, Prtable._recid, Prtable.zikatnr, Prtable.argtnr, Prmarket.nr, Prmarket._recid, Prtable0.product, Prtable0._recid, Prtable0.zikatnr, Prtable0.argtnr).join(Prmarket,(Prmarket.nr == Prtable.marknr)).join(Prtable0,(Prtable0.marknr == Prtable.marknr) & (Prtable0.prcode == "")).filter(
             (Prtable.prcode == (prcode).lower())).order_by(Prtable._recid).all():
        if prtable_obj_list.get(prtable._recid):
            continue
        else:
            prtable_obj_list[prtable._recid] = True


        for i in range(1,99 + 1) :

            zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, prtable0.zikatnr[i - 1])]})

            if zimkateg:
                for j in range(1,99 + 1) :

                    if prtable0.argtnr[j - 1] != 0:

                        arrangement = get_cache (Arrangement, {"argtnr": [(eq, prtable0.argtnr[j - 1])]})
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

                            qsy = get_cache (Queasy, {"key": [(eq, 152)],"number1": [(eq, zimkateg.typ)]})

                            if qsy:
                                roomtype = qsy.char1
                        else:
                            roomtype = zimkateg.kurzbez

                        ratecode_detail_list = query(ratecode_detail_list_data, filters=(lambda ratecode_detail_list: ratecode_detail_list.rmtype.lower()  == (roomtype).lower()  and ratecode_detail_list.argmt == arrangement.arrangement and ratecode_detail_list.flag == 1), first=True)

                        if not ratecode_detail_list:
                            has_contract_rate = False

                            rc_check = get_cache (Ratecode, {"code": [(eq, prcode)],"zikatnr": [(eq, prtable0.zikatnr[i - 1])],"argtnr": [(eq, prtable0.argtnr[j - 1])]})

                            if rc_check:
                                has_contract_rate = True

                            if has_contract_rate:
                                ratecode_detail_list = Ratecode_detail_list()
                                ratecode_detail_list_data.append(ratecode_detail_list)

                                ratecode_detail_list.id = curr_id
                                ratecode_detail_list.marknr = prmarket.nr
                                ratecode_detail_list.rcode = prcode
                                ratecode_detail_list.rmtype = roomtype
                                ratecode_detail_list.argmt = arrangement.arrangement
                                ratecode_detail_list.flag = to_int(found1)

                                if dyna_flag:
                                    ratecode_detail_list.rcode = prev_prcode

    for ratecode_detail_list in query(ratecode_detail_list_data, filters=(lambda ratecode_detail_list: ratecode_detail_list.cstr[ratecode_detail_list.flag + 1 - 1] == "")):
        ratecode_detail_list_data.remove(ratecode_detail_list)

    return generate_output()