from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import L_artikel, L_bestand

def select_sartnr2_1bl(curr_lager:int, recipe:bool, sorttype:int, s_artnr:int, s_bezeich:str):
    sartnr_list_list = []
    l_artikel = l_bestand = None

    sartnr_list = None

    sartnr_list_list, Sartnr_list = create_model("Sartnr_list", {"artnr":int, "bezeich":str, "anz_anf_best":decimal, "anz_eingang":decimal, "anz_ausgang":decimal, "masseinheit":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal sartnr_list_list, l_artikel, l_bestand


        nonlocal sartnr_list
        nonlocal sartnr_list_list
        return {"sartnr-list": sartnr_list_list}

    if curr_lager == 0:

        if sorttype == 1:

            for l_artikel in db_session.query(L_artikel).filter(
                    (L_artikel.artnr >= s_artnr)).all():
                sartnr_list = Sartnr_list()
                sartnr_list_list.append(sartnr_list)

                buffer_copy(l_artikel, sartnr_list)
        else:

            if substring(s_bezeich, 0, 1) != "*":

                for l_artikel in db_session.query(L_artikel).filter(
                        (func.lower(L_artikel.bezeich) >= (s_bezeich).lower())).all():
                    sartnr_list = Sartnr_list()
                    sartnr_list_list.append(sartnr_list)

                    buffer_copy(l_artikel, sartnr_list)

            else:

                if substring(s_bezeich, len(s_bezeich) - 1, 1) != "*":
                    s_bezeich = s_bezeich + "*"

                for l_artikel in db_session.query(L_artikel).filter(
                        (L_artikel.bezeich.op("~")(s_bezeich))).all():
                    sartnr_list = Sartnr_list()
                    sartnr_list_list.append(sartnr_list)

                    buffer_copy(l_artikel, sartnr_list)

        return generate_output()

    if not recipe:

        if sorttype == 1:

            l_artikel_obj_list = []
            for l_artikel, l_bestand in db_session.query(L_artikel, L_bestand).join(L_bestand,(L_bestand.artnr == L_artikel.artnr) &  (L_bestand.lager_nr == curr_lager)).filter(
                    (L_artikel.artnr >= s_artnr)).all():
                if l_artikel._recid in l_artikel_obj_list:
                    continue
                else:
                    l_artikel_obj_list.append(l_artikel._recid)


                sartnr_list = Sartnr_list()
                sartnr_list_list.append(sartnr_list)

                buffer_copy(l_artikel, sartnr_list)
                buffer_copy(l_bestand, sartnr_list)
        else:

            if substring(s_bezeich, 0, 1) != "*":

                l_artikel_obj_list = []
                for l_artikel, l_bestand in db_session.query(L_artikel, L_bestand).join(L_bestand,(L_bestand.artnr == L_artikel.artnr) &  (L_bestand.lager_nr == curr_lager)).filter(
                        (func.lower(L_artikel.bezeich) >= (s_bezeich).lower())).all():
                    if l_artikel._recid in l_artikel_obj_list:
                        continue
                    else:
                        l_artikel_obj_list.append(l_artikel._recid)


                    sartnr_list = Sartnr_list()
                    sartnr_list_list.append(sartnr_list)

                    buffer_copy(l_artikel, sartnr_list)
                    buffer_copy(l_bestand, sartnr_list)

            else:

                if substring(s_bezeich, len(s_bezeich) - 1, 1) != "*":
                    s_bezeich = s_bezeich + "*"

                l_artikel_obj_list = []
                for l_artikel, l_bestand in db_session.query(L_artikel, L_bestand).join(L_bestand,(L_bestand.artnr == L_artikel.artnr) &  (L_bestand.lager_nr == curr_lager)).filter(
                        (L_artikel.bezeich.op("~")(s_bezeich))).all():
                    if l_artikel._recid in l_artikel_obj_list:
                        continue
                    else:
                        l_artikel_obj_list.append(l_artikel._recid)


                    sartnr_list = Sartnr_list()
                    sartnr_list_list.append(sartnr_list)

                    buffer_copy(l_artikel, sartnr_list)
                    buffer_copy(l_bestand, sartnr_list)
    else:

        if sorttype == 1:

            for l_artikel in db_session.query(L_artikel).filter(
                    (L_artikel.artnr >= s_artnr) &  (L_artikel.betriebsnr != 0)).all():
                sartnr_list = Sartnr_list()
                sartnr_list_list.append(sartnr_list)

                buffer_copy(l_artikel, sartnr_list)
        else:

            for l_artikel in db_session.query(L_artikel).filter(
                    (func.lower(L_artikel.bezeich) >= (s_bezeich).lower()) &  (L_artikel.betriebsnr != 0)).all():
                sartnr_list = Sartnr_list()
                sartnr_list_list.append(sartnr_list)

                buffer_copy(l_artikel, sartnr_list)

    return generate_output()