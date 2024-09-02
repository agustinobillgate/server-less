from functions.additional_functions import *
import decimal
from datetime import date
from models import Htparam, Waehrung, Brief, Briefzei

def prepare_fo_parexcelbl(briefnr:int):
    serv_vat = False
    foreign_nr = 0
    start_date = None
    price_decimal = 0
    no_decimal = False
    outfile_dir = ""
    keycmd = ""
    keyvar = ""
    batch_list_list = []
    htv_list_list = []
    htp_list_list = []
    brief_list_list = []
    htparam = waehrung = brief = briefzei = None

    batch_list = htv_list = htp_list = brief_list = None

    batch_list_list, Batch_list = create_model("Batch_list", {"briefnr":int, "fname":str})
    htv_list_list, Htv_list = create_model("Htv_list", {"paramnr":int, "fchar":str})
    htp_list_list, Htp_list = create_model("Htp_list", {"paramnr":int, "fchar":str})
    brief_list_list, Brief_list = create_model("Brief_list", {"b_text":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal serv_vat, foreign_nr, start_date, price_decimal, no_decimal, outfile_dir, keycmd, keyvar, batch_list_list, htv_list_list, htp_list_list, brief_list_list, htparam, waehrung, brief, briefzei


        nonlocal batch_list, htv_list, htp_list, brief_list
        nonlocal batch_list_list, htv_list_list, htp_list_list, brief_list_list
        return {"serv_vat": serv_vat, "foreign_nr": foreign_nr, "start_date": start_date, "price_decimal": price_decimal, "no_decimal": no_decimal, "outfile_dir": outfile_dir, "keycmd": keycmd, "keyvar": keyvar, "batch-list": batch_list_list, "htv-list": htv_list_list, "htp-list": htp_list_list, "brief-list": brief_list_list}

    def fill_list():

        nonlocal serv_vat, foreign_nr, start_date, price_decimal, no_decimal, outfile_dir, keycmd, keyvar, batch_list_list, htv_list_list, htp_list_list, brief_list_list, htparam, waehrung, brief, briefzei


        nonlocal batch_list, htv_list, htp_list, brief_list
        nonlocal batch_list_list, htv_list_list, htp_list_list, brief_list_list

        i:int = 0
        j:int = 0
        n:int = 0
        c:str = ""
        l:int = 0
        continued:bool = False

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 600)).first()
        keycmd = htparam.fchar

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 2030)).first()
        keyvar = htparam.fchar

        for htparam in db_session.query(Htparam).filter(
                (Htparam.paramgruppe == 8) &  (htparam.fchar != "")).all():

            if substring(htparam.fchar, 0 , 1) == ".":
                htv_list = Htv_list()
                htv_list_list.append(htv_list)

                htv_list.paramnr = htparam.paramnr
                htv_list.fchar = htparam.fchar
            else:
                htp_list = Htp_list()
                htp_list_list.append(htp_list)

                htp_list.paramnr = htparam.paramnr
                htp_list.fchar = keycmd + htparam.fchar
        htv_list = Htv_list()
        htv_list_list.append(htv_list)

        htv_list.paramnr = 9199
        htv_list.fchar = ".yesterday"


        htv_list = Htv_list()
        htv_list_list.append(htv_list)

        htv_list.paramnr = 9198
        htv_list.fchar = ".lm_today"


        htv_list = Htv_list()
        htv_list_list.append(htv_list)

        htv_list.paramnr = 9197
        htv_list.fchar = ".ny_budget"


        htv_list = Htv_list()
        htv_list_list.append(htv_list)

        htv_list.paramnr = 9196
        htv_list.fchar = ".nmtd_budget"


        htv_list = Htv_list()
        htv_list_list.append(htv_list)

        htv_list.paramnr = 9195
        htv_list.fchar = ".nytd_budget"


        htv_list = Htv_list()
        htv_list_list.append(htv_list)

        htv_list.paramnr = 9194
        htv_list.fchar = ".today_serv"


        htv_list = Htv_list()
        htv_list_list.append(htv_list)

        htv_list.paramnr = 9193
        htv_list.fchar = ".today_tax"


        htv_list = Htv_list()
        htv_list_list.append(htv_list)

        htv_list.paramnr = 9192
        htv_list.fchar = ".mtd_serv"


        htv_list = Htv_list()
        htv_list_list.append(htv_list)

        htv_list.paramnr = 9191
        htv_list.fchar = ".mtd_tax"


        htv_list = Htv_list()
        htv_list_list.append(htv_list)

        htv_list.paramnr = 9190
        htv_list.fchar = ".ytd_serv"


        htv_list = Htv_list()
        htv_list_list.append(htv_list)

        htv_list.paramnr = 9189
        htv_list.fchar = ".ytd_tax"


        htv_list = Htv_list()
        htv_list_list.append(htv_list)

        htv_list.paramnr = 9188
        htv_list.fchar = ".lmtoday_serv"


        htv_list = Htv_list()
        htv_list_list.append(htv_list)

        htv_list.paramnr = 9187
        htv_list.fchar = ".lmtoday_tax"


        htv_list = Htv_list()
        htv_list_list.append(htv_list)

        htv_list.paramnr = 9186
        htv_list.fchar = ".pmtd_serv"


        htv_list = Htv_list()
        htv_list_list.append(htv_list)

        htv_list.paramnr = 9185
        htv_list.fchar = ".pmtd_tax"


        htv_list = Htv_list()
        htv_list_list.append(htv_list)

        htv_list.paramnr = 9184
        htv_list.fchar = ".lmtd_serv"


        htv_list = Htv_list()
        htv_list_list.append(htv_list)

        htv_list.paramnr = 9183
        htv_list.fchar = ".lmtd_tax"


        htv_list = Htv_list()
        htv_list_list.append(htv_list)

        htv_list.paramnr = 9182
        htv_list.fchar = ".lm_mtd"


        htp_list = Htp_list()
        htp_list_list.append(htp_list)

        htp_list.paramnr = 8092
        htp_list.fchar = keycmd + "NatRev"


        htp_list = Htp_list()
        htp_list_list.append(htp_list)

        htp_list.paramnr = 8813
        htp_list.fchar = keycmd + "NatRoom"


        htp_list = Htp_list()
        htp_list_list.append(htp_list)

        htp_list.paramnr = 8814
        htp_list.fchar = keycmd + "NatPers"


        htp_list = Htp_list()
        htp_list_list.append(htp_list)

        htp_list.paramnr = 9981
        htp_list.fchar = keycmd + "CompSaleRm"


        htp_list = Htp_list()
        htp_list_list.append(htp_list)

        htp_list.paramnr = 9982
        htp_list.fchar = keycmd + "CompOccRm"


        htp_list = Htp_list()
        htp_list_list.append(htp_list)

        htp_list.paramnr = 9983
        htp_list.fchar = keycmd + "CompCompliRm"


        htp_list = Htp_list()
        htp_list_list.append(htp_list)

        htp_list.paramnr = 9984
        htp_list.fchar = keycmd + "CompRmRev"


        htp_list = Htp_list()
        htp_list_list.append(htp_list)

        htp_list.paramnr = 9985
        htp_list.fchar = keycmd + "SgFbSales"


        htp_list = Htp_list()
        htp_list_list.append(htp_list)

        htp_list.paramnr = 9986
        htp_list.fchar = keycmd + "SgFbQty"


        htp_list = Htp_list()
        htp_list_list.append(htp_list)

        htp_list.paramnr = 1995
        htp_list.fchar = keycmd + "FP_Cover"


        htp_list = Htp_list()
        htp_list_list.append(htp_list)

        htp_list.paramnr = 1996
        htp_list.fchar = keycmd + "BP_Cover"


        htp_list = Htp_list()
        htp_list_list.append(htp_list)

        htp_list.paramnr = 1997
        htp_list.fchar = keycmd + "f_fbstat"


        htp_list = Htp_list()
        htp_list_list.append(htp_list)

        htp_list.paramnr = 1998
        htp_list.fchar = keycmd + "b_fbstat"


        htp_list = Htp_list()
        htp_list_list.append(htp_list)

        htp_list.paramnr = 1999
        htp_list.fchar = keycmd + "o_fbstat"


        htp_list = Htp_list()
        htp_list_list.append(htp_list)

        htp_list.paramnr = 9106
        htp_list.fchar = keycmd + "WIG"


        htp_list = Htp_list()
        htp_list_list.append(htp_list)

        htp_list.paramnr = 9092
        htp_list.fchar = keycmd + "SourceRev"


        htp_list = Htp_list()
        htp_list_list.append(htp_list)

        htp_list.paramnr = 9813
        htp_list.fchar = keycmd + "SourceRoom"


        htp_list = Htp_list()
        htp_list_list.append(htp_list)

        htp_list.paramnr = 9814
        htp_list.fchar = keycmd + "SourcePers"


        htp_list = Htp_list()
        htp_list_list.append(htp_list)

        htp_list.paramnr = 7194
        htp_list.fchar = keycmd + "Canc_night"


        htp_list = Htp_list()
        htp_list_list.append(htp_list)

        htp_list.paramnr = 9188
        htp_list.fchar = keycmd + "Child_arr"


        htp_list = Htp_list()
        htp_list_list.append(htp_list)

        htp_list.paramnr = 9190
        htp_list.fchar = keycmd + "Child_dep"


        htp_list = Htp_list()
        htp_list_list.append(htp_list)

        htp_list.paramnr = 1921
        htp_list.fchar = keycmd + "F_Cover1"


        htp_list = Htp_list()
        htp_list_list.append(htp_list)

        htp_list.paramnr = 1922
        htp_list.fchar = keycmd + "F_Cover2"


        htp_list = Htp_list()
        htp_list_list.append(htp_list)

        htp_list.paramnr = 1923
        htp_list.fchar = keycmd + "F_Cover3"


        htp_list = Htp_list()
        htp_list_list.append(htp_list)

        htp_list.paramnr = 1924
        htp_list.fchar = keycmd + "F_Cover4"


        htp_list = Htp_list()
        htp_list_list.append(htp_list)

        htp_list.paramnr = 1971
        htp_list.fchar = keycmd + "B_Cover1"


        htp_list = Htp_list()
        htp_list_list.append(htp_list)

        htp_list.paramnr = 1972
        htp_list.fchar = keycmd + "B_Cover2"


        htp_list = Htp_list()
        htp_list_list.append(htp_list)

        htp_list.paramnr = 1973
        htp_list.fchar = keycmd + "B_Cover3"


        htp_list = Htp_list()
        htp_list_list.append(htp_list)

        htp_list.paramnr = 1974
        htp_list.fchar = keycmd + "B_Cover4"


        htp_list = Htp_list()
        htp_list_list.append(htp_list)

        htp_list.paramnr = 1991
        htp_list.fchar = keycmd + "P_Cover1"


        htp_list = Htp_list()
        htp_list_list.append(htp_list)

        htp_list.paramnr = 1992
        htp_list.fchar = keycmd + "P_Cover2"


        htp_list = Htp_list()
        htp_list_list.append(htp_list)

        htp_list.paramnr = 1993
        htp_list.fchar = keycmd + "P_Cover3"


        htp_list = Htp_list()
        htp_list_list.append(htp_list)

        htp_list.paramnr = 1994
        htp_list.fchar = keycmd + "P_Cover4"


        htp_list = Htp_list()
        htp_list_list.append(htp_list)

        htp_list.paramnr = 9000
        htp_list.fchar = keycmd + "LOS"


        for n in range(1,31 + 1) :
            htv_list = Htv_list()
            htv_list_list.append(htv_list)

            htv_list.paramnr = 3000 + n
            htv_list.fchar = ".D" + to_string(n, "99")

        for briefzei in db_session.query(Briefzei).filter(
                (Briefzei.briefnr == briefnr)).all():
            j = 1
            for i in range(1,len(briefzei.texte)  + 1) :

                if ord(substring(briefzei.texte, i - 1, 1)) == 10:
                    n = i - j
                    c = substring(briefzei.texte, j - 1, n)
                    l = len(c)

                    if not continued:
                        brief_list = Brief_list()
                    brief_list_list.append(brief_list)

                    brief_list.b_text = brief_list.b_text + c
                    j = i + 1
            n = len(briefzei.texte) - j + 1
            c = substring(briefzei.texte, j - 1, n)

            if not continued:
                brief_list = Brief_list()
            brief_list_list.append(brief_list)

            b_text = b_text + c


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 479)).first()
    serv_vat = htparam.flogical

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 144)).first()

    if htparam.fchar != "":

        waehrung = db_session.query(Waehrung).filter(
                (Waehrung.wabkurz == htparam.fchar)).first()

        if waehrung:
            foreign_nr = waehrung.waehrungsnr

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 186)).first()

    if htparam.feldtyp == 3 and htparam.fdate != None:
        start_date = htparam.fdate

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 491)).first()
    price_decimal = htparam.finteger
    no_decimal = (price_decimal == 0)
    fill_list()
    batch_list = Batch_list()
    batch_list_list.append(batch_list)


    brief = db_session.query(Brief).filter(
            (briefnr == briefnr)).first()
    batch_list.briefnr = briefnr
    batch_list.fname = brief.fname

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 64)).first()
    outfile_dir = htparam.fchar

    if outfile_dir != "" and substring(outfile_dir, len(outfile_dir) - 1, 1) != "\\":
        outfile_dir = outfile_dir + "\\"

    return generate_output()