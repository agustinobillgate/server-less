from functions.additional_functions import *
import decimal
from models import L_kredit

obuff_list, Obuff = create_model("Obuff", {"srecid":int, "remark":str})

def ap_paylist_chgremarksbl(obuff_list:[Obuff]):
    l_kredit = None

    obuff = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal l_kredit


        nonlocal obuff
        nonlocal obuff_list
        return {}

    for obuff in query(obuff_list, filters=(lambda obuff: obuff.srecid != 0)):

        l_kredit = db_session.query(L_kredit).filter(
                 (L_kredit._recid == obuff.srecid)).first()
        l_kredit.bemerk = obuff.remark

    return generate_output()