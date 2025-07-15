#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Akt_code, Guest, Bediener, Akt_line, Akt_kont

def aktline_list_webbl(inp_gastnr:int, next_date:date, all_flag:bool, prior:int, act_combo:string, acttype:int, user_init:string, to_date:date):

    prepare_cache ([Akt_code, Guest, Bediener, Akt_line, Akt_kont])

    aktline_list_data = []
    prioritaet:List[string] = create_empty_list(3,"")
    akt_code = guest = bediener = akt_line = akt_kont = None

    aktline_list = None

    aktline_list_data, Aktline_list = create_model("Aktline_list", {"bezeich":string, "datum":date, "zeit":int, "dauer":int, "prioritaet":int, "kontakt":string, "name":string, "address":string, "regard":string, "userinit":string, "linenr":int, "telefon":string, "fax":string, "bemerk":string, "email":string, "username":string, "ftime":string, "ttime":string, "priority":string, "gastnr":int, "guest_type":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal aktline_list_data, prioritaet, akt_code, guest, bediener, akt_line, akt_kont
        nonlocal inp_gastnr, next_date, all_flag, prior, act_combo, acttype, user_init, to_date


        nonlocal aktline_list
        nonlocal aktline_list_data

        return {"aktline-list": aktline_list_data}

    def disp_all():

        nonlocal aktline_list_data, prioritaet, akt_code, guest, bediener, akt_line, akt_kont
        nonlocal inp_gastnr, next_date, all_flag, prior, act_combo, acttype, user_init, to_date


        nonlocal aktline_list
        nonlocal aktline_list_data

        if all_flag:

            if prior == 0:

                if act_combo.lower()  == ("ALL").lower() :

                    akt_line_obj_list = {}
                    akt_line = Akt_line()
                    akt_code = Akt_code()
                    guest = Guest()
                    bediener = Bediener()
                    for akt_line.datum, akt_line.zeit, akt_line.dauer, akt_line.prioritaet, akt_line.kontakt, akt_line.regard, akt_line.userinit, akt_line.linenr, akt_line.bemerk, akt_line.gastnr, akt_line.kontakt_nr, akt_line._recid, akt_code.bezeich, akt_code._recid, guest.name, guest.anredefirma, guest.adresse1, guest.adresse2, guest.adresse3, guest.telefon, guest.fax, guest.karteityp, guest.gastnr, guest._recid, bediener.username, bediener._recid in db_session.query(Akt_line.datum, Akt_line.zeit, Akt_line.dauer, Akt_line.prioritaet, Akt_line.kontakt, Akt_line.regard, Akt_line.userinit, Akt_line.linenr, Akt_line.bemerk, Akt_line.gastnr, Akt_line.kontakt_nr, Akt_line._recid, Akt_code.bezeich, Akt_code._recid, Guest.name, Guest.anredefirma, Guest.adresse1, Guest.adresse2, Guest.adresse3, Guest.telefon, Guest.fax, Guest.karteityp, Guest.gastnr, Guest._recid, Bediener.username, Bediener._recid).join(Akt_code,(Akt_code.aktionscode == Akt_line.aktionscode)).join(Guest,(Guest.gastnr == Akt_line.gastnr)).join(Bediener,(Bediener.userinit == Akt_line.userinit)).filter(
                             (Akt_line.flag == acttype)).order_by(Akt_line.datum, Akt_line.zeit, Akt_line.prioritaet.desc()).all():
                        if akt_line_obj_list.get(akt_line._recid):
                            continue
                        else:
                            akt_line_obj_list[akt_line._recid] = True


                        aktline_list = Aktline_list()
                        aktline_list_data.append(aktline_list)

                        aktline_list.bezeich = akt_code.bezeich
                        aktline_list.datum = akt_line.datum
                        aktline_list.zeit = akt_line.zeit
                        aktline_list.dauer = akt_line.dauer
                        aktline_list.ftime = to_string(akt_line.zeit, "HH:MM")
                        aktline_list.ttime = to_string(akt_line.dauer, "HH:MM")
                        aktline_list.prioritaet = akt_line.prioritaet
                        aktline_list.kontakt = akt_line.kontakt
                        aktline_list.name = guest.name + ", " + guest.anredefirma
                        aktline_list.regard = akt_line.regard
                        aktline_list.userinit = akt_line.userinit
                        aktline_list.linenr = akt_line.linenr
                        aktline_list.address = guest.adresse1 + " " + guest.adresse2 + " " + guest.adresse3
                        aktline_list.telefon = guest.telefon
                        aktline_list.fax = guest.fax
                        aktline_list.bemerk = akt_line.bemerk
                        aktline_list.username = bediener.username
                        aktline_list.gastnr = akt_line.gastnr
                        aktline_list.guest_type = guest.karteityp

                        akt_kont = get_cache (Akt_kont, {"gastnr": [(eq, guest.gastnr)],"kontakt_nr": [(eq, akt_line.kontakt_nr)]})

                        if akt_kont:
                            aktline_list.email = akt_kont.email
                        aktline_list.priority = prioritaet[aktline_list.prioritaet - 1]

                else:

                    akt_line_obj_list = {}
                    akt_line = Akt_line()
                    akt_code = Akt_code()
                    guest = Guest()
                    bediener = Bediener()
                    for akt_line.datum, akt_line.zeit, akt_line.dauer, akt_line.prioritaet, akt_line.kontakt, akt_line.regard, akt_line.userinit, akt_line.linenr, akt_line.bemerk, akt_line.gastnr, akt_line.kontakt_nr, akt_line._recid, akt_code.bezeich, akt_code._recid, guest.name, guest.anredefirma, guest.adresse1, guest.adresse2, guest.adresse3, guest.telefon, guest.fax, guest.karteityp, guest.gastnr, guest._recid, bediener.username, bediener._recid in db_session.query(Akt_line.datum, Akt_line.zeit, Akt_line.dauer, Akt_line.prioritaet, Akt_line.kontakt, Akt_line.regard, Akt_line.userinit, Akt_line.linenr, Akt_line.bemerk, Akt_line.gastnr, Akt_line.kontakt_nr, Akt_line._recid, Akt_code.bezeich, Akt_code._recid, Guest.name, Guest.anredefirma, Guest.adresse1, Guest.adresse2, Guest.adresse3, Guest.telefon, Guest.fax, Guest.karteityp, Guest.gastnr, Guest._recid, Bediener.username, Bediener._recid).join(Akt_code,(Akt_code.aktionscode == Akt_line.aktionscode) & (Akt_code.bezeich == (act_combo).lower())).join(Guest,(Guest.gastnr == Akt_line.gastnr)).join(Bediener,(Bediener.userinit == Akt_line.userinit)).filter(
                             (Akt_line.flag == acttype)).order_by(Akt_line.datum, Akt_line.zeit, Akt_line.prioritaet.desc()).all():
                        if akt_line_obj_list.get(akt_line._recid):
                            continue
                        else:
                            akt_line_obj_list[akt_line._recid] = True


                        aktline_list = Aktline_list()
                        aktline_list_data.append(aktline_list)

                        aktline_list.bezeich = akt_code.bezeich
                        aktline_list.datum = akt_line.datum
                        aktline_list.zeit = akt_line.zeit
                        aktline_list.dauer = akt_line.dauer
                        aktline_list.ftime = to_string(akt_line.zeit, "HH:MM")
                        aktline_list.ttime = to_string(akt_line.dauer, "HH:MM")
                        aktline_list.prioritaet = akt_line.prioritaet
                        aktline_list.kontakt = akt_line.kontakt
                        aktline_list.name = guest.name + ", " + guest.anredefirma
                        aktline_list.regard = akt_line.regard
                        aktline_list.userinit = akt_line.userinit
                        aktline_list.linenr = akt_line.linenr
                        aktline_list.address = guest.adresse1 + " " + guest.adresse2 + " " + guest.adresse3
                        aktline_list.telefon = guest.telefon
                        aktline_list.fax = guest.fax
                        aktline_list.bemerk = akt_line.bemerk
                        aktline_list.username = bediener.username
                        aktline_list.gastnr = akt_line.gastnr
                        aktline_list.guest_type = guest.karteityp

                        akt_kont = get_cache (Akt_kont, {"gastnr": [(eq, guest.gastnr)],"kontakt_nr": [(eq, akt_line.kontakt_nr)]})

                        if akt_kont:
                            aktline_list.email = akt_kont.email
                        aktline_list.priority = prioritaet[aktline_list.prioritaet - 1]

            else:

                if act_combo.lower()  == ("ALL").lower() :

                    akt_line_obj_list = {}
                    akt_line = Akt_line()
                    akt_code = Akt_code()
                    guest = Guest()
                    bediener = Bediener()
                    for akt_line.datum, akt_line.zeit, akt_line.dauer, akt_line.prioritaet, akt_line.kontakt, akt_line.regard, akt_line.userinit, akt_line.linenr, akt_line.bemerk, akt_line.gastnr, akt_line.kontakt_nr, akt_line._recid, akt_code.bezeich, akt_code._recid, guest.name, guest.anredefirma, guest.adresse1, guest.adresse2, guest.adresse3, guest.telefon, guest.fax, guest.karteityp, guest.gastnr, guest._recid, bediener.username, bediener._recid in db_session.query(Akt_line.datum, Akt_line.zeit, Akt_line.dauer, Akt_line.prioritaet, Akt_line.kontakt, Akt_line.regard, Akt_line.userinit, Akt_line.linenr, Akt_line.bemerk, Akt_line.gastnr, Akt_line.kontakt_nr, Akt_line._recid, Akt_code.bezeich, Akt_code._recid, Guest.name, Guest.anredefirma, Guest.adresse1, Guest.adresse2, Guest.adresse3, Guest.telefon, Guest.fax, Guest.karteityp, Guest.gastnr, Guest._recid, Bediener.username, Bediener._recid).join(Akt_code,(Akt_code.aktionscode == Akt_line.aktionscode)).join(Guest,(Guest.gastnr == Akt_line.gastnr)).join(Bediener,(Bediener.userinit == Akt_line.userinit)).filter(
                             (Akt_line.flag == acttype) & (Akt_line.prioritaet == prior)).order_by(Akt_line.datum, Akt_line.zeit, Akt_line.prioritaet.desc()).all():
                        if akt_line_obj_list.get(akt_line._recid):
                            continue
                        else:
                            akt_line_obj_list[akt_line._recid] = True


                        aktline_list = Aktline_list()
                        aktline_list_data.append(aktline_list)

                        aktline_list.bezeich = akt_code.bezeich
                        aktline_list.datum = akt_line.datum
                        aktline_list.zeit = akt_line.zeit
                        aktline_list.dauer = akt_line.dauer
                        aktline_list.ftime = to_string(akt_line.zeit, "HH:MM")
                        aktline_list.ttime = to_string(akt_line.dauer, "HH:MM")
                        aktline_list.prioritaet = akt_line.prioritaet
                        aktline_list.kontakt = akt_line.kontakt
                        aktline_list.name = guest.name + ", " + guest.anredefirma
                        aktline_list.regard = akt_line.regard
                        aktline_list.userinit = akt_line.userinit
                        aktline_list.linenr = akt_line.linenr
                        aktline_list.address = guest.adresse1 + " " + guest.adresse2 + " " + guest.adresse3
                        aktline_list.telefon = guest.telefon
                        aktline_list.fax = guest.fax
                        aktline_list.bemerk = akt_line.bemerk
                        aktline_list.username = bediener.username
                        aktline_list.gastnr = akt_line.gastnr
                        aktline_list.guest_type = guest.karteityp

                        akt_kont = get_cache (Akt_kont, {"gastnr": [(eq, guest.gastnr)],"kontakt_nr": [(eq, akt_line.kontakt_nr)]})

                        if akt_kont:
                            aktline_list.email = akt_kont.email
                        aktline_list.priority = prioritaet[aktline_list.prioritaet - 1]

                else:

                    akt_line_obj_list = {}
                    akt_line = Akt_line()
                    akt_code = Akt_code()
                    guest = Guest()
                    bediener = Bediener()
                    for akt_line.datum, akt_line.zeit, akt_line.dauer, akt_line.prioritaet, akt_line.kontakt, akt_line.regard, akt_line.userinit, akt_line.linenr, akt_line.bemerk, akt_line.gastnr, akt_line.kontakt_nr, akt_line._recid, akt_code.bezeich, akt_code._recid, guest.name, guest.anredefirma, guest.adresse1, guest.adresse2, guest.adresse3, guest.telefon, guest.fax, guest.karteityp, guest.gastnr, guest._recid, bediener.username, bediener._recid in db_session.query(Akt_line.datum, Akt_line.zeit, Akt_line.dauer, Akt_line.prioritaet, Akt_line.kontakt, Akt_line.regard, Akt_line.userinit, Akt_line.linenr, Akt_line.bemerk, Akt_line.gastnr, Akt_line.kontakt_nr, Akt_line._recid, Akt_code.bezeich, Akt_code._recid, Guest.name, Guest.anredefirma, Guest.adresse1, Guest.adresse2, Guest.adresse3, Guest.telefon, Guest.fax, Guest.karteityp, Guest.gastnr, Guest._recid, Bediener.username, Bediener._recid).join(Akt_code,(Akt_code.aktionscode == Akt_line.aktionscode) & (Akt_code.bezeich == (act_combo).lower())).join(Guest,(Guest.gastnr == Akt_line.gastnr)).join(Bediener,(Bediener.userinit == Akt_line.userinit)).filter(
                             (Akt_line.flag == acttype) & (Akt_line.prioritaet == prior)).order_by(Akt_line.datum, Akt_line.zeit, Akt_line.prioritaet.desc()).all():
                        if akt_line_obj_list.get(akt_line._recid):
                            continue
                        else:
                            akt_line_obj_list[akt_line._recid] = True


                        aktline_list = Aktline_list()
                        aktline_list_data.append(aktline_list)

                        aktline_list.bezeich = akt_code.bezeich
                        aktline_list.datum = akt_line.datum
                        aktline_list.zeit = akt_line.zeit
                        aktline_list.dauer = akt_line.dauer
                        aktline_list.ftime = to_string(akt_line.zeit, "HH:MM")
                        aktline_list.ttime = to_string(akt_line.dauer, "HH:MM")
                        aktline_list.prioritaet = akt_line.prioritaet
                        aktline_list.kontakt = akt_line.kontakt
                        aktline_list.name = guest.name + ", " + guest.anredefirma
                        aktline_list.regard = akt_line.regard
                        aktline_list.userinit = akt_line.userinit
                        aktline_list.linenr = akt_line.linenr
                        aktline_list.address = guest.adresse1 + " " + guest.adresse2 + " " + guest.adresse3
                        aktline_list.telefon = guest.telefon
                        aktline_list.fax = guest.fax
                        aktline_list.bemerk = akt_line.bemerk
                        aktline_list.username = bediener.username
                        aktline_list.gastnr = akt_line.gastnr
                        aktline_list.guest_type = guest.karteityp

                        akt_kont = get_cache (Akt_kont, {"gastnr": [(eq, guest.gastnr)],"kontakt_nr": [(eq, akt_line.kontakt_nr)]})

                        if akt_kont:
                            aktline_list.email = akt_kont.email
                        aktline_list.priority = prioritaet[aktline_list.prioritaet - 1]

        else:

            if prior == 0:

                if act_combo.lower()  == ("ALL").lower() :

                    akt_line_obj_list = {}
                    akt_line = Akt_line()
                    akt_code = Akt_code()
                    guest = Guest()
                    bediener = Bediener()
                    for akt_line.datum, akt_line.zeit, akt_line.dauer, akt_line.prioritaet, akt_line.kontakt, akt_line.regard, akt_line.userinit, akt_line.linenr, akt_line.bemerk, akt_line.gastnr, akt_line.kontakt_nr, akt_line._recid, akt_code.bezeich, akt_code._recid, guest.name, guest.anredefirma, guest.adresse1, guest.adresse2, guest.adresse3, guest.telefon, guest.fax, guest.karteityp, guest.gastnr, guest._recid, bediener.username, bediener._recid in db_session.query(Akt_line.datum, Akt_line.zeit, Akt_line.dauer, Akt_line.prioritaet, Akt_line.kontakt, Akt_line.regard, Akt_line.userinit, Akt_line.linenr, Akt_line.bemerk, Akt_line.gastnr, Akt_line.kontakt_nr, Akt_line._recid, Akt_code.bezeich, Akt_code._recid, Guest.name, Guest.anredefirma, Guest.adresse1, Guest.adresse2, Guest.adresse3, Guest.telefon, Guest.fax, Guest.karteityp, Guest.gastnr, Guest._recid, Bediener.username, Bediener._recid).join(Akt_code,(Akt_code.aktionscode == Akt_line.aktionscode)).join(Guest,(Guest.gastnr == Akt_line.gastnr)).join(Bediener,(Bediener.userinit == Akt_line.userinit)).filter(
                             (Akt_line.flag == acttype) & (Akt_line.userinit == (user_init).lower())).order_by(Akt_line.datum, Akt_line.zeit, Akt_line.prioritaet.desc()).all():
                        if akt_line_obj_list.get(akt_line._recid):
                            continue
                        else:
                            akt_line_obj_list[akt_line._recid] = True


                        aktline_list = Aktline_list()
                        aktline_list_data.append(aktline_list)

                        aktline_list.bezeich = akt_code.bezeich
                        aktline_list.datum = akt_line.datum
                        aktline_list.zeit = akt_line.zeit
                        aktline_list.dauer = akt_line.dauer
                        aktline_list.ftime = to_string(akt_line.zeit, "HH:MM")
                        aktline_list.ttime = to_string(akt_line.dauer, "HH:MM")
                        aktline_list.prioritaet = akt_line.prioritaet
                        aktline_list.kontakt = akt_line.kontakt
                        aktline_list.name = guest.name + ", " + guest.anredefirma
                        aktline_list.regard = akt_line.regard
                        aktline_list.userinit = akt_line.userinit
                        aktline_list.linenr = akt_line.linenr
                        aktline_list.address = guest.adresse1 + " " + guest.adresse2 + " " + guest.adresse3
                        aktline_list.telefon = guest.telefon
                        aktline_list.fax = guest.fax
                        aktline_list.bemerk = akt_line.bemerk
                        aktline_list.username = bediener.username
                        aktline_list.gastnr = akt_line.gastnr
                        aktline_list.guest_type = guest.karteityp

                        akt_kont = get_cache (Akt_kont, {"gastnr": [(eq, guest.gastnr)],"kontakt_nr": [(eq, akt_line.kontakt_nr)]})

                        if akt_kont:
                            aktline_list.email = akt_kont.email
                        aktline_list.priority = prioritaet[aktline_list.prioritaet - 1]

                else:

                    akt_line_obj_list = {}
                    akt_line = Akt_line()
                    akt_code = Akt_code()
                    guest = Guest()
                    bediener = Bediener()
                    for akt_line.datum, akt_line.zeit, akt_line.dauer, akt_line.prioritaet, akt_line.kontakt, akt_line.regard, akt_line.userinit, akt_line.linenr, akt_line.bemerk, akt_line.gastnr, akt_line.kontakt_nr, akt_line._recid, akt_code.bezeich, akt_code._recid, guest.name, guest.anredefirma, guest.adresse1, guest.adresse2, guest.adresse3, guest.telefon, guest.fax, guest.karteityp, guest.gastnr, guest._recid, bediener.username, bediener._recid in db_session.query(Akt_line.datum, Akt_line.zeit, Akt_line.dauer, Akt_line.prioritaet, Akt_line.kontakt, Akt_line.regard, Akt_line.userinit, Akt_line.linenr, Akt_line.bemerk, Akt_line.gastnr, Akt_line.kontakt_nr, Akt_line._recid, Akt_code.bezeich, Akt_code._recid, Guest.name, Guest.anredefirma, Guest.adresse1, Guest.adresse2, Guest.adresse3, Guest.telefon, Guest.fax, Guest.karteityp, Guest.gastnr, Guest._recid, Bediener.username, Bediener._recid).join(Akt_code,(Akt_code.aktionscode == Akt_line.aktionscode) & (Akt_code.bezeich == (act_combo).lower())).join(Guest,(Guest.gastnr == Akt_line.gastnr)).join(Bediener,(Bediener.userinit == Akt_line.userinit)).filter(
                             (Akt_line.flag == acttype) & (Akt_line.userinit == (user_init).lower())).order_by(Akt_line.datum, Akt_line.zeit, Akt_line.prioritaet.desc()).all():
                        if akt_line_obj_list.get(akt_line._recid):
                            continue
                        else:
                            akt_line_obj_list[akt_line._recid] = True


                        aktline_list = Aktline_list()
                        aktline_list_data.append(aktline_list)

                        aktline_list.bezeich = akt_code.bezeich
                        aktline_list.datum = akt_line.datum
                        aktline_list.zeit = akt_line.zeit
                        aktline_list.dauer = akt_line.dauer
                        aktline_list.ftime = to_string(akt_line.zeit, "HH:MM")
                        aktline_list.ttime = to_string(akt_line.dauer, "HH:MM")
                        aktline_list.prioritaet = akt_line.prioritaet
                        aktline_list.kontakt = akt_line.kontakt
                        aktline_list.name = guest.name + ", " + guest.anredefirma
                        aktline_list.regard = akt_line.regard
                        aktline_list.userinit = akt_line.userinit
                        aktline_list.linenr = akt_line.linenr
                        aktline_list.address = guest.adresse1 + " " + guest.adresse2 + " " + guest.adresse3
                        aktline_list.telefon = guest.telefon
                        aktline_list.fax = guest.fax
                        aktline_list.bemerk = akt_line.bemerk
                        aktline_list.username = bediener.username
                        aktline_list.gastnr = akt_line.gastnr
                        aktline_list.guest_type = guest.karteityp

                        akt_kont = get_cache (Akt_kont, {"gastnr": [(eq, guest.gastnr)],"kontakt_nr": [(eq, akt_line.kontakt_nr)]})

                        if akt_kont:
                            aktline_list.email = akt_kont.email
                        aktline_list.priority = prioritaet[aktline_list.prioritaet - 1]

            else:

                if act_combo.lower()  == ("ALL").lower() :

                    akt_line_obj_list = {}
                    akt_line = Akt_line()
                    akt_code = Akt_code()
                    guest = Guest()
                    bediener = Bediener()
                    for akt_line.datum, akt_line.zeit, akt_line.dauer, akt_line.prioritaet, akt_line.kontakt, akt_line.regard, akt_line.userinit, akt_line.linenr, akt_line.bemerk, akt_line.gastnr, akt_line.kontakt_nr, akt_line._recid, akt_code.bezeich, akt_code._recid, guest.name, guest.anredefirma, guest.adresse1, guest.adresse2, guest.adresse3, guest.telefon, guest.fax, guest.karteityp, guest.gastnr, guest._recid, bediener.username, bediener._recid in db_session.query(Akt_line.datum, Akt_line.zeit, Akt_line.dauer, Akt_line.prioritaet, Akt_line.kontakt, Akt_line.regard, Akt_line.userinit, Akt_line.linenr, Akt_line.bemerk, Akt_line.gastnr, Akt_line.kontakt_nr, Akt_line._recid, Akt_code.bezeich, Akt_code._recid, Guest.name, Guest.anredefirma, Guest.adresse1, Guest.adresse2, Guest.adresse3, Guest.telefon, Guest.fax, Guest.karteityp, Guest.gastnr, Guest._recid, Bediener.username, Bediener._recid).join(Akt_code,(Akt_code.aktionscode == Akt_line.aktionscode)).join(Guest,(Guest.gastnr == Akt_line.gastnr)).join(Bediener,(Bediener.userinit == Akt_line.userinit)).filter(
                             (Akt_line.flag == acttype) & (Akt_line.userinit == (user_init).lower()) & (Akt_line.prioritaet == prior)).order_by(Akt_line.datum, Akt_line.zeit, Akt_line.prioritaet.desc()).all():
                        if akt_line_obj_list.get(akt_line._recid):
                            continue
                        else:
                            akt_line_obj_list[akt_line._recid] = True


                        aktline_list = Aktline_list()
                        aktline_list_data.append(aktline_list)

                        aktline_list.bezeich = akt_code.bezeich
                        aktline_list.datum = akt_line.datum
                        aktline_list.zeit = akt_line.zeit
                        aktline_list.dauer = akt_line.dauer
                        aktline_list.ftime = to_string(akt_line.zeit, "HH:MM")
                        aktline_list.ttime = to_string(akt_line.dauer, "HH:MM")
                        aktline_list.prioritaet = akt_line.prioritaet
                        aktline_list.kontakt = akt_line.kontakt
                        aktline_list.name = guest.name + ", " + guest.anredefirma
                        aktline_list.regard = akt_line.regard
                        aktline_list.userinit = akt_line.userinit
                        aktline_list.linenr = akt_line.linenr
                        aktline_list.address = guest.adresse1 + " " + guest.adresse2 + " " + guest.adresse3
                        aktline_list.telefon = guest.telefon
                        aktline_list.fax = guest.fax
                        aktline_list.bemerk = akt_line.bemerk
                        aktline_list.username = bediener.username
                        aktline_list.gastnr = akt_line.gastnr
                        aktline_list.guest_type = guest.karteityp

                        akt_kont = get_cache (Akt_kont, {"gastnr": [(eq, guest.gastnr)],"kontakt_nr": [(eq, akt_line.kontakt_nr)]})

                        if akt_kont:
                            aktline_list.email = akt_kont.email
                        aktline_list.priority = prioritaet[aktline_list.prioritaet - 1]

                else:

                    akt_line_obj_list = {}
                    akt_line = Akt_line()
                    akt_code = Akt_code()
                    guest = Guest()
                    bediener = Bediener()
                    for akt_line.datum, akt_line.zeit, akt_line.dauer, akt_line.prioritaet, akt_line.kontakt, akt_line.regard, akt_line.userinit, akt_line.linenr, akt_line.bemerk, akt_line.gastnr, akt_line.kontakt_nr, akt_line._recid, akt_code.bezeich, akt_code._recid, guest.name, guest.anredefirma, guest.adresse1, guest.adresse2, guest.adresse3, guest.telefon, guest.fax, guest.karteityp, guest.gastnr, guest._recid, bediener.username, bediener._recid in db_session.query(Akt_line.datum, Akt_line.zeit, Akt_line.dauer, Akt_line.prioritaet, Akt_line.kontakt, Akt_line.regard, Akt_line.userinit, Akt_line.linenr, Akt_line.bemerk, Akt_line.gastnr, Akt_line.kontakt_nr, Akt_line._recid, Akt_code.bezeich, Akt_code._recid, Guest.name, Guest.anredefirma, Guest.adresse1, Guest.adresse2, Guest.adresse3, Guest.telefon, Guest.fax, Guest.karteityp, Guest.gastnr, Guest._recid, Bediener.username, Bediener._recid).join(Akt_code,(Akt_code.aktionscode == Akt_line.aktionscode) & (Akt_code.bezeich == (act_combo).lower())).join(Guest,(Guest.gastnr == Akt_line.gastnr)).join(Bediener,(Bediener.userinit == Akt_line.userinit)).filter(
                             (Akt_line.flag == acttype) & (Akt_line.userinit == (user_init).lower()) & (Akt_line.prioritaet == prior)).order_by(Akt_line.datum, Akt_line.zeit, Akt_line.prioritaet.desc()).all():
                        if akt_line_obj_list.get(akt_line._recid):
                            continue
                        else:
                            akt_line_obj_list[akt_line._recid] = True


                        aktline_list = Aktline_list()
                        aktline_list_data.append(aktline_list)

                        aktline_list.bezeich = akt_code.bezeich
                        aktline_list.datum = akt_line.datum
                        aktline_list.zeit = akt_line.zeit
                        aktline_list.dauer = akt_line.dauer
                        aktline_list.ftime = to_string(akt_line.zeit, "HH:MM")
                        aktline_list.ttime = to_string(akt_line.dauer, "HH:MM")
                        aktline_list.prioritaet = akt_line.prioritaet
                        aktline_list.kontakt = akt_line.kontakt
                        aktline_list.name = guest.name + ", " + guest.anredefirma
                        aktline_list.regard = akt_line.regard
                        aktline_list.userinit = akt_line.userinit
                        aktline_list.linenr = akt_line.linenr
                        aktline_list.address = guest.adresse1 + " " + guest.adresse2 + " " + guest.adresse3
                        aktline_list.telefon = guest.telefon
                        aktline_list.fax = guest.fax
                        aktline_list.bemerk = akt_line.bemerk
                        aktline_list.username = bediener.username
                        aktline_list.gastnr = akt_line.gastnr
                        aktline_list.guest_type = guest.karteityp

                        akt_kont = get_cache (Akt_kont, {"gastnr": [(eq, guest.gastnr)],"kontakt_nr": [(eq, akt_line.kontakt_nr)]})

                        if akt_kont:
                            aktline_list.email = akt_kont.email
                        aktline_list.priority = prioritaet[aktline_list.prioritaet - 1]

    def disp_all2():

        nonlocal aktline_list_data, prioritaet, akt_code, guest, bediener, akt_line, akt_kont
        nonlocal inp_gastnr, next_date, all_flag, prior, act_combo, acttype, user_init, to_date


        nonlocal aktline_list
        nonlocal aktline_list_data

        if all_flag:

            if act_combo.lower()  == ("ALL").lower() :

                akt_line_obj_list = {}
                akt_line = Akt_line()
                akt_code = Akt_code()
                guest = Guest()
                bediener = Bediener()
                for akt_line.datum, akt_line.zeit, akt_line.dauer, akt_line.prioritaet, akt_line.kontakt, akt_line.regard, akt_line.userinit, akt_line.linenr, akt_line.bemerk, akt_line.gastnr, akt_line.kontakt_nr, akt_line._recid, akt_code.bezeich, akt_code._recid, guest.name, guest.anredefirma, guest.adresse1, guest.adresse2, guest.adresse3, guest.telefon, guest.fax, guest.karteityp, guest.gastnr, guest._recid, bediener.username, bediener._recid in db_session.query(Akt_line.datum, Akt_line.zeit, Akt_line.dauer, Akt_line.prioritaet, Akt_line.kontakt, Akt_line.regard, Akt_line.userinit, Akt_line.linenr, Akt_line.bemerk, Akt_line.gastnr, Akt_line.kontakt_nr, Akt_line._recid, Akt_code.bezeich, Akt_code._recid, Guest.name, Guest.anredefirma, Guest.adresse1, Guest.adresse2, Guest.adresse3, Guest.telefon, Guest.fax, Guest.karteityp, Guest.gastnr, Guest._recid, Bediener.username, Bediener._recid).join(Akt_code,(Akt_code.aktionscode == Akt_line.aktionscode)).join(Guest,(Guest.gastnr == Akt_line.gastnr)).join(Bediener,(Bediener.userinit == Akt_line.userinit)).filter(
                             (Akt_line.flag == acttype) & (Akt_line.gastnr == inp_gastnr)).order_by(Akt_line.datum, Akt_line.zeit, Akt_line.prioritaet.desc()).all():
                    if akt_line_obj_list.get(akt_line._recid):
                        continue
                    else:
                        akt_line_obj_list[akt_line._recid] = True


                    aktline_list = Aktline_list()
                    aktline_list_data.append(aktline_list)

                    aktline_list.bezeich = akt_code.bezeich
                    aktline_list.datum = akt_line.datum
                    aktline_list.zeit = akt_line.zeit
                    aktline_list.dauer = akt_line.dauer
                    aktline_list.ftime = to_string(akt_line.zeit, "HH:MM")
                    aktline_list.ttime = to_string(akt_line.dauer, "HH:MM")
                    aktline_list.prioritaet = akt_line.prioritaet
                    aktline_list.kontakt = akt_line.kontakt
                    aktline_list.name = guest.name + ", " + guest.anredefirma
                    aktline_list.regard = akt_line.regard
                    aktline_list.userinit = akt_line.userinit
                    aktline_list.linenr = akt_line.linenr
                    aktline_list.address = guest.adresse1 + " " + guest.adresse2 + " " + guest.adresse3
                    aktline_list.telefon = guest.telefon
                    aktline_list.fax = guest.fax
                    aktline_list.bemerk = akt_line.bemerk
                    aktline_list.username = bediener.username
                    aktline_list.gastnr = akt_line.gastnr
                    aktline_list.guest_type = guest.karteityp

                    akt_kont = get_cache (Akt_kont, {"gastnr": [(eq, guest.gastnr)],"kontakt_nr": [(eq, akt_line.kontakt_nr)]})

                    if akt_kont:
                        aktline_list.email = akt_kont.email
                    aktline_list.priority = prioritaet[aktline_list.prioritaet - 1]

            else:

                akt_line_obj_list = {}
                akt_line = Akt_line()
                akt_code = Akt_code()
                guest = Guest()
                bediener = Bediener()
                for akt_line.datum, akt_line.zeit, akt_line.dauer, akt_line.prioritaet, akt_line.kontakt, akt_line.regard, akt_line.userinit, akt_line.linenr, akt_line.bemerk, akt_line.gastnr, akt_line.kontakt_nr, akt_line._recid, akt_code.bezeich, akt_code._recid, guest.name, guest.anredefirma, guest.adresse1, guest.adresse2, guest.adresse3, guest.telefon, guest.fax, guest.karteityp, guest.gastnr, guest._recid, bediener.username, bediener._recid in db_session.query(Akt_line.datum, Akt_line.zeit, Akt_line.dauer, Akt_line.prioritaet, Akt_line.kontakt, Akt_line.regard, Akt_line.userinit, Akt_line.linenr, Akt_line.bemerk, Akt_line.gastnr, Akt_line.kontakt_nr, Akt_line._recid, Akt_code.bezeich, Akt_code._recid, Guest.name, Guest.anredefirma, Guest.adresse1, Guest.adresse2, Guest.adresse3, Guest.telefon, Guest.fax, Guest.karteityp, Guest.gastnr, Guest._recid, Bediener.username, Bediener._recid).join(Akt_code,(Akt_code.aktionscode == Akt_line.aktionscode) & (Akt_code.bezeich == (act_combo).lower())).join(Guest,(Guest.gastnr == Akt_line.gastnr)).join(Bediener,(Bediener.userinit == Akt_line.userinit)).filter(
                             (Akt_line.flag == acttype) & (Akt_line.gastnr == inp_gastnr)).order_by(Akt_line.datum, Akt_line.zeit, Akt_line.prioritaet.desc()).all():
                    if akt_line_obj_list.get(akt_line._recid):
                        continue
                    else:
                        akt_line_obj_list[akt_line._recid] = True


                    aktline_list = Aktline_list()
                    aktline_list_data.append(aktline_list)

                    aktline_list.bezeich = akt_code.bezeich
                    aktline_list.datum = akt_line.datum
                    aktline_list.zeit = akt_line.zeit
                    aktline_list.dauer = akt_line.dauer
                    aktline_list.ftime = to_string(akt_line.zeit, "HH:MM")
                    aktline_list.ttime = to_string(akt_line.dauer, "HH:MM")
                    aktline_list.prioritaet = akt_line.prioritaet
                    aktline_list.kontakt = akt_line.kontakt
                    aktline_list.name = guest.name + ", " + guest.anredefirma
                    aktline_list.regard = akt_line.regard
                    aktline_list.userinit = akt_line.userinit
                    aktline_list.linenr = akt_line.linenr
                    aktline_list.address = guest.adresse1 + " " + guest.adresse2 + " " + guest.adresse3
                    aktline_list.telefon = guest.telefon
                    aktline_list.fax = guest.fax
                    aktline_list.bemerk = akt_line.bemerk
                    aktline_list.username = bediener.username
                    aktline_list.gastnr = akt_line.gastnr
                    aktline_list.guest_type = guest.karteityp

                    akt_kont = get_cache (Akt_kont, {"gastnr": [(eq, guest.gastnr)],"kontakt_nr": [(eq, akt_line.kontakt_nr)]})

                    if akt_kont:
                        aktline_list.email = akt_kont.email
                    aktline_list.priority = prioritaet[aktline_list.prioritaet - 1]

        else:

            if act_combo.lower()  == ("ALL").lower() :

                akt_line_obj_list = {}
                akt_line = Akt_line()
                akt_code = Akt_code()
                guest = Guest()
                bediener = Bediener()
                for akt_line.datum, akt_line.zeit, akt_line.dauer, akt_line.prioritaet, akt_line.kontakt, akt_line.regard, akt_line.userinit, akt_line.linenr, akt_line.bemerk, akt_line.gastnr, akt_line.kontakt_nr, akt_line._recid, akt_code.bezeich, akt_code._recid, guest.name, guest.anredefirma, guest.adresse1, guest.adresse2, guest.adresse3, guest.telefon, guest.fax, guest.karteityp, guest.gastnr, guest._recid, bediener.username, bediener._recid in db_session.query(Akt_line.datum, Akt_line.zeit, Akt_line.dauer, Akt_line.prioritaet, Akt_line.kontakt, Akt_line.regard, Akt_line.userinit, Akt_line.linenr, Akt_line.bemerk, Akt_line.gastnr, Akt_line.kontakt_nr, Akt_line._recid, Akt_code.bezeich, Akt_code._recid, Guest.name, Guest.anredefirma, Guest.adresse1, Guest.adresse2, Guest.adresse3, Guest.telefon, Guest.fax, Guest.karteityp, Guest.gastnr, Guest._recid, Bediener.username, Bediener._recid).join(Akt_code,(Akt_code.aktionscode == Akt_line.aktionscode)).join(Guest,(Guest.gastnr == Akt_line.gastnr)).join(Bediener,(Bediener.userinit == Akt_line.userinit)).filter(
                             (Akt_line.flag == acttype) & (Akt_line.userinit == (user_init).lower()) & (Akt_line.gastnr == inp_gastnr)).order_by(Akt_line.datum, Akt_line.zeit, Akt_line.prioritaet.desc()).all():
                    if akt_line_obj_list.get(akt_line._recid):
                        continue
                    else:
                        akt_line_obj_list[akt_line._recid] = True


                    aktline_list = Aktline_list()
                    aktline_list_data.append(aktline_list)

                    aktline_list.bezeich = akt_code.bezeich
                    aktline_list.datum = akt_line.datum
                    aktline_list.zeit = akt_line.zeit
                    aktline_list.dauer = akt_line.dauer
                    aktline_list.ftime = to_string(akt_line.zeit, "HH:MM")
                    aktline_list.ttime = to_string(akt_line.dauer, "HH:MM")
                    aktline_list.prioritaet = akt_line.prioritaet
                    aktline_list.kontakt = akt_line.kontakt
                    aktline_list.name = guest.name + ", " + guest.anredefirma
                    aktline_list.regard = akt_line.regard
                    aktline_list.userinit = akt_line.userinit
                    aktline_list.linenr = akt_line.linenr
                    aktline_list.address = guest.adresse1 + " " + guest.adresse2 + " " + guest.adresse3
                    aktline_list.telefon = guest.telefon
                    aktline_list.fax = guest.fax
                    aktline_list.bemerk = akt_line.bemerk
                    aktline_list.username = bediener.username
                    aktline_list.gastnr = akt_line.gastnr
                    aktline_list.guest_type = guest.karteityp

                    akt_kont = get_cache (Akt_kont, {"gastnr": [(eq, guest.gastnr)],"kontakt_nr": [(eq, akt_line.kontakt_nr)]})

                    if akt_kont:
                        aktline_list.email = akt_kont.email
                    aktline_list.priority = prioritaet[aktline_list.prioritaet - 1]

            else:

                akt_line_obj_list = {}
                akt_line = Akt_line()
                akt_code = Akt_code()
                guest = Guest()
                bediener = Bediener()
                for akt_line.datum, akt_line.zeit, akt_line.dauer, akt_line.prioritaet, akt_line.kontakt, akt_line.regard, akt_line.userinit, akt_line.linenr, akt_line.bemerk, akt_line.gastnr, akt_line.kontakt_nr, akt_line._recid, akt_code.bezeich, akt_code._recid, guest.name, guest.anredefirma, guest.adresse1, guest.adresse2, guest.adresse3, guest.telefon, guest.fax, guest.karteityp, guest.gastnr, guest._recid, bediener.username, bediener._recid in db_session.query(Akt_line.datum, Akt_line.zeit, Akt_line.dauer, Akt_line.prioritaet, Akt_line.kontakt, Akt_line.regard, Akt_line.userinit, Akt_line.linenr, Akt_line.bemerk, Akt_line.gastnr, Akt_line.kontakt_nr, Akt_line._recid, Akt_code.bezeich, Akt_code._recid, Guest.name, Guest.anredefirma, Guest.adresse1, Guest.adresse2, Guest.adresse3, Guest.telefon, Guest.fax, Guest.karteityp, Guest.gastnr, Guest._recid, Bediener.username, Bediener._recid).join(Akt_code,(Akt_code.aktionscode == Akt_line.aktionscode) & (Akt_code.bezeich == (act_combo).lower())).join(Guest,(Guest.gastnr == Akt_line.gastnr)).join(Bediener,(Bediener.userinit == Akt_line.userinit)).filter(
                             (Akt_line.flag == acttype) & (Akt_line.userinit == (user_init).lower()) & (Akt_line.gastnr == inp_gastnr)).order_by(Akt_line.datum, Akt_line.zeit, Akt_line.prioritaet.desc()).all():
                    if akt_line_obj_list.get(akt_line._recid):
                        continue
                    else:
                        akt_line_obj_list[akt_line._recid] = True


                    aktline_list = Aktline_list()
                    aktline_list_data.append(aktline_list)

                    aktline_list.bezeich = akt_code.bezeich
                    aktline_list.datum = akt_line.datum
                    aktline_list.zeit = akt_line.zeit
                    aktline_list.dauer = akt_line.dauer
                    aktline_list.ftime = to_string(akt_line.zeit, "HH:MM")
                    aktline_list.ttime = to_string(akt_line.dauer, "HH:MM")
                    aktline_list.prioritaet = akt_line.prioritaet
                    aktline_list.kontakt = akt_line.kontakt
                    aktline_list.name = guest.name + ", " + guest.anredefirma
                    aktline_list.regard = akt_line.regard
                    aktline_list.userinit = akt_line.userinit
                    aktline_list.linenr = akt_line.linenr
                    aktline_list.address = guest.adresse1 + " " + guest.adresse2 + " " + guest.adresse3
                    aktline_list.telefon = guest.telefon
                    aktline_list.fax = guest.fax
                    aktline_list.bemerk = akt_line.bemerk
                    aktline_list.username = bediener.username
                    aktline_list.gastnr = akt_line.gastnr
                    aktline_list.guest_type = guest.karteityp

                    akt_kont = get_cache (Akt_kont, {"gastnr": [(eq, guest.gastnr)],"kontakt_nr": [(eq, akt_line.kontakt_nr)]})

                    if akt_kont:
                        aktline_list.email = akt_kont.email
                    aktline_list.priority = prioritaet[aktline_list.prioritaet - 1]

    def disp_it():

        nonlocal aktline_list_data, prioritaet, akt_code, guest, bediener, akt_line, akt_kont
        nonlocal inp_gastnr, next_date, all_flag, prior, act_combo, acttype, user_init, to_date


        nonlocal aktline_list
        nonlocal aktline_list_data

        if all_flag:

            if prior == 0:

                if act_combo.lower()  == ("ALL").lower() :

                    akt_line_obj_list = {}
                    akt_line = Akt_line()
                    akt_code = Akt_code()
                    guest = Guest()
                    bediener = Bediener()
                    for akt_line.datum, akt_line.zeit, akt_line.dauer, akt_line.prioritaet, akt_line.kontakt, akt_line.regard, akt_line.userinit, akt_line.linenr, akt_line.bemerk, akt_line.gastnr, akt_line.kontakt_nr, akt_line._recid, akt_code.bezeich, akt_code._recid, guest.name, guest.anredefirma, guest.adresse1, guest.adresse2, guest.adresse3, guest.telefon, guest.fax, guest.karteityp, guest.gastnr, guest._recid, bediener.username, bediener._recid in db_session.query(Akt_line.datum, Akt_line.zeit, Akt_line.dauer, Akt_line.prioritaet, Akt_line.kontakt, Akt_line.regard, Akt_line.userinit, Akt_line.linenr, Akt_line.bemerk, Akt_line.gastnr, Akt_line.kontakt_nr, Akt_line._recid, Akt_code.bezeich, Akt_code._recid, Guest.name, Guest.anredefirma, Guest.adresse1, Guest.adresse2, Guest.adresse3, Guest.telefon, Guest.fax, Guest.karteityp, Guest.gastnr, Guest._recid, Bediener.username, Bediener._recid).join(Akt_code,(Akt_code.aktionscode == Akt_line.aktionscode)).join(Guest,(Guest.gastnr == Akt_line.gastnr)).join(Bediener,(Bediener.userinit == Akt_line.userinit)).filter(
                                 (Akt_line.flag == acttype) & (Akt_line.datum >= next_date) & (Akt_line.datum <= to_date)).order_by(Akt_line.datum, Akt_line.zeit, Akt_line.prioritaet.desc()).all():
                        if akt_line_obj_list.get(akt_line._recid):
                            continue
                        else:
                            akt_line_obj_list[akt_line._recid] = True


                        aktline_list = Aktline_list()
                        aktline_list_data.append(aktline_list)

                        aktline_list.bezeich = akt_code.bezeich
                        aktline_list.datum = akt_line.datum
                        aktline_list.zeit = akt_line.zeit
                        aktline_list.dauer = akt_line.dauer
                        aktline_list.ftime = to_string(akt_line.zeit, "HH:MM")
                        aktline_list.ttime = to_string(akt_line.dauer, "HH:MM")
                        aktline_list.prioritaet = akt_line.prioritaet
                        aktline_list.kontakt = akt_line.kontakt
                        aktline_list.name = guest.name + ", " + guest.anredefirma
                        aktline_list.regard = akt_line.regard
                        aktline_list.userinit = akt_line.userinit
                        aktline_list.linenr = akt_line.linenr
                        aktline_list.address = guest.adresse1 + " " + guest.adresse2 + " " + guest.adresse3
                        aktline_list.telefon = guest.telefon
                        aktline_list.fax = guest.fax
                        aktline_list.bemerk = akt_line.bemerk
                        aktline_list.username = bediener.username
                        aktline_list.gastnr = akt_line.gastnr
                        aktline_list.guest_type = guest.karteityp

                        akt_kont = get_cache (Akt_kont, {"gastnr": [(eq, guest.gastnr)],"kontakt_nr": [(eq, akt_line.kontakt_nr)]})

                        if akt_kont:
                            aktline_list.email = akt_kont.email
                        aktline_list.priority = prioritaet[aktline_list.prioritaet - 1]

                else:

                    akt_line_obj_list = {}
                    akt_line = Akt_line()
                    akt_code = Akt_code()
                    guest = Guest()
                    bediener = Bediener()
                    for akt_line.datum, akt_line.zeit, akt_line.dauer, akt_line.prioritaet, akt_line.kontakt, akt_line.regard, akt_line.userinit, akt_line.linenr, akt_line.bemerk, akt_line.gastnr, akt_line.kontakt_nr, akt_line._recid, akt_code.bezeich, akt_code._recid, guest.name, guest.anredefirma, guest.adresse1, guest.adresse2, guest.adresse3, guest.telefon, guest.fax, guest.karteityp, guest.gastnr, guest._recid, bediener.username, bediener._recid in db_session.query(Akt_line.datum, Akt_line.zeit, Akt_line.dauer, Akt_line.prioritaet, Akt_line.kontakt, Akt_line.regard, Akt_line.userinit, Akt_line.linenr, Akt_line.bemerk, Akt_line.gastnr, Akt_line.kontakt_nr, Akt_line._recid, Akt_code.bezeich, Akt_code._recid, Guest.name, Guest.anredefirma, Guest.adresse1, Guest.adresse2, Guest.adresse3, Guest.telefon, Guest.fax, Guest.karteityp, Guest.gastnr, Guest._recid, Bediener.username, Bediener._recid).join(Akt_code,(Akt_code.aktionscode == Akt_line.aktionscode) & (Akt_code.bezeich == (act_combo).lower())).join(Guest,(Guest.gastnr == Akt_line.gastnr)).join(Bediener,(Bediener.userinit == Akt_line.userinit)).filter(
                                 (Akt_line.flag == acttype) & (Akt_line.datum >= next_date) & (Akt_line.datum <= to_date)).order_by(Akt_line.datum, Akt_line.zeit, Akt_line.prioritaet.desc()).all():
                        if akt_line_obj_list.get(akt_line._recid):
                            continue
                        else:
                            akt_line_obj_list[akt_line._recid] = True


                        aktline_list = Aktline_list()
                        aktline_list_data.append(aktline_list)

                        aktline_list.bezeich = akt_code.bezeich
                        aktline_list.datum = akt_line.datum
                        aktline_list.zeit = akt_line.zeit
                        aktline_list.dauer = akt_line.dauer
                        aktline_list.ftime = to_string(akt_line.zeit, "HH:MM")
                        aktline_list.ttime = to_string(akt_line.dauer, "HH:MM")
                        aktline_list.prioritaet = akt_line.prioritaet
                        aktline_list.kontakt = akt_line.kontakt
                        aktline_list.name = guest.name + ", " + guest.anredefirma
                        aktline_list.regard = akt_line.regard
                        aktline_list.userinit = akt_line.userinit
                        aktline_list.linenr = akt_line.linenr
                        aktline_list.address = guest.adresse1 + " " + guest.adresse2 + " " + guest.adresse3
                        aktline_list.telefon = guest.telefon
                        aktline_list.fax = guest.fax
                        aktline_list.bemerk = akt_line.bemerk
                        aktline_list.username = bediener.username
                        aktline_list.gastnr = akt_line.gastnr
                        aktline_list.guest_type = guest.karteityp

                        akt_kont = get_cache (Akt_kont, {"gastnr": [(eq, guest.gastnr)],"kontakt_nr": [(eq, akt_line.kontakt_nr)]})

                        if akt_kont:
                            aktline_list.email = akt_kont.email
                        aktline_list.priority = prioritaet[aktline_list.prioritaet - 1]

            else:

                if act_combo.lower()  == ("ALL").lower() :

                    akt_line_obj_list = {}
                    akt_line = Akt_line()
                    akt_code = Akt_code()
                    guest = Guest()
                    bediener = Bediener()
                    for akt_line.datum, akt_line.zeit, akt_line.dauer, akt_line.prioritaet, akt_line.kontakt, akt_line.regard, akt_line.userinit, akt_line.linenr, akt_line.bemerk, akt_line.gastnr, akt_line.kontakt_nr, akt_line._recid, akt_code.bezeich, akt_code._recid, guest.name, guest.anredefirma, guest.adresse1, guest.adresse2, guest.adresse3, guest.telefon, guest.fax, guest.karteityp, guest.gastnr, guest._recid, bediener.username, bediener._recid in db_session.query(Akt_line.datum, Akt_line.zeit, Akt_line.dauer, Akt_line.prioritaet, Akt_line.kontakt, Akt_line.regard, Akt_line.userinit, Akt_line.linenr, Akt_line.bemerk, Akt_line.gastnr, Akt_line.kontakt_nr, Akt_line._recid, Akt_code.bezeich, Akt_code._recid, Guest.name, Guest.anredefirma, Guest.adresse1, Guest.adresse2, Guest.adresse3, Guest.telefon, Guest.fax, Guest.karteityp, Guest.gastnr, Guest._recid, Bediener.username, Bediener._recid).join(Akt_code,(Akt_code.aktionscode == Akt_line.aktionscode)).join(Guest,(Guest.gastnr == Akt_line.gastnr)).join(Bediener,(Bediener.userinit == Akt_line.userinit)).filter(
                                 (Akt_line.flag == acttype) & (Akt_line.datum >= next_date) & (Akt_line.datum <= to_date) & (Akt_line.prioritaet == prior)).order_by(Akt_line.datum, Akt_line.zeit, Akt_line.prioritaet.desc()).all():
                        if akt_line_obj_list.get(akt_line._recid):
                            continue
                        else:
                            akt_line_obj_list[akt_line._recid] = True


                        aktline_list = Aktline_list()
                        aktline_list_data.append(aktline_list)

                        aktline_list.bezeich = akt_code.bezeich
                        aktline_list.datum = akt_line.datum
                        aktline_list.zeit = akt_line.zeit
                        aktline_list.dauer = akt_line.dauer
                        aktline_list.ftime = to_string(akt_line.zeit, "HH:MM")
                        aktline_list.ttime = to_string(akt_line.dauer, "HH:MM")
                        aktline_list.prioritaet = akt_line.prioritaet
                        aktline_list.kontakt = akt_line.kontakt
                        aktline_list.name = guest.name + ", " + guest.anredefirma
                        aktline_list.regard = akt_line.regard
                        aktline_list.userinit = akt_line.userinit
                        aktline_list.linenr = akt_line.linenr
                        aktline_list.address = guest.adresse1 + " " + guest.adresse2 + " " + guest.adresse3
                        aktline_list.telefon = guest.telefon
                        aktline_list.fax = guest.fax
                        aktline_list.bemerk = akt_line.bemerk
                        aktline_list.username = bediener.username
                        aktline_list.gastnr = akt_line.gastnr
                        aktline_list.guest_type = guest.karteityp

                        akt_kont = get_cache (Akt_kont, {"gastnr": [(eq, guest.gastnr)],"kontakt_nr": [(eq, akt_line.kontakt_nr)]})

                        if akt_kont:
                            aktline_list.email = akt_kont.email
                        aktline_list.priority = prioritaet[aktline_list.prioritaet - 1]

                else:

                    akt_line_obj_list = {}
                    akt_line = Akt_line()
                    akt_code = Akt_code()
                    guest = Guest()
                    bediener = Bediener()
                    for akt_line.datum, akt_line.zeit, akt_line.dauer, akt_line.prioritaet, akt_line.kontakt, akt_line.regard, akt_line.userinit, akt_line.linenr, akt_line.bemerk, akt_line.gastnr, akt_line.kontakt_nr, akt_line._recid, akt_code.bezeich, akt_code._recid, guest.name, guest.anredefirma, guest.adresse1, guest.adresse2, guest.adresse3, guest.telefon, guest.fax, guest.karteityp, guest.gastnr, guest._recid, bediener.username, bediener._recid in db_session.query(Akt_line.datum, Akt_line.zeit, Akt_line.dauer, Akt_line.prioritaet, Akt_line.kontakt, Akt_line.regard, Akt_line.userinit, Akt_line.linenr, Akt_line.bemerk, Akt_line.gastnr, Akt_line.kontakt_nr, Akt_line._recid, Akt_code.bezeich, Akt_code._recid, Guest.name, Guest.anredefirma, Guest.adresse1, Guest.adresse2, Guest.adresse3, Guest.telefon, Guest.fax, Guest.karteityp, Guest.gastnr, Guest._recid, Bediener.username, Bediener._recid).join(Akt_code,(Akt_code.aktionscode == Akt_line.aktionscode) & (Akt_code.bezeich == (act_combo).lower())).join(Guest,(Guest.gastnr == Akt_line.gastnr)).join(Bediener,(Bediener.userinit == Akt_line.userinit)).filter(
                                 (Akt_line.flag == acttype) & (Akt_line.datum >= next_date) & (Akt_line.datum <= to_date) & (Akt_line.prioritaet == prior)).order_by(Akt_line.datum, Akt_line.zeit, Akt_line.prioritaet.desc()).all():
                        if akt_line_obj_list.get(akt_line._recid):
                            continue
                        else:
                            akt_line_obj_list[akt_line._recid] = True


                        aktline_list = Aktline_list()
                        aktline_list_data.append(aktline_list)

                        aktline_list.bezeich = akt_code.bezeich
                        aktline_list.datum = akt_line.datum
                        aktline_list.zeit = akt_line.zeit
                        aktline_list.dauer = akt_line.dauer
                        aktline_list.ftime = to_string(akt_line.zeit, "HH:MM")
                        aktline_list.ttime = to_string(akt_line.dauer, "HH:MM")
                        aktline_list.prioritaet = akt_line.prioritaet
                        aktline_list.kontakt = akt_line.kontakt
                        aktline_list.name = guest.name + ", " + guest.anredefirma
                        aktline_list.regard = akt_line.regard
                        aktline_list.userinit = akt_line.userinit
                        aktline_list.linenr = akt_line.linenr
                        aktline_list.address = guest.adresse1 + " " + guest.adresse2 + " " + guest.adresse3
                        aktline_list.telefon = guest.telefon
                        aktline_list.fax = guest.fax
                        aktline_list.bemerk = akt_line.bemerk
                        aktline_list.username = bediener.username
                        aktline_list.gastnr = akt_line.gastnr
                        aktline_list.guest_type = guest.karteityp

                        akt_kont = get_cache (Akt_kont, {"gastnr": [(eq, guest.gastnr)],"kontakt_nr": [(eq, akt_line.kontakt_nr)]})

                        if akt_kont:
                            aktline_list.email = akt_kont.email
                        aktline_list.priority = prioritaet[aktline_list.prioritaet - 1]

        else:

            if prior == 0:

                if act_combo.lower()  == ("ALL").lower() :

                    akt_line_obj_list = {}
                    akt_line = Akt_line()
                    akt_code = Akt_code()
                    guest = Guest()
                    bediener = Bediener()
                    for akt_line.datum, akt_line.zeit, akt_line.dauer, akt_line.prioritaet, akt_line.kontakt, akt_line.regard, akt_line.userinit, akt_line.linenr, akt_line.bemerk, akt_line.gastnr, akt_line.kontakt_nr, akt_line._recid, akt_code.bezeich, akt_code._recid, guest.name, guest.anredefirma, guest.adresse1, guest.adresse2, guest.adresse3, guest.telefon, guest.fax, guest.karteityp, guest.gastnr, guest._recid, bediener.username, bediener._recid in db_session.query(Akt_line.datum, Akt_line.zeit, Akt_line.dauer, Akt_line.prioritaet, Akt_line.kontakt, Akt_line.regard, Akt_line.userinit, Akt_line.linenr, Akt_line.bemerk, Akt_line.gastnr, Akt_line.kontakt_nr, Akt_line._recid, Akt_code.bezeich, Akt_code._recid, Guest.name, Guest.anredefirma, Guest.adresse1, Guest.adresse2, Guest.adresse3, Guest.telefon, Guest.fax, Guest.karteityp, Guest.gastnr, Guest._recid, Bediener.username, Bediener._recid).join(Akt_code,(Akt_code.aktionscode == Akt_line.aktionscode)).join(Guest,(Guest.gastnr == Akt_line.gastnr)).join(Bediener,(Bediener.userinit == Akt_line.userinit)).filter(
                                 (Akt_line.flag == acttype) & (Akt_line.userinit == (user_init).lower()) & (Akt_line.datum >= next_date) & (Akt_line.datum <= to_date)).order_by(Akt_line.datum, Akt_line.zeit, Akt_line.prioritaet.desc()).all():
                        if akt_line_obj_list.get(akt_line._recid):
                            continue
                        else:
                            akt_line_obj_list[akt_line._recid] = True


                        aktline_list = Aktline_list()
                        aktline_list_data.append(aktline_list)

                        aktline_list.bezeich = akt_code.bezeich
                        aktline_list.datum = akt_line.datum
                        aktline_list.zeit = akt_line.zeit
                        aktline_list.dauer = akt_line.dauer
                        aktline_list.ftime = to_string(akt_line.zeit, "HH:MM")
                        aktline_list.ttime = to_string(akt_line.dauer, "HH:MM")
                        aktline_list.prioritaet = akt_line.prioritaet
                        aktline_list.kontakt = akt_line.kontakt
                        aktline_list.name = guest.name + ", " + guest.anredefirma
                        aktline_list.regard = akt_line.regard
                        aktline_list.userinit = akt_line.userinit
                        aktline_list.linenr = akt_line.linenr
                        aktline_list.address = guest.adresse1 + " " + guest.adresse2 + " " + guest.adresse3
                        aktline_list.telefon = guest.telefon
                        aktline_list.fax = guest.fax
                        aktline_list.bemerk = akt_line.bemerk
                        aktline_list.username = bediener.username
                        aktline_list.gastnr = akt_line.gastnr
                        aktline_list.guest_type = guest.karteityp

                        akt_kont = get_cache (Akt_kont, {"gastnr": [(eq, guest.gastnr)],"kontakt_nr": [(eq, akt_line.kontakt_nr)]})

                        if akt_kont:
                            aktline_list.email = akt_kont.email
                        aktline_list.priority = prioritaet[aktline_list.prioritaet - 1]

                else:

                    akt_line_obj_list = {}
                    akt_line = Akt_line()
                    akt_code = Akt_code()
                    guest = Guest()
                    bediener = Bediener()
                    for akt_line.datum, akt_line.zeit, akt_line.dauer, akt_line.prioritaet, akt_line.kontakt, akt_line.regard, akt_line.userinit, akt_line.linenr, akt_line.bemerk, akt_line.gastnr, akt_line.kontakt_nr, akt_line._recid, akt_code.bezeich, akt_code._recid, guest.name, guest.anredefirma, guest.adresse1, guest.adresse2, guest.adresse3, guest.telefon, guest.fax, guest.karteityp, guest.gastnr, guest._recid, bediener.username, bediener._recid in db_session.query(Akt_line.datum, Akt_line.zeit, Akt_line.dauer, Akt_line.prioritaet, Akt_line.kontakt, Akt_line.regard, Akt_line.userinit, Akt_line.linenr, Akt_line.bemerk, Akt_line.gastnr, Akt_line.kontakt_nr, Akt_line._recid, Akt_code.bezeich, Akt_code._recid, Guest.name, Guest.anredefirma, Guest.adresse1, Guest.adresse2, Guest.adresse3, Guest.telefon, Guest.fax, Guest.karteityp, Guest.gastnr, Guest._recid, Bediener.username, Bediener._recid).join(Akt_code,(Akt_code.aktionscode == Akt_line.aktionscode) & (Akt_code.bezeich == (act_combo).lower())).join(Guest,(Guest.gastnr == Akt_line.gastnr)).join(Bediener,(Bediener.userinit == Akt_line.userinit)).filter(
                                 (Akt_line.flag == acttype) & (Akt_line.userinit == (user_init).lower()) & (Akt_line.datum >= next_date) & (Akt_line.datum <= to_date)).order_by(Akt_line.datum, Akt_line.zeit, Akt_line.prioritaet.desc()).all():
                        if akt_line_obj_list.get(akt_line._recid):
                            continue
                        else:
                            akt_line_obj_list[akt_line._recid] = True


                        aktline_list = Aktline_list()
                        aktline_list_data.append(aktline_list)

                        aktline_list.bezeich = akt_code.bezeich
                        aktline_list.datum = akt_line.datum
                        aktline_list.zeit = akt_line.zeit
                        aktline_list.dauer = akt_line.dauer
                        aktline_list.ftime = to_string(akt_line.zeit, "HH:MM")
                        aktline_list.ttime = to_string(akt_line.dauer, "HH:MM")
                        aktline_list.prioritaet = akt_line.prioritaet
                        aktline_list.kontakt = akt_line.kontakt
                        aktline_list.name = guest.name + ", " + guest.anredefirma
                        aktline_list.regard = akt_line.regard
                        aktline_list.userinit = akt_line.userinit
                        aktline_list.linenr = akt_line.linenr
                        aktline_list.address = guest.adresse1 + " " + guest.adresse2 + " " + guest.adresse3
                        aktline_list.telefon = guest.telefon
                        aktline_list.fax = guest.fax
                        aktline_list.bemerk = akt_line.bemerk
                        aktline_list.username = bediener.username
                        aktline_list.gastnr = akt_line.gastnr
                        aktline_list.guest_type = guest.karteityp

                        akt_kont = get_cache (Akt_kont, {"gastnr": [(eq, guest.gastnr)],"kontakt_nr": [(eq, akt_line.kontakt_nr)]})

                        if akt_kont:
                            aktline_list.email = akt_kont.email
                        aktline_list.priority = prioritaet[aktline_list.prioritaet - 1]

            else:

                if act_combo.lower()  == ("ALL").lower() :

                    akt_line_obj_list = {}
                    akt_line = Akt_line()
                    akt_code = Akt_code()
                    guest = Guest()
                    bediener = Bediener()
                    for akt_line.datum, akt_line.zeit, akt_line.dauer, akt_line.prioritaet, akt_line.kontakt, akt_line.regard, akt_line.userinit, akt_line.linenr, akt_line.bemerk, akt_line.gastnr, akt_line.kontakt_nr, akt_line._recid, akt_code.bezeich, akt_code._recid, guest.name, guest.anredefirma, guest.adresse1, guest.adresse2, guest.adresse3, guest.telefon, guest.fax, guest.karteityp, guest.gastnr, guest._recid, bediener.username, bediener._recid in db_session.query(Akt_line.datum, Akt_line.zeit, Akt_line.dauer, Akt_line.prioritaet, Akt_line.kontakt, Akt_line.regard, Akt_line.userinit, Akt_line.linenr, Akt_line.bemerk, Akt_line.gastnr, Akt_line.kontakt_nr, Akt_line._recid, Akt_code.bezeich, Akt_code._recid, Guest.name, Guest.anredefirma, Guest.adresse1, Guest.adresse2, Guest.adresse3, Guest.telefon, Guest.fax, Guest.karteityp, Guest.gastnr, Guest._recid, Bediener.username, Bediener._recid).join(Akt_code,(Akt_code.aktionscode == Akt_line.aktionscode)).join(Guest,(Guest.gastnr == Akt_line.gastnr)).join(Bediener,(Bediener.userinit == Akt_line.userinit)).filter(
                                 (Akt_line.flag == acttype) & (Akt_line.userinit == (user_init).lower()) & (Akt_line.datum >= next_date) & (Akt_line.datum <= to_date) & (Akt_line.prioritaet == prior)).order_by(Akt_line.datum, Akt_line.zeit, Akt_line.prioritaet.desc()).all():
                        if akt_line_obj_list.get(akt_line._recid):
                            continue
                        else:
                            akt_line_obj_list[akt_line._recid] = True


                        aktline_list = Aktline_list()
                        aktline_list_data.append(aktline_list)

                        aktline_list.bezeich = akt_code.bezeich
                        aktline_list.datum = akt_line.datum
                        aktline_list.zeit = akt_line.zeit
                        aktline_list.dauer = akt_line.dauer
                        aktline_list.ftime = to_string(akt_line.zeit, "HH:MM")
                        aktline_list.ttime = to_string(akt_line.dauer, "HH:MM")
                        aktline_list.prioritaet = akt_line.prioritaet
                        aktline_list.kontakt = akt_line.kontakt
                        aktline_list.name = guest.name + ", " + guest.anredefirma
                        aktline_list.regard = akt_line.regard
                        aktline_list.userinit = akt_line.userinit
                        aktline_list.linenr = akt_line.linenr
                        aktline_list.address = guest.adresse1 + " " + guest.adresse2 + " " + guest.adresse3
                        aktline_list.telefon = guest.telefon
                        aktline_list.fax = guest.fax
                        aktline_list.bemerk = akt_line.bemerk
                        aktline_list.username = bediener.username
                        aktline_list.gastnr = akt_line.gastnr
                        aktline_list.guest_type = guest.karteityp

                        akt_kont = get_cache (Akt_kont, {"gastnr": [(eq, guest.gastnr)],"kontakt_nr": [(eq, akt_line.kontakt_nr)]})

                        if akt_kont:
                            aktline_list.email = akt_kont.email
                        aktline_list.priority = prioritaet[aktline_list.prioritaet - 1]

                else:

                    akt_line_obj_list = {}
                    akt_line = Akt_line()
                    akt_code = Akt_code()
                    guest = Guest()
                    bediener = Bediener()
                    for akt_line.datum, akt_line.zeit, akt_line.dauer, akt_line.prioritaet, akt_line.kontakt, akt_line.regard, akt_line.userinit, akt_line.linenr, akt_line.bemerk, akt_line.gastnr, akt_line.kontakt_nr, akt_line._recid, akt_code.bezeich, akt_code._recid, guest.name, guest.anredefirma, guest.adresse1, guest.adresse2, guest.adresse3, guest.telefon, guest.fax, guest.karteityp, guest.gastnr, guest._recid, bediener.username, bediener._recid in db_session.query(Akt_line.datum, Akt_line.zeit, Akt_line.dauer, Akt_line.prioritaet, Akt_line.kontakt, Akt_line.regard, Akt_line.userinit, Akt_line.linenr, Akt_line.bemerk, Akt_line.gastnr, Akt_line.kontakt_nr, Akt_line._recid, Akt_code.bezeich, Akt_code._recid, Guest.name, Guest.anredefirma, Guest.adresse1, Guest.adresse2, Guest.adresse3, Guest.telefon, Guest.fax, Guest.karteityp, Guest.gastnr, Guest._recid, Bediener.username, Bediener._recid).join(Akt_code,(Akt_code.aktionscode == Akt_line.aktionscode) & (Akt_code.bezeich == (act_combo).lower())).join(Guest,(Guest.gastnr == Akt_line.gastnr)).join(Bediener,(Bediener.userinit == Akt_line.userinit)).filter(
                                 (Akt_line.flag == acttype) & (Akt_line.userinit == (user_init).lower()) & (Akt_line.datum >= next_date) & (Akt_line.datum <= to_date) & (Akt_line.prioritaet == prior)).order_by(Akt_line.datum, Akt_line.zeit, Akt_line.prioritaet.desc()).all():
                        if akt_line_obj_list.get(akt_line._recid):
                            continue
                        else:
                            akt_line_obj_list[akt_line._recid] = True


                        aktline_list = Aktline_list()
                        aktline_list_data.append(aktline_list)

                        aktline_list.bezeich = akt_code.bezeich
                        aktline_list.datum = akt_line.datum
                        aktline_list.zeit = akt_line.zeit
                        aktline_list.dauer = akt_line.dauer
                        aktline_list.ftime = to_string(akt_line.zeit, "HH:MM")
                        aktline_list.ttime = to_string(akt_line.dauer, "HH:MM")
                        aktline_list.prioritaet = akt_line.prioritaet
                        aktline_list.kontakt = akt_line.kontakt
                        aktline_list.name = guest.name + ", " + guest.anredefirma
                        aktline_list.regard = akt_line.regard
                        aktline_list.userinit = akt_line.userinit
                        aktline_list.linenr = akt_line.linenr
                        aktline_list.address = guest.adresse1 + " " + guest.adresse2 + " " + guest.adresse3
                        aktline_list.telefon = guest.telefon
                        aktline_list.fax = guest.fax
                        aktline_list.bemerk = akt_line.bemerk
                        aktline_list.username = bediener.username
                        aktline_list.gastnr = akt_line.gastnr
                        aktline_list.guest_type = guest.karteityp

                        akt_kont = get_cache (Akt_kont, {"gastnr": [(eq, guest.gastnr)],"kontakt_nr": [(eq, akt_line.kontakt_nr)]})

                        if akt_kont:
                            aktline_list.email = akt_kont.email
                        aktline_list.priority = prioritaet[aktline_list.prioritaet - 1]

    def disp_it2():

        nonlocal aktline_list_data, prioritaet, akt_code, guest, bediener, akt_line, akt_kont
        nonlocal inp_gastnr, next_date, all_flag, prior, act_combo, acttype, user_init, to_date


        nonlocal aktline_list
        nonlocal aktline_list_data

        if all_flag:

            if act_combo.lower()  == ("ALL").lower() :

                akt_line_obj_list = {}
                akt_line = Akt_line()
                akt_code = Akt_code()
                guest = Guest()
                bediener = Bediener()
                for akt_line.datum, akt_line.zeit, akt_line.dauer, akt_line.prioritaet, akt_line.kontakt, akt_line.regard, akt_line.userinit, akt_line.linenr, akt_line.bemerk, akt_line.gastnr, akt_line.kontakt_nr, akt_line._recid, akt_code.bezeich, akt_code._recid, guest.name, guest.anredefirma, guest.adresse1, guest.adresse2, guest.adresse3, guest.telefon, guest.fax, guest.karteityp, guest.gastnr, guest._recid, bediener.username, bediener._recid in db_session.query(Akt_line.datum, Akt_line.zeit, Akt_line.dauer, Akt_line.prioritaet, Akt_line.kontakt, Akt_line.regard, Akt_line.userinit, Akt_line.linenr, Akt_line.bemerk, Akt_line.gastnr, Akt_line.kontakt_nr, Akt_line._recid, Akt_code.bezeich, Akt_code._recid, Guest.name, Guest.anredefirma, Guest.adresse1, Guest.adresse2, Guest.adresse3, Guest.telefon, Guest.fax, Guest.karteityp, Guest.gastnr, Guest._recid, Bediener.username, Bediener._recid).join(Akt_code,(Akt_code.aktionscode == Akt_line.aktionscode)).join(Guest,(Guest.gastnr == Akt_line.gastnr)).join(Bediener,(Bediener.userinit == Akt_line.userinit)).filter(
                             (Akt_line.flag == acttype) & (Akt_line.datum >= next_date) & (Akt_line.datum <= to_date) & (Akt_line.gastnr == inp_gastnr)).order_by(Akt_line.datum, Akt_line.zeit, Akt_line.prioritaet.desc()).all():
                    if akt_line_obj_list.get(akt_line._recid):
                        continue
                    else:
                        akt_line_obj_list[akt_line._recid] = True


                    aktline_list = Aktline_list()
                    aktline_list_data.append(aktline_list)

                    aktline_list.bezeich = akt_code.bezeich
                    aktline_list.datum = akt_line.datum
                    aktline_list.zeit = akt_line.zeit
                    aktline_list.dauer = akt_line.dauer
                    aktline_list.ftime = to_string(akt_line.zeit, "HH:MM")
                    aktline_list.ttime = to_string(akt_line.dauer, "HH:MM")
                    aktline_list.prioritaet = akt_line.prioritaet
                    aktline_list.kontakt = akt_line.kontakt
                    aktline_list.name = guest.name + ", " + guest.anredefirma
                    aktline_list.regard = akt_line.regard
                    aktline_list.userinit = akt_line.userinit
                    aktline_list.linenr = akt_line.linenr
                    aktline_list.address = guest.adresse1 + " " + guest.adresse2 + " " + guest.adresse3
                    aktline_list.telefon = guest.telefon
                    aktline_list.fax = guest.fax
                    aktline_list.bemerk = akt_line.bemerk
                    aktline_list.username = bediener.username
                    aktline_list.gastnr = akt_line.gastnr
                    aktline_list.guest_type = guest.karteityp

                    akt_kont = get_cache (Akt_kont, {"gastnr": [(eq, guest.gastnr)],"kontakt_nr": [(eq, akt_line.kontakt_nr)]})

                    if akt_kont:
                        aktline_list.email = akt_kont.email
                    aktline_list.priority = prioritaet[aktline_list.prioritaet - 1]

            else:

                akt_line_obj_list = {}
                akt_line = Akt_line()
                akt_code = Akt_code()
                guest = Guest()
                bediener = Bediener()
                for akt_line.datum, akt_line.zeit, akt_line.dauer, akt_line.prioritaet, akt_line.kontakt, akt_line.regard, akt_line.userinit, akt_line.linenr, akt_line.bemerk, akt_line.gastnr, akt_line.kontakt_nr, akt_line._recid, akt_code.bezeich, akt_code._recid, guest.name, guest.anredefirma, guest.adresse1, guest.adresse2, guest.adresse3, guest.telefon, guest.fax, guest.karteityp, guest.gastnr, guest._recid, bediener.username, bediener._recid in db_session.query(Akt_line.datum, Akt_line.zeit, Akt_line.dauer, Akt_line.prioritaet, Akt_line.kontakt, Akt_line.regard, Akt_line.userinit, Akt_line.linenr, Akt_line.bemerk, Akt_line.gastnr, Akt_line.kontakt_nr, Akt_line._recid, Akt_code.bezeich, Akt_code._recid, Guest.name, Guest.anredefirma, Guest.adresse1, Guest.adresse2, Guest.adresse3, Guest.telefon, Guest.fax, Guest.karteityp, Guest.gastnr, Guest._recid, Bediener.username, Bediener._recid).join(Akt_code,(Akt_code.aktionscode == Akt_line.aktionscode) & (Akt_code.bezeich == (act_combo).lower())).join(Guest,(Guest.gastnr == Akt_line.gastnr)).join(Bediener,(Bediener.userinit == Akt_line.userinit)).filter(
                             (Akt_line.flag == acttype) & (Akt_line.datum >= next_date) & (Akt_line.datum <= to_date) & (Akt_line.gastnr == inp_gastnr)).order_by(Akt_line.datum, Akt_line.zeit, Akt_line.prioritaet.desc()).all():
                    if akt_line_obj_list.get(akt_line._recid):
                        continue
                    else:
                        akt_line_obj_list[akt_line._recid] = True


                    aktline_list = Aktline_list()
                    aktline_list_data.append(aktline_list)

                    aktline_list.bezeich = akt_code.bezeich
                    aktline_list.datum = akt_line.datum
                    aktline_list.zeit = akt_line.zeit
                    aktline_list.dauer = akt_line.dauer
                    aktline_list.ftime = to_string(akt_line.zeit, "HH:MM")
                    aktline_list.ttime = to_string(akt_line.dauer, "HH:MM")
                    aktline_list.prioritaet = akt_line.prioritaet
                    aktline_list.kontakt = akt_line.kontakt
                    aktline_list.name = guest.name + ", " + guest.anredefirma
                    aktline_list.regard = akt_line.regard
                    aktline_list.userinit = akt_line.userinit
                    aktline_list.linenr = akt_line.linenr
                    aktline_list.address = guest.adresse1 + " " + guest.adresse2 + " " + guest.adresse3
                    aktline_list.telefon = guest.telefon
                    aktline_list.fax = guest.fax
                    aktline_list.bemerk = akt_line.bemerk
                    aktline_list.username = bediener.username
                    aktline_list.gastnr = akt_line.gastnr
                    aktline_list.guest_type = guest.karteityp

                    akt_kont = get_cache (Akt_kont, {"gastnr": [(eq, guest.gastnr)],"kontakt_nr": [(eq, akt_line.kontakt_nr)]})

                    if akt_kont:
                        aktline_list.email = akt_kont.email
                    aktline_list.priority = prioritaet[aktline_list.prioritaet - 1]

        else:

            if act_combo.lower()  == ("ALL").lower() :

                akt_line_obj_list = {}
                akt_line = Akt_line()
                akt_code = Akt_code()
                guest = Guest()
                bediener = Bediener()
                for akt_line.datum, akt_line.zeit, akt_line.dauer, akt_line.prioritaet, akt_line.kontakt, akt_line.regard, akt_line.userinit, akt_line.linenr, akt_line.bemerk, akt_line.gastnr, akt_line.kontakt_nr, akt_line._recid, akt_code.bezeich, akt_code._recid, guest.name, guest.anredefirma, guest.adresse1, guest.adresse2, guest.adresse3, guest.telefon, guest.fax, guest.karteityp, guest.gastnr, guest._recid, bediener.username, bediener._recid in db_session.query(Akt_line.datum, Akt_line.zeit, Akt_line.dauer, Akt_line.prioritaet, Akt_line.kontakt, Akt_line.regard, Akt_line.userinit, Akt_line.linenr, Akt_line.bemerk, Akt_line.gastnr, Akt_line.kontakt_nr, Akt_line._recid, Akt_code.bezeich, Akt_code._recid, Guest.name, Guest.anredefirma, Guest.adresse1, Guest.adresse2, Guest.adresse3, Guest.telefon, Guest.fax, Guest.karteityp, Guest.gastnr, Guest._recid, Bediener.username, Bediener._recid).join(Akt_code,(Akt_code.aktionscode == Akt_line.aktionscode)).join(Guest,(Guest.gastnr == Akt_line.gastnr)).join(Bediener,(Bediener.userinit == Akt_line.userinit)).filter(
                             (Akt_line.flag == acttype) & (Akt_line.userinit == (user_init).lower()) & (Akt_line.datum >= next_date) & (Akt_line.datum <= to_date) & (Akt_line.gastnr == inp_gastnr)).order_by(Akt_line.datum, Akt_line.zeit, Akt_line.prioritaet.desc()).all():
                    if akt_line_obj_list.get(akt_line._recid):
                        continue
                    else:
                        akt_line_obj_list[akt_line._recid] = True


                    aktline_list = Aktline_list()
                    aktline_list_data.append(aktline_list)

                    aktline_list.bezeich = akt_code.bezeich
                    aktline_list.datum = akt_line.datum
                    aktline_list.zeit = akt_line.zeit
                    aktline_list.dauer = akt_line.dauer
                    aktline_list.ftime = to_string(akt_line.zeit, "HH:MM")
                    aktline_list.ttime = to_string(akt_line.dauer, "HH:MM")
                    aktline_list.prioritaet = akt_line.prioritaet
                    aktline_list.kontakt = akt_line.kontakt
                    aktline_list.name = guest.name + ", " + guest.anredefirma
                    aktline_list.regard = akt_line.regard
                    aktline_list.userinit = akt_line.userinit
                    aktline_list.linenr = akt_line.linenr
                    aktline_list.address = guest.adresse1 + " " + guest.adresse2 + " " + guest.adresse3
                    aktline_list.telefon = guest.telefon
                    aktline_list.fax = guest.fax
                    aktline_list.bemerk = akt_line.bemerk
                    aktline_list.username = bediener.username
                    aktline_list.gastnr = akt_line.gastnr
                    aktline_list.guest_type = guest.karteityp

                    akt_kont = get_cache (Akt_kont, {"gastnr": [(eq, guest.gastnr)],"kontakt_nr": [(eq, akt_line.kontakt_nr)]})

                    if akt_kont:
                        aktline_list.email = akt_kont.email
                    aktline_list.priority = prioritaet[aktline_list.prioritaet - 1]

            else:

                akt_line_obj_list = {}
                akt_line = Akt_line()
                akt_code = Akt_code()
                guest = Guest()
                bediener = Bediener()
                for akt_line.datum, akt_line.zeit, akt_line.dauer, akt_line.prioritaet, akt_line.kontakt, akt_line.regard, akt_line.userinit, akt_line.linenr, akt_line.bemerk, akt_line.gastnr, akt_line.kontakt_nr, akt_line._recid, akt_code.bezeich, akt_code._recid, guest.name, guest.anredefirma, guest.adresse1, guest.adresse2, guest.adresse3, guest.telefon, guest.fax, guest.karteityp, guest.gastnr, guest._recid, bediener.username, bediener._recid in db_session.query(Akt_line.datum, Akt_line.zeit, Akt_line.dauer, Akt_line.prioritaet, Akt_line.kontakt, Akt_line.regard, Akt_line.userinit, Akt_line.linenr, Akt_line.bemerk, Akt_line.gastnr, Akt_line.kontakt_nr, Akt_line._recid, Akt_code.bezeich, Akt_code._recid, Guest.name, Guest.anredefirma, Guest.adresse1, Guest.adresse2, Guest.adresse3, Guest.telefon, Guest.fax, Guest.karteityp, Guest.gastnr, Guest._recid, Bediener.username, Bediener._recid).join(Akt_code,(Akt_code.aktionscode == Akt_line.aktionscode) & (Akt_code.bezeich == (act_combo).lower())).join(Guest,(Guest.gastnr == Akt_line.gastnr)).join(Bediener,(Bediener.userinit == Akt_line.userinit)).filter(
                             (Akt_line.flag == acttype) & (Akt_line.userinit == (user_init).lower()) & (Akt_line.datum >= next_date) & (Akt_line.datum <= to_date) & (Akt_line.gastnr == inp_gastnr)).order_by(Akt_line.datum, Akt_line.zeit, Akt_line.prioritaet.desc()).all():
                    if akt_line_obj_list.get(akt_line._recid):
                        continue
                    else:
                        akt_line_obj_list[akt_line._recid] = True


                    aktline_list = Aktline_list()
                    aktline_list_data.append(aktline_list)

                    aktline_list.bezeich = akt_code.bezeich
                    aktline_list.datum = akt_line.datum
                    aktline_list.zeit = akt_line.zeit
                    aktline_list.dauer = akt_line.dauer
                    aktline_list.ftime = to_string(akt_line.zeit, "HH:MM")
                    aktline_list.ttime = to_string(akt_line.dauer, "HH:MM")
                    aktline_list.prioritaet = akt_line.prioritaet
                    aktline_list.kontakt = akt_line.kontakt
                    aktline_list.name = guest.name + ", " + guest.anredefirma
                    aktline_list.regard = akt_line.regard
                    aktline_list.userinit = akt_line.userinit
                    aktline_list.linenr = akt_line.linenr
                    aktline_list.address = guest.adresse1 + " " + guest.adresse2 + " " + guest.adresse3
                    aktline_list.telefon = guest.telefon
                    aktline_list.fax = guest.fax
                    aktline_list.bemerk = akt_line.bemerk
                    aktline_list.username = bediener.username
                    aktline_list.gastnr = akt_line.gastnr
                    aktline_list.guest_type = guest.karteityp

                    akt_kont = get_cache (Akt_kont, {"gastnr": [(eq, guest.gastnr)],"kontakt_nr": [(eq, akt_line.kontakt_nr)]})

                    if akt_kont:
                        aktline_list.email = akt_kont.email
                    aktline_list.priority = prioritaet[aktline_list.prioritaet - 1]


    prioritaet[0] = "Low"
    prioritaet[1] = "Medium"
    prioritaet[2] = "High"

    if inp_gastnr != 0:

        if next_date == None:
            disp_all2()
        else:
            disp_it2()
    else:

        if next_date == None:
            disp_all()
        else:
            disp_it()

    return generate_output()