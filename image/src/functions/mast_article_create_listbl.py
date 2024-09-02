from functions.additional_functions import *
import decimal
from functions.load_artikelbl import load_artikelbl
from models import Artikel

def mast_article_create_listbl(curr_dept:int):
    hart_list_list = []
    artikel = None

    t_artikel = artikel_list = hart_list = gart_list = None

    t_artikel_list, T_artikel = create_model_like(Artikel)
    artikel_list_list, Artikel_list = create_model("Artikel_list", {"artnr":int, "departement":int, "bezeich":str, "artart":int})
    hart_list_list, Hart_list = create_model("Hart_list", {"artnr":int, "departement":int, "bezeich":str, "artart":int})
    gart_list_list, Gart_list = create_model("Gart_list", {"artnr":int, "departement":int, "bezeich":str, "artart":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal hart_list_list, artikel


        nonlocal t_artikel, artikel_list, hart_list, gart_list
        nonlocal t_artikel_list, artikel_list_list, hart_list_list, gart_list_list
        return {"hart-list": hart_list_list}

    def create_list():

        nonlocal hart_list_list, artikel


        nonlocal t_artikel, artikel_list, hart_list, gart_list
        nonlocal t_artikel_list, artikel_list_list, hart_list_list, gart_list_list


        hart_list_list.clear()
        artikel_list_list, t_artikel_list = get_output(load_artikelbl(1, curr_dept))

        artikel_list = query(artikel_list_list, filters=(lambda artikel_list :(artikel_list.artart == 0 or artikel_list.artart == 5)), first=True)
        while None != artikel_list:

            gart_list = query(gart_list_list, filters=(lambda gart_list :gart_list.artnr == artikel_list.artnr and gart_list.departement == artikel_list.departement), first=True)

            if not gart_list:
                hart_list = Hart_list()
                hart_list_list.append(hart_list)

                buffer_copy(artikel_list, hart_list)

            artikel_list = query(artikel_list_list, filters=(lambda artikel_list :(artikel_list.artart == 0 or artikel_list.artart == 5)), next=True)

    create_list()

    return generate_output()