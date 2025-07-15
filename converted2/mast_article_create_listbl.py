#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from functions.load_artikelbl import load_artikelbl
from models import Artikel

def mast_article_create_listbl(curr_dept:int):
    hart_list_data = []
    artikel = None

    t_artikel = artikel_list = hart_list = gart_list = None

    t_artikel_data, T_artikel = create_model_like(Artikel)
    artikel_list_data, Artikel_list = create_model("Artikel_list", {"artnr":int, "departement":int, "bezeich":string, "artart":int})
    hart_list_data, Hart_list = create_model("Hart_list", {"artnr":int, "departement":int, "bezeich":string, "artart":int})
    gart_list_data, Gart_list = create_model("Gart_list", {"artnr":int, "departement":int, "bezeich":string, "artart":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal hart_list_data, artikel
        nonlocal curr_dept


        nonlocal t_artikel, artikel_list, hart_list, gart_list
        nonlocal t_artikel_data, artikel_list_data, hart_list_data, gart_list_data

        return {"hart-list": hart_list_data}

    def create_list():

        nonlocal hart_list_data, artikel
        nonlocal curr_dept


        nonlocal t_artikel, artikel_list, hart_list, gart_list
        nonlocal t_artikel_data, artikel_list_data, hart_list_data, gart_list_data


        hart_list_data.clear()
        artikel_list_data, t_artikel_data = get_output(load_artikelbl(1, curr_dept))

        artikel_list = query(artikel_list_data, filters=(lambda artikel_list:(artikel_list.artart == 0 or artikel_list.artart == 5)), first=True)
        while None != artikel_list:

            gart_list = query(gart_list_data, filters=(lambda gart_list: gart_list.artnr == artikel_list.artnr and gart_list.departement == artikel_list.departement), first=True)

            if not gart_list:
                hart_list = Hart_list()
                hart_list_data.append(hart_list)

                buffer_copy(artikel_list, hart_list)

            artikel_list = query(artikel_list_data, filters=(lambda artikel_list:(artikel_list.artart == 0 or artikel_list.artart == 5)), next=True)


    create_list()

    return generate_output()