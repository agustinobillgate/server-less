#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Kellner, Bediener

def prepare_ts_neubenutzerbl(curr_dept:int):

    prepare_cache ([Kellner, Bediener])

    kellner_list_list = []
    kellner = bediener = None

    kellner_list = None

    kellner_list_list, Kellner_list = create_model("Kellner_list", {"nr":int, "userinit":string, "username":string, "password":string, "mc_number":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal kellner_list_list, kellner, bediener
        nonlocal curr_dept


        nonlocal kellner_list
        nonlocal kellner_list_list

        return {"kellner-list": kellner_list_list}

    def create_list():

        nonlocal kellner_list_list, kellner, bediener
        nonlocal curr_dept


        nonlocal kellner_list
        nonlocal kellner_list_list

        bediener_obj_list = {}
        bediener = Bediener()
        kellner = Kellner()
        for bediener.nr, bediener.userinit, bediener.username, bediener.usercode, bediener._recid, kellner.sprachcode, kellner._recid in db_session.query(Bediener.nr, Bediener.userinit, Bediener.username, Bediener.usercode, Bediener._recid, Kellner.sprachcode, Kellner._recid).join(Kellner,(Kellner.kellnername == Bediener.username) & (Kellner.departement == curr_dept)).filter(
                 (Bediener.flag == 0) & ((substring(Bediener.perm, 18, 1) >= ("1").lower()) | (substring(Bediener.perm, 19, 1) >= ("1").lower()))).order_by(Bediener.username).all():
            if bediener_obj_list.get(bediener._recid):
                continue
            else:
                bediener_obj_list[bediener._recid] = True


            kellner_list = Kellner_list()
            kellner_list_list.append(kellner_list)

            kellner_list.nr = bediener.nr
            kellner_list.userinit = bediener.userinit
            kellner_list.username = bediener.username
            kellner_list.mc_number = to_string(kellner.sprachcode)


            kellner_list.password = decode_string1(bediener.usercode)


    def decode_string1(in_str:string):

        nonlocal kellner_list_list, kellner, bediener
        nonlocal curr_dept


        nonlocal kellner_list
        nonlocal kellner_list_list

        out_str = ""
        s:string = ""
        j:int = 0
        len_:int = 0

        def generate_inner_output():
            return (out_str)

        s = in_str
        j = asc(substring(s, 0, 1)) - 71
        len_ = length(in_str) - 1
        s = substring(in_str, 1, len_)
        for len_ in range(1,length(s)  + 1) :
            out_str = out_str + chr_unicode(asc(substring(s, len_ - 1, 1)) - j)
        out_str = substring(out_str, 4, (length(out_str) - 4))

        return generate_inner_output()

    create_list()

    return generate_output()