#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.new_drr_del_gs_cldbl import new_drr_del_gs_cldbl
from functions.new_drr_gs_cldbl import new_drr_gs_cldbl

rev_seg_list_data, Rev_seg_list = create_model("Rev_seg_list", {"ct":int, "segment_code":int, "descr":string, "departement":int, "t_day":Decimal, "dper":Decimal, "mtd":Decimal, "mtd_per":Decimal, "mtd_budget":Decimal, "variance":Decimal, "ytd":Decimal, "ytd_budget":Decimal, "ytd_per":Decimal, "flag":string, "flag_grup":bool})
rev_list_data, Rev_list = create_model("Rev_list", {"ct":int, "descr":string, "departement":int, "t_day":Decimal, "dper":Decimal, "mtd":Decimal, "mtd_per":Decimal, "mtd_budget":Decimal, "variance":Decimal, "ytd":Decimal, "ytd_budget":Decimal, "ytd_per":Decimal, "flag":string, "flag_grup":bool})
payable_list_data, Payable_list = create_model("Payable_list", {"ct":int, "descr":string, "departement":int, "t_day":Decimal, "dper":Decimal, "mtd":Decimal, "mtd_per":Decimal, "mtd_budget":Decimal, "variance":Decimal, "ytd":Decimal, "ytd_budget":Decimal, "ytd_per":Decimal, "flag":string, "flag_grup":bool})
stat_list_data, Stat_list = create_model("Stat_list", {"ct":int, "descr":string, "departement":int, "t_day":Decimal, "mtd":Decimal, "mtd_budget":Decimal, "variance":Decimal, "ytd":Decimal, "ytd_budget":Decimal, "flag":string})
payment_list_data, Payment_list = create_model("Payment_list", {"ct":int, "descr":string, "departement":int, "t_day":Decimal, "mtd":Decimal, "mtd_budget":Decimal, "variance":Decimal, "ytd":Decimal, "ytd_budget":Decimal, "flag":string})
gl_list_data, Gl_list = create_model("Gl_list", {"descr":string, "tot_rev":Decimal})
fb_sales_food_data, Fb_sales_food = create_model("Fb_sales_food", {"ct":int, "artnr":int, "departement":int, "descr":string, "tday_cov":Decimal, "tday_avg":Decimal, "tday_rev":Decimal, "mtd_cov":Decimal, "mtd_avg":Decimal, "mtd_rev":Decimal, "ytd_cov":Decimal, "ytd_avg":Decimal, "ytd_rev":Decimal, "flag":string})
fb_sales_beverage_data, Fb_sales_beverage = create_model("Fb_sales_beverage", {"ct":int, "artnr":int, "departement":int, "descr":string, "tday_cov":Decimal, "tday_avg":Decimal, "tday_rev":Decimal, "mtd_cov":Decimal, "mtd_avg":Decimal, "mtd_rev":Decimal, "ytd_cov":Decimal, "ytd_avg":Decimal, "ytd_rev":Decimal, "flag":string})
fb_sales_other_data, Fb_sales_other = create_model("Fb_sales_other", {"ct":int, "artnr":int, "departement":int, "descr":string, "tday_cov":Decimal, "tday_avg":Decimal, "tday_rev":Decimal, "mtd_cov":Decimal, "mtd_avg":Decimal, "mtd_rev":Decimal, "ytd_cov":Decimal, "ytd_avg":Decimal, "ytd_rev":Decimal, "flag":string})
fb_sales_tot_data, Fb_sales_tot = create_model("Fb_sales_tot", {"ct":int, "artnr":int, "departement":int, "descr":string, "tday_cov":Decimal, "tday_avg":Decimal, "tday_rev":Decimal, "mtd_cov":Decimal, "mtd_avg":Decimal, "mtd_rev":Decimal, "ytd_cov":Decimal, "ytd_avg":Decimal, "ytd_rev":Decimal, "flag":string})
rev_seg_list1_data, Rev_seg_list1 = create_model_like(Rev_seg_list)
fb_sales_material_data, Fb_sales_material = create_model("Fb_sales_material", {"ct":int, "artnr":int, "departement":int, "descr":string, "tday_cov":Decimal, "tday_avg":Decimal, "tday_rev":Decimal, "mtd_cov":Decimal, "mtd_avg":Decimal, "mtd_rev":Decimal, "ytd_cov":Decimal, "ytd_avg":Decimal, "ytd_rev":Decimal, "flag":string})

def new_drr_create_gsheet_webbl(from_date:date, to_date:date, gsheet_link:string, rev_seg_list_data:[Rev_seg_list], rev_list_data:[Rev_list], payable_list_data:[Payable_list], stat_list_data:[Stat_list], payment_list_data:[Payment_list], gl_list_data:[Gl_list], fb_sales_food_data:[Fb_sales_food], fb_sales_beverage_data:[Fb_sales_beverage], fb_sales_other_data:[Fb_sales_other], fb_sales_tot_data:[Fb_sales_tot], rev_seg_list1_data:[Rev_seg_list1], fb_sales_material_data:[Fb_sales_material]):
    shared = None

    rev_seg_list = rev_seg_list1 = rev_list = payable_list = tot_list = stat_list = payment_list = gl_list = fb_sales_food = fb_sales_beverage = fb_sales_other = fb_sales_tot = fb_sales_material = None

    tot_list_data, Tot_list = create_model("Tot_list", {"ct":int, "descr":string, "departement":int, "t_day":Decimal, "dper":Decimal, "mtd":Decimal, "mtd_per":Decimal, "mtd_budget":Decimal, "variance":Decimal, "ytd":Decimal, "ytd_budget":Decimal, "ytd_per":Decimal, "flag":string, "flag_grup":bool})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal shared
        nonlocal from_date, to_date, gsheet_link, rev_seg_list1_data


        nonlocal rev_seg_list, rev_seg_list1, rev_list, payable_list, tot_list, stat_list, payment_list, gl_list, fb_sales_food, fb_sales_beverage, fb_sales_other, fb_sales_tot, fb_sales_material
        nonlocal tot_list_data

        return {}


    hserver = SESSION:HANDLE
    local_storage.combo_flag = True
    get_output(new_drr_del_gs_cldbl(gsheet_link))
    local_storage.combo_flag = False

    local_storage.combo_flag = True
    get_output(new_drr_gs_cldbl(from_date, to_date, gsheet_link, rev_seg_list_data, rev_list_data, payable_list_data, stat_list_data, payment_list_data, gl_list_data, fb_sales_food_data, fb_sales_beverage_data, fb_sales_other_data, fb_sales_tot_data, rev_seg_list1_data, fb_sales_material_data))
    local_storage.combo_flag = False

    OS_COMMAND SILENT VALUE ("start " + gsheet_link)

    return generate_output()