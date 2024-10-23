from functions.additional_functions import *
import decimal
from models import Wgrpdep, H_artikel, Artikel, Queasy

def copy_hartikel_btn_gobl(all_flag:bool, dept1:int, dept2:int, art1:int, art2:int, overwrite_flag:bool):
    anzahl = ""
    wgrpdep = h_artikel = artikel = queasy = None

    subgrp = h_art = art = None

    Subgrp = create_buffer("Subgrp",Wgrpdep)
    H_art = create_buffer("H_art",H_artikel)
    Art = create_buffer("Art",Artikel)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal anzahl, wgrpdep, h_artikel, artikel, queasy
        nonlocal all_flag, dept1, dept2, art1, art2, overwrite_flag
        nonlocal subgrp, h_art, art


        nonlocal subgrp, h_art, art
        return {"anzahl": anzahl}

    def copy_sales():

        nonlocal anzahl, wgrpdep, h_artikel, artikel, queasy
        nonlocal all_flag, dept1, dept2, art1, art2, overwrite_flag
        nonlocal subgrp, h_art, art


        nonlocal subgrp, h_art, art

        n:int = 0
        qbuff = None
        Qbuff =  create_buffer("Qbuff",Queasy)
        anzahl = to_string(n)

        for h_art in db_session.query(H_art).filter(
                 (H_art.departement == dept1) & (H_art.activeflag) & (H_art.artart == 0) & (H_art.artnr >= art1) & (H_art.artnr <= art2)).order_by(H_art._recid).all():

            h_artikel = db_session.query(H_artikel).filter(
                     (H_artikel.artnr == h_art.artnr) & (H_artikel.departement == dept2)).first()

            if h_artikel and not overwrite_flag:
                pass
            else:
                n = n + 1
                anzahl = to_string(n)

                subgrp = db_session.query(Subgrp).filter(
                         (Subgrp.departement == dept1) & (Subgrp.zknr == h_art.zwkum)).first()

                wgrpdep = db_session.query(Wgrpdep).filter(
                         (Wgrpdep.departement == dept2) & (Wgrpdep.zknr == h_art.zwkum)).first()

                if not wgrpdep and subgrp:
                    wgrpdep = Wgrpdep()
                    db_session.add(wgrpdep)

                    wgrpdep.departement = dept2
                    wgrpdep.zknr = subgrp.zknr
                    wgrpdep.bezeich = subgrp.bezeich

                if not h_artikel:
                    h_artikel = H_artikel()
                db_session.add(h_artikel)

                h_artikel.artnr = h_art.artnr
                h_artikel.departement = dept2
                h_artikel.bezeich = h_art.bezeich
                h_artikel.epreis1 =  to_decimal(h_art.epreis1)
                h_artikel.epreis2 =  to_decimal(h_art.epreis2)
                h_artikel.zwkum = h_art.zwkum
                h_artikel.endkum = h_art.endkum
                h_artikel.mwst_code = h_art.mwst_code
                h_artikel.service_code = h_art.service_code
                h_artikel.autosaldo = h_art.autosaldo
                h_artikel.bezaendern = h_art.bezaendern
                h_artikel.bondruckernr[0] = h_art.bondruckernr[0]
                h_artikel.aenderwunsch = h_art.aenderwunsch
                h_artikel.s_gueltig = h_art.s_gueltig
                h_artikel.e_gueltig = h_art.e_gueltig
                h_artikel.artnrlager = h_art.artnrlager
                h_artikel.artnrrezept = h_art.artnrrezept
                h_artikel.lagernr = h_art.lagernr
                h_artikel.prozent =  to_decimal(h_art.prozent)
                h_artikel.artnrfront = h_art.artnrfront
                h_artikel.activeflag = True

                queasy = db_session.query(Queasy).filter(
                         (Queasy.key == 38) & (Queasy.number1 == dept1) & (Queasy.number2 == h_art.artnr)).first()

                if queasy:
                    qbuff = Queasy()
                    db_session.add(qbuff)

                    buffer_copy(queasy, qbuff,except_fields=["number1"])
                    qbuff.number1 = dept2

                art = db_session.query(Art).filter(
                         (Art.artnr == h_art.artnrfront) & (Art.departement == dept1)).first()

                artikel = db_session.query(Artikel).filter(
                         (Artikel.artnr == h_art.artnrfront) & (Artikel.departement == dept2)).first()

                if not artikel and art:
                    artikel = Artikel()
                    db_session.add(artikel)

                    artikel.departement = dept2
                    artikel.artnr = art.artnr
                    artikel.bezeich = art.bezeich
                    artikel.activeflag = True
                    artikel.fibukonto = art.fibukonto
                    artikel.bezeich1 = art.bezeich1
                    artikel.zwkum = art.zwkum
                    artikel.endkum = art.endkum
                    artikel.epreis =  to_decimal(art.epreis)
                    artikel.autosaldo = art.autosaldo
                    artikel.artart = art.artart
                    artikel.umsatzart = art.umsatzart
                    artikel.kassarapport = art.kassarapport
                    artikel.kassabuch = art.kassabuch
                    artikel.mwst_code = art.mwst_code
                    artikel.service_code = art.service_code
                    artikel.fibukonto = art.fibukonto
                    artikel.bezeich1 = art.bezeich
                    artikel.pricetab = art.pricetab
                    artikel.activeflag = art.activeflag
                    artikel.s_gueltig = art.s_gueltig
                    artikel.e_gueltig = art.e_gueltig
                    artikel.artnrlager = art.artnrlager
                    artikel.artnrrezept = art.artnrrezept
                    artikel.prozent =  to_decimal(art.prozent)
                    artikel.lagernr = art.lagernr


    def copy_all():

        nonlocal anzahl, wgrpdep, h_artikel, artikel, queasy
        nonlocal all_flag, dept1, dept2, art1, art2, overwrite_flag
        nonlocal subgrp, h_art, art


        nonlocal subgrp, h_art, art

        n:int = 0
        anzahl = to_string(n)

        for h_art in db_session.query(H_art).filter(
                 (H_art.departement == dept1) & (H_art.activeflag) & (H_art.artnr >= art1) & (H_art.artnr <= art2)).order_by(H_art._recid).all():

            h_artikel = db_session.query(H_artikel).filter(
                     (H_artikel.artnr == h_art.artnr) & (H_artikel.departement == dept2)).first()

            if h_artikel and not overwrite_flag:
                pass
            else:
                n = n + 1
                anzahl = to_string(n)

                subgrp = db_session.query(Subgrp).filter(
                         (Subgrp.departement == dept1) & (Subgrp.zknr == h_art.zwkum)).first()

                wgrpdep = db_session.query(Wgrpdep).filter(
                         (Wgrpdep.departement == dept2) & (Wgrpdep.zknr == h_art.zwkum)).first()

                if not wgrpdep and subgrp:
                    wgrpdep = Wgrpdep()
                    db_session.add(wgrpdep)

                    wgrpdep.departement = dept2
                    wgrpdep.zknr = subgrp.zknr
                    wgrpdep.bezeich = subgrp.bezeich

                if not h_artikel:
                    h_artikel = H_artikel()
                db_session.add(h_artikel)

                h_artikel.artnr = h_art.artnr
                h_artikel.artart = h_art.artart
                h_artikel.departement = dept2
                h_artikel.bezeich = h_art.bezeich
                h_artikel.epreis1 =  to_decimal(h_art.epreis1)
                h_artikel.epreis2 =  to_decimal(h_art.epreis2)
                h_artikel.zwkum = h_art.zwkum
                h_artikel.endkum = h_art.endkum
                h_artikel.mwst_code = h_art.mwst_code
                h_artikel.service_code = h_art.service_code
                h_artikel.autosaldo = h_art.autosaldo
                h_artikel.bezaendern = h_art.bezaendern
                h_artikel.bondruckernr[0] = h_art.bondruckernr[0]
                h_artikel.aenderwunsch = h_art.aenderwunsch
                h_artikel.s_gueltig = h_art.s_gueltig
                h_artikel.e_gueltig = h_art.e_gueltig
                h_artikel.artnrlager = h_art.artnrlager
                h_artikel.artnrrezept = h_art.artnrrezept
                h_artikel.lagernr = h_art.lagernr
                h_artikel.prozent =  to_decimal(h_art.prozent)
                h_artikel.artnrfront = h_art.artnrfront
                h_artikel.activeflag = True

                if h_art.artart == 0:

                    art = db_session.query(Art).filter(
                             (Art.artnr == h_art.artnrfront) & (Art.departement == dept1)).first()

                    artikel = db_session.query(Artikel).filter(
                             (Artikel.artnr == h_art.artnrfront) & (Artikel.departement == dept2)).first()

                    if not artikel and art:
                        artikel = Artikel()
                        db_session.add(artikel)

                        artikel.departement = dept2
                        artikel.artnr = art.artnr
                        artikel.bezeich = art.bezeich
                        artikel.activeflag = True
                        artikel.fibukonto = art.fibukonto
                        artikel.bezeich1 = art.bezeich1
                        artikel.zwkum = art.zwkum
                        artikel.endkum = art.endkum
                        artikel.epreis =  to_decimal(art.epreis)
                        artikel.autosaldo = art.autosaldo
                        artikel.artart = art.artart
                        artikel.umsatzart = art.umsatzart
                        artikel.kassarapport = art.kassarapport
                        artikel.kassabuch = art.kassabuch
                        artikel.mwst_code = art.mwst_code
                        artikel.service_code = art.service_code
                        artikel.fibukonto = art.fibukonto
                        artikel.bezeich1 = art.bezeich
                        artikel.pricetab = art.pricetab
                        artikel.activeflag = art.activeflag
                        artikel.s_gueltig = art.s_gueltig
                        artikel.e_gueltig = art.e_gueltig
                        artikel.artnrlager = art.artnrlager
                        artikel.artnrrezept = art.artnrrezept
                        artikel.prozent =  to_decimal(art.prozent)
                        artikel.lagernr = art.lagernr

    if not all_flag:
        copy_sales()
    else:
        copy_all()

    return generate_output()