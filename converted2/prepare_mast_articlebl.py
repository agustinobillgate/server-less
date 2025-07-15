#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from functions.read_mast_artbl import read_mast_artbl
from functions.read_artikelbl import read_artikelbl
from functions.read_res_linebl import read_res_linebl
from functions.read_fixleistbl import read_fixleistbl
from functions.write_mast_artbl import write_mast_artbl
from functions.load_artikelbl import load_artikelbl
from models import Artikel, Res_line, Fixleist, Mast_art

def prepare_mast_articlebl(resnr:int, new_res:bool, curr_dept:int):
    gart_list_data = []
    hart_list_data = []
    artikel = res_line = fixleist = mast_art = None

    t_artikel = t_res_line = t_fixleist = t_mast_art = artikel_list = hart_list = gart_list = None

    t_artikel_data, T_artikel = create_model_like(Artikel)
    t_res_line_data, T_res_line = create_model_like(Res_line)
    t_fixleist_data, T_fixleist = create_model_like(Fixleist)
    t_mast_art_data, T_mast_art = create_model_like(Mast_art)
    artikel_list_data, Artikel_list = create_model("Artikel_list", {"artnr":int, "departement":int, "bezeich":string, "artart":int})
    hart_list_data, Hart_list = create_model("Hart_list", {"artnr":int, "departement":int, "bezeich":string, "artart":int})
    gart_list_data, Gart_list = create_model("Gart_list", {"artnr":int, "departement":int, "bezeich":string, "artart":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal gart_list_data, hart_list_data, artikel, res_line, fixleist, mast_art
        nonlocal resnr, new_res, curr_dept


        nonlocal t_artikel, t_res_line, t_fixleist, t_mast_art, artikel_list, hart_list, gart_list
        nonlocal t_artikel_data, t_res_line_data, t_fixleist_data, t_mast_art_data, artikel_list_data, hart_list_data, gart_list_data

        return {"gart-list": gart_list_data, "hart-list": hart_list_data}

    def create_list():

        nonlocal gart_list_data, hart_list_data, artikel, res_line, fixleist, mast_art
        nonlocal resnr, new_res, curr_dept


        nonlocal t_artikel, t_res_line, t_fixleist, t_mast_art, artikel_list, hart_list, gart_list
        nonlocal t_artikel_data, t_res_line_data, t_fixleist_data, t_mast_art_data, artikel_list_data, hart_list_data, gart_list_data


        hart_list_data.clear()
        artikel_list_data, t_artikel_data = get_output(load_artikelbl(1, curr_dept))

        for artikel_list in query(artikel_list_data, filters=(lambda artikel_list:(artikel_list.artart == 0 or artikel_list.artart == 5))):

            gart_list = query(gart_list_data, filters=(lambda gart_list: gart_list.artnr == artikel_list.artnr and gart_list.departement == artikel_list.departement), first=True)

            if not gart_list:
                hart_list = Hart_list()
                hart_list_data.append(hart_list)

                buffer_copy(artikel_list, hart_list)

    t_mast_art_data = get_output(read_mast_artbl(1, resnr, None, None, None, None))

    for t_mast_art in query(t_mast_art_data):
        t_artikel_data = get_output(read_artikelbl(t_mast_art.artnr, t_mast_art.departement, ""))

        t_artikel = query(t_artikel_data, first=True)
        gart_list = Gart_list()
        gart_list_data.append(gart_list)

        gart_list.artnr = t_artikel.artnr
        gart_list.bezeich = t_artikel.bezeich
        gart_list.departement = t_artikel.departement

    if new_res:
        t_res_line_data = get_output(read_res_linebl(4, resnr, None, None, None, None, None, None, None, None, None))

        for t_res_line in query(t_res_line_data):
            t_fixleist_data = get_output(read_fixleistbl(1, resnr, t_res_line.reslinnr, 1))

            for t_fixleist in query(t_fixleist_data):

                gart_list = query(gart_list_data, filters=(lambda gart_list: gart_list.artnr == t_fixleist.artnr and gart_list.departement == t_fixleist.departement), first=True)

                if not gart_list:
                    t_artikel_data = get_output(read_artikelbl(t_fixleist.artnr, t_fixleist.departement, ""))

                    t_artikel = query(t_artikel_data, first=True)
                    gart_list = Gart_list()
                    gart_list_data.append(gart_list)

                    gart_list.artnr = t_artikel.artnr
                    gart_list.bezeich = t_artikel.bezeich
                    gart_list.departement = t_artikel.departement


        get_output(write_mast_artbl(1, resnr, gart_list_data))
    create_list()

    return generate_output()