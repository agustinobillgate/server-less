#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from sqlalchemy import func
from models import Queasy

input_list_list, Input_list = create_model("Input_list", {"guestno":int, "first_name":string, "last_name":string, "country":string, "city":string, "segment":string, "keyaccount":string})

def read_keyaccount_webbl(input_list_list:[Input_list]):

    prepare_cache ([Queasy])

    mess_result = ""
    i:int = 0
    keynumber:int = 0
    ans:bool = False
    queasy = None

    input_list = ilist = q212 = None

    Ilist = Input_list
    ilist_list = input_list_list

    Q212 = create_buffer("Q212",Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal mess_result, i, keynumber, ans, queasy
        nonlocal ilist, q212


        nonlocal input_list, ilist, q212

        return {"mess_result": mess_result}

    ilist = query(ilist_list, first=True)

    if ilist:

        for input_list in query(input_list_list, filters=(lambda input_list: input_list.keyaccount != "")):

            queasy = db_session.query(Queasy).filter(
                     (Queasy.key == 211) & (matches(Queasy.char1,("*" + input_list.keyaccount + "*")))).first()

            if queasy:
                i = 1
                keynumber = queasy.number1

                for q212 in db_session.query(Q212).filter(
                         (Q212.key == 212) & (Q212.number1 == keynumber)).order_by(Q212.number2.desc()).yield_per(100):
                    i = q212.number2 + 1

                    if i == 0:
                        i = 1
                    break

                queasy = get_cache (Queasy, {"key": [(eq, 212)],"number3": [(eq, input_list.guestno)]})

                if not queasy:
                    queasy = Queasy()
                    db_session.add(queasy)

                    queasy.key = 212
                    queasy.number1 = keynumber
                    queasy.number2 = i
                    queasy.char1 = input_list.last_name
                    queasy.number3 = input_list.guestno


                else:
                    queasy.number1 = keynumber
        mess_result = "Import Data Success"
    else:
        mess_result = "Please load data first, press ENTER in CSV Delimiter"

    return generate_output()