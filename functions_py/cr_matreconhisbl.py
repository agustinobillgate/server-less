#using conversion tools version: 1.0.0.117
#-----------------------------------------
# Rd 23/7/2025
# gitlab: 659
# payload:
# {
#     "request": {
#         "toDate": "09/30/24",
#         "lagerNo": 0,
#         "fromMain": 3,
#         "toMain": 3,
#         "sortType": 1,
#         "inputUserkey": "95EE44CBF839764A7690C157AC66C9C902905E01",
#         "inputUsername": "it",
#         "hotel_schema": "qcserverless3"
#     }
# }
#-----------------------------------------
from functions.additional_functions import *
from decimal import Decimal, ROUND_HALF_UP, ROUND_HALF_DOWN
from datetime import date
from sqlalchemy import func
from models import Gl_acct, L_artikel, L_untergrup, L_besthis, L_lager, L_ophis
from sqlalchemy import and_, not_, func


def cr_matreconhisbl(to_date:date, lager_no:int, from_main:int, to_main:int, sort_type:int):

    prepare_cache ([L_artikel, L_untergrup, L_besthis, L_lager, L_ophis])

    art_bestand_data = []
    from_date:date = get_current_date()
    gl_acct = l_artikel = l_untergrup = l_besthis = l_lager = l_ophis = None

    art_bestand = None

    art_bestand_data, Art_bestand = create_model("Art_bestand", {"nr":int, "zwkum":int, "bezeich":string, "prevval":Decimal, "adjust":Decimal, "inval":Decimal, "outval":Decimal, "actval":Decimal, "inv_acct":string, "fibukonto":string, "artnr":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal art_bestand_data, from_date, gl_acct, l_artikel, l_untergrup, l_besthis, l_lager, l_ophis
        nonlocal to_date, lager_no, from_main, to_main, sort_type


        nonlocal art_bestand
        nonlocal art_bestand_data

        return {"art-bestand": art_bestand_data}

    def custom_rounding(dec:Decimal, format_data:str, is_up:bool = True):
        if is_up:
            return dec.quantize(Decimal(format_data), rounding=ROUND_HALF_UP)
        else:
            return dec.quantize(Decimal(format_data), rounding=ROUND_HALF_DOWN)

    def create_list():

        nonlocal art_bestand_data, from_date, gl_acct, l_artikel, l_untergrup, l_besthis, l_lager, l_ophis
        nonlocal to_date, lager_no, from_main, to_main, sort_type


        nonlocal art_bestand
        nonlocal art_bestand_data

        zwkum:int = 0
        prevval:Decimal = to_decimal("0.0")
        inval:Decimal = to_decimal("0.0")
        outval:Decimal = to_decimal("0.0")
        actval:Decimal = to_decimal("0.0")
        bezeich:string = ""
        j:int = 0
        other_fibu:bool = False
        it_exist:bool = False
        fibukonto:string = ""
        cost_bezeich:string = ""
        cost_acct:string = ""
        create_it:bool = False
        gl_acct1 = None
        Gl_acct1 =  create_buffer("Gl_acct1",Gl_acct)
        art_bestand_data.clear()

        l_besthis_obj_list = {}
        l_besthis = L_besthis()
        l_artikel = L_artikel()
        l_untergrup = L_untergrup()

        for l_besthis.val_anf_best, l_besthis.artnr, l_besthis.anz_anf_best, l_besthis.anz_eingang, l_besthis.anz_ausgang, l_besthis._recid, l_besthis.wert_eingang, l_besthis.wert_ausgang, l_artikel.artnr, l_artikel.bezeich, l_artikel.vk_preis, l_artikel._recid, l_untergrup.zwkum, l_untergrup.bezeich, l_untergrup.fibukonto, l_untergrup._recid in db_session.query(L_besthis.val_anf_best, L_besthis.artnr, L_besthis.anz_anf_best, L_besthis.anz_eingang, L_besthis.anz_ausgang, L_besthis._recid, L_besthis.wert_eingang, L_besthis.wert_ausgang, L_artikel.artnr, L_artikel.bezeich, L_artikel.vk_preis, L_artikel._recid, L_untergrup.zwkum, L_untergrup.bezeich, L_untergrup.fibukonto, L_untergrup._recid).join(L_artikel,(L_artikel.artnr == L_besthis.artnr) & (L_artikel.endkum >= from_main) & (L_artikel.endkum <= to_main)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum)).filter((L_besthis.lager_nr == 0) & (L_besthis.anf_best_dat == from_date)).order_by(L_besthis._recid).all():

            # if l_besthis_obj_list.get(l_besthis._recid):
            #     continue
            # else:
            #     l_besthis_obj_list[l_besthis._recid] = True

            art_bestand = query(art_bestand_data, filters=(lambda art_bestand: art_bestand.zwkum == l_untergrup.zwkum), first=True)

            if not art_bestand:
                art_bestand = Art_bestand()
                art_bestand_data.append(art_bestand)

                art_bestand.bezeich = l_untergrup.bezeich
                art_bestand.zwkum = l_untergrup.zwkum
                art_bestand.fibukonto = l_untergrup.fibukonto
                art_bestand.artnr = l_artikel.artnr

            art_bestand.inv_acct = l_untergrup.fibukonto
            art_bestand.prevval =  to_decimal(art_bestand.prevval) + to_decimal(l_besthis.val_anf_best)
            prevval =  to_decimal(prevval) + to_decimal(l_besthis.val_anf_best)
            art_bestand.actval =  to_decimal(art_bestand.actval) + to_decimal(l_besthis.val_anf_best)

            for l_ophis, l_lager in db_session.query(L_ophis, L_lager).join(L_lager, L_ophis.lager_nr == L_lager.lager_nr).filter((L_ophis.datum >= from_date) & (L_ophis.datum <= to_date) & (L_ophis.artnr >= 1000000) & (L_ophis.artnr <= 9999999) & (L_ophis.anzahl != 0) & (L_ophis.op_art <= 2) & (L_ophis.artnr == l_artikel.artnr) & (not_(matches(L_ophis.fibukonto,"*CANCELLED*")))).order_by(func.substr(L_ophis.lscheinnr, 3, 12)).all():

                art_bestand = query(art_bestand_data, filters=(lambda art_bestand: art_bestand.zwkum == l_untergrup.zwkum), first=True)

                inval =  to_decimal(inval) + to_decimal(l_ophis.warenwert)
                art_bestand.inval =  to_decimal(art_bestand.inval) + to_decimal(l_ophis.warenwert)
                art_bestand.actval =  to_decimal(art_bestand.actval) + to_decimal(l_ophis.warenwert)

            
                
            # qquery = (
            #     db_session.query(L_ophis)
            #     .join(L_artikel, L_ophis.artnr == L_artikel.artnr)
            #     .filter(
            #         L_ophis.lager_nr == l_lager.lager_nr,
            #         L_ophis.datum >= from_date,
            #         L_ophis.datum <= to_date,
            #         L_ophis.artnr >= 1000000,
            #         L_ophis.artnr <= 9999999,
            #         L_ophis.anzahl != 0,
            #         L_ophis.op_art >= 3,
            #         L_ophis.op_art <= 4,
            #         not_(L_ophis.fibukonto.like('%CANCELLED%'))
            #     )
            #     .order_by(
            #         func.substring(L_ophis.lscheinnr, 4, 12),
            #         L_artikel.bezeich
            #     )
            # )

            # result_list = qquery.all()
            # for l_ophis in result_list:

            for l_ophis, l_lager in db_session.query(L_ophis, L_lager).join(L_lager, L_ophis.lager_nr == L_lager.lager_nr).filter((L_ophis.datum >= from_date) & (L_ophis.datum <= to_date) & (L_ophis.artnr >= 1000000) & (L_ophis.artnr <= 9999999) & (L_ophis.anzahl != 0) & (L_ophis.op_art >= 3) & (L_ophis.op_art <= 4) & (L_ophis.artnr == l_artikel.artnr) & (not_(matches(L_ophis.fibukonto,"*CANCELLED*")))).order_by(func.substr(L_ophis.lscheinnr, 3, 12)).all():

                it_exist = True
                other_fibu = False

                art_bestand = query(art_bestand_data, filters=(lambda art_bestand: art_bestand.zwkum == l_untergrup.zwkum), first=True)

                outval =  to_decimal(outval) + to_decimal(l_ophis.warenwert)
                art_bestand.outval =  to_decimal(art_bestand.outval) + to_decimal(l_ophis.warenwert)
                art_bestand.actval =  to_decimal(art_bestand.actval) - to_decimal(l_ophis.warenwert)

        j = 0

        if sort_type == 1:
            for art_bestand in query(art_bestand_data, sort_by=[("fibukonto",False),("artnr",False)]):
                j = j + 1
                art_bestand.nr = j
        else:
            for art_bestand in query(art_bestand_data, sort_by=[("bezeich",False),("artnr",False)]):
                j = j + 1
                art_bestand.nr = j

        actval =  to_decimal(prevval) + to_decimal(inval) - to_decimal(outval)
        art_bestand = Art_bestand()
        art_bestand_data.append(art_bestand)

        art_bestand.bezeich = " T O T A L"
        art_bestand.prevval =  to_decimal(prevval)
        art_bestand.inval =  to_decimal(inval)
        art_bestand.outval =  to_decimal(outval)
        art_bestand.actval =  to_decimal(actval)
        art_bestand.nr = 999


    def create_list1():

        nonlocal art_bestand_data, from_date, gl_acct, l_artikel, l_untergrup, l_besthis, l_lager, l_ophis
        nonlocal to_date, lager_no, from_main, to_main, sort_type


        nonlocal art_bestand
        nonlocal art_bestand_data

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
        L_oh =  create_buffer("L_oh",L_besthis)
        art_bestand_data.clear()

        l_besthis_obj_list = {}
        l_besthis = L_besthis()
        l_artikel = L_artikel()
        l_untergrup = L_untergrup()

        for l_besthis.val_anf_best, l_besthis.artnr, l_besthis.anz_anf_best, l_besthis.anz_eingang, l_besthis.anz_ausgang, l_besthis._recid, l_besthis.wert_eingang, l_besthis.wert_ausgang, l_artikel.artnr, l_artikel.bezeich, l_artikel.vk_preis, l_artikel._recid, l_untergrup.zwkum, l_untergrup.bezeich, l_untergrup.fibukonto, l_untergrup._recid in db_session.query(L_besthis.val_anf_best, L_besthis.artnr, L_besthis.anz_anf_best, L_besthis.anz_eingang, L_besthis.anz_ausgang, L_besthis._recid, L_besthis.wert_eingang, L_besthis.wert_ausgang, L_artikel.artnr, L_artikel.bezeich, L_artikel.vk_preis, L_artikel._recid, L_untergrup.zwkum, L_untergrup.bezeich, L_untergrup.fibukonto, L_untergrup._recid).join(L_artikel,(L_artikel.artnr == L_besthis.artnr) & (L_artikel.endkum >= from_main) & (L_artikel.endkum <= to_main)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum)).filter((L_besthis.lager_nr == lager_no) & (L_besthis.anf_best_dat == from_date)).order_by(L_besthis._recid).all():

            # if l_besthis_obj_list.get(l_besthis._recid):
            #     continue
            # else:
            #     l_besthis_obj_list[l_besthis._recid] = True

            art_bestand = query(art_bestand_data, filters=(lambda art_bestand: art_bestand.zwkum == l_untergrup.zwkum), first=True)

            if not art_bestand:
                art_bestand = Art_bestand()
                art_bestand_data.append(art_bestand)

                art_bestand.bezeich = l_untergrup.bezeich
                art_bestand.zwkum = l_untergrup.zwkum
                art_bestand.fibukonto = l_untergrup.fibukonto
                art_bestand.artnr = l_artikel.artnr

            art_bestand.inv_acct = l_untergrup.fibukonto

            l_oh = get_cache (L_besthis, {"lager_nr": [(eq, 0)],"artnr": [(eq, l_besthis.artnr)],"anf_best_dat": [(eq, from_date)]})
            qty =  l_besthis.anz_anf_best + l_besthis.anz_eingang - l_besthis.anz_ausgang
            qty0 =  l_oh.anz_anf_best + l_oh.anz_eingang - l_oh.anz_ausgang
            val0 =  l_oh.val_anf_best + l_oh.wert_eingang - l_oh.wert_ausgang

            if qty0 != 0:
                art_bestand.actval =  art_bestand.actval + custom_rounding((custom_rounding((qty / qty0), "0.0000000001") * val0), "0.0000000001")

            art_bestand.prevval =  art_bestand.prevval + l_besthis.val_anf_best
            prevval =  prevval + l_besthis.val_anf_best

            for l_ophis in db_session.query(L_ophis).filter((L_ophis.datum >= from_date) & (L_ophis.datum <= to_date) & (L_ophis.artnr == l_artikel.artnr) & (L_ophis.op_art <= 2) & (L_ophis.lager_nr == lager_no) & (not_(matches(L_ophis.fibukonto,"*CANCELLED*")))).order_by(L_ophis._recid).all():

                if l_ophis.op_art == 1:
                    inval =  inval + l_ophis.warenwert
                    art_bestand.inval =  art_bestand.inval + l_ophis.warenwert
                else:
                    inval =  inval + custom_rounding((l_ophis.anzahl * l_artikel.vk_preis), "0.0000000001")
                    art_bestand.inval =  art_bestand.inval + custom_rounding((l_ophis.anzahl * l_artikel.vk_preis), "0.0000000001")

            for l_ophis in db_session.query(L_ophis).filter((L_ophis.datum >= from_date) & (L_ophis.datum <= to_date) & (L_ophis.artnr == l_artikel.artnr) & (L_ophis.op_art >= 3) & (L_ophis.op_art <= 4) & (L_ophis.lager_nr == lager_no) & (not_(matches(L_ophis.fibukonto,"*CANCELLED*")))).order_by(L_ophis._recid).all():

                if l_ophis.op_art == 3:
                    outval =  outval + l_ophis.warenwert
                    art_bestand.outval =  art_bestand.outval + l_ophis.warenwert
                else:
                    outval =  outval + custom_rounding((l_ophis.anzahl * l_artikel.vk_preis), "0.0000000001")
                    art_bestand.outval =  art_bestand.outval + custom_rounding((l_ophis.anzahl * l_artikel.vk_preis), "0.0000000001")

        j = 0

        if sort_type == 1:
            for art_bestand in query(art_bestand_data, sort_by=[("fibukonto",False),("artnr",False)]):
                j = j + 1
                art_bestand.nr = j
        else:
            for art_bestand in query(art_bestand_data, sort_by=[("bezeich",False),("artnr",False)]):
                j = j + 1
                art_bestand.nr = j

        actval =  to_decimal("0")

        tmp_art_bestand_list = list()

        for art_bestand in query(art_bestand_data):

            if art_bestand.prevval == 0 and art_bestand.inval == 0 and art_bestand.outval == 0:
                # art_bestand_data.remove(art_bestand)
                pass
            else:
                art_bestand.adjust = ( art_bestand.prevval + art_bestand.inval - art_bestand.outval) - art_bestand.actval
                actval =  actval + art_bestand.actval

                tmp_art_bestand_list.append(art_bestand)

        art_bestand_data = tmp_art_bestand_list

        art_bestand = Art_bestand()
        art_bestand_data.append(art_bestand)

        art_bestand.bezeich = " T O T A L"
        art_bestand.prevval =  prevval
        art_bestand.inval =  inval
        art_bestand.outval =  outval
        art_bestand.actval =  actval
        art_bestand.adjust = (prevval + inval - outval) - actval
        art_bestand.nr = 999

    from_date = date_mdy(get_month(to_date) , 1 , get_year(to_date))

    if lager_no == 0:
        create_list()
    else:
        create_list1()

    return generate_output()