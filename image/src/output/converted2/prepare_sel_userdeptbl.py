#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Eg_staff, Queasy

def prepare_sel_userdeptbl(dept_nr:int):

    prepare_cache ([Eg_staff, Queasy])

    usr_list = []
    eg_staff = queasy = None

    usr = usr1 = None

    usr_list, Usr = create_model("Usr", {"nr":int, "name":string, "skill":string})

    Usr1 = create_buffer("Usr1",Eg_staff)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal usr_list, eg_staff, queasy
        nonlocal dept_nr
        nonlocal usr1


        nonlocal usr, usr1
        nonlocal usr_list

        return {"usr": usr_list}

    def create_user():

        nonlocal usr_list, eg_staff, queasy
        nonlocal dept_nr
        nonlocal usr1


        nonlocal usr, usr1
        nonlocal usr_list

        a:string = ""
        i:int = 0
        j:string = ""
        c:string = ""
        curr_num:int = 0
        usr_list.clear()

        for usr1 in db_session.query(Usr1).filter(
                 (Usr1.usergroup == dept_nr) & (Usr1.activeflag)).order_by(Usr1._recid).all():
            a = usr1.skill

            if a != "":
                for i in range(1,num_entries(a, ";")  + 1) :
                    j = entry(i - 1, a , ";")
                    curr_num = to_int(j)

                    queasy = get_cache (Queasy, {"key": [(eq, 132)],"number1": [(eq, curr_num)]})

                    if queasy:

                        if c == "":
                            c = queasy.char1
                        else:
                            c = c + "," + queasy.char1
            else:
                c = ""
            usr = Usr()
            usr_list.append(usr)

            usr.nr = usr1.nr
            usr.name = usr1.name
            usr.skill = c


            c = ""

    create_user()

    return generate_output()