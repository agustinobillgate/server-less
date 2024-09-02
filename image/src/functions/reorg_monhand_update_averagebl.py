from functions.additional_functions import *
import decimal
from datetime import date
from models import Htparam, L_bestand, L_artikel

def reorg_monhand_update_averagebl(art_type:int):
    main_grp:int = 0
    to_grp:int = 0
    to_date:date = None
    from_date:date = None
    htparam = l_bestand = l_artikel = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal main_grp, to_grp, to_date, from_date, htparam, l_bestand, l_artikel


        return {}

    def update_average():

        nonlocal main_grp, to_grp, to_date, from_date, htparam, l_bestand, l_artikel

        tot_anz:decimal = 0
        tot_wert:decimal = 0
        avrg_price:decimal = 0

        l_bestand = db_session.query(L_bestand).filter(
                (L_bestand.lager_nr == 0)).first()
        while None != l_bestand:

            l_artikel = db_session.query(L_artikel).filter(
                    (L_artikel.artnr == l_bestand.artnr)).first()

            if l_artikel and l_artikel.endkum >= main_grp and l_artikel.endkum <= to_grp:
                tot_anz = l_bestand.anz_anf_best + l_bestand.anz_eingang -\
                        l_bestand.anz_ausgang
                tot_wert = l_bestand.val_anf_best + l_bestand.wert_eingang -\
                        l_bestand.wert_ausgang

                if tot_anz == 0:
                    tot_anz = l_bestand.anz_anf_best + l_bestand.anz_eingang
                    tot_wert = l_bestand.val_anf_best + l_bestand.wert_eingang

                if tot_anz != 0:
                    avrg_price = tot_wert / tot_anz

                    l_artikel = db_session.query(L_artikel).filter(
                            (L_artikel.artnr == l_bestand.artnr)).first()
                    l_artikel.vk_preis = avrg_price

                    l_artikel = db_session.query(L_artikel).first()


            l_bestand = db_session.query(L_bestand).filter(
                    (L_bestand.lager_nr == 0)).first()


    if art_type == 1:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 257)).first()
        main_grp = htparam.finteger
        to_grp = main_grp

    elif art_type == 2:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 258)).first()
        main_grp = htparam.finteger
        to_grp = main_grp

    elif art_type == 3:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 268)).first()
        main_grp = htparam.finteger
        to_grp = 9

    if art_type <= 2:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 224)).first()
    else:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 221)).first()
    to_date = fdate
    from_date = date_mdy(get_month(to_date) , 1, get_year(to_date))
    update_average()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 232)).first()
    htparam.flogical = False

    htparam = db_session.query(Htparam).first()

    return generate_output()