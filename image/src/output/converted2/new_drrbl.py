from functions.additional_functions import *
import decimal
from datetime import date
from functions.calc_servtaxesbl import calc_servtaxesbl
from sqlalchemy import func
from models import Umsatz, Waehrung, Htparam, Queasy, Segment, Artikel, Hoteldpt, Uebertrag, Exrate, Genstat, Segmentstat, Budget, Zinrstat, Zkstat

def new_drrbl(from_date:date, to_date:date):
    rev_seg_list_list = []
    rev_list_list = []
    payable_list_list = []
    stat_list_list = []
    payment_list_list = []
    gl_list_list = []
    fb_sales_food_list = []
    fb_sales_beverage_list = []
    fb_sales_other_list = []
    fb_sales_tot_list = []
    rev_seg_list1_list = []
    fb_sales_material_list = []
    gsheet_link = ""
    ytd_flag:bool = True
    str1:str = ""
    str2:str = ""
    str3:str = ""
    st1:str = ""
    st2:str = ""
    st3:str = ""
    st4:str = ""
    st5:str = ""
    st6:str = ""
    st7:str = ""
    st8:str = ""
    st9:str = ""
    st10:str = ""
    st11:str = ""
    st12:str = ""
    st13:str = ""
    st14:str = ""
    st15:str = ""
    st16:str = ""
    st17:str = ""
    st18:str = ""
    st19:str = ""
    st20:str = ""
    st21:str = ""
    st22:str = ""
    st23:str = ""
    st24:str = ""
    st25:str = ""
    st26:str = ""
    st27:str = ""
    st28:str = ""
    st29:str = ""
    st30:str = ""
    st31:str = ""
    st32:str = ""
    st33:str = ""
    st34:str = ""
    st35:str = ""
    st36:str = ""
    st37:str = ""
    n:int = 0
    n1:int = 0
    n2:int = 0
    n3:int = 0
    n4:int = 0
    n5:int = 0
    n6:int = 0
    n7:int = 0
    n8:int = 0
    n9:int = 0
    n10:int = 0
    n11:int = 0
    n12:int = 0
    n13:int = 0
    n14:int = 0
    n15:int = 0
    n16:int = 0
    n17:int = 0
    n18:int = 0
    n19:int = 0
    n20:int = 0
    n21:int = 0
    n22:int = 0
    n23:int = 0
    n24:int = 0
    n25:int = 0
    n26:int = 0
    n27:int = 0
    n28:int = 0
    n29:int = 0
    n30:int = 0
    curr_date:date = None
    start_date:date = None
    datum1:date = None
    serv:decimal = to_decimal("0.0")
    vat:decimal = to_decimal("0.0")
    vat2:decimal = to_decimal("0.0")
    fact:decimal = to_decimal("0.0")
    n_betrag:decimal = to_decimal("0.0")
    n_serv:decimal = to_decimal("0.0")
    n_tax:decimal = to_decimal("0.0")
    ly_betrag:decimal = to_decimal("0.0")
    d_flag:bool = False
    dbudget_flag:bool = False
    dlmtd_flag:bool = False
    yes_serv:decimal = to_decimal("0.0")
    yes_vat:decimal = to_decimal("0.0")
    yes_vat2:decimal = to_decimal("0.0")
    yes_fact:decimal = to_decimal("0.0")
    yes_betrag:decimal = to_decimal("0.0")
    date1:date = None
    date2:date = None
    temp_date2:date = None
    temp_curr_date:date = None
    l_today:int = 0
    st_date:int = 0
    foreign_nr:int = 0
    foreign_flag:bool = True
    tot_betrag:decimal = to_decimal("0.0")
    price_decimal:int = 0
    no_decimal:bool = False
    dept:int = 0
    dept1:int = 0
    zwkum:int = 0
    dper:int = 0
    mtd_per:int = 0
    ytd_per:int = 0
    tot_today:decimal = to_decimal("0.0")
    tot_today_per:decimal = to_decimal("0.0")
    tot_mtd:decimal = to_decimal("0.0")
    tot_mtd_per:decimal = to_decimal("0.0")
    tot_mtd_budget:decimal = to_decimal("0.0")
    tot_variance:decimal = to_decimal("0.0")
    tot_ytd:decimal = to_decimal("0.0")
    tot_ytd_budget:decimal = to_decimal("0.0")
    tot_ytd_per:decimal = to_decimal("0.0")
    tot_today1:decimal = to_decimal("0.0")
    tot_today_per1:decimal = to_decimal("0.0")
    tot_mtd1:decimal = to_decimal("0.0")
    tot_mtd_per1:decimal = to_decimal("0.0")
    tot_mtd_budget1:decimal = to_decimal("0.0")
    tot_variance1:decimal = to_decimal("0.0")
    tot_ytd1:decimal = to_decimal("0.0")
    tot_ytd_budget1:decimal = to_decimal("0.0")
    tot_ytd_per1:decimal = to_decimal("0.0")
    tot_today2:decimal = to_decimal("0.0")
    tot_today_per2:decimal = to_decimal("0.0")
    tot_mtd2:decimal = to_decimal("0.0")
    tot_mtd_per2:decimal = to_decimal("0.0")
    tot_mtd_budget2:decimal = to_decimal("0.0")
    tot_variance2:decimal = to_decimal("0.0")
    tot_ytd2:decimal = to_decimal("0.0")
    tot_ytd_budget2:decimal = to_decimal("0.0")
    tot_ytd_per2:decimal = to_decimal("0.0")
    tot_today3:decimal = to_decimal("0.0")
    tot_mtd3:decimal = to_decimal("0.0")
    tot_mtd_budget3:decimal = to_decimal("0.0")
    tot_variance3:decimal = to_decimal("0.0")
    tot_ytd3:decimal = to_decimal("0.0")
    tot_ytd_budget3:decimal = to_decimal("0.0")
    tot_today4:decimal = to_decimal("0.0")
    tot_mtd4:decimal = to_decimal("0.0")
    tot_mtd_budget4:decimal = to_decimal("0.0")
    tot_variance4:decimal = to_decimal("0.0")
    tot_ytd4:decimal = to_decimal("0.0")
    tot_ytd_budget4:decimal = to_decimal("0.0")
    tot_today5:decimal = to_decimal("0.0")
    tot_mtd5:decimal = to_decimal("0.0")
    tot_mtd_budget5:decimal = to_decimal("0.0")
    tot_variance5:decimal = to_decimal("0.0")
    tot_ytd5:decimal = to_decimal("0.0")
    tot_ytd_budget5:decimal = to_decimal("0.0")
    tot_today6:decimal = to_decimal("0.0")
    tot_mtd6:decimal = to_decimal("0.0")
    tot_mtd_budget6:decimal = to_decimal("0.0")
    tot_variance6:decimal = to_decimal("0.0")
    tot_ytd6:decimal = to_decimal("0.0")
    tot_ytd_budget6:decimal = to_decimal("0.0")
    tot_today7:decimal = to_decimal("0.0")
    tot_mtd7:decimal = to_decimal("0.0")
    tot_mtd_budget7:decimal = to_decimal("0.0")
    tot_variance7:decimal = to_decimal("0.0")
    tot_ytd7:decimal = to_decimal("0.0")
    tot_ytd_budget7:decimal = to_decimal("0.0")
    tot_tday_cov:decimal = to_decimal("0.0")
    tot_tday_avg:decimal = to_decimal("0.0")
    tot_tday_rev:decimal = to_decimal("0.0")
    tot_mtd_cov:decimal = to_decimal("0.0")
    tot_mtd_avg:decimal = to_decimal("0.0")
    tot_mtd_rev:decimal = to_decimal("0.0")
    tot_ytd_cov:decimal = to_decimal("0.0")
    tot_ytd_avg:decimal = to_decimal("0.0")
    tot_ytd_rev:decimal = to_decimal("0.0")
    t_today:decimal = to_decimal("0.0")
    t_today_per:decimal = to_decimal("0.0")
    t_mtd:decimal = to_decimal("0.0")
    t_mtd_per:decimal = to_decimal("0.0")
    t_mtd_budget:decimal = to_decimal("0.0")
    t_variance:decimal = to_decimal("0.0")
    t_ytd:decimal = to_decimal("0.0")
    t_ytd_budget:decimal = to_decimal("0.0")
    t_ytd_per:decimal = to_decimal("0.0")
    t_today1:decimal = to_decimal("0.0")
    t_today_per1:decimal = to_decimal("0.0")
    t_mtd1:decimal = to_decimal("0.0")
    t_mtd_per1:decimal = to_decimal("0.0")
    t_mtd_budget1:decimal = to_decimal("0.0")
    t_variance1:decimal = to_decimal("0.0")
    t_ytd1:decimal = to_decimal("0.0")
    t_ytd_budget1:decimal = to_decimal("0.0")
    t_ytd_per1:decimal = to_decimal("0.0")
    t_today11:decimal = to_decimal("0.0")
    t_today_per11:decimal = to_decimal("0.0")
    t_mtd11:decimal = to_decimal("0.0")
    t_mtd_per11:decimal = to_decimal("0.0")
    t_mtd_budget11:decimal = to_decimal("0.0")
    t_variance11:decimal = to_decimal("0.0")
    t_ytd11:decimal = to_decimal("0.0")
    t_ytd_budget11:decimal = to_decimal("0.0")
    t_ytd_per11:decimal = to_decimal("0.0")
    t_today2:decimal = to_decimal("0.0")
    t_today_per2:decimal = to_decimal("0.0")
    t_mtd2:decimal = to_decimal("0.0")
    t_mtd_per2:decimal = to_decimal("0.0")
    t_mtd_budget2:decimal = to_decimal("0.0")
    t_variance2:decimal = to_decimal("0.0")
    t_ytd2:decimal = to_decimal("0.0")
    t_ytd_budget2:decimal = to_decimal("0.0")
    t_ytd_per2:decimal = to_decimal("0.0")
    t_today3:decimal = to_decimal("0.0")
    t_today_per3:decimal = to_decimal("0.0")
    t_mtd3:decimal = to_decimal("0.0")
    t_mtd_per3:decimal = to_decimal("0.0")
    t_mtd_budget3:decimal = to_decimal("0.0")
    t_variance3:decimal = to_decimal("0.0")
    t_ytd3:decimal = to_decimal("0.0")
    t_ytd_budget3:decimal = to_decimal("0.0")
    t_ytd_per3:decimal = to_decimal("0.0")
    tdy_gl1:decimal = to_decimal("0.0")
    ytd_gl:decimal = to_decimal("0.0")
    curr_flag:str = ""
    curr_dept:int = 0
    ct:int = 0
    ct3:int = 0
    ct4:int = 0
    t_day_serv:decimal = to_decimal("0.0")
    mtd_serv:decimal = to_decimal("0.0")
    mtd_budget_serv:decimal = to_decimal("0.0")
    ytd_serv:decimal = to_decimal("0.0")
    ytd_budget_serv:decimal = to_decimal("0.0")
    variance_serv:decimal = to_decimal("0.0")
    t_day_tax:decimal = to_decimal("0.0")
    mtd_tax:decimal = to_decimal("0.0")
    mtd_budget_tax:decimal = to_decimal("0.0")
    ytd_tax:decimal = to_decimal("0.0")
    ytd_budget_tax:decimal = to_decimal("0.0")
    variance_tax:decimal = to_decimal("0.0")
    ct1:int = 0
    curr_flag1:str = ""
    ct2:int = 0
    banq_dept:int = 0
    frate:decimal = 1
    jan1:date = None
    budget_flag:bool = False
    mon_saldo:List[decimal] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    mon_budget:List[decimal] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    foreign_curr:decimal = to_decimal("0.0")
    umsatz = waehrung = htparam = queasy = segment = artikel = hoteldpt = uebertrag = exrate = genstat = segmentstat = budget = zinrstat = zkstat = None

    rev_seg_list = rev_seg_list1 = rev_list = rev_list_tax = rev_list_serv = payable_list = tot_list = stat_list = payment_list = segment_list = gl_list = fb_sales_food = fb_sales_beverage = fb_sales_other = fb_sales_tot = fb_sales_material = setup_revenue = setup_segment = setup_payment = setup_stat = setup_fbcover = buff_umsatz = b_rev_list = b_rev_seg_list = b_rev_seg_list1 = b_stat_list = brev_list = b_payment_list = bpayment_list = bpayable_list = None

    rev_seg_list_list, Rev_seg_list = create_model("Rev_seg_list", {"ct":int, "segment_code":int, "descr":str, "departement":int, "t_day":decimal, "dper":decimal, "mtd":decimal, "mtd_per":decimal, "mtd_budget":decimal, "variance":decimal, "ytd":decimal, "ytd_budget":decimal, "ytd_per":decimal, "flag":str, "flag_grup":bool})
    rev_seg_list1_list, Rev_seg_list1 = create_model_like(Rev_seg_list)
    rev_list_list, Rev_list = create_model("Rev_list", {"ct":int, "descr":str, "departement":int, "t_day":decimal, "dper":decimal, "mtd":decimal, "mtd_per":decimal, "mtd_budget":decimal, "variance":decimal, "ytd":decimal, "ytd_budget":decimal, "ytd_per":decimal, "flag":str, "flag_grup":bool})
    rev_list_tax_list, Rev_list_tax = create_model_like(Rev_list)
    rev_list_serv_list, Rev_list_serv = create_model_like(Rev_list)
    payable_list_list, Payable_list = create_model_like(Rev_list)
    tot_list_list, Tot_list = create_model_like(Rev_list)
    stat_list_list, Stat_list = create_model("Stat_list", {"ct":int, "descr":str, "departement":int, "t_day":decimal, "mtd":decimal, "mtd_budget":decimal, "variance":decimal, "ytd":decimal, "ytd_budget":decimal, "flag":str})
    payment_list_list, Payment_list = create_model_like(Stat_list)
    segment_list_list, Segment_list = create_model("Segment_list", {"segmentcode":int, "bezeich":str})
    gl_list_list, Gl_list = create_model("Gl_list", {"descr":str, "tot_rev":decimal})
    fb_sales_food_list, Fb_sales_food = create_model("Fb_sales_food", {"ct":int, "artnr":int, "departement":int, "descr":str, "tday_cov":decimal, "tday_avg":decimal, "tday_rev":decimal, "mtd_cov":decimal, "mtd_avg":decimal, "mtd_rev":decimal, "ytd_cov":decimal, "ytd_avg":decimal, "ytd_rev":decimal, "flag":str})
    fb_sales_beverage_list, Fb_sales_beverage = create_model_like(Fb_sales_food)
    fb_sales_other_list, Fb_sales_other = create_model_like(Fb_sales_food)
    fb_sales_tot_list, Fb_sales_tot = create_model_like(Fb_sales_food)
    fb_sales_material_list, Fb_sales_material = create_model_like(Fb_sales_food)
    setup_revenue_list, Setup_revenue = create_model("Setup_revenue", {"artnr":int, "flag_used":bool, "flag_grup":bool, "descr":str, "departement":int, "flag":str}, {"flag_used": True})
    setup_segment_list, Setup_segment = create_model_like(Setup_revenue)
    setup_payment_list, Setup_payment = create_model("Setup_payment", {"artnr":int, "artart":int, "umsatzart":int, "departement":int, "flag":bool})
    setup_stat_list, Setup_stat = create_model("Setup_stat", {"zwkum":int, "artnr":int, "flag":str, "descr":str})
    setup_fbcover_list, Setup_fbcover = create_model("Setup_fbcover", {"departement":int, "artnr":int, "flag":str})

    Buff_umsatz = create_buffer("Buff_umsatz",Umsatz)
    B_rev_list = Rev_list
    b_rev_list_list = rev_list_list

    B_rev_seg_list = Rev_seg_list
    b_rev_seg_list_list = rev_seg_list_list

    B_rev_seg_list1 = Rev_seg_list1
    b_rev_seg_list1_list = rev_seg_list1_list

    B_stat_list = Stat_list
    b_stat_list_list = stat_list_list

    Brev_list = Rev_list
    brev_list_list = rev_list_list

    B_payment_list = Payment_list
    b_payment_list_list = payment_list_list

    Bpayment_list = Payment_list
    bpayment_list_list = payment_list_list

    Bpayable_list = Payable_list
    bpayable_list_list = payable_list_list


    db_session = local_storage.db_session

    def generate_output():
        nonlocal rev_seg_list_list, rev_list_list, payable_list_list, stat_list_list, payment_list_list, gl_list_list, fb_sales_food_list, fb_sales_beverage_list, fb_sales_other_list, fb_sales_tot_list, rev_seg_list1_list, fb_sales_material_list, gsheet_link, ytd_flag, str1, str2, str3, st1, st2, st3, st4, st5, st6, st7, st8, st9, st10, st11, st12, st13, st14, st15, st16, st17, st18, st19, st20, st21, st22, st23, st24, st25, st26, st27, st28, st29, st30, st31, st32, st33, st34, st35, st36, st37, n, n1, n2, n3, n4, n5, n6, n7, n8, n9, n10, n11, n12, n13, n14, n15, n16, n17, n18, n19, n20, n21, n22, n23, n24, n25, n26, n27, n28, n29, n30, curr_date, start_date, datum1, serv, vat, vat2, fact, n_betrag, n_serv, n_tax, ly_betrag, d_flag, dbudget_flag, dlmtd_flag, yes_serv, yes_vat, yes_vat2, yes_fact, yes_betrag, date1, date2, temp_date2, temp_curr_date, l_today, st_date, foreign_nr, foreign_flag, tot_betrag, price_decimal, no_decimal, dept, dept1, zwkum, dper, mtd_per, ytd_per, tot_today, tot_today_per, tot_mtd, tot_mtd_per, tot_mtd_budget, tot_variance, tot_ytd, tot_ytd_budget, tot_ytd_per, tot_today1, tot_today_per1, tot_mtd1, tot_mtd_per1, tot_mtd_budget1, tot_variance1, tot_ytd1, tot_ytd_budget1, tot_ytd_per1, tot_today2, tot_today_per2, tot_mtd2, tot_mtd_per2, tot_mtd_budget2, tot_variance2, tot_ytd2, tot_ytd_budget2, tot_ytd_per2, tot_today3, tot_mtd3, tot_mtd_budget3, tot_variance3, tot_ytd3, tot_ytd_budget3, tot_today4, tot_mtd4, tot_mtd_budget4, tot_variance4, tot_ytd4, tot_ytd_budget4, tot_today5, tot_mtd5, tot_mtd_budget5, tot_variance5, tot_ytd5, tot_ytd_budget5, tot_today6, tot_mtd6, tot_mtd_budget6, tot_variance6, tot_ytd6, tot_ytd_budget6, tot_today7, tot_mtd7, tot_mtd_budget7, tot_variance7, tot_ytd7, tot_ytd_budget7, tot_tday_cov, tot_tday_avg, tot_tday_rev, tot_mtd_cov, tot_mtd_avg, tot_mtd_rev, tot_ytd_cov, tot_ytd_avg, tot_ytd_rev, t_today, t_today_per, t_mtd, t_mtd_per, t_mtd_budget, t_variance, t_ytd, t_ytd_budget, t_ytd_per, t_today1, t_today_per1, t_mtd1, t_mtd_per1, t_mtd_budget1, t_variance1, t_ytd1, t_ytd_budget1, t_ytd_per1, t_today11, t_today_per11, t_mtd11, t_mtd_per11, t_mtd_budget11, t_variance11, t_ytd11, t_ytd_budget11, t_ytd_per11, t_today2, t_today_per2, t_mtd2, t_mtd_per2, t_mtd_budget2, t_variance2, t_ytd2, t_ytd_budget2, t_ytd_per2, t_today3, t_today_per3, t_mtd3, t_mtd_per3, t_mtd_budget3, t_variance3, t_ytd3, t_ytd_budget3, t_ytd_per3, tdy_gl1, ytd_gl, curr_flag, curr_dept, ct, ct3, ct4, t_day_serv, mtd_serv, mtd_budget_serv, ytd_serv, ytd_budget_serv, variance_serv, t_day_tax, mtd_tax, mtd_budget_tax, ytd_tax, ytd_budget_tax, variance_tax, ct1, curr_flag1, ct2, banq_dept, frate, jan1, budget_flag, mon_saldo, mon_budget, foreign_curr, umsatz, waehrung, htparam, queasy, segment, artikel, hoteldpt, uebertrag, exrate, genstat, segmentstat, budget, zinrstat, zkstat
        nonlocal from_date, to_date
        nonlocal buff_umsatz, b_rev_list, b_rev_seg_list, b_rev_seg_list1, b_stat_list, brev_list, b_payment_list, bpayment_list, bpayable_list


        nonlocal rev_seg_list, rev_seg_list1, rev_list, rev_list_tax, rev_list_serv, payable_list, tot_list, stat_list, payment_list, segment_list, gl_list, fb_sales_food, fb_sales_beverage, fb_sales_other, fb_sales_tot, fb_sales_material, setup_revenue, setup_segment, setup_payment, setup_stat, setup_fbcover, buff_umsatz, b_rev_list, b_rev_seg_list, b_rev_seg_list1, b_stat_list, brev_list, b_payment_list, bpayment_list, bpayable_list
        nonlocal rev_seg_list_list, rev_seg_list1_list, rev_list_list, rev_list_tax_list, rev_list_serv_list, payable_list_list, tot_list_list, stat_list_list, payment_list_list, segment_list_list, gl_list_list, fb_sales_food_list, fb_sales_beverage_list, fb_sales_other_list, fb_sales_tot_list, fb_sales_material_list, setup_revenue_list, setup_segment_list, setup_payment_list, setup_stat_list, setup_fbcover_list

        return {"rev-seg-list": rev_seg_list_list, "rev-list": rev_list_list, "payable-list": payable_list_list, "stat-list": stat_list_list, "payment-list": payment_list_list, "gl-list": gl_list_list, "fb-sales-food": fb_sales_food_list, "fb-sales-beverage": fb_sales_beverage_list, "fb-sales-other": fb_sales_other_list, "fb-sales-tot": fb_sales_tot_list, "rev-seg-list1": rev_seg_list1_list, "fb-sales-material": fb_sales_material_list, "gsheet_link": gsheet_link}

    def find_exrate(curr_date:date):

        nonlocal rev_seg_list_list, rev_list_list, payable_list_list, stat_list_list, payment_list_list, gl_list_list, fb_sales_food_list, fb_sales_beverage_list, fb_sales_other_list, fb_sales_tot_list, rev_seg_list1_list, fb_sales_material_list, gsheet_link, ytd_flag, str1, str2, str3, st1, st2, st3, st4, st5, st6, st7, st8, st9, st10, st11, st12, st13, st14, st15, st16, st17, st18, st19, st20, st21, st22, st23, st24, st25, st26, st27, st28, st29, st30, st31, st32, st33, st34, st35, st36, st37, n, n1, n2, n3, n4, n5, n6, n7, n8, n9, n10, n11, n12, n13, n14, n15, n16, n17, n18, n19, n20, n21, n22, n23, n24, n25, n26, n27, n28, n29, n30, start_date, datum1, serv, vat, vat2, fact, n_betrag, n_serv, n_tax, ly_betrag, d_flag, dbudget_flag, dlmtd_flag, yes_serv, yes_vat, yes_vat2, yes_fact, yes_betrag, date1, date2, temp_date2, temp_curr_date, l_today, st_date, foreign_nr, foreign_flag, tot_betrag, price_decimal, no_decimal, dept, dept1, zwkum, dper, mtd_per, ytd_per, tot_today, tot_today_per, tot_mtd, tot_mtd_per, tot_mtd_budget, tot_variance, tot_ytd, tot_ytd_budget, tot_ytd_per, tot_today1, tot_today_per1, tot_mtd1, tot_mtd_per1, tot_mtd_budget1, tot_variance1, tot_ytd1, tot_ytd_budget1, tot_ytd_per1, tot_today2, tot_today_per2, tot_mtd2, tot_mtd_per2, tot_mtd_budget2, tot_variance2, tot_ytd2, tot_ytd_budget2, tot_ytd_per2, tot_today3, tot_mtd3, tot_mtd_budget3, tot_variance3, tot_ytd3, tot_ytd_budget3, tot_today4, tot_mtd4, tot_mtd_budget4, tot_variance4, tot_ytd4, tot_ytd_budget4, tot_today5, tot_mtd5, tot_mtd_budget5, tot_variance5, tot_ytd5, tot_ytd_budget5, tot_today6, tot_mtd6, tot_mtd_budget6, tot_variance6, tot_ytd6, tot_ytd_budget6, tot_today7, tot_mtd7, tot_mtd_budget7, tot_variance7, tot_ytd7, tot_ytd_budget7, tot_tday_cov, tot_tday_avg, tot_tday_rev, tot_mtd_cov, tot_mtd_avg, tot_mtd_rev, tot_ytd_cov, tot_ytd_avg, tot_ytd_rev, t_today, t_today_per, t_mtd, t_mtd_per, t_mtd_budget, t_variance, t_ytd, t_ytd_budget, t_ytd_per, t_today1, t_today_per1, t_mtd1, t_mtd_per1, t_mtd_budget1, t_variance1, t_ytd1, t_ytd_budget1, t_ytd_per1, t_today11, t_today_per11, t_mtd11, t_mtd_per11, t_mtd_budget11, t_variance11, t_ytd11, t_ytd_budget11, t_ytd_per11, t_today2, t_today_per2, t_mtd2, t_mtd_per2, t_mtd_budget2, t_variance2, t_ytd2, t_ytd_budget2, t_ytd_per2, t_today3, t_today_per3, t_mtd3, t_mtd_per3, t_mtd_budget3, t_variance3, t_ytd3, t_ytd_budget3, t_ytd_per3, tdy_gl1, ytd_gl, curr_flag, curr_dept, ct, ct3, ct4, t_day_serv, mtd_serv, mtd_budget_serv, ytd_serv, ytd_budget_serv, variance_serv, t_day_tax, mtd_tax, mtd_budget_tax, ytd_tax, ytd_budget_tax, variance_tax, ct1, curr_flag1, ct2, banq_dept, frate, jan1, budget_flag, mon_saldo, mon_budget, foreign_curr, umsatz, waehrung, htparam, queasy, segment, artikel, hoteldpt, uebertrag, exrate, genstat, segmentstat, budget, zinrstat, zkstat
        nonlocal from_date, to_date
        nonlocal buff_umsatz, b_rev_list, b_rev_seg_list, b_rev_seg_list1, b_stat_list, brev_list, b_payment_list, bpayment_list, bpayable_list


        nonlocal rev_seg_list, rev_seg_list1, rev_list, rev_list_tax, rev_list_serv, payable_list, tot_list, stat_list, payment_list, segment_list, gl_list, fb_sales_food, fb_sales_beverage, fb_sales_other, fb_sales_tot, fb_sales_material, setup_revenue, setup_segment, setup_payment, setup_stat, setup_fbcover, buff_umsatz, b_rev_list, b_rev_seg_list, b_rev_seg_list1, b_stat_list, brev_list, b_payment_list, bpayment_list, bpayable_list
        nonlocal rev_seg_list_list, rev_seg_list1_list, rev_list_list, rev_list_tax_list, rev_list_serv_list, payable_list_list, tot_list_list, stat_list_list, payment_list_list, segment_list_list, gl_list_list, fb_sales_food_list, fb_sales_beverage_list, fb_sales_other_list, fb_sales_tot_list, fb_sales_material_list, setup_revenue_list, setup_segment_list, setup_payment_list, setup_stat_list, setup_fbcover_list

        if foreign_nr != 0:

            exrate = db_session.query(Exrate).filter(
                     (Exrate.artnr == foreign_nr) & (Exrate.datum == curr_date)).first()
        else:

            exrate = db_session.query(Exrate).filter(
                     (Exrate.datum == curr_date)).first()


    def fill_revenue_segement():

        nonlocal rev_seg_list_list, rev_list_list, payable_list_list, stat_list_list, payment_list_list, gl_list_list, fb_sales_food_list, fb_sales_beverage_list, fb_sales_other_list, fb_sales_tot_list, rev_seg_list1_list, fb_sales_material_list, gsheet_link, ytd_flag, str1, str2, str3, st1, st2, st3, st4, st5, st6, st7, st8, st9, st10, st11, st12, st13, st14, st15, st16, st17, st18, st19, st20, st21, st22, st23, st24, st25, st26, st27, st28, st29, st30, st31, st32, st33, st34, st35, st36, st37, n, n1, n2, n3, n4, n5, n6, n7, n8, n9, n10, n11, n12, n13, n14, n15, n16, n17, n18, n19, n20, n21, n22, n23, n24, n25, n26, n27, n28, n29, n30, curr_date, start_date, datum1, serv, vat, vat2, fact, n_betrag, n_serv, n_tax, ly_betrag, dbudget_flag, dlmtd_flag, yes_serv, yes_vat, yes_vat2, yes_fact, yes_betrag, date1, date2, temp_date2, temp_curr_date, l_today, st_date, foreign_nr, foreign_flag, tot_betrag, price_decimal, no_decimal, dept, dept1, zwkum, dper, mtd_per, ytd_per, tot_today, tot_today_per, tot_mtd, tot_mtd_per, tot_mtd_budget, tot_variance, tot_ytd, tot_ytd_budget, tot_ytd_per, tot_today1, tot_today_per1, tot_mtd1, tot_mtd_per1, tot_mtd_budget1, tot_variance1, tot_ytd1, tot_ytd_budget1, tot_ytd_per1, tot_today2, tot_today_per2, tot_mtd2, tot_mtd_per2, tot_mtd_budget2, tot_variance2, tot_ytd2, tot_ytd_budget2, tot_ytd_per2, tot_today3, tot_mtd3, tot_mtd_budget3, tot_variance3, tot_ytd3, tot_ytd_budget3, tot_today4, tot_mtd4, tot_mtd_budget4, tot_variance4, tot_ytd4, tot_ytd_budget4, tot_today5, tot_mtd5, tot_mtd_budget5, tot_variance5, tot_ytd5, tot_ytd_budget5, tot_today6, tot_mtd6, tot_mtd_budget6, tot_variance6, tot_ytd6, tot_ytd_budget6, tot_today7, tot_mtd7, tot_mtd_budget7, tot_variance7, tot_ytd7, tot_ytd_budget7, tot_tday_cov, tot_tday_avg, tot_tday_rev, tot_mtd_cov, tot_mtd_avg, tot_mtd_rev, tot_ytd_cov, tot_ytd_avg, tot_ytd_rev, t_today, t_today_per, t_mtd, t_mtd_per, t_mtd_budget, t_variance, t_ytd, t_ytd_budget, t_ytd_per, t_today1, t_today_per1, t_mtd1, t_mtd_per1, t_mtd_budget1, t_variance1, t_ytd1, t_ytd_budget1, t_ytd_per1, t_today11, t_today_per11, t_mtd11, t_mtd_per11, t_mtd_budget11, t_variance11, t_ytd11, t_ytd_budget11, t_ytd_per11, t_today2, t_today_per2, t_mtd2, t_mtd_per2, t_mtd_budget2, t_variance2, t_ytd2, t_ytd_budget2, t_ytd_per2, t_today3, t_today_per3, t_mtd3, t_mtd_per3, t_mtd_budget3, t_variance3, t_ytd3, t_ytd_budget3, t_ytd_per3, tdy_gl1, ytd_gl, curr_flag, curr_dept, ct, ct3, ct4, t_day_serv, mtd_serv, mtd_budget_serv, ytd_serv, ytd_budget_serv, variance_serv, t_day_tax, mtd_tax, mtd_budget_tax, ytd_tax, ytd_budget_tax, variance_tax, curr_flag1, ct2, banq_dept, frate, jan1, budget_flag, mon_saldo, mon_budget, foreign_curr, umsatz, waehrung, htparam, queasy, segment, artikel, hoteldpt, uebertrag, exrate, genstat, segmentstat, budget, zinrstat, zkstat
        nonlocal from_date, to_date
        nonlocal buff_umsatz, b_rev_list, b_rev_seg_list, b_rev_seg_list1, b_stat_list, brev_list, b_payment_list, bpayment_list, bpayable_list


        nonlocal rev_seg_list, rev_seg_list1, rev_list, rev_list_tax, rev_list_serv, payable_list, tot_list, stat_list, payment_list, segment_list, gl_list, fb_sales_food, fb_sales_beverage, fb_sales_other, fb_sales_tot, fb_sales_material, setup_revenue, setup_segment, setup_payment, setup_stat, setup_fbcover, buff_umsatz, b_rev_list, b_rev_seg_list, b_rev_seg_list1, b_stat_list, brev_list, b_payment_list, bpayment_list, bpayable_list
        nonlocal rev_seg_list_list, rev_seg_list1_list, rev_list_list, rev_list_tax_list, rev_list_serv_list, payable_list_list, tot_list_list, stat_list_list, payment_list_list, segment_list_list, gl_list_list, fb_sales_food_list, fb_sales_beverage_list, fb_sales_other_list, fb_sales_tot_list, fb_sales_material_list, setup_revenue_list, setup_segment_list, setup_payment_list, setup_stat_list, setup_fbcover_list

        t_day:decimal = to_decimal("0.0")
        mtd:decimal = to_decimal("0.0")
        mtd_budget:decimal = to_decimal("0.0")
        ytd:decimal = to_decimal("0.0")
        ytd_budget:decimal = to_decimal("0.0")
        variance:decimal = to_decimal("0.0")
        ct1:int = 0
        artnr:int = 0
        d_flag:bool = False
        mm:int = 0
        frate1:decimal = to_decimal("0.0")
        mm = get_month(to_date)
        artnr = setup_segment.artnr

        for genstat in db_session.query(Genstat).filter(
                 (Genstat.segmentcode == segment.segmentcode) & (Genstat.datum >= datum1) & (Genstat.datum <= to_date) & (Genstat.resstatus != 13) & (Genstat.segmentcode != 0) & (Genstat.nationnr != 0) & (Genstat.zinr != "") & (Genstat.res_logic[inc_value(1))]).order_by(Genstat._recid).all():

            if foreign_flag:
                find_exrate(genstat.datum)

                if exrate:
                    frate =  to_decimal(exrate.betrag)
            d_flag = (get_month(genstat.datum) == get_month(to_date)) and (get_year(genstat.datum) == get_year(to_date))

            if genstat.datum == to_date:
                t_day =  to_decimal(t_day) + to_decimal("1")

            if get_month(genstat.datum) == mm:
                mtd =  to_decimal(mtd) + to_decimal(mon_saldo[get_day(genstat.datum) - 1]) + to_decimal("1")
            ytd =  to_decimal(ytd) + to_decimal("1")

        for segmentstat in db_session.query(Segmentstat).filter(
                 (Segmentstat.datum >= datum1) & (Segmentstat.datum <= to_date) & (Segmentstat.segmentcode == segment.segmentcode)).order_by(Segmentstat._recid).all():

            if get_month(segmentstat.datum) == mm:
                mtd_budget =  to_decimal(mtd_budget) + to_decimal(segmentstat.budzimmeranz)
            ytd_budget =  to_decimal(ytd_budget) + to_decimal(segmentstat.budzimmeranz)
        variance =  to_decimal(mtd) - to_decimal(mtd_budget)

        rev_seg_list = query(rev_seg_list_list, filters=(lambda rev_seg_list: rev_seg_list.descr == setup_segment.descr), first=True)

        if rev_seg_list:
            rev_seg_list.t_day =  to_decimal(rev_seg_list.t_day) + to_decimal(t_day)
            rev_seg_list.mtd =  to_decimal(rev_seg_list.mtd) + to_decimal(mtd)
            rev_seg_list.mtd_budget =  to_decimal(rev_seg_list.mtd_budget) + to_decimal(mtd_budget)
            rev_seg_list.ytd =  to_decimal(rev_seg_list.ytd) + to_decimal(ytd)
            rev_seg_list.ytd_budget =  to_decimal(rev_seg_list.ytd_budget) + to_decimal(ytd_budget)
            rev_seg_list.variance =  to_decimal(rev_seg_list.variance) + to_decimal(variance)


        else:
            ct = ct + 1
            rev_seg_list = Rev_seg_list()
            rev_seg_list_list.append(rev_seg_list)

            rev_seg_list.ct = ct
            rev_seg_list.segment_code = setup_segment.artnr
            rev_seg_list.flag = setup_segment.flag
            rev_seg_list.departement = setup_segment.departement
            rev_seg_list.t_day =  to_decimal(t_day)
            rev_seg_list.mtd =  to_decimal(mtd)
            rev_seg_list.mtd_budget =  to_decimal(mtd_budget)
            rev_seg_list.ytd =  to_decimal(ytd)
            rev_seg_list.ytd_budget =  to_decimal(ytd_budget)
            rev_seg_list.variance =  to_decimal(variance)

            if setup_segment.flag_grup :
                rev_seg_list.descr = setup_segment.descr
                rev_seg_list.flag_grup = True


            else:
                rev_seg_list.descr = segment.bezeich


    def fill_revenue_segement1():

        nonlocal rev_seg_list_list, rev_list_list, payable_list_list, stat_list_list, payment_list_list, gl_list_list, fb_sales_food_list, fb_sales_beverage_list, fb_sales_other_list, fb_sales_tot_list, rev_seg_list1_list, fb_sales_material_list, gsheet_link, ytd_flag, str1, str2, str3, st1, st2, st3, st4, st5, st6, st7, st8, st9, st10, st11, st12, st13, st14, st15, st16, st17, st18, st19, st20, st21, st22, st23, st24, st25, st26, st27, st28, st29, st30, st31, st32, st33, st34, st35, st36, st37, n, n1, n2, n3, n4, n5, n6, n7, n8, n9, n10, n11, n12, n13, n14, n15, n16, n17, n18, n19, n20, n21, n22, n23, n24, n25, n26, n27, n28, n29, n30, curr_date, start_date, datum1, serv, vat, vat2, fact, n_betrag, n_serv, n_tax, ly_betrag, dbudget_flag, dlmtd_flag, yes_serv, yes_vat, yes_vat2, yes_fact, yes_betrag, date1, date2, temp_date2, temp_curr_date, l_today, st_date, foreign_nr, foreign_flag, tot_betrag, price_decimal, no_decimal, dept, dept1, zwkum, dper, mtd_per, ytd_per, tot_today, tot_today_per, tot_mtd, tot_mtd_per, tot_mtd_budget, tot_variance, tot_ytd, tot_ytd_budget, tot_ytd_per, tot_today1, tot_today_per1, tot_mtd1, tot_mtd_per1, tot_mtd_budget1, tot_variance1, tot_ytd1, tot_ytd_budget1, tot_ytd_per1, tot_today2, tot_today_per2, tot_mtd2, tot_mtd_per2, tot_mtd_budget2, tot_variance2, tot_ytd2, tot_ytd_budget2, tot_ytd_per2, tot_today3, tot_mtd3, tot_mtd_budget3, tot_variance3, tot_ytd3, tot_ytd_budget3, tot_today4, tot_mtd4, tot_mtd_budget4, tot_variance4, tot_ytd4, tot_ytd_budget4, tot_today5, tot_mtd5, tot_mtd_budget5, tot_variance5, tot_ytd5, tot_ytd_budget5, tot_today6, tot_mtd6, tot_mtd_budget6, tot_variance6, tot_ytd6, tot_ytd_budget6, tot_today7, tot_mtd7, tot_mtd_budget7, tot_variance7, tot_ytd7, tot_ytd_budget7, tot_tday_cov, tot_tday_avg, tot_tday_rev, tot_mtd_cov, tot_mtd_avg, tot_mtd_rev, tot_ytd_cov, tot_ytd_avg, tot_ytd_rev, t_today, t_today_per, t_mtd, t_mtd_per, t_mtd_budget, t_variance, t_ytd, t_ytd_budget, t_ytd_per, t_today1, t_today_per1, t_mtd1, t_mtd_per1, t_mtd_budget1, t_variance1, t_ytd1, t_ytd_budget1, t_ytd_per1, t_today11, t_today_per11, t_mtd11, t_mtd_per11, t_mtd_budget11, t_variance11, t_ytd11, t_ytd_budget11, t_ytd_per11, t_today2, t_today_per2, t_mtd2, t_mtd_per2, t_mtd_budget2, t_variance2, t_ytd2, t_ytd_budget2, t_ytd_per2, t_today3, t_today_per3, t_mtd3, t_mtd_per3, t_mtd_budget3, t_variance3, t_ytd3, t_ytd_budget3, t_ytd_per3, tdy_gl1, ytd_gl, curr_flag, curr_dept, ct, ct3, ct4, t_day_serv, mtd_serv, mtd_budget_serv, ytd_serv, ytd_budget_serv, variance_serv, t_day_tax, mtd_tax, mtd_budget_tax, ytd_tax, ytd_budget_tax, variance_tax, curr_flag1, ct2, banq_dept, frate, jan1, budget_flag, mon_saldo, mon_budget, foreign_curr, umsatz, waehrung, htparam, queasy, segment, artikel, hoteldpt, uebertrag, exrate, genstat, segmentstat, budget, zinrstat, zkstat
        nonlocal from_date, to_date
        nonlocal buff_umsatz, b_rev_list, b_rev_seg_list, b_rev_seg_list1, b_stat_list, brev_list, b_payment_list, bpayment_list, bpayable_list


        nonlocal rev_seg_list, rev_seg_list1, rev_list, rev_list_tax, rev_list_serv, payable_list, tot_list, stat_list, payment_list, segment_list, gl_list, fb_sales_food, fb_sales_beverage, fb_sales_other, fb_sales_tot, fb_sales_material, setup_revenue, setup_segment, setup_payment, setup_stat, setup_fbcover, buff_umsatz, b_rev_list, b_rev_seg_list, b_rev_seg_list1, b_stat_list, brev_list, b_payment_list, bpayment_list, bpayable_list
        nonlocal rev_seg_list_list, rev_seg_list1_list, rev_list_list, rev_list_tax_list, rev_list_serv_list, payable_list_list, tot_list_list, stat_list_list, payment_list_list, segment_list_list, gl_list_list, fb_sales_food_list, fb_sales_beverage_list, fb_sales_other_list, fb_sales_tot_list, fb_sales_material_list, setup_revenue_list, setup_segment_list, setup_payment_list, setup_stat_list, setup_fbcover_list

        t_day:decimal = to_decimal("0.0")
        mtd:decimal = to_decimal("0.0")
        mtd_budget:decimal = to_decimal("0.0")
        ytd:decimal = to_decimal("0.0")
        ytd_budget:decimal = to_decimal("0.0")
        variance:decimal = to_decimal("0.0")
        ct1:int = 0
        artnr:int = 0
        d_flag:bool = False
        mm:int = 0
        frate1:decimal = to_decimal("0.0")
        artnr = setup_segment.artnr

        for genstat in db_session.query(Genstat).filter(
                 (Genstat.segmentcode == segment.segmentcode) & (Genstat.datum >= datum1) & (Genstat.datum <= to_date) & (Genstat.resstatus != 13) & (Genstat.segmentcode != 0) & (Genstat.nationnr != 0) & (Genstat.zinr != "") & (Genstat.res_logic[inc_value(1))]).order_by(Genstat._recid).all():

            if foreign_flag:
                find_exrate(genstat.datum)

                if exrate:
                    frate =  to_decimal(exrate.betrag)
            d_flag = (get_month(genstat.datum) == get_month(to_date)) and (get_year(genstat.datum) == get_year(to_date))

            if genstat.datum == to_date:
                t_day =  to_decimal(t_day) + to_decimal(genstat.logis)

            if get_month(genstat.datum) == get_month(to_date):
                mtd =  to_decimal(mtd) + to_decimal(mon_saldo[get_day(genstat.datum) - 1]) + to_decimal(genstat.logis)
            ytd =  to_decimal(ytd) + to_decimal(genstat.logis)

        for segmentstat in db_session.query(Segmentstat).filter(
                 (Segmentstat.datum >= datum1) & (Segmentstat.datum <= to_date) & (Segmentstat.segmentcode == segment.segmentcode)).order_by(Segmentstat._recid).all():

            if get_month(segmentstat.datum) == get_month(to_date):
                mtd_budget =  to_decimal(mtd_budget) + to_decimal(segmentstat.budlogis)
            ytd_budget =  to_decimal(ytd_budget) + to_decimal(segmentstat.budlogis)
        variance =  to_decimal(mtd) - to_decimal(mtd_budget)

        rev_seg_list1 = query(rev_seg_list1_list, filters=(lambda rev_seg_list1: rev_seg_list1.descr == setup_segment.descr), first=True)

        if rev_seg_list1:
            rev_seg_list1.t_day =  to_decimal(rev_seg_list1.t_day) + to_decimal(t_day)
            rev_seg_list1.mtd =  to_decimal(rev_seg_list1.mtd) + to_decimal(mtd)
            rev_seg_list1.mtd_budget =  to_decimal(rev_seg_list1.mtd_budget) + to_decimal(mtd_budget)
            rev_seg_list1.ytd =  to_decimal(rev_seg_list1.ytd) + to_decimal(ytd)
            rev_seg_list1.ytd_budget =  to_decimal(rev_seg_list1.ytd_budget) + to_decimal(ytd_budget)
            rev_seg_list1.variance =  to_decimal(rev_seg_list1.variance) + to_decimal(variance)


        else:
            ct = ct + 1
            rev_seg_list1 = Rev_seg_list1()
            rev_seg_list1_list.append(rev_seg_list1)

            rev_seg_list1.ct = ct
            rev_seg_list1.segment_code = setup_segment.artnr
            rev_seg_list1.flag = setup_segment.flag
            rev_seg_list1.departement = setup_segment.departement
            rev_seg_list1.t_day =  to_decimal(t_day)
            rev_seg_list1.mtd =  to_decimal(mtd)
            rev_seg_list1.mtd_budget =  to_decimal(mtd_budget)
            rev_seg_list1.ytd =  to_decimal(ytd)
            rev_seg_list1.ytd_budget =  to_decimal(ytd_budget)
            rev_seg_list1.variance =  to_decimal(variance)

            if setup_segment.flag_grup :
                rev_seg_list1.descr = setup_segment.descr
                rev_seg_list1.flag_grup = True


            else:
                rev_seg_list1.descr = segment.bezeich


    def create_rev_list():

        nonlocal rev_seg_list_list, rev_list_list, payable_list_list, stat_list_list, payment_list_list, gl_list_list, fb_sales_food_list, fb_sales_beverage_list, fb_sales_other_list, fb_sales_tot_list, rev_seg_list1_list, fb_sales_material_list, gsheet_link, ytd_flag, str1, str2, str3, st1, st2, st3, st4, st5, st6, st7, st8, st9, st10, st11, st12, st13, st14, st15, st16, st17, st18, st19, st20, st21, st22, st23, st24, st25, st26, st27, st28, st29, st30, st31, st32, st33, st34, st35, st36, st37, n, n1, n2, n3, n4, n5, n6, n7, n8, n9, n10, n11, n12, n13, n14, n15, n16, n17, n18, n19, n20, n21, n22, n23, n24, n25, n26, n27, n28, n29, n30, curr_date, start_date, datum1, serv, vat, vat2, fact, n_betrag, n_serv, n_tax, ly_betrag, d_flag, dbudget_flag, dlmtd_flag, yes_serv, yes_vat, yes_vat2, yes_fact, yes_betrag, date1, date2, temp_date2, temp_curr_date, l_today, st_date, foreign_nr, foreign_flag, tot_betrag, price_decimal, no_decimal, dept, dept1, zwkum, dper, mtd_per, ytd_per, tot_today, tot_today_per, tot_mtd, tot_mtd_per, tot_mtd_budget, tot_variance, tot_ytd, tot_ytd_budget, tot_ytd_per, tot_today1, tot_today_per1, tot_mtd1, tot_mtd_per1, tot_mtd_budget1, tot_variance1, tot_ytd1, tot_ytd_budget1, tot_ytd_per1, tot_today2, tot_today_per2, tot_mtd2, tot_mtd_per2, tot_mtd_budget2, tot_variance2, tot_ytd2, tot_ytd_budget2, tot_ytd_per2, tot_today3, tot_mtd3, tot_mtd_budget3, tot_variance3, tot_ytd3, tot_ytd_budget3, tot_today4, tot_mtd4, tot_mtd_budget4, tot_variance4, tot_ytd4, tot_ytd_budget4, tot_today5, tot_mtd5, tot_mtd_budget5, tot_variance5, tot_ytd5, tot_ytd_budget5, tot_today6, tot_mtd6, tot_mtd_budget6, tot_variance6, tot_ytd6, tot_ytd_budget6, tot_today7, tot_mtd7, tot_mtd_budget7, tot_variance7, tot_ytd7, tot_ytd_budget7, tot_tday_cov, tot_tday_avg, tot_tday_rev, tot_mtd_cov, tot_mtd_avg, tot_mtd_rev, tot_ytd_cov, tot_ytd_avg, tot_ytd_rev, t_today, t_today_per, t_mtd, t_mtd_per, t_mtd_budget, t_variance, t_ytd, t_ytd_budget, t_ytd_per, t_today1, t_today_per1, t_mtd1, t_mtd_per1, t_mtd_budget1, t_variance1, t_ytd1, t_ytd_budget1, t_ytd_per1, t_today11, t_today_per11, t_mtd11, t_mtd_per11, t_mtd_budget11, t_variance11, t_ytd11, t_ytd_budget11, t_ytd_per11, t_today2, t_today_per2, t_mtd2, t_mtd_per2, t_mtd_budget2, t_variance2, t_ytd2, t_ytd_budget2, t_ytd_per2, t_today3, t_today_per3, t_mtd3, t_mtd_per3, t_mtd_budget3, t_variance3, t_ytd3, t_ytd_budget3, t_ytd_per3, tdy_gl1, ytd_gl, curr_flag, curr_dept, ct, ct3, ct4, t_day_serv, mtd_serv, mtd_budget_serv, ytd_serv, ytd_budget_serv, variance_serv, t_day_tax, mtd_tax, mtd_budget_tax, ytd_tax, ytd_budget_tax, variance_tax, ct1, curr_flag1, ct2, banq_dept, frate, jan1, budget_flag, mon_saldo, mon_budget, foreign_curr, umsatz, waehrung, htparam, queasy, segment, artikel, hoteldpt, uebertrag, exrate, genstat, segmentstat, budget, zinrstat, zkstat
        nonlocal from_date, to_date
        nonlocal buff_umsatz, b_rev_list, b_rev_seg_list, b_rev_seg_list1, b_stat_list, brev_list, b_payment_list, bpayment_list, bpayable_list


        nonlocal rev_seg_list, rev_seg_list1, rev_list, rev_list_tax, rev_list_serv, payable_list, tot_list, stat_list, payment_list, segment_list, gl_list, fb_sales_food, fb_sales_beverage, fb_sales_other, fb_sales_tot, fb_sales_material, setup_revenue, setup_segment, setup_payment, setup_stat, setup_fbcover, buff_umsatz, b_rev_list, b_rev_seg_list, b_rev_seg_list1, b_stat_list, brev_list, b_payment_list, bpayment_list, bpayable_list
        nonlocal rev_seg_list_list, rev_seg_list1_list, rev_list_list, rev_list_tax_list, rev_list_serv_list, payable_list_list, tot_list_list, stat_list_list, payment_list_list, segment_list_list, gl_list_list, fb_sales_food_list, fb_sales_beverage_list, fb_sales_other_list, fb_sales_tot_list, fb_sales_material_list, setup_revenue_list, setup_segment_list, setup_payment_list, setup_stat_list, setup_fbcover_list

        t_day:decimal = to_decimal("0.0")
        mtd:decimal = to_decimal("0.0")
        mtd_budget:decimal = to_decimal("0.0")
        ytd:decimal = to_decimal("0.0")
        ytd_budget:decimal = to_decimal("0.0")
        variance:decimal = to_decimal("0.0")
        for curr_date in date_range(datum1,to_date) :
            serv =  to_decimal("0")
            vat =  to_decimal("0")

            umsatz = db_session.query(Umsatz).filter(
                     (Umsatz.datum == curr_date) & (Umsatz.artnr == artikel.artnr) & (Umsatz.departement == artikel.departement)).first()

            if umsatz:
                serv, vat, vat2, fact = get_output(calc_servtaxesbl(1, umsatz.artnr, umsatz.departement, umsatz.datum))
            fact =  to_decimal(1.00) + to_decimal(serv) + to_decimal(vat) + to_decimal(vat2)
            d_flag = None != umsatz and (get_month(umsatz.datum) == get_month(to_date)) and (get_year(umsatz.datum) == get_year(to_date))
            n_betrag =  to_decimal("0")

            if umsatz:

                if foreign_flag:
                    find_exrate(curr_date)

                    if exrate:
                        frate =  to_decimal(exrate.betrag)
                n_betrag =  to_decimal(umsatz.betrag) / to_decimal((fact) * to_decimal(frate) )
                n_serv =  to_decimal(n_betrag) * to_decimal(serv)
                n_tax =  to_decimal(n_betrag) * to_decimal(vat)

                if umsat.datum == to_date:
                    t_day =  to_decimal(t_day) + to_decimal(n_betrag)
                    t_day_serv =  to_decimal(t_day_serv) + to_decimal(n_serv)
                    t_day_tax =  to_decimal(t_day_tax) + to_decimal(n_tax)

                if price_decimal == 0:
                    n_betrag = to_decimal(round(n_betrag , 0))
                    n_serv = to_decimal(round(n_serv , 0))
                    n_tax = to_decimal(round(n_tax , 0))

            budget = db_session.query(Budget).filter(
                     (Budget.artnr == artikel.artnr) & (Budget.departement == artikel.departement) & (Budget.datum == curr_date)).first()

            if curr_date < from_date:

                if umsatz:
                    ytd =  to_decimal(ytd) + to_decimal(n_betrag)
                    ytd_serv =  to_decimal(ytd_serv) + to_decimal(n_serv)
                    ytd_tax =  to_decimal(ytd_tax) + to_decimal(n_tax)

                if budget:
                    ytd_budget =  to_decimal(ytd_budget) + to_decimal(budget.betrag)


            else:

                if umsatz:

                    if ytd_flag:
                        ytd =  to_decimal(ytd) + to_decimal(n_betrag)
                        ytd_serv =  to_decimal(ytd_serv) + to_decimal(n_serv)
                        ytd_tax =  to_decimal(ytd_tax) + to_decimal(n_tax)

                    if get_month(curr_date) == get_month(to_date):
                        mtd =  to_decimal(mtd) + to_decimal(mon_saldo[get_day(umsatz.datum) - 1]) + to_decimal(n_betrag)
                        mtd_serv =  to_decimal(mtd_serv) + to_decimal(mon_saldo[get_day(umsatz.datum) - 1]) + to_decimal(n_serv)
                        mtd_tax =  to_decimal(mtd_tax) + to_decimal(mon_saldo[get_day(umsatz.datum) - 1]) + to_decimal(n_tax)

                if budget:
                    mtd_budget =  to_decimal(mtd_budget) + to_decimal(budget.betrag)
            variance =  to_decimal(mtd) - to_decimal(mtd_budget)

        rev_list = query(rev_list_list, filters=(lambda rev_list: rev_list.descr == setup_revenue.descr), first=True)

        if rev_list:
            rev_list.t_day =  to_decimal(rev_list.t_day) + to_decimal(t_day)
            rev_list.mtd =  to_decimal(rev_list.mtd) + to_decimal(mtd)
            rev_list.mtd_budget =  to_decimal(rev_list.mtd_budget) + to_decimal(mtd_budget)
            rev_list.ytd =  to_decimal(rev_list.ytd) + to_decimal(ytd)
            rev_list.ytd_budget =  to_decimal(rev_list.ytd_budget) + to_decimal(ytd_budget)
            rev_list.variance =  to_decimal(rev_list.variance) + to_decimal(variance)


        else:

            rev_list = query(rev_list_list, filters=(lambda rev_list: rev_list.departement == setup_revenue.departement), first=True)

            if not rev_list:
                ct = ct + 1

                hoteldpt = db_session.query(Hoteldpt).filter(
                         (Hoteldpt.num == setup_revenue.departement)).first()
                rev_list = Rev_list()
                rev_list_list.append(rev_list)

                rev_list.ct = ct
                rev_list.flag = "zeich-dept"
                rev_list.departement = setup_revenue.departement
                rev_list.descr = hoteldpt.depart


                pass
            ct = ct + 1
            rev_list = Rev_list()
            rev_list_list.append(rev_list)

            rev_list.ct = ct
            rev_list.flag = setup_revenue.flag
            rev_list.departement = setup_revenue.departement
            rev_list.t_day =  to_decimal(t_day)
            rev_list.mtd =  to_decimal(mtd)
            rev_list.mtd_budget =  to_decimal(mtd_budget)
            rev_list.ytd =  to_decimal(ytd)
            rev_list.ytd_budget =  to_decimal(ytd_budget)
            rev_list.variance =  to_decimal(variance)

            if setup_revenue.flag_grup :
                rev_list.descr = setup_revenue.descr
                rev_list.flag_grup = True


            else:
                rev_list.descr = artikel.bezeich


    def create_payable_list():

        nonlocal rev_seg_list_list, rev_list_list, payable_list_list, stat_list_list, payment_list_list, gl_list_list, fb_sales_food_list, fb_sales_beverage_list, fb_sales_other_list, fb_sales_tot_list, rev_seg_list1_list, fb_sales_material_list, gsheet_link, ytd_flag, str1, str2, str3, st1, st2, st3, st4, st5, st6, st7, st8, st9, st10, st11, st12, st13, st14, st15, st16, st17, st18, st19, st20, st21, st22, st23, st24, st25, st26, st27, st28, st29, st30, st31, st32, st33, st34, st35, st36, st37, n, n1, n2, n3, n4, n5, n6, n7, n8, n9, n10, n11, n12, n13, n14, n15, n16, n17, n18, n19, n20, n21, n22, n23, n24, n25, n26, n27, n28, n29, n30, curr_date, start_date, datum1, serv, vat, vat2, fact, n_betrag, n_serv, n_tax, ly_betrag, d_flag, dbudget_flag, dlmtd_flag, yes_serv, yes_vat, yes_vat2, yes_fact, yes_betrag, date1, date2, temp_date2, temp_curr_date, l_today, st_date, foreign_nr, foreign_flag, tot_betrag, price_decimal, no_decimal, dept, dept1, zwkum, dper, mtd_per, ytd_per, tot_today, tot_today_per, tot_mtd, tot_mtd_per, tot_mtd_budget, tot_variance, tot_ytd, tot_ytd_budget, tot_ytd_per, tot_today1, tot_today_per1, tot_mtd1, tot_mtd_per1, tot_mtd_budget1, tot_variance1, tot_ytd1, tot_ytd_budget1, tot_ytd_per1, tot_today2, tot_today_per2, tot_mtd2, tot_mtd_per2, tot_mtd_budget2, tot_variance2, tot_ytd2, tot_ytd_budget2, tot_ytd_per2, tot_today3, tot_mtd3, tot_mtd_budget3, tot_variance3, tot_ytd3, tot_ytd_budget3, tot_today4, tot_mtd4, tot_mtd_budget4, tot_variance4, tot_ytd4, tot_ytd_budget4, tot_today5, tot_mtd5, tot_mtd_budget5, tot_variance5, tot_ytd5, tot_ytd_budget5, tot_today6, tot_mtd6, tot_mtd_budget6, tot_variance6, tot_ytd6, tot_ytd_budget6, tot_today7, tot_mtd7, tot_mtd_budget7, tot_variance7, tot_ytd7, tot_ytd_budget7, tot_tday_cov, tot_tday_avg, tot_tday_rev, tot_mtd_cov, tot_mtd_avg, tot_mtd_rev, tot_ytd_cov, tot_ytd_avg, tot_ytd_rev, t_today, t_today_per, t_mtd, t_mtd_per, t_mtd_budget, t_variance, t_ytd, t_ytd_budget, t_ytd_per, t_today1, t_today_per1, t_mtd1, t_mtd_per1, t_mtd_budget1, t_variance1, t_ytd1, t_ytd_budget1, t_ytd_per1, t_today11, t_today_per11, t_mtd11, t_mtd_per11, t_mtd_budget11, t_variance11, t_ytd11, t_ytd_budget11, t_ytd_per11, t_today2, t_today_per2, t_mtd2, t_mtd_per2, t_mtd_budget2, t_variance2, t_ytd2, t_ytd_budget2, t_ytd_per2, t_today3, t_today_per3, t_mtd3, t_mtd_per3, t_mtd_budget3, t_variance3, t_ytd3, t_ytd_budget3, t_ytd_per3, tdy_gl1, ytd_gl, curr_flag, curr_dept, ct, ct3, ct4, t_day_serv, mtd_serv, mtd_budget_serv, ytd_serv, ytd_budget_serv, variance_serv, t_day_tax, mtd_tax, mtd_budget_tax, ytd_tax, ytd_budget_tax, variance_tax, ct1, curr_flag1, ct2, banq_dept, frate, jan1, budget_flag, mon_saldo, mon_budget, foreign_curr, umsatz, waehrung, htparam, queasy, segment, artikel, hoteldpt, uebertrag, exrate, genstat, segmentstat, budget, zinrstat, zkstat
        nonlocal from_date, to_date
        nonlocal buff_umsatz, b_rev_list, b_rev_seg_list, b_rev_seg_list1, b_stat_list, brev_list, b_payment_list, bpayment_list, bpayable_list


        nonlocal rev_seg_list, rev_seg_list1, rev_list, rev_list_tax, rev_list_serv, payable_list, tot_list, stat_list, payment_list, segment_list, gl_list, fb_sales_food, fb_sales_beverage, fb_sales_other, fb_sales_tot, fb_sales_material, setup_revenue, setup_segment, setup_payment, setup_stat, setup_fbcover, buff_umsatz, b_rev_list, b_rev_seg_list, b_rev_seg_list1, b_stat_list, brev_list, b_payment_list, bpayment_list, bpayable_list
        nonlocal rev_seg_list_list, rev_seg_list1_list, rev_list_list, rev_list_tax_list, rev_list_serv_list, payable_list_list, tot_list_list, stat_list_list, payment_list_list, segment_list_list, gl_list_list, fb_sales_food_list, fb_sales_beverage_list, fb_sales_other_list, fb_sales_tot_list, fb_sales_material_list, setup_revenue_list, setup_segment_list, setup_payment_list, setup_stat_list, setup_fbcover_list


        payable_list = Payable_list()
        payable_list_list.append(payable_list)

        payable_list.descr = artikel.bezeich
        payable_list.flag = setup_revenue.flag
        payable_list.departement = setup_revenue.departement


        for curr_date in date_range(datum1,to_date) :
            serv =  to_decimal("0")
            vat =  to_decimal("0")

            umsatz = db_session.query(Umsatz).filter(
                     (Umsatz.datum == curr_date) & (Umsatz.artnr == artikel.artnr) & (Umsatz.departement == artikel.departement)).first()

            if umsatz:
                serv, vat, vat2, fact = get_output(calc_servtaxesbl(1, umsatz.artnr, umsatz.departement, umsatz.datum))
            fact =  to_decimal(1.00) + to_decimal(serv) + to_decimal(vat) + to_decimal(vat2)
            d_flag = None != umsatz and (get_month(umsatz.datum) == get_month(to_date)) and (get_year(umsatz.datum) == get_year(to_date))
            n_betrag =  to_decimal("0")

            if umsatz:

                if foreign_flag:
                    find_exrate(curr_date)

                    if exrate:
                        frate =  to_decimal(exrate.betrag)
                n_betrag =  to_decimal(umsatz.betrag) / to_decimal((fact) * to_decimal(frate) )
                n_serv =  to_decimal(n_betrag) * to_decimal(serv)
                n_tax =  to_decimal(n_betrag) * to_decimal(vat)

                if umsat.datum == to_date:
                    payable_list.t_day =  to_decimal(payable_list.t_day) + to_decimal((umsatz.betrag) / to_decimal((fact) * to_decimal(frate)) )

                if price_decimal == 0:
                    n_betrag = to_decimal(round(n_betrag , 0))
                    n_serv = to_decimal(round(n_serv , 0))
                    n_tax = to_decimal(round(n_tax , 0))

            budget = db_session.query(Budget).filter(
                     (Budget.artnr == artikel.artnr) & (Budget.departement == artikel.departement) & (Budget.datum == curr_date)).first()

            if curr_date < from_date:

                if umsatz:
                    payable_list.ytd =  to_decimal(payable_list.ytd) + to_decimal(n_betrag)

                if budget:
                    payable_list.ytd_budget =  to_decimal(payable_list.ytd_budget) + to_decimal(budget.betrag)
            else:

                if umsatz:

                    if ytd_flag:
                        payable_list.ytd =  to_decimal(payable_list.ytd) + to_decimal(n_betrag)

                    if get_month(curr_date) == get_month(to_date):
                        payable_list.mtd =  to_decimal(payable_list.mtd) + to_decimal(mon_saldo[get_day(umsatz.datum) - 1]) + to_decimal(n_betrag)

                if budget:
                    payable_list.mtd_budget =  to_decimal(payable_list.mtd_budget) + to_decimal(budget.betrag)
            payable_list.variance =  to_decimal(payable_list.mtd) - to_decimal(payable_list.mtd_budget)


    def create_payment_list():

        nonlocal rev_seg_list_list, rev_list_list, payable_list_list, stat_list_list, payment_list_list, gl_list_list, fb_sales_food_list, fb_sales_beverage_list, fb_sales_other_list, fb_sales_tot_list, rev_seg_list1_list, fb_sales_material_list, gsheet_link, ytd_flag, str1, str2, str3, st1, st2, st3, st4, st5, st6, st7, st8, st9, st10, st11, st12, st13, st14, st15, st16, st17, st18, st19, st20, st21, st22, st23, st24, st25, st26, st27, st28, st29, st30, st31, st32, st33, st34, st35, st36, st37, n, n1, n2, n3, n4, n5, n6, n7, n8, n9, n10, n11, n12, n13, n14, n15, n16, n17, n18, n19, n20, n21, n22, n23, n24, n25, n26, n27, n28, n29, n30, curr_date, start_date, datum1, serv, vat, vat2, fact, n_betrag, n_serv, n_tax, ly_betrag, d_flag, dbudget_flag, dlmtd_flag, yes_serv, yes_vat, yes_vat2, yes_fact, yes_betrag, date1, date2, temp_date2, temp_curr_date, l_today, st_date, foreign_nr, foreign_flag, tot_betrag, price_decimal, no_decimal, dept, dept1, zwkum, dper, mtd_per, ytd_per, tot_today, tot_today_per, tot_mtd, tot_mtd_per, tot_mtd_budget, tot_variance, tot_ytd, tot_ytd_budget, tot_ytd_per, tot_today1, tot_today_per1, tot_mtd1, tot_mtd_per1, tot_mtd_budget1, tot_variance1, tot_ytd1, tot_ytd_budget1, tot_ytd_per1, tot_today2, tot_today_per2, tot_mtd2, tot_mtd_per2, tot_mtd_budget2, tot_variance2, tot_ytd2, tot_ytd_budget2, tot_ytd_per2, tot_today3, tot_mtd3, tot_mtd_budget3, tot_variance3, tot_ytd3, tot_ytd_budget3, tot_today4, tot_mtd4, tot_mtd_budget4, tot_variance4, tot_ytd4, tot_ytd_budget4, tot_today5, tot_mtd5, tot_mtd_budget5, tot_variance5, tot_ytd5, tot_ytd_budget5, tot_today6, tot_mtd6, tot_mtd_budget6, tot_variance6, tot_ytd6, tot_ytd_budget6, tot_today7, tot_mtd7, tot_mtd_budget7, tot_variance7, tot_ytd7, tot_ytd_budget7, tot_tday_cov, tot_tday_avg, tot_tday_rev, tot_mtd_cov, tot_mtd_avg, tot_mtd_rev, tot_ytd_cov, tot_ytd_avg, tot_ytd_rev, t_today, t_today_per, t_mtd, t_mtd_per, t_mtd_budget, t_variance, t_ytd, t_ytd_budget, t_ytd_per, t_today1, t_today_per1, t_mtd1, t_mtd_per1, t_mtd_budget1, t_variance1, t_ytd1, t_ytd_budget1, t_ytd_per1, t_today11, t_today_per11, t_mtd11, t_mtd_per11, t_mtd_budget11, t_variance11, t_ytd11, t_ytd_budget11, t_ytd_per11, t_today2, t_today_per2, t_mtd2, t_mtd_per2, t_mtd_budget2, t_variance2, t_ytd2, t_ytd_budget2, t_ytd_per2, t_today3, t_today_per3, t_mtd3, t_mtd_per3, t_mtd_budget3, t_variance3, t_ytd3, t_ytd_budget3, t_ytd_per3, tdy_gl1, ytd_gl, curr_flag, curr_dept, ct, ct3, ct4, t_day_serv, mtd_serv, mtd_budget_serv, ytd_serv, ytd_budget_serv, variance_serv, t_day_tax, mtd_tax, mtd_budget_tax, ytd_tax, ytd_budget_tax, variance_tax, ct1, curr_flag1, ct2, banq_dept, frate, jan1, budget_flag, mon_saldo, mon_budget, foreign_curr, umsatz, waehrung, htparam, queasy, segment, artikel, hoteldpt, uebertrag, exrate, genstat, segmentstat, budget, zinrstat, zkstat
        nonlocal from_date, to_date
        nonlocal buff_umsatz, b_rev_list, b_rev_seg_list, b_rev_seg_list1, b_stat_list, brev_list, b_payment_list, bpayment_list, bpayable_list


        nonlocal rev_seg_list, rev_seg_list1, rev_list, rev_list_tax, rev_list_serv, payable_list, tot_list, stat_list, payment_list, segment_list, gl_list, fb_sales_food, fb_sales_beverage, fb_sales_other, fb_sales_tot, fb_sales_material, setup_revenue, setup_segment, setup_payment, setup_stat, setup_fbcover, buff_umsatz, b_rev_list, b_rev_seg_list, b_rev_seg_list1, b_stat_list, brev_list, b_payment_list, bpayment_list, bpayable_list
        nonlocal rev_seg_list_list, rev_seg_list1_list, rev_list_list, rev_list_tax_list, rev_list_serv_list, payable_list_list, tot_list_list, stat_list_list, payment_list_list, segment_list_list, gl_list_list, fb_sales_food_list, fb_sales_beverage_list, fb_sales_other_list, fb_sales_tot_list, fb_sales_material_list, setup_revenue_list, setup_segment_list, setup_payment_list, setup_stat_list, setup_fbcover_list


        payment_list = Payment_list()
        payment_list_list.append(payment_list)

        payment_list.ct = ct2
        payment_list.descr = artikel.bezeich
        payment_list.departement = setup_payment.departement

        if artikel.artart == 6 and artikel.umsatzart == 0:
            payment_list.flag = "1Cash"

        elif artikel.artart == 7 and artikel.umsatzart == 0:
            payment_list.flag = "2Payment"

        elif artikel.artart == 2 and artikel.umsatzart == 0:
            payment_list.flag = "3Ledger"

        elif artikel.artart == 6 and artikel.umsatzart == 4:
            payment_list.flag = "4Foreign"

        elif artikel.artart == 5 and artikel.umsatzart == 0:
            payment_list.flag = "5Deposit"


        for curr_date in date_range(datum1,to_date) :
            serv =  to_decimal("0")
            vat =  to_decimal("0")

            umsatz = db_session.query(Umsatz).filter(
                     (Umsatz.datum == curr_date) & (Umsatz.artnr == artikel.artnr) & (Umsatz.departement == artikel.departement)).first()

            if umsatz:
                serv, vat, vat2, fact = get_output(calc_servtaxesbl(1, umsatz.artnr, umsatz.departement, umsatz.datum))
            fact =  to_decimal(1.00) + to_decimal(serv) + to_decimal(vat) + to_decimal(vat2)
            d_flag = None != umsatz and (get_month(umsatz.datum) == get_month(to_date)) and (get_year(umsatz.datum) == get_year(to_date))
            n_betrag =  to_decimal("0")

            if umsatz:

                if foreign_flag:
                    find_exrate(curr_date)

                    if exrate:
                        frate =  to_decimal(exrate.betrag)
                n_betrag =  to_decimal(umsatz.betrag) / to_decimal((fact) * to_decimal(frate) )
                n_serv =  to_decimal(n_betrag) * to_decimal(serv)
                n_tax =  to_decimal(n_betrag) * to_decimal(vat)

                if umsat.datum == to_date:
                    payment_list.t_day =  to_decimal(payment_list.t_day) + to_decimal(n_betrag)

                if price_decimal == 0:
                    n_betrag = to_decimal(round(n_betrag , 0))
                    n_serv = to_decimal(round(n_serv , 0))
                    n_tax = to_decimal(round(n_tax , 0))

            budget = db_session.query(Budget).filter(
                     (Budget.artnr == artikel.artnr) & (Budget.departement == artikel.departement) & (Budget.datum == curr_date)).first()

            if curr_date < from_date:

                if umsatz:
                    payment_list.ytd =  to_decimal(payment_list.ytd) + to_decimal(n_betrag)

                if budget:
                    payment_list.ytd_budget =  to_decimal(payment_list.ytd_budget) + to_decimal(budget.betrag)
            else:

                if umsatz:

                    if ytd_flag:
                        payment_list.ytd =  to_decimal(payment_list.ytd) + to_decimal(n_betrag)

                    if get_month(curr_date) == get_month(to_date):
                        payment_list.mtd =  to_decimal(payment_list.mtd) + to_decimal(mon_saldo[get_day(umsatz.datum) - 1]) + to_decimal(n_betrag)

                if budget:
                    payment_list.mtd_budget =  to_decimal(payment_list.mtd_budget) + to_decimal(budget.betrag)
            payment_list.variance =  to_decimal(payment_list.mtd) - to_decimal(payment_list.mtd_budget)


    def fill_tot_room():

        nonlocal rev_seg_list_list, rev_list_list, payable_list_list, stat_list_list, payment_list_list, gl_list_list, fb_sales_food_list, fb_sales_beverage_list, fb_sales_other_list, fb_sales_tot_list, rev_seg_list1_list, fb_sales_material_list, gsheet_link, ytd_flag, str1, str2, str3, st1, st2, st3, st4, st5, st6, st7, st8, st9, st10, st11, st12, st13, st14, st15, st16, st17, st18, st19, st20, st21, st22, st23, st24, st25, st26, st27, st28, st29, st30, st31, st32, st33, st34, st35, st36, st37, n, n1, n2, n3, n4, n5, n6, n7, n8, n9, n10, n11, n12, n13, n14, n15, n16, n17, n18, n19, n20, n21, n22, n23, n24, n25, n26, n27, n28, n29, n30, curr_date, start_date, datum1, serv, vat, vat2, fact, n_betrag, n_serv, n_tax, ly_betrag, dbudget_flag, yes_serv, yes_vat, yes_vat2, yes_fact, yes_betrag, date1, date2, temp_date2, temp_curr_date, l_today, st_date, foreign_nr, foreign_flag, tot_betrag, price_decimal, no_decimal, dept, dept1, zwkum, dper, mtd_per, ytd_per, tot_today, tot_today_per, tot_mtd, tot_mtd_per, tot_mtd_budget, tot_variance, tot_ytd, tot_ytd_budget, tot_ytd_per, tot_today1, tot_today_per1, tot_mtd1, tot_mtd_per1, tot_mtd_budget1, tot_variance1, tot_ytd1, tot_ytd_budget1, tot_ytd_per1, tot_today2, tot_today_per2, tot_mtd2, tot_mtd_per2, tot_mtd_budget2, tot_variance2, tot_ytd2, tot_ytd_budget2, tot_ytd_per2, tot_today3, tot_mtd3, tot_mtd_budget3, tot_variance3, tot_ytd3, tot_ytd_budget3, tot_today4, tot_mtd4, tot_mtd_budget4, tot_variance4, tot_ytd4, tot_ytd_budget4, tot_today5, tot_mtd5, tot_mtd_budget5, tot_variance5, tot_ytd5, tot_ytd_budget5, tot_today6, tot_mtd6, tot_mtd_budget6, tot_variance6, tot_ytd6, tot_ytd_budget6, tot_today7, tot_mtd7, tot_mtd_budget7, tot_variance7, tot_ytd7, tot_ytd_budget7, tot_tday_cov, tot_tday_avg, tot_tday_rev, tot_mtd_cov, tot_mtd_avg, tot_mtd_rev, tot_ytd_cov, tot_ytd_avg, tot_ytd_rev, t_today, t_today_per, t_mtd, t_mtd_per, t_mtd_budget, t_variance, t_ytd, t_ytd_budget, t_ytd_per, t_today1, t_today_per1, t_mtd1, t_mtd_per1, t_mtd_budget1, t_variance1, t_ytd1, t_ytd_budget1, t_ytd_per1, t_today11, t_today_per11, t_mtd11, t_mtd_per11, t_mtd_budget11, t_variance11, t_ytd11, t_ytd_budget11, t_ytd_per11, t_today2, t_today_per2, t_mtd2, t_mtd_per2, t_mtd_budget2, t_variance2, t_ytd2, t_ytd_budget2, t_ytd_per2, t_today3, t_today_per3, t_mtd3, t_mtd_per3, t_mtd_budget3, t_variance3, t_ytd3, t_ytd_budget3, t_ytd_per3, tdy_gl1, ytd_gl, curr_flag, curr_dept, ct, ct3, ct4, t_day_serv, mtd_serv, mtd_budget_serv, ytd_serv, ytd_budget_serv, variance_serv, t_day_tax, mtd_tax, mtd_budget_tax, ytd_tax, ytd_budget_tax, variance_tax, ct1, curr_flag1, ct2, banq_dept, frate, jan1, budget_flag, mon_saldo, mon_budget, foreign_curr, umsatz, waehrung, htparam, queasy, segment, artikel, hoteldpt, uebertrag, exrate, genstat, segmentstat, budget, zinrstat, zkstat
        nonlocal from_date, to_date
        nonlocal buff_umsatz, b_rev_list, b_rev_seg_list, b_rev_seg_list1, b_stat_list, brev_list, b_payment_list, bpayment_list, bpayable_list


        nonlocal rev_seg_list, rev_seg_list1, rev_list, rev_list_tax, rev_list_serv, payable_list, tot_list, stat_list, payment_list, segment_list, gl_list, fb_sales_food, fb_sales_beverage, fb_sales_other, fb_sales_tot, fb_sales_material, setup_revenue, setup_segment, setup_payment, setup_stat, setup_fbcover, buff_umsatz, b_rev_list, b_rev_seg_list, b_rev_seg_list1, b_stat_list, brev_list, b_payment_list, bpayment_list, bpayable_list
        nonlocal rev_seg_list_list, rev_seg_list1_list, rev_list_list, rev_list_tax_list, rev_list_serv_list, payable_list_list, tot_list_list, stat_list_list, payment_list_list, segment_list_list, gl_list_list, fb_sales_food_list, fb_sales_beverage_list, fb_sales_other_list, fb_sales_tot_list, fb_sales_material_list, setup_revenue_list, setup_segment_list, setup_payment_list, setup_stat_list, setup_fbcover_list

        datum:date = None
        anz:int = 0
        anz0:int = 0
        d_flag:bool = False
        dlmtd_flag:bool = False
        ct1 = ct1 + 1

        stat_list = query(stat_list_list, filters=(lambda stat_list: stat_list.flag.lower()  == ("tot-rm").lower()), first=True)

        if not stat_list:
            stat_list = Stat_list()
            stat_list_list.append(stat_list)

            stat_list.ct = ct1
            stat_list.descr = "Total Room"
            stat_list.flag = "tot-rm"


            for datum in date_range(datum1,to_date) :

                zinrstat = db_session.query(Zinrstat).filter(
                         (Zinrstat.datum == datum) & (func.lower(Zinrstat.zinr) == ("tot-rm").lower())).first()

                if zinrstat:
                    anz = zinrstat.zimmeranz
                else:
                    anz = anz0
                d_flag = None != zinrstat and (get_month(zinrstat.datum) == get_month(to_date)) and (get_year(zinrstat.datum) == get_year(to_date))

                if zinrstat:

                    if d_flag:
                        stat_list.mtd =  to_decimal(stat_list.mtd) + to_decimal(mon_saldo[get_day(zinrstat.datum) - 1]) + to_decimal(anz)

                if datum == to_date:
                    stat_list.t_day =  to_decimal(stat_list.t_day) + to_decimal(anz)

                if start_date != None:

                    if (datum < from_date) and (datum >= start_date):
                        stat_list.ytd =  to_decimal(stat_list.ytd) + to_decimal(anz)
                    else:

                        if ytd_flag and (datum >= start_date):
                            stat_list.ytd =  to_decimal(stat_list.ytd) + to_decimal(anz)
                else:

                    if (datum < from_date):
                        stat_list.ytd =  to_decimal(stat_list.ytd) + to_decimal(anz)
                    else:

                        if ytd_flag:
                            stat_list.ytd =  to_decimal(stat_list.ytd) + to_decimal(anz)

                if get_month(datum) == get_month(to_date):

                    setup_stat = query(setup_stat_list, filters=(lambda setup_stat: setup_stat.descr.lower()  == ("Total Room").lower()), first=True)

                    if setup_stat:

                        budget = db_session.query(Budget).filter(
                                 (Budget.artnr == setup_stat.artnr) & (Budget.departement == 0) & (Budget.datum == datum)).first()

                        if budget:
                            stat_list.mtd_budget =  to_decimal(stat_list.mtd_budget) + to_decimal(budget.betrag)


    def fill_tot_avail():

        nonlocal rev_seg_list_list, rev_list_list, payable_list_list, stat_list_list, payment_list_list, gl_list_list, fb_sales_food_list, fb_sales_beverage_list, fb_sales_other_list, fb_sales_tot_list, rev_seg_list1_list, fb_sales_material_list, gsheet_link, ytd_flag, str1, str2, str3, st1, st2, st3, st4, st5, st6, st7, st8, st9, st10, st11, st12, st13, st14, st15, st16, st17, st18, st19, st20, st21, st22, st23, st24, st25, st26, st27, st28, st29, st30, st31, st32, st33, st34, st35, st36, st37, n, n1, n2, n3, n4, n5, n6, n7, n8, n9, n10, n11, n12, n13, n14, n15, n16, n17, n18, n19, n20, n21, n22, n23, n24, n25, n26, n27, n28, n29, n30, curr_date, start_date, datum1, serv, vat, vat2, fact, n_betrag, n_serv, n_tax, ly_betrag, d_flag, dbudget_flag, dlmtd_flag, yes_serv, yes_vat, yes_vat2, yes_fact, yes_betrag, date1, date2, temp_date2, temp_curr_date, l_today, st_date, foreign_nr, foreign_flag, tot_betrag, price_decimal, no_decimal, dept, dept1, zwkum, dper, mtd_per, ytd_per, tot_today, tot_today_per, tot_mtd, tot_mtd_per, tot_mtd_budget, tot_variance, tot_ytd, tot_ytd_budget, tot_ytd_per, tot_today1, tot_today_per1, tot_mtd1, tot_mtd_per1, tot_mtd_budget1, tot_variance1, tot_ytd1, tot_ytd_budget1, tot_ytd_per1, tot_today2, tot_today_per2, tot_mtd2, tot_mtd_per2, tot_mtd_budget2, tot_variance2, tot_ytd2, tot_ytd_budget2, tot_ytd_per2, tot_today3, tot_mtd3, tot_mtd_budget3, tot_variance3, tot_ytd3, tot_ytd_budget3, tot_today4, tot_mtd4, tot_mtd_budget4, tot_variance4, tot_ytd4, tot_ytd_budget4, tot_today5, tot_mtd5, tot_mtd_budget5, tot_variance5, tot_ytd5, tot_ytd_budget5, tot_today6, tot_mtd6, tot_mtd_budget6, tot_variance6, tot_ytd6, tot_ytd_budget6, tot_today7, tot_mtd7, tot_mtd_budget7, tot_variance7, tot_ytd7, tot_ytd_budget7, tot_tday_cov, tot_tday_avg, tot_tday_rev, tot_mtd_cov, tot_mtd_avg, tot_mtd_rev, tot_ytd_cov, tot_ytd_avg, tot_ytd_rev, t_today, t_today_per, t_mtd, t_mtd_per, t_mtd_budget, t_variance, t_ytd, t_ytd_budget, t_ytd_per, t_today1, t_today_per1, t_mtd1, t_mtd_per1, t_mtd_budget1, t_variance1, t_ytd1, t_ytd_budget1, t_ytd_per1, t_today11, t_today_per11, t_mtd11, t_mtd_per11, t_mtd_budget11, t_variance11, t_ytd11, t_ytd_budget11, t_ytd_per11, t_today2, t_today_per2, t_mtd2, t_mtd_per2, t_mtd_budget2, t_variance2, t_ytd2, t_ytd_budget2, t_ytd_per2, t_today3, t_today_per3, t_mtd3, t_mtd_per3, t_mtd_budget3, t_variance3, t_ytd3, t_ytd_budget3, t_ytd_per3, tdy_gl1, ytd_gl, curr_flag, curr_dept, ct, ct3, ct4, t_day_serv, mtd_serv, mtd_budget_serv, ytd_serv, ytd_budget_serv, variance_serv, t_day_tax, mtd_tax, mtd_budget_tax, ytd_tax, ytd_budget_tax, variance_tax, ct1, curr_flag1, ct2, banq_dept, frate, jan1, budget_flag, mon_saldo, mon_budget, foreign_curr, umsatz, waehrung, htparam, queasy, segment, artikel, hoteldpt, uebertrag, exrate, genstat, segmentstat, budget, zinrstat, zkstat
        nonlocal from_date, to_date
        nonlocal buff_umsatz, b_rev_list, b_rev_seg_list, b_rev_seg_list1, b_stat_list, brev_list, b_payment_list, bpayment_list, bpayable_list


        nonlocal rev_seg_list, rev_seg_list1, rev_list, rev_list_tax, rev_list_serv, payable_list, tot_list, stat_list, payment_list, segment_list, gl_list, fb_sales_food, fb_sales_beverage, fb_sales_other, fb_sales_tot, fb_sales_material, setup_revenue, setup_segment, setup_payment, setup_stat, setup_fbcover, buff_umsatz, b_rev_list, b_rev_seg_list, b_rev_seg_list1, b_stat_list, brev_list, b_payment_list, bpayment_list, bpayable_list
        nonlocal rev_seg_list_list, rev_seg_list1_list, rev_list_list, rev_list_tax_list, rev_list_serv_list, payable_list_list, tot_list_list, stat_list_list, payment_list_list, segment_list_list, gl_list_list, fb_sales_food_list, fb_sales_beverage_list, fb_sales_other_list, fb_sales_tot_list, fb_sales_material_list, setup_revenue_list, setup_segment_list, setup_payment_list, setup_stat_list, setup_fbcover_list


        ct1 = ct1 + 1

        stat_list = query(stat_list_list, filters=(lambda stat_list: stat_list.flag.lower()  == ("tot-rmavail").lower()), first=True)

        if not stat_list:
            stat_list = Stat_list()
            stat_list_list.append(stat_list)

            stat_list.ct = ct1
            stat_list.descr = "Room Available"
            stat_list.flag = "tot-rmavail"

            for zkstat in db_session.query(Zkstat).filter(
                     (Zkstat.datum >= datum1) & (Zkstat.datum <= to_date)).order_by(Zkstat._recid).all():

                if zkstat.datum == to_date:
                    stat_list.t_day =  to_decimal(stat_list.t_day) + to_decimal(zkstat.anz100)

                if zkstat.datum < from_date:
                    stat_list.ytd =  to_decimal(stat_list.ytd) + to_decimal(zkstat.anz100)
                else:

                    if ytd_flag:
                        stat_list.ytd =  to_decimal(stat_list.ytd) + to_decimal(zkstat.anz100)

                if get_month(zkstat.datum) == get_month(to_date) and get_year(zkstat.datum) == get_year(to_date):
                    stat_list.mtd =  to_decimal(stat_list.mtd) + to_decimal(mon_saldo[get_day(zkstat.datum) - 1]) + to_decimal(zkstat.anz100)

            setup_stat = query(setup_stat_list, filters=(lambda setup_stat: setup_stat.descr.lower()  == ("Rooms Available").lower()), first=True)

            if setup_stat:

                budget = db_session.query(Budget).filter(
                         (Budget.artnr == setup_stat.artnr) & (Budget.departement == 0) & (Budget.datum == datum1)).first()

                if datum1 < from_date:
                    pass
                else:

                    if budget:
                        stat_list.mtd_budget =  to_decimal(stat_list.mtd_budget) + to_decimal(budget.betrag)


    def fill_inactive():

        nonlocal rev_seg_list_list, rev_list_list, payable_list_list, stat_list_list, payment_list_list, gl_list_list, fb_sales_food_list, fb_sales_beverage_list, fb_sales_other_list, fb_sales_tot_list, rev_seg_list1_list, fb_sales_material_list, gsheet_link, ytd_flag, str1, str2, str3, st1, st2, st3, st4, st5, st6, st7, st8, st9, st10, st11, st12, st13, st14, st15, st16, st17, st18, st19, st20, st21, st22, st23, st24, st25, st26, st27, st28, st29, st30, st31, st32, st33, st34, st35, st36, st37, n, n1, n2, n3, n4, n5, n6, n7, n8, n9, n10, n11, n12, n13, n14, n15, n16, n17, n18, n19, n20, n21, n22, n23, n24, n25, n26, n27, n28, n29, n30, curr_date, start_date, datum1, serv, vat, vat2, fact, n_betrag, n_serv, n_tax, ly_betrag, d_flag, dbudget_flag, dlmtd_flag, yes_serv, yes_vat, yes_vat2, yes_fact, yes_betrag, date1, date2, temp_date2, temp_curr_date, l_today, st_date, foreign_nr, foreign_flag, tot_betrag, price_decimal, no_decimal, dept, dept1, zwkum, dper, mtd_per, ytd_per, tot_today, tot_today_per, tot_mtd, tot_mtd_per, tot_mtd_budget, tot_variance, tot_ytd, tot_ytd_budget, tot_ytd_per, tot_today1, tot_today_per1, tot_mtd1, tot_mtd_per1, tot_mtd_budget1, tot_variance1, tot_ytd1, tot_ytd_budget1, tot_ytd_per1, tot_today2, tot_today_per2, tot_mtd2, tot_mtd_per2, tot_mtd_budget2, tot_variance2, tot_ytd2, tot_ytd_budget2, tot_ytd_per2, tot_today3, tot_mtd3, tot_mtd_budget3, tot_variance3, tot_ytd3, tot_ytd_budget3, tot_today4, tot_mtd4, tot_mtd_budget4, tot_variance4, tot_ytd4, tot_ytd_budget4, tot_today5, tot_mtd5, tot_mtd_budget5, tot_variance5, tot_ytd5, tot_ytd_budget5, tot_today6, tot_mtd6, tot_mtd_budget6, tot_variance6, tot_ytd6, tot_ytd_budget6, tot_today7, tot_mtd7, tot_mtd_budget7, tot_variance7, tot_ytd7, tot_ytd_budget7, tot_tday_cov, tot_tday_avg, tot_tday_rev, tot_mtd_cov, tot_mtd_avg, tot_mtd_rev, tot_ytd_cov, tot_ytd_avg, tot_ytd_rev, t_today, t_today_per, t_mtd, t_mtd_per, t_mtd_budget, t_variance, t_ytd, t_ytd_budget, t_ytd_per, t_today1, t_today_per1, t_mtd1, t_mtd_per1, t_mtd_budget1, t_variance1, t_ytd1, t_ytd_budget1, t_ytd_per1, t_today11, t_today_per11, t_mtd11, t_mtd_per11, t_mtd_budget11, t_variance11, t_ytd11, t_ytd_budget11, t_ytd_per11, t_today2, t_today_per2, t_mtd2, t_mtd_per2, t_mtd_budget2, t_variance2, t_ytd2, t_ytd_budget2, t_ytd_per2, t_today3, t_today_per3, t_mtd3, t_mtd_per3, t_mtd_budget3, t_variance3, t_ytd3, t_ytd_budget3, t_ytd_per3, tdy_gl1, ytd_gl, curr_flag, curr_dept, ct, ct3, ct4, t_day_serv, mtd_serv, mtd_budget_serv, ytd_serv, ytd_budget_serv, variance_serv, t_day_tax, mtd_tax, mtd_budget_tax, ytd_tax, ytd_budget_tax, variance_tax, ct1, curr_flag1, ct2, banq_dept, frate, jan1, budget_flag, mon_saldo, mon_budget, foreign_curr, umsatz, waehrung, htparam, queasy, segment, artikel, hoteldpt, uebertrag, exrate, genstat, segmentstat, budget, zinrstat, zkstat
        nonlocal from_date, to_date
        nonlocal buff_umsatz, b_rev_list, b_rev_seg_list, b_rev_seg_list1, b_stat_list, brev_list, b_payment_list, bpayment_list, bpayable_list


        nonlocal rev_seg_list, rev_seg_list1, rev_list, rev_list_tax, rev_list_serv, payable_list, tot_list, stat_list, payment_list, segment_list, gl_list, fb_sales_food, fb_sales_beverage, fb_sales_other, fb_sales_tot, fb_sales_material, setup_revenue, setup_segment, setup_payment, setup_stat, setup_fbcover, buff_umsatz, b_rev_list, b_rev_seg_list, b_rev_seg_list1, b_stat_list, brev_list, b_payment_list, bpayment_list, bpayable_list
        nonlocal rev_seg_list_list, rev_seg_list1_list, rev_list_list, rev_list_tax_list, rev_list_serv_list, payable_list_list, tot_list_list, stat_list_list, payment_list_list, segment_list_list, gl_list_list, fb_sales_food_list, fb_sales_beverage_list, fb_sales_other_list, fb_sales_tot_list, fb_sales_material_list, setup_revenue_list, setup_segment_list, setup_payment_list, setup_stat_list, setup_fbcover_list

        tday1:int = 0
        tday2:int = 0
        tday3:int = 0
        mtd1:int = 0
        mtd2:int = 0
        mtd3:int = 0
        ytd1:int = 0
        ytd2:int = 0
        ytd3:int = 0
        ct1 = ct1 + 1

        stat_list = query(stat_list_list, filters=(lambda stat_list: stat_list.flag.lower()  == ("tot-inactive").lower()), first=True)

        if not stat_list:
            stat_list = Stat_list()
            stat_list_list.append(stat_list)

            stat_list.ct = ct1
            stat_list.descr = "InactiveRoom"
            stat_list.flag = "tot-inactive"

            for b_stat_list in query(b_stat_list_list):

                if b_stat_list.flag.lower()  == ("tot-rm").lower() :
                    tday1 = b_stat_list.t_day
                    mtd1 = b_stat_list.mtd
                    ytd1 = b_stat_list.ytd

                if b_stat_list.flag.lower()  == ("tot-rmavail").lower() :
                    tday2 = b_stat_list.t_day
                    mtd2 = b_stat_list.mtd
                    ytd2 = b_stat_list.ytd


            stat_list.t_day =  to_decimal(tday1) - to_decimal(tday2)
            stat_list.mtd =  to_decimal(mtd1) - to_decimal(mtd2)
            stat_list.ytd =  to_decimal(ytd1) - to_decimal(ytd2)


    def fill_rmstat(key_word:str):

        nonlocal rev_seg_list_list, rev_list_list, payable_list_list, stat_list_list, payment_list_list, gl_list_list, fb_sales_food_list, fb_sales_beverage_list, fb_sales_other_list, fb_sales_tot_list, rev_seg_list1_list, fb_sales_material_list, gsheet_link, ytd_flag, str1, str2, str3, st1, st2, st3, st4, st5, st6, st7, st8, st9, st10, st11, st12, st13, st14, st15, st16, st17, st18, st19, st20, st21, st22, st23, st24, st25, st26, st27, st28, st29, st30, st31, st32, st33, st34, st35, st36, st37, n, n1, n2, n3, n4, n5, n6, n7, n8, n9, n10, n11, n12, n13, n14, n15, n16, n17, n18, n19, n20, n21, n22, n23, n24, n25, n26, n27, n28, n29, n30, curr_date, start_date, datum1, serv, vat, vat2, fact, n_betrag, n_serv, n_tax, ly_betrag, dbudget_flag, yes_serv, yes_vat, yes_vat2, yes_fact, yes_betrag, date1, date2, temp_date2, temp_curr_date, l_today, st_date, foreign_nr, foreign_flag, tot_betrag, price_decimal, no_decimal, dept, dept1, zwkum, dper, mtd_per, ytd_per, tot_today, tot_today_per, tot_mtd, tot_mtd_per, tot_mtd_budget, tot_variance, tot_ytd, tot_ytd_budget, tot_ytd_per, tot_today1, tot_today_per1, tot_mtd1, tot_mtd_per1, tot_mtd_budget1, tot_variance1, tot_ytd1, tot_ytd_budget1, tot_ytd_per1, tot_today2, tot_today_per2, tot_mtd2, tot_mtd_per2, tot_mtd_budget2, tot_variance2, tot_ytd2, tot_ytd_budget2, tot_ytd_per2, tot_today3, tot_mtd3, tot_mtd_budget3, tot_variance3, tot_ytd3, tot_ytd_budget3, tot_today4, tot_mtd4, tot_mtd_budget4, tot_variance4, tot_ytd4, tot_ytd_budget4, tot_today5, tot_mtd5, tot_mtd_budget5, tot_variance5, tot_ytd5, tot_ytd_budget5, tot_today6, tot_mtd6, tot_mtd_budget6, tot_variance6, tot_ytd6, tot_ytd_budget6, tot_today7, tot_mtd7, tot_mtd_budget7, tot_variance7, tot_ytd7, tot_ytd_budget7, tot_tday_cov, tot_tday_avg, tot_tday_rev, tot_mtd_cov, tot_mtd_avg, tot_mtd_rev, tot_ytd_cov, tot_ytd_avg, tot_ytd_rev, t_today, t_today_per, t_mtd, t_mtd_per, t_mtd_budget, t_variance, t_ytd, t_ytd_budget, t_ytd_per, t_today1, t_today_per1, t_mtd1, t_mtd_per1, t_mtd_budget1, t_variance1, t_ytd1, t_ytd_budget1, t_ytd_per1, t_today11, t_today_per11, t_mtd11, t_mtd_per11, t_mtd_budget11, t_variance11, t_ytd11, t_ytd_budget11, t_ytd_per11, t_today2, t_today_per2, t_mtd2, t_mtd_per2, t_mtd_budget2, t_variance2, t_ytd2, t_ytd_budget2, t_ytd_per2, t_today3, t_today_per3, t_mtd3, t_mtd_per3, t_mtd_budget3, t_variance3, t_ytd3, t_ytd_budget3, t_ytd_per3, tdy_gl1, ytd_gl, curr_flag, curr_dept, ct, ct3, ct4, t_day_serv, mtd_serv, mtd_budget_serv, ytd_serv, ytd_budget_serv, variance_serv, t_day_tax, mtd_tax, mtd_budget_tax, ytd_tax, ytd_budget_tax, variance_tax, ct1, curr_flag1, ct2, banq_dept, frate, jan1, budget_flag, mon_saldo, mon_budget, foreign_curr, umsatz, waehrung, htparam, queasy, segment, artikel, hoteldpt, uebertrag, exrate, genstat, segmentstat, budget, zinrstat, zkstat
        nonlocal from_date, to_date
        nonlocal buff_umsatz, b_rev_list, b_rev_seg_list, b_rev_seg_list1, b_stat_list, brev_list, b_payment_list, bpayment_list, bpayable_list


        nonlocal rev_seg_list, rev_seg_list1, rev_list, rev_list_tax, rev_list_serv, payable_list, tot_list, stat_list, payment_list, segment_list, gl_list, fb_sales_food, fb_sales_beverage, fb_sales_other, fb_sales_tot, fb_sales_material, setup_revenue, setup_segment, setup_payment, setup_stat, setup_fbcover, buff_umsatz, b_rev_list, b_rev_seg_list, b_rev_seg_list1, b_stat_list, brev_list, b_payment_list, bpayment_list, bpayable_list
        nonlocal rev_seg_list_list, rev_seg_list1_list, rev_list_list, rev_list_tax_list, rev_list_serv_list, payable_list_list, tot_list_list, stat_list_list, payment_list_list, segment_list_list, gl_list_list, fb_sales_food_list, fb_sales_beverage_list, fb_sales_other_list, fb_sales_tot_list, fb_sales_material_list, setup_revenue_list, setup_segment_list, setup_payment_list, setup_stat_list, setup_fbcover_list

        datum:date = None
        anz:int = 0
        anz0:int = 0
        d_flag:bool = False
        dlmtd_flag:bool = False
        cur_key:str = ""
        ct1 = ct1 + 1

        stat_list = query(stat_list_list, filters=(lambda stat_list: stat_list.flag.lower()  == (key_word).lower()), first=True)

        if not stat_list:
            stat_list = Stat_list()
            stat_list_list.append(stat_list)

            stat_list.ct = ct1
            stat_list.flag = key_word

            if key_word.lower()  == ("ooo").lower() :
                stat_list.descr = "Out of Order Rooms"

            elif key_word.lower()  == ("oos").lower() :
                stat_list.descr = "Rooms Occupied"

            elif key_word.lower()  == ("dayuse").lower() :
                stat_list.descr = "Day Use"

            elif key_word.lower()  == ("No-Show").lower() :
                stat_list.descr = "No Show"

            elif key_word.lower()  == ("arrival-WIG").lower() :
                stat_list.descr = "Walk in Guest"

            elif key_word.lower()  == ("NewRes").lower() :
                stat_list.descr = "Reservation Made Today"

            elif key_word.lower()  == ("CancRes").lower() :
                stat_list.descr = "Cancellation For Today"

            elif key_word.lower()  == ("Early-CO").lower() :
                stat_list.descr = "Early Check Out"

            elif key_word.lower()  == ("arrival").lower() :
                stat_list.descr = "Room Arrivals"

            elif key_word.lower()  == ("pers-arrival").lower() :
                cur_key = "pers-arrival"
                key_word = "arrival"
                stat_list.descr = "Person Arrivals"

            elif key_word.lower()  == ("departure").lower() :
                stat_list.descr = "Room Departures"

            elif key_word.lower()  == ("pers-depature").lower() :
                cur_key = "pers-depature"
                key_word = "departure"
                stat_list.descr = "Person Depatures"

            elif key_word.lower()  == ("ArrTmrw").lower() :
                stat_list.descr = "Room Arrivals Tomorrow"

            elif key_word.lower()  == ("pers-ArrTmrw").lower() :
                cur_key = "pers-ArrTmrw"
                key_word = "ArrTmrw"
                stat_list.descr = "Person Arrivals Tomorrow"

            elif key_word.lower()  == ("DepTmrw").lower() :
                stat_list.descr = "Room Departures Tomorrow"

            elif key_word.lower()  == ("pers-DepTmrw").lower() :
                cur_key = "pers-DepTmrw"
                key_word = "DepTmrw"
                stat_list.descr = "Person Departures Tomorrow"

            for zinrstat in db_session.query(Zinrstat).filter(
                     (Zinrstat.datum >= datum1) & (Zinrstat.datum <= to_date) & (func.lower(Zinrstat.zinr) == (key_word).lower())).order_by(Zinrstat._recid).all():
                d_flag = (get_month(zinrstat.datum) == get_month(to_date)) and (get_year(zinrstat.datum) == get_year(to_date))

                if d_flag:

                    if substring(cur_key, 0, 4) == ("pers").lower() :
                        stat_list.mtd =  to_decimal(stat_list.mtd) + to_decimal(mon_saldo[get_day(zinrstat.datum) - 1]) + to_decimal(zinrstat.personen)
                    else:
                        stat_list.mtd =  to_decimal(stat_list.mtd) + to_decimal(mon_saldo[get_day(zinrstat.datum) - 1]) + to_decimal(zinrstat.zimmeranz)

                if zinrstat.datum == to_date:

                    if substring(cur_key, 0, 4) == ("pers").lower() :
                        stat_list.t_day =  to_decimal(stat_list.t_day) + to_decimal(zinrstat.personen)
                    else:
                        stat_list.t_day =  to_decimal(stat_list.t_day) + to_decimal(zinrstat.zimmeranz)

                if zinrstat.datum < from_date:

                    if substring(cur_key, 0, 4) == ("pers").lower() :
                        stat_list.ytd =  to_decimal(stat_list.ytd) + to_decimal(zinrstat.personen)
                    else:
                        stat_list.ytd =  to_decimal(stat_list.ytd) + to_decimal(zinrstat.zimmeranz)
                else:

                    if ytd_flag:

                        if substring(cur_key, 0, 4) == ("pers").lower() :
                            stat_list.ytd =  to_decimal(stat_list.ytd) + to_decimal(zinrstat.personen)
                        else:
                            stat_list.ytd =  to_decimal(stat_list.ytd) + to_decimal(zinrstat.zimmeranz)

            for setup_stat in query(setup_stat_list):

                budget = db_session.query(Budget).filter(
                         (Budget.artnr == setup_stat.artnr) & (Budget.departement == 0) & (Budget.datum == curr_date)).first()

                if curr_date < from_date:
                    pass
                else:

                    if budget:

                        if setup_stat.descr.lower()  == ("OOO Room").lower()  and key_word.lower()  == ("ooo").lower() :
                            stat_list.mtd_budget =  to_decimal(stat_list.mtd_budget) + to_decimal(budget.betrag)

                        elif setup_stat.descr.lower()  == ("Rooms Occupied").lower()  and key_word.lower()  == ("occ").lower() :
                            stat_list.mtd_budget =  to_decimal(stat_list.mtd_budget) + to_decimal(budget.betrag)


    def fill_rmocc():

        nonlocal rev_seg_list_list, rev_list_list, payable_list_list, stat_list_list, payment_list_list, gl_list_list, fb_sales_food_list, fb_sales_beverage_list, fb_sales_other_list, fb_sales_tot_list, rev_seg_list1_list, fb_sales_material_list, gsheet_link, ytd_flag, str1, str2, str3, st1, st2, st3, st4, st5, st6, st7, st8, st9, st10, st11, st12, st13, st14, st15, st16, st17, st18, st19, st20, st21, st22, st23, st24, st25, st26, st27, st28, st29, st30, st31, st32, st33, st34, st35, st36, st37, n, n1, n2, n3, n4, n5, n6, n7, n8, n9, n10, n11, n12, n13, n14, n15, n16, n17, n18, n19, n20, n21, n22, n23, n24, n25, n26, n27, n28, n29, n30, start_date, serv, vat, vat2, fact, n_betrag, n_serv, n_tax, ly_betrag, yes_serv, yes_vat, yes_vat2, yes_fact, yes_betrag, date1, date2, temp_date2, temp_curr_date, l_today, st_date, foreign_nr, foreign_flag, tot_betrag, price_decimal, no_decimal, dept, dept1, zwkum, dper, mtd_per, ytd_per, tot_today, tot_today_per, tot_mtd, tot_mtd_per, tot_mtd_budget, tot_variance, tot_ytd, tot_ytd_budget, tot_ytd_per, tot_today1, tot_today_per1, tot_mtd1, tot_mtd_per1, tot_mtd_budget1, tot_variance1, tot_ytd1, tot_ytd_budget1, tot_ytd_per1, tot_today2, tot_today_per2, tot_mtd2, tot_mtd_per2, tot_mtd_budget2, tot_variance2, tot_ytd2, tot_ytd_budget2, tot_ytd_per2, tot_today3, tot_mtd3, tot_mtd_budget3, tot_variance3, tot_ytd3, tot_ytd_budget3, tot_today4, tot_mtd4, tot_mtd_budget4, tot_variance4, tot_ytd4, tot_ytd_budget4, tot_today5, tot_mtd5, tot_mtd_budget5, tot_variance5, tot_ytd5, tot_ytd_budget5, tot_today6, tot_mtd6, tot_mtd_budget6, tot_variance6, tot_ytd6, tot_ytd_budget6, tot_today7, tot_mtd7, tot_mtd_budget7, tot_variance7, tot_ytd7, tot_ytd_budget7, tot_tday_cov, tot_tday_avg, tot_tday_rev, tot_mtd_cov, tot_mtd_avg, tot_mtd_rev, tot_ytd_cov, tot_ytd_avg, tot_ytd_rev, t_today, t_today_per, t_mtd, t_mtd_per, t_mtd_budget, t_variance, t_ytd, t_ytd_budget, t_ytd_per, t_today1, t_today_per1, t_mtd1, t_mtd_per1, t_mtd_budget1, t_variance1, t_ytd1, t_ytd_budget1, t_ytd_per1, t_today11, t_today_per11, t_mtd11, t_mtd_per11, t_mtd_budget11, t_variance11, t_ytd11, t_ytd_budget11, t_ytd_per11, t_today2, t_today_per2, t_mtd2, t_mtd_per2, t_mtd_budget2, t_variance2, t_ytd2, t_ytd_budget2, t_ytd_per2, t_today3, t_today_per3, t_mtd3, t_mtd_per3, t_mtd_budget3, t_variance3, t_ytd3, t_ytd_budget3, t_ytd_per3, tdy_gl1, ytd_gl, curr_flag, curr_dept, ct, ct3, ct4, t_day_serv, mtd_serv, mtd_budget_serv, ytd_serv, ytd_budget_serv, variance_serv, t_day_tax, mtd_tax, mtd_budget_tax, ytd_tax, ytd_budget_tax, variance_tax, ct1, curr_flag1, ct2, banq_dept, frate, jan1, budget_flag, mon_saldo, mon_budget, foreign_curr, umsatz, waehrung, htparam, queasy, segment, artikel, hoteldpt, uebertrag, exrate, genstat, segmentstat, budget, zinrstat, zkstat
        nonlocal from_date, to_date
        nonlocal buff_umsatz, b_rev_list, b_rev_seg_list, b_rev_seg_list1, b_stat_list, brev_list, b_payment_list, bpayment_list, bpayable_list


        nonlocal rev_seg_list, rev_seg_list1, rev_list, rev_list_tax, rev_list_serv, payable_list, tot_list, stat_list, payment_list, segment_list, gl_list, fb_sales_food, fb_sales_beverage, fb_sales_other, fb_sales_tot, fb_sales_material, setup_revenue, setup_segment, setup_payment, setup_stat, setup_fbcover, buff_umsatz, b_rev_list, b_rev_seg_list, b_rev_seg_list1, b_stat_list, brev_list, b_payment_list, bpayment_list, bpayable_list
        nonlocal rev_seg_list_list, rev_seg_list1_list, rev_list_list, rev_list_tax_list, rev_list_serv_list, payable_list_list, tot_list_list, stat_list_list, payment_list_list, segment_list_list, gl_list_list, fb_sales_food_list, fb_sales_beverage_list, fb_sales_other_list, fb_sales_tot_list, fb_sales_material_list, setup_revenue_list, setup_segment_list, setup_payment_list, setup_stat_list, setup_fbcover_list

        curr_date:date = None
        datum1:date = None
        datum2:date = None
        d_flag:bool = False
        dbudget_flag:bool = False
        dlmtd_flag:bool = False
        frate1:decimal = to_decimal("0.0")

        if ytd_flag:
            datum1 = jan1
        else:
            datum1 = from_date
        ct1 = ct1 + 1
        stat_list = Stat_list()
        stat_list_list.append(stat_list)

        stat_list.ct = ct1
        stat_list.descr = "Rooms Occupied"
        stat_list.flag = "occ"

        segmentstat_obj_list = []
        for segmentstat, segment in db_session.query(Segmentstat, Segment).join(Segment,(Segment.segmentcode == Segmentstat.segmentcode)).filter(
                 (Segmentstat.datum >= datum1) & (Segmentstat.datum <= to_date)).order_by(Segmentstat._recid).all():
            if segmentstat._recid in segmentstat_obj_list:
                continue
            else:
                segmentstat_obj_list.append(segmentstat._recid)


            frate =  to_decimal("1")

            if foreign_flag:
                find_exrate(segmentstat.datum)

                if exrate:
                    frate =  to_decimal(exrate.betrag)

            if segmentstat.datum == to_date:
                stat_list.t_day =  to_decimal(stat_list.t_day) + to_decimal(segmentstat.zimmeranz)

            if get_month(segmentstat.datum) == get_month(to_date):
                stat_list.mtd =  to_decimal(stat_list.mtd) + to_decimal(segmentstat.zimmeranz)
            stat_list.ytd =  to_decimal(stat_list.ytd) + to_decimal(segmentstat.zimmeranz)

        setup_stat = query(setup_stat_list, filters=(lambda setup_stat: setup_stat.descr.lower()  == ("Rooms Occupied").lower()), first=True)

        if setup_stat:

            for budget in db_session.query(Budget).filter(
                     (Budget.artnr == setup_stat.artnr) & (Budget.departement == 0) & (Budget.datum >= from_date) & (Budget.datum <= to_date)).order_by(Budget._recid).all():
                stat_list.mtd_budget =  to_decimal(stat_list.mtd_budget) + to_decimal(budget.betrag)


    def fill_stat(key_word:str):

        nonlocal rev_seg_list_list, rev_list_list, payable_list_list, stat_list_list, payment_list_list, gl_list_list, fb_sales_food_list, fb_sales_beverage_list, fb_sales_other_list, fb_sales_tot_list, rev_seg_list1_list, fb_sales_material_list, gsheet_link, ytd_flag, str1, str2, str3, st1, st2, st3, st4, st5, st6, st7, st8, st9, st10, st11, st12, st13, st14, st15, st16, st17, st18, st19, st20, st21, st22, st23, st24, st25, st26, st27, st28, st29, st30, st31, st32, st33, st34, st35, st36, st37, n, n1, n2, n3, n4, n5, n6, n7, n8, n9, n10, n11, n12, n13, n14, n15, n16, n17, n18, n19, n20, n21, n22, n23, n24, n25, n26, n27, n28, n29, n30, curr_date, start_date, datum1, serv, vat, vat2, fact, n_betrag, n_serv, n_tax, ly_betrag, d_flag, dbudget_flag, dlmtd_flag, yes_serv, yes_vat, yes_vat2, yes_fact, yes_betrag, date1, date2, temp_date2, temp_curr_date, l_today, st_date, foreign_nr, foreign_flag, tot_betrag, price_decimal, no_decimal, dept, dept1, zwkum, dper, mtd_per, ytd_per, tot_today, tot_today_per, tot_mtd, tot_mtd_per, tot_mtd_budget, tot_variance, tot_ytd, tot_ytd_budget, tot_ytd_per, tot_today1, tot_today_per1, tot_mtd1, tot_mtd_per1, tot_mtd_budget1, tot_variance1, tot_ytd1, tot_ytd_budget1, tot_ytd_per1, tot_today2, tot_today_per2, tot_mtd2, tot_mtd_per2, tot_mtd_budget2, tot_variance2, tot_ytd2, tot_ytd_budget2, tot_ytd_per2, tot_today3, tot_mtd3, tot_mtd_budget3, tot_variance3, tot_ytd3, tot_ytd_budget3, tot_today4, tot_mtd4, tot_mtd_budget4, tot_variance4, tot_ytd4, tot_ytd_budget4, tot_today5, tot_mtd5, tot_mtd_budget5, tot_variance5, tot_ytd5, tot_ytd_budget5, tot_today6, tot_mtd6, tot_mtd_budget6, tot_variance6, tot_ytd6, tot_ytd_budget6, tot_today7, tot_mtd7, tot_mtd_budget7, tot_variance7, tot_ytd7, tot_ytd_budget7, tot_tday_cov, tot_tday_avg, tot_tday_rev, tot_mtd_cov, tot_mtd_avg, tot_mtd_rev, tot_ytd_cov, tot_ytd_avg, tot_ytd_rev, t_today, t_today_per, t_mtd, t_mtd_per, t_mtd_budget, t_variance, t_ytd, t_ytd_budget, t_ytd_per, t_today1, t_today_per1, t_mtd1, t_mtd_per1, t_mtd_budget1, t_variance1, t_ytd1, t_ytd_budget1, t_ytd_per1, t_today11, t_today_per11, t_mtd11, t_mtd_per11, t_mtd_budget11, t_variance11, t_ytd11, t_ytd_budget11, t_ytd_per11, t_today2, t_today_per2, t_mtd2, t_mtd_per2, t_mtd_budget2, t_variance2, t_ytd2, t_ytd_budget2, t_ytd_per2, t_today3, t_today_per3, t_mtd3, t_mtd_per3, t_mtd_budget3, t_variance3, t_ytd3, t_ytd_budget3, t_ytd_per3, tdy_gl1, ytd_gl, curr_flag, curr_dept, ct, ct3, ct4, t_day_serv, mtd_serv, mtd_budget_serv, ytd_serv, ytd_budget_serv, variance_serv, t_day_tax, mtd_tax, mtd_budget_tax, ytd_tax, ytd_budget_tax, variance_tax, ct1, curr_flag1, ct2, banq_dept, frate, jan1, budget_flag, mon_saldo, mon_budget, foreign_curr, umsatz, waehrung, htparam, queasy, segment, artikel, hoteldpt, uebertrag, exrate, genstat, segmentstat, budget, zinrstat, zkstat
        nonlocal from_date, to_date
        nonlocal buff_umsatz, b_rev_list, b_rev_seg_list, b_rev_seg_list1, b_stat_list, brev_list, b_payment_list, bpayment_list, bpayable_list


        nonlocal rev_seg_list, rev_seg_list1, rev_list, rev_list_tax, rev_list_serv, payable_list, tot_list, stat_list, payment_list, segment_list, gl_list, fb_sales_food, fb_sales_beverage, fb_sales_other, fb_sales_tot, fb_sales_material, setup_revenue, setup_segment, setup_payment, setup_stat, setup_fbcover, buff_umsatz, b_rev_list, b_rev_seg_list, b_rev_seg_list1, b_stat_list, brev_list, b_payment_list, bpayment_list, bpayable_list
        nonlocal rev_seg_list_list, rev_seg_list1_list, rev_list_list, rev_list_tax_list, rev_list_serv_list, payable_list_list, tot_list_list, stat_list_list, payment_list_list, segment_list_list, gl_list_list, fb_sales_food_list, fb_sales_beverage_list, fb_sales_other_list, fb_sales_tot_list, fb_sales_material_list, setup_revenue_list, setup_segment_list, setup_payment_list, setup_stat_list, setup_fbcover_list

        tday1:int = 0
        tday2:int = 0
        tday3:int = 0
        mtd1:int = 0
        mtd2:int = 0
        mtd3:int = 0
        ytd1:int = 0
        ytd2:int = 0
        ytd3:int = 0
        ct1 = ct1 + 1

        stat_list = query(stat_list_list, filters=(lambda stat_list: stat_list.flag.lower()  == (key_word).lower()), first=True)

        if not stat_list:
            stat_list = Stat_list()
            stat_list_list.append(stat_list)

            stat_list.ct = ct1
            stat_list.flag = key_word

            if key_word.lower()  == ("vacant").lower() :
                stat_list.descr = "Vacant Rooms"

            for b_stat_list in query(b_stat_list_list):

                if b_stat_list.flag.lower()  == ("tot-rmavail").lower() :
                    tday1 = b_stat_list.t_day
                    mtd1 = b_stat_list.mtd
                    ytd1 = b_stat_list.ytd

                if b_stat_list.flag.lower()  == ("ooo").lower() :
                    tday2 = b_stat_list.t_day
                    mtd2 = b_stat_list.mtd
                    ytd2 = b_stat_list.ytd

                if b_stat_list.flag.lower()  == ("occ").lower() :
                    tday3 = b_stat_list.t_day
                    mtd3 = b_stat_list.mtd
                    ytd3 = b_stat_list.ytd


            stat_list.t_day =  to_decimal(tday1) - to_decimal(tday2) - to_decimal(tday3)
            stat_list.mtd =  to_decimal(mtd1) - to_decimal(mtd2) - to_decimal(mtd3)
            stat_list.ytd =  to_decimal(ytd1) - to_decimal(ytd2) - to_decimal(ytd3)

            setup_stat = query(setup_stat_list, filters=(lambda setup_stat: setup_stat.descr.lower()  == ("Vacant Rooms").lower()), first=True)

            if setup_stat:

                for budget in db_session.query(Budget).filter(
                         (Budget.artnr == setup_stat.artnr) & (Budget.departement == 0) & (Budget.datum >= from_date) & (Budget.datum >= to_date)).order_by(Budget._recid).all():
                    stat_list.mtd_budget =  to_decimal(stat_list.mtd_budget) + to_decimal(budget.betrag)


    def fill_segm(key_word:str):

        nonlocal rev_seg_list_list, rev_list_list, payable_list_list, stat_list_list, payment_list_list, gl_list_list, fb_sales_food_list, fb_sales_beverage_list, fb_sales_other_list, fb_sales_tot_list, rev_seg_list1_list, fb_sales_material_list, gsheet_link, ytd_flag, str1, str2, str3, st1, st2, st3, st4, st5, st6, st7, st8, st9, st10, st11, st12, st13, st14, st15, st16, st17, st18, st19, st20, st21, st22, st23, st24, st25, st26, st27, st28, st29, st30, st31, st32, st33, st34, st35, st36, st37, n, n1, n2, n3, n4, n5, n6, n7, n8, n9, n10, n11, n12, n13, n14, n15, n16, n17, n18, n19, n20, n21, n22, n23, n24, n25, n26, n27, n28, n29, n30, curr_date, start_date, datum1, serv, vat, vat2, fact, n_betrag, n_serv, n_tax, ly_betrag, dbudget_flag, dlmtd_flag, yes_serv, yes_vat, yes_vat2, yes_fact, yes_betrag, date1, date2, temp_date2, temp_curr_date, l_today, st_date, foreign_nr, foreign_flag, tot_betrag, price_decimal, no_decimal, dept, dept1, zwkum, dper, mtd_per, ytd_per, tot_today, tot_today_per, tot_mtd, tot_mtd_per, tot_mtd_budget, tot_variance, tot_ytd, tot_ytd_budget, tot_ytd_per, tot_today1, tot_today_per1, tot_mtd1, tot_mtd_per1, tot_mtd_budget1, tot_variance1, tot_ytd1, tot_ytd_budget1, tot_ytd_per1, tot_today2, tot_today_per2, tot_mtd2, tot_mtd_per2, tot_mtd_budget2, tot_variance2, tot_ytd2, tot_ytd_budget2, tot_ytd_per2, tot_today3, tot_mtd3, tot_mtd_budget3, tot_variance3, tot_ytd3, tot_ytd_budget3, tot_today4, tot_mtd4, tot_mtd_budget4, tot_variance4, tot_ytd4, tot_ytd_budget4, tot_today5, tot_mtd5, tot_mtd_budget5, tot_variance5, tot_ytd5, tot_ytd_budget5, tot_today6, tot_mtd6, tot_mtd_budget6, tot_variance6, tot_ytd6, tot_ytd_budget6, tot_today7, tot_mtd7, tot_mtd_budget7, tot_variance7, tot_ytd7, tot_ytd_budget7, tot_tday_cov, tot_tday_avg, tot_tday_rev, tot_mtd_cov, tot_mtd_avg, tot_mtd_rev, tot_ytd_cov, tot_ytd_avg, tot_ytd_rev, t_today, t_today_per, t_mtd, t_mtd_per, t_mtd_budget, t_variance, t_ytd, t_ytd_budget, t_ytd_per, t_today1, t_today_per1, t_mtd1, t_mtd_per1, t_mtd_budget1, t_variance1, t_ytd1, t_ytd_budget1, t_ytd_per1, t_today11, t_today_per11, t_mtd11, t_mtd_per11, t_mtd_budget11, t_variance11, t_ytd11, t_ytd_budget11, t_ytd_per11, t_today2, t_today_per2, t_mtd2, t_mtd_per2, t_mtd_budget2, t_variance2, t_ytd2, t_ytd_budget2, t_ytd_per2, t_today3, t_today_per3, t_mtd3, t_mtd_per3, t_mtd_budget3, t_variance3, t_ytd3, t_ytd_budget3, t_ytd_per3, tdy_gl1, ytd_gl, curr_flag, curr_dept, ct, ct3, ct4, t_day_serv, mtd_serv, mtd_budget_serv, ytd_serv, ytd_budget_serv, variance_serv, t_day_tax, mtd_tax, mtd_budget_tax, ytd_tax, ytd_budget_tax, variance_tax, ct1, curr_flag1, ct2, banq_dept, frate, jan1, budget_flag, mon_saldo, mon_budget, foreign_curr, umsatz, waehrung, htparam, queasy, segment, artikel, hoteldpt, uebertrag, exrate, genstat, segmentstat, budget, zinrstat, zkstat
        nonlocal from_date, to_date
        nonlocal buff_umsatz, b_rev_list, b_rev_seg_list, b_rev_seg_list1, b_stat_list, brev_list, b_payment_list, bpayment_list, bpayable_list


        nonlocal rev_seg_list, rev_seg_list1, rev_list, rev_list_tax, rev_list_serv, payable_list, tot_list, stat_list, payment_list, segment_list, gl_list, fb_sales_food, fb_sales_beverage, fb_sales_other, fb_sales_tot, fb_sales_material, setup_revenue, setup_segment, setup_payment, setup_stat, setup_fbcover, buff_umsatz, b_rev_list, b_rev_seg_list, b_rev_seg_list1, b_stat_list, brev_list, b_payment_list, bpayment_list, bpayable_list
        nonlocal rev_seg_list_list, rev_seg_list1_list, rev_list_list, rev_list_tax_list, rev_list_serv_list, payable_list_list, tot_list_list, stat_list_list, payment_list_list, segment_list_list, gl_list_list, fb_sales_food_list, fb_sales_beverage_list, fb_sales_other_list, fb_sales_tot_list, fb_sales_material_list, setup_revenue_list, setup_segment_list, setup_payment_list, setup_stat_list, setup_fbcover_list

        d_flag:bool = False
        mm:int = 0
        frate1:decimal = to_decimal("0.0")
        mm = get_month(to_date)
        ct1 = ct1 + 1

        if key_word.lower()  == ("HSE").lower() :

            segment = db_session.query(Segment).filter(
                     (Segment.betriebsnr == 2)).first()

        elif key_word.lower()  == ("COM").lower() :

            segment = db_session.query(Segment).filter(
                     (Segment.betriebsnr == 1)).first()

        if segment:
            stat_list = Stat_list()
            stat_list_list.append(stat_list)

            stat_list.ct = ct1
            stat_list.flag = key_word

            if key_word.lower()  == ("HSE").lower() :
                stat_list.descr = "House Uses"

            elif key_word.lower()  == ("COM").lower() :
                stat_list.descr = "Complimentary"

            for genstat in db_session.query(Genstat).filter(
                     (Genstat.segmentcode == segment.segmentcode) & (Genstat.datum >= datum1) & (Genstat.datum <= to_date) & (Genstat.resstatus != 13) & (Genstat.segmentcode != 0) & (Genstat.nationnr != 0) & (Genstat.zinr != "") & (Genstat.res_logic[inc_value(1))]).order_by(Genstat._recid).all():

                if foreign_flag:
                    find_exrate(genstat.datum)

                    if exrate:
                        frate =  to_decimal(exrate.betrag)
                d_flag = (get_month(genstat.datum) == get_month(to_date)) and (get_year(genstat.datum) == get_year(to_date))

                if genstat.datum == to_date:
                    stat_list.t_day =  to_decimal(stat_list.t_day) + to_decimal("1")

                if get_month(genstat.datum) == mm:
                    stat_list.mtd =  to_decimal(stat_list.mtd) + to_decimal(mon_saldo[get_day(genstat.datum) - 1]) + to_decimal("1")
                stat_list.ytd =  to_decimal(stat_list.ytd) + to_decimal("1")

            for segmentstat in db_session.query(Segmentstat).filter(
                     (Segmentstat.datum >= datum1) & (Segmentstat.datum <= to_date) & (Segmentstat.segmentcode == segment_list.segmentcode)).order_by(Segmentstat._recid).all():

                if get_month(segmentstat.datum) == mm:
                    stat_list.mtd_budget =  to_decimal(stat_list.mtd_budget) + to_decimal(mon_budget[get_day(segmentstat.datum) - 1]) + to_decimal(segmentstat.budzimmeranz)
                stat_list.ytd_budget =  to_decimal(stat_list.ytd_budget) + to_decimal(segmentstat.budzimmeranz)


    def create_fbcover():

        nonlocal rev_seg_list_list, rev_list_list, payable_list_list, stat_list_list, payment_list_list, gl_list_list, fb_sales_food_list, fb_sales_beverage_list, fb_sales_other_list, fb_sales_tot_list, rev_seg_list1_list, fb_sales_material_list, gsheet_link, ytd_flag, str1, str2, str3, st1, st2, st3, st4, st5, st6, st7, st8, st9, st10, st11, st12, st13, st14, st15, st16, st17, st18, st19, st20, st21, st22, st23, st24, st25, st26, st27, st28, st29, st30, st31, st32, st33, st34, st35, st36, st37, n, n1, n2, n3, n4, n5, n6, n7, n8, n9, n10, n11, n12, n13, n14, n15, n16, n17, n18, n19, n20, n21, n22, n23, n24, n25, n26, n27, n28, n29, n30, start_date, serv, vat, vat2, fact, n_betrag, n_serv, n_tax, ly_betrag, d_flag, dbudget_flag, dlmtd_flag, yes_serv, yes_vat, yes_vat2, yes_fact, yes_betrag, date1, date2, temp_date2, temp_curr_date, l_today, st_date, foreign_nr, foreign_flag, tot_betrag, price_decimal, no_decimal, dept, dept1, zwkum, dper, mtd_per, ytd_per, tot_today, tot_today_per, tot_mtd, tot_mtd_per, tot_mtd_budget, tot_variance, tot_ytd, tot_ytd_budget, tot_ytd_per, tot_today1, tot_today_per1, tot_mtd1, tot_mtd_per1, tot_mtd_budget1, tot_variance1, tot_ytd1, tot_ytd_budget1, tot_ytd_per1, tot_today2, tot_today_per2, tot_mtd2, tot_mtd_per2, tot_mtd_budget2, tot_variance2, tot_ytd2, tot_ytd_budget2, tot_ytd_per2, tot_today3, tot_mtd3, tot_mtd_budget3, tot_variance3, tot_ytd3, tot_ytd_budget3, tot_today4, tot_mtd4, tot_mtd_budget4, tot_variance4, tot_ytd4, tot_ytd_budget4, tot_today5, tot_mtd5, tot_mtd_budget5, tot_variance5, tot_ytd5, tot_ytd_budget5, tot_today6, tot_mtd6, tot_mtd_budget6, tot_variance6, tot_ytd6, tot_ytd_budget6, tot_today7, tot_mtd7, tot_mtd_budget7, tot_variance7, tot_ytd7, tot_ytd_budget7, tot_tday_cov, tot_tday_avg, tot_tday_rev, tot_mtd_cov, tot_mtd_avg, tot_mtd_rev, tot_ytd_cov, tot_ytd_avg, tot_ytd_rev, t_today, t_today_per, t_mtd, t_mtd_per, t_mtd_budget, t_variance, t_ytd, t_ytd_budget, t_ytd_per, t_today1, t_today_per1, t_mtd1, t_mtd_per1, t_mtd_budget1, t_variance1, t_ytd1, t_ytd_budget1, t_ytd_per1, t_today11, t_today_per11, t_mtd11, t_mtd_per11, t_mtd_budget11, t_variance11, t_ytd11, t_ytd_budget11, t_ytd_per11, t_today2, t_today_per2, t_mtd2, t_mtd_per2, t_mtd_budget2, t_variance2, t_ytd2, t_ytd_budget2, t_ytd_per2, t_today3, t_today_per3, t_mtd3, t_mtd_per3, t_mtd_budget3, t_variance3, t_ytd3, t_ytd_budget3, t_ytd_per3, tdy_gl1, ytd_gl, curr_flag, curr_dept, ct, ct3, ct4, t_day_serv, mtd_serv, mtd_budget_serv, ytd_serv, ytd_budget_serv, variance_serv, t_day_tax, mtd_tax, mtd_budget_tax, ytd_tax, ytd_budget_tax, variance_tax, ct1, curr_flag1, ct2, banq_dept, frate, jan1, budget_flag, mon_saldo, mon_budget, foreign_curr, umsatz, waehrung, htparam, queasy, segment, artikel, hoteldpt, uebertrag, exrate, genstat, segmentstat, budget, zinrstat, zkstat
        nonlocal from_date, to_date
        nonlocal buff_umsatz, b_rev_list, b_rev_seg_list, b_rev_seg_list1, b_stat_list, brev_list, b_payment_list, bpayment_list, bpayable_list


        nonlocal rev_seg_list, rev_seg_list1, rev_list, rev_list_tax, rev_list_serv, payable_list, tot_list, stat_list, payment_list, segment_list, gl_list, fb_sales_food, fb_sales_beverage, fb_sales_other, fb_sales_tot, fb_sales_material, setup_revenue, setup_segment, setup_payment, setup_stat, setup_fbcover, buff_umsatz, b_rev_list, b_rev_seg_list, b_rev_seg_list1, b_stat_list, brev_list, b_payment_list, bpayment_list, bpayable_list
        nonlocal rev_seg_list_list, rev_seg_list1_list, rev_list_list, rev_list_tax_list, rev_list_serv_list, payable_list_list, tot_list_list, stat_list_list, payment_list_list, segment_list_list, gl_list_list, fb_sales_food_list, fb_sales_beverage_list, fb_sales_other_list, fb_sales_tot_list, fb_sales_material_list, setup_revenue_list, setup_segment_list, setup_payment_list, setup_stat_list, setup_fbcover_list

        datum1:date = None
        datum2:date = None
        curr_date:date = None
        t_day:decimal = to_decimal("0.0")
        mtd:decimal = to_decimal("0.0")
        ytd:decimal = to_decimal("0.0")
        t_day_rev:decimal = to_decimal("0.0")
        mtd_rev:decimal = to_decimal("0.0")
        ytd_rev:decimal = to_decimal("0.0")
        t_day_avg:decimal = to_decimal("0.0")
        mtd_avg:decimal = to_decimal("0.0")
        ytd_avg:decimal = to_decimal("0.0")

        if ytd_flag:
            datum1 = jan1
        else:
            datum1 = from_date
        for curr_date in date_range(datum1,to_date) :
            serv =  to_decimal("0")
            vat =  to_decimal("0")

            umsatz = db_session.query(Umsatz).filter(
                     (Umsatz.datum == curr_date) & (Umsatz.artnr == artikel.artnr) & (Umsatz.departement == setup_fbcover.departement)).first()

            if umsatz:
                serv, vat, vat2, fact = get_output(calc_servtaxesbl(1, umsatz.artnr, umsatz.departement, umsatz.datum))
            fact =  to_decimal(1.00) + to_decimal(serv) + to_decimal(vat) + to_decimal(vat2)
            n_betrag =  to_decimal("0")

            if umsatz:

                if foreign_flag:
                    find_exrate(curr_date)

                    if exrate:
                        frate =  to_decimal(exrate.betrag)
                n_betrag =  to_decimal(umsatz.betrag) / to_decimal((fact) * to_decimal(frate) )
                n_serv =  to_decimal(n_betrag) * to_decimal(serv)
                n_tax =  to_decimal(n_betrag) * to_decimal(vat)


                t_day =  to_decimal(t_day) + to_decimal(umsatz.anzahl)
                t_day_rev =  to_decimal(t_day_rev) + to_decimal(n_betrag)

                if price_decimal == 0:
                    n_betrag = to_decimal(round(n_betrag , 0))
                    n_serv = to_decimal(round(n_serv , 0))
                    n_tax = to_decimal(round(n_tax , 0))

            if curr_date < from_date:

                if umsatz:
                    ytd_rev =  to_decimal(ytd_rev) + to_decimal(n_betrag)
                    ytd =  to_decimal(ytd) + to_decimal(umsatz.anzahl)


            else:

                if umsatz:

                    if ytd_flag:
                        ytd_rev =  to_decimal(ytd_rev) + to_decimal(n_betrag)
                        ytd =  to_decimal(ytd) + to_decimal(umsatz.anzahl)

                    if get_month(curr_date) == get_month(to_date):
                        mtd_rev =  to_decimal(mtd_rev) + to_decimal(mon_saldo[get_day(umsatz.datum) - 1]) + to_decimal(n_betrag)
                        mtd =  to_decimal(mtd) + to_decimal(mon_saldo[get_day(umsatz.datum) - 1]) + to_decimal(umsatz.anzahl)

            if t_day != 0:
                t_day_avg =  to_decimal(t_day_rev) / to_decimal(t_day)
                mtd_avg =  to_decimal(mtd_rev) / to_decimal(mtd)
                ytd_avg =  to_decimal(ytd_rev) / to_decimal(ytd)

        if setup_fbcover.flag.lower()  == ("1Food").lower() :

            fb_sales_food = query(fb_sales_food_list, filters=(lambda fb_sales_food: fb_sales_food.departement == setup_fbcover.departement and fb_sales_food.flag.lower()  == ("1Food").lower()), first=True)

            if not fb_sales_food:

                hoteldpt = db_session.query(Hoteldpt).filter(
                         (Hoteldpt.num == setup_fbcover.departement)).first()

                if hoteldpt:
                    ct = ct + 1
                    fb_sales_food = Fb_sales_food()
                    fb_sales_food_list.append(fb_sales_food)

                    fb_sales_food.ct = ct
                    fb_sales_food.departement = setup_fbcover.departement
                    fb_sales_food.descr = hoteldpt.depart
                    fb_sales_food.flag = "1Food"

        elif setup_fbcover.flag.lower()  == ("2Beverage").lower() :

            fb_sales_beverage = query(fb_sales_beverage_list, filters=(lambda fb_sales_beverage: fb_sales_beverage.departement == setup_fbcover.departement and fb_sales_beverage.flag.lower()  == ("2Beverage").lower()), first=True)

            if not fb_sales_beverage:

                hoteldpt = db_session.query(Hoteldpt).filter(
                         (Hoteldpt.num == setup_fbcover.departement)).first()

                if hoteldpt:
                    ct = ct + 1
                    fb_sales_beverage = Fb_sales_beverage()
                    fb_sales_beverage_list.append(fb_sales_beverage)

                    fb_sales_beverage.ct = ct
                    fb_sales_beverage.departement = setup_fbcover.departement
                    fb_sales_beverage.descr = hoteldpt.depart
                    fb_sales_beverage.flag = "2Beverage"

        elif setup_fbcover.flag.lower()  == ("3Banquet").lower() :

            fb_sales_other = query(fb_sales_other_list, filters=(lambda fb_sales_other: fb_sales_other.departement == setup_fbcover.departement and fb_sales_other.flag.lower()  == ("3Banquet").lower()), first=True)

            if not fb_sales_other:

                hoteldpt = db_session.query(Hoteldpt).filter(
                         (Hoteldpt.num == setup_fbcover.departement)).first()

                if hoteldpt:
                    ct = ct + 1
                    fb_sales_other = Fb_sales_other()
                    fb_sales_other_list.append(fb_sales_other)

                    fb_sales_other.ct = ct
                    fb_sales_other.departement = setup_fbcover.departement
                    fb_sales_other.descr = hoteldpt.depart
                    fb_sales_other.flag = "3Banquet"

        elif setup_fbcover.flag.lower()  == ("4Material").lower() :

            fb_sales_material = query(fb_sales_material_list, filters=(lambda fb_sales_material: fb_sales_material.departement == setup_fbcover.departement and fb_sales_material.flag.lower()  == ("4Material").lower()), first=True)

            if not fb_sales_material:

                hoteldpt = db_session.query(Hoteldpt).filter(
                         (Hoteldpt.num == setup_fbcover.departement)).first()

                if hoteldpt:
                    ct = ct + 1
                    fb_sales_material = Fb_sales_material()
                    fb_sales_material_list.append(fb_sales_material)

                    fb_sales_material.ct = ct
                    fb_sales_material.departement = setup_fbcover.departement
                    fb_sales_material.descr = hoteldpt.depart
                    fb_sales_material.flag = "4Material"


        ct = ct + 1

        if setup_fbcover.flag.lower()  == ("1Food").lower() :
            fb_sales_food = Fb_sales_food()
            fb_sales_food_list.append(fb_sales_food)


            if mtd_avg == None:
                mtd_avg =  to_decimal("0")
            fb_sales_food.ct = ct
            fb_sales_food.departement = setup_fbcover.departement
            fb_sales_food.artnr = setup_fbcover.artnr
            fb_sales_food.descr = artikel.bezeich
            fb_sales_food.tday_cov =  to_decimal(t_day)
            fb_sales_food.tday_avg =  to_decimal(t_day_avg)
            fb_sales_food.tday_rev =  to_decimal(t_day_rev)
            fb_sales_food.mtd_cov =  to_decimal(mtd)
            fb_sales_food.mtd_avg =  to_decimal(mtd_avg)
            fb_sales_food.mtd_rev =  to_decimal(mtd_rev)
            fb_sales_food.ytd_cov =  to_decimal(ytd)
            fb_sales_food.ytd_avg =  to_decimal(ytd_avg)
            fb_sales_food.ytd_rev =  to_decimal(ytd_rev)
            fb_sales_food.flag = "1Food"
            t_day =  to_decimal("0")
            mtd =  to_decimal("0")
            ytd =  to_decimal("0")
            t_day_rev =  to_decimal("0")
            mtd_rev =  to_decimal("0")
            ytd_rev =  to_decimal("0")
            t_day_avg =  to_decimal("0")
            mtd_avg =  to_decimal("0")
            ytd_avg =  to_decimal("0")

        elif setup_fbcover.flag.lower()  == ("2Beverage").lower() :
            fb_sales_beverage = Fb_sales_beverage()
            fb_sales_beverage_list.append(fb_sales_beverage)


            if mtd_avg == None:
                mtd_avg =  to_decimal("0")
            fb_sales_beverage.ct = ct
            fb_sales_beverage.departement = setup_fbcover.departement
            fb_sales_beverage.artnr = setup_fbcover.artnr
            fb_sales_beverage.descr = artikel.bezeich
            fb_sales_beverage.tday_cov =  to_decimal(t_day)
            fb_sales_beverage.tday_avg =  to_decimal(t_day_avg)
            fb_sales_beverage.tday_rev =  to_decimal(t_day_rev)
            fb_sales_beverage.mtd_cov =  to_decimal(mtd)
            fb_sales_beverage.mtd_avg =  to_decimal(mtd_avg)
            fb_sales_beverage.mtd_rev =  to_decimal(mtd_rev)
            fb_sales_beverage.ytd_cov =  to_decimal(ytd)
            fb_sales_beverage.ytd_avg =  to_decimal(ytd_avg)
            fb_sales_beverage.ytd_rev =  to_decimal(ytd_rev)
            fb_sales_beverage.flag = "2Beverage"
            t_day =  to_decimal("0")
            mtd =  to_decimal("0")
            ytd =  to_decimal("0")
            t_day_rev =  to_decimal("0")
            mtd_rev =  to_decimal("0")
            ytd_rev =  to_decimal("0")
            t_day_avg =  to_decimal("0")
            mtd_avg =  to_decimal("0")
            ytd_avg =  to_decimal("0")

        elif setup_fbcover.flag.lower()  == ("3Banquet").lower() :
            fb_sales_other = Fb_sales_other()
            fb_sales_other_list.append(fb_sales_other)


            if mtd_avg == None:
                mtd_avg =  to_decimal("0")
            fb_sales_other.ct = ct
            fb_sales_other.departement = setup_fbcover.departement
            fb_sales_other.artnr = setup_fbcover.artnr
            fb_sales_other.descr = artikel.bezeich
            fb_sales_other.tday_cov =  to_decimal(t_day)
            fb_sales_other.tday_avg =  to_decimal(t_day_avg)
            fb_sales_other.tday_rev =  to_decimal(t_day_rev)
            fb_sales_other.mtd_cov =  to_decimal(mtd)
            fb_sales_other.mtd_avg =  to_decimal(mtd_avg)
            fb_sales_other.mtd_rev =  to_decimal(mtd_rev)
            fb_sales_other.ytd_cov =  to_decimal(ytd)
            fb_sales_other.ytd_avg =  to_decimal(ytd_avg)
            fb_sales_other.ytd_rev =  to_decimal(ytd_rev)
            fb_sales_other.flag = "3Banquet"
            t_day =  to_decimal("0")
            mtd =  to_decimal("0")
            ytd =  to_decimal("0")
            t_day_rev =  to_decimal("0")
            mtd_rev =  to_decimal("0")
            ytd_rev =  to_decimal("0")
            t_day_avg =  to_decimal("0")
            mtd_avg =  to_decimal("0")
            ytd_avg =  to_decimal("0")

        elif setup_fbcover.flag.lower()  == ("4Material").lower() :
            fb_sales_material = Fb_sales_material()
            fb_sales_material_list.append(fb_sales_material)


            if mtd_avg == None:
                mtd_avg =  to_decimal("0")
            fb_sales_material.ct = ct
            fb_sales_material.departement = setup_fbcover.departement
            fb_sales_material.artnr = setup_fbcover.artnr
            fb_sales_material.descr = artikel.bezeich
            fb_sales_material.tday_cov =  to_decimal(t_day)
            fb_sales_material.tday_avg =  to_decimal(t_day_avg)
            fb_sales_material.tday_rev =  to_decimal(t_day_rev)
            fb_sales_material.mtd_cov =  to_decimal(mtd)
            fb_sales_material.mtd_avg =  to_decimal(mtd_avg)
            fb_sales_material.mtd_rev =  to_decimal(mtd_rev)
            fb_sales_material.ytd_cov =  to_decimal(ytd)
            fb_sales_material.ytd_avg =  to_decimal(ytd_avg)
            fb_sales_material.ytd_rev =  to_decimal(ytd_rev)
            fb_sales_material.flag = "4Material"
            t_day =  to_decimal("0")
            mtd =  to_decimal("0")
            ytd =  to_decimal("0")
            t_day_rev =  to_decimal("0")
            mtd_rev =  to_decimal("0")
            ytd_rev =  to_decimal("0")
            t_day_avg =  to_decimal("0")
            mtd_avg =  to_decimal("0")
            ytd_avg =  to_decimal("0")


    def fill_comproomnew():

        nonlocal rev_seg_list_list, rev_list_list, payable_list_list, stat_list_list, payment_list_list, gl_list_list, fb_sales_food_list, fb_sales_beverage_list, fb_sales_other_list, fb_sales_tot_list, rev_seg_list1_list, fb_sales_material_list, gsheet_link, ytd_flag, str1, str2, str3, st1, st2, st3, st4, st5, st6, st7, st8, st9, st10, st11, st12, st13, st14, st15, st16, st17, st18, st19, st20, st21, st22, st23, st24, st25, st26, st27, st28, st29, st30, st31, st32, st33, st34, st35, st36, st37, n, n1, n2, n3, n4, n5, n6, n7, n8, n9, n10, n11, n12, n13, n14, n15, n16, n17, n18, n19, n20, n21, n22, n23, n24, n25, n26, n27, n28, n29, n30, curr_date, start_date, datum1, serv, vat, vat2, fact, n_betrag, n_serv, n_tax, ly_betrag, dbudget_flag, dlmtd_flag, yes_serv, yes_vat, yes_vat2, yes_fact, yes_betrag, date1, date2, temp_date2, temp_curr_date, l_today, st_date, foreign_nr, foreign_flag, tot_betrag, price_decimal, no_decimal, dept, dept1, zwkum, dper, mtd_per, ytd_per, tot_today, tot_today_per, tot_mtd, tot_mtd_per, tot_mtd_budget, tot_variance, tot_ytd, tot_ytd_budget, tot_ytd_per, tot_today1, tot_today_per1, tot_mtd1, tot_mtd_per1, tot_mtd_budget1, tot_variance1, tot_ytd1, tot_ytd_budget1, tot_ytd_per1, tot_today2, tot_today_per2, tot_mtd2, tot_mtd_per2, tot_mtd_budget2, tot_variance2, tot_ytd2, tot_ytd_budget2, tot_ytd_per2, tot_today3, tot_mtd3, tot_mtd_budget3, tot_variance3, tot_ytd3, tot_ytd_budget3, tot_today4, tot_mtd4, tot_mtd_budget4, tot_variance4, tot_ytd4, tot_ytd_budget4, tot_today5, tot_mtd5, tot_mtd_budget5, tot_variance5, tot_ytd5, tot_ytd_budget5, tot_today6, tot_mtd6, tot_mtd_budget6, tot_variance6, tot_ytd6, tot_ytd_budget6, tot_today7, tot_mtd7, tot_mtd_budget7, tot_variance7, tot_ytd7, tot_ytd_budget7, tot_tday_cov, tot_tday_avg, tot_tday_rev, tot_mtd_cov, tot_mtd_avg, tot_mtd_rev, tot_ytd_cov, tot_ytd_avg, tot_ytd_rev, t_today, t_today_per, t_mtd, t_mtd_per, t_mtd_budget, t_variance, t_ytd, t_ytd_budget, t_ytd_per, t_today1, t_today_per1, t_mtd1, t_mtd_per1, t_mtd_budget1, t_variance1, t_ytd1, t_ytd_budget1, t_ytd_per1, t_today11, t_today_per11, t_mtd11, t_mtd_per11, t_mtd_budget11, t_variance11, t_ytd11, t_ytd_budget11, t_ytd_per11, t_today2, t_today_per2, t_mtd2, t_mtd_per2, t_mtd_budget2, t_variance2, t_ytd2, t_ytd_budget2, t_ytd_per2, t_today3, t_today_per3, t_mtd3, t_mtd_per3, t_mtd_budget3, t_variance3, t_ytd3, t_ytd_budget3, t_ytd_per3, tdy_gl1, ytd_gl, curr_flag, curr_dept, ct, ct3, ct4, t_day_serv, mtd_serv, mtd_budget_serv, ytd_serv, ytd_budget_serv, variance_serv, t_day_tax, mtd_tax, mtd_budget_tax, ytd_tax, ytd_budget_tax, variance_tax, ct1, curr_flag1, ct2, banq_dept, frate, jan1, budget_flag, mon_saldo, mon_budget, foreign_curr, umsatz, waehrung, htparam, queasy, segment, artikel, hoteldpt, uebertrag, exrate, genstat, segmentstat, budget, zinrstat, zkstat
        nonlocal from_date, to_date
        nonlocal buff_umsatz, b_rev_list, b_rev_seg_list, b_rev_seg_list1, b_stat_list, brev_list, b_payment_list, bpayment_list, bpayable_list


        nonlocal rev_seg_list, rev_seg_list1, rev_list, rev_list_tax, rev_list_serv, payable_list, tot_list, stat_list, payment_list, segment_list, gl_list, fb_sales_food, fb_sales_beverage, fb_sales_other, fb_sales_tot, fb_sales_material, setup_revenue, setup_segment, setup_payment, setup_stat, setup_fbcover, buff_umsatz, b_rev_list, b_rev_seg_list, b_rev_seg_list1, b_stat_list, brev_list, b_payment_list, bpayment_list, bpayable_list
        nonlocal rev_seg_list_list, rev_seg_list1_list, rev_list_list, rev_list_tax_list, rev_list_serv_list, payable_list_list, tot_list_list, stat_list_list, payment_list_list, segment_list_list, gl_list_list, fb_sales_food_list, fb_sales_beverage_list, fb_sales_other_list, fb_sales_tot_list, fb_sales_material_list, setup_revenue_list, setup_segment_list, setup_payment_list, setup_stat_list, setup_fbcover_list

        d_flag:bool = False
        mm:int = 0
        frate1:decimal = to_decimal("0.0")
        mm = get_month(to_date)
        ct1 = ct1 + 1
        stat_list = Stat_list()
        stat_list_list.append(stat_list)

        stat_list.ct = ct1
        stat_list.flag = "Compl"
        stat_list.descr = "Complimentary Paying Guest"

        genstat_obj_list = []
        for genstat, segment in db_session.query(Genstat, Segment).join(Segment,(Segment.segmentcode == Genstat.segmentcode)).filter(
                 (Genstat.datum >= datum1) & (Genstat.datum <= to_date) & (Genstat.zipreis == 0) & (Genstat.gratis == 0) & (Genstat.resstatus == 6) & (Genstat.res_logic[inc_value(2))]).order_by(Genstat._recid).all():
            if genstat._recid in genstat_obj_list:
                continue
            else:
                genstat_obj_list.append(genstat._recid)

            if segment.betriebsnr == 0:

                if foreign_flag:
                    find_exrate(genstat.datum)

                    if exrate:
                        frate =  to_decimal(exrate.betrag)
                d_flag = (get_month(genstat.datum) == get_month(to_date)) and (get_year(genstat.datum) == get_year(to_date))

                if genstat.datum == to_date:
                    stat_list.t_day =  to_decimal(stat_list.t_day) + to_decimal("1")

                if get_month(genstat.datum) == mm:
                    stat_list.mtd =  to_decimal(stat_list.mtd) + to_decimal(mon_saldo[get_day(genstat.datum) - 1]) + to_decimal("1")
                stat_list.ytd =  to_decimal(stat_list.ytd) + to_decimal("1")


    def fill_roomsold():

        nonlocal rev_seg_list_list, rev_list_list, payable_list_list, stat_list_list, payment_list_list, gl_list_list, fb_sales_food_list, fb_sales_beverage_list, fb_sales_other_list, fb_sales_tot_list, rev_seg_list1_list, fb_sales_material_list, gsheet_link, ytd_flag, str1, str2, str3, st1, st2, st3, st4, st5, st6, st7, st8, st9, st10, st11, st12, st13, st14, st15, st16, st17, st18, st19, st20, st21, st22, st23, st24, st25, st26, st27, st28, st29, st30, st31, st32, st33, st34, st35, st36, st37, n, n1, n2, n3, n4, n5, n6, n7, n8, n9, n10, n11, n12, n13, n14, n15, n16, n17, n18, n19, n20, n21, n22, n23, n24, n25, n26, n27, n28, n29, n30, curr_date, start_date, datum1, serv, vat, vat2, fact, n_betrag, n_serv, n_tax, ly_betrag, d_flag, dbudget_flag, dlmtd_flag, yes_serv, yes_vat, yes_vat2, yes_fact, yes_betrag, date1, date2, temp_date2, temp_curr_date, l_today, st_date, foreign_nr, foreign_flag, tot_betrag, price_decimal, no_decimal, dept, dept1, zwkum, dper, mtd_per, ytd_per, tot_today, tot_today_per, tot_mtd, tot_mtd_per, tot_mtd_budget, tot_variance, tot_ytd, tot_ytd_budget, tot_ytd_per, tot_today1, tot_today_per1, tot_mtd1, tot_mtd_per1, tot_mtd_budget1, tot_variance1, tot_ytd1, tot_ytd_budget1, tot_ytd_per1, tot_today2, tot_today_per2, tot_mtd2, tot_mtd_per2, tot_mtd_budget2, tot_variance2, tot_ytd2, tot_ytd_budget2, tot_ytd_per2, tot_today3, tot_mtd3, tot_mtd_budget3, tot_variance3, tot_ytd3, tot_ytd_budget3, tot_today4, tot_mtd4, tot_mtd_budget4, tot_variance4, tot_ytd4, tot_ytd_budget4, tot_today5, tot_mtd5, tot_mtd_budget5, tot_variance5, tot_ytd5, tot_ytd_budget5, tot_today6, tot_mtd6, tot_mtd_budget6, tot_variance6, tot_ytd6, tot_ytd_budget6, tot_today7, tot_mtd7, tot_mtd_budget7, tot_variance7, tot_ytd7, tot_ytd_budget7, tot_tday_cov, tot_tday_avg, tot_tday_rev, tot_mtd_cov, tot_mtd_avg, tot_mtd_rev, tot_ytd_cov, tot_ytd_avg, tot_ytd_rev, t_today, t_today_per, t_mtd, t_mtd_per, t_mtd_budget, t_variance, t_ytd, t_ytd_budget, t_ytd_per, t_today1, t_today_per1, t_mtd1, t_mtd_per1, t_mtd_budget1, t_variance1, t_ytd1, t_ytd_budget1, t_ytd_per1, t_today11, t_today_per11, t_mtd11, t_mtd_per11, t_mtd_budget11, t_variance11, t_ytd11, t_ytd_budget11, t_ytd_per11, t_today2, t_today_per2, t_mtd2, t_mtd_per2, t_mtd_budget2, t_variance2, t_ytd2, t_ytd_budget2, t_ytd_per2, t_today3, t_today_per3, t_mtd3, t_mtd_per3, t_mtd_budget3, t_variance3, t_ytd3, t_ytd_budget3, t_ytd_per3, tdy_gl1, ytd_gl, curr_flag, curr_dept, ct, ct3, ct4, t_day_serv, mtd_serv, mtd_budget_serv, ytd_serv, ytd_budget_serv, variance_serv, t_day_tax, mtd_tax, mtd_budget_tax, ytd_tax, ytd_budget_tax, variance_tax, ct1, curr_flag1, ct2, banq_dept, frate, jan1, budget_flag, mon_saldo, mon_budget, foreign_curr, umsatz, waehrung, htparam, queasy, segment, artikel, hoteldpt, uebertrag, exrate, genstat, segmentstat, budget, zinrstat, zkstat
        nonlocal from_date, to_date
        nonlocal buff_umsatz, b_rev_list, b_rev_seg_list, b_rev_seg_list1, b_stat_list, brev_list, b_payment_list, bpayment_list, bpayable_list


        nonlocal rev_seg_list, rev_seg_list1, rev_list, rev_list_tax, rev_list_serv, payable_list, tot_list, stat_list, payment_list, segment_list, gl_list, fb_sales_food, fb_sales_beverage, fb_sales_other, fb_sales_tot, fb_sales_material, setup_revenue, setup_segment, setup_payment, setup_stat, setup_fbcover, buff_umsatz, b_rev_list, b_rev_seg_list, b_rev_seg_list1, b_stat_list, brev_list, b_payment_list, bpayment_list, bpayable_list
        nonlocal rev_seg_list_list, rev_seg_list1_list, rev_list_list, rev_list_tax_list, rev_list_serv_list, payable_list_list, tot_list_list, stat_list_list, payment_list_list, segment_list_list, gl_list_list, fb_sales_food_list, fb_sales_beverage_list, fb_sales_other_list, fb_sales_tot_list, fb_sales_material_list, setup_revenue_list, setup_segment_list, setup_payment_list, setup_stat_list, setup_fbcover_list

        tday1:int = 0
        tday2:int = 0
        tday3:int = 0
        mtd1:int = 0
        mtd2:int = 0
        mtd3:int = 0
        ytd1:int = 0
        ytd2:int = 0
        ytd3:int = 0
        ct1 = ct1 + 1

        stat_list = query(stat_list_list, filters=(lambda stat_list: stat_list.flag.lower()  == ("rmsold").lower()), first=True)

        if not stat_list:
            stat_list = Stat_list()
            stat_list_list.append(stat_list)

            stat_list.ct = ct1
            stat_list.flag = "rmsold"
            stat_list.descr = "Rooms Sold"

            for b_stat_list in query(b_stat_list_list):

                if b_stat_list.flag.lower()  == ("houseuse").lower() :
                    tday1 = b_stat_list.t_day
                    mtd1 = b_stat_list.mtd
                    ytd1 = b_stat_list.ytd

                if b_stat_list.flag.lower()  == ("comp").lower() :
                    tday2 = b_stat_list.t_day
                    mtd2 = b_stat_list.mtd
                    ytd2 = b_stat_list.ytd

                if b_stat_list.flag.lower()  == ("occ").lower() :
                    tday3 = b_stat_list.t_day
                    mtd3 = b_stat_list.mtd
                    ytd3 = b_stat_list.ytd


            stat_list.t_day =  to_decimal(tday1) + to_decimal(tday2) + to_decimal(tday3)
            stat_list.mtd =  to_decimal(mtd1) + to_decimal(mtd2) + to_decimal(mtd3)
            stat_list.ytd =  to_decimal(ytd1) + to_decimal(ytd2) + to_decimal(ytd3)

            setup_stat = query(setup_stat_list, filters=(lambda setup_stat: setup_stat.descr.lower()  == ("Room Sold").lower()), first=True)

            if setup_stat:

                budget = db_session.query(Budget).filter(
                         (Budget.artnr == setup_stat.artnr) & (Budget.departement == 0) & (Budget.datum == curr_date)).first()

                if curr_date < from_date:
                    pass
                else:

                    if budget:
                        stat_list.mtd_budget =  to_decimal(stat_list.mtd_budget) + to_decimal(budget.betrag)


    def fill_occ_pay():

        nonlocal rev_seg_list_list, rev_list_list, payable_list_list, stat_list_list, payment_list_list, gl_list_list, fb_sales_food_list, fb_sales_beverage_list, fb_sales_other_list, fb_sales_tot_list, rev_seg_list1_list, fb_sales_material_list, gsheet_link, ytd_flag, str1, str2, str3, st1, st2, st3, st4, st5, st6, st7, st8, st9, st10, st11, st12, st13, st14, st15, st16, st17, st18, st19, st20, st21, st22, st23, st24, st25, st26, st27, st28, st29, st30, st31, st32, st33, st34, st35, st36, st37, n, n1, n2, n3, n4, n5, n6, n7, n8, n9, n10, n11, n12, n13, n14, n15, n16, n17, n18, n19, n20, n21, n22, n23, n24, n25, n26, n27, n28, n29, n30, curr_date, start_date, datum1, serv, vat, vat2, fact, n_betrag, n_serv, n_tax, ly_betrag, d_flag, dbudget_flag, dlmtd_flag, yes_serv, yes_vat, yes_vat2, yes_fact, yes_betrag, date1, date2, temp_date2, temp_curr_date, l_today, st_date, foreign_nr, foreign_flag, tot_betrag, price_decimal, no_decimal, dept, dept1, zwkum, dper, mtd_per, ytd_per, tot_today, tot_today_per, tot_mtd, tot_mtd_per, tot_mtd_budget, tot_variance, tot_ytd, tot_ytd_budget, tot_ytd_per, tot_today1, tot_today_per1, tot_mtd1, tot_mtd_per1, tot_mtd_budget1, tot_variance1, tot_ytd1, tot_ytd_budget1, tot_ytd_per1, tot_today2, tot_today_per2, tot_mtd2, tot_mtd_per2, tot_mtd_budget2, tot_variance2, tot_ytd2, tot_ytd_budget2, tot_ytd_per2, tot_today3, tot_mtd3, tot_mtd_budget3, tot_variance3, tot_ytd3, tot_ytd_budget3, tot_today4, tot_mtd4, tot_mtd_budget4, tot_variance4, tot_ytd4, tot_ytd_budget4, tot_today5, tot_mtd5, tot_mtd_budget5, tot_variance5, tot_ytd5, tot_ytd_budget5, tot_today6, tot_mtd6, tot_mtd_budget6, tot_variance6, tot_ytd6, tot_ytd_budget6, tot_today7, tot_mtd7, tot_mtd_budget7, tot_variance7, tot_ytd7, tot_ytd_budget7, tot_tday_cov, tot_tday_avg, tot_tday_rev, tot_mtd_cov, tot_mtd_avg, tot_mtd_rev, tot_ytd_cov, tot_ytd_avg, tot_ytd_rev, t_today, t_today_per, t_mtd, t_mtd_per, t_mtd_budget, t_variance, t_ytd, t_ytd_budget, t_ytd_per, t_today1, t_today_per1, t_mtd1, t_mtd_per1, t_mtd_budget1, t_variance1, t_ytd1, t_ytd_budget1, t_ytd_per1, t_today11, t_today_per11, t_mtd11, t_mtd_per11, t_mtd_budget11, t_variance11, t_ytd11, t_ytd_budget11, t_ytd_per11, t_today2, t_today_per2, t_mtd2, t_mtd_per2, t_mtd_budget2, t_variance2, t_ytd2, t_ytd_budget2, t_ytd_per2, t_today3, t_today_per3, t_mtd3, t_mtd_per3, t_mtd_budget3, t_variance3, t_ytd3, t_ytd_budget3, t_ytd_per3, tdy_gl1, ytd_gl, curr_flag, curr_dept, ct, ct3, ct4, t_day_serv, mtd_serv, mtd_budget_serv, ytd_serv, ytd_budget_serv, variance_serv, t_day_tax, mtd_tax, mtd_budget_tax, ytd_tax, ytd_budget_tax, variance_tax, ct1, curr_flag1, ct2, banq_dept, frate, jan1, budget_flag, mon_saldo, mon_budget, foreign_curr, umsatz, waehrung, htparam, queasy, segment, artikel, hoteldpt, uebertrag, exrate, genstat, segmentstat, budget, zinrstat, zkstat
        nonlocal from_date, to_date
        nonlocal buff_umsatz, b_rev_list, b_rev_seg_list, b_rev_seg_list1, b_stat_list, brev_list, b_payment_list, bpayment_list, bpayable_list


        nonlocal rev_seg_list, rev_seg_list1, rev_list, rev_list_tax, rev_list_serv, payable_list, tot_list, stat_list, payment_list, segment_list, gl_list, fb_sales_food, fb_sales_beverage, fb_sales_other, fb_sales_tot, fb_sales_material, setup_revenue, setup_segment, setup_payment, setup_stat, setup_fbcover, buff_umsatz, b_rev_list, b_rev_seg_list, b_rev_seg_list1, b_stat_list, brev_list, b_payment_list, bpayment_list, bpayable_list
        nonlocal rev_seg_list_list, rev_seg_list1_list, rev_list_list, rev_list_tax_list, rev_list_serv_list, payable_list_list, tot_list_list, stat_list_list, payment_list_list, segment_list_list, gl_list_list, fb_sales_food_list, fb_sales_beverage_list, fb_sales_other_list, fb_sales_tot_list, fb_sales_material_list, setup_revenue_list, setup_segment_list, setup_payment_list, setup_stat_list, setup_fbcover_list

        tday1:int = 0
        tday2:int = 0
        tday3:int = 0
        mtd1:int = 0
        mtd2:int = 0
        mtd3:int = 0
        ytd1:int = 0
        ytd2:int = 0
        ytd3:int = 0
        ct1 = ct1 + 1

        stat_list = query(stat_list_list, filters=(lambda stat_list: stat_list.flag.lower()  == ("occpay").lower()), first=True)

        if not stat_list:
            stat_list = Stat_list()
            stat_list_list.append(stat_list)

            stat_list.ct = ct1
            stat_list.flag = "occ-pay"
            stat_list.descr = "% Occupancy (Paying)"

            for b_stat_list in query(b_stat_list_list):

                if b_stat_list.flag.lower()  == ("tot-rm").lower() :
                    tday1 = b_stat_list.t_day
                    mtd1 = b_stat_list.mtd
                    ytd1 = b_stat_list.ytd

                if b_stat_list.flag.lower()  == ("rmsold").lower() :
                    tday2 = b_stat_list.t_day
                    mtd2 = b_stat_list.mtd
                    ytd2 = b_stat_list.ytd

            if tday2 != 0 or mtd2 != 0 or ytd2 != 0:
                stat_list.t_day = ( to_decimal(tday2) / to_decimal(tday1)) * to_decimal("100")
                stat_list.mtd = ( to_decimal(mtd2) / to_decimal(mtd1)) * to_decimal("100")
                stat_list.ytd = ( to_decimal(ytd2) / to_decimal(ytd1)) * to_decimal("100")

            setup_stat = query(setup_stat_list, filters=(lambda setup_stat: setup_stat.descr.lower()  == ("% Occupancy").lower()), first=True)

            if setup_stat:

                budget = db_session.query(Budget).filter(
                         (Budget.artnr == setup_stat.artnr) & (Budget.departement == 0) & (Budget.datum == curr_date)).first()

                if curr_date < from_date:
                    pass
                else:

                    if budget:
                        stat_list.mtd_budget =  to_decimal(stat_list.mtd_budget) + to_decimal(budget.betrag)


    def fill_occ_comp_hu():

        nonlocal rev_seg_list_list, rev_list_list, payable_list_list, stat_list_list, payment_list_list, gl_list_list, fb_sales_food_list, fb_sales_beverage_list, fb_sales_other_list, fb_sales_tot_list, rev_seg_list1_list, fb_sales_material_list, gsheet_link, ytd_flag, str1, str2, str3, st1, st2, st3, st4, st5, st6, st7, st8, st9, st10, st11, st12, st13, st14, st15, st16, st17, st18, st19, st20, st21, st22, st23, st24, st25, st26, st27, st28, st29, st30, st31, st32, st33, st34, st35, st36, st37, n, n1, n2, n3, n4, n5, n6, n7, n8, n9, n10, n11, n12, n13, n14, n15, n16, n17, n18, n19, n20, n21, n22, n23, n24, n25, n26, n27, n28, n29, n30, curr_date, start_date, datum1, serv, vat, vat2, fact, n_betrag, n_serv, n_tax, ly_betrag, d_flag, dbudget_flag, dlmtd_flag, yes_serv, yes_vat, yes_vat2, yes_fact, yes_betrag, date1, date2, temp_date2, temp_curr_date, l_today, st_date, foreign_nr, foreign_flag, tot_betrag, price_decimal, no_decimal, dept, dept1, zwkum, dper, mtd_per, ytd_per, tot_today, tot_today_per, tot_mtd, tot_mtd_per, tot_mtd_budget, tot_variance, tot_ytd, tot_ytd_budget, tot_ytd_per, tot_today1, tot_today_per1, tot_mtd1, tot_mtd_per1, tot_mtd_budget1, tot_variance1, tot_ytd1, tot_ytd_budget1, tot_ytd_per1, tot_today2, tot_today_per2, tot_mtd2, tot_mtd_per2, tot_mtd_budget2, tot_variance2, tot_ytd2, tot_ytd_budget2, tot_ytd_per2, tot_today3, tot_mtd3, tot_mtd_budget3, tot_variance3, tot_ytd3, tot_ytd_budget3, tot_today4, tot_mtd4, tot_mtd_budget4, tot_variance4, tot_ytd4, tot_ytd_budget4, tot_today5, tot_mtd5, tot_mtd_budget5, tot_variance5, tot_ytd5, tot_ytd_budget5, tot_today6, tot_mtd6, tot_mtd_budget6, tot_variance6, tot_ytd6, tot_ytd_budget6, tot_today7, tot_mtd7, tot_mtd_budget7, tot_variance7, tot_ytd7, tot_ytd_budget7, tot_tday_cov, tot_tday_avg, tot_tday_rev, tot_mtd_cov, tot_mtd_avg, tot_mtd_rev, tot_ytd_cov, tot_ytd_avg, tot_ytd_rev, t_today, t_today_per, t_mtd, t_mtd_per, t_mtd_budget, t_variance, t_ytd, t_ytd_budget, t_ytd_per, t_today1, t_today_per1, t_mtd1, t_mtd_per1, t_mtd_budget1, t_variance1, t_ytd1, t_ytd_budget1, t_ytd_per1, t_today11, t_today_per11, t_mtd11, t_mtd_per11, t_mtd_budget11, t_variance11, t_ytd11, t_ytd_budget11, t_ytd_per11, t_today2, t_today_per2, t_mtd2, t_mtd_per2, t_mtd_budget2, t_variance2, t_ytd2, t_ytd_budget2, t_ytd_per2, t_today3, t_today_per3, t_mtd3, t_mtd_per3, t_mtd_budget3, t_variance3, t_ytd3, t_ytd_budget3, t_ytd_per3, tdy_gl1, ytd_gl, curr_flag, curr_dept, ct, ct3, ct4, t_day_serv, mtd_serv, mtd_budget_serv, ytd_serv, ytd_budget_serv, variance_serv, t_day_tax, mtd_tax, mtd_budget_tax, ytd_tax, ytd_budget_tax, variance_tax, ct1, curr_flag1, ct2, banq_dept, frate, jan1, budget_flag, mon_saldo, mon_budget, foreign_curr, umsatz, waehrung, htparam, queasy, segment, artikel, hoteldpt, uebertrag, exrate, genstat, segmentstat, budget, zinrstat, zkstat
        nonlocal from_date, to_date
        nonlocal buff_umsatz, b_rev_list, b_rev_seg_list, b_rev_seg_list1, b_stat_list, brev_list, b_payment_list, bpayment_list, bpayable_list


        nonlocal rev_seg_list, rev_seg_list1, rev_list, rev_list_tax, rev_list_serv, payable_list, tot_list, stat_list, payment_list, segment_list, gl_list, fb_sales_food, fb_sales_beverage, fb_sales_other, fb_sales_tot, fb_sales_material, setup_revenue, setup_segment, setup_payment, setup_stat, setup_fbcover, buff_umsatz, b_rev_list, b_rev_seg_list, b_rev_seg_list1, b_stat_list, brev_list, b_payment_list, bpayment_list, bpayable_list
        nonlocal rev_seg_list_list, rev_seg_list1_list, rev_list_list, rev_list_tax_list, rev_list_serv_list, payable_list_list, tot_list_list, stat_list_list, payment_list_list, segment_list_list, gl_list_list, fb_sales_food_list, fb_sales_beverage_list, fb_sales_other_list, fb_sales_tot_list, fb_sales_material_list, setup_revenue_list, setup_segment_list, setup_payment_list, setup_stat_list, setup_fbcover_list

        tday1:int = 0
        tday2:int = 0
        tday3:int = 0
        mtd1:int = 0
        mtd2:int = 0
        mtd3:int = 0
        ytd1:int = 0
        ytd2:int = 0
        ytd3:int = 0
        ct1 = ct1 + 1

        stat_list = query(stat_list_list, filters=(lambda stat_list: stat_list.flag.lower()  == ("occ-comp-hu").lower()), first=True)

        if not stat_list:
            stat_list = Stat_list()
            stat_list_list.append(stat_list)

            stat_list.ct = ct1
            stat_list.flag = "occ-comp-hu"
            stat_list.descr = "% Occupancy (Comp + HU)"

            for b_stat_list in query(b_stat_list_list):

                if b_stat_list.flag.lower()  == ("occ").lower() :
                    tday1 = b_stat_list.t_day
                    mtd1 = b_stat_list.mtd
                    ytd1 = b_stat_list.ytd

                if b_stat_list.flag.lower()  == ("tot-rm").lower() :
                    tday2 = b_stat_list.t_day
                    mtd2 = b_stat_list.mtd
                    ytd2 = b_stat_list.ytd

            if tday2 != 0 or mtd2 != 0 or ytd2 != 0:
                stat_list.t_day = ( to_decimal(tday1) / to_decimal(tday2)) * to_decimal("100")
                stat_list.mtd = ( to_decimal(mtd1) / to_decimal(mtd2)) * to_decimal("100")
                stat_list.ytd = ( to_decimal(ytd1) / to_decimal(ytd2)) * to_decimal("100")

            setup_stat = query(setup_stat_list, filters=(lambda setup_stat: setup_stat.descr.lower()  == ("% Occupancy with Comp and HU").lower()), first=True)

            if setup_stat:

                budget = db_session.query(Budget).filter(
                         (Budget.artnr == setup_stat.artnr) & (Budget.departement == 0) & (Budget.datum == curr_date)).first()

                if curr_date < from_date:
                    pass
                else:

                    if budget:
                        stat_list.mtd_budget =  to_decimal(stat_list.mtd_budget) + to_decimal(budget.betrag)


    def fill_tot_rev():

        nonlocal rev_seg_list_list, rev_list_list, payable_list_list, stat_list_list, payment_list_list, gl_list_list, fb_sales_food_list, fb_sales_beverage_list, fb_sales_other_list, fb_sales_tot_list, rev_seg_list1_list, fb_sales_material_list, gsheet_link, ytd_flag, str1, str2, str3, st1, st2, st3, st4, st5, st6, st7, st8, st9, st10, st11, st12, st13, st14, st15, st16, st17, st18, st19, st20, st21, st22, st23, st24, st25, st26, st27, st28, st29, st30, st31, st32, st33, st34, st35, st36, st37, n, n1, n2, n3, n4, n5, n6, n7, n8, n9, n10, n11, n12, n13, n14, n15, n16, n17, n18, n19, n20, n21, n22, n23, n24, n25, n26, n27, n28, n29, n30, curr_date, start_date, datum1, serv, vat, vat2, fact, n_betrag, n_serv, n_tax, ly_betrag, d_flag, dbudget_flag, dlmtd_flag, yes_serv, yes_vat, yes_vat2, yes_fact, yes_betrag, date1, date2, temp_date2, temp_curr_date, l_today, st_date, foreign_nr, foreign_flag, tot_betrag, price_decimal, no_decimal, dept, dept1, zwkum, dper, mtd_per, ytd_per, tot_today, tot_today_per, tot_mtd, tot_mtd_per, tot_mtd_budget, tot_variance, tot_ytd, tot_ytd_budget, tot_ytd_per, tot_today1, tot_today_per1, tot_mtd1, tot_mtd_per1, tot_mtd_budget1, tot_variance1, tot_ytd1, tot_ytd_budget1, tot_ytd_per1, tot_today2, tot_today_per2, tot_mtd2, tot_mtd_per2, tot_mtd_budget2, tot_variance2, tot_ytd2, tot_ytd_budget2, tot_ytd_per2, tot_today3, tot_mtd3, tot_mtd_budget3, tot_variance3, tot_ytd3, tot_ytd_budget3, tot_today4, tot_mtd4, tot_mtd_budget4, tot_variance4, tot_ytd4, tot_ytd_budget4, tot_today5, tot_mtd5, tot_mtd_budget5, tot_variance5, tot_ytd5, tot_ytd_budget5, tot_today6, tot_mtd6, tot_mtd_budget6, tot_variance6, tot_ytd6, tot_ytd_budget6, tot_today7, tot_mtd7, tot_mtd_budget7, tot_variance7, tot_ytd7, tot_ytd_budget7, tot_tday_cov, tot_tday_avg, tot_tday_rev, tot_mtd_cov, tot_mtd_avg, tot_mtd_rev, tot_ytd_cov, tot_ytd_avg, tot_ytd_rev, t_today, t_today_per, t_mtd, t_mtd_per, t_mtd_budget, t_variance, t_ytd, t_ytd_budget, t_ytd_per, t_today1, t_today_per1, t_mtd1, t_mtd_per1, t_mtd_budget1, t_variance1, t_ytd1, t_ytd_budget1, t_ytd_per1, t_today11, t_today_per11, t_mtd11, t_mtd_per11, t_mtd_budget11, t_variance11, t_ytd11, t_ytd_budget11, t_ytd_per11, t_today2, t_today_per2, t_mtd2, t_mtd_per2, t_mtd_budget2, t_variance2, t_ytd2, t_ytd_budget2, t_ytd_per2, t_today3, t_today_per3, t_mtd3, t_mtd_per3, t_mtd_budget3, t_variance3, t_ytd3, t_ytd_budget3, t_ytd_per3, tdy_gl1, ytd_gl, curr_flag, curr_dept, ct, ct3, ct4, t_day_serv, mtd_serv, mtd_budget_serv, ytd_serv, ytd_budget_serv, variance_serv, t_day_tax, mtd_tax, mtd_budget_tax, ytd_tax, ytd_budget_tax, variance_tax, ct1, curr_flag1, ct2, banq_dept, frate, jan1, budget_flag, mon_saldo, mon_budget, foreign_curr, umsatz, waehrung, htparam, queasy, segment, artikel, hoteldpt, uebertrag, exrate, genstat, segmentstat, budget, zinrstat, zkstat
        nonlocal from_date, to_date
        nonlocal buff_umsatz, b_rev_list, b_rev_seg_list, b_rev_seg_list1, b_stat_list, brev_list, b_payment_list, bpayment_list, bpayable_list


        nonlocal rev_seg_list, rev_seg_list1, rev_list, rev_list_tax, rev_list_serv, payable_list, tot_list, stat_list, payment_list, segment_list, gl_list, fb_sales_food, fb_sales_beverage, fb_sales_other, fb_sales_tot, fb_sales_material, setup_revenue, setup_segment, setup_payment, setup_stat, setup_fbcover, buff_umsatz, b_rev_list, b_rev_seg_list, b_rev_seg_list1, b_stat_list, brev_list, b_payment_list, bpayment_list, bpayable_list
        nonlocal rev_seg_list_list, rev_seg_list1_list, rev_list_list, rev_list_tax_list, rev_list_serv_list, payable_list_list, tot_list_list, stat_list_list, payment_list_list, segment_list_list, gl_list_list, fb_sales_food_list, fb_sales_beverage_list, fb_sales_other_list, fb_sales_tot_list, fb_sales_material_list, setup_revenue_list, setup_segment_list, setup_payment_list, setup_stat_list, setup_fbcover_list

        tday1:decimal = to_decimal("0.0")
        tday2:decimal = to_decimal("0.0")
        tday3:decimal = to_decimal("0.0")
        mtd1:decimal = to_decimal("0.0")
        mtd2:decimal = to_decimal("0.0")
        mtd3:decimal = to_decimal("0.0")
        ytd1:decimal = to_decimal("0.0")
        ytd2:decimal = to_decimal("0.0")
        ytd3:decimal = to_decimal("0.0")
        ct1 = ct1 + 1

        stat_list = query(stat_list_list, filters=(lambda stat_list: stat_list.flag.lower()  == ("tot-rev").lower()), first=True)

        if not stat_list:
            stat_list = Stat_list()
            stat_list_list.append(stat_list)

            stat_list.ct = ct1
            stat_list.flag = "tot-rev"
            stat_list.descr = "Total Room Revenue"

            rev_list = query(rev_list_list, filters=(lambda rev_list: rev_list.flag.lower()  == ("Room").lower()  and re.match(r".*Total Room Revenue.*",rev_list.descr, re.IGNORECASE)), first=True)

            if rev_list:
                stat_list.t_day =  to_decimal(rev_list.t_day)
                stat_list.mtd =  to_decimal(rev_list.mtd)
                stat_list.ytd =  to_decimal(rev_list.ytd)
                stat_list.mtd_budget =  to_decimal(rev_list.mtd_budget)


    def fill_avg_rmrate_rp():

        nonlocal rev_seg_list_list, rev_list_list, payable_list_list, stat_list_list, payment_list_list, gl_list_list, fb_sales_food_list, fb_sales_beverage_list, fb_sales_other_list, fb_sales_tot_list, rev_seg_list1_list, fb_sales_material_list, gsheet_link, ytd_flag, str1, str2, str3, st1, st2, st3, st4, st5, st6, st7, st8, st9, st10, st11, st12, st13, st14, st15, st16, st17, st18, st19, st20, st21, st22, st23, st24, st25, st26, st27, st28, st29, st30, st31, st32, st33, st34, st35, st36, st37, n, n1, n2, n3, n4, n5, n6, n7, n8, n9, n10, n11, n12, n13, n14, n15, n16, n17, n18, n19, n20, n21, n22, n23, n24, n25, n26, n27, n28, n29, n30, curr_date, start_date, datum1, serv, vat, vat2, fact, n_betrag, n_serv, n_tax, ly_betrag, d_flag, dbudget_flag, dlmtd_flag, yes_serv, yes_vat, yes_vat2, yes_fact, yes_betrag, date1, date2, temp_date2, temp_curr_date, l_today, st_date, foreign_nr, foreign_flag, tot_betrag, price_decimal, no_decimal, dept, dept1, zwkum, dper, mtd_per, ytd_per, tot_today, tot_today_per, tot_mtd, tot_mtd_per, tot_mtd_budget, tot_variance, tot_ytd, tot_ytd_budget, tot_ytd_per, tot_today1, tot_today_per1, tot_mtd1, tot_mtd_per1, tot_mtd_budget1, tot_variance1, tot_ytd1, tot_ytd_budget1, tot_ytd_per1, tot_today2, tot_today_per2, tot_mtd2, tot_mtd_per2, tot_mtd_budget2, tot_variance2, tot_ytd2, tot_ytd_budget2, tot_ytd_per2, tot_today3, tot_mtd3, tot_mtd_budget3, tot_variance3, tot_ytd3, tot_ytd_budget3, tot_today4, tot_mtd4, tot_mtd_budget4, tot_variance4, tot_ytd4, tot_ytd_budget4, tot_today5, tot_mtd5, tot_mtd_budget5, tot_variance5, tot_ytd5, tot_ytd_budget5, tot_today6, tot_mtd6, tot_mtd_budget6, tot_variance6, tot_ytd6, tot_ytd_budget6, tot_today7, tot_mtd7, tot_mtd_budget7, tot_variance7, tot_ytd7, tot_ytd_budget7, tot_tday_cov, tot_tday_avg, tot_tday_rev, tot_mtd_cov, tot_mtd_avg, tot_mtd_rev, tot_ytd_cov, tot_ytd_avg, tot_ytd_rev, t_today, t_today_per, t_mtd, t_mtd_per, t_mtd_budget, t_variance, t_ytd, t_ytd_budget, t_ytd_per, t_today1, t_today_per1, t_mtd1, t_mtd_per1, t_mtd_budget1, t_variance1, t_ytd1, t_ytd_budget1, t_ytd_per1, t_today11, t_today_per11, t_mtd11, t_mtd_per11, t_mtd_budget11, t_variance11, t_ytd11, t_ytd_budget11, t_ytd_per11, t_today2, t_today_per2, t_mtd2, t_mtd_per2, t_mtd_budget2, t_variance2, t_ytd2, t_ytd_budget2, t_ytd_per2, t_today3, t_today_per3, t_mtd3, t_mtd_per3, t_mtd_budget3, t_variance3, t_ytd3, t_ytd_budget3, t_ytd_per3, tdy_gl1, ytd_gl, curr_flag, curr_dept, ct, ct3, ct4, t_day_serv, mtd_serv, mtd_budget_serv, ytd_serv, ytd_budget_serv, variance_serv, t_day_tax, mtd_tax, mtd_budget_tax, ytd_tax, ytd_budget_tax, variance_tax, ct1, curr_flag1, ct2, banq_dept, frate, jan1, budget_flag, mon_saldo, mon_budget, foreign_curr, umsatz, waehrung, htparam, queasy, segment, artikel, hoteldpt, uebertrag, exrate, genstat, segmentstat, budget, zinrstat, zkstat
        nonlocal from_date, to_date
        nonlocal buff_umsatz, b_rev_list, b_rev_seg_list, b_rev_seg_list1, b_stat_list, brev_list, b_payment_list, bpayment_list, bpayable_list


        nonlocal rev_seg_list, rev_seg_list1, rev_list, rev_list_tax, rev_list_serv, payable_list, tot_list, stat_list, payment_list, segment_list, gl_list, fb_sales_food, fb_sales_beverage, fb_sales_other, fb_sales_tot, fb_sales_material, setup_revenue, setup_segment, setup_payment, setup_stat, setup_fbcover, buff_umsatz, b_rev_list, b_rev_seg_list, b_rev_seg_list1, b_stat_list, brev_list, b_payment_list, bpayment_list, bpayable_list
        nonlocal rev_seg_list_list, rev_seg_list1_list, rev_list_list, rev_list_tax_list, rev_list_serv_list, payable_list_list, tot_list_list, stat_list_list, payment_list_list, segment_list_list, gl_list_list, fb_sales_food_list, fb_sales_beverage_list, fb_sales_other_list, fb_sales_tot_list, fb_sales_material_list, setup_revenue_list, setup_segment_list, setup_payment_list, setup_stat_list, setup_fbcover_list

        tday1:decimal = to_decimal("0.0")
        tday2:decimal = to_decimal("0.0")
        tday3:decimal = to_decimal("0.0")
        mtd1:decimal = to_decimal("0.0")
        mtd2:decimal = to_decimal("0.0")
        mtd3:decimal = to_decimal("0.0")
        ytd1:decimal = to_decimal("0.0")
        ytd2:decimal = to_decimal("0.0")
        ytd3:decimal = to_decimal("0.0")
        ct1 = ct1 + 1

        stat_list = query(stat_list_list, filters=(lambda stat_list: stat_list.flag.lower()  == ("avg-rmrate-rp").lower()), first=True)

        if not stat_list:
            stat_list = Stat_list()
            stat_list_list.append(stat_list)

            stat_list.ct = ct1
            stat_list.flag = "avg-rmrate-rp"
            stat_list.descr = "Average Room Rate Rp."

            for b_stat_list in query(b_stat_list_list):

                if b_stat_list.flag.lower()  == ("rmsold").lower() :
                    tday2 =  to_decimal(b_stat_list.t_day)
                    mtd2 =  to_decimal(b_stat_list.mtd)
                    ytd2 =  to_decimal(b_stat_list.ytd)

            rev_list = query(rev_list_list, filters=(lambda rev_list: rev_list.descr.lower()  == ("TOTAL ROOM REVENUE").lower()), first=True)

            if rev_list:
                tday1 =  to_decimal(rev_list.t_day)
                mtd1 =  to_decimal(rev_list.mtd)
                ytd1 =  to_decimal(rev_list.ytd)

            if tday2 != 0 or mtd2 != 0 or ytd2 != 0:
                stat_list.t_day = ( to_decimal(tday1) / to_decimal(tday2) )
                stat_list.mtd = ( to_decimal(mtd1) / to_decimal(mtd2) )
                stat_list.ytd = ( to_decimal(ytd1) / to_decimal(ytd2) )

            setup_stat = query(setup_stat_list, filters=(lambda setup_stat: setup_stat.descr.lower()  == ("Average Room Rate Rp").lower()), first=True)

            if setup_stat:

                budget = db_session.query(Budget).filter(
                         (Budget.artnr == setup_stat.artnr) & (Budget.departement == 0) & (Budget.datum == curr_date)).first()

                if curr_date < from_date:
                    pass
                else:

                    if budget:
                        stat_list.mtd_budget =  to_decimal(stat_list.mtd_budget) + to_decimal(budget.betrag)


    def fill_avg_rmrate_frg():

        nonlocal rev_seg_list_list, rev_list_list, payable_list_list, stat_list_list, payment_list_list, gl_list_list, fb_sales_food_list, fb_sales_beverage_list, fb_sales_other_list, fb_sales_tot_list, rev_seg_list1_list, fb_sales_material_list, gsheet_link, ytd_flag, str1, str2, str3, st1, st2, st3, st4, st5, st6, st7, st8, st9, st10, st11, st12, st13, st14, st15, st16, st17, st18, st19, st20, st21, st22, st23, st24, st25, st26, st27, st28, st29, st30, st31, st32, st33, st34, st35, st36, st37, n, n1, n2, n3, n4, n5, n6, n7, n8, n9, n10, n11, n12, n13, n14, n15, n16, n17, n18, n19, n20, n21, n22, n23, n24, n25, n26, n27, n28, n29, n30, curr_date, start_date, datum1, serv, vat, vat2, fact, n_betrag, n_serv, n_tax, ly_betrag, d_flag, dbudget_flag, dlmtd_flag, yes_serv, yes_vat, yes_vat2, yes_fact, yes_betrag, date1, date2, temp_date2, temp_curr_date, l_today, st_date, foreign_nr, foreign_flag, tot_betrag, price_decimal, no_decimal, dept, dept1, zwkum, dper, mtd_per, ytd_per, tot_today, tot_today_per, tot_mtd, tot_mtd_per, tot_mtd_budget, tot_variance, tot_ytd, tot_ytd_budget, tot_ytd_per, tot_today1, tot_today_per1, tot_mtd1, tot_mtd_per1, tot_mtd_budget1, tot_variance1, tot_ytd1, tot_ytd_budget1, tot_ytd_per1, tot_today2, tot_today_per2, tot_mtd2, tot_mtd_per2, tot_mtd_budget2, tot_variance2, tot_ytd2, tot_ytd_budget2, tot_ytd_per2, tot_today3, tot_mtd3, tot_mtd_budget3, tot_variance3, tot_ytd3, tot_ytd_budget3, tot_today4, tot_mtd4, tot_mtd_budget4, tot_variance4, tot_ytd4, tot_ytd_budget4, tot_today5, tot_mtd5, tot_mtd_budget5, tot_variance5, tot_ytd5, tot_ytd_budget5, tot_today6, tot_mtd6, tot_mtd_budget6, tot_variance6, tot_ytd6, tot_ytd_budget6, tot_today7, tot_mtd7, tot_mtd_budget7, tot_variance7, tot_ytd7, tot_ytd_budget7, tot_tday_cov, tot_tday_avg, tot_tday_rev, tot_mtd_cov, tot_mtd_avg, tot_mtd_rev, tot_ytd_cov, tot_ytd_avg, tot_ytd_rev, t_today, t_today_per, t_mtd, t_mtd_per, t_mtd_budget, t_variance, t_ytd, t_ytd_budget, t_ytd_per, t_today1, t_today_per1, t_mtd1, t_mtd_per1, t_mtd_budget1, t_variance1, t_ytd1, t_ytd_budget1, t_ytd_per1, t_today11, t_today_per11, t_mtd11, t_mtd_per11, t_mtd_budget11, t_variance11, t_ytd11, t_ytd_budget11, t_ytd_per11, t_today2, t_today_per2, t_mtd2, t_mtd_per2, t_mtd_budget2, t_variance2, t_ytd2, t_ytd_budget2, t_ytd_per2, t_today3, t_today_per3, t_mtd3, t_mtd_per3, t_mtd_budget3, t_variance3, t_ytd3, t_ytd_budget3, t_ytd_per3, tdy_gl1, ytd_gl, curr_flag, curr_dept, ct, ct3, ct4, t_day_serv, mtd_serv, mtd_budget_serv, ytd_serv, ytd_budget_serv, variance_serv, t_day_tax, mtd_tax, mtd_budget_tax, ytd_tax, ytd_budget_tax, variance_tax, ct1, curr_flag1, ct2, banq_dept, frate, jan1, budget_flag, mon_saldo, mon_budget, foreign_curr, umsatz, waehrung, htparam, queasy, segment, artikel, hoteldpt, uebertrag, exrate, genstat, segmentstat, budget, zinrstat, zkstat
        nonlocal from_date, to_date
        nonlocal buff_umsatz, b_rev_list, b_rev_seg_list, b_rev_seg_list1, b_stat_list, brev_list, b_payment_list, bpayment_list, bpayable_list


        nonlocal rev_seg_list, rev_seg_list1, rev_list, rev_list_tax, rev_list_serv, payable_list, tot_list, stat_list, payment_list, segment_list, gl_list, fb_sales_food, fb_sales_beverage, fb_sales_other, fb_sales_tot, fb_sales_material, setup_revenue, setup_segment, setup_payment, setup_stat, setup_fbcover, buff_umsatz, b_rev_list, b_rev_seg_list, b_rev_seg_list1, b_stat_list, brev_list, b_payment_list, bpayment_list, bpayable_list
        nonlocal rev_seg_list_list, rev_seg_list1_list, rev_list_list, rev_list_tax_list, rev_list_serv_list, payable_list_list, tot_list_list, stat_list_list, payment_list_list, segment_list_list, gl_list_list, fb_sales_food_list, fb_sales_beverage_list, fb_sales_other_list, fb_sales_tot_list, fb_sales_material_list, setup_revenue_list, setup_segment_list, setup_payment_list, setup_stat_list, setup_fbcover_list

        tday1:decimal = to_decimal("0.0")
        tday2:decimal = to_decimal("0.0")
        tday3:decimal = to_decimal("0.0")
        mtd1:decimal = to_decimal("0.0")
        mtd2:decimal = to_decimal("0.0")
        mtd3:decimal = to_decimal("0.0")
        ytd1:decimal = to_decimal("0.0")
        ytd2:decimal = to_decimal("0.0")
        ytd3:decimal = to_decimal("0.0")
        ct1 = ct1 + 1

        stat_list = query(stat_list_list, filters=(lambda stat_list: stat_list.flag.lower()  == ("avg-rmrate-frg").lower()), first=True)

        if not stat_list:
            stat_list = Stat_list()
            stat_list_list.append(stat_list)

            stat_list.ct = ct1
            stat_list.flag = "avg-rmrate-frg"
            stat_list.descr = "Average Room Rate US$"

            for b_stat_list in query(b_stat_list_list):

                if b_stat_list.flag.lower()  == ("rmsold").lower() :
                    tday2 =  to_decimal(b_stat_list.t_day)
                    mtd2 =  to_decimal(b_stat_list.mtd)
                    ytd2 =  to_decimal(b_stat_list.ytd)

            rev_list = query(rev_list_list, first=True)

            if rev_list:
                find_exrate(to_date)

                if exrate:
                    frate =  to_decimal(exrate.betrag)
                tday1 =  to_decimal(rev_list.t_day) / to_decimal((fact) * to_decimal(frate) )
                mtd1 =  to_decimal(rev_list.mtd) / to_decimal((fact) * to_decimal(frate) )
                ytd1 =  to_decimal(rev_list.ytd) / to_decimal((fact) * to_decimal(frate) )

            if tday2 != 0 or mtd2 != 0 or ytd2 != 0:
                stat_list.t_day = ( to_decimal(tday1) / to_decimal(tday2)) / to_decimal(foreign_curr)
                stat_list.mtd = ( to_decimal(mtd1) / to_decimal(mtd2)) / to_decimal(foreign_curr)
                stat_list.ytd = ( to_decimal(ytd1) / to_decimal(ytd2)) / to_decimal(foreign_curr)

            setup_stat = query(setup_stat_list, filters=(lambda setup_stat: setup_stat.descr.lower()  == ("Average Room Rate Rp").lower()), first=True)

            if setup_stat:

                budget = db_session.query(Budget).filter(
                         (Budget.artnr == setup_stat.artnr) & (Budget.departement == 0) & (Budget.datum == curr_date)).first()

                if curr_date < from_date:
                    pass
                else:

                    if budget:
                        stat_list.mtd_budget =  to_decimal(stat_list.mtd_budget) + to_decimal(budget.betrag)


    def fill_revpar():

        nonlocal rev_seg_list_list, rev_list_list, payable_list_list, stat_list_list, payment_list_list, gl_list_list, fb_sales_food_list, fb_sales_beverage_list, fb_sales_other_list, fb_sales_tot_list, rev_seg_list1_list, fb_sales_material_list, gsheet_link, ytd_flag, str1, str2, str3, st1, st2, st3, st4, st5, st6, st7, st8, st9, st10, st11, st12, st13, st14, st15, st16, st17, st18, st19, st20, st21, st22, st23, st24, st25, st26, st27, st28, st29, st30, st31, st32, st33, st34, st35, st36, st37, n, n1, n2, n3, n4, n5, n6, n7, n8, n9, n10, n11, n12, n13, n14, n15, n16, n17, n18, n19, n20, n21, n22, n23, n24, n25, n26, n27, n28, n29, n30, curr_date, start_date, datum1, serv, vat, vat2, fact, n_betrag, n_serv, n_tax, ly_betrag, d_flag, dbudget_flag, dlmtd_flag, yes_serv, yes_vat, yes_vat2, yes_fact, yes_betrag, date1, date2, temp_date2, temp_curr_date, l_today, st_date, foreign_nr, foreign_flag, tot_betrag, price_decimal, no_decimal, dept, dept1, zwkum, dper, mtd_per, ytd_per, tot_today, tot_today_per, tot_mtd, tot_mtd_per, tot_mtd_budget, tot_variance, tot_ytd, tot_ytd_budget, tot_ytd_per, tot_today1, tot_today_per1, tot_mtd1, tot_mtd_per1, tot_mtd_budget1, tot_variance1, tot_ytd1, tot_ytd_budget1, tot_ytd_per1, tot_today2, tot_today_per2, tot_mtd2, tot_mtd_per2, tot_mtd_budget2, tot_variance2, tot_ytd2, tot_ytd_budget2, tot_ytd_per2, tot_today3, tot_mtd3, tot_mtd_budget3, tot_variance3, tot_ytd3, tot_ytd_budget3, tot_today4, tot_mtd4, tot_mtd_budget4, tot_variance4, tot_ytd4, tot_ytd_budget4, tot_today5, tot_mtd5, tot_mtd_budget5, tot_variance5, tot_ytd5, tot_ytd_budget5, tot_today6, tot_mtd6, tot_mtd_budget6, tot_variance6, tot_ytd6, tot_ytd_budget6, tot_today7, tot_mtd7, tot_mtd_budget7, tot_variance7, tot_ytd7, tot_ytd_budget7, tot_tday_cov, tot_tday_avg, tot_tday_rev, tot_mtd_cov, tot_mtd_avg, tot_mtd_rev, tot_ytd_cov, tot_ytd_avg, tot_ytd_rev, t_today, t_today_per, t_mtd, t_mtd_per, t_mtd_budget, t_variance, t_ytd, t_ytd_budget, t_ytd_per, t_today1, t_today_per1, t_mtd1, t_mtd_per1, t_mtd_budget1, t_variance1, t_ytd1, t_ytd_budget1, t_ytd_per1, t_today11, t_today_per11, t_mtd11, t_mtd_per11, t_mtd_budget11, t_variance11, t_ytd11, t_ytd_budget11, t_ytd_per11, t_today2, t_today_per2, t_mtd2, t_mtd_per2, t_mtd_budget2, t_variance2, t_ytd2, t_ytd_budget2, t_ytd_per2, t_today3, t_today_per3, t_mtd3, t_mtd_per3, t_mtd_budget3, t_variance3, t_ytd3, t_ytd_budget3, t_ytd_per3, tdy_gl1, ytd_gl, curr_flag, curr_dept, ct, ct3, ct4, t_day_serv, mtd_serv, mtd_budget_serv, ytd_serv, ytd_budget_serv, variance_serv, t_day_tax, mtd_tax, mtd_budget_tax, ytd_tax, ytd_budget_tax, variance_tax, ct1, curr_flag1, ct2, banq_dept, frate, jan1, budget_flag, mon_saldo, mon_budget, foreign_curr, umsatz, waehrung, htparam, queasy, segment, artikel, hoteldpt, uebertrag, exrate, genstat, segmentstat, budget, zinrstat, zkstat
        nonlocal from_date, to_date
        nonlocal buff_umsatz, b_rev_list, b_rev_seg_list, b_rev_seg_list1, b_stat_list, brev_list, b_payment_list, bpayment_list, bpayable_list


        nonlocal rev_seg_list, rev_seg_list1, rev_list, rev_list_tax, rev_list_serv, payable_list, tot_list, stat_list, payment_list, segment_list, gl_list, fb_sales_food, fb_sales_beverage, fb_sales_other, fb_sales_tot, fb_sales_material, setup_revenue, setup_segment, setup_payment, setup_stat, setup_fbcover, buff_umsatz, b_rev_list, b_rev_seg_list, b_rev_seg_list1, b_stat_list, brev_list, b_payment_list, bpayment_list, bpayable_list
        nonlocal rev_seg_list_list, rev_seg_list1_list, rev_list_list, rev_list_tax_list, rev_list_serv_list, payable_list_list, tot_list_list, stat_list_list, payment_list_list, segment_list_list, gl_list_list, fb_sales_food_list, fb_sales_beverage_list, fb_sales_other_list, fb_sales_tot_list, fb_sales_material_list, setup_revenue_list, setup_segment_list, setup_payment_list, setup_stat_list, setup_fbcover_list

        tday1:decimal = to_decimal("0.0")
        tday2:decimal = to_decimal("0.0")
        mtd1:decimal = to_decimal("0.0")
        mtd2:decimal = to_decimal("0.0")
        mtd_budget1:decimal = to_decimal("0.0")
        mtd_budget2:decimal = to_decimal("0.0")
        ytd1:decimal = to_decimal("0.0")
        ytd2:decimal = to_decimal("0.0")
        ct1 = ct1 + 1

        stat_list = query(stat_list_list, filters=(lambda stat_list: stat_list.flag.lower()  == ("revpar").lower()), first=True)

        if not stat_list:
            stat_list = Stat_list()
            stat_list_list.append(stat_list)

            stat_list.ct = ct1
            stat_list.flag = "revpar"
            stat_list.descr = "Revenue Per Available Room / Revpar"

            for b_stat_list in query(b_stat_list_list):

                if b_stat_list.flag.lower()  == ("tot-rmav").lower() :
                    tday2 =  to_decimal(b_stat_list.t_day)
                    mtd2 =  to_decimal(b_stat_list.mtd)
                    mtd_budget2 =  to_decimal(b_stat_list.mtd_budget)
                    ytd2 =  to_decimal(b_stat_list.ytd)

            rev_list = query(rev_list_list, filters=(lambda rev_list: rev_list.descr.lower()  == ("TOTAL ROOM REVENUE").lower()), first=True)

            if rev_list:
                tday1 =  to_decimal(rev_list.t_day)
                mtd1 =  to_decimal(rev_list.mtd)
                mtd_budget1 =  to_decimal(rev_list.mtd_budget)
                ytd1 =  to_decimal(rev_list.ytd)

            if mtd_budget1 != 0 and mtd_budget2 != 0:
                stat_list.mtd_budget = ( to_decimal(mtd_budget1) / to_decimal(mtd_budget2))

            if tday2 != 0 or mtd2 != 0 or ytd2 != 0:
                stat_list.t_day = ( to_decimal(tday1) / to_decimal(tday2) )
                stat_list.mtd = ( to_decimal(mtd1) / to_decimal(mtd2) )
                stat_list.ytd = ( to_decimal(ytd1) / to_decimal(ytd2) )

    jan1 = date_mdy(1, 1, get_year(to_date))

    waehrung = db_session.query(Waehrung).filter(
             (Waehrung.waehrungsnr == 2)).first()

    if waehrung:
        foreign_curr =  to_decimal(waehrung.ankauf)

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 184)).first()
    foreign_nr = htparam.fint

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 186)).first()

    if htparam.feldtyp == 3 and htparam.fdate != None:
        start_date = htparam.fdate

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 900)).first()
    banq_dept = htparam.fint

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 491)).first()
    price_decimal = htparam.finteger
    no_decimal = (price_decimal == 0)

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 801)).first()

    if ytd_flag:
        datum1 = jan1
    else:
        datum1 = from_date

    if price_decimal == 0:
        price_decimal = 2
    no_decimal = (price_decimal == 0)

    queasy = db_session.query(Queasy).filter(
             (Queasy.key == 265)).first()

    if queasy:
        str1 = queasy.char1
        str2 = queasy.char2
        str3 = queasy.char3

    for segment in db_session.query(Segment).order_by(Segment._recid).all():

        segment_list = query(segment_list_list, filters=(lambda segment_list: segment_list.segmentcode == segment.segmentcode), first=True)

        if not segment_list:
            segment_list = Segment_list()
            segment_list_list.append(segment_list)

            segment_list.segmentcode = segment.segmentcode
            segment_list.bezeich = segment.bezeich


    for n1 in range(1,num_entries(str2, ";")  + 1) :
        st2 = entry(n1 - 1, str2, ";")

        if substring(st2, 0, 11) == ("$FOrevenue$").lower()  and substring(st2, 11, 3) == ("YES").lower() :
            st3 = substring(st2, 11, 3)
            st4 = substring(st2, 15)


            for n2 in range(1,num_entries(st4, ",")  + 1) :
                st5 = entry(n2 - 1, st4, ",")
                setup_revenue = Setup_revenue()
                setup_revenue_list.append(setup_revenue)

                setup_revenue.artnr = to_int(entry(0, st5, "-"))
                setup_revenue.flag = "Room"
                setup_revenue.departement = 0

                if entry(1, st5, "-") == ("YES").lower() :
                    setup_revenue.flag_grup = logical(entry(1, st5, "-"))
                    setup_revenue.descr = entry(2, st5, "-")

        if substring(st2, 0, 13) == ("$otherincome$").lower()  and substring(st2, 13, 3) == ("YES").lower() :
            st6 = substring(st2, 13, 3)
            st7 = substring(st2, 17)


            for n3 in range(1,num_entries(st7, ",")  + 1) :
                st8 = entry(n3 - 1, st7, ",")
                setup_revenue = Setup_revenue()
                setup_revenue_list.append(setup_revenue)

                setup_revenue.artnr = to_int(entry(0, st8, "-"))
                setup_revenue.flag = "Other"
                setup_revenue.departement = 0

                if entry(1, st8, "-") == ("YES").lower() :
                    setup_revenue.flag_grup = logical(entry(1, st8, "-"))
                    setup_revenue.descr = entry(2, st8, "-")

        if substring(st2, 0, 9) == ("$segment$").lower()  and substring(st2, 9, 3) == ("YES").lower() :
            st29 = substring(st2, 13)
            for n23 in range(1,num_entries(st29, ",")  + 1) :
                st30 = entry(n23 - 1, st29, ",")
                setup_segment = Setup_segment()
                setup_segment_list.append(setup_segment)

                setup_segment.artnr = to_int(entry(0, st30, "-"))
                setup_segment.flag = "Segment"
                setup_segment.departement = 0

                if entry(1, st30, "-") == ("YES").lower() :
                    setup_segment.flag_grup = logical(entry(1, st30, "-"))
                    setup_segment.descr = entry(2, st30, "-")

        if substring(st2, 0, 11) == ("$statistic$").lower()  and substring(st2, 11, 3) == ("YES").lower() :
            st31 = substring(st2, 15)
            for n24 in range(1,num_entries(st31, "/")  + 1) :
                st32 = entry(n24 - 1, st31, "/")

                if n24 == 1 and st32 != "":
                    zwkum = to_int(entry(0, st32, "/"))

                elif n24 > 1 and st32 != "":
                    for n25 in range(1,num_entries(st32, ",")  + 1) :
                        st33 = entry(n25 - 1, st32, ",")
                        setup_stat = Setup_stat()
                        setup_stat_list.append(setup_stat)

                        setup_stat.zwkum = zwkum


                        for n26 in range(1,num_entries(st33, "-")  + 1) :
                            setup_stat.artnr = to_int(entry(0, st33, "-"))
                            setup_stat.descr = entry(1, st33, "-")
                            setup_stat.flag = "Statistic"


    for n4 in range(1,num_entries(str3, "*")  + 1) :
        st9 = entry(n4 - 1, str3, "*")

        if substring(st9, 0, 16) == ("$revenueOutlets$").lower()  and substring(st9, 16, 3) == ("YES").lower() :
            st10 = substring(st9, 19)


            for n5 in range(1,num_entries(st10, ";")  + 1) :
                st11 = entry(n5 - 1, st10, ";")
                for n6 in range(1,num_entries(st11, "|")  + 1) :
                    st12 = entry(n6 - 1, st11, "|")

                    if n6 == 1 and st12 != "" and entry(1, st11, "|") != "":
                        dept = to_int(st12)

                    elif st12 != "" and n6 > 1:
                        for n7 in range(1,num_entries(st12, ",")  + 1) :
                            st13 = entry(n7 - 1, st12, ",")

                            if st13 != "":
                                setup_revenue = Setup_revenue()
                                setup_revenue_list.append(setup_revenue)

                                setup_revenue.departement = dept
                                setup_revenue.artnr = to_int(entry(0, st13, "-"))
                                setup_revenue.flag = "Outlet"

                                if entry(1, st13, "-") == ("YES").lower() :
                                    setup_revenue.flag_grup = logical(entry(1, st13, "-"))
                                    setup_revenue.descr = entry(2, st13, "-")

        if substring(st9, 0, 9) == ("$FBcover$").lower()  and substring(st9, 9, 3) == ("YES").lower() :
            st23 = substring(st9, 12)


            for n18 in range(1,num_entries(st23, ";")  + 1) :
                st24 = entry(n18 - 1, st23, ";")
                for n19 in range(1,num_entries(st24, "|")  + 1) :
                    st25 = entry(n19 - 1, st24, "|")

                    if n19 == 1 and st25 != "" and entry(1, st24, "|") != "":
                        dept1 = to_int(st25)

                    elif st25 != "" and n19 > 1:
                        for n20 in range(1,num_entries(st25, "-")  + 1) :
                            st26 = entry(n20 - 1, st25, "-")

                            if substring(st26, 0, 1) == ("F").lower() :
                                st27 = substring(st26, 1)
                                for n21 in range(1,num_entries(st27, ",")  + 1) :
                                    setup_fbcover = Setup_fbcover()
                                    setup_fbcover_list.append(setup_fbcover)

                                    setup_fbcover.departement = dept1
                                    setup_fbcover.artnr = to_int(entry(n21 - 1, st27, ","))

                                    if dept1 == banq_dept:
                                        setup_fbcover.flag = "3Banquet"


                                    else:
                                        setup_fbcover.flag = "1Food"

                            elif substring(st26, 0, 1) == ("B").lower() :
                                st28 = substring(st26, 1)
                                for n22 in range(1,num_entries(st28, ",")  + 1) :
                                    setup_fbcover = Setup_fbcover()
                                    setup_fbcover_list.append(setup_fbcover)

                                    setup_fbcover.departement = dept1
                                    setup_fbcover.artnr = to_int(entry(n22 - 1, st28, ","))

                                    if dept1 == banq_dept:
                                        setup_fbcover.flag = "3Banquet"


                                    else:
                                        setup_fbcover.flag = "2Beverage"

                            elif substring(st26, 0, 1) == ("M").lower() :
                                st28 = substring(st26, 1)
                                for n22 in range(1,num_entries(st28, ",")  + 1) :
                                    setup_fbcover = Setup_fbcover()
                                    setup_fbcover_list.append(setup_fbcover)

                                    setup_fbcover.departement = dept1
                                    setup_fbcover.artnr = to_int(entry(n22 - 1, st28, ","))

                                    if dept1 == banq_dept:
                                        setup_fbcover.flag = "3Banquet"


                                    else:
                                        setup_fbcover.flag = "4Material"
    for n8 in range(1,num_entries(str1, ";")  + 1) :
        st14 = entry(n8 - 1, str1, ";")

        if substring(st14, 0, 10) == ("$otherPay$").lower()  and substring(st14, 10, 3) == ("YES").lower() :
            st15 = substring(st14, 14)
            for n9 in range(1,num_entries(st15, ",")  + 1) :
                st16 = entry(n9 - 1, st15, ",")

                if st16 != "":
                    setup_revenue = Setup_revenue()
                    setup_revenue_list.append(setup_revenue)

                    setup_revenue.departement = 0
                    setup_revenue.artnr = to_int(entry(n9 - 1, st15, ","))
                    setup_revenue.flag = "OtherPayable"


    for n10 in range(1,num_entries(str1, ";")  + 1) :
        st17 = entry(n10 - 1, str1, ";")

        if substring(st17, 0, 9) == ("$payment$").lower()  and substring(st17, 9, 3) == ("YES").lower() :
            st18 = substring(st17, 13)
            for n11 in range(1,num_entries(st18, ",")  + 1) :
                setup_payment = Setup_payment()
                setup_payment_list.append(setup_payment)

                setup_payment.artnr = to_int(entry(n11 - 1, st18, ","))
                setup_payment.artart = 7
                setup_payment.umsatzart = 0
                setup_payment.flag = True

        elif substring(st17, 0, 8) == ("$ledger$").lower()  and substring(st17, 8, 3) == ("YES").lower() :
            st19 = substring(st17, 12)
            for n12 in range(1,num_entries(st19, ",")  + 1) :
                setup_payment = Setup_payment()
                setup_payment_list.append(setup_payment)

                setup_payment.artnr = to_int(entry(n12 - 1, st19, ","))
                setup_payment.artart = 2
                setup_payment.umsatzart = 0
                setup_payment.flag = True

        elif substring(st17, 0, 6) == ("$cash$").lower()  and substring(st17, 6, 3) == ("YES").lower() :
            st20 = substring(st17, 10)
            for n13 in range(1,num_entries(st20, ",")  + 1) :
                setup_payment = Setup_payment()
                setup_payment_list.append(setup_payment)

                setup_payment.artnr = to_int(entry(n13 - 1, st20, ","))
                setup_payment.artart = 6
                setup_payment.umsatzart = 0
                setup_payment.flag = True

        elif substring(st17, 0, 9) == ("$foreign$").lower()  and substring(st17, 9, 3) == ("YES").lower() :
            st21 = substring(st17, 13)
            for n14 in range(1,num_entries(st21, ",")  + 1) :
                setup_payment = Setup_payment()
                setup_payment_list.append(setup_payment)

                setup_payment.artnr = to_int(entry(n14 - 1, st21, ","))
                setup_payment.artart = 6
                setup_payment.umsatzart = 4
                setup_payment.flag = True

        elif substring(st17, 0, 9) == ("$deposit$").lower()  and substring(st17, 9, 3) == ("YES").lower() :
            st22 = substring(st17, 13)
            for n15 in range(1,num_entries(st22, ",")  + 1) :
                setup_payment = Setup_payment()
                setup_payment_list.append(setup_payment)

                setup_payment.artnr = to_int(entry(n15 - 1, st22, ","))
                setup_payment.artart = 5
                setup_payment.umsatzart = 0
                setup_payment.flag = True

        elif substring(st17, 0, 8) == ("$Gsheet$").lower() :
            gsheet_link = substring(st17, 8)

    for setup_revenue in query(setup_revenue_list, sort_by=[("flag",True),("departement",False),("flag_grup",True),("descr",False)]):

        artikel = db_session.query(Artikel).filter(
                 (Artikel.departement == setup_revenue.departement) & (Artikel.artnr == setup_revenue.artnr)).first()

        if artikel:

            if setup_revenue.flag.lower()  == ("OtherPayable").lower() :
                create_payable_list()
            else:
                create_rev_list()

    for setup_segment in query(setup_segment_list):

        segment = db_session.query(Segment).filter(
                 (Segment.segmentcode == setup_segment.artnr)).first()

        if segment:
            fill_revenue_segement()
            fill_revenue_segement1()

    for setup_payment in query(setup_payment_list):

        artikel = db_session.query(Artikel).filter(
                 (Artikel.departement == setup_payment.departement) & (Artikel.artnr == setup_payment.artnr) & (Artikel.artart == setup_payment.artart) & (Artikel.umsatzart == setup_payment.umsatzart)).first()

        if artikel:
            ct2 = ct2 + 1
            create_payment_list()

    for setup_fbcover in query(setup_fbcover_list, sort_by=[("departement",False)]):

        hoteldpt = db_session.query(Hoteldpt).filter(
                 (Hoteldpt.num == setup_fbcover.departement)).first()

        artikel = db_session.query(Artikel).filter(
                 (Artikel.artnr == setup_fbcover.artnr) & (Artikel.departement == setup_fbcover.departement)).first()

        if artikel:
            create_fbcover()

    for rev_list in query(rev_list_list, sort_by=[("flag",False),("departement",False)]):

        if curr_flag != "" and rev_list.flag.lower()  != ("zeich-dept").lower()  and (curr_flag != rev_list.flag.lower() ) and curr_dept == 0:

            if curr_flag.lower()  == ("Room").lower() :
                b_rev_list = B_rev_list()
                b_rev_list_list.append(b_rev_list)

                b_rev_list.ct = ct + 1
                b_rev_list.descr = "TOTAL ROOM REVENUE"
                b_rev_list.departement = 0
                b_rev_list.t_day =  to_decimal(tot_today)
                b_rev_list.dper =  to_decimal(tot_today_per)
                b_rev_list.mtd =  to_decimal(tot_mtd)
                b_rev_list.mtd_per =  to_decimal(tot_mtd_per)
                b_rev_list.mtd_budget =  to_decimal(tot_mtd_budget)
                b_rev_list.variance =  to_decimal(tot_variance)
                b_rev_list.ytd =  to_decimal(tot_ytd)
                b_rev_list.ytd_budget =  to_decimal(tot_ytd_budget)
                b_rev_list.ytd_per =  to_decimal(tot_ytd_per)
                b_rev_list.flag = "Room"
                tot_today =  to_decimal("0")
                tot_today_per =  to_decimal("0")
                tot_mtd =  to_decimal("0")
                tot_mtd_per =  to_decimal("0")
                tot_mtd_budget =  to_decimal("0")
                tot_variance =  to_decimal("0")
                tot_ytd =  to_decimal("0")
                tot_ytd_budget =  to_decimal("0")
                tot_ytd_per =  to_decimal("0")

            elif curr_flag.lower()  == ("Other").lower() :
                b_rev_list = B_rev_list()
                b_rev_list_list.append(b_rev_list)

                b_rev_list.ct = ct + 1
                b_rev_list.descr = "TOTAL OTHER REVENUE"
                b_rev_list.departement = 0
                b_rev_list.t_day =  to_decimal(tot_today1)
                b_rev_list.dper =  to_decimal(tot_today_per1)
                b_rev_list.mtd =  to_decimal(tot_mtd1)
                b_rev_list.mtd_per =  to_decimal(tot_mtd_per1)
                b_rev_list.mtd_budget =  to_decimal(tot_mtd_budget1)
                b_rev_list.variance =  to_decimal(tot_variance1)
                b_rev_list.ytd =  to_decimal(tot_ytd1)
                b_rev_list.ytd_budget =  to_decimal(tot_ytd_budget1)
                b_rev_list.ytd_per =  to_decimal(tot_ytd_per1)
                b_rev_list.flag = "Other"
                tot_today1 =  to_decimal("0")
                tot_today_per1 =  to_decimal("0")
                tot_mtd1 =  to_decimal("0")
                tot_mtd_per1 =  to_decimal("0")
                tot_mtd_budget1 =  to_decimal("0")
                tot_variance1 =  to_decimal("0")
                tot_ytd1 =  to_decimal("0")
                tot_ytd_budget1 =  to_decimal("0")
                tot_ytd_per1 =  to_decimal("0")

        elif curr_flag.lower()  != "" and curr_flag.lower()  != ("zeich-dept").lower()  and curr_dept != 0 and curr_dept != rev_list.departement:

            hoteldpt = db_session.query(Hoteldpt).filter(
                     (Hoteldpt.num == curr_dept)).first()
            b_rev_list = B_rev_list()
            b_rev_list_list.append(b_rev_list)

            b_rev_list.ct = ct + 1
            b_rev_list.descr = "TOTAL " + hoteldpt.depart + " REVENUE"
            b_rev_list.departement = curr_dept
            b_rev_list.t_day =  to_decimal(tot_today2)
            b_rev_list.dper =  to_decimal(tot_today_per2)
            b_rev_list.mtd =  to_decimal(tot_mtd2)
            b_rev_list.mtd_per =  to_decimal(tot_mtd_per2)
            b_rev_list.mtd_budget =  to_decimal(tot_mtd_budget2)
            b_rev_list.variance =  to_decimal(tot_variance2)
            b_rev_list.ytd =  to_decimal(tot_ytd2)
            b_rev_list.ytd_budget =  to_decimal(tot_ytd_budget2)
            b_rev_list.ytd_per =  to_decimal(tot_ytd_per2)
            b_rev_list.flag = "Outlet"
            tot_today2 =  to_decimal("0")
            tot_today_per2 =  to_decimal("0")
            tot_mtd2 =  to_decimal("0")
            tot_mtd_per2 =  to_decimal("0")
            tot_mtd_budget2 =  to_decimal("0")
            tot_variance2 =  to_decimal("0")
            tot_ytd2 =  to_decimal("0")
            tot_ytd_budget2 =  to_decimal("0")
            tot_ytd_per2 =  to_decimal("0")


        curr_flag = rev_list.flag
        curr_dept = rev_list.departement

        if rev_list.flag.lower()  == ("Room").lower() :
            tot_today =  to_decimal(tot_today) + to_decimal(rev_list.t_day)
            tot_today_per =  to_decimal(tot_today_per) + to_decimal(rev_list.dper)
            tot_mtd =  to_decimal(tot_mtd) + to_decimal(rev_list.mtd)
            tot_mtd_per =  to_decimal(tot_mtd_per) + to_decimal(rev_list.mtd_per)
            tot_mtd_budget =  to_decimal(tot_mtd_budget) + to_decimal(rev_list.mtd_budget)
            tot_variance =  to_decimal(tot_variance) + to_decimal(rev_list.variance)
            tot_ytd =  to_decimal(tot_ytd) + to_decimal(rev_list.ytd)
            tot_ytd_budget =  to_decimal(tot_ytd_budget) + to_decimal(rev_list.ytd_budget)
            tot_ytd_per =  to_decimal(tot_ytd_per) + to_decimal(rev_list.ytd_per)

        elif rev_list.flag.lower()  == ("Other").lower() :
            tot_today1 =  to_decimal(tot_today1) + to_decimal(rev_list.t_day)
            tot_today_per1 =  to_decimal(tot_today_per1) + to_decimal(rev_list.dper)
            tot_mtd1 =  to_decimal(tot_mtd1) + to_decimal(rev_list.mtd)
            tot_mtd_per1 =  to_decimal(tot_mtd_per1) + to_decimal(rev_list.mtd_per)
            tot_mtd_budget1 =  to_decimal(tot_mtd_budget1) + to_decimal(rev_list.mtd_budget)
            tot_variance1 =  to_decimal(tot_variance1) + to_decimal(rev_list.variance)
            tot_ytd1 =  to_decimal(tot_ytd1) + to_decimal(rev_list.ytd)
            tot_ytd_budget1 =  to_decimal(tot_ytd_budget1) + to_decimal(rev_list.ytd_budget)
            tot_ytd_per1 =  to_decimal(tot_ytd_per1) + to_decimal(rev_list.ytd_per)

        elif rev_list.flag.lower()  == ("Outlet").lower() :
            tot_today2 =  to_decimal(tot_today2) + to_decimal(rev_list.t_day)
            tot_today_per2 =  to_decimal(tot_today_per2) + to_decimal(rev_list.dper)
            tot_mtd2 =  to_decimal(tot_mtd2) + to_decimal(rev_list.mtd)
            tot_mtd_per2 =  to_decimal(tot_mtd_per2) + to_decimal(rev_list.mtd_per)
            tot_mtd_budget2 =  to_decimal(tot_mtd_budget2) + to_decimal(rev_list.mtd_budget)
            tot_variance2 =  to_decimal(tot_variance2) + to_decimal(rev_list.variance)
            tot_ytd2 =  to_decimal(tot_ytd2) + to_decimal(rev_list.ytd)
            tot_ytd_budget2 =  to_decimal(tot_ytd_budget2) + to_decimal(rev_list.ytd_budget)
            tot_ytd_per2 =  to_decimal(tot_ytd_per2) + to_decimal(rev_list.ytd_per)


    b_rev_list = B_rev_list()
    b_rev_list_list.append(b_rev_list)

    b_rev_list.ct = ct + 1
    b_rev_list.descr = "TOTAL ROOM REVENUE"
    b_rev_list.departement = 0
    b_rev_list.t_day =  to_decimal(tot_today)
    b_rev_list.dper =  to_decimal(tot_today_per)
    b_rev_list.mtd =  to_decimal(tot_mtd)
    b_rev_list.mtd_per =  to_decimal(tot_mtd_per)
    b_rev_list.mtd_budget =  to_decimal(tot_mtd_budget)
    b_rev_list.variance =  to_decimal(tot_variance)
    b_rev_list.ytd =  to_decimal(tot_ytd)
    b_rev_list.ytd_budget =  to_decimal(tot_ytd_budget)
    b_rev_list.ytd_per =  to_decimal(tot_ytd_per)
    b_rev_list.flag = "Room"

    for brev_list in query(brev_list_list):

        if substring(brev_list.descr, 0, 5) == ("TOTAL").lower() :
            t_today =  to_decimal(t_today) + to_decimal(brev_list.t_day)
            t_today_per =  to_decimal(t_today_per) + to_decimal(brev_list.dper)
            t_mtd =  to_decimal(t_mtd) + to_decimal(brev_list.mtd)
            t_mtd_per =  to_decimal(t_mtd_per) + to_decimal(brev_list.mtd_per)
            t_mtd_budget =  to_decimal(t_mtd_budget) + to_decimal(brev_list.mtd_budget)
            t_variance =  to_decimal(t_variance) + to_decimal(brev_list.variance)
            t_ytd =  to_decimal(t_ytd) + to_decimal(brev_list.ytd)
            t_ytd_budget =  to_decimal(t_ytd_budget) + to_decimal(brev_list.ytd_budget)
            t_ytd_per =  to_decimal(t_ytd_per) + to_decimal(brev_list.ytd_per)


    ct = ct + 1 + 1
    rev_list = Rev_list()
    rev_list_list.append(rev_list)

    rev_list.ct = ct
    rev_list.descr = "TOTAL NETT REVENUE"
    rev_list.departement = 100
    rev_list.t_day =  to_decimal(t_today)
    rev_list.dper =  to_decimal("100")
    rev_list.mtd =  to_decimal(t_mtd)
    rev_list.mtd_per =  to_decimal("100")
    rev_list.mtd_budget =  to_decimal(t_mtd_budget)
    rev_list.variance =  to_decimal(t_variance)
    rev_list.ytd =  to_decimal(t_ytd)
    rev_list.ytd_budget =  to_decimal(t_ytd_budget)
    rev_list.ytd_per =  to_decimal("100")
    rev_list.flag = "D"

    for rev_list in query(rev_list_list, sort_by=[("flag",False)]):

        if rev_list.t_day != 0:
            rev_list.dper = ( to_decimal(rev_list.t_day) / to_decimal(t_today)) * to_decimal("100")

        if rev_list.mtd != 0:
            rev_list.mtd_per = ( to_decimal(rev_list.mtd) / to_decimal(t_mtd)) * to_decimal("100")

        if rev_list.ytd != 0:
            rev_list.ytd_per = ( to_decimal(rev_list.ytd) / to_decimal(t_ytd)) * to_decimal("100")
    ct = ct + 1
    rev_list = Rev_list()
    rev_list_list.append(rev_list)

    rev_list.ct = ct
    rev_list.descr = "Service Charge"
    rev_list.departement = 101
    rev_list.t_day =  to_decimal(t_day_serv)
    rev_list.dper =  to_decimal("100")
    rev_list.mtd =  to_decimal(mtd_serv)
    rev_list.mtd_per =  to_decimal("100")
    rev_list.mtd_budget =  to_decimal("0")
    rev_list.variance =  to_decimal("0")
    rev_list.ytd =  to_decimal(ytd_serv)
    rev_list.ytd_budget =  to_decimal("0")
    rev_list.ytd_per =  to_decimal("100")
    rev_list.flag = "B"


    ct = ct + 1
    rev_list = Rev_list()
    rev_list_list.append(rev_list)

    rev_list.ct = ct
    rev_list.descr = "Government Tax"
    rev_list.departement = 101
    rev_list.t_day =  to_decimal(t_day_tax)
    rev_list.dper =  to_decimal("100")
    rev_list.mtd =  to_decimal(mtd_tax)
    rev_list.mtd_per =  to_decimal("100")
    rev_list.mtd_budget =  to_decimal("0")
    rev_list.variance =  to_decimal("0")
    rev_list.ytd =  to_decimal(ytd_tax)
    rev_list.ytd_budget =  to_decimal("0")
    rev_list.ytd_per =  to_decimal("100")
    rev_list.flag = "C"


    ct = ct + 1
    rev_list = Rev_list()
    rev_list_list.append(rev_list)

    rev_list.ct = ct
    rev_list.descr = "TOTAL GROSS REVENUE"
    rev_list.departement = 102
    rev_list.t_day =  to_decimal(t_day_serv) + to_decimal(t_day_tax) + to_decimal(t_today)
    rev_list.dper =  to_decimal("100")
    rev_list.mtd =  to_decimal(mtd_serv) + to_decimal(mtd_tax) + to_decimal(t_mtd)
    rev_list.mtd_per =  to_decimal("100")
    rev_list.mtd_budget =  to_decimal("0")
    rev_list.variance =  to_decimal("0")
    rev_list.ytd =  to_decimal(ytd_serv) + to_decimal(ytd_tax) + to_decimal(t_ytd)
    rev_list.ytd_budget =  to_decimal("0")
    rev_list.ytd_per =  to_decimal("100")
    rev_list.flag = "A"

    for payment_list in query(payment_list_list, sort_by=[("flag",False),("departement",False)]):

        if curr_flag1 != "" and (curr_flag1 != payment_list.flag):

            if curr_flag.lower()  == ("1Cash").lower() :
                b_payment_list = B_payment_list()
                b_payment_list_list.append(b_payment_list)

                b_payment_list.ct = ct2 + 1
                b_payment_list.descr = "TOTAL CASH"
                b_payment_list.departement = 0
                b_payment_list.t_day =  to_decimal(tot_today3)
                b_payment_list.mtd =  to_decimal(tot_mtd3)
                b_payment_list.mtd_budget =  to_decimal(tot_mtd_budget3)
                b_payment_list.variance =  to_decimal(tot_variance3)
                b_payment_list.ytd =  to_decimal(tot_ytd3)
                b_payment_list.ytd_budget =  to_decimal(tot_ytd_budget3)
                b_payment_list.flag = "1Cash"
                tot_today3 =  to_decimal("0")
                tot_mtd3 =  to_decimal("0")
                tot_mtd_budget3 =  to_decimal("0")
                tot_variance3 =  to_decimal("0")
                tot_ytd3 =  to_decimal("0")
                tot_ytd_budget3 =  to_decimal("0")

            if curr_flag.lower()  == ("2Payment").lower() :
                b_payment_list = B_payment_list()
                b_payment_list_list.append(b_payment_list)

                b_payment_list.ct = ct2 + 1
                b_payment_list.descr = "TOTAL CREDIT CARD"
                b_payment_list.departement = 0
                b_payment_list.t_day =  to_decimal(tot_today4)
                b_payment_list.mtd =  to_decimal(tot_mtd4)
                b_payment_list.mtd_budget =  to_decimal(tot_mtd_budget4)
                b_payment_list.variance =  to_decimal(tot_variance4)
                b_payment_list.ytd =  to_decimal(tot_ytd4)
                b_payment_list.ytd_budget =  to_decimal(tot_ytd_budget4)
                b_payment_list.flag = "2Payment"
                tot_today4 =  to_decimal("0")
                tot_mtd4 =  to_decimal("0")
                tot_mtd_budget4 =  to_decimal("0")
                tot_variance4 =  to_decimal("0")
                tot_ytd4 =  to_decimal("0")
                tot_ytd_budget4 =  to_decimal("0")

            if curr_flag.lower()  == ("3Ledger").lower() :
                b_payment_list = B_payment_list()
                b_payment_list_list.append(b_payment_list)

                b_payment_list.ct = ct2 + 1
                b_payment_list.descr = "TOTAL CITY LEDGER"
                b_payment_list.departement = 0
                b_payment_list.t_day =  to_decimal(tot_today5)
                b_payment_list.mtd =  to_decimal(tot_mtd5)
                b_payment_list.mtd_budget =  to_decimal(tot_mtd_budget5)
                b_payment_list.variance =  to_decimal(tot_variance5)
                b_payment_list.ytd =  to_decimal(tot_ytd5)
                b_payment_list.ytd_budget =  to_decimal(tot_ytd_budget5)
                b_payment_list.flag = "3Ledger"
                tot_today5 =  to_decimal("0")
                tot_mtd5 =  to_decimal("0")
                tot_mtd_budget5 =  to_decimal("0")
                tot_variance5 =  to_decimal("0")
                tot_ytd5 =  to_decimal("0")
                tot_ytd_budget5 =  to_decimal("0")

            if curr_flag.lower()  == ("4Foreign").lower() :
                b_payment_list = B_payment_list()
                b_payment_list_list.append(b_payment_list)

                b_payment_list.ct = ct2 + 1
                b_payment_list.descr = "TOTAL FOREIGN"
                b_payment_list.departement = 0
                b_payment_list.t_day =  to_decimal(tot_today6)
                b_payment_list.mtd =  to_decimal(tot_mtd6)
                b_payment_list.mtd_budget =  to_decimal(tot_mtd_budget6)
                b_payment_list.variance =  to_decimal(tot_variance6)
                b_payment_list.ytd =  to_decimal(tot_ytd6)
                b_payment_list.ytd_budget =  to_decimal(tot_ytd_budget6)
                b_payment_list.flag = "4Foreign"
                tot_today6 =  to_decimal("0")
                tot_mtd6 =  to_decimal("0")
                tot_mtd_budget6 =  to_decimal("0")
                tot_variance6 =  to_decimal("0")
                tot_ytd6 =  to_decimal("0")
                tot_ytd_budget6 =  to_decimal("0")

            if curr_flag.lower()  == ("4Foreign").lower() :
                b_payment_list = B_payment_list()
                b_payment_list_list.append(b_payment_list)

                b_payment_list.ct = ct2 + 1
                b_payment_list.descr = "TOTAL FOREIGN"
                b_payment_list.departement = 0
                b_payment_list.t_day =  to_decimal(tot_today6)
                b_payment_list.mtd =  to_decimal(tot_mtd6)
                b_payment_list.mtd_budget =  to_decimal(tot_mtd_budget6)
                b_payment_list.variance =  to_decimal(tot_variance6)
                b_payment_list.ytd =  to_decimal(tot_ytd6)
                b_payment_list.ytd_budget =  to_decimal(tot_ytd_budget6)
                b_payment_list.flag = "4Foreign"
                tot_today6 =  to_decimal("0")
                tot_mtd6 =  to_decimal("0")
                tot_mtd_budget6 =  to_decimal("0")
                tot_variance6 =  to_decimal("0")
                tot_ytd6 =  to_decimal("0")
                tot_ytd_budget6 =  to_decimal("0")

            if curr_flag.lower()  == ("5Deposit").lower() :
                b_payment_list = B_payment_list()
                b_payment_list_list.append(b_payment_list)

                b_payment_list.ct = ct2 + 1
                b_payment_list.descr = "TOTAL ADVANCE DEPOSIT"
                b_payment_list.departement = 0
                b_payment_list.t_day =  to_decimal(tot_today7)
                b_payment_list.mtd =  to_decimal(tot_mtd7)
                b_payment_list.mtd_budget =  to_decimal(tot_mtd_budget7)
                b_payment_list.variance =  to_decimal(tot_variance7)
                b_payment_list.ytd =  to_decimal(tot_ytd7)
                b_payment_list.ytd_budget =  to_decimal(tot_ytd_budget7)
                b_payment_list.flag = "5Deposit"
                tot_today7 =  to_decimal("0")
                tot_mtd7 =  to_decimal("0")
                tot_mtd_budget7 =  to_decimal("0")
                tot_variance7 =  to_decimal("0")
                tot_ytd7 =  to_decimal("0")
                tot_ytd_budget7 =  to_decimal("0")


        curr_flag = payment_list.flag

        if payment_list.flag.lower()  == ("1Cash").lower() :
            tot_today3 =  to_decimal(tot_today3) + to_decimal(payment_list.t_day)
            tot_mtd3 =  to_decimal(tot_mtd3) + to_decimal(payment_list.mtd)
            tot_mtd_budget3 =  to_decimal(tot_mtd_budget3) + to_decimal(payment_list.mtd_budget)
            tot_variance3 =  to_decimal(tot_variance3) + to_decimal(payment_list.variance)
            tot_ytd3 =  to_decimal(tot_ytd3) + to_decimal(payment_list.ytd)
            tot_ytd_budget3 =  to_decimal(tot_ytd_budget3) + to_decimal(payment_list.ytd_budget)

        if payment_list.flag.lower()  == ("2Payment").lower() :
            tot_today4 =  to_decimal(tot_today4) + to_decimal(payment_list.t_day)
            tot_mtd4 =  to_decimal(tot_mtd4) + to_decimal(payment_list.mtd)
            tot_mtd_budget4 =  to_decimal(tot_mtd_budget4) + to_decimal(payment_list.mtd_budget)
            tot_variance4 =  to_decimal(tot_variance4) + to_decimal(payment_list.variance)
            tot_ytd4 =  to_decimal(tot_ytd4) + to_decimal(payment_list.ytd)
            tot_ytd_budget4 =  to_decimal(tot_ytd_budget4) + to_decimal(payment_list.ytd_budget)

        if payment_list.flag.lower()  == ("3Ledger").lower() :
            tot_today5 =  to_decimal(tot_today5) + to_decimal(payment_list.t_day)
            tot_mtd5 =  to_decimal(tot_mtd5) + to_decimal(payment_list.mtd)
            tot_mtd_budget5 =  to_decimal(tot_mtd_budget5) + to_decimal(payment_list.mtd_budget)
            tot_variance5 =  to_decimal(tot_variance5) + to_decimal(payment_list.variance)
            tot_ytd5 =  to_decimal(tot_ytd5) + to_decimal(payment_list.ytd)
            tot_ytd_budget5 =  to_decimal(tot_ytd_budget5) + to_decimal(payment_list.ytd_budget)

        if payment_list.flag.lower()  == ("4Foreign").lower() :
            tot_today6 =  to_decimal(tot_today6) + to_decimal(payment_list.t_day)
            tot_mtd6 =  to_decimal(tot_mtd6) + to_decimal(payment_list.mtd)
            tot_mtd_budget6 =  to_decimal(tot_mtd_budget6) + to_decimal(payment_list.mtd_budget)
            tot_variance6 =  to_decimal(tot_variance6) + to_decimal(payment_list.variance)
            tot_ytd6 =  to_decimal(tot_ytd6) + to_decimal(payment_list.ytd)
            tot_ytd_budget6 =  to_decimal(tot_ytd_budget6) + to_decimal(payment_list.ytd_budget)

        if payment_list.flag.lower()  == ("5Deposit").lower() :
            tot_today7 =  to_decimal(tot_today7) + to_decimal(payment_list.t_day)
            tot_mtd7 =  to_decimal(tot_mtd7) + to_decimal(payment_list.mtd)
            tot_mtd_budget7 =  to_decimal(tot_mtd_budget7) + to_decimal(payment_list.mtd_budget)
            tot_variance7 =  to_decimal(tot_variance7) + to_decimal(payment_list.variance)
            tot_ytd7 =  to_decimal(tot_ytd7) + to_decimal(payment_list.ytd)
            tot_ytd_budget7 =  to_decimal(tot_ytd_budget7) + to_decimal(payment_list.ytd_budget)


    b_payment_list = B_payment_list()
    b_payment_list_list.append(b_payment_list)

    b_payment_list.ct = ct2 + 1
    b_payment_list.descr = "TOTAL CASH"
    b_payment_list.departement = 0
    b_payment_list.t_day =  to_decimal(tot_today3)
    b_payment_list.mtd =  to_decimal(tot_mtd3)
    b_payment_list.mtd_budget =  to_decimal(tot_mtd_budget3)
    b_payment_list.variance =  to_decimal(tot_variance3)
    b_payment_list.ytd =  to_decimal(tot_ytd3)
    b_payment_list.ytd_budget =  to_decimal(tot_ytd_budget3)
    b_payment_list.flag = "1Cash"


    b_payment_list = B_payment_list()
    b_payment_list_list.append(b_payment_list)

    b_payment_list.ct = ct2 + 1
    b_payment_list.descr = "TOTAL CREDIT CARD"
    b_payment_list.departement = 0
    b_payment_list.t_day =  to_decimal(tot_today4)
    b_payment_list.mtd =  to_decimal(tot_mtd4)
    b_payment_list.mtd_budget =  to_decimal(tot_mtd_budget4)
    b_payment_list.variance =  to_decimal(tot_variance4)
    b_payment_list.ytd =  to_decimal(tot_ytd4)
    b_payment_list.ytd_budget =  to_decimal(tot_ytd_budget4)
    b_payment_list.flag = "2Payment"


    b_payment_list = B_payment_list()
    b_payment_list_list.append(b_payment_list)

    b_payment_list.ct = ct2 + 1
    b_payment_list.descr = "TOTAL CITY LEDGER"
    b_payment_list.departement = 0
    b_payment_list.t_day =  to_decimal(tot_today5)
    b_payment_list.mtd =  to_decimal(tot_mtd5)
    b_payment_list.mtd_budget =  to_decimal(tot_mtd_budget5)
    b_payment_list.variance =  to_decimal(tot_variance5)
    b_payment_list.ytd =  to_decimal(tot_ytd5)
    b_payment_list.ytd_budget =  to_decimal(tot_ytd_budget5)
    b_payment_list.flag = "3Ledger"


    b_payment_list = B_payment_list()
    b_payment_list_list.append(b_payment_list)

    b_payment_list.ct = ct2 + 1
    b_payment_list.descr = "TOTAL FOREIGN"
    b_payment_list.departement = 0
    b_payment_list.t_day =  to_decimal(tot_today6)
    b_payment_list.mtd =  to_decimal(tot_mtd6)
    b_payment_list.mtd_budget =  to_decimal(tot_mtd_budget6)
    b_payment_list.variance =  to_decimal(tot_variance6)
    b_payment_list.ytd =  to_decimal(tot_ytd6)
    b_payment_list.ytd_budget =  to_decimal(tot_ytd_budget6)
    b_payment_list.flag = "4Foreign"


    b_payment_list = B_payment_list()
    b_payment_list_list.append(b_payment_list)

    b_payment_list.ct = ct2 + 1
    b_payment_list.descr = "TOTAL ADVANCE DEPOSIT"
    b_payment_list.departement = 0
    b_payment_list.t_day =  to_decimal(tot_today7)
    b_payment_list.mtd =  to_decimal(tot_mtd7)
    b_payment_list.mtd_budget =  to_decimal(tot_mtd_budget7)
    b_payment_list.variance =  to_decimal(tot_variance7)
    b_payment_list.ytd =  to_decimal(tot_ytd7)
    b_payment_list.ytd_budget =  to_decimal(tot_ytd_budget7)
    b_payment_list.flag = "5Deposit"

    for b_rev_seg_list in query(b_rev_seg_list_list):
        t_today1 =  to_decimal(t_today1) + to_decimal(b_rev_seg_list.t_day)
        t_mtd1 =  to_decimal(t_mtd1) + to_decimal(b_rev_seg_list.mtd)
        t_mtd_budget1 =  to_decimal(t_mtd_budget1) + to_decimal(b_rev_seg_list.mtd_budget)
        t_variance1 =  to_decimal(t_variance1) + to_decimal(b_rev_seg_list.variance)
        t_ytd1 =  to_decimal(t_ytd1) + to_decimal(b_rev_seg_list.ytd)
        t_ytd_budget1 =  to_decimal(t_ytd_budget1) + to_decimal(b_rev_seg_list.ytd_budget)


    rev_seg_list = Rev_seg_list()
    rev_seg_list_list.append(rev_seg_list)

    rev_seg_list.ct = 9999
    rev_seg_list.descr = "TOTAL OCCUPANCY BY GUEST SEGMENT"
    rev_seg_list.departement = 100
    rev_seg_list.t_day =  to_decimal(t_today1)
    rev_seg_list.dper =  to_decimal("100")
    rev_seg_list.mtd =  to_decimal(t_mtd1)
    rev_seg_list.mtd_per =  to_decimal("100")
    rev_seg_list.mtd_budget =  to_decimal(t_mtd_budget1)
    rev_seg_list.variance =  to_decimal(t_variance1)
    rev_seg_list.ytd =  to_decimal(t_ytd1)
    rev_seg_list.ytd_budget =  to_decimal(t_ytd_budget1)
    rev_seg_list.ytd_per =  to_decimal("100")
    rev_seg_list.flag = "ZZ Total"

    for rev_seg_list in query(rev_seg_list_list):

        if rev_seg_list.t_day != 0:
            rev_seg_list.dper = ( to_decimal(rev_seg_list.t_day) / to_decimal(t_today1)) * to_decimal("100")

        if rev_seg_list.mtd != 0:
            rev_seg_list.mtd_per = ( to_decimal(rev_seg_list.mtd) / to_decimal(t_mtd1)) * to_decimal("100")

        if rev_seg_list.ytd != 0:
            rev_seg_list.ytd_per = ( to_decimal(rev_seg_list.ytd) / to_decimal(t_ytd1)) * to_decimal("100")

    for b_rev_seg_list1 in query(b_rev_seg_list1_list):
        t_today11 =  to_decimal(t_today11) + to_decimal(b_rev_seg_list1.t_day)
        t_mtd11 =  to_decimal(t_mtd11) + to_decimal(b_rev_seg_list1.mtd)
        t_mtd_budget11 =  to_decimal(t_mtd_budget11) + to_decimal(b_rev_seg_list1.mtd_budget)
        t_variance11 =  to_decimal(t_variance11) + to_decimal(b_rev_seg_list1.variance)
        t_ytd11 =  to_decimal(t_ytd11) + to_decimal(b_rev_seg_list1.ytd)
        t_ytd_budget11 =  to_decimal(t_ytd_budget11) + to_decimal(b_rev_seg_list1.ytd_budget)


    rev_seg_list1 = Rev_seg_list1()
    rev_seg_list1_list.append(rev_seg_list1)

    rev_seg_list1.ct = 9999
    rev_seg_list1.descr = "TOTAL LODGING BY GUEST SEGMENT"
    rev_seg_list1.departement = 100
    rev_seg_list1.t_day =  to_decimal(t_today11)
    rev_seg_list1.dper =  to_decimal("100")
    rev_seg_list1.mtd =  to_decimal(t_mtd11)
    rev_seg_list1.mtd_per =  to_decimal("100")
    rev_seg_list1.mtd_budget =  to_decimal(t_mtd_budget11)
    rev_seg_list1.variance =  to_decimal(t_variance11)
    rev_seg_list1.ytd =  to_decimal(t_ytd11)
    rev_seg_list1.ytd_budget =  to_decimal(t_ytd_budget11)
    rev_seg_list1.ytd_per =  to_decimal("100")
    rev_seg_list1.flag = "ZZ Total"

    for rev_seg_list1 in query(rev_seg_list1_list):

        if rev_seg_list1.t_day != 0:
            rev_seg_list1.dper = ( to_decimal(rev_seg_list1.t_day) / to_decimal(t_today11)) * to_decimal("100")

        if rev_seg_list1.mtd != 0:
            rev_seg_list1.mtd_per = ( to_decimal(rev_seg_list1.mtd) / to_decimal(t_mtd11)) * to_decimal("100")

        if rev_seg_list1.ytd != 0:
            rev_seg_list1.ytd_per = ( to_decimal(rev_seg_list1.ytd) / to_decimal(t_ytd11)) * to_decimal("100")

    for bpayment_list in query(bpayment_list_list):

        if substring(bpayment_list.descr, 0, 5) == ("TOTAL").lower() :
            t_today2 =  to_decimal(t_today2) + to_decimal(bpayment_list.t_day)
            t_mtd2 =  to_decimal(t_mtd2) + to_decimal(bpayment_list.mtd)
            t_mtd_budget2 =  to_decimal(t_mtd_budget2) + to_decimal(bpayment_list.mtd_budget)
            t_variance2 =  to_decimal(t_variance2) + to_decimal(bpayment_list.variance)
            t_ytd2 =  to_decimal(t_ytd2) + to_decimal(bpayment_list.ytd)
            t_ytd_budget2 =  to_decimal(t_ytd_budget2) + to_decimal(bpayment_list.ytd_budget)


    payment_list = Payment_list()
    payment_list_list.append(payment_list)

    payment_list.ct = 9999
    payment_list.descr = "TOTAL PAYMENT"
    payment_list.departement = 100
    payment_list.t_day =  to_decimal(t_today2)
    payment_list.mtd =  to_decimal(t_mtd2)
    payment_list.mtd_budget =  to_decimal(t_mtd_budget2)
    payment_list.variance =  to_decimal(t_variance2)
    payment_list.ytd =  to_decimal(t_ytd2)
    payment_list.ytd_budget =  to_decimal(t_ytd_budget2)
    payment_list.flag = "ZZ Total"

    for bpayable_list in query(bpayable_list_list):
        t_today3 =  to_decimal(t_today3) + to_decimal(bpayable_list.t_day)
        t_today_per3 =  to_decimal(t_today_per3) + to_decimal(bpayable_list.dper)
        t_mtd3 =  to_decimal(t_mtd3) + to_decimal(bpayable_list.mtd)
        t_mtd_per3 =  to_decimal(t_mtd_per3) + to_decimal(bpayable_list.mtd_per)
        t_mtd_budget3 =  to_decimal(t_mtd_budget3) + to_decimal(bpayable_list.mtd_budget)
        t_variance3 =  to_decimal(t_variance3) + to_decimal(bpayable_list.variance)
        t_ytd3 =  to_decimal(t_ytd3) + to_decimal(bpayable_list.ytd)
        t_ytd_budget3 =  to_decimal(t_ytd_budget3) + to_decimal(bpayable_list.ytd_budget)
        t_ytd_per3 =  to_decimal(t_ytd_per3) + to_decimal(bpayable_list.ytd_per)

    if t_today3 == 0:
        dper = 0
    else:
        dper = 100

    if t_mtd3 == 0:
        mtd_per = 0
    else:
        mtd_per = 100

    if t_ytd3 == 0:
        ytd_per = 0
    else:
        ytd_per = 100
    payable_list = Payable_list()
    payable_list_list.append(payable_list)

    payable_list.ct = 9999
    payable_list.descr = "TOTAL PAYABLE"
    payable_list.departement = 100
    payable_list.t_day =  to_decimal(t_today3)
    payable_list.dper =  to_decimal(dper)
    payable_list.mtd =  to_decimal(t_mtd3)
    payable_list.mtd_per =  to_decimal(mtd_per)
    payable_list.mtd_budget =  to_decimal(t_mtd_budget3)
    payable_list.variance =  to_decimal(t_variance3)
    payable_list.ytd =  to_decimal(t_ytd3)
    payable_list.ytd_budget =  to_decimal(t_ytd_budget3)
    payable_list.ytd_per =  to_decimal(ytd_per)
    payable_list.flag = "ZZ Total"

    for payable_list in query(payable_list_list):

        if payable_list.t_day != 0:
            payable_list.dper = ( to_decimal(payable_list.t_day) / to_decimal(t_today3)) * to_decimal("100")

        if payable_list.mtd != 0:
            payable_list.mtd_per = ( to_decimal(payable_list.mtd) / to_decimal(t_mtd3)) * to_decimal("100")

        if payable_list.ytd != 0:
            payable_list.ytd_per = ( to_decimal(payable_list.ytd) / to_decimal(t_ytd3)) * to_decimal("100")

    for fb_sales_food in query(fb_sales_food_list, sort_by=[("departement",False)]):
        tot_tday_cov =  to_decimal(tot_tday_cov) + to_decimal(fb_sales_food.tday_cov)
        tot_tday_avg =  to_decimal(tot_tday_avg) + to_decimal(fb_sales_food.tday_avg)
        tot_tday_rev =  to_decimal(tot_tday_rev) + to_decimal(fb_sales_food.tday_rev)
        tot_mtd_cov =  to_decimal(tot_mtd_cov) + to_decimal(fb_sales_food.mtd_cov)
        tot_mtd_avg =  to_decimal(tot_mtd_avg) + to_decimal(fb_sales_food.mtd_avg)
        tot_mtd_rev =  to_decimal(tot_mtd_rev) + to_decimal(fb_sales_food.mtd_rev)
        tot_ytd_cov =  to_decimal(tot_ytd_cov) + to_decimal(fb_sales_food.ytd_cov)
        tot_ytd_avg =  to_decimal(tot_ytd_avg) + to_decimal(fb_sales_food.ytd_avg)
        tot_ytd_rev =  to_decimal(tot_ytd_rev) + to_decimal(fb_sales_food.ytd_rev)


    fb_sales_food = Fb_sales_food()
    fb_sales_food_list.append(fb_sales_food)

    fb_sales_food.ct = 9999
    fb_sales_food.departement = 0
    fb_sales_food.artnr = 0
    fb_sales_food.descr = "TOTAL FOOD"
    fb_sales_food.tday_cov =  to_decimal(tot_tday_cov)
    fb_sales_food.tday_avg =  to_decimal(tot_tday_avg)
    fb_sales_food.tday_rev =  to_decimal(tot_tday_rev)
    fb_sales_food.mtd_cov =  to_decimal(tot_mtd_cov)
    fb_sales_food.mtd_avg =  to_decimal(tot_mtd_avg)
    fb_sales_food.mtd_rev =  to_decimal(tot_mtd_rev)
    fb_sales_food.ytd_cov =  to_decimal(tot_ytd_cov)
    fb_sales_food.ytd_avg =  to_decimal(tot_ytd_avg)
    fb_sales_food.ytd_rev =  to_decimal(tot_ytd_rev)
    fb_sales_food.flag = "1Food"


    fb_sales_tot = Fb_sales_tot()
    fb_sales_tot_list.append(fb_sales_tot)

    fb_sales_tot.ct = 1
    fb_sales_tot.descr = "TOTAL FOOD"
    fb_sales_tot.tday_cov =  to_decimal(tot_tday_cov)
    fb_sales_tot.tday_avg =  to_decimal(tot_tday_avg)
    fb_sales_tot.tday_rev =  to_decimal(tot_tday_rev)
    fb_sales_tot.mtd_cov =  to_decimal(tot_mtd_cov)
    fb_sales_tot.mtd_avg =  to_decimal(tot_mtd_avg)
    fb_sales_tot.mtd_rev =  to_decimal(tot_mtd_rev)
    fb_sales_tot.ytd_cov =  to_decimal(tot_ytd_cov)
    fb_sales_tot.ytd_avg =  to_decimal(tot_ytd_avg)
    fb_sales_tot.ytd_rev =  to_decimal(tot_ytd_rev)
    fb_sales_tot.flag = "1Food"
    tot_tday_cov =  to_decimal("0")
    tot_tday_avg =  to_decimal("0")
    tot_tday_rev =  to_decimal("0")
    tot_mtd_cov =  to_decimal("0")
    tot_mtd_avg =  to_decimal("0")
    tot_mtd_rev =  to_decimal("0")
    tot_ytd_cov =  to_decimal("0")
    tot_ytd_avg =  to_decimal("0")
    tot_ytd_rev =  to_decimal("0")

    for fb_sales_beverage in query(fb_sales_beverage_list, sort_by=[("departement",False)]):
        tot_tday_cov =  to_decimal(tot_tday_cov) + to_decimal(fb_sales_beverage.tday_cov)
        tot_tday_avg =  to_decimal(tot_tday_avg) + to_decimal(fb_sales_beverage.tday_avg)
        tot_tday_rev =  to_decimal(tot_tday_rev) + to_decimal(fb_sales_beverage.tday_rev)
        tot_mtd_cov =  to_decimal(tot_mtd_cov) + to_decimal(fb_sales_beverage.mtd_cov)
        tot_mtd_avg =  to_decimal(tot_mtd_avg) + to_decimal(fb_sales_beverage.mtd_avg)
        tot_mtd_rev =  to_decimal(tot_mtd_rev) + to_decimal(fb_sales_beverage.mtd_rev)
        tot_ytd_cov =  to_decimal(tot_ytd_cov) + to_decimal(fb_sales_beverage.ytd_cov)
        tot_ytd_avg =  to_decimal(tot_ytd_avg) + to_decimal(fb_sales_beverage.ytd_avg)
        tot_ytd_rev =  to_decimal(tot_ytd_rev) + to_decimal(fb_sales_beverage.ytd_rev)


    fb_sales_beverage = Fb_sales_beverage()
    fb_sales_beverage_list.append(fb_sales_beverage)

    fb_sales_beverage.ct = 9999
    fb_sales_beverage.departement = 0
    fb_sales_beverage.artnr = 0
    fb_sales_beverage.descr = "TOTAL BEVERAGE"
    fb_sales_beverage.tday_cov =  to_decimal(tot_tday_cov)
    fb_sales_beverage.tday_avg =  to_decimal(tot_tday_avg)
    fb_sales_beverage.tday_rev =  to_decimal(tot_tday_rev)
    fb_sales_beverage.mtd_cov =  to_decimal(tot_mtd_cov)
    fb_sales_beverage.mtd_avg =  to_decimal(tot_mtd_avg)
    fb_sales_beverage.mtd_rev =  to_decimal(tot_mtd_rev)
    fb_sales_beverage.ytd_cov =  to_decimal(tot_ytd_cov)
    fb_sales_beverage.ytd_avg =  to_decimal(tot_ytd_avg)
    fb_sales_beverage.ytd_rev =  to_decimal(tot_ytd_rev)
    fb_sales_beverage.flag = "2Beverage"


    fb_sales_tot = Fb_sales_tot()
    fb_sales_tot_list.append(fb_sales_tot)

    fb_sales_tot.ct = 2
    fb_sales_tot.descr = "TOTAL BEVERAGE"
    fb_sales_tot.tday_cov =  to_decimal(tot_tday_cov)
    fb_sales_tot.tday_avg =  to_decimal(tot_tday_avg)
    fb_sales_tot.tday_rev =  to_decimal(tot_tday_rev)
    fb_sales_tot.mtd_cov =  to_decimal(tot_mtd_cov)
    fb_sales_tot.mtd_avg =  to_decimal(tot_mtd_avg)
    fb_sales_tot.mtd_rev =  to_decimal(tot_mtd_rev)
    fb_sales_tot.ytd_cov =  to_decimal(tot_ytd_cov)
    fb_sales_tot.ytd_avg =  to_decimal(tot_ytd_avg)
    fb_sales_tot.ytd_rev =  to_decimal(tot_ytd_rev)
    fb_sales_tot.flag = "2Beverage"
    tot_tday_cov =  to_decimal("0")
    tot_tday_avg =  to_decimal("0")
    tot_tday_rev =  to_decimal("0")
    tot_mtd_cov =  to_decimal("0")
    tot_mtd_avg =  to_decimal("0")
    tot_mtd_rev =  to_decimal("0")
    tot_ytd_cov =  to_decimal("0")
    tot_ytd_avg =  to_decimal("0")
    tot_ytd_rev =  to_decimal("0")

    for fb_sales_material in query(fb_sales_material_list, sort_by=[("departement",False)]):
        tot_tday_cov =  to_decimal(tot_tday_cov) + to_decimal(fb_sales_material.tday_cov)
        tot_tday_avg =  to_decimal(tot_tday_avg) + to_decimal(fb_sales_material.tday_avg)
        tot_tday_rev =  to_decimal(tot_tday_rev) + to_decimal(fb_sales_material.tday_rev)
        tot_mtd_cov =  to_decimal(tot_mtd_cov) + to_decimal(fb_sales_material.mtd_cov)
        tot_mtd_avg =  to_decimal(tot_mtd_avg) + to_decimal(fb_sales_material.mtd_avg)
        tot_mtd_rev =  to_decimal(tot_mtd_rev) + to_decimal(fb_sales_material.mtd_rev)
        tot_ytd_cov =  to_decimal(tot_ytd_cov) + to_decimal(fb_sales_material.ytd_cov)
        tot_ytd_avg =  to_decimal(tot_ytd_avg) + to_decimal(fb_sales_material.ytd_avg)
        tot_ytd_rev =  to_decimal(tot_ytd_rev) + to_decimal(fb_sales_material.ytd_rev)


    fb_sales_material = Fb_sales_material()
    fb_sales_material_list.append(fb_sales_material)

    fb_sales_material.ct = 9999
    fb_sales_material.departement = 0
    fb_sales_material.artnr = 0
    fb_sales_material.descr = "TOTAL MATERIAL"
    fb_sales_material.tday_cov =  to_decimal(tot_tday_cov)
    fb_sales_material.tday_avg =  to_decimal(tot_tday_avg)
    fb_sales_material.tday_rev =  to_decimal(tot_tday_rev)
    fb_sales_material.mtd_cov =  to_decimal(tot_mtd_cov)
    fb_sales_material.mtd_avg =  to_decimal(tot_mtd_avg)
    fb_sales_material.mtd_rev =  to_decimal(tot_mtd_rev)
    fb_sales_material.ytd_cov =  to_decimal(tot_ytd_cov)
    fb_sales_material.ytd_avg =  to_decimal(tot_ytd_avg)
    fb_sales_material.ytd_rev =  to_decimal(tot_ytd_rev)
    fb_sales_material.flag = "4Material"


    fb_sales_tot = Fb_sales_tot()
    fb_sales_tot_list.append(fb_sales_tot)

    fb_sales_tot.ct = 3
    fb_sales_tot.descr = "TOTAL MATRIAL"
    fb_sales_tot.tday_cov =  to_decimal(tot_tday_cov)
    fb_sales_tot.tday_avg =  to_decimal(tot_tday_avg)
    fb_sales_tot.tday_rev =  to_decimal(tot_tday_rev)
    fb_sales_tot.mtd_cov =  to_decimal(tot_mtd_cov)
    fb_sales_tot.mtd_avg =  to_decimal(tot_mtd_avg)
    fb_sales_tot.mtd_rev =  to_decimal(tot_mtd_rev)
    fb_sales_tot.ytd_cov =  to_decimal(tot_ytd_cov)
    fb_sales_tot.ytd_avg =  to_decimal(tot_ytd_avg)
    fb_sales_tot.ytd_rev =  to_decimal(tot_ytd_rev)
    fb_sales_tot.flag = "4Material"
    tot_tday_cov =  to_decimal("0")
    tot_tday_avg =  to_decimal("0")
    tot_tday_rev =  to_decimal("0")
    tot_mtd_cov =  to_decimal("0")
    tot_mtd_avg =  to_decimal("0")
    tot_mtd_rev =  to_decimal("0")
    tot_ytd_cov =  to_decimal("0")
    tot_ytd_avg =  to_decimal("0")
    tot_ytd_rev =  to_decimal("0")

    for fb_sales_other in query(fb_sales_other_list, sort_by=[("departement",False)]):
        tot_tday_cov =  to_decimal(tot_tday_cov) + to_decimal(fb_sales_other.tday_cov)
        tot_tday_avg =  to_decimal(tot_tday_avg) + to_decimal(fb_sales_other.tday_avg)
        tot_tday_rev =  to_decimal(tot_tday_rev) + to_decimal(fb_sales_other.tday_rev)
        tot_mtd_cov =  to_decimal(tot_mtd_cov) + to_decimal(fb_sales_other.mtd_cov)
        tot_mtd_avg =  to_decimal(tot_mtd_avg) + to_decimal(fb_sales_other.mtd_avg)
        tot_mtd_rev =  to_decimal(tot_mtd_rev) + to_decimal(fb_sales_other.mtd_rev)
        tot_ytd_cov =  to_decimal(tot_ytd_cov) + to_decimal(fb_sales_other.ytd_cov)
        tot_ytd_avg =  to_decimal(tot_ytd_avg) + to_decimal(fb_sales_other.ytd_avg)
        tot_ytd_rev =  to_decimal(tot_ytd_rev) + to_decimal(fb_sales_other.ytd_rev)


    fb_sales_other = Fb_sales_other()
    fb_sales_other_list.append(fb_sales_other)

    fb_sales_other.ct = 9999
    fb_sales_other.departement = 0
    fb_sales_other.artnr = 0
    fb_sales_other.descr = "TOTAL BANQUET"
    fb_sales_other.tday_cov =  to_decimal(tot_tday_cov)
    fb_sales_other.tday_avg =  to_decimal(tot_tday_avg)
    fb_sales_other.tday_rev =  to_decimal(tot_tday_rev)
    fb_sales_other.mtd_cov =  to_decimal(tot_mtd_cov)
    fb_sales_other.mtd_avg =  to_decimal(tot_mtd_avg)
    fb_sales_other.mtd_rev =  to_decimal(tot_mtd_rev)
    fb_sales_other.ytd_cov =  to_decimal(tot_ytd_cov)
    fb_sales_other.ytd_avg =  to_decimal(tot_ytd_avg)
    fb_sales_other.ytd_rev =  to_decimal(tot_ytd_rev)
    fb_sales_other.flag = "3Banquet"


    fb_sales_tot = Fb_sales_tot()
    fb_sales_tot_list.append(fb_sales_tot)

    fb_sales_tot.ct = 4
    fb_sales_tot.descr = "TOTAL OTHER"
    fb_sales_tot.tday_cov =  to_decimal(tot_tday_cov)
    fb_sales_tot.tday_avg =  to_decimal(tot_tday_avg)
    fb_sales_tot.tday_rev =  to_decimal(tot_tday_rev)
    fb_sales_tot.mtd_cov =  to_decimal(tot_mtd_cov)
    fb_sales_tot.mtd_avg =  to_decimal(tot_mtd_avg)
    fb_sales_tot.mtd_rev =  to_decimal(tot_mtd_rev)
    fb_sales_tot.ytd_cov =  to_decimal(tot_ytd_cov)
    fb_sales_tot.ytd_avg =  to_decimal(tot_ytd_avg)
    fb_sales_tot.ytd_rev =  to_decimal(tot_ytd_rev)
    fb_sales_tot.flag = "3Banquet"
    tot_tday_cov =  to_decimal("0")
    tot_tday_avg =  to_decimal("0")
    tot_tday_rev =  to_decimal("0")
    tot_mtd_cov =  to_decimal("0")
    tot_mtd_avg =  to_decimal("0")
    tot_mtd_rev =  to_decimal("0")
    tot_ytd_cov =  to_decimal("0")
    tot_ytd_avg =  to_decimal("0")
    tot_ytd_rev =  to_decimal("0")

    for fb_sales_tot in query(fb_sales_tot_list, sort_by=[("departement",False)]):
        tot_tday_cov =  to_decimal(tot_tday_cov) + to_decimal(fb_sales_tot.tday_cov)
        tot_tday_avg =  to_decimal(tot_tday_avg) + to_decimal(fb_sales_tot.tday_avg)
        tot_tday_rev =  to_decimal(tot_tday_rev) + to_decimal(fb_sales_tot.tday_rev)
        tot_mtd_cov =  to_decimal(tot_mtd_cov) + to_decimal(fb_sales_tot.mtd_cov)
        tot_mtd_avg =  to_decimal(tot_mtd_avg) + to_decimal(fb_sales_tot.mtd_avg)
        tot_mtd_rev =  to_decimal(tot_mtd_rev) + to_decimal(fb_sales_tot.mtd_rev)
        tot_ytd_cov =  to_decimal(tot_ytd_cov) + to_decimal(fb_sales_tot.ytd_cov)
        tot_ytd_avg =  to_decimal(tot_ytd_avg) + to_decimal(fb_sales_tot.ytd_avg)
        tot_ytd_rev =  to_decimal(tot_ytd_rev) + to_decimal(fb_sales_tot.ytd_rev)


    fb_sales_tot = Fb_sales_tot()
    fb_sales_tot_list.append(fb_sales_tot)

    fb_sales_tot.ct = 5
    fb_sales_tot.descr = "TOTAL F&B REVENUE"
    fb_sales_tot.tday_cov =  to_decimal(tot_tday_cov)
    fb_sales_tot.tday_avg =  to_decimal(tot_tday_avg)
    fb_sales_tot.tday_rev =  to_decimal(tot_tday_rev)
    fb_sales_tot.mtd_cov =  to_decimal(tot_mtd_cov)
    fb_sales_tot.mtd_avg =  to_decimal(tot_mtd_avg)
    fb_sales_tot.mtd_rev =  to_decimal(tot_mtd_rev)
    fb_sales_tot.ytd_cov =  to_decimal(tot_ytd_cov)
    fb_sales_tot.ytd_avg =  to_decimal(tot_ytd_avg)
    fb_sales_tot.ytd_rev =  to_decimal(tot_ytd_rev)
    fb_sales_tot.flag = "5Grand-total"
    tot_tday_cov =  to_decimal("0")
    tot_tday_avg =  to_decimal("0")
    tot_tday_rev =  to_decimal("0")
    tot_mtd_cov =  to_decimal("0")
    tot_mtd_avg =  to_decimal("0")
    tot_mtd_rev =  to_decimal("0")
    tot_ytd_cov =  to_decimal("0")
    tot_ytd_avg =  to_decimal("0")
    tot_ytd_rev =  to_decimal("0")

    rev_list = query(rev_list_list, filters=(lambda rev_list: rev_list.descr.lower()  == ("TOTAL GROSS REVENUE").lower()), first=True)

    if rev_list:
        tdy_gl1 =  to_decimal(rev_list.t_day)

    payable_list = query(payable_list_list, filters=(lambda payable_list: payable_list.descr.lower()  == ("TOTAL PAYABLE").lower()), first=True)

    if payable_list:
        tdy_gl1 =  to_decimal(tdy_gl1) + to_decimal(payable_list.t_day)

    payment_list = query(payment_list_list, filters=(lambda payment_list: payment_list.descr.lower()  == ("TOTAL PAYMENT").lower()), first=True)

    if payment_list:
        tdy_gl1 =  to_decimal(tdy_gl1) + to_decimal(payment_list.t_day)

    uebertrag = db_session.query(Uebertrag).filter(
             (Uebertrag.datum == to_date - timedelta(days=1))).first()

    if uebertrag:
        ytd_gl =  to_decimal(uebertrag.betrag)

    gl_list = query(gl_list_list, first=True)

    if not gl_list:
        gl_list = Gl_list()
        gl_list_list.append(gl_list)

        gl_list.descr = "Today Guest Ledger"
        gl_list.tot_rev =  to_decimal(tdy_gl1)


        gl_list = Gl_list()
        gl_list_list.append(gl_list)

        gl_list.descr = "Yesterday Guest Ledger"
        gl_list.tot_rev =  to_decimal(ytd_gl)


        gl_list = Gl_list()
        gl_list_list.append(gl_list)

        gl_list.descr = "TODAY BALANCE"
        gl_list.tot_rev =  to_decimal(tdy_gl1) + to_decimal(ytd_gl)


    fill_tot_room()
    fill_tot_avail()
    fill_inactive()
    fill_rmstat("ooo")
    fill_rmocc()
    fill_stat("vacant")
    fill_segm("HSE")
    fill_segm("COM")
    fill_comproomnew()
    fill_roomsold()
    fill_occ_pay()
    fill_occ_comp_hu()
    fill_tot_rev()
    fill_avg_rmrate_rp()
    fill_avg_rmrate_frg()
    fill_revpar()
    fill_rmstat("dayuse")
    fill_rmstat("No-Show")
    fill_rmstat("arrival-WIG")
    fill_rmstat("NewRes")
    fill_rmstat("CancRes")
    fill_rmstat("Early-CO")
    fill_rmstat("arrival")
    fill_rmstat("pers-arrival")
    fill_rmstat("departure")
    fill_rmstat("pers-depature")
    fill_rmstat("ArrTmrw")
    fill_rmstat("pers-ArrTmrw")
    fill_rmstat("DepTmrw")
    fill_rmstat("pers-DepTmrw")

    return generate_output()