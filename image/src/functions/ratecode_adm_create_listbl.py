from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Prtable, Zimkateg, Arrangement

def ratecode_adm_create_listbl(prcode:str, market_nr:int):
    pr_list_list = []
    prtable = zimkateg = arrangement = None

    pr_list = prtable0 = None

    pr_list_list, Pr_list = create_model("Pr_list", {"cstr":str, "prcode":str, "rmcat":str, "argt":str, "zikatnr":int, "argtnr":int, "i_typ":int, "flag":int})

    Prtable0 = Prtable

    db_session = local_storage.db_session

    def generate_output():
        nonlocal pr_list_list, prtable, zimkateg, arrangement
        nonlocal prtable0


        nonlocal pr_list, prtable0
        nonlocal pr_list_list
        return {"pr-list": pr_list_list}

    def create_list():

        nonlocal pr_list_list, prtable, zimkateg, arrangement
        nonlocal prtable0


        nonlocal pr_list, prtable0
        nonlocal pr_list_list

        i:int = 0
        j:int = 0
        k:int = 0
        argtnr:int = 0
        zikatnr:int = 0
        found1:bool = False
        found2:bool = False
        pr_str:str = ""
        Prtable0 = Prtable

        if market_nr > 0:

            prtable0 = db_session.query(Prtable0).filter(
                    (Prtable0.marknr == market_nr) &  (Prtable0.prcode == "")).first()

            if prtable0:

                prtable = db_session.query(Prtable).filter(
                        (Prtable.marknr == market_nr) &  (func.lower(Prtable.prcode.lower()) == prcode.lower())).first()
                
                for i in range(1,99 + 1) :

                    if prtable0.zikatnr[i - 1] != 0:

                        zimkateg = db_session.query(Zimkateg).filter(
                                (Zimkateg.zikatnr == prtable0.zikatnr[i - 1])).first()

                        if zimkateg:
                            for j in range(1,99 + 1) :

                                if prtable0.argtnr[j - 1] != 0:

                                    arrangement = db_session.query(Arrangement).filter(
                                            (Arrangement.argtnr == prtable0.argtnr[j - 1])).first()
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

    return generate_output()