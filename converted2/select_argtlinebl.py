#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from functions.read_arrangementbl import read_arrangementbl
from functions.load_argt_linebl import load_argt_linebl
from functions.read_artikelbl import read_artikelbl
from functions.read_hoteldptbl import read_hoteldptbl
from models import Argt_line, Arrangement, Artikel, Hoteldpt

def select_argtlinebl(pvilanguage:int, argtnr:int):
    t_list_data = []
    lvcarea:string = "select-argtline"
    post_type:List[string] = create_empty_list(6,"")
    pers_type:List[string] = create_empty_list(3,"")
    argt_line = arrangement = artikel = hoteldpt = None

    t_argt_line = t_arrangement = t_artikel = t_hoteldpt = artbuff = htlbuff = t_list = None

    t_argt_line_data, T_argt_line = create_model_like(Argt_line)
    t_arrangement_data, T_arrangement = create_model_like(Arrangement)
    t_artikel_data, T_artikel = create_model_like(Artikel)
    t_hoteldpt_data, T_hoteldpt = create_model_like(Hoteldpt)
    artbuff_data, Artbuff = create_model_like(Artikel)
    htlbuff_data, Htlbuff = create_model_like(Hoteldpt)
    t_list_data, T_list = create_model("T_list", {"arrangement":string, "artnr":int, "bezeich":string, "depart":string, "betrag":Decimal, "post_type":string, "inrate":bool, "pers_type":string, "fixcost":bool, "argt_artnr":int, "departement":int, "vt_percnt":Decimal, "betriebsnr":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_list_data, lvcarea, post_type, pers_type, argt_line, arrangement, artikel, hoteldpt
        nonlocal pvilanguage, argtnr


        nonlocal t_argt_line, t_arrangement, t_artikel, t_hoteldpt, artbuff, htlbuff, t_list
        nonlocal t_argt_line_data, t_arrangement_data, t_artikel_data, t_hoteldpt_data, artbuff_data, htlbuff_data, t_list_data

        return {"t-list": t_list_data}


    post_type[0] = translateExtended ("Daily", lvcarea, "")
    post_type[1] = translateExtended ("CI Day", lvcarea, "")
    post_type[2] = translateExtended ("2nd Day", lvcarea, "")
    post_type[3] = translateExtended ("Mon 1st Day", lvcarea, "")
    post_type[4] = translateExtended ("Mon LastDay", lvcarea, "")
    post_type[5] = translateExtended ("Special", lvcarea, "")


    pers_type[0] = translateExtended ("Adult", lvcarea, "")
    pers_type[1] = translateExtended ("Child", lvcarea, "")
    pers_type[2] = translateExtended ("Ch2", lvcarea, "")


    t_arrangement_data = get_output(read_arrangementbl(1, argtnr, ""))

    t_arrangement = query(t_arrangement_data, first=True)
    t_argt_line_data = get_output(load_argt_linebl(argtnr))

    t_argt_line = query(t_argt_line_data, first=True)
    while None != t_argt_line:

        t_artikel = query(t_artikel_data, filters=(lambda t_artikel: t_artikel.artnr == t_argt_line.argt_artnr and t_artikel.departement == t_argt_line.departement), first=True)

        if not t_artikel:
            artbuff_data = get_output(read_artikelbl(t_argt_line.argt_artnr, t_argt_line.departement, ""))

            artbuff = query(artbuff_data, first=True)
            t_artikel = T_artikel()
            t_artikel_data.append(t_artikel)

            buffer_copy(artbuff, t_artikel)

        t_hoteldpt = query(t_hoteldpt_data, filters=(lambda t_hoteldpt: t_hoteldpt.num == t_argt_line.departement), first=True)

        if not t_hoteldpt:
            htlBuff_data = get_output(read_hoteldptbl(t_argt_line.departement))

            htlbuff = query(htlbuff_data, first=True)
            t_hoteldpt = T_hoteldpt()
            t_hoteldpt_data.append(t_hoteldpt)

            buffer_copy(htlBuff, t_hoteldpt)

        t_argt_line = query(t_argt_line_data, next=True)

    for t_argt_line in query(t_argt_line_data, sort_by=[("argt_artnr",False)]):
        t_arrangement = query(t_arrangement_data, (lambda t_arrangement: t_arrangement.argtnr == t_argt_line.argtnr), first=True)
        if not t_arrangement:
            continue

        t_artikel = query(t_artikel_data, (lambda t_artikel: t_artikel.artnr == t_argt_line.argt_artnr and t_artikel.departement == t_argt_line.departement), first=True)
        if not t_artikel:
            continue

        t_hoteldpt = query(t_hoteldpt_data, (lambda t_hoteldpt: t_hoteldpt.num == t_artikel.departement), first=True)
        if not t_hoteldpt:
            continue

        t_list = T_list()
        t_list_data.append(t_list)

        t_list.arrangement = t_arrangement.arrangement
        t_list.artnr = t_artikel.artnr
        t_list.bezeich = t_artikel.bezeich
        t_list.depart = t_hoteldpt.depart
        t_list.betrag =  to_decimal(t_argt_line.betrag)
        t_list.post_type = post_type[t_argt_line.fakt_modus - 1]
        t_list.inrate = logical(t_argt_line.kind1)
        t_list.pers_type = pers_type[to_int(t_argt_line.vt_percnt) + 1 - 1]
        t_list.fixcost = t_argt_line.kind2
        t_list.argt_artnr = t_argt_line.argt_artnr
        t_list.departement = t_argt_line.departement
        t_list.vt_percnt =  to_decimal(t_argt_line.vt_percnt)
        t_list.betriebsnr = t_argt_line.betriebsnr

    return generate_output()