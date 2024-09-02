from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import H_artikel, Bediener, Res_history, Queasy

def rarticle_admin_btn_exit_2bl(h_list:[H_list], case_type:int, fract_flag:bool, ask_voucher:bool, bezeich2:str, barcode:str, user_init:str):
    v_log:bool = False
    h_artikel = bediener = res_history = queasy = None

    h_list = buff_hart = None

    h_list_list, H_list = create_model_like(H_artikel)

    Buff_hart = H_artikel

    db_session = local_storage.db_session

    def generate_output():
        nonlocal v_log, h_artikel, bediener, res_history, queasy
        nonlocal buff_hart


        nonlocal h_list, buff_hart
        nonlocal h_list_list
        return {}

    def fill_artikel():

        nonlocal v_log, h_artikel, bediener, res_history, queasy
        nonlocal buff_hart


        nonlocal h_list, buff_hart
        nonlocal h_list_list

        if case_type == 2:

            if trim(h_artikel.bezeich) != trim(h_list.bezeich) or h_artikel.zwkum != h_list.zwkum or h_artikel.endkum != h_list.endkum or h_artikel.epreis1 != h_list.epreis1 or h_artikel.artart != h_list.artart or h_artikel.mwst_code != h_list.mwst_code or h_artikel.service_code != h_list.service_code or h_artikel.artnrfront != h_list.artnrfront or h_artikel.bondruckernr[0] != h_list.bondruckernr[0] or h_artikel.activeflag != h_list.activeflag:
                v_log = True

            if v_log:

                bediener = db_session.query(Bediener).filter(
                        (func.lower(Bediener.userinit) == (user_init).lower())).first()
                res_history = Res_history()
                db_session.add(res_history)

                res_history.nr = bediener.nr
                res_history.datum = get_current_date()
                res_history.zeit = get_current_time_in_seconds()
                res_history.action = "Outlet Article Setup"
                res_history.aenderung = "Modify ArtNo " + to_string(h_artikel.artnr) + "  == > "

                if trim(h_artikel.bezeich) != trim(h_list.bezeich):
                    res_history.aenderung = res_history.aenderung + h_artikel.bezeich + " to " + h_list.bezeich + ";"

                if h_artikel.zwkum != h_list.zwkum:
                    res_history.aenderung = res_history.aenderung + "SubGroup " + to_string(h_artikel.zwkum) + " to " + to_string(h_list.zwkum) + ";"

                if h_artikel.endkum != h_list.endkum:
                    res_history.aenderung = res_history.aenderung + "MainGroup " + to_string(h_artikel.endkum) + " to " + to_string(h_list.endkum) + ";"

                if h_artikel.epreis1 != h_list.epreis1:
                    res_history.aenderung = res_history.aenderung + "UnitPrice " + to_string(h_artikel.epreis1) + " to " + to_string(h_list.epreis1) + ";"

                if h_artikel.artart != h_list.artart:
                    res_history.aenderung = res_history.aenderung + "ArtType " + to_string(h_artikel.artart) + " to " + to_string(h_list.artart) + ";"

                if h_artikel.mwst_code != h_list.mwst_code:
                    res_history.aenderung = res_history.aenderung + "VAT " + to_string(h_artikel.mwst_code) + " to " + to_string(h_list.mwst_code) + ";"

                if h_artikel.service_code != h_list.service_code:
                    res_history.aenderung = res_history.aenderung + "Service " + to_string(h_artikel.service_code) + " to " + to_string(h_list.service_code) + ";"

                if h_artikel.artnrfront != h_list.artnrfront:
                    res_history.aenderung = res_history.aenderung + "FO ArtNo " + to_string(h_artikel.artnrfront) + " to " + to_string(h_list.artnrfront) + ";"

                if h_artikel.bondruckernr[0] != h_list.bondruckernr[0]:
                    res_history.aenderung = res_history.aenderung + "KP No " + to_string(h_artikel.bondruckernr[0]) + " to " + to_string(h_list.bondruckernr[0]) + ";"

                if h_artikel.activeflag != h_list.activeflag:
                    res_history.aenderung = res_history.aenderung + "ActiveArt " + to_string(h_artikel.activeflag) + " to " + to_string(h_list.activeflag) + ";"
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

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == 200) &  (Queasy.number1 == h_list.departement) &  (Queasy.number2 == h_list.artnr)).first()

        if not queasy:
            queasy = Queasy()
            db_session.add(queasy)

            queasy.key = 200
            queasy.number1 = h_list.departement
            queasy.number2 = h_list.artnr
            queasy.char1 = barcode
            queasy.char2 = h_list.bezeich


        else:
            queasy.char1 = barcode

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