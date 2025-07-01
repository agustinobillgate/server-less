#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import H_artikel, Queasy, Bediener, Res_history

h_list_list, H_list = create_model_like(H_artikel, {"max_soldout_qty":int, "soldout_flag":bool})

def rarticle_admin_btn_exit2_webbl(h_list_list:[H_list], case_type:int, fract_flag:bool, ask_voucher:bool, bezeich2:string, barcode:string, user_init:string):

    prepare_cache ([H_artikel, Bediener, Res_history])

    v_log:bool = False
    v_log2:bool = False
    h_artikel = queasy = bediener = res_history = None

    h_list = buff_hart = None

    Buff_hart = create_buffer("Buff_hart",H_artikel)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal v_log, v_log2, h_artikel, queasy, bediener, res_history
        nonlocal case_type, fract_flag, ask_voucher, bezeich2, barcode, user_init
        nonlocal buff_hart


        nonlocal h_list, buff_hart

        return {}

    def fill_artikel():

        nonlocal v_log, v_log2, h_artikel, queasy, bediener, res_history
        nonlocal case_type, fract_flag, ask_voucher, bezeich2, barcode, user_init
        nonlocal buff_hart


        nonlocal h_list, buff_hart

        if case_type == 2:

            if trim(h_artikel.bezeich) != trim(h_list.bezeich) or h_artikel.zwkum != h_list.zwkum or h_artikel.endkum != h_list.endkum or h_artikel.epreis1 != h_list.epreis1 or h_artikel.artart != h_list.artart or h_artikel.mwst_code != h_list.mwst_code or h_artikel.service_code != h_list.service_code or h_artikel.artnrfront != h_list.artnrfront or h_artikel.bondruckernr[0] != h_list.bondruckernr[0] or h_artikel.activeflag != h_list.activeflag:
                v_log = True

            queasy = get_cache (Queasy, {"key": [(eq, 222)],"number1": [(eq, 2)],"number2": [(eq, h_list.artnr)],"number3": [(eq, h_list.departement)]})

            if queasy:

                if (to_int(queasy.deci1) != h_list.max_soldout_qty) or (queasy.logi2 != h_list.soldout_flag):
                    v_log = True
                    v_log2 = True

            if v_log:

                bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})
                res_history = Res_history()
                db_session.add(res_history)

                res_history.nr = bediener.nr
                res_history.datum = get_current_date()
                res_history.zeit = get_current_time_in_seconds()
                res_history.action = "Outlet Article Setup"
                res_history.aenderung = "Modify ArtNo " + to_string(h_artikel.artnr) + " => "

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

                if v_log2 and queasy:

                    if to_int(queasy.deci1) != h_list.max_soldout_qty:
                        res_history.aenderung = res_history.aenderung + "MaxQtySoldOut " + to_string(to_int(queasy.deci1)) + " to " + to_string(h_list.max_soldout_qty) + ";"

                    elif queasy.logi2 != h_list.soldout_flag:
                        res_history.aenderung = res_history.aenderung + "SoldOut " + to_string(queasy.logi2) + " to " + to_string(h_list.soldout_flag) + ";"
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

        queasy = get_cache (Queasy, {"key": [(eq, 200)],"number1": [(eq, h_list.departement)],"number2": [(eq, h_list.artnr)]})

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


        pass

        queasy = get_cache (Queasy, {"key": [(eq, 222)],"number1": [(eq, 2)],"number2": [(eq, h_list.artnr)],"number3": [(eq, h_list.departement)]})

        if not queasy:
            queasy = Queasy()
            db_session.add(queasy)

            queasy.key = 222
            queasy.number1 = 2
            queasy.number2 = h_list.artnr
            queasy.number3 = h_list.departement
            queasy.logi2 = h_list.soldout_flag
            queasy.deci1 =  to_decimal(h_list.max_soldout_qty)


        else:
            queasy.logi2 = h_list.soldout_flag
            queasy.deci1 =  to_decimal(h_list.max_soldout_qty)


        pass
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
            pass

    return generate_output()