from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Kellner, Bediener

def prepare_ts_neubenutzerbl(curr_dept:int):
    kellner_list_list = []
    kellner = bediener = None

    kellner_list = None

    kellner_list_list, Kellner_list = create_model("Kellner_list", {"nr":int, "userinit":str, "username":str, "password":str, "mc_number":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal kellner_list_list, kellner, bediener


        nonlocal kellner_list
        nonlocal kellner_list_list
        return {"kellner-list": kellner_list_list}

    def create_list():

        nonlocal kellner_list_list, kellner, bediener


        nonlocal kellner_list
        nonlocal kellner_list_list

        bediener_obj_list = []
        for bediener, kellner in db_session.query(Bediener, Kellner).join(Kellner,(Kellnername == Bediener.username) &  (Kellner.departement == curr_dept)).filter(
                (Bediener.flag == 0) &  ((substring(Bediener.perm, 18, 1) >= "1") |  (substring(Bediener.perm, 19, 1) >= "1"))).all():
            if bediener._recid in bediener_obj_list:
                continue
            else:
                bediener_obj_list.append(bediener._recid)


            kellner_list = Kellner_list()
            kellner_list_list.append(kellner_list)

            kellner_list.nr = bediener.nr
            kellner_list.userinit = bediener.userinit
            kellner_list.username = bediener.username
            kellner_list.mc_number = to_string(kellner.sprachcode)


            kellner_list.password = decode_string1(bediener.usercode)

    def decode_string1(in_str:str):

        nonlocal kellner_list_list, kellner, bediener


        nonlocal kellner_list
        nonlocal kellner_list_list

        out_str = ""
        s:str = ""
        j:int = 0
        len_:int = 0

        def generate_inner_output():
            return out_str
        s = in_str
        j = ord(substring(s, 0, 1)) - 71
        len_ = len(in_str) - 1
        s = substring(in_str, 1, len_)
        for len_ in range(1,len(s)  + 1) :
            out_str = out_str + chr(ord(substring(s, len_ - 1, 1)) - j)
        out_str = substring(out_str, 4, (len(out_str) - 4))


        return generate_inner_output()


    create_list()

    return generate_output()