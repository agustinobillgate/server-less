#using conversion tools version: 1.0.0.117

# ==========================================
# Rulita, 10-10-2025
# Tiket ID : 8CF423 | Recompile Program
# ==========================================

from functions.additional_functions import *
from decimal import Decimal
from models import Htparam, Wgrpdep, Wgrpgen, Hoteldpt, H_artikel

input_list_data, Input_list = create_model("Input_list", {"dept_num":int, "art_name":string})

def prepare_rarticle_setup_wizardbl(input_list_data:[Input_list]):

    prepare_cache ([Htparam, Wgrpdep, Wgrpgen, Hoteldpt, H_artikel])

    subgrp_list_data = []
    maingrp_list_data = []
    menu_artlist_data = []
    output_list_data = []
    dept:int = 0
    art_name:string = ""
    htparam = wgrpdep = wgrpgen = hoteldpt = h_artikel = None

    input_list = subgrp_list = maingrp_list = output_list = menu_artlist = None

    subgrp_list_data, Subgrp_list = create_model("Subgrp_list", {"departement":int, "zknr":int, "bezeich":string})
    maingrp_list_data, Maingrp_list = create_model("Maingrp_list", {"eknr":int, "bezeich":string})
    output_list_data, Output_list = create_model("Output_list", {"depart":string, "num":int, "dpttype":string, "long_digit":bool, "msg_str":string, "success_flag":bool}, {"success_flag": True})
    menu_artlist_data, Menu_artlist = create_model("Menu_artlist", {"artnr":int, "bezeich":string, "zknr":int, "epreis":Decimal, "endkum":int, "isselected":bool, "rec_id":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal subgrp_list_data, maingrp_list_data, menu_artlist_data, output_list_data, dept, art_name, htparam, wgrpdep, wgrpgen, hoteldpt, h_artikel


        nonlocal input_list, subgrp_list, maingrp_list, output_list, menu_artlist
        nonlocal subgrp_list_data, maingrp_list_data, output_list_data, menu_artlist_data

        return {"subgrp-list": subgrp_list_data, "maingrp-list": maingrp_list_data, "menu-artlist": menu_artlist_data, "output-list": output_list_data}


    output_list = Output_list()
    output_list_data.append(output_list)


    input_list = query(input_list_data, first=True)

    if not input_list:
        output_list.msg_str = "Error loading.. please contact our Customer Service"
        output_list.success_flag = False

        return generate_output()
    else:
        dept = input_list.dept_num

        if input_list.art_name != None:
            art_name = trim(input_list.art_name)

    htparam = get_cache (Htparam, {"paramnr": [(eq, 246)]})
    output_list.long_digit = htparam.flogical

    for wgrpdep in db_session.query(Wgrpdep).filter(
             (Wgrpdep.departement == dept)).order_by(Wgrpdep._recid).all():
        subgrp_list = Subgrp_list()
        subgrp_list_data.append(subgrp_list)

        subgrp_list.departement = dept
        subgrp_list.zknr = wgrpdep.zknr
        subgrp_list.bezeich = wgrpdep.bezeich

    for wgrpgen in db_session.query(Wgrpgen).order_by(Wgrpgen.eknr).all():
        maingrp_list = Maingrp_list()
        maingrp_list_data.append(maingrp_list)

        maingrp_list.eknr = wgrpgen.eknr
        maingrp_list.bezeich = wgrpgen.bezeich

    hoteldpt = get_cache (Hoteldpt, {"num": [(eq, dept)]})

    if hoteldpt:
        output_list.num = hoteldpt.num
        output_list.depart = hoteldpt.depart

        if hoteldpt.departtyp == 1:
            output_list.dpttype = "Food & Beverage"
        elif hoteldpt.departtyp == 2:
            output_list.dpttype = "Minibar"
        elif hoteldpt.departtyp == 3:
            output_list.dpttype = "Laundry"
        elif hoteldpt.departtyp == 4:
            output_list.dpttype = "Banquet"
        elif hoteldpt.departtyp == 5:
            output_list.dpttype = "Drug Store"
        elif hoteldpt.departtyp == 6:
            output_list.dpttype = "Others"
        elif hoteldpt.departtyp == 7:
            output_list.dpttype = "Spa"
        elif hoteldpt.departtyp == 8:
            output_list.dpttype = "Boutique"
        else:
            ""

    if art_name == "" or art_name == None:

        h_artikel_obj_list = {}
        for h_artikel in db_session.query(H_artikel).filter(
                 (H_artikel.departement == dept) & (H_artikel.artart == 0)).order_by(H_artikel.activeflag.desc(), H_artikel.zwkum, H_artikel.artnr).all():
            subgrp_list = query(subgrp_list_data, (lambda subgrp_list: subgrp_list.zknr == h_artikel.zwkum and subgrp_list.departement == h_artikel.departement), first=True)
            if not subgrp_list:
                continue

            if h_artikel_obj_list.get(h_artikel._recid):
                continue
            else:
                h_artikel_obj_list[h_artikel._recid] = True


            menu_artlist = Menu_artlist()
            menu_artlist_data.append(menu_artlist)

            menu_artlist.bezeich = h_artikel.bezeich
            menu_artlist.artnr = h_artikel.artnr
            menu_artlist.zknr = h_artikel.zwkum
            menu_artlist.endkum = h_artikel.endkum
            menu_artlist.epreis =  to_decimal(h_artikel.epreis1)
            menu_artlist.isselected = False
            menu_artlist.rec_id = h_artikel._recid


    else:

        h_artikel_obj_list = {}
        for h_artikel in db_session.query(H_artikel).filter(
                 (H_artikel.departement == dept) & (H_artikel.artart == 0) & (get_index(H_artikel.bezeich, art_name) > 0)).order_by(H_artikel.activeflag.desc(), H_artikel.zwkum, H_artikel.artnr).all():
            subgrp_list = query(subgrp_list_data, (lambda subgrp_list: subgrp_list.zknr == h_artikel.zwkum and subgrp_list.departement == h_artikel.departement), first=True)
            if not subgrp_list:
                continue

            if h_artikel_obj_list.get(h_artikel._recid):
                continue
            else:
                h_artikel_obj_list[h_artikel._recid] = True


            menu_artlist = Menu_artlist()
            menu_artlist_data.append(menu_artlist)

            menu_artlist.bezeich = h_artikel.bezeich
            menu_artlist.artnr = h_artikel.artnr
            menu_artlist.zknr = h_artikel.zwkum
            menu_artlist.endkum = h_artikel.endkum
            menu_artlist.epreis =  to_decimal(h_artikel.epreis1)
            menu_artlist.isselected = False
            menu_artlist.rec_id = h_artikel._recid

    return generate_output()