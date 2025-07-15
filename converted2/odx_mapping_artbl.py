#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import H_artikel, Queasy, Wgrpdep

art_list_data, Art_list = create_model("Art_list", {"vhp_artdept":int, "vhp_artnr":int, "vhp_arttype":string, "vhp_artname":string, "rms_artname":string, "rms_arttype":string})

def odx_mapping_artbl(case_type:int, dept:int, art_list_data:[Art_list]):

    prepare_cache ([H_artikel, Queasy, Wgrpdep])

    h_artikel = queasy = wgrpdep = None

    art_list = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal h_artikel, queasy, wgrpdep
        nonlocal case_type, dept


        nonlocal art_list

        return {"art-list": art_list_data}

    if case_type == 1:

        for h_artikel in db_session.query(H_artikel).filter(
                 (H_artikel.departemen == dept) & (H_artikel.artart != 0)).order_by(H_artikel._recid).all():

            queasy = get_cache (Queasy, {"key": [(eq, 242)],"number1": [(eq, 98)],"number2": [(eq, h_artikel.departemen)],"number3": [(eq, h_artikel.artnr)]})

            if not queasy:
                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 242
                queasy.number1 = 98
                queasy.number2 = h_artikel.departemen
                queasy.number3 = h_artikel.artnr
                queasy.char1 = h_artikel.bezeich


            pass
            pass

    elif case_type == 2:

        for art_list in query(art_list_data, sort_by=[("vhp_artnr",False)]):

            queasy = get_cache (Queasy, {"key": [(eq, 242)],"number1": [(eq, 98)],"number2": [(eq, art_list.vhp_artdept)],"number3": [(eq, art_list.vhp_artnr)]})

            if queasy:
                queasy.char2 = art_list.rms_arttype
                queasy.char3 = art_list.rms_artname


            pass
            pass
    art_list_data.clear()

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 242) & (Queasy.number1 == 98) & (Queasy.number2 == dept)).order_by(Queasy.number2, Queasy.number3).all():

        h_artikel = get_cache (H_artikel, {"departement": [(eq, dept)],"artnr": [(eq, queasy.number3)]})

        wgrpdep = get_cache (Wgrpdep, {"departement": [(eq, dept)],"zknr": [(eq, h_artikel.zwkum)]})
        art_list = Art_list()
        art_list_data.append(art_list)

        art_list.vhp_artdept = queasy.number2
        art_list.vhp_artnr = queasy.number3
        art_list.vhp_arttype = wgrpdep.bezeich
        art_list.vhp_artname = queasy.char1
        art_list.rms_arttype = queasy.char2
        art_list.rms_artname = queasy.char3


    pass

    return generate_output()