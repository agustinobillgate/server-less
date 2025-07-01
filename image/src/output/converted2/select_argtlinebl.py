#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from functions.read_arrangementbl import read_arrangementbl
from functions.load_argt_linebl import load_argt_linebl
from functions.read_artikelbl import read_artikelbl
from functions.read_hoteldptbl import read_hoteldptbl
from models import Argt_line, Arrangement, Artikel, Hoteldpt

def select_argtlinebl(pvilanguage:int, argtnr:int):
    t_list_list = []
    lvcarea:string = "select-argtline"
    post_type:List[string] = create_empty_list(6,"")
    pers_type:List[string] = create_empty_list(3,"")
    argt_line = arrangement = artikel = hoteldpt = None

    t_argt_line = t_arrangement = t_artikel = t_hoteldpt = artbuff = htlbuff = t_list = None

    t_argt_line_list, T_argt_line = create_model_like(Argt_line)
    t_arrangement_list, T_arrangement = create_model_like(Arrangement)
    t_artikel_list, T_artikel = create_model_like(Artikel)
    t_hoteldpt_list, T_hoteldpt = create_model_like(Hoteldpt)
    artbuff_list, Artbuff = create_model_like(Artikel)
    htlbuff_list, Htlbuff = create_model_like(Hoteldpt)
    t_list_list, T_list = create_model("T_list", {"arrangement":string, "artnr":int, "bezeich":string, "depart":string, "betrag":Decimal, "post_type":string, "inrate":bool, "pers_type":string, "fixcost":bool, "argt_artnr":int, "departement":int, "vt_percnt":Decimal, "betriebsnr":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_list_list, lvcarea, post_type, pers_type, argt_line, arrangement, artikel, hoteldpt
        nonlocal pvilanguage, argtnr


        nonlocal t_argt_line, t_arrangement, t_artikel, t_hoteldpt, artbuff, htlbuff, t_list
        nonlocal t_argt_line_list, t_arrangement_list, t_artikel_list, t_hoteldpt_list, artbuff_list, htlbuff_list, t_list_list

        return {"t-list": t_list_list}


    post_type[0] = translateExtended ("Daily", lvcarea, "")
    post_type[1] = translateExtended ("CI Day", lvcarea, "")
    post_type[2] = translateExtended ("2nd Day", lvcarea, "")
    post_type[3] = translateExtended ("Mon 1st Day", lvcarea, "")
    post_type[4] = translateExtended ("Mon LastDay", lvcarea, "")
    post_type[5] = translateExtended ("Special", lvcarea, "")


    pers_type[0] = translateExtended ("Adult", lvcarea, "")
    pers_type[1] = translateExtended ("Child", lvcarea, "")
    pers_type[2] = translateExtended ("Ch2", lvcarea, "")


    t_arrangement_list = get_output(read_arrangementbl(1, argtnr, ""))

    t_arrangement = query(t_arrangement_list, first=True)
    t_argt_line_list = get_output(load_argt_linebl(argtnr))

    t_argt_line = query(t_argt_line_list, first=True)
    while None != t_argt_line:

        t_artikel = query(t_artikel_list, filters=(lambda t_artikel: t_artikel.artnr == t_argt_line.argt_artnr and t_artikel.departement == t_argt_line.departement), first=True)

        if not t_artikel:
            artbuff_list = get_output(read_artikelbl(t_argt_line.argt_artnr, t_argt_line.departement, ""))

            artbuff = query(artbuff_list, first=True)
            t_artikel = T_artikel()
            t_artikel_list.append(t_artikel)

            buffer_copy(artbuff, t_artikel)

        t_hoteldpt = query(t_hoteldpt_list, filters=(lambda t_hoteldpt: t_hoteldpt.num == t_argt_line.departement), first=True)

        if not t_hoteldpt:
            htlBuff_list = get_output(read_hoteldptbl(t_argt_line.departement))

            htlbuff = query(htlbuff_list, first=True)
            t_hoteldpt = T_hoteldpt()
            t_hoteldpt_list.append(t_hoteldpt)

            buffer_copy(htlBuff, t_hoteldpt)

        t_argt_line = query(t_argt_line_list, next=True)

    for t_argt_line in query(t_argt_line_list, sort_by=[("argt_artnr",False)]):
        t_arrangement = query(t_arrangement_list, (lambda t_arrangement: t_arrangement.argtnr == t_argt_line.argtnr), first=True)
        if not t_arrangement:
            continue

        t_artikel = query(t_artikel_list, (lambda t_artikel: t_artikel.artnr == t_argt_line.argt_artnr and t_artikel.departement == t_argt_line.departement), first=True)
        if not t_artikel:
            continue

        t_hoteldpt = query(t_hoteldpt_list, (lambda t_hoteldpt: t_hoteldpt.num == t_artikel.departement), first=True)
        if not t_hoteldpt:
            continue

        t_list = T_list()
        t_list_list.append(t_list)

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