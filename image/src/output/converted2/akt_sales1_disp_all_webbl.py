from functions.additional_functions import *
import decimal
from models import Akthdr, Akt_code, Akt_line, Guest, Akt_kont, Bediener

def akt_sales1_disp_all_webbl(aktnr:int):
    q1_list_list = []
    q2_list_list = []
    akthdr = akt_code = akt_line = guest = akt_kont = bediener = None

    q1_list = akt_code1 = akt_line1 = q2_list = None

    q1_list_list, Q1_list = create_model_like(Akthdr, {"akthdr_recid":int, "guest_name":str, "guest_anredefirma":str, "akt_kont_name":str, "akt_kont_vorname":str, "akt_kont_anrede":str, "akt_code_bezeich":str})
    q2_list_list, Q2_list = create_model_like(Akt_line, {"recid_akt_line":int, "akt_code_bezeich":str, "bediener_username":str, "company_name":str})

    Akt_code1 = create_buffer("Akt_code1",Akt_code)
    Akt_line1 = create_buffer("Akt_line1",Akt_line)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal q1_list_list, q2_list_list, akthdr, akt_code, akt_line, guest, akt_kont, bediener
        nonlocal aktnr
        nonlocal akt_code1, akt_line1


        nonlocal q1_list, akt_code1, akt_line1, q2_list
        nonlocal q1_list_list, q2_list_list
        return {"q1-list": q1_list_list, "q2-list": q2_list_list}


    akthdr_obj_list = []
    for akthdr, guest, akt_code, akt_kont in db_session.query(Akthdr, Guest, Akt_code, Akt_kont).join(Guest,(Guest.gastnr == Akthdr.gastnr)).join(Akt_code,(Akt_code.aktiongrup == 2) & (Akt_code.aktionscode == Akthdr.stufe)).join(Akt_kont,(Akt_kont.gastnr == Akthdr.gastnr)).filter(
             (Akthdr.aktnr == aktnr) & (Akthdr.flag != 0)).order_by(Guest.name, Akthdr.next_datum.desc()).all():
        if akthdr._recid in akthdr_obj_list:
            continue
        else:
            akthdr_obj_list.append(akthdr._recid)


        q1_list = Q1_list()
        q1_list_list.append(q1_list)

        buffer_copy(akthdr, q1_list)
        q1_list.akthdr_recid = akthdr._recid
        q1_list.guest_name = guest.name
        q1_list.guest_anredefirma = guest.anredefirma
        q1_list.akt_kont_name = akt_kont.name
        q1_list.akt_kont_vorname = akt_kont.vorname
        q1_list.akt_kont_anrede = akt_kont.anrede
        q1_list.akt_code_bezeich = akt_code.bezeich

    akt_line_obj_list = []
    for akt_line, akt_code1, bediener, akthdr, guest in db_session.query(Akt_line, Akt_code1, Bediener, Akthdr, Guest).join(Akt_code1,(Akt_code1.aktionscode == Akt_line.aktionscode)).join(Bediener,(Bediener.userinit == Akt_line.userinit)).join(Akthdr,(Akthdr.aktnr == Akt_line.aktnr) & (Akthdr.flag != 0)).join(Guest,(Guest.gastnr == Akthdr.gastnr)).filter(
             (Akt_line.aktnr == aktnr) & (Akt_line.flag != 2)).order_by(Akt_line.datum, Akt_line.prioritaet.desc()).all():
        if akt_line._recid in akt_line_obj_list:
            continue
        else:
            akt_line_obj_list.append(akt_line._recid)


        q2_list = Q2_list()
        q2_list_list.append(q2_list)

        buffer_copy(akt_line, q2_list)
        q2_list.recid_akt_line = akt_line._recid
        q2_list.akt_code_bezeich = akt_code1.bezeich
        q2_list.bediener_username = bediener.username


        q2_list.company_name = guest.name + ", " + guest.anredefirma

    return generate_output()