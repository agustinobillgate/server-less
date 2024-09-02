from functions.additional_functions import *
import decimal
from models import Queasy

def na_start_get_info_webbl():
    na_done = False
    plist_list = []
    inpfile:str = ""
    lic_nr:str = ""
    search_txt:str = ""
    temp_char:str = ""
    queasy = None

    plist = None

    plist_list, Plist = create_model("Plist", {"bezeich":str, "progres":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal na_done, plist_list, inpfile, lic_nr, search_txt, temp_char, queasy


        nonlocal plist
        nonlocal plist_list
        return {"na_done": na_done, "plist": plist_list}

    def decode_string(in_str:str):

        nonlocal na_done, plist_list, inpfile, lic_nr, search_txt, temp_char, queasy


        nonlocal plist
        nonlocal plist_list

        out_str = ""
        s:str = ""
        j:int = 0
        len_:int = 0

        def generate_inner_output():
            return out_str
        s = in_str
        j = ord(substring(s, 0, 1)) - 70
        len_ = len(in_str) - 1
        s = substring(in_str, 1, len_)
        for len_ in range(1,len(s)  + 1) :
            out_str = out_str + chr (ord(substring(s, len_ - 1, 1)) - j)


        return generate_inner_output()


    plist_list.clear()

    queasy = db_session.query(Queasy).filter(
            (Queasy.key == 232) &  (Queasy.date1 == get_current_date())).first()

    if not queasy:
        na_done = True

        return generate_output()

    for queasy in db_session.query(Queasy).filter(
            (Queasy.key == 232) &  (Queasy.date1 == get_current_date())).all():
        plist = Plist()
        plist_list.append(plist)

        plist.bezeich = queasy.char2
        plist.progres = queasy.char3

    return generate_output()