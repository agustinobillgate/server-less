#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Htparam, H_artikel, Artikel

def ts_disc1_get_articlebl(dept:int, disc_value:Decimal, procent:Decimal, b_billart:int, b2_billart:int):

    prepare_cache ([Htparam, H_artikel, Artikel])

    billart = 0
    description = ""
    b_artnrfront = 0
    o_artnrfront = 0
    disc_list_data = []
    b2_artnrfront:int = 0
    b2_vcode:int = 0
    b_vcode:int = 0
    disc_descript:string = ""
    o_billart:int = 0
    htparam = h_artikel = artikel = None

    disc_list = None

    disc_list_data, Disc_list = create_model("Disc_list", {"h_artnr":int, "bezeich":string, "artnr":int, "mwst":int, "service":int, "umsatzart":int, "defaultflag":bool, "amount":Decimal, "netto_amt":Decimal, "service_amt":Decimal, "mwst_amt":Decimal})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal billart, description, b_artnrfront, o_artnrfront, disc_list_data, b2_artnrfront, b2_vcode, b_vcode, disc_descript, o_billart, htparam, h_artikel, artikel
        nonlocal dept, disc_value, procent, b_billart, b2_billart


        nonlocal disc_list
        nonlocal disc_list_data

        return {"billart": billart, "description": description, "b_artnrfront": b_artnrfront, "o_artnrfront": o_artnrfront, "disc-list": disc_list_data}

    def get_article():

        nonlocal billart, description, b_artnrfront, o_artnrfront, disc_list_data, b2_artnrfront, b2_vcode, b_vcode, disc_descript, o_billart, htparam, h_artikel, artikel
        nonlocal dept, disc_value, procent, b_billart, b2_billart


        nonlocal disc_list
        nonlocal disc_list_data

        voucher_art:int = 0

        if disc_value != 0:

            htparam = get_cache (Htparam, {"paramnr": [(eq, 1001)]})
            voucher_art = htparam.finteger

            h_artikel = get_cache (H_artikel, {"artnr": [(eq, htparam.finteger)],"departement": [(eq, dept)]})

            if h_artikel:
                billart = h_artikel.artnr
                description = h_artikel.bezeich + " " + to_string(disc_value)
                disc_descript = description

        if voucher_art != 0:

            return

        htparam = get_cache (Htparam, {"paramnr": [(eq, 557)]})

        if htparam.finteger != 0:

            h_artikel = get_cache (H_artikel, {"artnr": [(eq, htparam.finteger)],"departement": [(eq, dept)]})

            if h_artikel:
                billart = h_artikel.artnr

                if disc_value == 0:

                    if (procent != to_int(procent)):
                        description = h_artikel.bezeich + " " + trim(to_string(procent, "->>9.99")) + "%"
                    else:
                        description = h_artikel.bezeich + " " + trim(to_string(procent, "->>9")) + "%"
                else:
                    description = h_artikel.bezeich

        htparam = get_cache (Htparam, {"paramnr": [(eq, 596)]})

        if htparam.finteger != 0:

            h_artikel = get_cache (H_artikel, {"artnr": [(eq, htparam.finteger)],"departement": [(eq, dept)]})

            if h_artikel:
                b_billart = h_artikel.artnr
                b_artnrfront = h_artikel.artnrfront
                b_vcode = h_artikel.mwst_code

        htparam = get_cache (Htparam, {"paramnr": [(eq, 1009)]})

        if htparam.finteger != 0:

            h_artikel = get_cache (H_artikel, {"artnr": [(eq, htparam.finteger)],"departement": [(eq, dept)]})

            if h_artikel:
                b2_billart = h_artikel.artnr
                b2_artnrfront = h_artikel.artnrfront
                b2_vcode = h_artikel.mwst_code

        htparam = get_cache (Htparam, {"paramnr": [(eq, 556)]})

        if htparam.finteger != 0:

            h_artikel = get_cache (H_artikel, {"artnr": [(eq, htparam.finteger)],"departement": [(eq, dept)]})

            if h_artikel:
                o_billart = h_artikel.artnr
                o_artnrfront = h_artikel.artnrfront


    def create_disclist():

        nonlocal billart, description, b_artnrfront, o_artnrfront, disc_list_data, b2_artnrfront, b2_vcode, b_vcode, disc_descript, o_billart, htparam, h_artikel, artikel
        nonlocal dept, disc_value, procent, b_billart, b2_billart


        nonlocal disc_list
        nonlocal disc_list_data

        zwkum:int = 0

        h_artikel = get_cache (H_artikel, {"artnr": [(eq, billart)],"departement": [(eq, dept)]})

        if not h_artikel:

            return

        artikel = get_cache (Artikel, {"artnr": [(eq, h_artikel.artnrfront)],"departement": [(eq, dept)]})
        zwkum = artikel.zwkum
        disc_list = Disc_list()
        disc_list_data.append(disc_list)

        disc_list.h_artnr = billart
        disc_list.bezeich = h_artikel.bezeich
        disc_list.artnr = h_artikel.artnrfront
        disc_list.mwst = h_artikel.mwst_code
        disc_list.service = h_artikel.service_code
        disc_list.umsatzart = artikel.umsatzart
        disc_list.defaultflag = True

        if disc_value != 0:
            disc_list.bezeich = disc_list.bezeich + " " + to_string(disc_value)
        else:

            if (procent != to_int(procent)):
                disc_list.bezeich = disc_list.bezeich + " " + trim(to_string(procent, "->>9.99")) + "%"
            else:
                disc_list.bezeich = disc_list.bezeich + " " + trim(to_string(procent, "->>9")) + "%"

        if b_billart != 0:

            h_artikel = get_cache (H_artikel, {"artnr": [(eq, b_billart)],"departement": [(eq, dept)]})

            artikel = get_cache (Artikel, {"artnr": [(eq, h_artikel.artnrfront)],"departement": [(eq, dept)]})
            disc_list = Disc_list()
            disc_list_data.append(disc_list)

            disc_list.h_artnr = h_artikel.artnr
            disc_list.bezeich = h_artikel.bezeich
            disc_list.artnr = h_artikel.artnrfront
            disc_list.mwst = h_artikel.mwst_code
            disc_list.service = h_artikel.service_code
            disc_list.umsatzart = artikel.umsatzart
            disc_list.defaultflag = True

            if disc_value != 0:
                disc_list.bezeich = disc_list.bezeich + " " + to_string(disc_value)
            else:

                if (procent != to_int(procent)):
                    disc_list.bezeich = disc_list.bezeich + " " + trim(to_string(procent, "->>9.99")) + "%"
                else:
                    disc_list.bezeich = disc_list.bezeich + " " + trim(to_string(procent, "->>9")) + "%"

        if b2_billart != 0:

            h_artikel = get_cache (H_artikel, {"artnr": [(eq, b2_billart)],"departement": [(eq, dept)]})

            artikel = get_cache (Artikel, {"artnr": [(eq, h_artikel.artnrfront)],"departement": [(eq, dept)]})
            disc_list = Disc_list()
            disc_list_data.append(disc_list)

            disc_list.h_artnr = h_artikel.artnr
            disc_list.bezeich = h_artikel.bezeich
            disc_list.artnr = h_artikel.artnrfront
            disc_list.mwst = h_artikel.mwst_code
            disc_list.service = h_artikel.service_code
            disc_list.umsatzart = artikel.umsatzart
            disc_list.defaultflag = True

            if disc_value != 0:
                disc_list.bezeich = disc_list.bezeich + " " + to_string(disc_value)
            else:

                if (procent != to_int(procent)):
                    disc_list.bezeich = disc_list.bezeich + " " + trim(to_string(procent, "->>9.99")) + "%"
                else:
                    disc_list.bezeich = disc_list.bezeich + " " + trim(to_string(procent, "->>9")) + "%"

        if o_billart != 0:

            h_artikel = get_cache (H_artikel, {"artnr": [(eq, o_billart)],"departement": [(eq, dept)]})

            artikel = get_cache (Artikel, {"artnr": [(eq, h_artikel.artnrfront)],"departement": [(eq, dept)]})
            disc_list = Disc_list()
            disc_list_data.append(disc_list)

            disc_list.h_artnr = h_artikel.artnr
            disc_list.bezeich = h_artikel.bezeich
            disc_list.artnr = h_artikel.artnrfront
            disc_list.mwst = h_artikel.mwst_code
            disc_list.service = h_artikel.service_code
            disc_list.umsatzart = artikel.umsatzart
            disc_list.defaultflag = True

            if disc_value != 0:
                disc_list.bezeich = disc_list.bezeich + " " + to_string(disc_value)
            else:

                if (procent != to_int(procent)):
                    disc_list.bezeich = disc_list.bezeich + " " + trim(to_string(procent, "->>9.99")) + "%"
                else:
                    disc_list.bezeich = disc_list.bezeich + " " + trim(to_string(procent, "->>9")) + "%"

        for artikel in db_session.query(Artikel).filter(
                 (Artikel.departement == dept) & (Artikel.zwkum == zwkum)).order_by(Artikel._recid).all():

            disc_list = query(disc_list_data, filters=(lambda disc_list: disc_list.artnr == artikel.artnr), first=True)

            if not disc_list:

                h_artikel = get_cache (H_artikel, {"artnrfront": [(eq, artikel.artnr)],"departement": [(eq, dept)]})

                if h_artikel:
                    disc_list = Disc_list()
                    disc_list_data.append(disc_list)

                    disc_list.h_artnr = h_artikel.artnr
                    disc_list.bezeich = h_artikel.bezeich
                    disc_list.artnr = h_artikel.artnrfront
                    disc_list.mwst = h_artikel.mwst_code
                    disc_list.service = h_artikel.service_code
                    disc_list.umsatzart = artikel.umsatzart
                    disc_list.defaultflag = False

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