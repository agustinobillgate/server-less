from functions.additional_functions import *
import decimal
from datetime import date
from functions.new_drr_del_gs_cldbl import new_drr_del_gs_cldbl
from functions.new_drr_gs_cldbl import new_drr_gs_cldbl

rev_seg_list_list, Rev_seg_list = create_model("Rev_seg_list", {"ct":int, "segment_code":int, "descr":str, "departement":int, "t_day":decimal, "dper":decimal, "mtd":decimal, "mtd_per":decimal, "mtd_budget":decimal, "variance":decimal, "ytd":decimal, "ytd_budget":decimal, "ytd_per":decimal, "flag":str, "flag_grup":bool})
rev_list_list, Rev_list = create_model("Rev_list", {"ct":int, "descr":str, "departement":int, "t_day":decimal, "dper":decimal, "mtd":decimal, "mtd_per":decimal, "mtd_budget":decimal, "variance":decimal, "ytd":decimal, "ytd_budget":decimal, "ytd_per":decimal, "flag":str, "flag_grup":bool})
payable_list_list, Payable_list = create_model("Payable_list", {"ct":int, "descr":str, "departement":int, "t_day":decimal, "dper":decimal, "mtd":decimal, "mtd_per":decimal, "mtd_budget":decimal, "variance":decimal, "ytd":decimal, "ytd_budget":decimal, "ytd_per":decimal, "flag":str, "flag_grup":bool})
stat_list_list, Stat_list = create_model("Stat_list", {"ct":int, "descr":str, "departement":int, "t_day":decimal, "mtd":decimal, "mtd_budget":decimal, "variance":decimal, "ytd":decimal, "ytd_budget":decimal, "flag":str})
payment_list_list, Payment_list = create_model("Payment_list", {"ct":int, "descr":str, "departement":int, "t_day":decimal, "mtd":decimal, "mtd_budget":decimal, "variance":decimal, "ytd":decimal, "ytd_budget":decimal, "flag":str})
gl_list_list, Gl_list = create_model("Gl_list", {"descr":str, "tot_rev":decimal})
fb_sales_food_list, Fb_sales_food = create_model("Fb_sales_food", {"ct":int, "artnr":int, "departement":int, "descr":str, "tday_cov":decimal, "tday_avg":decimal, "tday_rev":decimal, "mtd_cov":decimal, "mtd_avg":decimal, "mtd_rev":decimal, "ytd_cov":decimal, "ytd_avg":decimal, "ytd_rev":decimal, "flag":str})
fb_sales_beverage_list, Fb_sales_beverage = create_model("Fb_sales_beverage", {"ct":int, "artnr":int, "departement":int, "descr":str, "tday_cov":decimal, "tday_avg":decimal, "tday_rev":decimal, "mtd_cov":decimal, "mtd_avg":decimal, "mtd_rev":decimal, "ytd_cov":decimal, "ytd_avg":decimal, "ytd_rev":decimal, "flag":str})
fb_sales_other_list, Fb_sales_other = create_model("Fb_sales_other", {"ct":int, "artnr":int, "departement":int, "descr":str, "tday_cov":decimal, "tday_avg":decimal, "tday_rev":decimal, "mtd_cov":decimal, "mtd_avg":decimal, "mtd_rev":decimal, "ytd_cov":decimal, "ytd_avg":decimal, "ytd_rev":decimal, "flag":str})
fb_sales_tot_list, Fb_sales_tot = create_model("Fb_sales_tot", {"ct":int, "artnr":int, "departement":int, "descr":str, "tday_cov":decimal, "tday_avg":decimal, "tday_rev":decimal, "mtd_cov":decimal, "mtd_avg":decimal, "mtd_rev":decimal, "ytd_cov":decimal, "ytd_avg":decimal, "ytd_rev":decimal, "flag":str})
rev_seg_list1_list, Rev_seg_list1 = create_model_like(Rev_seg_list)
fb_sales_material_list, Fb_sales_material = create_model("Fb_sales_material", {"ct":int, "artnr":int, "departement":int, "descr":str, "tday_cov":decimal, "tday_avg":decimal, "tday_rev":decimal, "mtd_cov":decimal, "mtd_avg":decimal, "mtd_rev":decimal, "ytd_cov":decimal, "ytd_avg":decimal, "ytd_rev":decimal, "flag":str})

def new_drr_create_gsheet_webbl(from_date:date, to_date:date, gsheet_link:str, rev_seg_list_list:[Rev_seg_list], rev_list_list:[Rev_list], payable_list_list:[Payable_list], stat_list_list:[Stat_list], payment_list_list:[Payment_list], gl_list_list:[Gl_list], fb_sales_food_list:[Fb_sales_food], fb_sales_beverage_list:[Fb_sales_beverage], fb_sales_other_list:[Fb_sales_other], fb_sales_tot_list:[Fb_sales_tot], rev_seg_list1_list:[Rev_seg_list1], fb_sales_material_list:[Fb_sales_material]):
    shared = None

    rev_seg_list = rev_seg_list1 = rev_list = payable_list = tot_list = stat_list = payment_list = gl_list = fb_sales_food = fb_sales_beverage = fb_sales_other = fb_sales_tot = fb_sales_material = None

    tot_list_list, Tot_list = create_model("Tot_list", {"ct":int, "descr":str, "departement":int, "t_day":decimal, "dper":decimal, "mtd":decimal, "mtd_per":decimal, "mtd_budget":decimal, "variance":decimal, "ytd":decimal, "ytd_budget":decimal, "ytd_per":decimal, "flag":str, "flag_grup":bool})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal shared
        nonlocal from_date, to_date, gsheet_link, rev_seg_list1_list


        nonlocal rev_seg_list, rev_seg_list1, rev_list, payable_list, tot_list, stat_list, payment_list, gl_list, fb_sales_food, fb_sales_beverage, fb_sales_other, fb_sales_tot, fb_sales_material
        nonlocal tot_list_list

        return {}


    hserver = SESSION:HANDLE
    local_storage.combo_flag = True
    get_output(new_drr_del_gs_cldbl(gsheet_link))
    local_storage.combo_flag = False

    local_storage.combo_flag = True
    get_output(new_drr_gs_cldbl(from_date, to_date, gsheet_link, rev_seg_list_list, rev_list_list, payable_list_list, stat_list_list, payment_list_list, gl_list_list, fb_sales_food_list, fb_sales_beverage_list, fb_sales_other_list, fb_sales_tot_list, rev_seg_list1_list, fb_sales_material_list))
    local_storage.combo_flag = False

    OS_COMMAND SILENT VALUE ("start " + gsheet_link)

    return generate_output()