from functions.additional_functions import *
import decimal
from models import Zimmer, Nebenst

def ever_nebst():
    zimmer = nebenst = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal zimmer, nebenst

        return {}


    for zimmer in db_session.query(Zimmer).order_by(Zimmer._recid).all():
        nebenst = Nebenst()
        db_session.add(nebenst)

        nebenst.artnr = 0
        nebenst.betriebsnr = 0
        nebenst.bezeich = "KEY" + zimmer.zinr
        nebenst.departement = 0
        nebenst.nebenstelle = "010" + zimmer.zinr
        nebenst.nebst_type = 0
        nebenst.nebstart = 3
        nebenst.rechnr = 0
        nebenst.vipnr = ""
        nebenst.zinr = zimmer.zinr

    return generate_output()