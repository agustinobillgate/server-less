#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Parameters, Brief, Htparam, Waehrung, Zimmer, Briefzei

def prepare_fo_parxlsbl(pvilanguage:int, briefnr:int):

    prepare_cache ([Htparam, Waehrung, Briefzei])

    xls_dir = ""
    msg_str = ""
    serv_vat = False
    foreign_nr = 0
    start_date = None
    price_decimal = 0
    no_decimal = False
    keycmd = ""
    keyvar = ""
    outfile_dir = ""
    anz0 = 0
    htv_list_data = []
    htp_list_data = []
    brief_list_data = []
    t_brief_data = []
    t_parameters_data = []
    lvcarea:string = "prepare-fo-parxls"
    parameters = brief = htparam = waehrung = zimmer = briefzei = None

    htv_list = htp_list = brief_list = t_parameters = t_brief = None

    htv_list_data, Htv_list = create_model("Htv_list", {"paramnr":int, "fchar":string})
    htp_list_data, Htp_list = create_model("Htp_list", {"paramnr":int, "fchar":string})
    brief_list_data, Brief_list = create_model("Brief_list", {"b_text":string})
    t_parameters_data, T_parameters = create_model_like(Parameters)
    t_brief_data, T_brief = create_model_like(Brief)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal xls_dir, msg_str, serv_vat, foreign_nr, start_date, price_decimal, no_decimal, keycmd, keyvar, outfile_dir, anz0, htv_list_data, htp_list_data, brief_list_data, t_brief_data, t_parameters_data, lvcarea, parameters, brief, htparam, waehrung, zimmer, briefzei
        nonlocal pvilanguage, briefnr


        nonlocal htv_list, htp_list, brief_list, t_parameters, t_brief
        nonlocal htv_list_data, htp_list_data, brief_list_data, t_parameters_data, t_brief_data

        return {"xls_dir": xls_dir, "msg_str": msg_str, "serv_vat": serv_vat, "foreign_nr": foreign_nr, "start_date": start_date, "price_decimal": price_decimal, "no_decimal": no_decimal, "keycmd": keycmd, "keyvar": keyvar, "outfile_dir": outfile_dir, "anz0": anz0, "htv-list": htv_list_data, "htp-list": htp_list_data, "brief-list": brief_list_data, "t-brief": t_brief_data, "t-parameters": t_parameters_data}

    def fill_list():

        nonlocal xls_dir, msg_str, serv_vat, foreign_nr, start_date, price_decimal, no_decimal, keycmd, keyvar, outfile_dir, anz0, htv_list_data, htp_list_data, brief_list_data, t_brief_data, t_parameters_data, lvcarea, parameters, brief, htparam, waehrung, zimmer, briefzei
        nonlocal pvilanguage, briefnr


        nonlocal htv_list, htp_list, brief_list, t_parameters, t_brief
        nonlocal htv_list_data, htp_list_data, brief_list_data, t_parameters_data, t_brief_data

        i:int = 0
        j:int = 0
        n:int = 0
        l:int = 0
        continued:bool = False
        c:string = ""
        ct:string = ""

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

        htv_list.paramnr = 9200
        htv_list.fchar = ".lytd-serv"


        htv_list = Htv_list()
        htv_list_data.append(htv_list)

        htv_list.paramnr = 9201
        htv_list.fchar = ".lytd-tax"


        htv_list = Htv_list()
        htv_list_data.append(htv_list)

        htv_list.paramnr = 9202
        htv_list.fchar = ".lytoday-serv"


        htv_list = Htv_list()
        htv_list_data.append(htv_list)

        htv_list.paramnr = 9203
        htv_list.fchar = ".lytoday-tax"


        htv_list = Htv_list()
        htv_list_data.append(htv_list)

        htv_list.paramnr = 9204
        htv_list.fchar = ".month-budget"


        htv_list = Htv_list()
        htv_list_data.append(htv_list)

        htv_list.paramnr = 9205
        htv_list.fchar = ".year-budget"


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

        htp_list.paramnr = 2001
        htp_list.fchar = keycmd + "PI-Cover1"


        htp_list = Htp_list()
        htp_list_data.append(htp_list)

        htp_list.paramnr = 2002
        htp_list.fchar = keycmd + "PI-Cover2"


        htp_list = Htp_list()
        htp_list_data.append(htp_list)

        htp_list.paramnr = 2003
        htp_list.fchar = keycmd + "PI-Cover3"


        htp_list = Htp_list()
        htp_list_data.append(htp_list)

        htp_list.paramnr = 2004
        htp_list.fchar = keycmd + "PI-Cover4"


        htp_list = Htp_list()
        htp_list_data.append(htp_list)

        htp_list.paramnr = 2005
        htp_list.fchar = keycmd + "PN-Cover1"


        htp_list = Htp_list()
        htp_list_data.append(htp_list)

        htp_list.paramnr = 2006
        htp_list.fchar = keycmd + "PN-Cover2"


        htp_list = Htp_list()
        htp_list_data.append(htp_list)

        htp_list.paramnr = 2007
        htp_list.fchar = keycmd + "PN-Cover3"


        htp_list = Htp_list()
        htp_list_data.append(htp_list)

        htp_list.paramnr = 2008
        htp_list.fchar = keycmd + "PN-Cover4"


        htp_list = Htp_list()
        htp_list_data.append(htp_list)

        htp_list.paramnr = 2009
        htp_list.fchar = keycmd + "PH-Cover1"


        htp_list = Htp_list()
        htp_list_data.append(htp_list)

        htp_list.paramnr = 2010
        htp_list.fchar = keycmd + "PH-Cover2"


        htp_list = Htp_list()
        htp_list_data.append(htp_list)

        htp_list.paramnr = 2011
        htp_list.fchar = keycmd + "PH-Cover3"


        htp_list = Htp_list()
        htp_list_data.append(htp_list)

        htp_list.paramnr = 2012
        htp_list.fchar = keycmd + "PH-Cover4"


        htp_list = Htp_list()
        htp_list_data.append(htp_list)

        htp_list.paramnr = 2013
        htp_list.fchar = keycmd + "PW-Cover1"


        htp_list = Htp_list()
        htp_list_data.append(htp_list)

        htp_list.paramnr = 2014
        htp_list.fchar = keycmd + "PW-Cover2"


        htp_list = Htp_list()
        htp_list_data.append(htp_list)

        htp_list.paramnr = 2015
        htp_list.fchar = keycmd + "PW-Cover3"


        htp_list = Htp_list()
        htp_list_data.append(htp_list)

        htp_list.paramnr = 2016
        htp_list.fchar = keycmd + "PW-Cover4"


        htp_list = Htp_list()
        htp_list_data.append(htp_list)

        htp_list.paramnr = 2020
        htp_list.fchar = keycmd + "FP-Cover1"


        htp_list = Htp_list()
        htp_list_data.append(htp_list)

        htp_list.paramnr = 2021
        htp_list.fchar = keycmd + "FP-Cover2"


        htp_list = Htp_list()
        htp_list_data.append(htp_list)

        htp_list.paramnr = 2022
        htp_list.fchar = keycmd + "FP-Cover3"


        htp_list = Htp_list()
        htp_list_data.append(htp_list)

        htp_list.paramnr = 2023
        htp_list.fchar = keycmd + "FP-Cover4"


        htp_list = Htp_list()
        htp_list_data.append(htp_list)

        htp_list.paramnr = 2024
        htp_list.fchar = keycmd + "BP-Cover1"


        htp_list = Htp_list()
        htp_list_data.append(htp_list)

        htp_list.paramnr = 2025
        htp_list.fchar = keycmd + "BP-Cover2"


        htp_list = Htp_list()
        htp_list_data.append(htp_list)

        htp_list.paramnr = 2026
        htp_list.fchar = keycmd + "BP-Cover3"


        htp_list = Htp_list()
        htp_list_data.append(htp_list)

        htp_list.paramnr = 2027
        htp_list.fchar = keycmd + "BP-Cover4"


        htp_list = Htp_list()
        htp_list_data.append(htp_list)

        htp_list.paramnr = 2028
        htp_list.fchar = keycmd + "G-Cover"


        htp_list = Htp_list()
        htp_list_data.append(htp_list)

        htp_list.paramnr = 2029
        htp_list.fchar = keycmd + "TOT-BILL"


        htp_list = Htp_list()
        htp_list_data.append(htp_list)

        htp_list.paramnr = 2031
        htp_list.fchar = keycmd + "PAX-TABLE"


        htp_list = Htp_list()
        htp_list_data.append(htp_list)

        htp_list.paramnr = 2032
        htp_list.fchar = keycmd + "PC-Cover1"


        htp_list = Htp_list()
        htp_list_data.append(htp_list)

        htp_list.paramnr = 2033
        htp_list.fchar = keycmd + "PC-Cover2"


        htp_list = Htp_list()
        htp_list_data.append(htp_list)

        htp_list.paramnr = 2034
        htp_list.fchar = keycmd + "PC-Cover3"


        htp_list = Htp_list()
        htp_list_data.append(htp_list)

        htp_list.paramnr = 2035
        htp_list.fchar = keycmd + "PC-Cover4"


        htp_list = Htp_list()
        htp_list_data.append(htp_list)

        htp_list.paramnr = 2036
        htp_list.fchar = keycmd + "PO-Cover1"


        htp_list = Htp_list()
        htp_list_data.append(htp_list)

        htp_list.paramnr = 2037
        htp_list.fchar = keycmd + "PO-Cover2"


        htp_list = Htp_list()
        htp_list_data.append(htp_list)

        htp_list.paramnr = 2038
        htp_list.fchar = keycmd + "PO-Cover3"


        htp_list = Htp_list()
        htp_list_data.append(htp_list)

        htp_list.paramnr = 2039
        htp_list.fchar = keycmd + "PO-Cover4"


        htp_list = Htp_list()
        htp_list_data.append(htp_list)

        htp_list.paramnr = 2040
        htp_list.fchar = keycmd + "PCO-Cover1"


        htp_list = Htp_list()
        htp_list_data.append(htp_list)

        htp_list.paramnr = 2041
        htp_list.fchar = keycmd + "PCO-Cover2"


        htp_list = Htp_list()
        htp_list_data.append(htp_list)

        htp_list.paramnr = 2042
        htp_list.fchar = keycmd + "PCO-Cover3"


        htp_list = Htp_list()
        htp_list_data.append(htp_list)

        htp_list.paramnr = 2043
        htp_list.fchar = keycmd + "PCO-Cover4"


        htp_list = Htp_list()
        htp_list_data.append(htp_list)

        htp_list.paramnr = 2044
        htp_list.fchar = keycmd + "Rev-Inhouse1"


        htp_list = Htp_list()
        htp_list_data.append(htp_list)

        htp_list.paramnr = 2045
        htp_list.fchar = keycmd + "Rev-Inhouse2"


        htp_list = Htp_list()
        htp_list_data.append(htp_list)

        htp_list.paramnr = 2046
        htp_list.fchar = keycmd + "Rev-Inhouse3"


        htp_list = Htp_list()
        htp_list_data.append(htp_list)

        htp_list.paramnr = 2047
        htp_list.fchar = keycmd + "Rev-Inhouse4"


        htp_list = Htp_list()
        htp_list_data.append(htp_list)

        htp_list.paramnr = 2048
        htp_list.fchar = keycmd + "Rev-Outsider1"


        htp_list = Htp_list()
        htp_list_data.append(htp_list)

        htp_list.paramnr = 2049
        htp_list.fchar = keycmd + "Rev-Outsider2"


        htp_list = Htp_list()
        htp_list_data.append(htp_list)

        htp_list.paramnr = 2050
        htp_list.fchar = keycmd + "Rev-Outsider3"


        htp_list = Htp_list()
        htp_list_data.append(htp_list)

        htp_list.paramnr = 2051
        htp_list.fchar = keycmd + "Rev-Outsider4"


        htp_list = Htp_list()
        htp_list_data.append(htp_list)

        htp_list.paramnr = 2052
        htp_list.fchar = keycmd + "RF-QTY"


        htp_list = Htp_list()
        htp_list_data.append(htp_list)

        htp_list.paramnr = 2053
        htp_list.fchar = keycmd + "RB-QTY"


        htp_list = Htp_list()
        htp_list_data.append(htp_list)

        htp_list.paramnr = 2054
        htp_list.fchar = keycmd + "GF-QTY"


        htp_list = Htp_list()
        htp_list_data.append(htp_list)

        htp_list.paramnr = 2055
        htp_list.fchar = keycmd + "GB-QTY"


        htp_list = Htp_list()
        htp_list_data.append(htp_list)

        htp_list.paramnr = 2056
        htp_list.fchar = keycmd + "FB-Direct"


        htp_list = Htp_list()
        htp_list_data.append(htp_list)

        htp_list.paramnr = 2057
        htp_list.fchar = keycmd + "FB-Transfer"


        htp_list = Htp_list()
        htp_list_data.append(htp_list)

        htp_list.paramnr = 2058
        htp_list.fchar = keycmd + "FB-Cost-Alloc"


        htp_list = Htp_list()
        htp_list_data.append(htp_list)

        htp_list.paramnr = 2059
        htp_list.fchar = keycmd + "FB-Compliment"


        htp_list = Htp_list()
        htp_list_data.append(htp_list)

        htp_list.paramnr = 2060
        htp_list.fchar = keycmd + "Cancel-CI"


        htp_list = Htp_list()
        htp_list_data.append(htp_list)

        htp_list.paramnr = 2061
        htp_list.fchar = keycmd + "WIG-CI"


        htp_list = Htp_list()
        htp_list_data.append(htp_list)

        htp_list.paramnr = 9106
        htp_list.fchar = keycmd + "WIG"


        htp_list = Htp_list()
        htp_list_data.append(htp_list)

        htp_list.paramnr = 7194
        htp_list.fchar = keycmd + "Canc-night"


        htp_list = Htp_list()
        htp_list_data.append(htp_list)

        htp_list.paramnr = 7195
        htp_list.fchar = keycmd + "canc-cidate"


        htp_list = Htp_list()
        htp_list_data.append(htp_list)

        htp_list.paramnr = 7196
        htp_list.fchar = keycmd + "canc-cidate-nite"


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

        htp_list.paramnr = 9180
        htp_list.fchar = keycmd + "statRoom"


        htp_list = Htp_list()
        htp_list_data.append(htp_list)

        htp_list.paramnr = 8180
        htp_list.fchar = keycmd + "rComp"


        htp_list = Htp_list()
        htp_list_data.append(htp_list)

        htp_list.paramnr = 9000
        htp_list.fchar = keycmd + "LOS"


        htp_list = Htp_list()
        htp_list_data.append(htp_list)

        htp_list.paramnr = 9001
        htp_list.fchar = keycmd + "CountryRev"


        htp_list = Htp_list()
        htp_list_data.append(htp_list)

        htp_list.paramnr = 9002
        htp_list.fchar = keycmd + "CountryRoom"


        htp_list = Htp_list()
        htp_list_data.append(htp_list)

        htp_list.paramnr = 9003
        htp_list.fchar = keycmd + "RcRev"


        htp_list = Htp_list()
        htp_list_data.append(htp_list)

        htp_list.paramnr = 9004
        htp_list.fchar = keycmd + "RcRoom"


        htp_list = Htp_list()
        htp_list_data.append(htp_list)

        htp_list.paramnr = 9005
        htp_list.fchar = keycmd + "RcSegRev"


        htp_list = Htp_list()
        htp_list_data.append(htp_list)

        htp_list.paramnr = 9006
        htp_list.fchar = keycmd + "RcSegRoom"


        htp_list = Htp_list()
        htp_list_data.append(htp_list)

        htp_list.paramnr = 9007
        htp_list.fchar = keycmd + "SEGMREV-OTH"


        htp_list = Htp_list()
        htp_list_data.append(htp_list)

        htp_list.paramnr = 9008
        htp_list.fchar = keycmd + "comp-bonus"


        htp_list = Htp_list()
        htp_list_data.append(htp_list)

        htp_list.paramnr = 9051
        htp_list.fchar = keycmd + "sameday-res"


        htp_list = Htp_list()
        htp_list_data.append(htp_list)

        htp_list.paramnr = 9052
        htp_list.fchar = keycmd + "grp-arr"


        htp_list = Htp_list()
        htp_list_data.append(htp_list)

        htp_list.paramnr = 9053
        htp_list.fchar = keycmd + "grp-dep"


        htp_list = Htp_list()
        htp_list_data.append(htp_list)

        htp_list.paramnr = 9054
        htp_list.fchar = keycmd + "grp-room"


        htp_list = Htp_list()
        htp_list_data.append(htp_list)

        htp_list.paramnr = 9055
        htp_list.fchar = keycmd + "indv-room"


        for n in range(1,31 + 1) :
            htv_list = Htv_list()
            htv_list_data.append(htv_list)

            htv_list.paramnr = 3000 + n
            htv_list.fchar = ".D" + to_string(n, "99")


        htp_list = Htp_list()
        htp_list_data.append(htp_list)

        htp_list.paramnr = 9009
        htp_list.fchar = keycmd + "rmrev"


        htp_list = Htp_list()
        htp_list_data.append(htp_list)

        htp_list.paramnr = 9010
        htp_list.fchar = keycmd + "rmnight"


        htp_list = Htp_list()
        htp_list_data.append(htp_list)

        htp_list.paramnr = 9011
        htp_list.fchar = keycmd + "lyrmrev"


        htp_list = Htp_list()
        htp_list_data.append(htp_list)

        htp_list.paramnr = 9012
        htp_list.fchar = keycmd + "lyrmnight"


        htp_list = Htp_list()
        htp_list_data.append(htp_list)

        htp_list.paramnr = 9013
        htp_list.fchar = keycmd + "rmrev-sob"


        htp_list = Htp_list()
        htp_list_data.append(htp_list)

        htp_list.paramnr = 9014
        htp_list.fchar = keycmd + "rmnight-sob"


        htp_list = Htp_list()
        htp_list_data.append(htp_list)

        htp_list.paramnr = 9015
        htp_list.fchar = keycmd + "lyrmrev-sob"


        htp_list = Htp_list()
        htp_list_data.append(htp_list)

        htp_list.paramnr = 9016
        htp_list.fchar = keycmd + "lyrmnight-sob"


        htp_list = Htp_list()
        htp_list_data.append(htp_list)

        htp_list.paramnr = 9017
        htp_list.fchar = keycmd + "rmrev-segm"


        htp_list = Htp_list()
        htp_list_data.append(htp_list)

        htp_list.paramnr = 9018
        htp_list.fchar = keycmd + "rmnight-segm"


        htp_list = Htp_list()
        htp_list_data.append(htp_list)

        htp_list.paramnr = 9019
        htp_list.fchar = keycmd + "lyrmrev-segm"


        htp_list = Htp_list()
        htp_list_data.append(htp_list)

        htp_list.paramnr = 9020
        htp_list.fchar = keycmd + "lyrmnight-segm"


        htp_list = Htp_list()
        htp_list_data.append(htp_list)

        htp_list.paramnr = 9021
        htp_list.fchar = keycmd + "rmrev-compt"


        htp_list = Htp_list()
        htp_list_data.append(htp_list)

        htp_list.paramnr = 9022
        htp_list.fchar = keycmd + "rmocc-compt"


        htp_list = Htp_list()
        htp_list_data.append(htp_list)

        htp_list.paramnr = 9023
        htp_list.fchar = keycmd + "revbud-segm"


        htp_list = Htp_list()
        htp_list_data.append(htp_list)

        htp_list.paramnr = 9024
        htp_list.fchar = keycmd + "nightbud-segm"


        htp_list = Htp_list()
        htp_list_data.append(htp_list)

        htp_list.paramnr = 9025
        htp_list.fchar = keycmd + "lyrevbud-segm"


        htp_list = Htp_list()
        htp_list_data.append(htp_list)

        htp_list.paramnr = 9026
        htp_list.fchar = keycmd + "lynightbud-segm"


        htp_list = Htp_list()
        htp_list_data.append(htp_list)

        htp_list.paramnr = 829
        htp_list.fchar = keycmd + "INCL-BUDGET-ALL"


        for n in range(1,12 + 1) :
            htv_list = Htv_list()
            htv_list_data.append(htv_list)

            htv_list.paramnr = 4000 + n
            htv_list.fchar = ".M" + to_string(n, "99")

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


    for parameters in db_session.query(Parameters).filter(
             (Parameters.progname == ("FO-macro").lower()) & (Parameters.section == to_string(briefnr))).order_by(Parameters._recid).all():
        t_parameters = T_parameters()
        t_parameters_data.append(t_parameters)

        buffer_copy(parameters, t_parameters)

    htparam = get_cache (Htparam, {"paramnr": [(eq, 418)]})

    if htparam.fchar == "":
        msg_str = msg_str + chr_unicode(2) + translateExtended ("Excel Output Directory not defined (Param 418 Grp 15)", lvcarea, "")

        return generate_output()
    xls_dir = htparam.fchar

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

    brief = get_cache (Brief, {"briefnr": [(eq, briefnr)]})
    t_brief = T_brief()
    t_brief_data.append(t_brief)

    buffer_copy(brief, t_brief)

    htparam = get_cache (Htparam, {"paramnr": [(eq, 64)]})
    outfile_dir = htparam.fchar

    for zimmer in db_session.query(Zimmer).order_by(Zimmer._recid).all():
        anz0 = anz0 + 1

    return generate_output()