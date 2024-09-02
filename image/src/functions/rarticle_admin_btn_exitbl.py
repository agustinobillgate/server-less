from functions.additional_functions import *
import decimal
from models import H_artikel, Queasy

def rarticle_admin_btn_exitbl(h_list:[H_list], case_type:int, fract_flag:bool, ask_voucher:bool, bezeich2:str):
    h_artikel = queasy = None

    h_list = None

    h_list_list, H_list = create_model_like(H_artikel)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal h_artikel, queasy


        nonlocal h_list
        nonlocal h_list_list
        return {}

    def fill_artikel():

        nonlocal h_artikel, queasy


        nonlocal h_list
        nonlocal h_list_list


        h_artikel.artnr = h_list.artnr
        h_artikel.departement = h_list.departement
        h_artikel.bezaendern = h_list.bezaendern
        h_artikel.bezeich = h_list.bezeich
        h_artikel.zwkum = h_list.zwkum
        h_artikel.endkum = h_list.endkum
        h_artikel.epreis1 = h_list.epreis1
        h_artikel.abbuchung = h_list.abbuchung
        h_artikel.autosaldo = h_list.autosaldo
        h_artikel.artart = h_list.artart
        h_artikel.epreis2 = h_list.epreis2
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
        h_artikel.prozent = h_list.prozent
        h_artikel.lagernr = h_list.lagernr
        h_artikel.betriebsnr = h_list.betriebsnr
        h_artikel.bondruckernr[3] = to_int(ask_voucher)

        if bezeich2 == "":

            queasy = db_session.query(Queasy).filter(
                    (Queasy.key == 38) &  (Queasy.number1 == h_list.departement) &  (Queasy.number2 == h_list.artnr)).first()

            if queasy:
                db_session.delete(queasy)
        else:

            queasy = db_session.query(Queasy).filter(
                    (Queasy.key == 38) &  (Queasy.number1 == h_list.departement) &  (Queasy.number2 == h_list.artnr)).first()

            if not queasy:
                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 38
                queasy.number1 = h_list.departement
                queasy.number2 = h_list.artnr


            queasy.char3 = bezeich2

            queasy = db_session.query(Queasy).first()

    h_list = query(h_list_list, first=True)

    if case_type == 1:
        h_artikel = H_artikel()
        db_session.add(h_artikel)

        fill_artikel()

    elif case_type == 2:

        h_artikel = db_session.query(H_artikel).filter(
                (H_artikel.artnr == h_list.artnr) &  (H_artikel.departement == h_list.departement)).first()

        if h_artikel:
            fill_artikel()

            h_artikel = db_session.query(H_artikel).first()

    return generate_output()