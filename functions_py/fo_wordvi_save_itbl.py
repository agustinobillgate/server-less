#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 28/11/2025, with_for_update added
#-------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import Briefzei

t_list_data, T_list = create_model("T_list", {"texte":string})

def fo_wordvi_save_itbl(t_list_data:[T_list], briefnr:int):
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

        return {}

    for t_list in query(t_list_data):

        if counter == 0:

            bzeile = db_session.query(Bzeile).filter(
                     (Bzeile.briefnr == briefnr)).first()
            reihenfolge = reihenfolge + 1

            bzeile = db_session.query(Bzeile).filter(
                     (Bzeile.briefnr == briefnr) & (Bzeile.briefzeilnr == reihenfolge)).with_for_update().first()

            if not bzeile:
                bzeile = Briefzei()
                db_session.add(bzeile)

                bzeile.briefnr = briefnr
                bzeile.briefzeilnr = reihenfolge


            bzeile.texte = ""
        bzeile.texte = bzeile.texte + t_list.texte + chr_unicode(10)
        counter = counter + length(t_list.texte) + 1

        if counter >= 20000:
            counter = 0
    pass

    for bzeile in db_session.query(Bzeile).filter(
             (Bzeile.briefnr == briefnr) & (Bzeile.briefzeilnr > reihenfolge)).order_by(Bzeile._recid).with_for_update().all():
        db_session.delete(bzeile)

    return generate_output()