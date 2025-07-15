#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, Waehrung, Brief, Briefzei

def prepare_fo_parexcelbl(briefnr:int):

    prepare_cache ([Htparam, Waehrung, Brief, Briefzei])

    serv_vat = False
    foreign_nr = 0
    start_date = None
    price_decimal = 0
    no_decimal = False
    outfile_dir = ""
    keycmd = ""
    keyvar = ""
    batch_list_data = []
    htv_list_data = []
    htp_list_data = []
    brief_list_data = []
    htparam = waehrung = brief = briefzei = None

    batch_list = htv_list = htp_list = brief_list = None

    batch_list_data, Batch_list = create_model("Batch_list", {"briefnr":int, "fname":string})
    htv_list_data, Htv_list = create_model("Htv_list", {"paramnr":int, "fchar":string})
    htp_list_data, Htp_list = create_model("Htp_list", {"paramnr":int, "fchar":string})
    brief_list_data, Brief_list = create_model("Brief_list", {"b_text":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal serv_vat, foreign_nr, start_date, price_decimal, no_decimal, outfile_dir, keycmd, keyvar, batch_list_data, htv_list_data, htp_list_data, brief_list_data, htparam, waehrung, brief, briefzei
        nonlocal briefnr


        nonlocal batch_list, htv_list, htp_list, brief_list
        nonlocal batch_list_data, htv_list_data, htp_list_data, brief_list_data

        return {"serv_vat": serv_vat, "foreign_nr": foreign_nr, "start_date": start_date, "price_decimal": price_decimal, "no_decimal": no_decimal, "outfile_dir": outfile_dir, "keycmd": keycmd, "keyvar": keyvar, "batch-list": batch_list_data, "htv-list": htv_list_data, "htp-list": htp_list_data, "brief-list": brief_list_data}

    def fill_list():

        nonlocal serv_vat, foreign_nr, start_date, price_decimal, no_decimal, outfile_dir, keycmd, keyvar, batch_list_data, htv_list_data, htp_list_data, brief_list_data, htparam, waehrung, brief, briefzei
        nonlocal briefnr


        nonlocal batch_list, htv_list, htp_list, brief_list
        nonlocal batch_list_data, htv_list_data, htp_list_data, brief_list_data

        i:int = 0
        j:int = 0
        n:int = 0
        c:string = ""
        l:int = 0
        continued:bool = False

        htparam = get_cache (Htparam, {"paramnr": [(eq, 600)]})
        keycmd = htparam.fchar

        htparam = get_cache (Htparam, {"paramnr": [(eq, 2030)]})
        keyvar = htparam.fchar

        for htparam in db_session.query(Htparam).filter(
                 (Htparam.paramgruppe == 8) & (Htparam.fchar != "")).order_by(length(Htparam.fchar).desc()).all():

            if substring(htparam.fchar, 0 , 1) == (".").lower() :
                htv_list = Htv_list()
                htv_list_data.append(htv_list)

                htv_list.paramnr = htparam.paramnr
                htv_list.fchar = htparam.fchar
            else:
                htp_list = Htp_list()
                htp_list_data.append(htp_list)

                htp_list.paramnr = htparam.paramnr
                htp_list.fchar = keycmd + htparam.fchar
        htv_list = Htv_list()
        htv_list_data.append(htv_list)

        htv_list.paramnr = 9199
        htv_list.fchar = ".yesterday"


        htv_list = Htv_list()
        htv_list_data.append(htv_list)

        htv_list.paramnr = 9198
        htv_list.fchar = ".lm-today"


        htv_list = Htv_list()
        htv_list_data.append(htv_list)

        htv_list.paramnr = 9197
        htv_list.fchar = ".ny-budget"


        htv_list = Htv_list()
        htv_list_data.append(htv_list)

        htv_list.paramnr = 9196
        htv_list.fchar = ".nmtd-budget"


        htv_list = Htv_list()
        htv_list_data.append(htv_list)

        htv_list.paramnr = 9195
        htv_list.fchar = ".nytd-budget"


        htv_list = Htv_list()
        htv_list_data.append(htv_list)

        htv_list.paramnr = 9194
        htv_list.fchar = ".today-serv"


        htv_list = Htv_list()
        htv_list_data.append(htv_list)

        htv_list.paramnr = 9193
        htv_list.fchar = ".today-tax"


        htv_list = Htv_list()
        htv_list_data.append(htv_list)

        htv_list.paramnr = 9192
        htv_list.fchar = ".mtd-serv"


        htv_list = Htv_list()
        htv_list_data.append(htv_list)

        htv_list.paramnr = 9191
        htv_list.fchar = ".mtd-tax"


        htv_list = Htv_list()
        htv_list_data.append(htv_list)

        htv_list.paramnr = 9190
        htv_list.fchar = ".ytd-serv"


        htv_list = Htv_list()
        htv_list_data.append(htv_list)

        htv_list.paramnr = 9189
        htv_list.fchar = ".ytd-tax"


        htv_list = Htv_list()
        htv_list_data.append(htv_list)

        htv_list.paramnr = 9188
        htv_list.fchar = ".lmtoday-serv"


        htv_list = Htv_list()
        htv_list_data.append(htv_list)

        htv_list.paramnr = 9187
        htv_list.fchar = ".lmtoday-tax"


        htv_list = Htv_list()
        htv_list_data.append(htv_list)

        htv_list.paramnr = 9186
        htv_list.fchar = ".pmtd-serv"


        htv_list = Htv_list()
        htv_list_data.append(htv_list)

        htv_list.paramnr = 9185
        htv_list.fchar = ".pmtd-tax"


        htv_list = Htv_list()
        htv_list_data.append(htv_list)

        htv_list.paramnr = 9184
        htv_list.fchar = ".lmtd-serv"


        htv_list = Htv_list()
        htv_list_data.append(htv_list)

        htv_list.paramnr = 9183
        htv_list.fchar = ".lmtd-tax"


        htv_list = Htv_list()
        htv_list_data.append(htv_list)

        htv_list.paramnr = 9182
        htv_list.fchar = ".lm-mtd"


        htp_list = Htp_list()
        htp_list_data.append(htp_list)

        htp_list.paramnr = 8092
        htp_list.fchar = keycmd + "NatRev"


        htp_list = Htp_list()
        htp_list_data.append(htp_list)

        htp_list.paramnr = 8813
        htp_list.fchar = keycmd + "NatRoom"


        htp_list = Htp_list()
        htp_list_data.append(htp_list)

        htp_list.paramnr = 8814
        htp_list.fchar = keycmd + "NatPers"


        htp_list = Htp_list()
        htp_list_data.append(htp_list)

        htp_list.paramnr = 9981
        htp_list.fchar = keycmd + "CompSaleRm"


        htp_list = Htp_list()
        htp_list_data.append(htp_list)

        htp_list.paramnr = 9982
        htp_list.fchar = keycmd + "CompOccRm"


        htp_list = Htp_list()
        htp_list_data.append(htp_list)

        htp_list.paramnr = 9983
        htp_list.fchar = keycmd + "CompCompliRm"


        htp_list = Htp_list()
        htp_list_data.append(htp_list)

        htp_list.paramnr = 9984
        htp_list.fchar = keycmd + "CompRmRev"


        htp_list = Htp_list()
        htp_list_data.append(htp_list)

        htp_list.paramnr = 9985
        htp_list.fchar = keycmd + "SgFbSales"


        htp_list = Htp_list()
        htp_list_data.append(htp_list)

        htp_list.paramnr = 9986
        htp_list.fchar = keycmd + "SgFbQty"


        htp_list = Htp_list()
        htp_list_data.append(htp_list)

        htp_list.paramnr = 1995
        htp_list.fchar = keycmd + "FP-Cover"


        htp_list = Htp_list()
        htp_list_data.append(htp_list)

        htp_list.paramnr = 1996
        htp_list.fchar = keycmd + "BP-Cover"


        htp_list = Htp_list()
        htp_list_data.append(htp_list)

        htp_list.paramnr = 1997
        htp_list.fchar = keycmd + "f-fbstat"


        htp_list = Htp_list()
        htp_list_data.append(htp_list)

        htp_list.paramnr = 1998
        htp_list.fchar = keycmd + "b-fbstat"


        htp_list = Htp_list()
        htp_list_data.append(htp_list)

        htp_list.paramnr = 1999
        htp_list.fchar = keycmd + "o-fbstat"


        htp_list = Htp_list()
        htp_list_data.append(htp_list)

        htp_list.paramnr = 9106
        htp_list.fchar = keycmd + "WIG"


        htp_list = Htp_list()
        htp_list_data.append(htp_list)

        htp_list.paramnr = 9092
        htp_list.fchar = keycmd + "SourceRev"


        htp_list = Htp_list()
        htp_list_data.append(htp_list)

        htp_list.paramnr = 9813
        htp_list.fchar = keycmd + "SourceRoom"


        htp_list = Htp_list()
        htp_list_data.append(htp_list)

        htp_list.paramnr = 9814
        htp_list.fchar = keycmd + "SourcePers"


        htp_list = Htp_list()
        htp_list_data.append(htp_list)

        htp_list.paramnr = 7194
        htp_list.fchar = keycmd + "Canc-night"


        htp_list = Htp_list()
        htp_list_data.append(htp_list)

        htp_list.paramnr = 9188
        htp_list.fchar = keycmd + "Child-arr"


        htp_list = Htp_list()
        htp_list_data.append(htp_list)

        htp_list.paramnr = 9190
        htp_list.fchar = keycmd + "Child-dep"


        htp_list = Htp_list()
        htp_list_data.append(htp_list)

        htp_list.paramnr = 1921
        htp_list.fchar = keycmd + "F-Cover1"


        htp_list = Htp_list()
        htp_list_data.append(htp_list)

        htp_list.paramnr = 1922
        htp_list.fchar = keycmd + "F-Cover2"


        htp_list = Htp_list()
        htp_list_data.append(htp_list)

        htp_list.paramnr = 1923
        htp_list.fchar = keycmd + "F-Cover3"


        htp_list = Htp_list()
        htp_list_data.append(htp_list)

        htp_list.paramnr = 1924
        htp_list.fchar = keycmd + "F-Cover4"


        htp_list = Htp_list()
        htp_list_data.append(htp_list)

        htp_list.paramnr = 1971
        htp_list.fchar = keycmd + "B-Cover1"


        htp_list = Htp_list()
        htp_list_data.append(htp_list)

        htp_list.paramnr = 1972
        htp_list.fchar = keycmd + "B-Cover2"


        htp_list = Htp_list()
        htp_list_data.append(htp_list)

        htp_list.paramnr = 1973
        htp_list.fchar = keycmd + "B-Cover3"


        htp_list = Htp_list()
        htp_list_data.append(htp_list)

        htp_list.paramnr = 1974
        htp_list.fchar = keycmd + "B-Cover4"


        htp_list = Htp_list()
        htp_list_data.append(htp_list)

        htp_list.paramnr = 1991
        htp_list.fchar = keycmd + "P-Cover1"


        htp_list = Htp_list()
        htp_list_data.append(htp_list)

        htp_list.paramnr = 1992
        htp_list.fchar = keycmd + "P-Cover2"


        htp_list = Htp_list()
        htp_list_data.append(htp_list)

        htp_list.paramnr = 1993
        htp_list.fchar = keycmd + "P-Cover3"


        htp_list = Htp_list()
        htp_list_data.append(htp_list)

        htp_list.paramnr = 1994
        htp_list.fchar = keycmd + "P-Cover4"


        htp_list = Htp_list()
        htp_list_data.append(htp_list)

        htp_list.paramnr = 9000
        htp_list.fchar = keycmd + "LOS"


        for n in range(1,31 + 1) :
            htv_list = Htv_list()
            htv_list_data.append(htv_list)

            htv_list.paramnr = 3000 + n
            htv_list.fchar = ".D" + to_string(n, "99")

        for briefzei in db_session.query(Briefzei).filter(
                 (Briefzei.briefnr == briefnr)).order_by(Briefzei.briefzeilnr).all():
            j = 1
            for i in range(1,length(briefzei.texte)  + 1) :

                if asc(substring(briefzei.texte, i - 1, 1)) == 10:
                    n = i - j
                    c = substring(briefzei.texte, j - 1, n)
                    l = length(c)

                    if not continued:
                        brief_list = Brief_list()
                        brief_list_data.append(brief_list)

                    brief_list.b_text = brief_list.b_text + c
                    j = i + 1
            n = length(briefzei.texte) - j + 1
            c = substring(briefzei.texte, j - 1, n)

            if not continued:
                brief_list = Brief_list()
                brief_list_data.append(brief_list)

            b_text = b_text + c

    htparam = get_cache (Htparam, {"paramnr": [(eq, 479)]})
    serv_vat = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 144)]})

    if htparam.fchar != "":

        waehrung = get_cache (Waehrung, {"wabkurz": [(eq, htparam.fchar)]})

        if waehrung:
            foreign_nr = waehrung.waehrungsnr

    htparam = get_cache (Htparam, {"paramnr": [(eq, 186)]})

    if htparam.feldtyp == 3 and htparam.fdate != None:
        start_date = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 491)]})
    price_decimal = htparam.finteger
    no_decimal = (price_decimal == 0)
    fill_list()
    batch_list = Batch_list()
    batch_list_data.append(batch_list)


    brief = get_cache (Brief, {"briefnr": [(eq, briefnr)]})
    batch_list.briefnr = briefnr
    batch_list.fname = brief.fname

    htparam = get_cache (Htparam, {"paramnr": [(eq, 64)]})
    outfile_dir = htparam.fchar

    if outfile_dir != "" and substring(outfile_dir, length(outfile_dir) - 1, 1) != ("\\").lower() :
        outfile_dir = outfile_dir + "\\"

    return generate_output()