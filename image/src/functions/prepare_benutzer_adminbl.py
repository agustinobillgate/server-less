from functions.additional_functions import *
import decimal
import random
from models import Bediener, Queasy

def prepare_benutzer_adminbl():
    usr_list_list = []
    bediener = queasy = None

    usr_list = usrbuff = None

    usr_list_list, Usr_list = create_model_like(Bediener, {"email":str, "mphone":str, "pager":str, "grp_str":str})

    Usrbuff = Bediener

    db_session = local_storage.db_session

    def generate_output():
        nonlocal usr_list_list, bediener, queasy
        nonlocal usrbuff


        nonlocal usr_list, usrbuff
        nonlocal usr_list_list
        return {"usr-list": usr_list_list}

    def create_usrlist():

        nonlocal usr_list_list, bediener, queasy
        nonlocal usrbuff


        nonlocal usr_list, usrbuff
        nonlocal usr_list_list

        for bediener in db_session.query(Bediener).all():
            usr_list = Usr_list()
            usr_list_list.append(usr_list)

            buffer_copy(bediener, usr_list)

            queasy = db_session.query(Queasy).filter(
                    (Queasy.key == 134) &  (Queasy.number1 == bediener.nr) &  (Queasy.betriebsnr == 0) &  (Queasy.deci1 == 0) &  (Queasy.logi1 == False)).first()

            if queasy:
                usr_list.email = queasy.char2
                usr_list.mphone = queasy.char1
                usr_list.pager = queasy.char3

            if bediener.user_group > 0:

                queasy = db_session.query(Queasy).filter(
                        (Queasy.key == 19) &  (Queasy.number1 == bediener.user_group)).first()

                if queasy:
                    usr_list.grp_str = queasy.char3

    def create_blist():

        nonlocal usr_list_list, bediener, queasy
        nonlocal usrbuff


        nonlocal usr_list, usrbuff
        nonlocal usr_list_list

        usr_code:str = ""
        Usrbuff = Bediener

        usr_list = query(usr_list_list, filters=(lambda usr_list :usr_list.betriebsnr == 0 and usr_list.flag == 0), first=True)
        while None != usr_list:
            usr_code = encode_string(usr_list.usercode)

            usr_list = query(usr_list_list, current=True)
            usr_list.usercode = usr_code
            usr_list.betriebsnr = 1

            usr_list = query(usr_list_list, current=True)

            usrbuff = db_session.query(Usrbuff).filter(
                    (Usrbuff.nr == usr_list.nr)).first()
            usrbuff.usercode = usr_code
            usrbuff.betriebsnr = 1

            usrbuff = db_session.query(Usrbuff).first()

            usr_list = query(usr_list_list, filters=(lambda usr_list :usr_list.betriebsnr == 0 and usr_list.flag == 0), next=True)

    def encode_string(in_str:str):

        nonlocal usr_list_list, bediener, queasy
        nonlocal usrbuff


        nonlocal usr_list, usrbuff
        nonlocal usr_list_list

        out_str = ""
        s:str = ""
        j:int = 0
        len_:int = 0
        ch:str = ""

        def generate_inner_output():
            return out_str
        j = random.randint(1, 9)
        in_str = to_string(j) + in_str
        j = random.randint(1, 9)
        in_str = to_string(j) + in_str
        j = random.randint(1, 9)
        in_str = to_string(j) + in_str
        j = random.randint(1, 9)
        in_str = to_string(j) + in_str
        j = random.randint(1, 9)
        ch = chr(ord(to_string(j)) + 23)
        out_str = ch
        j = ord(ch) - 71
        for len_ in range(1,len(in_str)  + 1) :
            out_str = out_str + chr (ord(substring(in_str, len_ - 1, 1)) + j)


        return generate_inner_output()


    create_usrlist()
    create_blist()

    return generate_output()