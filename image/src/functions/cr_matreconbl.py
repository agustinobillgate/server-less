from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Htparam, L_artikel, L_untergrup, L_bestand, L_lager, L_op, L_ophdr, Gl_acct

def cr_matreconbl(pvilanguage:int, to_date:date, lager_no:int, from_main:int, to_main:int, sort_type:int):
    art_bestand_list = []
    long_digit:bool = False
    from_date:date = get_current_date()
    lvcarea:str = "mat_reconsile"
    htparam = l_artikel = l_untergrup = l_bestand = l_lager = l_op = l_ophdr = gl_acct = None

    art_bestand = l_oh = None

    art_bestand_list, Art_bestand = create_model("Art_bestand", {"nr":int, "zwkum":int, "bezeich":str, "prevval":decimal, "adjust":decimal, "inval":decimal, "outval":decimal, "actval":decimal, "inv_acct":str, "fibukonto":str, "artnr":int})

    L_oh = L_bestand

    db_session = local_storage.db_session

    def generate_output():
        nonlocal art_bestand_list, long_digit, from_date, lvcarea, htparam, l_artikel, l_untergrup, l_bestand, l_lager, l_op, l_ophdr, gl_acct
        nonlocal l_oh


        nonlocal art_bestand, l_oh
        nonlocal art_bestand_list
        return {"art-bestand": art_bestand_list}

    def create_list():

        nonlocal art_bestand_list, long_digit, from_date, lvcarea, htparam, l_artikel, l_untergrup, l_bestand, l_lager, l_op, l_ophdr, gl_acct
        nonlocal l_oh


        nonlocal art_bestand, l_oh
        nonlocal art_bestand_list

        zwkum:int = 0
        prevval:decimal = 0
        inval:decimal = 0
        outval:decimal = 0
        actval:decimal = 0
        bezeich:str = ""
        j:int = 0
        art_bestand_list.clear()

        l_bestand_obj_list = []
        for l_bestand, l_artikel, l_untergrup in db_session.query(L_bestand, L_artikel, L_untergrup).join(L_artikel,(L_artikel.artnr == L_bestand.artnr) &  (L_artikel.endkum >= from_main) &  (L_artikel.endkum <= to_main)).join(L_untergrup,(L_untergrup.zwkum == l_artikel.zwkum)).filter(
                (L_bestand.lager_nr == 0)).all():
            if l_bestand._recid in l_bestand_obj_list:
                continue
            else:
                l_bestand_obj_list.append(l_bestand._recid)

            art_bestand = query(art_bestand_list, filters=(lambda art_bestand :art_bestand.zwkum == l_untergrup.zwkum), first=True)

            if not art_bestand:
                art_bestand = Art_bestand()
                art_bestand_list.append(art_bestand)

                art_bestand.bezeich = l_untergrup.bezeich
                art_bestand.zwkum = l_untergrup.zwkum
                art_bestand.fibukonto = l_untergrup.fibukonto
                art_bestand.artnr = l_artikel.artnr
            art_bestand.inv_acct = l_untergrup.fibukonto
            art_bestand.prevval = art_bestand.prevval + l_bestand.val_anf_best
            prevval = prevval + l_bestand.val_anf_best
            art_bestand.actval = art_bestand.actval + l_bestand.val_anf_best

            for l_lager in db_session.query(L_lager).all():

                for l_op in db_session.query(L_op).filter(
                        (L_op.datum >= from_date) &  (L_op.datum <= to_date) &  (L_op.artnr == l_artikel.artnr) &  (L_op.op_art == 1) &  (L_op.lager_nr == l_lager.lager_nr) &  (L_op.loeschflag <= 1)).all():
                    inval = inval + l_op.warenwert
                    art_bestand.inval = art_bestand.inval + l_op.warenwert
                    art_bestand.actval = art_bestand.actval + l_op.warenwert

                l_op_obj_list = []
                for l_op, l_ophdr, gl_acct in db_session.query(L_op, L_ophdr, Gl_acct).join(L_ophdr,(L_ophdr.lscheinnr == L_op.lscheinnr) &  (func.lower(L_ophdr.op_typ) == "STT") &  (L_ophdr.fibukonto != "")).join(Gl_acct,(Gl_acct.fibukonto == L_op.stornogrund)).filter(
                        (L_op.datum >= from_date) &  (L_op.datum <= to_date) &  (L_op.artnr == l_artikel.artnr) &  (L_op.op_art == 3) &  (L_op.lager_nr == l_lager.lager_nr) &  (L_op.loeschflag <= 1)).all():
                    if l_op._recid in l_op_obj_list:
                        continue
                    else:
                        l_op_obj_list.append(l_op._recid)


                    outval = outval + l_op.warenwert
                    art_bestand.outval = art_bestand.outval + l_op.warenwert
                    art_bestand.actval = art_bestand.actval - l_op.warenwert
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

        nonlocal art_bestand_list, long_digit, from_date, lvcarea, htparam, l_artikel, l_untergrup, l_bestand, l_lager, l_op, l_ophdr, gl_acct
        nonlocal l_oh


        nonlocal art_bestand, l_oh
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
        L_oh = L_bestand
        art_bestand_list.clear()

        l_bestand_obj_list = []
        for l_bestand, l_artikel, l_untergrup in db_session.query(L_bestand, L_artikel, L_untergrup).join(L_artikel,(L_artikel.artnr == L_bestand.artnr) &  (L_artikel.endkum >= from_main) &  (L_artikel.endkum <= to_main)).join(L_untergrup,(L_untergrup.zwkum == l_artikel.zwkum)).filter(
                (L_bestand.lager_nr == lager_no)).all():
            if l_bestand._recid in l_bestand_obj_list:
                continue
            else:
                l_bestand_obj_list.append(l_bestand._recid)

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
                    (L_oh.lager_nr == 0) &  (L_oh.artnr == l_bestand.artnr)).first()
            qty = l_bestand.anz_anf_best + l_bestand.anz_eingang - l_bestand.anz_ausgang
            qty0 = l_oh.anz_anf_best + l_oh.anz_eingang - l_oh.anz_ausgang
            val0 = l_oh.val_anf_best + l_oh.wert_eingang - l_oh.wert_ausgang

            if qty0 != 0:
                art_bestand.actval = art_bestand.actval + (qty / qty0) * val0
            art_bestand.prevval = art_bestand.prevval + l_bestand.val_anf_best
            prevval = prevval + l_bestand.val_anf_best

            for l_op in db_session.query(L_op).filter(
                    (L_op.datum >= from_date) &  (L_op.datum <= to_date) &  (L_op.artnr == l_artikel.artnr) &  (L_op.op_art <= 2) &  (L_op.lager_nr == lager_no) &  (L_op.loeschflag <= 1)).all():

                if l_op.op_art == 1:
                    inval = inval + l_op.warenwert
                    art_bestand.inval = art_bestand.inval + l_op.warenwert
                else:
                    inval = inval + l_op.anzahl * l_artikel.vk_preis
                    art_bestand.inval = art_bestand.inval + l_op.anzahl * l_artikel.vk_preis

            for l_op in db_session.query(L_op).filter(
                    (L_op.datum >= from_date) &  (L_op.datum <= to_date) &  (L_op.artnr == l_artikel.artnr) &  (L_op.op_art >= 3) &  (L_op.op_art <= 4) &  (L_op.lager_nr == lager_no) &  (L_op.loeschflag <= 1)).all():

                if l_op.op_art == 3:
                    outval = outval + l_op.warenwert
                    art_bestand.outval = art_bestand.outval + l_op.warenwert
                else:
                    outval = outval + l_op.anzahl * l_artikel.vk_preis
                    art_bestand.outval = art_bestand.outval + l_op.anzahl * l_artikel.vk_preis
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
                art_bestand.adjust = art_bestand.actval - (art_bestand.prevval + art_bestand.inval - art_bestand.outval)
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

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 246)).first()
    long_digit = htparam.flogical
    from_date = date_mdy(get_month(to_date) , 1 , get_year(to_date))

    if lager_no == 0:
        create_list()
    else:
        create_list1()

    return generate_output()