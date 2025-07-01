#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import H_artikel, Queasy

h_list_list, H_list = create_model_like(H_artikel)

def rarticle_admin_btn_exitbl(h_list_list:[H_list], case_type:int, fract_flag:bool, ask_voucher:bool, bezeich2:string):

    prepare_cache ([H_artikel])

    h_artikel = queasy = None

    h_list = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal h_artikel, queasy
        nonlocal case_type, fract_flag, ask_voucher, bezeich2


        nonlocal h_list

        return {}

    def fill_artikel():

        nonlocal h_artikel, queasy
        nonlocal case_type, fract_flag, ask_voucher, bezeich2


        nonlocal h_list


        h_artikel.artnr = h_list.artnr
        h_artikel.departement = h_list.departement
        h_artikel.bezaendern = h_list.bezaendern
        h_artikel.bezeich = h_list.bezeich
        h_artikel.zwkum = h_list.zwkum
        h_artikel.endkum = h_list.endkum
        h_artikel.epreis1 =  to_decimal(h_list.epreis1)
        h_artikel.abbuchung = h_list.abbuchung
        h_artikel.autosaldo = h_list.autosaldo
        h_artikel.artart = h_list.artart
        h_artikel.epreis2 =  to_decimal(h_list.epreis2)
        h_artikel.gang = to_int(fract_flag)
        h_artikel.bondruckernr[0] = h_list.bondruckernr[0]
        h_artikel.aenderwunsch = h_list.aenderwunsch
        h_artikel.artnrfront = h_list.artnrfront
        h_artikel.mwst_code = h_list.mwst_code
        h_artikel.service_code = h_list.service_code
        h_artikel.activeflag = h_list.activeflag
        h_artikel.s_gueltig = h_list.s_gueltig
        h_artikel.e_gueltig = h_list.e_gueltig
        h_artikel.artnrlager = h_list.artnrlager
        h_artikel.artnrrezept = h_list.artnrrezept
        h_artikel.prozent =  to_decimal(h_list.prozent)
        h_artikel.lagernr = h_list.lagernr
        h_artikel.betriebsnr = h_list.betriebsnr
        h_artikel.bondruckernr[3] = to_int(ask_voucher)

        if bezeich2 == "":

            queasy = get_cache (Queasy, {"key": [(eq, 38)],"number1": [(eq, h_list.departement)],"number2": [(eq, h_list.artnr)]})

            if queasy:
                db_session.delete(queasy)
        else:

            queasy = get_cache (Queasy, {"key": [(eq, 38)],"number1": [(eq, h_list.departement)],"number2": [(eq, h_list.artnr)]})

            if not queasy:
                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 38
                queasy.number1 = h_list.departement
                queasy.number2 = h_list.artnr


            queasy.char3 = bezeich2


            pass


    h_list = query(h_list_list, first=True)

    if case_type == 1:
        h_artikel = H_artikel()
        db_session.add(h_artikel)

        fill_artikel()

    elif case_type == 2:

        h_artikel = get_cache (H_artikel, {"artnr": [(eq, h_list.artnr)],"departement": [(eq, h_list.departement)]})

        if h_artikel:
            fill_artikel()
            pass

    return generate_output()