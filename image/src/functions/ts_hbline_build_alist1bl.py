from functions.additional_functions import *
import decimal
from models import H_artikel

def ts_hbline_build_alist1bl(artno:int, dept:int):
    curr_apos = 0
    art_list_list = []
    h_artikel = None

    art_list = None

    art_list_list, Art_list = create_model("Art_list", {"pos":int, "artnr":int, "bezeich":str, "epreis":decimal, "item_bgcol":int, "item_fgcol":int}, {"item_bgcol": 2, "item_fgcol": 15})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal curr_apos, art_list_list, h_artikel


        nonlocal art_list
        nonlocal art_list_list
        return {"curr_apos": curr_apos, "art-list": art_list_list}

    def build_alist1():

        nonlocal curr_apos, art_list_list, h_artikel


        nonlocal art_list
        nonlocal art_list_list


        art_list_list.clear()
        curr_apos = 1

        h_artikel = db_session.query(H_artikel).filter(
                (H_artikel.departement == dept) &  (H_artikel.artnr == artno)).first()
        art_list = Art_list()
        art_list_list.append(art_list)

        art_list.pos = 1
        art_list.artnr = h_artikel.artnr
        art_list.bezeich = h_artikel.bezeich
        art_list.epreis = h_artikel.epreis1


    build_alist1()

    return generate_output()