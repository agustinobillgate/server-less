#using conversion tools version: 1.0.0.117

# ==========================================
# Rulita, 10-10-2025
# Tiket ID : 8CF423 | Recompile Program
# issue :progress -> INTEGER(NO)
# - h_artikel.gang = to_int(0)
# - h_artikel.bondruckernr[3] = to_int(0)
# Rd, 28/11/2025, with_for_update added
# ==========================================

from functions.additional_functions import *
from decimal import Decimal
from models import H_artikel, Hoteldpt, Artikel, Queasy

input_list_data, Input_list = create_model("Input_list", {"case_type":int, "dept_num":int})
menu_artlist_data, Menu_artlist = create_model("Menu_artlist", {"artnr":int, "bezeich":string, "zknr":int, "epreis":Decimal, "endkum":int, "departement":int, "isselected":bool, "rec_id":int})

def save_rarticle_setup_wizardbl(input_list_data:[Input_list], menu_artlist_data:[Menu_artlist]):

    prepare_cache ([H_artikel, Hoteldpt, Artikel, Queasy])

    output_list_data = []
    case_type:int = 0
    dept:int = 0
    h_artikel = hoteldpt = artikel = queasy = None

    input_list = menu_artlist = output_list = hart_buff = None

    output_list_data, Output_list = create_model("Output_list", {"msg_str":string, "success_flag":bool})

    Hart_buff = create_buffer("Hart_buff",H_artikel)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal output_list_data, case_type, dept, h_artikel, hoteldpt, artikel, queasy
        nonlocal hart_buff


        nonlocal input_list, menu_artlist, output_list, hart_buff
        nonlocal output_list_data

        return {"output-list": output_list_data}

    def create_artikel():

        nonlocal output_list_data, case_type, dept, h_artikel, hoteldpt, artikel, queasy
        nonlocal hart_buff


        nonlocal input_list, menu_artlist, output_list, hart_buff
        nonlocal output_list_data

        temp_artnr:int = 0

        menu_artlist = query(menu_artlist_data, filters=(lambda menu_artlist: menu_artlist.rec_id == -1), first=True)

        if not menu_artlist:
            output_list.msg_str = "No new artikel inserted, please check your input"
            output_list.success_flag = False

            return

        for menu_artlist in query(menu_artlist_data, filters=(lambda menu_artlist: menu_artlist.rec_id == -1)):

            h_artikel = get_cache (H_artikel, {"bezeich": [(eq, trim(menu_artlist.bezeich))],"endkum": [(eq, menu_artlist.endkum)],"zwkum": [(eq, menu_artlist.zknr)],"departement": [(eq, menu_artlist.departement)]})

            if h_artikel:
                output_list.msg_str = "Artikel " + trim(menu_artlist.bezeich) + " already exists, please check your input"
                output_list.success_flag = False

                return
            temp_artnr = 0

            for h_artikel in db_session.query(H_artikel).filter(
                     (H_artikel.endkum == menu_artlist.endkum) & (H_artikel.zwkum == menu_artlist.zknr) & (H_artikel.departement == menu_artlist.departement)).order_by(H_artikel.artnr.desc()).all():
                temp_artnr = h_artikel.artnr
                break

            if temp_artnr != 0:
                temp_artnr = temp_artnr + 1

                if substring(to_string(temp_artnr) , length(to_string(temp_artnr)) - 3 - 1) == ("0000").lower() :
                    output_list.msg_str = "Artikel created in this submenu has reached the limit" + chr_unicode(10) +\
                            trim(menu_artlist.bezeich) + chr_unicode(10) +\
                            "Change to other menu categories or contact our Customer Service"
                    output_list.success_flag = False

                    return

        for menu_artlist in query(menu_artlist_data, filters=(lambda menu_artlist: menu_artlist.rec_id == -1)):

            h_artikel = get_cache (H_artikel, {"bezeich": [(eq, trim(menu_artlist.bezeich))],"endkum": [(eq, menu_artlist.endkum)],"zwkum": [(eq, menu_artlist.zknr)],"departement": [(eq, menu_artlist.departement)]})

            if h_artikel:
                output_list.msg_str = "Artikel " + trim(menu_artlist.bezeich) + " already exists, please check your input"
                output_list.success_flag = False

                return
            temp_artnr = 0

            for h_artikel in db_session.query(H_artikel).filter(
                     (H_artikel.endkum == menu_artlist.endkum) & (H_artikel.zwkum == menu_artlist.zknr) & (H_artikel.departement == menu_artlist.departement)).order_by(H_artikel.artnr.desc()).all():
                temp_artnr = h_artikel.artnr
                break

            if temp_artnr == 0:
                temp_artnr = to_int(to_string(menu_artlist.endkum, "99") + to_string(menu_artlist.zknr, "999") + to_string(1, "9999"))
            else:
                temp_artnr = temp_artnr + 1

                if substring(to_string(temp_artnr) , length(to_string(temp_artnr)) - 3 - 1) == ("0000").lower() :
                    output_list.msg_str = "Artikel created in this submenu has reached the limit" + chr_unicode(10) +\
                            trim(menu_artlist.bezeich) + chr_unicode(10) +\
                            "Change to other menu categories or contact our Customer Service"
                    output_list.success_flag = False

                    return
            h_artikel = H_artikel()
            db_session.add(h_artikel)


            hoteldpt = get_cache (Hoteldpt, {"num": [(eq, menu_artlist.departement)]})
            h_artikel.artnr = temp_artnr
            h_artikel.departement = menu_artlist.departement
            h_artikel.bezeich = trim(menu_artlist.bezeich)
            h_artikel.zwkum = menu_artlist.zknr
            h_artikel.endkum = menu_artlist.endkum

            if menu_artlist.endkum == 1:
                h_artikel.artnrfront = 10
            elif menu_artlist.endkum == 2:
                h_artikel.artnrfront = 11
            else:
                h_artikel.artnrfront = 30
            h_artikel.bezaendern = False
            h_artikel.epreis1 =  to_decimal(menu_artlist.epreis)
            h_artikel.abbuchung = 0
            h_artikel.autosaldo = False
            h_artikel.artart = 0
            h_artikel.epreis2 =  to_decimal("0")
            h_artikel.gang = to_int(0)                          # Rulita | progress -> INTEGER(NO)
            h_artikel.bondruckernr[0] = 0
            h_artikel.aenderwunsch = False
            h_artikel.activeflag = True
            h_artikel.artnrlager = 0
            h_artikel.artnrrezept = 0
            h_artikel.prozent =  to_decimal("0")
            h_artikel.lagernr = 0
            h_artikel.betriebsnr = 0
            h_artikel.bondruckernr[3] = to_int(0)               # Rulita | progress -> INTEGER(NO)

            artikel = get_cache (Artikel, {"artnr": [(eq, h_artikel.artnrfront)],"departement": [(eq, hoteldpt.num)]})

            if artikel:
                h_artikel.mwst_code = artikel.mwst_code
                h_artikel.service_code = artikel.service_code


        output_list.msg_str = "Create artikel successfully"
        output_list.success_flag = True


    def update_artikel():

        nonlocal output_list_data, case_type, dept, h_artikel, hoteldpt, artikel, queasy
        nonlocal hart_buff


        nonlocal input_list, menu_artlist, output_list, hart_buff
        nonlocal output_list_data

        temp_artnr:int = 0

        menu_artlist = query(menu_artlist_data, filters=(lambda menu_artlist: menu_artlist.rec_id > 0 and menu_artlist.isSelected), first=True)

        if not menu_artlist:
            output_list.msg_str = "No artikel selected for modification"
            output_list.success_flag = False

            return

        for menu_artlist in query(menu_artlist_data, filters=(lambda menu_artlist: menu_artlist.rec_id > 0 and menu_artlist.isSelected)):

            h_artikel = get_cache (H_artikel, {"_recid": [(ne, menu_artlist.rec_id)],"bezeich": [(eq, trim(menu_artlist.bezeich))],"endkum": [(eq, menu_artlist.endkum)],"zwkum": [(eq, menu_artlist.zknr)],"departement": [(eq, menu_artlist.departement)]})

            if h_artikel:
                output_list.msg_str = "Selected artikel " + trim(menu_artlist.bezeich) + " already exists, please check your input"
                output_list.success_flag = False

                return

            h_artikel = get_cache (H_artikel, {"_recid": [(eq, menu_artlist.rec_id)]})

            if not h_artikel:
                output_list.msg_str = "Selected artikel " + trim(menu_artlist.bezeich) + " not found, please check your input"
                output_list.success_flag = False

                return

            hoteldpt = get_cache (Hoteldpt, {"num": [(eq, menu_artlist.departement)]})

            if h_artikel.endkum != menu_artlist.endkum and h_artikel.zwkum != menu_artlist.zknr:
                temp_artnr = 0

                for hart_buff in db_session.query(Hart_buff).filter(
                         (Hart_buff.endkum == menu_artlist.endkum) & (Hart_buff.zwkum == menu_artlist.zknr) & (Hart_buff.departement == menu_artlist.departement)).order_by(Hart_buff.artnr.desc()).all():
                    temp_artnr = hart_buff.artnr
                    break

                if temp_artnr != 0:
                    temp_artnr = temp_artnr + 1

                    if substring(to_string(temp_artnr) , length(to_string(temp_artnr)) - 3 - 1) == ("0000").lower() :
                        output_list.msg_str = "Artikel created in this submenu has reached the limit" + chr_unicode(10) +\
                                trim(menu_artlist.bezeich) + chr_unicode(10) +\
                                "Change to other menu categories or contact our Customer Service"
                        output_list.success_flag = False

                        return

        for menu_artlist in query(menu_artlist_data, filters=(lambda menu_artlist: menu_artlist.rec_id > 0 and menu_artlist.isSelected)):

            h_artikel = get_cache (H_artikel, {"_recid": [(ne, menu_artlist.rec_id)],"bezeich": [(eq, trim(menu_artlist.bezeich))],"endkum": [(eq, menu_artlist.endkum)],"zwkum": [(eq, menu_artlist.zknr)],"departement": [(eq, menu_artlist.departement)]})

            if h_artikel:
                output_list.msg_str = "Selected artikel " + trim(menu_artlist.bezeich) + " already exists, please check your input"
                output_list.success_flag = False

                return

            # h_artikel = get_cache (H_artikel, {"_recid": [(eq, menu_artlist.rec_id)]})
            h_artikel = db_session.query(H_artikel).filter(
                     (H_artikel._recid == menu_artlist.rec_id)).with_for_update().first()

            if not h_artikel:
                output_list.msg_str = "Selected artikel " + trim(menu_artlist.bezeich) + " not found, please check your input"
                output_list.success_flag = False

                return

            hoteldpt = get_cache (Hoteldpt, {"num": [(eq, menu_artlist.departement)]})

            if h_artikel.endkum != menu_artlist.endkum and h_artikel.zwkum != menu_artlist.zknr:
                temp_artnr = 0

                for hart_buff in db_session.query(Hart_buff).filter(
                         (Hart_buff.endkum == menu_artlist.endkum) & (Hart_buff.zwkum == menu_artlist.zknr) & (Hart_buff.departement == menu_artlist.departement)).order_by(Hart_buff.artnr.desc()).all():
                    temp_artnr = hart_buff.artnr
                    break

                if temp_artnr == 0:
                    temp_artnr = to_int(to_string(menu_artlist.endkum, "99") + to_string(menu_artlist.zknr, "999") + to_string(1, "9999"))
                else:
                    temp_artnr = temp_artnr + 1

                    if substring(to_string(temp_artnr) , length(to_string(temp_artnr)) - 3 - 1) == ("0000").lower() :
                        output_list.msg_str = "Artikel created in this submenu has reached the limit" + chr_unicode(10) +\
                                trim(menu_artlist.bezeich) + chr_unicode(10) +\
                                "Change to other menu categories or contact our Customer Service"
                        output_list.success_flag = False

                        return
            else:
                temp_artnr = h_artikel.artnr
            pass
            h_artikel.artnr = temp_artnr
            h_artikel.bezeich = trim(menu_artlist.bezeich)
            h_artikel.zwkum = menu_artlist.zknr
            h_artikel.endkum = menu_artlist.endkum
            h_artikel.epreis1 =  to_decimal(menu_artlist.epreis)

            if menu_artlist.endkum == 1:
                h_artikel.artnrfront = 10
            elif menu_artlist.endkum == 2:
                h_artikel.artnrfront = 11
            else:
                h_artikel.artnrfront = 30

            artikel = get_cache (Artikel, {"artnr": [(eq, h_artikel.artnrfront)],"departement": [(eq, hoteldpt.num)]})

            if artikel:
                h_artikel.mwst_code = artikel.mwst_code
                h_artikel.service_code = artikel.service_code


            pass
            pass
        output_list.msg_str = "Selected artikel modified successfully"
        output_list.success_flag = True


    def delete_artikel():

        nonlocal output_list_data, case_type, dept, h_artikel, hoteldpt, artikel, queasy
        nonlocal hart_buff


        nonlocal input_list, menu_artlist, output_list, hart_buff
        nonlocal output_list_data

        menu_artlist = query(menu_artlist_data, filters=(lambda menu_artlist: menu_artlist.rec_id > 0 and menu_artlist.isSelected), first=True)

        if not menu_artlist:
            output_list.msg_str = "No artikel selected for deletion"
            output_list.success_flag = False

            return

        for menu_artlist in query(menu_artlist_data, filters=(lambda menu_artlist: menu_artlist.rec_id > 0 and menu_artlist.isSelected)):

            h_artikel = get_cache (H_artikel, {"_recid": [(eq, menu_artlist.rec_id)]})

            if not h_artikel:
                output_list.msg_str = "Selected artikel " + trim(menu_artlist.bezeich) + " not found, delete failed"
                output_list.success_flag = False

                return

        for menu_artlist in query(menu_artlist_data, filters=(lambda menu_artlist: menu_artlist.rec_id > 0 and menu_artlist.isSelected)):

            # h_artikel = get_cache (H_artikel, {"_recid": [(eq, menu_artlist.rec_id)]})
            h_artikel = db_session.query(H_artikel).filter(
                     (H_artikel._recid == menu_artlist.rec_id)).with_for_update().first()

            if not h_artikel:
                output_list.msg_str = "Selected artikel " + trim(menu_artlist.bezeich) + " not found, delete failed"
                output_list.success_flag = False

                return
            pass
            db_session.delete(h_artikel)
        output_list.msg_str = "Selected artikel deleted successfully"
        output_list.success_flag = True


    def create_section(pos_num:int):

        nonlocal output_list_data, case_type, dept, h_artikel, hoteldpt, artikel, queasy
        nonlocal hart_buff


        nonlocal input_list, menu_artlist, output_list, hart_buff
        nonlocal output_list_data

        queasy = get_cache (Queasy, {"key": [(eq, 357)],"number1": [(eq, 2)],"number2": [(eq, pos_num)],"deci1": [(eq, 2.3)],"char1": [(eq, "outlet administration")],"char2": [(eq, "menu item setup")],"logi1": [(eq, True)]})

        if not queasy:
            queasy = Queasy()
            db_session.add(queasy)

            queasy.key = 357
            queasy.number1 = 2
            queasy.number2 = pos_num
            queasy.deci1 =  to_decimal(2.3)
            queasy.char1 = "OUTLET ADMINISTRATION"
            queasy.char2 = "menu ITEM SETUP"
            queasy.logi1 = True


        output_list.msg_str = "Progress saved successfully"
        output_list.success_flag = True

    output_list = Output_list()
    output_list_data.append(output_list)


    input_list = query(input_list_data, first=True)

    if not input_list:
        output_list.msg_str = "Error loading.. please contact our Customer Service"
        output_list.success_flag = False

        return generate_output()
    else:
        case_type = input_list.case_type
        dept = input_list.dept_num

    hoteldpt = get_cache (Hoteldpt, {"num": [(eq, dept)]})

    if not hoteldpt:
        output_list.msg_str = "No department found, please contact our Customer Service"
        output_list.success_flag = False

        return generate_output()

    if case_type == 1:
        create_artikel()
    elif case_type == 2:
        update_artikel()
    elif case_type == 3:
        delete_artikel()
    elif case_type == 4:
        create_section(dept)
    else:
        output_list.msg_str = "Invalid case type, please contact our Customer Service"
        output_list.success_flag = False

        return generate_output()

    return generate_output()