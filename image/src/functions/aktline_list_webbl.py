from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Akt_code, Guest, Bediener, Akt_line, Akt_kont

def aktline_list_webbl(inp_gastnr:int, next_date:date, all_flag:bool, prior:int, act_combo:str, acttype:int, user_init:str, to_date:date):
    aktline_list_list = []
    prioritaet:[str] = ["", "", "", ""]
    akt_code = guest = bediener = akt_line = akt_kont = None

    aktline_list = None

    aktline_list_list, Aktline_list = create_model("Aktline_list", {"bezeich":str, "datum":date, "zeit":int, "dauer":int, "prioritaet":int, "kontakt":str, "name":str, "address":str, "regard":str, "userinit":str, "linenr":int, "telefon":str, "fax":str, "bemerk":str, "email":str, "username":str, "ftime":str, "ttime":str, "priority":str, "gastnr":int, "guest_type":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal aktline_list_list, prioritaet, akt_code, guest, bediener, akt_line, akt_kont


        nonlocal aktline_list
        nonlocal aktline_list_list
        return {"aktline-list": aktline_list_list}

    def disp_all():

        nonlocal aktline_list_list, prioritaet, akt_code, guest, bediener, akt_line, akt_kont


        nonlocal aktline_list
        nonlocal aktline_list_list

        if all_flag:

            if prior == 0:

                if act_combo.lower()  == "ALL":

                    akt_line_obj_list = []
                    for akt_line, akt_code, guest, bediener in db_session.query(Akt_line, Akt_code, Guest, Bediener).join(Akt_code,(Akt_code.aktionscode == Akt_line.aktionscode)).join(Guest,(Guest.gastnr == Akt_line.gastnr)).join(Bediener,(Bediener.userinit == Akt_line.userinit)).filter(
                            (Akt_line.flag == acttype)).all():
                        if akt_line._recid in akt_line_obj_list:
                            continue
                        else:
                            akt_line_obj_list.append(akt_line._recid)


                        aktline_list = Aktline_list()
                        aktline_list_list.append(aktline_list)

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

                        akt_kont = db_session.query(Akt_kont).filter(
                                (Akt_kont.gastnr == guest.gastnr) &  (Akt_kont.kontakt_nr == akt_line.kontakt_nr)).first()

                        if akt_kont:
                            aktline_list.email = akt_kont.email
                        aktline_list.priority = prioritaet[aktline_list.prioritaet - 1]

                else:

                    akt_line_obj_list = []
                    for akt_line, akt_code, guest, bediener in db_session.query(Akt_line, Akt_code, Guest, Bediener).join(Akt_code,(Akt_code.aktionscode == Akt_line.aktionscode) &  (func.lower(Akt_code.bezeich) == (act_combo).lower())).join(Guest,(Guest.gastnr == Akt_line.gastnr)).join(Bediener,(Bediener.userinit == Akt_line.userinit)).filter(
                            (Akt_line.flag == acttype)).all():
                        if akt_line._recid in akt_line_obj_list:
                            continue
                        else:
                            akt_line_obj_list.append(akt_line._recid)


                        aktline_list = Aktline_list()
                        aktline_list_list.append(aktline_list)

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

                        akt_kont = db_session.query(Akt_kont).filter(
                                (Akt_kont.gastnr == guest.gastnr) &  (Akt_kont.kontakt_nr == akt_line.kontakt_nr)).first()

                        if akt_kont:
                            aktline_list.email = akt_kont.email
                        aktline_list.priority = prioritaet[aktline_list.prioritaet - 1]

            else:

                if act_combo.lower()  == "ALL":

                    akt_line_obj_list = []
                    for akt_line, akt_code, guest, bediener in db_session.query(Akt_line, Akt_code, Guest, Bediener).join(Akt_code,(Akt_code.aktionscode == Akt_line.aktionscode)).join(Guest,(Guest.gastnr == Akt_line.gastnr)).join(Bediener,(Bediener.userinit == Akt_line.userinit)).filter(
                            (Akt_line.flag == acttype) &  (Akt_line.prioritaet == prior)).all():
                        if akt_line._recid in akt_line_obj_list:
                            continue
                        else:
                            akt_line_obj_list.append(akt_line._recid)


                        aktline_list = Aktline_list()
                        aktline_list_list.append(aktline_list)

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

                        akt_kont = db_session.query(Akt_kont).filter(
                                (Akt_kont.gastnr == guest.gastnr) &  (Akt_kont.kontakt_nr == akt_line.kontakt_nr)).first()

                        if akt_kont:
                            aktline_list.email = akt_kont.email
                        aktline_list.priority = prioritaet[aktline_list.prioritaet - 1]

                else:

                    akt_line_obj_list = []
                    for akt_line, akt_code, guest, bediener in db_session.query(Akt_line, Akt_code, Guest, Bediener).join(Akt_code,(Akt_code.aktionscode == Akt_line.aktionscode) &  (func.lower(Akt_code.bezeich) == (act_combo).lower())).join(Guest,(Guest.gastnr == Akt_line.gastnr)).join(Bediener,(Bediener.userinit == Akt_line.userinit)).filter(
                            (Akt_line.flag == acttype) &  (Akt_line.prioritaet == prior)).all():
                        if akt_line._recid in akt_line_obj_list:
                            continue
                        else:
                            akt_line_obj_list.append(akt_line._recid)


                        aktline_list = Aktline_list()
                        aktline_list_list.append(aktline_list)

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

                        akt_kont = db_session.query(Akt_kont).filter(
                                (Akt_kont.gastnr == guest.gastnr) &  (Akt_kont.kontakt_nr == akt_line.kontakt_nr)).first()

                        if akt_kont:
                            aktline_list.email = akt_kont.email
                        aktline_list.priority = prioritaet[aktline_list.prioritaet - 1]

        else:

            if prior == 0:

                if act_combo.lower()  == "ALL":

                    akt_line_obj_list = []
                    for akt_line, akt_code, guest, bediener in db_session.query(Akt_line, Akt_code, Guest, Bediener).join(Akt_code,(Akt_code.aktionscode == Akt_line.aktionscode)).join(Guest,(Guest.gastnr == Akt_line.gastnr)).join(Bediener,(Bediener.userinit == Akt_line.userinit)).filter(
                            (Akt_line.flag == acttype) &  (func.lower(Akt_line.userinit) == (user_init).lower())).all():
                        if akt_line._recid in akt_line_obj_list:
                            continue
                        else:
                            akt_line_obj_list.append(akt_line._recid)


                        aktline_list = Aktline_list()
                        aktline_list_list.append(aktline_list)

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

                        akt_kont = db_session.query(Akt_kont).filter(
                                (Akt_kont.gastnr == guest.gastnr) &  (Akt_kont.kontakt_nr == akt_line.kontakt_nr)).first()

                        if akt_kont:
                            aktline_list.email = akt_kont.email
                        aktline_list.priority = prioritaet[aktline_list.prioritaet - 1]

                else:

                    akt_line_obj_list = []
                    for akt_line, akt_code, guest, bediener in db_session.query(Akt_line, Akt_code, Guest, Bediener).join(Akt_code,(Akt_code.aktionscode == Akt_line.aktionscode) &  (func.lower(Akt_code.bezeich) == (act_combo).lower())).join(Guest,(Guest.gastnr == Akt_line.gastnr)).join(Bediener,(Bediener.userinit == Akt_line.userinit)).filter(
                            (Akt_line.flag == acttype) &  (func.lower(Akt_line.userinit) == (user_init).lower())).all():
                        if akt_line._recid in akt_line_obj_list:
                            continue
                        else:
                            akt_line_obj_list.append(akt_line._recid)


                        aktline_list = Aktline_list()
                        aktline_list_list.append(aktline_list)

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

                        akt_kont = db_session.query(Akt_kont).filter(
                                (Akt_kont.gastnr == guest.gastnr) &  (Akt_kont.kontakt_nr == akt_line.kontakt_nr)).first()

                        if akt_kont:
                            aktline_list.email = akt_kont.email
                        aktline_list.priority = prioritaet[aktline_list.prioritaet - 1]

            else:

                if act_combo.lower()  == "ALL":

                    akt_line_obj_list = []
                    for akt_line, akt_code, guest, bediener in db_session.query(Akt_line, Akt_code, Guest, Bediener).join(Akt_code,(Akt_code.aktionscode == Akt_line.aktionscode)).join(Guest,(Guest.gastnr == Akt_line.gastnr)).join(Bediener,(Bediener.userinit == Akt_line.userinit)).filter(
                            (Akt_line.flag == acttype) &  (func.lower(Akt_line.userinit) == (user_init).lower()) &  (Akt_line.prioritaet == prior)).all():
                        if akt_line._recid in akt_line_obj_list:
                            continue
                        else:
                            akt_line_obj_list.append(akt_line._recid)


                        aktline_list = Aktline_list()
                        aktline_list_list.append(aktline_list)

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

                        akt_kont = db_session.query(Akt_kont).filter(
                                (Akt_kont.gastnr == guest.gastnr) &  (Akt_kont.kontakt_nr == akt_line.kontakt_nr)).first()

                        if akt_kont:
                            aktline_list.email = akt_kont.email
                        aktline_list.priority = prioritaet[aktline_list.prioritaet - 1]

                else:

                    akt_line_obj_list = []
                    for akt_line, akt_code, guest, bediener in db_session.query(Akt_line, Akt_code, Guest, Bediener).join(Akt_code,(Akt_code.aktionscode == Akt_line.aktionscode) &  (func.lower(Akt_code.bezeich) == (act_combo).lower())).join(Guest,(Guest.gastnr == Akt_line.gastnr)).join(Bediener,(Bediener.userinit == Akt_line.userinit)).filter(
                            (Akt_line.flag == acttype) &  (func.lower(Akt_line.userinit) == (user_init).lower()) &  (Akt_line.prioritaet == prior)).all():
                        if akt_line._recid in akt_line_obj_list:
                            continue
                        else:
                            akt_line_obj_list.append(akt_line._recid)


                        aktline_list = Aktline_list()
                        aktline_list_list.append(aktline_list)

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

                        akt_kont = db_session.query(Akt_kont).filter(
                                (Akt_kont.gastnr == guest.gastnr) &  (Akt_kont.kontakt_nr == akt_line.kontakt_nr)).first()

                        if akt_kont:
                            aktline_list.email = akt_kont.email
                        aktline_list.priority = prioritaet[aktline_list.prioritaet - 1]


    def disp_all2():

        nonlocal aktline_list_list, prioritaet, akt_code, guest, bediener, akt_line, akt_kont


        nonlocal aktline_list
        nonlocal aktline_list_list

        if all_flag:

            if act_combo.lower()  == "ALL":

                akt_line_obj_list = []
                for akt_line, akt_code, guest, bediener in db_session.query(Akt_line, Akt_code, Guest, Bediener).join(Akt_code,(Akt_code.aktionscode == Akt_line.aktionscode)).join(Guest,(Guest.gastnr == Akt_line.gastnr)).join(Bediener,(Bediener.userinit == Akt_line.userinit)).filter(
                            (Akt_line.flag == acttype) &  (Akt_line.gastnr == inp_gastnr)).all():
                    if akt_line._recid in akt_line_obj_list:
                        continue
                    else:
                        akt_line_obj_list.append(akt_line._recid)


                    aktline_list = Aktline_list()
                    aktline_list_list.append(aktline_list)

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

                    akt_kont = db_session.query(Akt_kont).filter(
                                (Akt_kont.gastnr == guest.gastnr) &  (Akt_kont.kontakt_nr == akt_line.kontakt_nr)).first()

                    if akt_kont:
                        aktline_list.email = akt_kont.email
                    aktline_list.priority = prioritaet[aktline_list.prioritaet - 1]

            else:

                akt_line_obj_list = []
                for akt_line, akt_code, guest, bediener in db_session.query(Akt_line, Akt_code, Guest, Bediener).join(Akt_code,(Akt_code.aktionscode == Akt_line.aktionscode) &  (func.lower(Akt_code.bezeich) == (act_combo).lower())).join(Guest,(Guest.gastnr == Akt_line.gastnr)).join(Bediener,(Bediener.userinit == Akt_line.userinit)).filter(
                            (Akt_line.flag == acttype) &  (Akt_line.gastnr == inp_gastnr)).all():
                    if akt_line._recid in akt_line_obj_list:
                        continue
                    else:
                        akt_line_obj_list.append(akt_line._recid)


                    aktline_list = Aktline_list()
                    aktline_list_list.append(aktline_list)

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

                    akt_kont = db_session.query(Akt_kont).filter(
                                (Akt_kont.gastnr == guest.gastnr) &  (Akt_kont.kontakt_nr == akt_line.kontakt_nr)).first()

                    if akt_kont:
                        aktline_list.email = akt_kont.email
                    aktline_list.priority = prioritaet[aktline_list.prioritaet - 1]

        else:

            if act_combo.lower()  == "ALL":

                akt_line_obj_list = []
                for akt_line, akt_code, guest, bediener in db_session.query(Akt_line, Akt_code, Guest, Bediener).join(Akt_code,(Akt_code.aktionscode == Akt_line.aktionscode)).join(Guest,(Guest.gastnr == Akt_line.gastnr)).join(Bediener,(Bediener.userinit == Akt_line.userinit)).filter(
                            (Akt_line.flag == acttype) &  (func.lower(Akt_line.userinit) == (user_init).lower()) &  (Akt_line.gastnr == inp_gastnr)).all():
                    if akt_line._recid in akt_line_obj_list:
                        continue
                    else:
                        akt_line_obj_list.append(akt_line._recid)


                    aktline_list = Aktline_list()
                    aktline_list_list.append(aktline_list)

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

                    akt_kont = db_session.query(Akt_kont).filter(
                                (Akt_kont.gastnr == guest.gastnr) &  (Akt_kont.kontakt_nr == akt_line.kontakt_nr)).first()

                    if akt_kont:
                        aktline_list.email = akt_kont.email
                    aktline_list.priority = prioritaet[aktline_list.prioritaet - 1]

            else:

                akt_line_obj_list = []
                for akt_line, akt_code, guest, bediener in db_session.query(Akt_line, Akt_code, Guest, Bediener).join(Akt_code,(Akt_code.aktionscode == Akt_line.aktionscode) &  (func.lower(Akt_code.bezeich) == (act_combo).lower())).join(Guest,(Guest.gastnr == Akt_line.gastnr)).join(Bediener,(Bediener.userinit == Akt_line.userinit)).filter(
                            (Akt_line.flag == acttype) &  (func.lower(Akt_line.userinit) == (user_init).lower()) &  (Akt_line.gastnr == inp_gastnr)).all():
                    if akt_line._recid in akt_line_obj_list:
                        continue
                    else:
                        akt_line_obj_list.append(akt_line._recid)


                    aktline_list = Aktline_list()
                    aktline_list_list.append(aktline_list)

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

                    akt_kont = db_session.query(Akt_kont).filter(
                                (Akt_kont.gastnr == guest.gastnr) &  (Akt_kont.kontakt_nr == akt_line.kontakt_nr)).first()

                    if akt_kont:
                        aktline_list.email = akt_kont.email
                    aktline_list.priority = prioritaet[aktline_list.prioritaet - 1]


    def disp_it():

        nonlocal aktline_list_list, prioritaet, akt_code, guest, bediener, akt_line, akt_kont


        nonlocal aktline_list
        nonlocal aktline_list_list

        if all_flag:

            if prior == 0:

                if act_combo.lower()  == "ALL":

                    akt_line_obj_list = []
                    for akt_line, akt_code, guest, bediener in db_session.query(Akt_line, Akt_code, Guest, Bediener).join(Akt_code,(Akt_code.aktionscode == Akt_line.aktionscode)).join(Guest,(Guest.gastnr == Akt_line.gastnr)).join(Bediener,(Bediener.userinit == Akt_line.userinit)).filter(
                                (Akt_line.flag == acttype) &  (Akt_line.datum >= next_date) &  (Akt_line.datum <= to_date)).all():
                        if akt_line._recid in akt_line_obj_list:
                            continue
                        else:
                            akt_line_obj_list.append(akt_line._recid)


                        aktline_list = Aktline_list()
                        aktline_list_list.append(aktline_list)

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

                        akt_kont = db_session.query(Akt_kont).filter(
                                    (Akt_kont.gastnr == guest.gastnr) &  (Akt_kont.kontakt_nr == akt_line.kontakt_nr)).first()

                        if akt_kont:
                            aktline_list.email = akt_kont.email
                        aktline_list.priority = prioritaet[aktline_list.prioritaet - 1]

                else:

                    akt_line_obj_list = []
                    for akt_line, akt_code, guest, bediener in db_session.query(Akt_line, Akt_code, Guest, Bediener).join(Akt_code,(Akt_code.aktionscode == Akt_line.aktionscode) &  (func.lower(Akt_code.bezeich) == (act_combo).lower())).join(Guest,(Guest.gastnr == Akt_line.gastnr)).join(Bediener,(Bediener.userinit == Akt_line.userinit)).filter(
                                (Akt_line.flag == acttype) &  (Akt_line.datum >= next_date) &  (Akt_line.datum <= to_date)).all():
                        if akt_line._recid in akt_line_obj_list:
                            continue
                        else:
                            akt_line_obj_list.append(akt_line._recid)


                        aktline_list = Aktline_list()
                        aktline_list_list.append(aktline_list)

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

                        akt_kont = db_session.query(Akt_kont).filter(
                                    (Akt_kont.gastnr == guest.gastnr) &  (Akt_kont.kontakt_nr == akt_line.kontakt_nr)).first()

                        if akt_kont:
                            aktline_list.email = akt_kont.email
                        aktline_list.priority = prioritaet[aktline_list.prioritaet - 1]

            else:

                if act_combo.lower()  == "ALL":

                    akt_line_obj_list = []
                    for akt_line, akt_code, guest, bediener in db_session.query(Akt_line, Akt_code, Guest, Bediener).join(Akt_code,(Akt_code.aktionscode == Akt_line.aktionscode)).join(Guest,(Guest.gastnr == Akt_line.gastnr)).join(Bediener,(Bediener.userinit == Akt_line.userinit)).filter(
                                (Akt_line.flag == acttype) &  (Akt_line.datum >= next_date) &  (Akt_line.datum <= to_date) &  (Akt_line.prioritaet == prior)).all():
                        if akt_line._recid in akt_line_obj_list:
                            continue
                        else:
                            akt_line_obj_list.append(akt_line._recid)


                        aktline_list = Aktline_list()
                        aktline_list_list.append(aktline_list)

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

                        akt_kont = db_session.query(Akt_kont).filter(
                                    (Akt_kont.gastnr == guest.gastnr) &  (Akt_kont.kontakt_nr == akt_line.kontakt_nr)).first()

                        if akt_kont:
                            aktline_list.email = akt_kont.email
                        aktline_list.priority = prioritaet[aktline_list.prioritaet - 1]

                else:

                    akt_line_obj_list = []
                    for akt_line, akt_code, guest, bediener in db_session.query(Akt_line, Akt_code, Guest, Bediener).join(Akt_code,(Akt_code.aktionscode == Akt_line.aktionscode) &  (func.lower(Akt_code.bezeich) == (act_combo).lower())).join(Guest,(Guest.gastnr == Akt_line.gastnr)).join(Bediener,(Bediener.userinit == Akt_line.userinit)).filter(
                                (Akt_line.flag == acttype) &  (Akt_line.datum >= next_date) &  (Akt_line.datum <= to_date) &  (Akt_line.prioritaet == prior)).all():
                        if akt_line._recid in akt_line_obj_list:
                            continue
                        else:
                            akt_line_obj_list.append(akt_line._recid)


                        aktline_list = Aktline_list()
                        aktline_list_list.append(aktline_list)

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

                        akt_kont = db_session.query(Akt_kont).filter(
                                    (Akt_kont.gastnr == guest.gastnr) &  (Akt_kont.kontakt_nr == akt_line.kontakt_nr)).first()

                        if akt_kont:
                            aktline_list.email = akt_kont.email
                        aktline_list.priority = prioritaet[aktline_list.prioritaet - 1]

        else:

            if prior == 0:

                if act_combo.lower()  == "ALL":

                    akt_line_obj_list = []
                    for akt_line, akt_code, guest, bediener in db_session.query(Akt_line, Akt_code, Guest, Bediener).join(Akt_code,(Akt_code.aktionscode == Akt_line.aktionscode)).join(Guest,(Guest.gastnr == Akt_line.gastnr)).join(Bediener,(Bediener.userinit == Akt_line.userinit)).filter(
                                (Akt_line.flag == acttype) &  (func.lower(Akt_line.userinit) == (user_init).lower()) &  (Akt_line.datum >= next_date) &  (Akt_line.datum <= to_date)).all():
                        if akt_line._recid in akt_line_obj_list:
                            continue
                        else:
                            akt_line_obj_list.append(akt_line._recid)


                        aktline_list = Aktline_list()
                        aktline_list_list.append(aktline_list)

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

                        akt_kont = db_session.query(Akt_kont).filter(
                                    (Akt_kont.gastnr == guest.gastnr) &  (Akt_kont.kontakt_nr == akt_line.kontakt_nr)).first()

                        if akt_kont:
                            aktline_list.email = akt_kont.email
                        aktline_list.priority = prioritaet[aktline_list.prioritaet - 1]

                else:

                    akt_line_obj_list = []
                    for akt_line, akt_code, guest, bediener in db_session.query(Akt_line, Akt_code, Guest, Bediener).join(Akt_code,(Akt_code.aktionscode == Akt_line.aktionscode) &  (func.lower(Akt_code.bezeich) == (act_combo).lower())).join(Guest,(Guest.gastnr == Akt_line.gastnr)).join(Bediener,(Bediener.userinit == Akt_line.userinit)).filter(
                                (Akt_line.flag == acttype) &  (func.lower(Akt_line.userinit) == (user_init).lower()) &  (Akt_line.datum >= next_date) &  (Akt_line.datum <= to_date)).all():
                        if akt_line._recid in akt_line_obj_list:
                            continue
                        else:
                            akt_line_obj_list.append(akt_line._recid)


                        aktline_list = Aktline_list()
                        aktline_list_list.append(aktline_list)

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

                        akt_kont = db_session.query(Akt_kont).filter(
                                    (Akt_kont.gastnr == guest.gastnr) &  (Akt_kont.kontakt_nr == akt_line.kontakt_nr)).first()

                        if akt_kont:
                            aktline_list.email = akt_kont.email
                        aktline_list.priority = prioritaet[aktline_list.prioritaet - 1]

            else:

                if act_combo.lower()  == "ALL":

                    akt_line_obj_list = []
                    for akt_line, akt_code, guest, bediener in db_session.query(Akt_line, Akt_code, Guest, Bediener).join(Akt_code,(Akt_code.aktionscode == Akt_line.aktionscode)).join(Guest,(Guest.gastnr == Akt_line.gastnr)).join(Bediener,(Bediener.userinit == Akt_line.userinit)).filter(
                                (Akt_line.flag == acttype) &  (func.lower(Akt_line.userinit) == (user_init).lower()) &  (Akt_line.datum >= next_date) &  (Akt_line.datum <= to_date) &  (Akt_line.prioritaet == prior)).all():
                        if akt_line._recid in akt_line_obj_list:
                            continue
                        else:
                            akt_line_obj_list.append(akt_line._recid)


                        aktline_list = Aktline_list()
                        aktline_list_list.append(aktline_list)

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

                        akt_kont = db_session.query(Akt_kont).filter(
                                    (Akt_kont.gastnr == guest.gastnr) &  (Akt_kont.kontakt_nr == akt_line.kontakt_nr)).first()

                        if akt_kont:
                            aktline_list.email = akt_kont.email
                        aktline_list.priority = prioritaet[aktline_list.prioritaet - 1]

                else:

                    akt_line_obj_list = []
                    for akt_line, akt_code, guest, bediener in db_session.query(Akt_line, Akt_code, Guest, Bediener).join(Akt_code,(Akt_code.aktionscode == Akt_line.aktionscode) &  (func.lower(Akt_code.bezeich) == (act_combo).lower())).join(Guest,(Guest.gastnr == Akt_line.gastnr)).join(Bediener,(Bediener.userinit == Akt_line.userinit)).filter(
                                (Akt_line.flag == acttype) &  (func.lower(Akt_line.userinit) == (user_init).lower()) &  (Akt_line.datum >= next_date) &  (Akt_line.datum <= to_date) &  (Akt_line.prioritaet == prior)).all():
                        if akt_line._recid in akt_line_obj_list:
                            continue
                        else:
                            akt_line_obj_list.append(akt_line._recid)


                        aktline_list = Aktline_list()
                        aktline_list_list.append(aktline_list)

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

                        akt_kont = db_session.query(Akt_kont).filter(
                                    (Akt_kont.gastnr == guest.gastnr) &  (Akt_kont.kontakt_nr == akt_line.kontakt_nr)).first()

                        if akt_kont:
                            aktline_list.email = akt_kont.email
                        aktline_list.priority = prioritaet[aktline_list.prioritaet - 1]


    def disp_it2():

        nonlocal aktline_list_list, prioritaet, akt_code, guest, bediener, akt_line, akt_kont


        nonlocal aktline_list
        nonlocal aktline_list_list

        if all_flag:

            if act_combo.lower()  == "ALL":

                akt_line_obj_list = []
                for akt_line, akt_code, guest, bediener in db_session.query(Akt_line, Akt_code, Guest, Bediener).join(Akt_code,(Akt_code.aktionscode == Akt_line.aktionscode)).join(Guest,(Guest.gastnr == Akt_line.gastnr)).join(Bediener,(Bediener.userinit == Akt_line.userinit)).filter(
                            (Akt_line.flag == acttype) &  (Akt_line.datum >= next_date) &  (Akt_line.datum <= to_date) &  (Akt_line.gastnr == inp_gastnr)).all():
                    if akt_line._recid in akt_line_obj_list:
                        continue
                    else:
                        akt_line_obj_list.append(akt_line._recid)


                    aktline_list = Aktline_list()
                    aktline_list_list.append(aktline_list)

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

                    akt_kont = db_session.query(Akt_kont).filter(
                                (Akt_kont.gastnr == guest.gastnr) &  (Akt_kont.kontakt_nr == akt_line.kontakt_nr)).first()

                    if akt_kont:
                        aktline_list.email = akt_kont.email
                    aktline_list.priority = prioritaet[aktline_list.prioritaet - 1]

            else:

                akt_line_obj_list = []
                for akt_line, akt_code, guest, bediener in db_session.query(Akt_line, Akt_code, Guest, Bediener).join(Akt_code,(Akt_code.aktionscode == Akt_line.aktionscode) &  (func.lower(Akt_code.bezeich) == (act_combo).lower())).join(Guest,(Guest.gastnr == Akt_line.gastnr)).join(Bediener,(Bediener.userinit == Akt_line.userinit)).filter(
                            (Akt_line.flag == acttype) &  (Akt_line.datum >= next_date) &  (Akt_line.datum <= to_date) &  (Akt_line.gastnr == inp_gastnr)).all():
                    if akt_line._recid in akt_line_obj_list:
                        continue
                    else:
                        akt_line_obj_list.append(akt_line._recid)


                    aktline_list = Aktline_list()
                    aktline_list_list.append(aktline_list)

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

                    akt_kont = db_session.query(Akt_kont).filter(
                                (Akt_kont.gastnr == guest.gastnr) &  (Akt_kont.kontakt_nr == akt_line.kontakt_nr)).first()

                    if akt_kont:
                        aktline_list.email = akt_kont.email
                    aktline_list.priority = prioritaet[aktline_list.prioritaet - 1]

        else:

            if act_combo.lower()  == "ALL":

                akt_line_obj_list = []
                for akt_line, akt_code, guest, bediener in db_session.query(Akt_line, Akt_code, Guest, Bediener).join(Akt_code,(Akt_code.aktionscode == Akt_line.aktionscode)).join(Guest,(Guest.gastnr == Akt_line.gastnr)).join(Bediener,(Bediener.userinit == Akt_line.userinit)).filter(
                            (Akt_line.flag == acttype) &  (func.lower(Akt_line.userinit) == (user_init).lower()) &  (Akt_line.datum >= next_date) &  (Akt_line.datum <= to_date) &  (Akt_line.gastnr == inp_gastnr)).all():
                    if akt_line._recid in akt_line_obj_list:
                        continue
                    else:
                        akt_line_obj_list.append(akt_line._recid)


                    aktline_list = Aktline_list()
                    aktline_list_list.append(aktline_list)

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

                    akt_kont = db_session.query(Akt_kont).filter(
                                (Akt_kont.gastnr == guest.gastnr) &  (Akt_kont.kontakt_nr == akt_line.kontakt_nr)).first()

                    if akt_kont:
                        aktline_list.email = akt_kont.email
                    aktline_list.priority = prioritaet[aktline_list.prioritaet - 1]

            else:

                akt_line_obj_list = []
                for akt_line, akt_code, guest, bediener in db_session.query(Akt_line, Akt_code, Guest, Bediener).join(Akt_code,(Akt_code.aktionscode == Akt_line.aktionscode) &  (func.lower(Akt_code.bezeich) == (act_combo).lower())).join(Guest,(Guest.gastnr == Akt_line.gastnr)).join(Bediener,(Bediener.userinit == Akt_line.userinit)).filter(
                            (Akt_line.flag == acttype) &  (func.lower(Akt_line.userinit) == (user_init).lower()) &  (Akt_line.datum >= next_date) &  (Akt_line.datum <= to_date) &  (Akt_line.gastnr == inp_gastnr)).all():
                    if akt_line._recid in akt_line_obj_list:
                        continue
                    else:
                        akt_line_obj_list.append(akt_line._recid)


                    aktline_list = Aktline_list()
                    aktline_list_list.append(aktline_list)

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

                    akt_kont = db_session.query(Akt_kont).filter(
                                (Akt_kont.gastnr == guest.gastnr) &  (Akt_kont.kontakt_nr == akt_line.kontakt_nr)).first()

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