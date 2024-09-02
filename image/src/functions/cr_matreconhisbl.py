from functions.additional_functions import *
import decimal
from datetime import date
from models import Gl_acct, L_artikel, L_untergrup, L_besthis, L_lager, L_ophis

def cr_matreconhisbl(to_date:date, lager_no:int, from_main:int, to_main:int, sort_type:int):
    art_bestand_list = []
    from_date:date = get_current_date()
    gl_acct = l_artikel = l_untergrup = l_besthis = l_lager = l_ophis = None

    art_bestand = gl_acct1 = l_oh = None

    art_bestand_list, Art_bestand = create_model("Art_bestand", {"nr":int, "zwkum":int, "bezeich":str, "prevval":decimal, "adjust":decimal, "inval":decimal, "outval":decimal, "actval":decimal, "inv_acct":str, "fibukonto":str, "artnr":int})

    Gl_acct1 = Gl_acct
    L_oh = L_besthis

    db_session = local_storage.db_session

    def generate_output():
        nonlocal art_bestand_list, from_date, gl_acct, l_artikel, l_untergrup, l_besthis, l_lager, l_ophis
        nonlocal gl_acct1, l_oh


        nonlocal art_bestand, gl_acct1, l_oh
        nonlocal art_bestand_list
        return {"art-bestand": art_bestand_list}

    def create_list():

        nonlocal art_bestand_list, from_date, gl_acct, l_artikel, l_untergrup, l_besthis, l_lager, l_ophis
        nonlocal gl_acct1, l_oh


        nonlocal art_bestand, gl_acct1, l_oh
        nonlocal art_bestand_list

        zwkum:int = 0
        prevval:decimal = 0
        inval:decimal = 0
        outval:decimal = 0
        actval:decimal = 0
        bezeich:str = ""
        j:int = 0
        other_fibu:bool = False
        it_exist:bool = False
        fibukonto:str = ""
        cost_bezeich:str = ""
        cost_acct:str = ""
        create_it:bool = False
        testa:decimal = 0
        Gl_acct1 = Gl_acct
        art_bestand_list.clear()

        l_besthis_obj_list = []
        for l_besthis, l_artikel, l_untergrup in db_session.query(L_besthis, L_artikel, L_untergrup).join(L_artikel,(L_artikel.artnr == L_besthis.artnr) &  (L_artikel.endkum >= from_main) &  (L_artikel.endkum <= to_main)).join(L_untergrup,(L_untergrup.zwkum == l_artikel.zwkum)).filter(
                (L_besthis.lager_nr == 0) &  (L_besthis.anf_best_dat == from_date)).all():
            if l_besthis._recid in l_besthis_obj_list:
                continue
            else:
                l_besthis_obj_list.append(l_besthis._recid)

            art_bestand = query(art_bestand_list, filters=(lambda art_bestand :art_bestand.zwkum == l_untergrup.zwkum), first=True)

            if not art_bestand:
                art_bestand = Art_bestand()
                art_bestand_list.append(art_bestand)

                art_bestand.bezeich = l_untergrup.bezeich
                art_bestand.zwkum = l_untergrup.zwkum
                art_bestand.fibukonto = l_untergrup.fibukonto
                art_bestand.artnr = l_artikel.artnr
            art_bestand.inv_acct = l_untergrup.fibukonto
            art_bestand.prevval = art_bestand.prevval + l_besthis.val_anf_best
            prevval = prevval + l_besthis.val_anf_best
            art_bestand.actval = art_bestand.actval + l_besthis.val_anf_best
            testa = 0
            testa = l_besthis.val_anf_best

            for l_lager in db_session.query(L_lager).all():

                for l_ophis in db_session.query(L_ophis).filter(
                        (L_ophis.datum >= from_date) &  (L_ophis.datum <= to_date) &  (L_ophis.op_art == 1) &  (L_ophis.lager_nr == l_lager.lager_nr) &  (L_ophis.artnr == l_artikel.artnr) &  (not (L_ophis.fibukonto.op("~")(".*CANCELLED.*")))).all():

                    art_bestand = query(art_bestand_list, filters=(lambda art_bestand :art_bestand.zwkum == l_untergrup.zwkum), first=True)
                    inval = inval + l_ophis.warenwert
                    art_bestand.inval = art_bestand.inval + l_ophis.warenwert
                    art_bestand.actval = art_bestand.actval + l_ophis.warenwert
                    testa = testa + l_ophis.warenwert

                for l_ophis in db_session.query(L_ophis).filter(
                        (L_ophis.lager_nr == l_lager.lager_nr) &  (L_ophis.datum >= from_date) &  (L_ophis.datum <= to_date) &  (L_ophis.artnr >= 3000000) &  (L_ophis.artnr <= 9999999) &  (L_ophis.anzahl != 0) &  (L_ophis.op_art == 3) &  (L_ophis.artnr == l_artikel.artnr) &  (not (L_ophis.fibukonto.op("~")(".*CANCELLED.*")))).all():
                    it_exist = True
                    other_fibu = False

                    art_bestand = query(art_bestand_list, filters=(lambda art_bestand :art_bestand.zwkum == l_untergrup.zwkum), first=True)
                    outval = outval + l_ophis.warenwert
                    art_bestand.outval = art_bestand.outval + l_ophis.warenwert
                    art_bestand.actval = art_bestand.actval - l_ophis.warenwert
                    testa = testa - l_ophis.warenwert
        j = 0

        if sort_type == 1:

            for art_bestand in query(art_bestand_list):
                j = j + 1
                art_bestand.nr = j

        else:

            for art_bestand in query(art_bestand_list):
                j = j + 1
                art_bestand.nr = j

        actval = prevval + inval - outval
        art_bestand = Art_bestand()
        art_bestand_list.append(art_bestand)

        art_bestand.bezeich = "                   T O T A L"
        art_bestand.prevval = prevval
        art_bestand.inval = inval
        art_bestand.outval = outval
        art_bestand.actval = actval
        art_bestand.nr = 999

    def create_list1():

        nonlocal art_bestand_list, from_date, gl_acct, l_artikel, l_untergrup, l_besthis, l_lager, l_ophis
        nonlocal gl_acct1, l_oh


        nonlocal art_bestand, gl_acct1, l_oh
        nonlocal art_bestand_list

        zwkum:int = 0
        prevval:decimal = 0
        inval:decimal = 0
        outval:decimal = 0
        actval:decimal = 0
        bezeich:str = ""
        j:int = 0
        qty:decimal = 0
        qty0:decimal = 0
        val0:decimal = 0
        L_oh = L_besthis
        art_bestand_list.clear()

        l_besthis_obj_list = []
        for l_besthis, l_artikel, l_untergrup in db_session.query(L_besthis, L_artikel, L_untergrup).join(L_artikel,(L_artikel.artnr == L_besthis.artnr) &  (L_artikel.endkum >= from_main) &  (L_artikel.endkum <= to_main)).join(L_untergrup,(L_untergrup.zwkum == l_artikel.zwkum)).filter(
                (L_besthis.lager_nr == lager_no) &  (L_besthis.anf_best_dat == from_date)).all():
            if l_besthis._recid in l_besthis_obj_list:
                continue
            else:
                l_besthis_obj_list.append(l_besthis._recid)

            art_bestand = query(art_bestand_list, filters=(lambda art_bestand :art_bestand.zwkum == l_untergrup.zwkum), first=True)

            if not art_bestand:
                art_bestand = Art_bestand()
                art_bestand_list.append(art_bestand)

                art_bestand.bezeich = l_untergrup.bezeich
                art_bestand.zwkum = l_untergrup.zwkum
                art_bestand.fibukonto = l_untergrup.fibukonto
                art_bestand.artnr = l_artikel.artnr
            art_bestand.inv_acct = l_untergrup.fibukonto

            l_oh = db_session.query(L_oh).filter(
                    (L_oh.lager_nr == 0) &  (L_oh.artnr == l_besthis.artnr) &  (L_oh.anf_best_dat == from_date)).first()
            qty = l_besthis.anz_anf_best + l_besthis.anz_eingang - l_besthis.anz_ausgang
            qty0 = l_oh.anz_anf_best + l_oh.anz_eingang - l_oh.anz_ausgang
            val0 = l_oh.val_anf_best + l_oh.wert_eingang - l_oh.wert_ausgang

            if qty0 != 0:
                art_bestand.actval = art_bestand.actval + (qty / qty0) * val0
            art_bestand.prevval = art_bestand.prevval + l_besthis.val_anf_best
            prevval = prevval + l_besthis.val_anf_best

            for l_ophis in db_session.query(L_ophis).filter(
                    (L_ophis.datum >= from_date) &  (L_ophis.datum <= to_date) &  (L_ophis.artnr == l_artikel.artnr) &  (L_ophis.op_art <= 2) &  (L_ophis.lager_nr == lager_no) &  (not (L_ophis.fibukonto.op("~")(".*CANCELLED.*")))).all():

                if l_ophis.op_art == 1:
                    inval = inval + l_ophis.warenwert
                    art_bestand.inval = art_bestand.inval + l_ophis.warenwert
                else:
                    inval = inval + l_ophis.anzahl * l_artikel.vk_preis
                    art_bestand.inval = art_bestand.inval + l_ophis.anzahl * l_artikel.vk_preis

            for l_ophis in db_session.query(L_ophis).filter(
                    (L_ophis.datum >= from_date) &  (L_ophis.datum <= to_date) &  (L_ophis.artnr == l_artikel.artnr) &  (L_ophis.op_art >= 3) &  (L_ophis.op_art <= 4) &  (L_ophis.lager_nr == lager_no) &  (not (L_ophis.fibukonto.op("~")(".*CANCELLED.*")))).all():

                if l_ophis.op_art == 3:
                    outval = outval + l_ophis.warenwert
                    art_bestand.outval = art_bestand.outval + l_ophis.warenwert
                else:
                    outval = outval + l_ophis.anzahl * l_artikel.vk_preis
                    art_bestand.outval = art_bestand.outval + l_ophis.anzahl * l_artikel.vk_preis
        j = 0

        if sort_type == 1:

            for art_bestand in query(art_bestand_list):
                j = j + 1
                art_bestand.nr = j

        else:

            for art_bestand in query(art_bestand_list):
                j = j + 1
                art_bestand.nr = j

        actval = 0

        for art_bestand in query(art_bestand_list):

            if art_bestand.prevval == 0 and art_bestand.inval == 0 and art_bestand.outval == 0:
                art_bestand_list.remove(art_bestand)
            else:
                art_bestand.adjust = (art_bestand.prevval + art_bestand.inval - art_bestand.outval) - art_bestand.actval
                actval = actval + art_bestand.actval
        art_bestand = Art_bestand()
        art_bestand_list.append(art_bestand)

        art_bestand.bezeich = "                   T O T A L"
        art_bestand.prevval = prevval
        art_bestand.inval = inval
        art_bestand.outval = outval
        art_bestand.actval = actval
        art_bestand.adjust = (prevval + inval - outval) - actval
        art_bestand.nr = 999


    from_date = date_mdy(get_month(to_date) , 1 , get_year(to_date))

    if lager_no == 0:
        create_list()
    else:
        create_list1()

    return generate_output()