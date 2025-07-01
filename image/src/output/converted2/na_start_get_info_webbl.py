#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy

def na_start_get_info_webbl():

    prepare_cache ([Queasy])

    na_done = False
    plist_list = []
    inpfile:string = ""
    lic_nr:string = ""
    search_txt:string = ""
    temp_char:string = ""
    queasy = None

    plist = None

    plist_list, Plist = create_model("Plist", {"bezeich":string, "progres":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal na_done, plist_list, inpfile, lic_nr, search_txt, temp_char, queasy


        nonlocal plist
        nonlocal plist_list

        return {"na_done": na_done, "plist": plist_list}

    def decode_string(in_str:string):

        nonlocal na_done, plist_list, inpfile, lic_nr, search_txt, temp_char, queasy


        nonlocal plist
        nonlocal plist_list

        out_str = ""
        s:string = ""
        j:int = 0
        len_:int = 0

        def generate_inner_output():
            return (out_str)

        s = in_str
        j = asc(substring(s, 0, 1)) - 70
        len_ = length(in_str) - 1
        s = substring(in_str, 1, len_)
        for len_ in range(1,length(s)  + 1) :
            out_str = out_str + chr_unicode(asc(substring(s, len_ - 1, 1)) - j)

        return generate_inner_output()

    plist_list.clear()

    queasy = get_cache (Queasy, {"key": [(eq, 232)],"date1": [(eq, get_current_date())]})

    if not queasy:
        na_done = True

        return generate_output()

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 232) & (Queasy.date1 == get_current_date())).order_by(Queasy.char3.desc()).all():
        plist = Plist()
        plist_list.append(plist)

        plist.bezeich = queasy.char2
        plist.progres = queasy.char3

    return generate_output()