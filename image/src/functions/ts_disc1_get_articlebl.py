from functions.additional_functions import *
import decimal
from models import Htparam, H_artikel, Artikel

def ts_disc1_get_articlebl(dept:int, disc_value:decimal, procent:decimal, b_billart:int, b2_billart:int):
    billart = 0
    description = ""
    b_artnrfront = 0
    o_artnrfront = 0
    disc_list_list = []
    b2_artnrfront:int = 0
    b2_vcode:int = 0
    b_vcode:int = 0
    disc_descript:str = ""
    o_billart:int = 0
    htparam = h_artikel = artikel = None

    disc_list = None

    disc_list_list, Disc_list = create_model("Disc_list", {"h_artnr":int, "bezeich":str, "artnr":int, "mwst":int, "service":int, "umsatzart":int, "defaultflag":bool, "amount":decimal, "netto_amt":decimal, "service_amt":decimal, "mwst_amt":decimal})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal billart, description, b_artnrfront, o_artnrfront, disc_list_list, b2_artnrfront, b2_vcode, b_vcode, disc_descript, o_billart, htparam, h_artikel, artikel


        nonlocal disc_list
        nonlocal disc_list_list
        return {"billart": billart, "description": description, "b_artnrfront": b_artnrfront, "o_artnrfront": o_artnrfront, "disc-list": disc_list_list}

    def get_article():

        nonlocal billart, description, b_artnrfront, o_artnrfront, disc_list_list, b2_artnrfront, b2_vcode, b_vcode, disc_descript, o_billart, htparam, h_artikel, artikel


        nonlocal disc_list
        nonlocal disc_list_list

        voucher_art:int = 0

        if disc_value != 0:

            htparam = db_session.query(Htparam).filter(
                    (Htparam.paramnr == 1001)).first()
            voucher_art = htparam.finteger

            h_artikel = db_session.query(H_artikel).filter(
                    (H_artikel.artnr == htparam.finteger) &  (H_artikel.departement == dept)).first()

            if h_artikel:
                billart = h_artikel.artnr
                description = h_artikel.bezeich + " " + to_string(disc_value)
                disc_descript = description

        if voucher_art != 0:

            return

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 557)).first()

        if htparam.finteger != 0:

            h_artikel = db_session.query(H_artikel).filter(
                    (H_artikel.artnr == htparam.finteger) &  (H_artikel.departement == dept)).first()

            if h_artikel:
                billart = h_artikel.artnr

                if disc_value == 0:

                    if (procent != to_int(procent)):
                        description = h_artikel.bezeich + " " + trim(to_string(procent, "->>9.99")) + "%"
                    else:
                        description = h_artikel.bezeich + " " + trim(to_string(procent, "->>9")) + "%"
                else:
                    description = h_artikel.bezeich

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 596)).first()

        if htparam.finteger != 0:

            h_artikel = db_session.query(H_artikel).filter(
                    (H_artikel.artnr == htparam.finteger) &  (H_artikel.departement == dept)).first()

            if h_artikel:
                b_billart = h_artikel.artnr
                b_artnrfront = h_artikel.artnrfront
                b_vcode = h_artikel.mwst_code

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 1009)).first()

        if htparam.finteger != 0:

            h_artikel = db_session.query(H_artikel).filter(
                    (H_artikel.artnr == htparam.finteger) &  (H_artikel.departement == dept)).first()

            if h_artikel:
                b2_billart = h_artikel.artnr
                b2_artnrfront = h_artikel.artnrfront
                b2_vcode = h_artikel.mwst_code

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 556)).first()

        if htparam.finteger != 0:

            h_artikel = db_session.query(H_artikel).filter(
                    (H_artikel.artnr == htparam.finteger) &  (H_artikel.departement == dept)).first()

            if h_artikel:
                o_billart = h_artikel.artnr
                o_artnrfront = h_artikel.artnrfront

    def create_disclist():

        nonlocal billart, description, b_artnrfront, o_artnrfront, disc_list_list, b2_artnrfront, b2_vcode, b_vcode, disc_descript, o_billart, htparam, h_artikel, artikel


        nonlocal disc_list
        nonlocal disc_list_list

        zwkum:int = 0

        h_artikel = db_session.query(H_artikel).filter(
                (H_artikel.artnr == billart) &  (H_artikel.departement == dept)).first()

        if not h_artikel:

            return

        artikel = db_session.query(Artikel).filter(
                (Artikel.artnr == h_Artikel.artnrfront) &  (Artikel.departement == dept)).first()
        zwkum = artikel.zwkum
        disc_list = Disc_list()
        disc_list_list.append(disc_list)

        disc_list.h_artnr = billart
        disc_list.bezeich = h_artikel.bezeich
        disc_list.artnr = h_artikel.artnrfront
        disc_list.mwst = h_artikel.mwst
        disc_list.service = h_artikel.service
        disc_list.umsatzart = artikel.umsatzart
        disc_list.defaultFlag = True

        if disc_value != 0:
            disc_list.bezeich = disc_list.bezeich + " " + to_string(disc_value)
        else:

            if (procent != to_int(procent)):
                disc_list.bezeich = disc_list.bezeich + " " + trim(to_string(procent, "->>9.99")) + "%"
            else:
                disc_list.bezeich = disc_list.bezeich + " " + trim(to_string(procent, "->>9")) + "%"

        if b_billart != 0:

            h_artikel = db_session.query(H_artikel).filter(
                    (H_artikel.artnr == b_billart) &  (H_artikel.departement == dept)).first()

            artikel = db_session.query(Artikel).filter(
                    (Artikel.artnr == h_Artikel.artnrfront) &  (Artikel.departement == dept)).first()
            disc_list = Disc_list()
            disc_list_list.append(disc_list)

            disc_list.h_artnr = h_artikel.artnr
            disc_list.bezeich = h_artikel.bezeich
            disc_list.artnr = h_artikel.artnrfront
            disc_list.mwst = h_artikel.mwst
            disc_list.service = h_artikel.service
            disc_list.umsatzart = artikel.umsatzart
            disc_list.defaultFlag = True

            if disc_value != 0:
                disc_list.bezeich = disc_list.bezeich + " " + to_string(disc_value)
            else:

                if (procent != to_int(procent)):
                    disc_list.bezeich = disc_list.bezeich + " " + trim(to_string(procent, "->>9.99")) + "%"
                else:
                    disc_list.bezeich = disc_list.bezeich + " " + trim(to_string(procent, "->>9")) + "%"

        if b2_billart != 0:

            h_artikel = db_session.query(H_artikel).filter(
                    (H_artikel.artnr == b2_billart) &  (H_artikel.departement == dept)).first()

            artikel = db_session.query(Artikel).filter(
                    (Artikel.artnr == h_Artikel.artnrfront) &  (Artikel.departement == dept)).first()
            disc_list = Disc_list()
            disc_list_list.append(disc_list)

            disc_list.h_artnr = h_artikel.artnr
            disc_list.bezeich = h_artikel.bezeich
            disc_list.artnr = h_artikel.artnrfront
            disc_list.mwst = h_artikel.mwst
            disc_list.service = h_artikel.service
            disc_list.umsatzart = artikel.umsatzart
            disc_list.defaultFlag = True

            if disc_value != 0:
                disc_list.bezeich = disc_list.bezeich + " " + to_string(disc_value)
            else:

                if (procent != to_int(procent)):
                    disc_list.bezeich = disc_list.bezeich + " " + trim(to_string(procent, "->>9.99")) + "%"
                else:
                    disc_list.bezeich = disc_list.bezeich + " " + trim(to_string(procent, "->>9")) + "%"

        if o_billart != 0:

            h_artikel = db_session.query(H_artikel).filter(
                    (H_artikel.artnr == o_billart) &  (H_artikel.departement == dept)).first()

            artikel = db_session.query(Artikel).filter(
                    (Artikel.artnr == h_Artikel.artnrfront) &  (Artikel.departement == dept)).first()
            disc_list = Disc_list()
            disc_list_list.append(disc_list)

            disc_list.h_artnr = h_artikel.artnr
            disc_list.bezeich = h_artikel.bezeich
            disc_list.artnr = h_artikel.artnrfront
            disc_list.mwst = h_artikel.mwst
            disc_list.service = h_artikel.service
            disc_list.umsatzart = artikel.umsatzart
            disc_list.defaultFlag = True

            if disc_value != 0:
                disc_list.bezeich = disc_list.bezeich + " " + to_string(disc_value)
            else:

                if (procent != to_int(procent)):
                    disc_list.bezeich = disc_list.bezeich + " " + trim(to_string(procent, "->>9.99")) + "%"
                else:
                    disc_list.bezeich = disc_list.bezeich + " " + trim(to_string(procent, "->>9")) + "%"

        for artikel in db_session.query(Artikel).filter(
                (Artikel.departement == dept) &  (Artikel.zwkum == zwkum)).all():

            disc_list = query(disc_list_list, filters=(lambda disc_list :disc_list.artnr == artikel.artnr), first=True)

            if not disc_list:

                h_artikel = db_session.query(H_artikel).filter(
                        (H_artikel.artnrfront == artikel.artnr) &  (H_artikel.departement == dept)).first()

                if h_artikel:
                    disc_list = Disc_list()
                    disc_list_list.append(disc_list)

                    disc_list.h_artnr = h_artikel.artnr
                    disc_list.bezeich = h_artikel.bezeich
                    disc_list.artnr = h_artikel.artnrfront
                    disc_list.mwst = h_artikel.mwst
                    disc_list.service = h_artikel.service
                    disc_list.umsatzart = artikel.umsatzart
                    disc_list.defaultFlag = False

                    if disc_value != 0:
                        disc_list.bezeich = disc_list.bezeich + " " + to_string(disc_value)
                    else:

                        if (procent != to_int(procent)):
                            disc_list.bezeich = disc_list.bezeich + " " + trim(to_string(procent, "->>9.99")) + "%"
                        else:
                            disc_list.bezeich = disc_list.bezeich + " " + trim(to_string(procent, "->>9")) + "%"


    get_article()
    create_disclist()

    return generate_output()