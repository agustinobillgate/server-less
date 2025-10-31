#using conversion tools version: 1.0.0.117
#------------------------------------------
# Rd, 30/10/2025
# Flag -> update
#------------------------------------------
#using conversion tools version: 1.0.0.119

from functions.additional_functions import *
from decimal import Decimal
from models import Ratecode, Queasy, Prtable, Zimkateg, Arrangement

def ratecode_adm_create_list_1bl(prcode:string, market_nr:int):

    prepare_cache ([Ratecode, Queasy, Prtable, Zimkateg, Arrangement])

    childflag = False
    pr_list_data = []
    ratecode = queasy = prtable = zimkateg = arrangement = None

    pr_list = None

    pr_list_data, Pr_list = create_model("Pr_list", {"cstr":[string,2], "prcode":string, "rmcat":string, "argt":string, "zikatnr":int, "argtnr":int, "i_typ":int, "flag":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal childflag, pr_list_data, ratecode, queasy, prtable, zimkateg, arrangement
        nonlocal prcode, market_nr


        nonlocal pr_list
        nonlocal pr_list_data

        return {"childflag": childflag, "pr-list": pr_list_data}

    def create_list():

        nonlocal childflag, pr_list_data, ratecode, queasy, prtable, zimkateg, arrangement
        nonlocal prcode, market_nr


        nonlocal pr_list
        nonlocal pr_list_data

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
                                        # batas loop sesuai panjang product array agar tidak IndexError
                                        product_len = len(prtable.product) if prtable and prtable.product else 0
                                        while k <= product_len and not found1 and prtable:
                                            val = prtable.product[k - 1] if k - 1 < product_len else 0

                                            if val > 100000:
                                                # 6 digit atau lebih (format 2 + 4)
                                                pr_str = to_string(val)
                                                zikatnr = to_int(substring(pr_str, 0, 2))
                                                argtnr = to_int(substring(pr_str, 2))
                                                if zikatnr >= 91:
                                                    zikatnr -= 90

                                            elif val > 10000:
                                                # 5 digit (format 2 + 3)
                                                pr_str = to_string(val)
                                                zikatnr = to_int(substring(pr_str, 0, 2))
                                                argtnr = to_int(substring(pr_str, 2))
                                                if zikatnr >= 91:
                                                    zikatnr -= 90

                                            elif val > 0:
                                                # pola "2 digit zikatnr" + "2/3 digit argtnr"
                                                if prtable0.argtnr[j - 1] <= 99:
                                                    zikatnr = int(round((val / 100 - 0.5), 0))
                                                    argtnr = int(val - zikatnr * 100)
                                                else:
                                                    zikatnr = int(round((val / 1000 - 0.5), 0))
                                                    argtnr = int(val - zikatnr * 1000)
                                            else:
                                                # nilai kosong, lewati
                                                k += 1
                                                continue

                                            # jika match, flag ditemukan
                                            if (
                                                zikatnr == prtable0.zikatnr[i - 1]
                                                and argtnr == prtable0.argtnr[j - 1]
                                            ):
                                                found1 = True

                                            k += 1
                                            
                                    pr_list = Pr_list()
                                    pr_list_data.append(pr_list)

                                    pr_list.rmcat = zimkateg.kurzbez
                                    pr_list.argt = arrangement.argt_bez
                                    pr_list.zikatnr = zimkateg.zikatnr
                                    pr_list.argtnr = arrangement.argtnr
                                    pr_list.prcode = prcode
                                    pr_list.i_typ = zimkateg.typ
                                    # print("prcode:", prcode, "rmcat:", pr_list.rmcat, "argt:", pr_list.argt, "zikatnr:", pr_list.zikatnr, "argtnr:", pr_list.argtnr, "i_typ:", pr_list.i_typ, "found1:", found1)
                                    pr_list.flag = to_int(found1)

    create_list()

    ratecode = get_cache (Ratecode, {"code": [(eq, prcode)]})

    if ratecode:

        queasy = get_cache (Queasy, {"key": [(eq, 2)],"char1": [(eq, ratecode.code)]})

        if queasy:

            if num_entries(queasy.char3, ";") > 2:
                childflag = True

    return generate_output()