#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from functions.read_artikelbl import read_artikelbl
from functions.read_hoteldptbl import read_hoteldptbl
from models import Artikel, Hoteldpt, Argt_line

t_argt_line_list, T_argt_line = create_model_like(Argt_line)

def select_argtline_webbl(t_argt_line_list:[T_argt_line]):
    t_artikel_list = []
    t_hoteldpt_list = []
    artikel = hoteldpt = argt_line = None

    t_artikel = t_hoteldpt = t_argt_line = None

    t_artikel_list, T_artikel = create_model_like(Artikel)
    t_hoteldpt_list, T_hoteldpt = create_model_like(Hoteldpt)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_artikel_list, t_hoteldpt_list, artikel, hoteldpt, argt_line


        nonlocal t_artikel, t_hoteldpt, t_argt_line
        nonlocal t_artikel_list, t_hoteldpt_list

        return {"t-artikel": t_artikel_list, "t-hoteldpt": t_hoteldpt_list}

    t_argt_line = query(t_argt_line_list, first=True)
    while None != t_argt_line:

        t_artikel = query(t_artikel_list, filters=(lambda t_artikel: t_artikel.artnr == t_argt_line.argt_artnr and t_artikel.departement == t_argt_line.departement), first=True)

        if not t_artikel:
            t_artikel_list = get_output(read_artikelbl(t_argt_line.argt_artnr, t_argt_line.departement, ""))

        t_hoteldpt = query(t_hoteldpt_list, filters=(lambda t_hoteldpt: t_hoteldpt.num == t_argt_line.departement), first=True)

        if not t_hoteldpt:
            t_hoteldpt_list = get_output(read_hoteldptbl(t_argt_line.departement))

        t_argt_line = query(t_argt_line_list, next=True)

    return generate_output()