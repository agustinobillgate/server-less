from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Gl_acct, Gl_main, Gl_fstype, Gl_department, Htparam, L_lieferant

def prepare_glacct_adminbl():
    from_acct = ""
    gst_flag = False
    b1_list_list = []
    gl_main1_list = []
    gl_fstype1_list = []
    gl_dept1_list = []
    gl_acct = gl_main = gl_fstype = gl_department = htparam = l_lieferant = None

    b1_list = gl_main1 = gl_fstype1 = gl_dept1 = None

    b1_list_list, B1_list = create_model_like(Gl_acct, {"main_bezeich":str, "kurzbez":str, "dept_bezeich":str, "fstype_bezeich":str})
    gl_main1_list, Gl_main1 = create_model_like(Gl_main)
    gl_fstype1_list, Gl_fstype1 = create_model_like(Gl_fstype)
    gl_dept1_list, Gl_dept1 = create_model_like(Gl_department)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal from_acct, gst_flag, b1_list_list, gl_main1_list, gl_fstype1_list, gl_dept1_list, gl_acct, gl_main, gl_fstype, gl_department, htparam, l_lieferant


        nonlocal b1_list, gl_main1, gl_fstype1, gl_dept1
        nonlocal b1_list_list, gl_main1_list, gl_fstype1_list, gl_dept1_list

        return {"from_acct": from_acct, "gst_flag": gst_flag, "b1-list": b1_list_list, "gl-main1": gl_main1_list, "gl-fstype1": gl_fstype1_list, "gl-dept1": gl_dept1_list}


    gl_acct = db_session.query(Gl_acct).filter(
             (to_int(Gl_acct.fibukonto) == 0) & (Gl_acct.bezeich == "") & (Gl_acct.main_nr == 0)).first()

    if gl_acct:
        db_session.delete(gl_acct)

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 551)).first()

    if htparam.paramgruppe == 38 and htparam.fchar != "":
        from_acct = htparam.fchar

    gl_acct_obj_list = []
    for gl_acct, gl_main, gl_fstype, gl_department in db_session.query(Gl_acct, Gl_main, Gl_fstype, Gl_department).join(Gl_main,(Gl_main.nr == Gl_acct.main_nr)).join(Gl_fstype,(Gl_fstype.nr == Gl_acct.fs_type)).join(Gl_department,(Gl_department.nr == Gl_acct.deptnr)).filter(
             (func.lower(Gl_acct.fibukonto) >= (from_acct).lower())).order_by(Gl_acct.fibukonto).all():
        if gl_acct._recid in gl_acct_obj_list:
            continue
        else:
            gl_acct_obj_list.append(gl_acct._recid)


        b1_list = B1_list()
        b1_list_list.append(b1_list)

        buffer_copy(gl_acct, b1_list)
        b1_list.main_bezeich = gl_main.bezeich
        b1_list.kurzbez = gl_fstype.kurzbez
        b1_list.dept_bezeich = gl_department.bezeich
        b1_list.fstype_bezeich = gl_fstype.bezeich

    for gl_main in db_session.query(Gl_main).order_by(Gl_main._recid).all():
        gl_main1 = Gl_main1()
        gl_main1_list.append(gl_main1)

        buffer_copy(gl_main, gl_main1)

    for gl_fstype in db_session.query(Gl_fstype).order_by(Gl_fstype._recid).all():
        gl_fstype1 = Gl_fstype1()
        gl_fstype1_list.append(gl_fstype1)

        buffer_copy(gl_fstype, gl_fstype1)

    for gl_department in db_session.query(Gl_department).order_by(Gl_department._recid).all():
        gl_dept1 = Gl_dept1()
        gl_dept1_list.append(gl_dept1)

        buffer_copy(gl_department, gl_dept1)

    l_lieferant = db_session.query(L_lieferant).filter(
             (func.lower(L_lieferant.firma) == ("GST").lower())).first()

    if l_lieferant:
        gst_flag = True


    else:
        gst_flag = False

    return generate_output()