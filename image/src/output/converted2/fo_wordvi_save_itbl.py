from functions.additional_functions import *
import decimal
from models import Briefzei

t_list_list, T_list = create_model("T_list", {"texte":str})

def fo_wordvi_save_itbl(t_list_list:[T_list], briefnr:int):
    counter:int = 0
    reihenfolge:int = 0
    briefzei = None

    t_list = bzeile = None

    Bzeile = create_buffer("Bzeile",Briefzei)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal counter, reihenfolge, briefzei
        nonlocal briefnr
        nonlocal bzeile


        nonlocal t_list, bzeile
        nonlocal t_list_list
        return {}

    for t_list in query(t_list_list):

        if counter == 0:

            bzeile = db_session.query(Bzeile).filter(
                     (Bzeile.briefnr == briefnr)).first()
            reihenfolge = reihenfolge + 1

            bzeile = db_session.query(Bzeile).filter(
                     (Bzeile.briefnr == briefnr) & (Bzeile.briefzeilnr == reihenfolge)).first()

            if not bzeile:
                bzeile = Bzeile()
                db_session.add(bzeile)

                bzeile.briefnr = briefnr
                bzeile.briefzeilnr = reihenfolge


            bzeile.texte = ""
        bzeile.texte = bzeile.texte + t_list.texte + chr(10)
        counter = counter + len(t_list.texte) + 1

        if counter >= 20000:
            counter = 0

    for bzeile in db_session.query(Bzeile).filter(
             (Bzeile.briefnr == briefnr) & (Bzeile.briefzeilnr > reihenfolge)).order_by(Bzeile._recid).all():
        bzeile_list.remove(bzeile)

    return generate_output()