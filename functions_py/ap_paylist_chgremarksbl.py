#using conversion tools version: 1.0.0.119

from functions.additional_functions import *
from decimal import Decimal
from models import L_kredit

obuff_data, Obuff = create_model("Obuff", {"srecid":int, "remark":string})

def ap_paylist_chgremarksbl(obuff_data:[Obuff]):

    prepare_cache ([L_kredit])

    l_kredit = None

    obuff = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal l_kredit


        nonlocal obuff

        return {}

    for obuff in query(obuff_data, filters=(lambda obuff: obuff.srecid != 0)):

        l_kredit = db_session.query(L_kredit).filter(L_kredit._recid == obuff.srecid).first()

        if l_kredit:
            db_session.refresh(l_kredit, with_for_update=True)
            l_kredit.bemerk = obuff.remark

    return generate_output()