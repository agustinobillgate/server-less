#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Debitor

def write_debitor_1bl(tb_recid:int, remarks:string):

    prepare_cache ([Debitor])

    successflag = True
    verscod_str:List[string] = create_empty_list(5,"")
    new_verscod:string = ""
    entries:int = 0
    i:int = 0
    debitor = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal successflag, verscod_str, new_verscod, entries, i, debitor
        nonlocal tb_recid, remarks

        return {"successflag": successflag}


    debitor = get_cache (Debitor, {"_recid": [(eq, tb_recid)]})

    if debitor:
        entries = num_entries(debitor.vesrcod, ";")

        if entries >= 1:
            for i in range(1,entries + 1) :
                verscod_str[i - 1] = entry(i - 1, debitor.vesrcod, ";")
            new_verscod = verscod_str[0] + ";" + remarks + ";"

            if verscod_str[2] != "":
                new_verscod = new_verscod + ";" + verscod_str[2] + ";"

            if verscod_str[3] != "":
                new_verscod = new_verscod + ";" + verscod_str[3] + ";"

            if verscod_str[4] != "":
                new_verscod = new_verscod + ";" + verscod_str[4] + ";"
        else:
            new_verscod = remarks
        debitor.vesrcod = new_verscod


        pass
        pass
        successflag = True

    return generate_output()