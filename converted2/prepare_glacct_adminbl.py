#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Gl_acct, Gl_main, Gl_fstype, Gl_department, Htparam, L_lieferant

def prepare_glacct_adminbl():

    prepare_cache ([Htparam])

    from_acct = ""
    gst_flag = False
    b1_list_data = []
    gl_main1_data = []
    gl_fstype1_data = []
    gl_dept1_data = []
    gl_acct = gl_main = gl_fstype = gl_department = htparam = l_lieferant = None

    b1_list = gl_main1 = gl_fstype1 = gl_dept1 = None

    b1_list_data, B1_list = create_model_like(Gl_acct, {"main_bezeich":string, "kurzbez":string, "dept_bezeich":string, "fstype_bezeich":string})
    gl_main1_data, Gl_main1 = create_model_like(Gl_main)
    gl_fstype1_data, Gl_fstype1 = create_model_like(Gl_fstype)
    gl_dept1_data, Gl_dept1 = create_model_like(Gl_department)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal from_acct, gst_flag, b1_list_data, gl_main1_data, gl_fstype1_data, gl_dept1_data, gl_acct, gl_main, gl_fstype, gl_department, htparam, l_lieferant


        nonlocal b1_list, gl_main1, gl_fstype1, gl_dept1
        nonlocal b1_list_data, gl_main1_data, gl_fstype1_data, gl_dept1_data

        return {"from_acct": from_acct, "gst_flag": gst_flag, "b1-list": b1_list_data, "gl-main1": gl_main1_data, "gl-fstype1": gl_fstype1_data, "gl-dept1": gl_dept1_data}


    gl_acct = db_session.query(Gl_acct).filter(
             (to_int(Gl_acct.fibukonto) == 0) & (Gl_acct.bezeich == "") & (Gl_acct.main_nr == 0)).with_for_update().first()

    if gl_acct:
        db_session.delete(gl_acct)

    htparam = get_cache (Htparam, {"paramnr": [(eq, 551)]})

    if htparam.paramgruppe == 38 and htparam.fchar != "":
        from_acct = htparam.fchar

    gl_acct_obj_list = {}
    for gl_acct, gl_main, gl_fstype, gl_department in db_session.query(Gl_acct, Gl_main, Gl_fstype, Gl_department).join(Gl_main,(Gl_main.nr == Gl_acct.main_nr)).join(Gl_fstype,(Gl_fstype.nr == Gl_acct.fs_type)).join(Gl_department,(Gl_department.nr == Gl_acct.deptnr)).filter(
             (Gl_acct.fibukonto >= (from_acct).lower())).order_by(Gl_acct.fibukonto).all():
        if gl_acct_obj_list.get(gl_acct._recid):
            continue
        else:
            gl_acct_obj_list[gl_acct._recid] = True


        b1_list = B1_list()
        b1_list_data.append(b1_list)

        buffer_copy(gl_acct, b1_list)
        b1_list.main_bezeich = gl_main.bezeich
        b1_list.kurzbez = gl_fstype.kurzbez
        b1_list.dept_bezeich = gl_department.bezeich
        b1_list.fstype_bezeich = gl_fstype.bezeich

    for gl_main in db_session.query(Gl_main).order_by(Gl_main._recid).all():
        gl_main1 = Gl_main1()
        gl_main1_data.append(gl_main1)

        buffer_copy(gl_main, gl_main1)

    for gl_fstype in db_session.query(Gl_fstype).order_by(Gl_fstype._recid).all():
        gl_fstype1 = Gl_fstype1()
        gl_fstype1_data.append(gl_fstype1)

        buffer_copy(gl_fstype, gl_fstype1)

    for gl_department in db_session.query(Gl_department).order_by(Gl_department._recid).all():
        gl_dept1 = Gl_dept1()
        gl_dept1_data.append(gl_dept1)

        buffer_copy(gl_department, gl_dept1)

    l_lieferant = get_cache (L_lieferant, {"firma": [(eq, "gst")]})

    if l_lieferant:
        gst_flag = True


    else:
        gst_flag = False

    return generate_output()