#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Ratecode, Queasy

def update_dynaratecode2_create_contrate_listbl(currcode:string, rmtype:string):

    prepare_cache ([Ratecode, Queasy])

    iftask:string = ""
    tokcounter:int = 0
    mestoken:string = ""
    mesvalue:string = ""
    rcode:string = ""
    ratecode_list_list = []
    t_list_list = []
    doit:bool = False
    ratecode = queasy = None

    t_list = ratecode_list = None

    t_list_list, T_list = create_model("T_list", {"mesvalue":string})
    ratecode_list_list, Ratecode_list = create_model("Ratecode_list", {"rcode":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal iftask, tokcounter, mestoken, mesvalue, rcode, ratecode_list_list, t_list_list, doit, ratecode, queasy
        nonlocal currcode, rmtype


        nonlocal t_list, ratecode_list
        nonlocal t_list_list, ratecode_list_list

        return {"ratecode-list": ratecode_list_list, "t-list": t_list_list}


    for ratecode in db_session.query(Ratecode).filter(
             (Ratecode.code == (currcode).lower())).order_by(Ratecode._recid).all():
        iftask = ratecode.char1[4]
        for tokcounter in range(1,num_entries(iftask, ";") - 1 + 1) :
            mestoken = substring(entry(tokcounter - 1, iftask, ";") , 0, 2)
            mesvalue = trim(substring(entry(tokcounter - 1, iftask, ";") , 2))

            if mestoken == "RT":
                rcode = mesvalue

        if rcode.lower()  == (rmtype).lower() :
            doit = True

            queasy = get_cache (Queasy, {"key": [(eq, 264)],"char1": [(eq, mesvalue)]})

            if queasy:
                doit = not queasy.logi1

            if doit:

                ratecode_list = query(ratecode_list_list, filters=(lambda ratecode_list: ratecode_list.rcode == mesvalue), first=True)

                if not ratecode_list:
                    t_list = T_list()
                    t_list_list.append(t_list)

                    t_list.mesvalue = mesvalue


                    ratecode_list = Ratecode_list()
                    ratecode_list_list.append(ratecode_list)

                    ratecode_list.rcode = mesvalue

    return generate_output()