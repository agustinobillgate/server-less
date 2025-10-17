#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
print("--> Masuk ke fo_parxls_gs_1bl")
from models import Segmentstat, Arrangement, Res_line, Bill_line, Zimmer, Zinrstat, Zkstat, H_umsatz, Segment, Genstat, Uebertrag, Artikel, H_artikel, Wgrpdep, Umsatz, Budget, Htparam, Exrate, H_cost, H_journal, Reservation, Zimkateg, Guest, H_bill_line, H_bill, Bill, Queasy, Gl_acct, Waehrung, L_lager, L_artikel, L_op, H_compli, Fbstat, Sources, Paramtext, Parameters

import os
import subprocess
import shutil


w1_data, W1 = create_model("W1", {"nr":int, "varname":string, "main_code":int, "s_artnr":string, "artnr":int, "dept":int, "grpflag":int, "done":bool, "bezeich":string, "int_flag":bool, "tday":Decimal, "tday_serv":Decimal, "tday_tax":Decimal, "mtd_serv":Decimal, "mtd_tax":Decimal, "ytd_serv":Decimal, "ytd_tax":Decimal, "yesterday":Decimal, "saldo":Decimal, "lastmon":Decimal, "pmtd_serv":Decimal, "pmtd_tax":Decimal, "lmtd_serv":Decimal, "lmtd_tax":Decimal, "lastyr":Decimal, "lytoday":Decimal, "ytd_saldo":Decimal, "lytd_saldo":Decimal, "year_saldo":[Decimal,12], "mon_saldo":[Decimal,31], "mon_budget":[Decimal,31], "mon_lmtd":[Decimal,31], "tbudget":Decimal, "budget":Decimal, "lm_budget":Decimal, "lm_today":Decimal, "lm_today_serv":Decimal, "lm_today_tax":Decimal, "lm_mtd":Decimal, "lm_ytd":Decimal, "ly_budget":Decimal, "ny_budget":Decimal, "ytd_budget":Decimal, "nytd_budget":Decimal, "nmtd_budget":Decimal, "lytd_budget":Decimal, "lytd_serv":Decimal, "lytd_tax":Decimal, "lytoday_serv":Decimal, "lytoday_tax":Decimal, "month_budget":Decimal, "year_budget":Decimal, "tischnr":int, "mon_serv":[Decimal,31], "mon_tax":[Decimal,31]})
w2_data, W2 = create_model("W2", {"val_sign":int, "nr1":int, "nr2":int}, {"val_sign": 1})

def fo_parxls_gs_1bl(pvilanguage:int, ytd_flag:bool, jan1:date, ljan1:date, lfrom_date:date, lto_date:date, pfrom_date:date, pto_date:date, from_date:date, to_date:date, start_date:date, lytd_flag:bool, lmtd_flag:bool, pmtd_flag:bool, lytoday_flag:bool, lytoday:date, foreign_flag:bool, budget_flag:bool, foreign_nr:int, price_decimal:int, briefnr:int, link:string, budget_all:bool, user_init:string, w1_data:[W1], w2_data:[W2]):

   

    def generate_output():
       

        return {"msg_str": "OK"}

    

    return generate_output()