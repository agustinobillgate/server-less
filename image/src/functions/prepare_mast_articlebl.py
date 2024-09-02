from functions.additional_functions import *
import decimal
from functions.read_mast_artbl import read_mast_artbl
from functions.read_artikelbl import read_artikelbl
from functions.read_res_linebl import read_res_linebl
from functions.read_fixleistbl import read_fixleistbl
from functions.write_mast_artbl import write_mast_artbl
from functions.load_artikelbl import load_artikelbl
from models import Artikel, Res_line, Fixleist, Mast_art

def prepare_mast_articlebl(resnr:int, new_res:bool, curr_dept:int):
    gart_list_list = []
    hart_list_list = []
    artikel = res_line = fixleist = mast_art = None

    t_artikel = t_res_line = t_fixleist = t_mast_art = artikel_list = hart_list = gart_list = None

    t_artikel_list, T_artikel = create_model_like(Artikel)
    t_res_line_list, T_res_line = create_model_like(Res_line)
    t_fixleist_list, T_fixleist = create_model_like(Fixleist)
    t_mast_art_list, T_mast_art = create_model_like(Mast_art)
    artikel_list_list, Artikel_list = create_model("Artikel_list", {"artnr":int, "departement":int, "bezeich":str, "artart":int})
    hart_list_list, Hart_list = create_model("Hart_list", {"artnr":int, "departement":int, "bezeich":str, "artart":int})
    gart_list_list, Gart_list = create_model("Gart_list", {"artnr":int, "departement":int, "bezeich":str, "artart":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal gart_list_list, hart_list_list, artikel, res_line, fixleist, mast_art


        nonlocal t_artikel, t_res_line, t_fixleist, t_mast_art, artikel_list, hart_list, gart_list
        nonlocal t_artikel_list, t_res_line_list, t_fixleist_list, t_mast_art_list, artikel_list_list, hart_list_list, gart_list_list
        return {"gart-list": gart_list_list, "hart-list": hart_list_list}

    def create_list():

        nonlocal gart_list_list, hart_list_list, artikel, res_line, fixleist, mast_art


        nonlocal t_artikel, t_res_line, t_fixleist, t_mast_art, artikel_list, hart_list, gart_list
        nonlocal t_artikel_list, t_res_line_list, t_fixleist_list, t_mast_art_list, artikel_list_list, hart_list_list, gart_list_list


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


    t_mast_art_list = get_output(read_mast_artbl(1, resnr, None, None, None, None))

    t_mast_art = query(t_mast_art_list, first=True)
    while None != t_mast_art:
        t_artikel_list = get_output(read_artikelbl(t_mast_art.artnr, t_mast_art.departement, ""))

        t_artikel = query(t_artikel_list, first=True)
        gart_list = Gart_list()
        gart_list_list.append(gart_list)

        gart_list.artnr = t_artikel.artnr
        gart_list.bezeich = t_artikel.bezeich
        gart_list.departement = t_artikel.departement

        t_mast_art = query(t_mast_art_list, next=True)

    if new_res:
        t_res_line_list = get_output(read_res_linebl(4, resnr, None, None, None, None, None, None, None, None, None))

        t_res_line = query(t_res_line_list, first=True)
        while None != t_res_line:
            t_fixleist_list = get_output(read_fixleistbl(1, resnr, t_res_line.reslinnr, 1))

            t_fixleist = query(t_fixleist_list, first=True)
            while None != t_fixleist:

                gart_list = query(gart_list_list, filters=(lambda gart_list :gart_list.artnr == t_fixleist.artnr and gart_list.departement == t_fixleist.departement), first=True)

                if not gart_list:
                    t_artikel_list = get_output(read_artikelbl(t_fixleist.artnr, t_fixleist.departement, ""))

                    t_artikel = query(t_artikel_list, first=True)
                    gart_list = Gart_list()
                    gart_list_list.append(gart_list)

                    gart_list.artnr = t_artikel.artnr
                    gart_list.bezeich = t_artikel.bezeich
                    gart_list.departement = t_artikel.departement

                t_fixleist = query(t_fixleist_list, next=True)

            t_res_line = query(t_res_line_list, next=True)
        get_output(write_mast_artbl(1, resnr, gart_list))
    create_list()

    return generate_output()