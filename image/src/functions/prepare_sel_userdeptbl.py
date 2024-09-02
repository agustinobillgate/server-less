from functions.additional_functions import *
import decimal
from models import Eg_staff, Queasy

def prepare_sel_userdeptbl(dept_nr:int):
    usr_list = []
    eg_staff = queasy = None

    usr = usr1 = None

    usr_list, Usr = create_model("Usr", {"nr":int, "name":str, "skill":str})

    Usr1 = Eg_staff

    db_session = local_storage.db_session

    def generate_output():
        nonlocal usr_list, eg_staff, queasy
        nonlocal usr1


        nonlocal usr, usr1
        nonlocal usr_list
        return {"usr": usr_list}

    def create_user():

        nonlocal usr_list, eg_staff, queasy
        nonlocal usr1


        nonlocal usr, usr1
        nonlocal usr_list

        a:str = ""
        i:int = 0
        j:str = ""
        c:str = ""
        usr_list.clear()

        for usr1 in db_session.query(Usr1).filter(
                (Usr1.usergroup == dept_nr) &  (Usr1.activeflag)).all():
            a = usr1.skill

            if a != "":
                for i in range(1,num_entries(a, ";")  + 1) :
                    j = entry(i - 1, a , ";")

                    queasy = db_session.query(Queasy).filter(
                            (Queasy.key == 132) &  (Queasy.number1 == int (j))).first()

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