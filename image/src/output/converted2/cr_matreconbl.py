#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, L_artikel, L_untergrup, L_bestand, L_lager, L_op, L_ophdr, Gl_acct

def cr_matreconbl(pvilanguage:int, to_date:date, lager_no:int, from_main:int, to_main:int, sort_type:int):

    prepare_cache ([Htparam, L_artikel, L_untergrup, L_bestand, L_op])

    art_bestand_list = []
    long_digit:bool = False
    from_date:date = get_current_date()
    lvcarea:string = "mat-reconsile"
    htparam = l_artikel = l_untergrup = l_bestand = l_lager = l_op = l_ophdr = gl_acct = None

    art_bestand = None

    art_bestand_list, Art_bestand = create_model("Art_bestand", {"nr":int, "zwkum":int, "bezeich":string, "prevval":Decimal, "adjust":Decimal, "inval":Decimal, "outval":Decimal, "actval":Decimal, "inv_acct":string, "fibukonto":string, "artnr":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal art_bestand_list, long_digit, from_date, lvcarea, htparam, l_artikel, l_untergrup, l_bestand, l_lager, l_op, l_ophdr, gl_acct
        nonlocal pvilanguage, to_date, lager_no, from_main, to_main, sort_type


        nonlocal art_bestand
        nonlocal art_bestand_list

        return {"art-bestand": art_bestand_list}

    def create_list():

        nonlocal art_bestand_list, long_digit, from_date, lvcarea, htparam, l_artikel, l_untergrup, l_bestand, l_lager, l_op, l_ophdr, gl_acct
        nonlocal pvilanguage, to_date, lager_no, from_main, to_main, sort_type


        nonlocal art_bestand
        nonlocal art_bestand_list

        zwkum:int = 0
        prevval:Decimal = to_decimal("0.0")
        inval:Decimal = to_decimal("0.0")
        outval:Decimal = to_decimal("0.0")
        actval:Decimal = to_decimal("0.0")
        bezeich:string = ""
        j:int = 0
        art_bestand_list.clear()

        l_bestand_obj_list = {}
        l_bestand = L_bestand()
        l_artikel = L_artikel()
        l_untergrup = L_untergrup()
        for l_bestand.val_anf_best, l_bestand.artnr, l_bestand.anz_anf_best, l_bestand.anz_eingang, l_bestand.anz_ausgang, l_bestand._recid, l_bestand.wert_eingang, l_bestand.wert_ausgang, l_artikel.artnr, l_artikel.vk_preis, l_artikel._recid, l_untergrup.zwkum, l_untergrup.bezeich, l_untergrup.fibukonto, l_untergrup._recid in db_session.query(L_bestand.val_anf_best, L_bestand.artnr, L_bestand.anz_anf_best, L_bestand.anz_eingang, L_bestand.anz_ausgang, L_bestand._recid, L_bestand.wert_eingang, L_bestand.wert_ausgang, L_artikel.artnr, L_artikel.vk_preis, L_artikel._recid, L_untergrup.zwkum, L_untergrup.bezeich, L_untergrup.fibukonto, L_untergrup._recid).join(L_artikel,(L_artikel.artnr == L_bestand.artnr) & (L_artikel.endkum >= from_main) & (L_artikel.endkum <= to_main)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum)).filter(
                 (L_bestand.lager_nr == 0)).order_by(L_untergrup.fibukonto, L_artikel.artnr).all():
            if l_bestand_obj_list.get(l_bestand._recid):
                continue
            else:
                l_bestand_obj_list[l_bestand._recid] = True

            art_bestand = query(art_bestand_list, filters=(lambda art_bestand: art_bestand.zwkum == l_untergrup.zwkum), first=True)

            if not art_bestand:
                art_bestand = Art_bestand()
                art_bestand_list.append(art_bestand)

                art_bestand.bezeich = l_untergrup.bezeich
                art_bestand.zwkum = l_untergrup.zwkum
                art_bestand.fibukonto = l_untergrup.fibukonto
                art_bestand.artnr = l_artikel.artnr
            art_bestand.inv_acct = l_untergrup.fibukonto
            art_bestand.prevval =  to_decimal(art_bestand.prevval) + to_decimal(l_bestand.val_anf_best)
            prevval =  to_decimal(prevval) + to_decimal(l_bestand.val_anf_best)
            art_bestand.actval =  to_decimal(art_bestand.actval) + to_decimal(l_bestand.val_anf_best)

            l_op_obj_list = {}
            for l_op, l_lager in db_session.query(L_op, L_lager).join(L_lager,(L_lager.lager_nr == L_op.lager_nr)).filter(
                     (L_op.datum >= from_date) & (L_op.datum <= to_date) & (L_op.artnr == l_artikel.artnr) & (L_op.op_art <= 4) & (L_op.loeschflag <= 1)).order_by(L_op._recid).all():
                if l_op_obj_list.get(l_op._recid):
                    continue
                else:
                    l_op_obj_list[l_op._recid] = True

                if l_op.op_art <= 2:

                    if l_op.op_art == 1:
                        inval =  to_decimal(inval) + to_decimal(l_op.warenwert)
                        art_bestand.inval =  to_decimal(art_bestand.inval) + to_decimal(l_op.warenwert)
                        art_bestand.actval =  to_decimal(art_bestand.actval) + to_decimal(l_op.warenwert)

                    if l_op.op_art == 2 and l_op.herkunftflag == 3:
                        inval =  to_decimal(inval) + to_decimal(l_op.anzahl) * to_decimal(l_artikel.vk_preis)
                        art_bestand.inval =  to_decimal(art_bestand.inval) + to_decimal(l_op.anzahl) * to_decimal(l_artikel.vk_preis)
                        art_bestand.actval =  to_decimal(art_bestand.actval) + to_decimal(l_op.anzahl) * to_decimal(l_artikel.vk_preis)

                elif l_op.op_art <= 4:

                    l_ophdr = get_cache (L_ophdr, {"lscheinnr": [(eq, l_op.lscheinnr)],"op_typ": [(eq, "stt")],"fibukonto": [(ne, "")]})

                    gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, l_op.stornogrund)]})

                    if l_ophdr and gl_acct:

                        if l_op.op_art == 3:
                            outval =  to_decimal(outval) + to_decimal(l_op.warenwert)
                            art_bestand.outval =  to_decimal(art_bestand.outval) + to_decimal(l_op.warenwert)
                            art_bestand.actval =  to_decimal(art_bestand.actval) - to_decimal(l_op.warenwert)

                        if l_op.op_art == 4 and l_op.herkunftflag == 3:
                            outval =  to_decimal(outval) + to_decimal(l_op.anzahl) * to_decimal(l_artikel.vk_preis)
                            art_bestand.outval =  to_decimal(art_bestand.outval) + to_decimal(l_op.anzahl) * to_decimal(l_artikel.vk_preis)
                            art_bestand.actval =  to_decimal(art_bestand.outval) - to_decimal(l_op.anzahl) * to_decimal(l_artikel.vk_preis)
        j = 0

        if sort_type == 1:

            for art_bestand in query(art_bestand_list, sort_by=[("fibukonto",False),("artnr",False)]):
                j = j + 1
                art_bestand.nr = j

        else:

            for art_bestand in query(art_bestand_list, sort_by=[("bezeich",False),("artnr",False)]):
                j = j + 1
                art_bestand.nr = j

        actval =  to_decimal(prevval) + to_decimal(inval) - to_decimal(outval)
        art_bestand = Art_bestand()
        art_bestand_list.append(art_bestand)

        art_bestand.bezeich = " T O T A L"
        art_bestand.prevval =  to_decimal(prevval)
        art_bestand.inval =  to_decimal(inval)
        art_bestand.outval =  to_decimal(outval)
        art_bestand.actval =  to_decimal(actval)
        art_bestand.nr = 999


    def create_list1():

        nonlocal art_bestand_list, long_digit, from_date, lvcarea, htparam, l_artikel, l_untergrup, l_bestand, l_lager, l_op, l_ophdr, gl_acct
        nonlocal pvilanguage, to_date, lager_no, from_main, to_main, sort_type


        nonlocal art_bestand
        nonlocal art_bestand_list

        zwkum:int = 0
        prevval:Decimal = to_decimal("0.0")
        inval:Decimal = to_decimal("0.0")
        outval:Decimal = to_decimal("0.0")
        actval:Decimal = to_decimal("0.0")
        bezeich:string = ""
        j:int = 0
        qty:Decimal = to_decimal("0.0")
        qty0:Decimal = to_decimal("0.0")
        val0:Decimal = to_decimal("0.0")
        l_oh = None
        L_oh =  create_buffer("L_oh",L_bestand)
        art_bestand_list.clear()

        l_bestand_obj_list = {}
        l_bestand = L_bestand()
        l_artikel = L_artikel()
        l_untergrup = L_untergrup()
        for l_bestand.val_anf_best, l_bestand.artnr, l_bestand.anz_anf_best, l_bestand.anz_eingang, l_bestand.anz_ausgang, l_bestand._recid, l_bestand.wert_eingang, l_bestand.wert_ausgang, l_artikel.artnr, l_artikel.vk_preis, l_artikel._recid, l_untergrup.zwkum, l_untergrup.bezeich, l_untergrup.fibukonto, l_untergrup._recid in db_session.query(L_bestand.val_anf_best, L_bestand.artnr, L_bestand.anz_anf_best, L_bestand.anz_eingang, L_bestand.anz_ausgang, L_bestand._recid, L_bestand.wert_eingang, L_bestand.wert_ausgang, L_artikel.artnr, L_artikel.vk_preis, L_artikel._recid, L_untergrup.zwkum, L_untergrup.bezeich, L_untergrup.fibukonto, L_untergrup._recid).join(L_artikel,(L_artikel.artnr == L_bestand.artnr) & (L_artikel.endkum >= from_main) & (L_artikel.endkum <= to_main)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum)).filter(
                 (L_bestand.lager_nr == lager_no)).order_by(L_untergrup.fibukonto, L_artikel.artnr).all():
            if l_bestand_obj_list.get(l_bestand._recid):
                continue
            else:
                l_bestand_obj_list[l_bestand._recid] = True

            art_bestand = query(art_bestand_list, filters=(lambda art_bestand: art_bestand.zwkum == l_untergrup.zwkum), first=True)

            if not art_bestand:
                art_bestand = Art_bestand()
                art_bestand_list.append(art_bestand)

                art_bestand.bezeich = l_untergrup.bezeich
                art_bestand.zwkum = l_untergrup.zwkum
                art_bestand.fibukonto = l_untergrup.fibukonto
                art_bestand.artnr = l_artikel.artnr
            art_bestand.inv_acct = l_untergrup.fibukonto

            l_oh = get_cache (L_bestand, {"lager_nr": [(eq, 0)],"artnr": [(eq, l_bestand.artnr)]})
            qty =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) - to_decimal(l_bestand.anz_ausgang)
            qty0 =  to_decimal(l_oh.anz_anf_best) + to_decimal(l_oh.anz_eingang) - to_decimal(l_oh.anz_ausgang)
            val0 =  to_decimal(l_oh.val_anf_best) + to_decimal(l_oh.wert_eingang) - to_decimal(l_oh.wert_ausgang)

            if qty0 != 0:
                art_bestand.actval =  to_decimal(art_bestand.actval) + to_decimal((qty) / to_decimal(qty0)) * to_decimal(val0)
            art_bestand.prevval =  to_decimal(art_bestand.prevval) + to_decimal(l_bestand.val_anf_best)
            prevval =  to_decimal(prevval) + to_decimal(l_bestand.val_anf_best)

            for l_op in db_session.query(L_op).filter(
                     (L_op.datum >= from_date) & (L_op.datum <= to_date) & (L_op.artnr == l_artikel.artnr) & (L_op.op_art <= 2) & (L_op.lager_nr == lager_no) & (L_op.loeschflag <= 1)).order_by(L_op._recid).all():

                if l_op.op_art == 1:
                    inval =  to_decimal(inval) + to_decimal(l_op.warenwert)
                    art_bestand.inval =  to_decimal(art_bestand.inval) + to_decimal(l_op.warenwert)
                else:
                    inval =  to_decimal(inval) + to_decimal(l_op.anzahl) * to_decimal(l_artikel.vk_preis)
                    art_bestand.inval =  to_decimal(art_bestand.inval) + to_decimal(l_op.anzahl) * to_decimal(l_artikel.vk_preis)

            for l_op in db_session.query(L_op).filter(
                     (L_op.datum >= from_date) & (L_op.datum <= to_date) & (L_op.artnr == l_artikel.artnr) & (L_op.op_art >= 3) & (L_op.op_art <= 4) & (L_op.lager_nr == lager_no) & (L_op.loeschflag <= 1)).order_by(L_op._recid).all():

                if l_op.op_art == 3:
                    outval =  to_decimal(outval) + to_decimal(l_op.warenwert)
                    art_bestand.outval =  to_decimal(art_bestand.outval) + to_decimal(l_op.warenwert)
                else:
                    outval =  to_decimal(outval) + to_decimal(l_op.anzahl) * to_decimal(l_artikel.vk_preis)
                    art_bestand.outval =  to_decimal(art_bestand.outval) + to_decimal(l_op.anzahl) * to_decimal(l_artikel.vk_preis)
        j = 0

        if sort_type == 1:

            for art_bestand in query(art_bestand_list, sort_by=[("fibukonto",False),("artnr",False)]):
                j = j + 1
                art_bestand.nr = j

        else:

            for art_bestand in query(art_bestand_list, sort_by=[("bezeich",False),("artnr",False)]):
                j = j + 1
                art_bestand.nr = j

        actval =  to_decimal("0")

        for art_bestand in query(art_bestand_list):

            if art_bestand.prevval == 0 and art_bestand.inval == 0 and art_bestand.outval == 0:
                art_bestand_list.remove(art_bestand)
            else:
                art_bestand.adjust =  to_decimal(art_bestand.actval) - to_decimal((art_bestand.prevval) + to_decimal(art_bestand.inval) - to_decimal(art_bestand.outval))
                actval =  to_decimal(actval) + to_decimal(art_bestand.actval)
        art_bestand = Art_bestand()
        art_bestand_list.append(art_bestand)

        art_bestand.bezeich = " T O T A L"
        art_bestand.prevval =  to_decimal(prevval)
        art_bestand.inval =  to_decimal(inval)
        art_bestand.outval =  to_decimal(outval)
        art_bestand.actval =  to_decimal(actval)
        art_bestand.adjust = ( to_decimal(prevval) + to_decimal(inval) - to_decimal(outval)) - to_decimal(actval)
        art_bestand.nr = 999


    htparam = get_cache (Htparam, {"paramnr": [(eq, 246)]})
    long_digit = htparam.flogical
    from_date = date_mdy(get_month(to_date) , 1 , get_year(to_date))

    if lager_no == 0:
        create_list()
    else:
        create_list1()

    return generate_output()