#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
import random
from models import Bediener, Queasy

def prepare_benutzer_adminbl():

    prepare_cache ([Queasy])

    usr_list_list = []
    bediener = queasy = None

    usr_list = totpdata = None

    usr_list_list, Usr_list = create_model_like(Bediener, {"email":string, "mphone":string, "pager":string, "grp_str":string, "totp_flag":bool, "totp_status":string})

    Totpdata = create_buffer("Totpdata",Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal usr_list_list, bediener, queasy
        nonlocal totpdata


        nonlocal usr_list, totpdata
        nonlocal usr_list_list

        return {"usr-list": usr_list_list}

    def create_usrlist():

        nonlocal usr_list_list, bediener, queasy
        nonlocal totpdata


        nonlocal usr_list, totpdata
        nonlocal usr_list_list

        for bediener in db_session.query(Bediener).order_by(Bediener._recid).all():
            usr_list = Usr_list()
            usr_list_list.append(usr_list)

            buffer_copy(bediener, usr_list)

            queasy = get_cache (Queasy, {"key": [(eq, 134)],"number1": [(eq, bediener.nr)],"betriebsnr": [(eq, 0)],"deci1": [(eq, 0)],"logi1": [(eq, False)]})

            if queasy:
                usr_list.email = queasy.char2
                usr_list.mphone = queasy.char1
                usr_list.pager = queasy.char3

            if bediener.user_group > 0:

                queasy = get_cache (Queasy, {"key": [(eq, 19)],"number1": [(eq, bediener.user_group)]})

                if queasy:
                    usr_list.grp_str = queasy.char3

            totpdata = get_cache (Queasy, {"key": [(eq, 341)],"char1": [(eq, bediener.username)]})

            if totpdata:
                usr_list.totp_flag = True

                if totpdata.logi1 :
                    usr_list.totp_status = "ACTIVE"
                else:
                    usr_list.totp_status = "INACTIVE"


    def create_blist():

        nonlocal usr_list_list, bediener, queasy
        nonlocal totpdata


        nonlocal usr_list, totpdata
        nonlocal usr_list_list

        usr_code:string = ""
        usrbuff = None
        Usrbuff =  create_buffer("Usrbuff",Bediener)

        usr_list = query(usr_list_list, filters=(lambda usr_list: usr_list.betriebsnr == 0 and usr_list.flag == 0), first=True)
        while None != usr_list:
            usr_code = encode_string(usr_list.usercode)
            pass
            usr_list.usercode = usr_code
            usr_list.betriebsnr = 1
            pass

            usrbuff = db_session.query(Usrbuff).filter(
                     (Usrbuff.nr == usr_list.nr)).first()
            usrbuff.usercode = usr_code
            usrbuff.betriebsnr = 1


            pass

            usr_list = query(usr_list_list, filters=(lambda usr_list: usr_list.betriebsnr == 0 and usr_list.flag == 0), next=True)


    def encode_string(in_str:string):

        nonlocal usr_list_list, bediener, queasy
        nonlocal totpdata


        nonlocal usr_list, totpdata
        nonlocal usr_list_list

        out_str = ""
        s:string = ""
        j:int = 0
        len_:int = 0
        ch:string = ""

        def generate_inner_output():
            return (out_str)

        j = random.randint(1, 9)
        in_str = to_string(j) + in_str
        j = random.randint(1, 9)
        in_str = to_string(j) + in_str
        j = random.randint(1, 9)
        in_str = to_string(j) + in_str
        j = random.randint(1, 9)
        in_str = to_string(j) + in_str
        j = random.randint(1, 9)
        ch = chr_unicode(asc(to_string(j)) + 23)
        out_str = ch
        j = asc(ch) - 71
        for len_ in range(1,length(in_str)  + 1) :
            out_str = out_str + chr_unicode(asc(substring(in_str, len_ - 1, 1)) + j)

        return generate_inner_output()

    create_usrlist()
    create_blist()

    return generate_output()