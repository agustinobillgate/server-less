#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import H_artikel

def ts_hbline_build_alistbl(zero_flag:bool, dept:int, curr_zwkum:int, billdate:date):

    prepare_cache ([H_artikel])

    curr_apos = 0
    max_apos = 0
    art_list_list = []
    fgcol_array:List[int] = [15, 15, 15, 15, 15, 15, 15, 15, 0, 15, 0, 0, 15, 15, 0, 0, 15]
    h_artikel = None

    art_list = None

    art_list_list, Art_list = create_model("Art_list", {"pos":int, "artnr":int, "bezeich":string, "epreis":Decimal, "item_bgcol":int, "item_fgcol":int}, {"item_bgcol": 2, "item_fgcol": 15})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal curr_apos, max_apos, art_list_list, fgcol_array, h_artikel
        nonlocal zero_flag, dept, curr_zwkum, billdate


        nonlocal art_list
        nonlocal art_list_list

        return {"curr_apos": curr_apos, "max_apos": max_apos, "art-list": art_list_list}

    def build_alist():

        nonlocal curr_apos, max_apos, art_list_list, fgcol_array, h_artikel
        nonlocal zero_flag, dept, curr_zwkum, billdate


        nonlocal art_list
        nonlocal art_list_list

        i:int = 0
        art_list_list.clear()
        curr_apos = 1

        if not zero_flag:

            for h_artikel in db_session.query(H_artikel).filter(
                     (H_artikel.departement == dept) & (H_artikel.artart == 0) & (H_artikel.zwkum == curr_zwkum) & (H_artikel.epreis1 != 0) & (H_artikel.activeflag) & ((H_artikel.s_gueltig == None) | ((H_artikel.s_gueltig <= billdate) & (H_artikel.e_gueltig >= billdate)))).order_by(H_artikel.abbuchung.desc(), H_artikel.bezeich).all():
                i = i + 1
                art_list = Art_list()
                art_list_list.append(art_list)

                art_list.pos = i
                art_list.artnr = h_artikel.artnr
                art_list.bezeich = h_artikel.bezeich
                art_list.epreis =  to_decimal(h_artikel.epreis1)
                art_list.item_bgcol = h_artikel.abbuchung
                art_list.item_fgcol = fgcol_array[art_list.item_bgcol + 1 - 1]

                if art_list.item_bgcol == 0:
                    art_list.item_bgcol = 2

        else:

            for h_artikel in db_session.query(H_artikel).filter(
                     (H_artikel.departement == dept) & (H_artikel.artart == 0) & (H_artikel.zwkum == curr_zwkum) & (H_artikel.activeflag) & ((H_artikel.s_gueltig == None) | ((H_artikel.s_gueltig <= billdate) & (H_artikel.e_gueltig >= billdate)))).order_by(H_artikel.abbuchung.desc(), H_artikel.bezeich).all():
                i = i + 1
                art_list = Art_list()
                art_list_list.append(art_list)

                art_list.pos = i
                art_list.artnr = h_artikel.artnr
                art_list.bezeich = h_artikel.bezeich
                art_list.epreis =  to_decimal(h_artikel.epreis1)
                art_list.item_bgcol = h_artikel.abbuchung
                art_list.item_fgcol = fgcol_array[art_list.item_bgcol + 1 - 1]

                if art_list.item_bgcol == 0:
                    art_list.item_bgcol = 2

        max_apos = i

    build_alist()

    return generate_output()