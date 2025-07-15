#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Gl_jouhdr, Gl_journal, Gl_htljournal, Counters

t_gl_jouhdr_data, T_gl_jouhdr = create_model_like(Gl_jouhdr)
t_gl_journal_data, T_gl_journal = create_model_like(Gl_journal)

def gl_transf_headoffice2bl(lic_nr:string, t_gl_jouhdr_data:[T_gl_jouhdr], t_gl_journal_data:[T_gl_journal]):

    prepare_cache ([Gl_htljournal, Counters])

    gl_jouhdr = gl_journal = gl_htljournal = counters = None

    t_gl_jouhdr = t_gl_journal = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal gl_jouhdr, gl_journal, gl_htljournal, counters
        nonlocal lic_nr


        nonlocal t_gl_jouhdr, t_gl_journal

        return {}


    for t_gl_jouhdr in query(t_gl_jouhdr_data, sort_by=[("jnr",False)]):

        gl_htljournal = get_cache (Gl_htljournal, {"htl_jnr": [(eq, t_gl_jouhdr.jnr)],"htl_license": [(eq, lic_nr)]})

        if gl_htljournal:

            for gl_jouhdr in db_session.query(Gl_jouhdr).filter(
                         (Gl_jouhdr.jnr == gl_htljournal.jnr)).order_by(Gl_jouhdr._recid).all():
                db_session.delete(gl_jouhdr)

            for gl_journal in db_session.query(Gl_journal).filter(
                         (Gl_journal.jnr == gl_htljournal.jnr)).order_by(Gl_journal._recid).all():
                db_session.delete(gl_journal)
        else:

            counters = get_cache (Counters, {"counter_no": [(eq, 25)]})

            if not counters:
                counters = Counters()
                db_session.add(counters)

                counters.counter_no = 25
                counters.counter_bez = "G/L Transaction Journal"


            counters.counter = counters.counter + 1


            pass
            gl_htljournal = Gl_htljournal()
            db_session.add(gl_htljournal)

            gl_htljournal.htl_jnr = t_gl_jouhdr.jnr
            gl_htljournal.jnr = counters.counter
            gl_htljournal.htl_license = lic_nr
            gl_htljournal.datum = t_gl_jouhdr.datum


            pass
        gl_jouhdr = Gl_jouhdr()
        db_session.add(gl_jouhdr)

        buffer_copy(t_gl_jouhdr, gl_jouhdr,except_fields=["t_gl_jouhdr.jnr"])
        gl_jouhdr.jnr = gl_htljournal.jnr
        gl_jouhdr.jtype = gl_jouhdr.jtype + 10
        gl_jouhdr.activeflag = 0

        for t_gl_journal in query(t_gl_journal_data, filters=(lambda t_gl_journal: t_gl_journal.jnr == t_gl_jouhdr.jnr)):
            gl_journal = Gl_journal()
            db_session.add(gl_journal)

            buffer_copy(t_gl_journal, gl_journal,except_fields=["t_gl_journal.jnr"])
            gl_journal.jnr = gl_htljournal.jnr
            gl_journal.activeflag = 0


            t_gl_journal_data.remove(t_gl_journal)
            pass
            pass
        pass
        pass
        pass
        pass

    return generate_output()