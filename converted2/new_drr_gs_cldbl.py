#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Paramtext

rev_seg_list_data, Rev_seg_list = create_model("Rev_seg_list", {"ct":int, "segment_code":int, "descr":string, "departement":int, "t_day":Decimal, "dper":Decimal, "mtd":Decimal, "mtd_per":Decimal, "mtd_budget":Decimal, "variance":Decimal, "ytd":Decimal, "ytd_budget":Decimal, "ytd_per":Decimal, "flag":string, "flag_grup":bool})
rev_list_data, Rev_list = create_model("Rev_list", {"ct":int, "descr":string, "departement":int, "t_day":Decimal, "dper":Decimal, "mtd":Decimal, "mtd_per":Decimal, "mtd_budget":Decimal, "variance":Decimal, "ytd":Decimal, "ytd_budget":Decimal, "ytd_per":Decimal, "flag":string, "flag_grup":bool})
payable_list_data, Payable_list = create_model_like(Rev_list)
stat_list_data, Stat_list = create_model("Stat_list", {"ct":int, "descr":string, "departement":int, "t_day":Decimal, "mtd":Decimal, "mtd_budget":Decimal, "variance":Decimal, "ytd":Decimal, "ytd_budget":Decimal, "flag":string})
payment_list_data, Payment_list = create_model_like(Stat_list)
gl_list_data, Gl_list = create_model("Gl_list", {"descr":string, "tot_rev":Decimal})
fb_sales_food_data, Fb_sales_food = create_model("Fb_sales_food", {"ct":int, "artnr":int, "departement":int, "descr":string, "tday_cov":Decimal, "tday_avg":Decimal, "tday_rev":Decimal, "mtd_cov":Decimal, "mtd_avg":Decimal, "mtd_rev":Decimal, "ytd_cov":Decimal, "ytd_avg":Decimal, "ytd_rev":Decimal, "flag":string})
fb_sales_beverage_data, Fb_sales_beverage = create_model_like(Fb_sales_food)
fb_sales_other_data, Fb_sales_other = create_model_like(Fb_sales_food)
fb_sales_tot_data, Fb_sales_tot = create_model_like(Fb_sales_food)

def new_drr_gs_cldbl(from_date:date, to_date:date, gsheet_link:string, rev_seg_list_data:[Rev_seg_list], rev_list_data:[Rev_list], payable_list_data:[Payable_list], stat_list_data:[Stat_list], payment_list_data:[Payment_list], gl_list_data:[Gl_list], fb_sales_food_data:[Fb_sales_food], fb_sales_beverage_data:[Fb_sales_beverage], fb_sales_other_data:[Fb_sales_other], fb_sales_tot_data:[Fb_sales_tot]):

    prepare_cache ([Paramtext])

    tot_netpay_tdy:Decimal = to_decimal("0.0")
    tot_netpay_mtd:Decimal = to_decimal("0.0")
    tot_netpay_mtdbudget:Decimal = to_decimal("0.0")
    tot_netpay_ytd:Decimal = to_decimal("0.0")
    tot_grosspay_tdy:Decimal = to_decimal("0.0")
    tot_grosspay_mtd:Decimal = to_decimal("0.0")
    tot_grosspay_mtdbudget:Decimal = to_decimal("0.0")
    tot_grosspay_ytd:Decimal = to_decimal("0.0")
    prev_param:string = ""
    ct_row:int = 0
    ct_row2:int = 0
    j:int = 0
    curr_row:int = 0
    curr_col:string = ""
    htl_no:string = ""
    cell_value:string = ""
    out_path:string = ""
    paramtext = None

    rev_seg_list = rev_list = payable_list = tot_list = stat_list = payment_list = gl_list = fb_sales_food = fb_sales_beverage = fb_sales_other = fb_sales_tot = menu_drr = stream_list = None

    tot_list_data, Tot_list = create_model_like(Rev_list)
    menu_drr_data, Menu_drr = create_model("Menu_drr", {"nr":int, "descr":string})
    stream_list_data, Stream_list = create_model("Stream_list", {"crow":int, "ccol":int, "cval":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal tot_netpay_tdy, tot_netpay_mtd, tot_netpay_mtdbudget, tot_netpay_ytd, tot_grosspay_tdy, tot_grosspay_mtd, tot_grosspay_mtdbudget, tot_grosspay_ytd, prev_param, ct_row, ct_row2, j, curr_row, curr_col, htl_no, cell_value, out_path, paramtext
        nonlocal from_date, to_date, gsheet_link


        nonlocal rev_seg_list, rev_list, payable_list, tot_list, stat_list, payment_list, gl_list, fb_sales_food, fb_sales_beverage, fb_sales_other, fb_sales_tot, menu_drr, stream_list
        nonlocal tot_list_data, menu_drr_data, stream_list_data

        return {}

    def decode_string(in_str:string):

        nonlocal tot_netpay_tdy, tot_netpay_mtd, tot_netpay_mtdbudget, tot_netpay_ytd, tot_grosspay_tdy, tot_grosspay_mtd, tot_grosspay_mtdbudget, tot_grosspay_ytd, prev_param, ct_row, ct_row2, curr_row, curr_col, htl_no, cell_value, out_path, paramtext
        nonlocal from_date, to_date, gsheet_link


        nonlocal rev_seg_list, rev_list, payable_list, tot_list, stat_list, payment_list, gl_list, fb_sales_food, fb_sales_beverage, fb_sales_other, fb_sales_tot, menu_drr, stream_list
        nonlocal tot_list_data, menu_drr_data, stream_list_data

        out_str = ""
        s:string = ""
        j:int = 0
        len_:int = 0

        def generate_inner_output():
            return (out_str)

            s = in_str
            j = asc(substring(s, 0, 1)) - 70
            len_ = length(in_str) - 1
            s = substring(in_str, 1, len_)
            for len_ in range(1,length(s)  + 1) :
                out_str = out_str + chr_unicode(asc(substring(s, len_ - 1, 1)) - j)

        return generate_inner_output()


    paramtext = get_cache (Paramtext, {"txtnr": [(eq, 243)]})

    if paramtext and paramtext.ptexte != "":
        htl_no = decode_string(paramtext.ptexte)
    OS_DELETE VALUE ("/usr1/vhp/tmp/outputFO_" + htl_no + ".txt")
    OUTPUT STREAM s1 TO VALUE ("/usr1/vhp/tmp/outputFO_" + htl_no + ".txt") APPEND UNBUFFERED
    ct_row = 8
    stream_list = Stream_list()
    stream_list_data.append(stream_list)

    stream_list.crow = 2
    stream_list.ccol = 9
    stream_list.cval = "DAILY REVENUE REPORT"


    stream_list = Stream_list()
    stream_list_data.append(stream_list)

    stream_list.crow = 5
    stream_list.ccol = 13
    stream_list.cval = "Report Date : " + to_string(from_date) + "-" + to_string(to_date)


    stream_list = Stream_list()
    stream_list_data.append(stream_list)

    stream_list.crow = 6
    stream_list.ccol = 13
    stream_list.cval = "Printed : " + to_string(get_current_date())


    stream_list = Stream_list()
    stream_list_data.append(stream_list)

    stream_list.crow = 8
    stream_list.ccol = 2
    stream_list.cval = "D E s C R I P T I O N"


    stream_list = Stream_list()
    stream_list_data.append(stream_list)

    stream_list.crow = 7
    stream_list.ccol = 6
    stream_list.cval = "R E V E N U E B Y s E G M E N T"


    stream_list = Stream_list()
    stream_list_data.append(stream_list)

    stream_list.crow = 8
    stream_list.ccol = 3
    stream_list.cval = "TODAY"


    stream_list = Stream_list()
    stream_list_data.append(stream_list)

    stream_list.crow = 8
    stream_list.ccol = 4
    stream_list.cval = "%"


    stream_list = Stream_list()
    stream_list_data.append(stream_list)

    stream_list.crow = 8
    stream_list.ccol = 5
    stream_list.cval = "MTD"


    stream_list = Stream_list()
    stream_list_data.append(stream_list)

    stream_list.crow = 8
    stream_list.ccol = 6
    stream_list.cval = "%"


    stream_list = Stream_list()
    stream_list_data.append(stream_list)

    stream_list.crow = 8
    stream_list.ccol = 7
    stream_list.cval = "MTD BUDGET"


    stream_list = Stream_list()
    stream_list_data.append(stream_list)

    stream_list.crow = 8
    stream_list.ccol = 8
    stream_list.cval = "VARIANCE"


    stream_list = Stream_list()
    stream_list_data.append(stream_list)

    stream_list.crow = 8
    stream_list.ccol = 9
    stream_list.cval = "YTD"


    stream_list = Stream_list()
    stream_list_data.append(stream_list)

    stream_list.crow = 8
    stream_list.ccol = 10
    stream_list.cval = "%"

    for rev_seg_list in query(rev_seg_list_data, sort_by=[("flag",False)]):
        ct_row = ct_row + 1
        stream_list = Stream_list()
        stream_list_data.append(stream_list)

        stream_list.crow = ct_row
        stream_list.ccol = 1
        stream_list.cval = ""


        stream_list = Stream_list()
        stream_list_data.append(stream_list)

        stream_list.crow = ct_row
        stream_list.ccol = 2
        stream_list.cval = rev_seg_list.descr


        stream_list = Stream_list()
        stream_list_data.append(stream_list)

        stream_list.crow = ct_row
        stream_list.ccol = 3
        stream_list.cval = to_string(rev_seg_list.t_day, "->>,>>>,>>>,>>9.99")


        stream_list = Stream_list()
        stream_list_data.append(stream_list)

        stream_list.crow = ct_row
        stream_list.ccol = 4
        stream_list.cval = to_string(rev_seg_list.dper, "->>9.99")


        stream_list = Stream_list()
        stream_list_data.append(stream_list)

        stream_list.crow = ct_row
        stream_list.ccol = 5
        stream_list.cval = to_string(rev_seg_list.mtd, "->>,>>>,>>>,>>9.99")


        stream_list = Stream_list()
        stream_list_data.append(stream_list)

        stream_list.crow = ct_row
        stream_list.ccol = 6
        stream_list.cval = to_string(rev_seg_list.mtd_per, "->>9.99")


        stream_list = Stream_list()
        stream_list_data.append(stream_list)

        stream_list.crow = ct_row
        stream_list.ccol = 7
        stream_list.cval = to_string(rev_seg_list.mtd_budget, "->>,>>>,>>>,>>9.99")


        stream_list = Stream_list()
        stream_list_data.append(stream_list)

        stream_list.crow = ct_row
        stream_list.ccol = 8
        stream_list.cval = to_string(rev_seg_list.variance, "->>,>>>,>>>,>>9.99")


        stream_list = Stream_list()
        stream_list_data.append(stream_list)

        stream_list.crow = ct_row
        stream_list.ccol = 9
        stream_list.cval = to_string(rev_seg_list.ytd, "->>,>>>,>>>,>>9.99")


        stream_list = Stream_list()
        stream_list_data.append(stream_list)

        stream_list.crow = ct_row
        stream_list.ccol = 10
        stream_list.cval = to_string(rev_seg_list.ytd_per, "->>9.99")


    ct_row = ct_row + 3


    stream_list = Stream_list()
    stream_list_data.append(stream_list)

    stream_list.crow = ct_row
    stream_list.ccol = 6
    stream_list.cval = "R E V E N U E"


    ct_row = ct_row + 1


    stream_list = Stream_list()
    stream_list_data.append(stream_list)

    stream_list.crow = ct_row
    stream_list.ccol = 2
    stream_list.cval = "D E s C R I P T I O N"


    stream_list = Stream_list()
    stream_list_data.append(stream_list)

    stream_list.crow = ct_row
    stream_list.ccol = 3
    stream_list.cval = "TODAY"


    stream_list = Stream_list()
    stream_list_data.append(stream_list)

    stream_list.crow = ct_row
    stream_list.ccol = 4
    stream_list.cval = "%"


    stream_list = Stream_list()
    stream_list_data.append(stream_list)

    stream_list.crow = ct_row
    stream_list.ccol = 5
    stream_list.cval = "MTD"


    stream_list = Stream_list()
    stream_list_data.append(stream_list)

    stream_list.crow = ct_row
    stream_list.ccol = 6
    stream_list.cval = "%"


    stream_list = Stream_list()
    stream_list_data.append(stream_list)

    stream_list.crow = ct_row
    stream_list.ccol = 7
    stream_list.cval = "MTD BUDGET"


    stream_list = Stream_list()
    stream_list_data.append(stream_list)

    stream_list.crow = ct_row
    stream_list.ccol = 8
    stream_list.cval = "VARIANCE"


    stream_list = Stream_list()
    stream_list_data.append(stream_list)

    stream_list.crow = ct_row
    stream_list.ccol = 9
    stream_list.cval = "YTD"


    stream_list = Stream_list()
    stream_list_data.append(stream_list)

    stream_list.crow = ct_row
    stream_list.ccol = 10
    stream_list.cval = "%"

    for rev_list in query(rev_list_data, sort_by=[("flag",True),("departement",False),("ct",False)]):
        ct_row = ct_row + 1
        stream_list = Stream_list()
        stream_list_data.append(stream_list)

        stream_list.crow = ct_row
        stream_list.ccol = 1
        stream_list.cval = ""


        stream_list = Stream_list()
        stream_list_data.append(stream_list)

        stream_list.crow = ct_row
        stream_list.ccol = 2
        stream_list.cval = rev_list.descr


        stream_list = Stream_list()
        stream_list_data.append(stream_list)

        stream_list.crow = ct_row
        stream_list.ccol = 3
        stream_list.cval = to_string(rev_list.t_day, "->>,>>>,>>>,>>9.99")


        stream_list = Stream_list()
        stream_list_data.append(stream_list)

        stream_list.crow = ct_row
        stream_list.ccol = 4
        stream_list.cval = to_string(rev_list.dper, "->>9.99")


        stream_list = Stream_list()
        stream_list_data.append(stream_list)

        stream_list.crow = ct_row
        stream_list.ccol = 5
        stream_list.cval = to_string(rev_list.mtd, "->>,>>>,>>>,>>9.99")


        stream_list = Stream_list()
        stream_list_data.append(stream_list)

        stream_list.crow = ct_row
        stream_list.ccol = 6
        stream_list.cval = to_string(rev_list.mtd_per, "->>9.99")


        stream_list = Stream_list()
        stream_list_data.append(stream_list)

        stream_list.crow = ct_row
        stream_list.ccol = 7
        stream_list.cval = to_string(rev_list.mtd_budget, "->>,>>>,>>>,>>9.99")


        stream_list = Stream_list()
        stream_list_data.append(stream_list)

        stream_list.crow = ct_row
        stream_list.ccol = 8
        stream_list.cval = to_string(rev_list.variance, "->>,>>>,>>>,>>9.99")


        stream_list = Stream_list()
        stream_list_data.append(stream_list)

        stream_list.crow = ct_row
        stream_list.ccol = 9
        stream_list.cval = to_string(rev_list.ytd, "->>,>>>,>>>,>>9.99")


        stream_list = Stream_list()
        stream_list_data.append(stream_list)

        stream_list.crow = ct_row
        stream_list.ccol = 10
        stream_list.cval = to_string(rev_list.ytd_per, "->>9.99")


    ct_row = ct_row + 3


    stream_list = Stream_list()
    stream_list_data.append(stream_list)

    stream_list.crow = ct_row
    stream_list.ccol = 6
    stream_list.cval = "P A Y A B L E"


    ct_row = ct_row + 1


    stream_list = Stream_list()
    stream_list_data.append(stream_list)

    stream_list.crow = ct_row
    stream_list.ccol = 2
    stream_list.cval = "D E s C R I P T I O N"


    stream_list = Stream_list()
    stream_list_data.append(stream_list)

    stream_list.crow = ct_row
    stream_list.ccol = 3
    stream_list.cval = "TODAY"


    stream_list = Stream_list()
    stream_list_data.append(stream_list)

    stream_list.crow = ct_row
    stream_list.ccol = 4
    stream_list.cval = "%"


    stream_list = Stream_list()
    stream_list_data.append(stream_list)

    stream_list.crow = ct_row
    stream_list.ccol = 5
    stream_list.cval = "MTD"


    stream_list = Stream_list()
    stream_list_data.append(stream_list)

    stream_list.crow = ct_row
    stream_list.ccol = 6
    stream_list.cval = "%"


    stream_list = Stream_list()
    stream_list_data.append(stream_list)

    stream_list.crow = ct_row
    stream_list.ccol = 7
    stream_list.cval = "MTD BUDGET"


    stream_list = Stream_list()
    stream_list_data.append(stream_list)

    stream_list.crow = ct_row
    stream_list.ccol = 8
    stream_list.cval = "VARIANCE"


    stream_list = Stream_list()
    stream_list_data.append(stream_list)

    stream_list.crow = ct_row
    stream_list.ccol = 9
    stream_list.cval = "YTD"


    stream_list = Stream_list()
    stream_list_data.append(stream_list)

    stream_list.crow = ct_row
    stream_list.ccol = 10
    stream_list.cval = "%"

    for payable_list in query(payable_list_data, sort_by=[("flag",False)]):
        ct_row = ct_row + 1
        stream_list = Stream_list()
        stream_list_data.append(stream_list)

        stream_list.crow = ct_row
        stream_list.ccol = 1
        stream_list.cval = ""


        stream_list = Stream_list()
        stream_list_data.append(stream_list)

        stream_list.crow = ct_row
        stream_list.ccol = 2
        stream_list.cval = payable_list.descr


        stream_list = Stream_list()
        stream_list_data.append(stream_list)

        stream_list.crow = ct_row
        stream_list.ccol = 3
        stream_list.cval = to_string(payable_list.t_day, "->>,>>>,>>>,>>9.99")


        stream_list = Stream_list()
        stream_list_data.append(stream_list)

        stream_list.crow = ct_row
        stream_list.ccol = 4
        stream_list.cval = to_string(payable_list.dper, "->>9.99")


        stream_list = Stream_list()
        stream_list_data.append(stream_list)

        stream_list.crow = ct_row
        stream_list.ccol = 5
        stream_list.cval = to_string(payable_list.mtd, "->>,>>>,>>>,>>9.99")


        stream_list = Stream_list()
        stream_list_data.append(stream_list)

        stream_list.crow = ct_row
        stream_list.ccol = 6
        stream_list.cval = to_string(payable_list.mtd_per, "->>9.99")


        stream_list = Stream_list()
        stream_list_data.append(stream_list)

        stream_list.crow = ct_row
        stream_list.ccol = 7
        stream_list.cval = to_string(payable_list.mtd_budget, "->>,>>>,>>>,>>9.99")


        stream_list = Stream_list()
        stream_list_data.append(stream_list)

        stream_list.crow = ct_row
        stream_list.ccol = 8
        stream_list.cval = to_string(payable_list.variance, "->>,>>>,>>>,>>9.99")


        stream_list = Stream_list()
        stream_list_data.append(stream_list)

        stream_list.crow = ct_row
        stream_list.ccol = 9
        stream_list.cval = to_string(payable_list.ytd, "->>,>>>,>>>,>>9.99")


        stream_list = Stream_list()
        stream_list_data.append(stream_list)

        stream_list.crow = ct_row
        stream_list.ccol = 10
        stream_list.cval = to_string(payable_list.ytd_per, "->>9.99")

    rev_list = query(rev_list_data, filters=(lambda rev_list: rev_list.descr.lower()  == ("TOTAL NETT REVENUE").lower()), first=True)

    if rev_list:
        tot_netpay_tdy =  to_decimal(rev_list.t_day)
        tot_netpay_mtd =  to_decimal(rev_list.mtd)
        tot_netpay_mtdbudget =  to_decimal(rev_list.mtd_budget)
        tot_netpay_ytd =  to_decimal(rev_list.ytd)

    rev_list = query(rev_list_data, filters=(lambda rev_list: rev_list.descr.lower()  == ("TOTAL GROSS REVENUE").lower()), first=True)

    if rev_list:
        tot_grosspay_tdy =  to_decimal(rev_list.t_day)
        tot_grosspay_mtd =  to_decimal(rev_list.mtd)
        tot_grosspay_mtdbudget =  to_decimal(rev_list.mtd_budget)
        tot_grosspay_ytd =  to_decimal(rev_list.ytd)

    payable_list = query(payable_list_data, filters=(lambda payable_list: payable_list.descr.lower()  == ("TOTAL PAYABLE").lower()), first=True)

    if payable_list:
        tot_netpay_tdy =  to_decimal(tot_netpay_tdy) + to_decimal(payable_list.t_day)
        tot_netpay_mtd =  to_decimal(tot_netpay_mtd) + to_decimal(payable_list.mtd)
        tot_netpay_mtdbudget =  to_decimal(tot_netpay_mtdbudget) + to_decimal(payable_list.mtd_budget)
        tot_netpay_ytd =  to_decimal(tot_netpay_ytd) + to_decimal(payable_list.ytd)
        tot_grosspay_tdy =  to_decimal(tot_grosspay_tdy) + to_decimal(payable_list.t_day)
        tot_grosspay_mtd =  to_decimal(tot_grosspay_mtd) + to_decimal(payable_list.mtd)
        tot_grosspay_mtdbudget =  to_decimal(tot_grosspay_mtdbudget) + to_decimal(payable_list.mtd_budget)
        tot_grosspay_ytd =  to_decimal(tot_grosspay_ytd) + to_decimal(payable_list.ytd)


    ct_row = ct_row + 2
    stream_list = Stream_list()
    stream_list_data.append(stream_list)

    stream_list.crow = ct_row
    stream_list.ccol = 1
    stream_list.cval = ""


    stream_list = Stream_list()
    stream_list_data.append(stream_list)

    stream_list.crow = ct_row
    stream_list.ccol = 2
    stream_list.cval = "NETT REVENUE + TOTAL PAYABLE"


    stream_list = Stream_list()
    stream_list_data.append(stream_list)

    stream_list.crow = ct_row
    stream_list.ccol = 3
    stream_list.cval = to_string(tot_netpay_tdy, "->>,>>>,>>>,>>9.99")


    stream_list = Stream_list()
    stream_list_data.append(stream_list)

    stream_list.crow = ct_row
    stream_list.ccol = 4
    stream_list.cval = to_string(100, "->>9.99")


    stream_list = Stream_list()
    stream_list_data.append(stream_list)

    stream_list.crow = ct_row
    stream_list.ccol = 5
    stream_list.cval = to_string(tot_netpay_mtd, "->>,>>>,>>>,>>9.99")


    stream_list = Stream_list()
    stream_list_data.append(stream_list)

    stream_list.crow = ct_row
    stream_list.ccol = 6
    stream_list.cval = to_string(100, "->>9.99")


    stream_list = Stream_list()
    stream_list_data.append(stream_list)

    stream_list.crow = ct_row
    stream_list.ccol = 7
    stream_list.cval = to_string(tot_netpay_mtdbudget, "->>,>>>,>>>,>>9.99")


    stream_list = Stream_list()
    stream_list_data.append(stream_list)

    stream_list.crow = ct_row
    stream_list.ccol = 8
    stream_list.cval = to_string(100, "->>,>>>,>>>,>>9.99")


    stream_list = Stream_list()
    stream_list_data.append(stream_list)

    stream_list.crow = ct_row
    stream_list.ccol = 9
    stream_list.cval = to_string(tot_netpay_ytd, "->>,>>>,>>>,>>9.99")


    stream_list = Stream_list()
    stream_list_data.append(stream_list)

    stream_list.crow = ct_row
    stream_list.ccol = 10
    stream_list.cval = to_string(100, "->>9.99")


    ct_row = ct_row + 2
    stream_list = Stream_list()
    stream_list_data.append(stream_list)

    stream_list.crow = ct_row
    stream_list.ccol = 1
    stream_list.cval = ""


    stream_list = Stream_list()
    stream_list_data.append(stream_list)

    stream_list.crow = ct_row
    stream_list.ccol = 2
    stream_list.cval = "TOTAL REVENUE + PAYABLE"


    stream_list = Stream_list()
    stream_list_data.append(stream_list)

    stream_list.crow = ct_row
    stream_list.ccol = 3
    stream_list.cval = to_string(tot_grosspay_tdy, "->>,>>>,>>>,>>9.99")


    stream_list = Stream_list()
    stream_list_data.append(stream_list)

    stream_list.crow = ct_row
    stream_list.ccol = 4
    stream_list.cval = to_string(100, "->>9.99")


    stream_list = Stream_list()
    stream_list_data.append(stream_list)

    stream_list.crow = ct_row
    stream_list.ccol = 5
    stream_list.cval = to_string(tot_grosspay_mtd, "->>,>>>,>>>,>>9.99")


    stream_list = Stream_list()
    stream_list_data.append(stream_list)

    stream_list.crow = ct_row
    stream_list.ccol = 6
    stream_list.cval = to_string(100, "->>9.99")


    stream_list = Stream_list()
    stream_list_data.append(stream_list)

    stream_list.crow = ct_row
    stream_list.ccol = 7
    stream_list.cval = to_string(tot_grosspay_mtdbudget, "->>,>>>,>>>,>>9.99")


    stream_list = Stream_list()
    stream_list_data.append(stream_list)

    stream_list.crow = ct_row
    stream_list.ccol = 8
    stream_list.cval = to_string(100, "->>,>>>,>>>,>>9.99")


    stream_list = Stream_list()
    stream_list_data.append(stream_list)

    stream_list.crow = ct_row
    stream_list.ccol = 9
    stream_list.cval = to_string(tot_grosspay_ytd, "->>,>>>,>>>,>>9.99")


    stream_list = Stream_list()
    stream_list_data.append(stream_list)

    stream_list.crow = ct_row
    stream_list.ccol = 10
    stream_list.cval = to_string(100, "->>9.99")


    ct_row = ct_row + 3
    stream_list = Stream_list()
    stream_list_data.append(stream_list)

    stream_list.crow = ct_row
    stream_list.ccol = 2
    stream_list.cval = "G U E s T L E D G E R"


    stream_list = Stream_list()
    stream_list_data.append(stream_list)

    stream_list.crow = ct_row
    stream_list.ccol = 3
    stream_list.cval = ""

    for gl_list in query(gl_list_data):
        ct_row = ct_row + 1
        stream_list = Stream_list()
        stream_list_data.append(stream_list)

        stream_list.crow = ct_row
        stream_list.ccol = 1
        stream_list.cval = ""


        stream_list = Stream_list()
        stream_list_data.append(stream_list)

        stream_list.crow = ct_row
        stream_list.ccol = 2
        stream_list.cval = gl_list.descr


        stream_list = Stream_list()
        stream_list_data.append(stream_list)

        stream_list.crow = ct_row
        stream_list.ccol = 3
        stream_list.cval = to_string(gl_list.tot_rev, "->>,>>>,>>>,>>9.99")


    stream_list = Stream_list()
    stream_list_data.append(stream_list)

    stream_list.crow = 7
    stream_list.ccol = 15
    stream_list.cval = "s T A T I s T I C"


    stream_list = Stream_list()
    stream_list_data.append(stream_list)

    stream_list.crow = 8
    stream_list.ccol = 12
    stream_list.cval = "D E s C R I P T I O N"


    stream_list = Stream_list()
    stream_list_data.append(stream_list)

    stream_list.crow = 8
    stream_list.ccol = 13
    stream_list.cval = "TODAY"


    stream_list = Stream_list()
    stream_list_data.append(stream_list)

    stream_list.crow = 8
    stream_list.ccol = 14
    stream_list.cval = "MTD"


    stream_list = Stream_list()
    stream_list_data.append(stream_list)

    stream_list.crow = 8
    stream_list.ccol = 15
    stream_list.cval = "MTD BUDGET"


    stream_list = Stream_list()
    stream_list_data.append(stream_list)

    stream_list.crow = 8
    stream_list.ccol = 16
    stream_list.cval = "VARIANCE"


    stream_list = Stream_list()
    stream_list_data.append(stream_list)

    stream_list.crow = 8
    stream_list.ccol = 17
    stream_list.cval = "YTD"


    ct_row2 = 8

    for stat_list in query(stat_list_data, sort_by=[("flag",False)]):
        ct_row2 = ct_row2 + 1
        stream_list = Stream_list()
        stream_list_data.append(stream_list)

        stream_list.crow = ct_row2
        stream_list.ccol = 11
        stream_list.cval = ""


        stream_list = Stream_list()
        stream_list_data.append(stream_list)

        stream_list.crow = ct_row2
        stream_list.ccol = 12
        stream_list.cval = stat_list.descr


        stream_list = Stream_list()
        stream_list_data.append(stream_list)

        stream_list.crow = ct_row2
        stream_list.ccol = 13
        stream_list.cval = to_string(stat_list.t_day, "->>,>>>,>>>,>>9.99")


        stream_list = Stream_list()
        stream_list_data.append(stream_list)

        stream_list.crow = ct_row2
        stream_list.ccol = 14
        stream_list.cval = to_string(stat_list.mtd, "->>,>>>,>>>,>>9.99")


        stream_list = Stream_list()
        stream_list_data.append(stream_list)

        stream_list.crow = ct_row2
        stream_list.ccol = 15
        stream_list.cval = to_string(stat_list.mtd_budget, "->>,>>>,>>>,>>9.99")


        stream_list = Stream_list()
        stream_list_data.append(stream_list)

        stream_list.crow = ct_row2
        stream_list.ccol = 16
        stream_list.cval = to_string(stat_list.variance, "->>,>>>,>>>,>>9.99")


        stream_list = Stream_list()
        stream_list_data.append(stream_list)

        stream_list.crow = ct_row2
        stream_list.ccol = 17
        stream_list.cval = to_string(stat_list.ytd, "->>,>>>,>>>,>>9.99")


    ct_row2 = ct_row2 + 3
    stream_list = Stream_list()
    stream_list_data.append(stream_list)

    stream_list.crow = ct_row2
    stream_list.ccol = 15
    stream_list.cval = "P A Y M E N T"


    ct_row2 = ct_row2 + 1
    stream_list = Stream_list()
    stream_list_data.append(stream_list)

    stream_list.crow = ct_row2
    stream_list.ccol = 12
    stream_list.cval = "D E s C R I P T I O N"


    stream_list = Stream_list()
    stream_list_data.append(stream_list)

    stream_list.crow = ct_row2
    stream_list.ccol = 12
    stream_list.cval = ""


    stream_list = Stream_list()
    stream_list_data.append(stream_list)

    stream_list.crow = ct_row2
    stream_list.ccol = 13
    stream_list.cval = "TODAY"


    stream_list = Stream_list()
    stream_list_data.append(stream_list)

    stream_list.crow = ct_row2
    stream_list.ccol = 14
    stream_list.cval = "MTD"


    stream_list = Stream_list()
    stream_list_data.append(stream_list)

    stream_list.crow = ct_row2
    stream_list.ccol = 15
    stream_list.cval = "MTD BUDGET"


    stream_list = Stream_list()
    stream_list_data.append(stream_list)

    stream_list.crow = ct_row2
    stream_list.ccol = 16
    stream_list.cval = "VARIANCE"


    stream_list = Stream_list()
    stream_list_data.append(stream_list)

    stream_list.crow = ct_row2
    stream_list.ccol = 17
    stream_list.cval = "YTD"

    for payment_list in query(payment_list_data, sort_by=[("flag",False),("ct",False)]):
        ct_row2 = ct_row2 + 1
        stream_list = Stream_list()
        stream_list_data.append(stream_list)

        stream_list.crow = ct_row2
        stream_list.ccol = 11
        stream_list.cval = ""


        stream_list = Stream_list()
        stream_list_data.append(stream_list)

        stream_list.crow = ct_row2
        stream_list.ccol = 12
        stream_list.cval = payment_list.descr


        stream_list = Stream_list()
        stream_list_data.append(stream_list)

        stream_list.crow = ct_row2
        stream_list.ccol = 13
        stream_list.cval = to_string(payment_list.t_day, "->>,>>>,>>>,>>9.99")


        stream_list = Stream_list()
        stream_list_data.append(stream_list)

        stream_list.crow = ct_row2
        stream_list.ccol = 14
        stream_list.cval = to_string(payment_list.mtd, "->>,>>>,>>>,>>9.99")


        stream_list = Stream_list()
        stream_list_data.append(stream_list)

        stream_list.crow = ct_row2
        stream_list.ccol = 15
        stream_list.cval = to_string(payment_list.mtd_budget, "->>,>>>,>>>,>>9.99")


        stream_list = Stream_list()
        stream_list_data.append(stream_list)

        stream_list.crow = ct_row2
        stream_list.ccol = 16
        stream_list.cval = to_string(payment_list.variance, "->>,>>>,>>>,>>9.99")


        stream_list = Stream_list()
        stream_list_data.append(stream_list)

        stream_list.crow = ct_row2
        stream_list.ccol = 17
        stream_list.cval = to_string(payment_list.ytd, "->>,>>>,>>>,>>9.99")


    ct_row2 = ct_row2 + 3
    stream_list = Stream_list()
    stream_list_data.append(stream_list)

    stream_list.crow = ct_row2
    stream_list.ccol = 16
    stream_list.cval = "F&B SALES BY SHIFT"


    ct_row2 = ct_row2 + 1
    stream_list = Stream_list()
    stream_list_data.append(stream_list)

    stream_list.crow = ct_row2
    stream_list.ccol = 12
    stream_list.cval = "FOOD REVENUE"


    stream_list = Stream_list()
    stream_list_data.append(stream_list)

    stream_list.crow = ct_row2
    stream_list.ccol = 13
    stream_list.cval = "Today Cover"


    stream_list = Stream_list()
    stream_list_data.append(stream_list)

    stream_list.crow = ct_row2
    stream_list.ccol = 14
    stream_list.cval = "Today Average"


    stream_list = Stream_list()
    stream_list_data.append(stream_list)

    stream_list.crow = ct_row2
    stream_list.ccol = 15
    stream_list.cval = "Today Revenue"


    stream_list = Stream_list()
    stream_list_data.append(stream_list)

    stream_list.crow = ct_row2
    stream_list.ccol = 16
    stream_list.cval = "MTD Cover"


    stream_list = Stream_list()
    stream_list_data.append(stream_list)

    stream_list.crow = ct_row2
    stream_list.ccol = 17
    stream_list.cval = "MTD Average"


    stream_list = Stream_list()
    stream_list_data.append(stream_list)

    stream_list.crow = ct_row2
    stream_list.ccol = 18
    stream_list.cval = "MTD Revenue"


    stream_list = Stream_list()
    stream_list_data.append(stream_list)

    stream_list.crow = ct_row2
    stream_list.ccol = 19
    stream_list.cval = "YTD Cover"


    stream_list = Stream_list()
    stream_list_data.append(stream_list)

    stream_list.crow = ct_row2
    stream_list.ccol = 20
    stream_list.cval = "YTD Average"


    stream_list = Stream_list()
    stream_list_data.append(stream_list)

    stream_list.crow = ct_row2
    stream_list.ccol = 21
    stream_list.cval = "YTD Revenue"

    for fb_sales_food in query(fb_sales_food_data):
        ct_row2 = ct_row2 + 1
        stream_list = Stream_list()
        stream_list_data.append(stream_list)

        stream_list.crow = ct_row2
        stream_list.ccol = 12
        stream_list.cval = to_string(fb_sales_food.descr)


        stream_list = Stream_list()
        stream_list_data.append(stream_list)

        stream_list.crow = ct_row2
        stream_list.ccol = 13
        stream_list.cval = to_string(fb_sales_food.tday_cov, "->>,>>>,>>>,>>9.99")


        stream_list = Stream_list()
        stream_list_data.append(stream_list)

        stream_list.crow = ct_row2
        stream_list.ccol = 14
        stream_list.cval = to_string(fb_sales_food.tday_avg, "->>,>>>,>>>,>>9.99")


        stream_list = Stream_list()
        stream_list_data.append(stream_list)

        stream_list.crow = ct_row2
        stream_list.ccol = 15
        stream_list.cval = to_string(fb_sales_food.tday_rev, "->>,>>>,>>>,>>9.99")


        stream_list = Stream_list()
        stream_list_data.append(stream_list)

        stream_list.crow = ct_row2
        stream_list.ccol = 16
        stream_list.cval = to_string(fb_sales_food.mtd_cov, "->>,>>>,>>>,>>9.99")


        stream_list = Stream_list()
        stream_list_data.append(stream_list)

        stream_list.crow = ct_row2
        stream_list.ccol = 17
        stream_list.cval = to_string(fb_sales_food.mtd_avg, "->>,>>>,>>>,>>9.99")


        stream_list = Stream_list()
        stream_list_data.append(stream_list)

        stream_list.crow = ct_row2
        stream_list.ccol = 18
        stream_list.cval = to_string(fb_sales_food.mtd_rev, "->>,>>>,>>>,>>9.99")


        stream_list = Stream_list()
        stream_list_data.append(stream_list)

        stream_list.crow = ct_row2
        stream_list.ccol = 19
        stream_list.cval = to_string(fb_sales_food.ytd_cov, "->>,>>>,>>>,>>9.99")


        stream_list = Stream_list()
        stream_list_data.append(stream_list)

        stream_list.crow = ct_row2
        stream_list.ccol = 20
        stream_list.cval = to_string(fb_sales_food.ytd_avg, "->>,>>>,>>>,>>9.99")


        stream_list = Stream_list()
        stream_list_data.append(stream_list)

        stream_list.crow = ct_row2
        stream_list.ccol = 21
        stream_list.cval = to_string(fb_sales_food.ytd_rev, "->>,>>>,>>>,>>9.99")


    ct_row2 = ct_row2 + 3
    stream_list = Stream_list()
    stream_list_data.append(stream_list)

    stream_list.crow = ct_row2
    stream_list.ccol = 12
    stream_list.cval = "BEVERAGE REVENUE"


    stream_list = Stream_list()
    stream_list_data.append(stream_list)

    stream_list.crow = ct_row2
    stream_list.ccol = 13
    stream_list.cval = "Today Cover"


    stream_list = Stream_list()
    stream_list_data.append(stream_list)

    stream_list.crow = ct_row2
    stream_list.ccol = 14
    stream_list.cval = "Today Average"


    stream_list = Stream_list()
    stream_list_data.append(stream_list)

    stream_list.crow = ct_row2
    stream_list.ccol = 15
    stream_list.cval = "Today Revenue"


    stream_list = Stream_list()
    stream_list_data.append(stream_list)

    stream_list.crow = ct_row2
    stream_list.ccol = 16
    stream_list.cval = "MTD Cover"


    stream_list = Stream_list()
    stream_list_data.append(stream_list)

    stream_list.crow = ct_row2
    stream_list.ccol = 17
    stream_list.cval = "MTD Average"


    stream_list = Stream_list()
    stream_list_data.append(stream_list)

    stream_list.crow = ct_row2
    stream_list.ccol = 18
    stream_list.cval = "MTD Revenue"


    stream_list = Stream_list()
    stream_list_data.append(stream_list)

    stream_list.crow = ct_row2
    stream_list.ccol = 19
    stream_list.cval = "YTD Cover"


    stream_list = Stream_list()
    stream_list_data.append(stream_list)

    stream_list.crow = ct_row2
    stream_list.ccol = 20
    stream_list.cval = "YTD Average"


    stream_list = Stream_list()
    stream_list_data.append(stream_list)

    stream_list.crow = ct_row2
    stream_list.ccol = 21
    stream_list.cval = "YTD Revenue"

    for fb_sales_beverage in query(fb_sales_beverage_data):
        ct_row2 = ct_row2 + 1
        stream_list = Stream_list()
        stream_list_data.append(stream_list)

        stream_list.crow = ct_row2
        stream_list.ccol = 12
        stream_list.cval = to_string(fb_sales_beverage.descr)


        stream_list = Stream_list()
        stream_list_data.append(stream_list)

        stream_list.crow = ct_row2
        stream_list.ccol = 13
        stream_list.cval = to_string(fb_sales_beverage.tday_cov, "->>,>>>,>>>,>>9.99")


        stream_list = Stream_list()
        stream_list_data.append(stream_list)

        stream_list.crow = ct_row2
        stream_list.ccol = 14
        stream_list.cval = to_string(fb_sales_beverage.tday_avg, "->>,>>>,>>>,>>9.99")


        stream_list = Stream_list()
        stream_list_data.append(stream_list)

        stream_list.crow = ct_row2
        stream_list.ccol = 15
        stream_list.cval = to_string(fb_sales_beverage.tday_rev, "->>,>>>,>>>,>>9.99")


        stream_list = Stream_list()
        stream_list_data.append(stream_list)

        stream_list.crow = ct_row2
        stream_list.ccol = 16
        stream_list.cval = to_string(fb_sales_beverage.mtd_cov, "->>,>>>,>>>,>>9.99")


        stream_list = Stream_list()
        stream_list_data.append(stream_list)

        stream_list.crow = ct_row2
        stream_list.ccol = 17
        stream_list.cval = to_string(fb_sales_beverage.mtd_avg, "->>,>>>,>>>,>>9.99")


        stream_list = Stream_list()
        stream_list_data.append(stream_list)

        stream_list.crow = ct_row2
        stream_list.ccol = 18
        stream_list.cval = to_string(fb_sales_beverage.mtd_rev, "->>,>>>,>>>,>>9.99")


        stream_list = Stream_list()
        stream_list_data.append(stream_list)

        stream_list.crow = ct_row2
        stream_list.ccol = 19
        stream_list.cval = to_string(fb_sales_beverage.ytd_cov, "->>,>>>,>>>,>>9.99")


        stream_list = Stream_list()
        stream_list_data.append(stream_list)

        stream_list.crow = ct_row2
        stream_list.ccol = 20
        stream_list.cval = to_string(fb_sales_beverage.ytd_avg, "->>,>>>,>>>,>>9.99")


        stream_list = Stream_list()
        stream_list_data.append(stream_list)

        stream_list.crow = ct_row2
        stream_list.ccol = 21
        stream_list.cval = to_string(fb_sales_beverage.ytd_rev, "->>,>>>,>>>,>>9.99")


    ct_row2 = ct_row2 + 3
    stream_list = Stream_list()
    stream_list_data.append(stream_list)

    stream_list.crow = ct_row2
    stream_list.ccol = 12
    stream_list.cval = "OTHER REVENUE"


    stream_list = Stream_list()
    stream_list_data.append(stream_list)

    stream_list.crow = ct_row2
    stream_list.ccol = 13
    stream_list.cval = "Today Cover"


    stream_list = Stream_list()
    stream_list_data.append(stream_list)

    stream_list.crow = ct_row2
    stream_list.ccol = 14
    stream_list.cval = "Today Average"


    stream_list = Stream_list()
    stream_list_data.append(stream_list)

    stream_list.crow = ct_row2
    stream_list.ccol = 15
    stream_list.cval = "Today Revenue"


    stream_list = Stream_list()
    stream_list_data.append(stream_list)

    stream_list.crow = ct_row2
    stream_list.ccol = 16
    stream_list.cval = "MTD Cover"


    stream_list = Stream_list()
    stream_list_data.append(stream_list)

    stream_list.crow = ct_row2
    stream_list.ccol = 17
    stream_list.cval = "MTD Average"


    stream_list = Stream_list()
    stream_list_data.append(stream_list)

    stream_list.crow = ct_row2
    stream_list.ccol = 18
    stream_list.cval = "MTD Revenue"


    stream_list = Stream_list()
    stream_list_data.append(stream_list)

    stream_list.crow = ct_row2
    stream_list.ccol = 19
    stream_list.cval = "YTD Cover"


    stream_list = Stream_list()
    stream_list_data.append(stream_list)

    stream_list.crow = ct_row2
    stream_list.ccol = 20
    stream_list.cval = "YTD Average"


    stream_list = Stream_list()
    stream_list_data.append(stream_list)

    stream_list.crow = ct_row2
    stream_list.ccol = 21
    stream_list.cval = "YTD Revenue"

    for fb_sales_other in query(fb_sales_other_data):
        ct_row2 = ct_row2 + 1
        stream_list = Stream_list()
        stream_list_data.append(stream_list)

        stream_list.crow = ct_row2
        stream_list.ccol = 12
        stream_list.cval = to_string(fb_sales_other.descr)


        stream_list = Stream_list()
        stream_list_data.append(stream_list)

        stream_list.crow = ct_row2
        stream_list.ccol = 13
        stream_list.cval = to_string(fb_sales_other.tday_cov, "->>,>>>,>>>,>>9.99")


        stream_list = Stream_list()
        stream_list_data.append(stream_list)

        stream_list.crow = ct_row2
        stream_list.ccol = 14
        stream_list.cval = to_string(fb_sales_other.tday_avg, "->>,>>>,>>>,>>9.99")


        stream_list = Stream_list()
        stream_list_data.append(stream_list)

        stream_list.crow = ct_row2
        stream_list.ccol = 15
        stream_list.cval = to_string(fb_sales_other.tday_rev, "->>,>>>,>>>,>>9.99")


        stream_list = Stream_list()
        stream_list_data.append(stream_list)

        stream_list.crow = ct_row2
        stream_list.ccol = 16
        stream_list.cval = to_string(fb_sales_other.mtd_cov, "->>,>>>,>>>,>>9.99")


        stream_list = Stream_list()
        stream_list_data.append(stream_list)

        stream_list.crow = ct_row2
        stream_list.ccol = 17
        stream_list.cval = to_string(fb_sales_other.mtd_avg, "->>,>>>,>>>,>>9.99")


        stream_list = Stream_list()
        stream_list_data.append(stream_list)

        stream_list.crow = ct_row2
        stream_list.ccol = 18
        stream_list.cval = to_string(fb_sales_other.mtd_rev, "->>,>>>,>>>,>>9.99")


        stream_list = Stream_list()
        stream_list_data.append(stream_list)

        stream_list.crow = ct_row2
        stream_list.ccol = 19
        stream_list.cval = to_string(fb_sales_other.ytd_cov, "->>,>>>,>>>,>>9.99")


        stream_list = Stream_list()
        stream_list_data.append(stream_list)

        stream_list.crow = ct_row2
        stream_list.ccol = 20
        stream_list.cval = to_string(fb_sales_other.ytd_avg, "->>,>>>,>>>,>>9.99")


        stream_list = Stream_list()
        stream_list_data.append(stream_list)

        stream_list.crow = ct_row2
        stream_list.ccol = 21
        stream_list.cval = to_string(fb_sales_other.ytd_rev, "->>,>>>,>>>,>>9.99")


    ct_row2 = ct_row2 + 2

    for fb_sales_tot in query(fb_sales_tot_data):
        ct_row2 = ct_row2 + 1
        stream_list = Stream_list()
        stream_list_data.append(stream_list)

        stream_list.crow = ct_row2
        stream_list.ccol = 12
        stream_list.cval = to_string(fb_sales_tot.descr)


        stream_list = Stream_list()
        stream_list_data.append(stream_list)

        stream_list.crow = ct_row2
        stream_list.ccol = 13
        stream_list.cval = to_string(fb_sales_tot.tday_cov, "->>,>>>,>>>,>>9.99")


        stream_list = Stream_list()
        stream_list_data.append(stream_list)

        stream_list.crow = ct_row2
        stream_list.ccol = 14
        stream_list.cval = to_string(fb_sales_tot.tday_avg, "->>,>>>,>>>,>>9.99")


        stream_list = Stream_list()
        stream_list_data.append(stream_list)

        stream_list.crow = ct_row2
        stream_list.ccol = 15
        stream_list.cval = to_string(fb_sales_tot.tday_rev, "->>,>>>,>>>,>>9.99")


        stream_list = Stream_list()
        stream_list_data.append(stream_list)

        stream_list.crow = ct_row2
        stream_list.ccol = 16
        stream_list.cval = to_string(fb_sales_tot.mtd_cov, "->>,>>>,>>>,>>9.99")


        stream_list = Stream_list()
        stream_list_data.append(stream_list)

        stream_list.crow = ct_row2
        stream_list.ccol = 17
        stream_list.cval = to_string(fb_sales_tot.mtd_avg, "->>,>>>,>>>,>>9.99")


        stream_list = Stream_list()
        stream_list_data.append(stream_list)

        stream_list.crow = ct_row2
        stream_list.ccol = 18
        stream_list.cval = to_string(fb_sales_tot.mtd_rev, "->>,>>>,>>>,>>9.99")


        stream_list = Stream_list()
        stream_list_data.append(stream_list)

        stream_list.crow = ct_row2
        stream_list.ccol = 19
        stream_list.cval = to_string(fb_sales_tot.ytd_cov, "->>,>>>,>>>,>>9.99")


        stream_list = Stream_list()
        stream_list_data.append(stream_list)

        stream_list.crow = ct_row2
        stream_list.ccol = 20
        stream_list.cval = to_string(fb_sales_tot.ytd_avg, "->>,>>>,>>>,>>9.99")


        stream_list = Stream_list()
        stream_list_data.append(stream_list)

        stream_list.crow = ct_row2
        stream_list.ccol = 21
        stream_list.cval = to_string(fb_sales_tot.ytd_rev, "->>,>>>,>>>,>>9.99")


    ct_row2 = ct_row2 + 3
    stream_list = Stream_list()
    stream_list_data.append(stream_list)

    stream_list.crow = ct_row2
    stream_list.ccol = 12
    stream_list.cval = "Prepared By"


    stream_list = Stream_list()
    stream_list_data.append(stream_list)

    stream_list.crow = ct_row2
    stream_list.ccol = 14
    stream_list.cval = "Checked By"


    stream_list = Stream_list()
    stream_list_data.append(stream_list)

    stream_list.crow = ct_row2
    stream_list.ccol = 16
    stream_list.cval = "Approved By"


    ct_row2 = ct_row2 + 6
    stream_list = Stream_list()
    stream_list_data.append(stream_list)

    stream_list.crow = ct_row2
    stream_list.ccol = 12
    stream_list.cval = "Night Audit"


    stream_list = Stream_list()
    stream_list_data.append(stream_list)

    stream_list.crow = ct_row2
    stream_list.ccol = 14
    stream_list.cval = "Income Audit"


    stream_list = Stream_list()
    stream_list_data.append(stream_list)

    stream_list.crow = ct_row2
    stream_list.ccol = 16
    stream_list.cval = "Chief Accountant"

    for stream_list in query(stream_list_data, sort_by=[("crow",False),("ccol",False)]):

        if stream_list.cval != "":
            else:
            OUTPUT STREAM s1 CLOSE
        OS_COMMAND SILENT VALUE ("php /usr1/vhp/php-script/write-sheet.php /usr1/vhp/tmp/outputFO_" + htl_no + ".txt " + gsheet_link)

    return generate_output()