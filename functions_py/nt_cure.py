from functions.additional_functions import *
import decimal
from models import Kresline, Htparam, Artikel, Kabine, Masseur, Guest, K_history

def nt_cure():
    endtime:str = ""
    kresline = htparam = artikel = kabine = masseur = guest = k_history = None

    kresline1 = None

    Kresline1 = create_buffer("Kresline1",Kresline)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal endtime, kresline, htparam, artikel, kabine, masseur, guest, k_history
        nonlocal kresline1


        nonlocal kresline1

        return {}


    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 110)).first()

    kresline_obj_list = []
    for kresline, artikel, kabine, masseur, guest in db_session.query(Kresline, Artikel, Kabine, Masseur, Guest).join(Artikel,(Artikel.departement == Kresline.departement) & (Artikel.artnr == Kresline.artnr)).join(Kabine,(Kabine.kabnr == Kresline.kabnr)).join(Masseur,(Masseur.massnr == Kresline.massnr)).join(Guest,(Guest.gastnr == Kresline.gastnr)).filter(
             (Kresline.datum == htparam.fdate)).order_by(Kresline.zeitanw).all():
        if kresline._recid in kresline_obj_list:
            continue
        else:
            kresline_obj_list.append(kresline._recid)

        if kresline.betriebsnr != 9:
            endtime = to_string((to_int(substring(kresline.zeitanw, 0, 2)) * 60 * 60) + (to_int(substring(kresline.zeitanw, 2, 2)) * 60) + (artikel.anwdauer * 60) , "HH:MM")

            k_history = db_session.query(K_history).filter(
                     (K_history.resnr == kresline.kurresnr)).first()

            if not k_history:
                k_history = K_history()
                db_session.add(k_history)

                k_history.resnr = kresline.kurresnr
                k_history.gastnr = kresline.gastnr

            if k_history.from_date == None:
                k_history.from_date = kresline.datum
                k_history.to_date = kresline.datum
            else:

                if k_history.from_date > kresline.datum:
                    k_history.from_date = kresline.datum

                elif k_history.to_date < kresline.datum:
                    k_history.to_date = kresline.datum
            k_history.info2 = "Weight : " + to_string(guest.groesse, ">>9") + " " + "Kg" + "; " + "Height : " + to_string(guest.gewicht, ">>9") + " " + "Cm"
            k_history.treatment = k_history.treatment + to_string(kresline.datum, "99/99/99") + " " + to_string(kresline.zeitanw, "99:99") + "-" + endtime + " " + artikel.bezeich + " " + "In" + " " + kabine.kabbez + " " + "By" + " " + masseur.name + ";" + chr(10)

    for kresline in db_session.query(Kresline).filter(
             (Kresline.datum <= htparam.fdate)).with_for_update().order_by(Kresline._recid).all():

        kresline1 = db_session.query(Kresline1).filter(
                 (Kresline1.kurresnr == kresline.kurresnr) & (Kresline1.kreslinr != kresline.kreslinr) & (Kresline1.datum > htparam.fdate)).first()

        if not kresline1:
            db_session.delete(kresline)

    return generate_output()