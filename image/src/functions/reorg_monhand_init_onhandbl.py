from functions.additional_functions import *
import decimal
from datetime import date
from models import Htparam, L_bestand, L_artikel, L_lager

def reorg_monhand_init_onhandbl(art_type:int):
    main_grp:int = 0
    to_grp:int = 0
    to_date:date = None
    from_date:date = None
    htparam = l_bestand = l_artikel = l_lager = None

    l_oh = buf_lart = None

    L_oh = L_bestand
    Buf_lart = L_artikel

    db_session = local_storage.db_session

    def generate_output():
        nonlocal main_grp, to_grp, to_date, from_date, htparam, l_bestand, l_artikel, l_lager
        nonlocal l_oh, buf_lart


        nonlocal l_oh, buf_lart
        return {}

    def init_onhand():

        nonlocal main_grp, to_grp, to_date, from_date, htparam, l_bestand, l_artikel, l_lager
        nonlocal l_oh, buf_lart


        nonlocal l_oh, buf_lart

        loopi:int = 0
        L_oh = L_bestand
        Buf_lart = L_artikel

        l_bestand = db_session.query(L_bestand).filter(
                (L_bestand.lager_nr == 0)).first()
        while None != l_bestand:

            buf_lart = db_session.query(Buf_lart).filter(
                    (Buf_lart.artnr == l_bestand.artnr) &  (Buf_lart.endkum >= main_grp) &  (Buf_lart.endkum <= to_grp)).first()

            if buf_lart:

                l_oh = db_session.query(L_oh).filter(
                        (L_oh._recid == l_bestand._recid)).first()
                l_oh.anz_eingang = 0
                l_oh.wert_eingang = 0
                l_oh.anz_ausgang = 0
                l_oh.wert_ausgang = 0

                l_oh = db_session.query(L_oh).first()


            l_bestand = db_session.query(L_bestand).filter(
                    (L_bestand.lager_nr == 0)).first()

        l_lager = db_session.query(L_lager).first()
        while None != l_lager:

            l_bestand = db_session.query(L_bestand).filter(
                    (L_bestand.lager_nr == l_lager.lager_nr)).first()
            while None != l_bestand:

                buf_lart = db_session.query(Buf_lart).filter(
                        (Buf_lart.artnr == l_bestand.artnr) &  (Buf_lart.endkum >= main_grp) &  (Buf_lart.endkum <= to_grp)).first()

                if buf_lart:

                    l_oh = db_session.query(L_oh).filter(
                            (L_oh._recid == l_bestand._recid)).first()
                    l_oh.anz_eingang = 0
                    l_oh.wert_eingang = 0
                    l_oh.anz_ausgang = 0
                    l_oh.wert_ausgang = 0

                    l_oh = db_session.query(L_oh).first()


                l_bestand = db_session.query(L_bestand).filter(
                        (L_bestand.lager_nr == l_lager.lager_nr)).first()

            l_lager = db_session.query(L_lager).first()


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

    htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 232)).first()
    htparam.flogical = True

    htparam = db_session.query(Htparam).first()


    if art_type <= 2:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 224)).first()
    else:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 221)).first()
    to_date = fdate
    from_date = date_mdy(get_month(to_date) , 1, get_year(to_date))
    init_onhand()

    return generate_output()