#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Ratecode, Queasy, Prtable, Zimkateg, Arrangement

def ratecode_adm_create_list_1bl(prcode:string, market_nr:int):

    prepare_cache ([Ratecode, Queasy, Prtable, Zimkateg, Arrangement])

    childflag = False
    pr_list_list = []
    ratecode = queasy = prtable = zimkateg = arrangement = None

    pr_list = None

    pr_list_list, Pr_list = create_model("Pr_list", {"cstr":[string,2], "prcode":string, "rmcat":string, "argt":string, "zikatnr":int, "argtnr":int, "i_typ":int, "flag":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal childflag, pr_list_list, ratecode, queasy, prtable, zimkateg, arrangement
        nonlocal prcode, market_nr


        nonlocal pr_list
        nonlocal pr_list_list

        return {"childflag": childflag, "pr-list": pr_list_list}

    def create_list():

        nonlocal childflag, pr_list_list, ratecode, queasy, prtable, zimkateg, arrangement
        nonlocal prcode, market_nr


        nonlocal pr_list
        nonlocal pr_list_list

        i:int = 0
        j:int = 0
        k:int = 0
        argtnr:int = 0
        zikatnr:int = 0
        found1:bool = False
        found2:bool = False
        pr_str:string = ""
        prtable0 = None
        Prtable0 =  create_buffer("Prtable0",Prtable)

        if market_nr > 0:

            prtable0 = get_cache (Prtable, {"marknr": [(eq, market_nr)],"prcode": [(eq, "")]})

            if prtable0:

                prtable = get_cache (Prtable, {"marknr": [(eq, market_nr)],"prcode": [(eq, prcode)]})
                for i in range(1,99 + 1) :

                    if prtable0.zikatnr[i - 1] != 0:

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

                                            elif prtable.product[k - 1] > 100000:
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
                                    pr_list = Pr_list()
                                    pr_list_list.append(pr_list)

                                    pr_list.rmcat = zimkateg.kurzbez
                                    pr_list.argt = arrangement.argt_bez
                                    pr_list.zikatnr = zimkateg.zikatnr
                                    pr_list.argtnr = arrangement.argtnr
                                    pr_list.prcode = prcode
                                    pr_list.i_typ = zimkateg.typ
                                    pr_list.flag = to_int(found1)

    create_list()

    ratecode = get_cache (Ratecode, {"code": [(eq, prcode)]})

    if ratecode:

        queasy = get_cache (Queasy, {"key": [(eq, 2)],"char1": [(eq, ratecode.code)]})

        if queasy:

            if num_entries(queasy.char3, ";") > 2:
                childflag = True

    return generate_output()