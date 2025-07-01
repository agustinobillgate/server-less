#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import L_kredit

obuff_list, Obuff = create_model("Obuff", {"srecid":int, "remark":string})

def ap_paylist_chgremarksbl(obuff_list:[Obuff]):

    prepare_cache ([L_kredit])

    l_kredit = None

    obuff = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal l_kredit


        nonlocal obuff

        return {}

    for obuff in query(obuff_list, filters=(lambda obuff: obuff.srecid != 0)):

        l_kredit = get_cache (L_kredit, {"_recid": [(eq, obuff.srecid)]})

        if l_kredit:
            pass
            l_kredit.bemerk = obuff.remark


            pass
            pass

    return generate_output()