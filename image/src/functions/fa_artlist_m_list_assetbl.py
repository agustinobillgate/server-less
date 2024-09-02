from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Mathis, Fa_artikel

def fa_artlist_m_list_assetbl(asset:str):
    avail_asset = False
    mathis_name = ""
    mathis = fa_artikel = None

    mathis1 = None

    Mathis1 = Mathis

    db_session = local_storage.db_session

    def generate_output():
        nonlocal avail_asset, mathis_name, mathis, fa_artikel
        nonlocal mathis1


        nonlocal mathis1
        return {"avail_asset": avail_asset, "mathis_name": mathis_name}


    mathis1 = db_session.query(Mathis1).filter(
            (func.lower(Mathis1.(asset).lower()) == (asset).lower())).first()

    if mathis1:

        fa_artikel = db_session.query(Fa_artikel).filter(
                (Fa_artikel.nr == mathis1.nr)).first()

        if fa_artikel.loeschflag == 0:
            avail_asset = True
            mathis_name = mathis1.name

    return generate_output()