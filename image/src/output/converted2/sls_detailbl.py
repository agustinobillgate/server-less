#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Guest, Akt_line, Akt_code, Akt_kont, Akthdr

def sls_detailbl(layer:int, inp_gastnr:int):

    prepare_cache ([Akt_line, Akt_code, Akthdr])

    layer1_list_list = []
    layer2_list_list = []
    layer3_list_list = []
    guest = akt_line = akt_code = akt_kont = akthdr = None

    layer1_list = layer2_list = layer3_list = None

    layer1_list_list, Layer1_list = create_model("Layer1_list", {"datum":date, "zeit":int, "kontakt":string, "bemerk":string, "fname":string, "linenr":int})
    layer2_list_list, Layer2_list = create_model("Layer2_list", {"linenr":int, "bezeich":string, "datum":date, "zeit":int, "dauer":int, "prioritaet":int, "kontakt":string, "regard":string})
    layer3_list_list, Layer3_list = create_model("Layer3_list", {"aktnr":int, "flag":int, "akthdr_bezeich":string, "akt_code_bezeich":string, "wertigkeit":int, "stichwort":string, "t_betrag":Decimal, "erl_datum":date})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal layer1_list_list, layer2_list_list, layer3_list_list, guest, akt_line, akt_code, akt_kont, akthdr
        nonlocal layer, inp_gastnr


        nonlocal layer1_list, layer2_list, layer3_list
        nonlocal layer1_list_list, layer2_list_list, layer3_list_list

        return {"layer1-list": layer1_list_list, "layer2-list": layer2_list_list, "layer3-list": layer3_list_list}

    def layer1():

        nonlocal layer1_list_list, layer2_list_list, layer3_list_list, guest, akt_line, akt_code, akt_kont, akthdr
        nonlocal layer, inp_gastnr


        nonlocal layer1_list, layer2_list, layer3_list
        nonlocal layer1_list_list, layer2_list_list, layer3_list_list

        akt_line_obj_list = {}
        for akt_line, guest in db_session.query(Akt_line, Guest).join(Guest,(Guest.gastnr == Akt_line.gastnr)).filter(
                 (Akt_line.grupnr == 1) & (Akt_line.gastnr == inp_gastnr)).order_by(Akt_line.datum, Akt_line.zeit).all():
            if akt_line_obj_list.get(akt_line._recid):
                continue
            else:
                akt_line_obj_list[akt_line._recid] = True


            layer1_list = Layer1_list()
            layer1_list_list.append(layer1_list)

            layer1_list.datum = akt_line.datum
            layer1_list.zeit = akt_line.zeit
            layer1_list.kontakt = akt_line.kontakt
            layer1_list.bemerk = akt_line.bemerk
            layer1_list.fname = akt_line.fname
            layer1_list.linenr = akt_line.linenr


    def layer2():

        nonlocal layer1_list_list, layer2_list_list, layer3_list_list, guest, akt_line, akt_code, akt_kont, akthdr
        nonlocal layer, inp_gastnr


        nonlocal layer1_list, layer2_list, layer3_list
        nonlocal layer1_list_list, layer2_list_list, layer3_list_list

        akt_line_obj_list = {}
        akt_line = Akt_line()
        akt_code = Akt_code()
        for akt_line.datum, akt_line.zeit, akt_line.kontakt, akt_line.bemerk, akt_line.fname, akt_line.linenr, akt_line.dauer, akt_line.prioritaet, akt_line.regard, akt_line._recid, akt_code.bezeich, akt_code.wertigkeit, akt_code._recid in db_session.query(Akt_line.datum, Akt_line.zeit, Akt_line.kontakt, Akt_line.bemerk, Akt_line.fname, Akt_line.linenr, Akt_line.dauer, Akt_line.prioritaet, Akt_line.regard, Akt_line._recid, Akt_code.bezeich, Akt_code.wertigkeit, Akt_code._recid).join(Akt_code,(Akt_code.aktionscode == Akt_line.aktionscode)).filter(
                 (Akt_line.flag == 0) & (Akt_line.gastnr == inp_gastnr)).order_by(Akt_line.datum, Akt_line.zeit, Akt_line.prioritaet.desc()).all():
            if akt_line_obj_list.get(akt_line._recid):
                continue
            else:
                akt_line_obj_list[akt_line._recid] = True


            layer2_list = Layer2_list()
            layer2_list_list.append(layer2_list)

            layer2_list.linenr = akt_line.linenr
            layer2_list.bezeich = akt_code.bezeich
            layer2_list.datum = akt_line.datum
            layer2_list.zeit = akt_line.zeit
            layer2_list.dauer = akt_line.dauer
            layer2_list.prioritaet = akt_line.prioritaet
            layer2_list.kontakt = akt_line.kontakt
            layer2_list.regard = akt_line.regard


    def layer3():

        nonlocal layer1_list_list, layer2_list_list, layer3_list_list, guest, akt_line, akt_code, akt_kont, akthdr
        nonlocal layer, inp_gastnr


        nonlocal layer1_list, layer2_list, layer3_list
        nonlocal layer1_list_list, layer2_list_list, layer3_list_list

        akthdr_obj_list = {}
        for akthdr, akt_code, akt_kont in db_session.query(Akthdr, Akt_code, Akt_kont).join(Akt_code,(Akt_code.aktiongrup == 2) & (Akt_code.aktionscode == Akthdr.stufe)).join(Akt_kont,(Akt_kont.gastnr == Akthdr.gastnr)).filter(
                 (Akthdr.gastnr == inp_gastnr)).order_by(Akthdr.next_datum, Akthdr.stufe.desc()).all():
            if akthdr_obj_list.get(akthdr._recid):
                continue
            else:
                akthdr_obj_list[akthdr._recid] = True


            layer3_list = Layer3_list()
            layer3_list_list.append(layer3_list)

            layer3_list.aktnr = akthdr.aktnr
            layer3_list.flag = akthdr.flag
            layer3_list.akthdr_bezeich = akthdr.bezeich
            layer3_list.akt_code_bezeich = akt_code.bezeich
            layer3_list.wertigkeit = akt_code.wertigkeit
            layer3_list.stichwort = akthdr.stichwort
            layer3_list.t_betrag =  to_decimal(akthdr.t_betrag)
            layer3_list.erl_datum = akthdr.erl_datum


    if layer == 1:
        layer1()

    elif layer == 2:
        layer2()

    elif layer == 3:
        layer3()

    return generate_output()