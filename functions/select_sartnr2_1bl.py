#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from sqlalchemy import func
from models import L_artikel, L_bestand

def select_sartnr2_1bl(curr_lager:int, recipe:bool, sorttype:int, s_artnr:int, s_bezeich:string):
    sartnr_list_data = []
    l_artikel = l_bestand = None

    sartnr_list = None

    sartnr_list_data, Sartnr_list = create_model("Sartnr_list", {"artnr":int, "bezeich":string, "anz_anf_best":Decimal, "anz_eingang":Decimal, "anz_ausgang":Decimal, "masseinheit":string, "is_receipt":bool, "hrecipe_nr":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal sartnr_list_data, l_artikel, l_bestand
        nonlocal curr_lager, recipe, sorttype, s_artnr, s_bezeich


        nonlocal sartnr_list
        nonlocal sartnr_list_data

        return {"sartnr-list": sartnr_list_data}

    if curr_lager == 0:

        if sorttype == 1:

            for l_artikel in db_session.query(L_artikel).filter(
                     (L_artikel.artnr >= s_artnr)).order_by(L_artikel.artnr).all():
                sartnr_list = Sartnr_list()
                sartnr_list_data.append(sartnr_list)

                buffer_copy(l_artikel, sartnr_list)
                sartnr_list.is_receipt = False
                sartnr_list.hrecipe_nr = 0
        else:

            if substring(s_bezeich, 0, 1) != ("*").lower() :

                for l_artikel in db_session.query(L_artikel).filter(
                         (L_artikel.bezeich >= (s_bezeich).lower())).order_by(L_artikel.bezeich).all():
                    sartnr_list = Sartnr_list()
                    sartnr_list_data.append(sartnr_list)

                    buffer_copy(l_artikel, sartnr_list)
                    sartnr_list.is_receipt = False
                    sartnr_list.hrecipe_nr = 0

            else:

                if substring(s_bezeich, length(s_bezeich) - 1, 1) != ("*").lower() :
                    s_bezeich = s_bezeich + "*"

                for l_artikel in db_session.query(L_artikel).filter(
                         (matches(L_artikel.bezeich,(s_bezeich)))).order_by(L_artikel.bezeich).all():
                    sartnr_list = Sartnr_list()
                    sartnr_list_data.append(sartnr_list)

                    buffer_copy(l_artikel, sartnr_list)
                    sartnr_list.is_receipt = False
                    sartnr_list.hrecipe_nr = 0

        return generate_output()

    if not recipe:

        if sorttype == 1:

            l_artikel_obj_list = {}
            for l_artikel, l_bestand in db_session.query(L_artikel, L_bestand).join(L_bestand,(L_bestand.artnr == L_artikel.artnr) & (L_bestand.lager_nr == curr_lager)).filter(
                     (L_artikel.artnr >= s_artnr)).order_by(L_artikel.artnr).all():
                if l_artikel_obj_list.get(l_artikel._recid):
                    continue
                else:
                    l_artikel_obj_list[l_artikel._recid] = True


                sartnr_list = Sartnr_list()
                sartnr_list_data.append(sartnr_list)

                buffer_copy(l_artikel, sartnr_list)
                buffer_copy(l_bestand, sartnr_list)
                sartnr_list.is_receipt = False
                sartnr_list.hrecipe_nr = 0
        else:

            if substring(s_bezeich, 0, 1) != ("*").lower() :

                l_artikel_obj_list = {}
                for l_artikel, l_bestand in db_session.query(L_artikel, L_bestand).join(L_bestand,(L_bestand.artnr == L_artikel.artnr) & (L_bestand.lager_nr == curr_lager)).filter(
                         (L_artikel.bezeich >= (s_bezeich).lower())).order_by(L_artikel.bezeich).all():
                    if l_artikel_obj_list.get(l_artikel._recid):
                        continue
                    else:
                        l_artikel_obj_list[l_artikel._recid] = True


                    sartnr_list = Sartnr_list()
                    sartnr_list_data.append(sartnr_list)

                    buffer_copy(l_artikel, sartnr_list)
                    buffer_copy(l_bestand, sartnr_list)
                    sartnr_list.is_receipt = False
                    sartnr_list.hrecipe_nr = 0

            else:

                if substring(s_bezeich, length(s_bezeich) - 1, 1) != ("*").lower() :
                    s_bezeich = s_bezeich + "*"

                l_artikel_obj_list = {}
                for l_artikel, l_bestand in db_session.query(L_artikel, L_bestand).join(L_bestand,(L_bestand.artnr == L_artikel.artnr) & (L_bestand.lager_nr == curr_lager)).filter(
                         (matches(L_artikel.bezeich,(s_bezeich)))).order_by(L_artikel.bezeich).all():
                    if l_artikel_obj_list.get(l_artikel._recid):
                        continue
                    else:
                        l_artikel_obj_list[l_artikel._recid] = True


                    sartnr_list = Sartnr_list()
                    sartnr_list_data.append(sartnr_list)

                    buffer_copy(l_artikel, sartnr_list)
                    buffer_copy(l_bestand, sartnr_list)
                    sartnr_list.is_receipt = False
                    sartnr_list.hrecipe_nr = 0
    else:

        if sorttype == 1:

            for l_artikel in db_session.query(L_artikel).filter(
                     (L_artikel.artnr >= s_artnr) & (L_artikel.betriebsnr != 0)).order_by(L_artikel.artnr).all():
                sartnr_list = Sartnr_list()
                sartnr_list_data.append(sartnr_list)

                buffer_copy(l_artikel, sartnr_list)
                sartnr_list.is_receipt = True
                sartnr_list.hrecipe_nr = l_artikel.betriebsnr
        else:

            for l_artikel in db_session.query(L_artikel).filter(
                     (L_artikel.bezeich >= (s_bezeich).lower()) & (L_artikel.betriebsnr != 0)).order_by(L_artikel.bezeich).all():
                sartnr_list = Sartnr_list()
                sartnr_list_data.append(sartnr_list)

                buffer_copy(l_artikel, sartnr_list)
                sartnr_list.is_receipt = True
                sartnr_list.hrecipe_nr = l_artikel.betriebsnr

    return generate_output()