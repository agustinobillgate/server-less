#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from functions.read_htparambl import read_htparambl
from functions.read_artikelbl import read_artikelbl
from models import Artikel, Htparam

def hk_availextra_getartbl():
    temp_art_data = []
    i:int = 0
    int_art:string = ""
    artikel = htparam = None

    temp_art = t_artikel = t_htparam = None

    temp_art_data, Temp_art = create_model("Temp_art", {"art_nr":int, "art_nm":string})
    t_artikel_data, T_artikel = create_model_like(Artikel)
    t_htparam_data, T_htparam = create_model_like(Htparam)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal temp_art_data, i, int_art, artikel, htparam


        nonlocal temp_art, t_artikel, t_htparam
        nonlocal temp_art_data, t_artikel_data, t_htparam_data

        return {"temp-art": temp_art_data}


    temp_art_data.clear()
    t_htparam_data = get_output(read_htparambl(3, 2999, 5))

    t_htparam = query(t_htparam_data, first=True)

    if t_htparam:
        for i in range(1,num_entries(t_htparam.fchar , ";")  + 1) :
            int_art = entry(i - 1, t_htparam.fchar, ";")

            if int_art != "":
                temp_art = Temp_art()
                temp_art_data.append(temp_art)

                temp_art.art_nr = int (int_art)

    for temp_art in query(temp_art_data):
        t_artikel_data = get_output(read_artikelbl(temp_art.art_nr, 0, ""))

        t_artikel = query(t_artikel_data, first=True)

        if t_artikel:
            temp_art.art_nm = t_artikel.bezeich

    return generate_output()