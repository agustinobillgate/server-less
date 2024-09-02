from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Parameters, Brief, Htparam, Waehrung, Zimmer, Briefzei

def prepare_fo_parxlsbl(pvilanguage:int, briefnr:int):
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
    htv_list_list = []
    htp_list_list = []
    brief_list_list = []
    t_brief_list = []
    t_parameters_list = []
    lvcarea:str = "prepare_fo_parxls"
    parameters = brief = htparam = waehrung = zimmer = briefzei = None

    htv_list = htp_list = brief_list = t_parameters = t_brief = None

    htv_list_list, Htv_list = create_model("Htv_list", {"paramnr":int, "fchar":str})
    htp_list_list, Htp_list = create_model("Htp_list", {"paramnr":int, "fchar":str})
    brief_list_list, Brief_list = create_model("Brief_list", {"b_text":str})
    t_parameters_list, T_parameters = create_model_like(Parameters)
    t_brief_list, T_brief = create_model_like(Brief)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal xls_dir, msg_str, serv_vat, foreign_nr, start_date, price_decimal, no_decimal, keycmd, keyvar, outfile_dir, anz0, htv_list_list, htp_list_list, brief_list_list, t_brief_list, t_parameters_list, lvcarea, parameters, brief, htparam, waehrung, zimmer, briefzei


        nonlocal htv_list, htp_list, brief_list, t_parameters, t_brief
        nonlocal htv_list_list, htp_list_list, brief_list_list, t_parameters_list, t_brief_list
        return {"xls_dir": xls_dir, "msg_str": msg_str, "serv_vat": serv_vat, "foreign_nr": foreign_nr, "start_date": start_date, "price_decimal": price_decimal, "no_decimal": no_decimal, "keycmd": keycmd, "keyvar": keyvar, "outfile_dir": outfile_dir, "anz0": anz0, "htv-list": htv_list_list, "htp-list": htp_list_list, "brief-list": brief_list_list, "t-brief": t_brief_list, "t-parameters": t_parameters_list}

    def fill_list():

        nonlocal xls_dir, msg_str, serv_vat, foreign_nr, start_date, price_decimal, no_decimal, keycmd, keyvar, outfile_dir, anz0, htv_list_list, htp_list_list, brief_list_list, t_brief_list, t_parameters_list, lvcarea, parameters, brief, htparam, waehrung, zimmer, briefzei


        nonlocal htv_list, htp_list, brief_list, t_parameters, t_brief
        nonlocal htv_list_list, htp_list_list, brief_list_list, t_parameters_list, t_brief_list

        i:int = 0
        j:int = 0
        n:int = 0
        l:int = 0
        continued:bool = False
        c:str = ""
        ct:str = ""

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 600)).first()
        keycmd = htparam.fchar

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 2030)).first()
        keyvar = htparam.fchar

        for htparam in db_session.query(Htparam).filter(
                (Htparam.paramgruppe == 8) &  (Htparam.fchar != "")).all():

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

        htv_list.paramnr = 9200
        htv_list.fchar = ".lytd_serv"


        htv_list = Htv_list()
        htv_list_list.append(htv_list)

        htv_list.paramnr = 9201
        htv_list.fchar = ".lytd_tax"


        htv_list = Htv_list()
        htv_list_list.append(htv_list)

        htv_list.paramnr = 9202
        htv_list.fchar = ".lytoday_serv"


        htv_list = Htv_list()
        htv_list_list.append(htv_list)

        htv_list.paramnr = 9203
        htv_list.fchar = ".lytoday_tax"


        htv_list = Htv_list()
        htv_list_list.append(htv_list)

        htv_list.paramnr = 9204
        htv_list.fchar = ".month_budget"


        htv_list = Htv_list()
        htv_list_list.append(htv_list)

        htv_list.paramnr = 9205
        htv_list.fchar = ".year_budget"


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

        htp_list.paramnr = 2020
        htp_list.fchar = keycmd + "FP_Cover1"


        htp_list = Htp_list()
        htp_list_list.append(htp_list)

        htp_list.paramnr = 2021
        htp_list.fchar = keycmd + "FP_Cover2"


        htp_list = Htp_list()
        htp_list_list.append(htp_list)

        htp_list.paramnr = 2022
        htp_list.fchar = keycmd + "FP_Cover3"


        htp_list = Htp_list()
        htp_list_list.append(htp_list)

        htp_list.paramnr = 2023
        htp_list.fchar = keycmd + "FP_Cover4"


        htp_list = Htp_list()
        htp_list_list.append(htp_list)

        htp_list.paramnr = 2024
        htp_list.fchar = keycmd + "BP_Cover1"


        htp_list = Htp_list()
        htp_list_list.append(htp_list)

        htp_list.paramnr = 2025
        htp_list.fchar = keycmd + "BP_Cover2"


        htp_list = Htp_list()
        htp_list_list.append(htp_list)

        htp_list.paramnr = 2026
        htp_list.fchar = keycmd + "BP_Cover3"


        htp_list = Htp_list()
        htp_list_list.append(htp_list)

        htp_list.paramnr = 2027
        htp_list.fchar = keycmd + "BP_Cover4"


        htp_list = Htp_list()
        htp_list_list.append(htp_list)

        htp_list.paramnr = 2028
        htp_list.fchar = keycmd + "G_Cover"


        htp_list = Htp_list()
        htp_list_list.append(htp_list)

        htp_list.paramnr = 2029
        htp_list.fchar = keycmd + "TOT_BILL"


        htp_list = Htp_list()
        htp_list_list.append(htp_list)

        htp_list.paramnr = 2031
        htp_list.fchar = keycmd + "PAX_TABLE"


        htp_list = Htp_list()
        htp_list_list.append(htp_list)

        htp_list.paramnr = 2032
        htp_list.fchar = keycmd + "PC_Cover1"


        htp_list = Htp_list()
        htp_list_list.append(htp_list)

        htp_list.paramnr = 2033
        htp_list.fchar = keycmd + "PC_Cover2"


        htp_list = Htp_list()
        htp_list_list.append(htp_list)

        htp_list.paramnr = 2034
        htp_list.fchar = keycmd + "PC_Cover3"


        htp_list = Htp_list()
        htp_list_list.append(htp_list)

        htp_list.paramnr = 2035
        htp_list.fchar = keycmd + "PC_Cover4"


        htp_list = Htp_list()
        htp_list_list.append(htp_list)

        htp_list.paramnr = 2036
        htp_list.fchar = keycmd + "PO_Cover1"


        htp_list = Htp_list()
        htp_list_list.append(htp_list)

        htp_list.paramnr = 2037
        htp_list.fchar = keycmd + "PO_Cover2"


        htp_list = Htp_list()
        htp_list_list.append(htp_list)

        htp_list.paramnr = 2038
        htp_list.fchar = keycmd + "PO_Cover3"


        htp_list = Htp_list()
        htp_list_list.append(htp_list)

        htp_list.paramnr = 2039
        htp_list.fchar = keycmd + "PO_Cover4"


        htp_list = Htp_list()
        htp_list_list.append(htp_list)

        htp_list.paramnr = 2040
        htp_list.fchar = keycmd + "PCO_Cover1"


        htp_list = Htp_list()
        htp_list_list.append(htp_list)

        htp_list.paramnr = 2041
        htp_list.fchar = keycmd + "PCO_Cover2"


        htp_list = Htp_list()
        htp_list_list.append(htp_list)

        htp_list.paramnr = 2042
        htp_list.fchar = keycmd + "PCO_Cover3"


        htp_list = Htp_list()
        htp_list_list.append(htp_list)

        htp_list.paramnr = 2043
        htp_list.fchar = keycmd + "PCO_Cover4"


        htp_list = Htp_list()
        htp_list_list.append(htp_list)

        htp_list.paramnr = 2044
        htp_list.fchar = keycmd + "Rev_Inhouse1"


        htp_list = Htp_list()
        htp_list_list.append(htp_list)

        htp_list.paramnr = 2045
        htp_list.fchar = keycmd + "Rev_Inhouse2"


        htp_list = Htp_list()
        htp_list_list.append(htp_list)

        htp_list.paramnr = 2046
        htp_list.fchar = keycmd + "Rev_Inhouse3"


        htp_list = Htp_list()
        htp_list_list.append(htp_list)

        htp_list.paramnr = 2047
        htp_list.fchar = keycmd + "Rev_Inhouse4"


        htp_list = Htp_list()
        htp_list_list.append(htp_list)

        htp_list.paramnr = 2048
        htp_list.fchar = keycmd + "Rev_Outsider1"


        htp_list = Htp_list()
        htp_list_list.append(htp_list)

        htp_list.paramnr = 2049
        htp_list.fchar = keycmd + "Rev_Outsider2"


        htp_list = Htp_list()
        htp_list_list.append(htp_list)

        htp_list.paramnr = 2050
        htp_list.fchar = keycmd + "Rev_Outsider3"


        htp_list = Htp_list()
        htp_list_list.append(htp_list)

        htp_list.paramnr = 2051
        htp_list.fchar = keycmd + "Rev_Outsider4"


        htp_list = Htp_list()
        htp_list_list.append(htp_list)

        htp_list.paramnr = 2052
        htp_list.fchar = keycmd + "Pax"


        htp_list = Htp_list()
        htp_list_list.append(htp_list)

        htp_list.paramnr = 9106
        htp_list.fchar = keycmd + "WIG"


        htp_list = Htp_list()
        htp_list_list.append(htp_list)

        htp_list.paramnr = 7194
        htp_list.fchar = keycmd + "Canc_night"


        htp_list = Htp_list()
        htp_list_list.append(htp_list)

        htp_list.paramnr = 7195
        htp_list.fchar = keycmd + "canc_cidate"


        htp_list = Htp_list()
        htp_list_list.append(htp_list)

        htp_list.paramnr = 7196
        htp_list.fchar = keycmd + "canc_cidate_nite"


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

        htp_list.paramnr = 9180
        htp_list.fchar = keycmd + "statRoom"


        htp_list = Htp_list()
        htp_list_list.append(htp_list)

        htp_list.paramnr = 8180
        htp_list.fchar = keycmd + "rComp"


        htp_list = Htp_list()
        htp_list_list.append(htp_list)

        htp_list.paramnr = 9000
        htp_list.fchar = keycmd + "LOS"


        htp_list = Htp_list()
        htp_list_list.append(htp_list)

        htp_list.paramnr = 9001
        htp_list.fchar = keycmd + "CountryRev"


        htp_list = Htp_list()
        htp_list_list.append(htp_list)

        htp_list.paramnr = 9002
        htp_list.fchar = keycmd + "CountryRoom"


        htp_list = Htp_list()
        htp_list_list.append(htp_list)

        htp_list.paramnr = 9003
        htp_list.fchar = keycmd + "RcRev"


        htp_list = Htp_list()
        htp_list_list.append(htp_list)

        htp_list.paramnr = 9004
        htp_list.fchar = keycmd + "RcRoom"


        htp_list = Htp_list()
        htp_list_list.append(htp_list)

        htp_list.paramnr = 9005
        htp_list.fchar = keycmd + "RcSegRev"


        htp_list = Htp_list()
        htp_list_list.append(htp_list)

        htp_list.paramnr = 9006
        htp_list.fchar = keycmd + "RcSegRoom"


        htp_list = Htp_list()
        htp_list_list.append(htp_list)

        htp_list.paramnr = 9007
        htp_list.fchar = keycmd + "SEGMREV_OTH"


        htp_list = Htp_list()
        htp_list_list.append(htp_list)

        htp_list.paramnr = 9008
        htp_list.fchar = keycmd + "comp_bonus"


        htp_list = Htp_list()
        htp_list_list.append(htp_list)

        htp_list.paramnr = 2001
        htp_list.fchar = keycmd + "PI_Cover1"


        htp_list = Htp_list()
        htp_list_list.append(htp_list)

        htp_list.paramnr = 2002
        htp_list.fchar = keycmd + "PI_Cover2"


        htp_list = Htp_list()
        htp_list_list.append(htp_list)

        htp_list.paramnr = 2003
        htp_list.fchar = keycmd + "PI_Cover3"


        htp_list = Htp_list()
        htp_list_list.append(htp_list)

        htp_list.paramnr = 2004
        htp_list.fchar = keycmd + "PI_Cover4"


        htp_list = Htp_list()
        htp_list_list.append(htp_list)

        htp_list.paramnr = 2005
        htp_list.fchar = keycmd + "PN_Cover1"


        htp_list = Htp_list()
        htp_list_list.append(htp_list)

        htp_list.paramnr = 2006
        htp_list.fchar = keycmd + "PN_Cover2"


        htp_list = Htp_list()
        htp_list_list.append(htp_list)

        htp_list.paramnr = 2007
        htp_list.fchar = keycmd + "PN_Cover3"


        htp_list = Htp_list()
        htp_list_list.append(htp_list)

        htp_list.paramnr = 2008
        htp_list.fchar = keycmd + "PN_Cover4"


        htp_list = Htp_list()
        htp_list_list.append(htp_list)

        htp_list.paramnr = 2009
        htp_list.fchar = keycmd + "PH_Cover1"


        htp_list = Htp_list()
        htp_list_list.append(htp_list)

        htp_list.paramnr = 2010
        htp_list.fchar = keycmd + "PH_Cover2"


        htp_list = Htp_list()
        htp_list_list.append(htp_list)

        htp_list.paramnr = 2011
        htp_list.fchar = keycmd + "PH_Cover3"


        htp_list = Htp_list()
        htp_list_list.append(htp_list)

        htp_list.paramnr = 2012
        htp_list.fchar = keycmd + "PH_Cover4"


        htp_list = Htp_list()
        htp_list_list.append(htp_list)

        htp_list.paramnr = 2013
        htp_list.fchar = keycmd + "PW_Cover1"


        htp_list = Htp_list()
        htp_list_list.append(htp_list)

        htp_list.paramnr = 2014
        htp_list.fchar = keycmd + "PW_Cover2"


        htp_list = Htp_list()
        htp_list_list.append(htp_list)

        htp_list.paramnr = 2015
        htp_list.fchar = keycmd + "PW_Cover3"


        htp_list = Htp_list()
        htp_list_list.append(htp_list)

        htp_list.paramnr = 2016
        htp_list.fchar = keycmd + "PW_Cover4"


        htp_list = Htp_list()
        htp_list_list.append(htp_list)

        htp_list.paramnr = 9051
        htp_list.fchar = keycmd + "sameday_res"


        htp_list = Htp_list()
        htp_list_list.append(htp_list)

        htp_list.paramnr = 9052
        htp_list.fchar = keycmd + "grp_arr"


        htp_list = Htp_list()
        htp_list_list.append(htp_list)

        htp_list.paramnr = 9053
        htp_list.fchar = keycmd + "grp_dep"


        htp_list = Htp_list()
        htp_list_list.append(htp_list)

        htp_list.paramnr = 9054
        htp_list.fchar = keycmd + "grp_room"


        htp_list = Htp_list()
        htp_list_list.append(htp_list)

        htp_list.paramnr = 9055
        htp_list.fchar = keycmd + "indv_room"


        for n in range(1,31 + 1) :
            htv_list = Htv_list()
            htv_list_list.append(htv_list)

            htv_list.paramnr = 3000 + n
            htv_list.fchar = ".D" + to_string(n, "99")


        htp_list = Htp_list()
        htp_list_list.append(htp_list)

        htp_list.paramnr = 9009
        htp_list.fchar = keycmd + "rmrev"


        htp_list = Htp_list()
        htp_list_list.append(htp_list)

        htp_list.paramnr = 9010
        htp_list.fchar = keycmd + "rmnight"


        htp_list = Htp_list()
        htp_list_list.append(htp_list)

        htp_list.paramnr = 9011
        htp_list.fchar = keycmd + "lyrmrev"


        htp_list = Htp_list()
        htp_list_list.append(htp_list)

        htp_list.paramnr = 9012
        htp_list.fchar = keycmd + "lyrmnight"


        htp_list = Htp_list()
        htp_list_list.append(htp_list)

        htp_list.paramnr = 9013
        htp_list.fchar = keycmd + "rmrev_sob"


        htp_list = Htp_list()
        htp_list_list.append(htp_list)

        htp_list.paramnr = 9014
        htp_list.fchar = keycmd + "rmnight_sob"


        htp_list = Htp_list()
        htp_list_list.append(htp_list)

        htp_list.paramnr = 9015
        htp_list.fchar = keycmd + "lyrmrev_sob"


        htp_list = Htp_list()
        htp_list_list.append(htp_list)

        htp_list.paramnr = 9016
        htp_list.fchar = keycmd + "lyrmnight_sob"


        htp_list = Htp_list()
        htp_list_list.append(htp_list)

        htp_list.paramnr = 9017
        htp_list.fchar = keycmd + "rmrev_segm"


        htp_list = Htp_list()
        htp_list_list.append(htp_list)

        htp_list.paramnr = 9018
        htp_list.fchar = keycmd + "rmnight_segm"


        htp_list = Htp_list()
        htp_list_list.append(htp_list)

        htp_list.paramnr = 9019
        htp_list.fchar = keycmd + "lyrmrev_segm"


        htp_list = Htp_list()
        htp_list_list.append(htp_list)

        htp_list.paramnr = 9020
        htp_list.fchar = keycmd + "lyrmnight_segm"


        htp_list = Htp_list()
        htp_list_list.append(htp_list)

        htp_list.paramnr = 9021
        htp_list.fchar = keycmd + "rmrev_compt"


        htp_list = Htp_list()
        htp_list_list.append(htp_list)

        htp_list.paramnr = 9022
        htp_list.fchar = keycmd + "rmocc_compt"


        htp_list = Htp_list()
        htp_list_list.append(htp_list)

        htp_list.paramnr = 9023
        htp_list.fchar = keycmd + "revbud_segm"


        htp_list = Htp_list()
        htp_list_list.append(htp_list)

        htp_list.paramnr = 9024
        htp_list.fchar = keycmd + "nightbud_segm"


        htp_list = Htp_list()
        htp_list_list.append(htp_list)

        htp_list.paramnr = 9025
        htp_list.fchar = keycmd + "lyrevbud_segm"


        htp_list = Htp_list()
        htp_list_list.append(htp_list)

        htp_list.paramnr = 9026
        htp_list.fchar = keycmd + "lynightbud_segm"


        htp_list = Htp_list()
        htp_list_list.append(htp_list)

        htp_list.paramnr = 829
        htp_list.fchar = keycmd + "INCL_BUDGET_ALL"


        for n in range(1,12 + 1) :
            htv_list = Htv_list()
            htv_list_list.append(htv_list)

            htv_list.paramnr = 4000 + n
            htv_list.fchar = ".M" + to_string(n, "99")

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

    for parameters in db_session.query(Parameters).filter(
            (func.lower(Parameters.progname) == "FO_macro") &  (Parameters.SECTION == to_string(briefnr))).all():
        t_parameters = T_parameters()
        t_parameters_list.append(t_parameters)

        buffer_copy(parameters, t_parameters)

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 418)).first()

    if htparam.fchar == "":
        msg_str = msg_str + chr(2) + translateExtended ("Excel Output Directory not defined (Param 418 Grp 15)", lvcarea, "")

        return generate_output()
    xls_dir = htparam.fchar

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 479)).first()
    serv_vat = htparam.flogical

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 144)).first()

    if htparam.fchar != "":

        waehrung = db_session.query(Waehrung).filter(
                (Waehrung.wabkurz == htparam.fchar)).first()

        if waehrung:
            foreign_nr = waehrungsnr

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 186)).first()

    if htparam.feldtyp == 3 and htparam.fdate != None:
        start_date = htparam.fdate

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 491)).first()
    price_decimal = htparam.finteger
    no_decimal = (price_decimal == 0)
    fill_list()

    brief = db_session.query(Brief).filter(
            (briefnr == briefnr)).first()
    t_brief = T_brief()
    t_brief_list.append(t_brief)

    buffer_copy(brief, t_brief)

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 64)).first()
    outfile_dir = htparam.fchar

    for zimmer in db_session.query(Zimmer).all():
        anz0 = anz0 + 1

    return generate_output()