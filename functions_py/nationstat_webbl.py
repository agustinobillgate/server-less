#using conversion tools version: 1.0.0.117
#-----------------------------------------
# Rd, 29/7/2025
# gitlab: 111/979
# error konversi, # mtd_totrm = 0 mtd_act == 0 ytd_act == 0 ytd_totrm == 0
# Requery, pisahkan Nation dulu
#-----------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, Nation, Nationstat

def nationstat_webbl(printer_nr:int, call_from:int, txt_file:string, from_month:string, hide_zero:bool, mi_arrival:bool, mi_comp:bool, mi_show_d_percent:bool):

    prepare_cache ([Htparam, Nation, Nationstat])

    room_list_data = []
    tot_all:int = 0
    from_date:date = None
    to_date:date = None
    ci_date:date = None
    curr_day:int = 0
    diff_one:int = 0
    ok:bool = False
    i:int = 0
    htparam = nation = nationstat = None

    room_list = total_per_day = None

    room_list_data, Room_list = create_model("Room_list", {"nationnr":int, "name":string, "bezeich":string, "summe":int, "room":[int,31], "proz":Decimal, "d_percent":[Decimal,31]})
    total_per_day_data, Total_per_day = create_model("Total_per_day", {"date_day":int, "total_nat":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal room_list_data, tot_all, from_date, to_date, ci_date, curr_day, diff_one, ok, i, htparam, nation, nationstat
        nonlocal printer_nr, call_from, txt_file, from_month, hide_zero, mi_arrival, mi_comp, mi_show_d_percent


        nonlocal room_list, total_per_day
        nonlocal room_list_data, total_per_day_data

        return {"room-list": room_list_data}

    def create_browse():

        nonlocal room_list_data, tot_all, from_date, to_date, ci_date, curr_day, diff_one, ok, htparam, nation, nationstat
        nonlocal printer_nr, call_from, txt_file, from_month, hide_zero, mi_arrival, mi_comp, mi_show_d_percent


        nonlocal room_list, total_per_day
        nonlocal room_list_data, total_per_day_data

        mm:int = 0
        yy:int = 0
        datum:date = None
        i:int = 0
        incl_comp:bool = True
        bezeich:string = ""
        incl_comp = not mi_comp
        tot_all = 0
        room_list_data.clear()
        mm = to_int(substring(from_month, 0, 2))
        yy = to_int(substring(from_month, 2, 4))
        from_date = date_mdy(mm, 1, yy)
        mm = mm + 1

        if mm == 13:
            mm = 1
            yy = yy + 1
        to_date = date_mdy(mm, 1, yy) - timedelta(days=1)

        if to_date > ci_date:
            to_date = ci_date
        bezeich = None
        i = 0

        for nation in db_session.query(Nation).filter(
                 (Nation.natcode == 0)).order_by(Nation.bezeich).all():
            room_list = Room_list()
            room_list_data.append(room_list)

            room_list.name = entry(0, nation.bezeich , ";")
            room_list.bezeich = nation.kurzbez
            room_list.nationnr = nation.nationnr

        
        # Rd, 29/7/2025
        # requery
        # for nationstat in db_session.query(Nationstat).filter(
        #         ((Nationstat.nationnr.in_(list(set([room_list.nationnr for room_list in room_list_data])))) & 
        #          (Nationstat.datum >= from_date) & (Nationstat.datum <= to_date))).order_by(room_list.bezeich, Nationstat.datum).all():            
        nation_numbers = {r.nationnr for r in room_list_data}
        nation_bezeich = {r.nationnr: r.bezeich for r in room_list_data}

        nationstat_list = (
            db_session.query(Nationstat)
            .filter(
                Nationstat.nationnr.in_(nation_numbers),
                Nationstat.datum >= from_date,
                Nationstat.datum <= to_date
            )
            .order_by(Nationstat.datum)
            .all()
        )

        # sort by bezeich + datum
        nationstat_list.sort(key=lambda x: (nation_bezeich.get(x.nationnr, ""), x.datum))

        for nationstat in nationstat_list:        
            # Rd, 29/7/2025
            # indentation error
            room_list = query(room_list_data, (lambda room_list: (nationstat.nationnr == room_list.nationnr)), first=True)
            i = get_day(nationstat.datum)

            total_per_day = query(total_per_day_data, filters=(lambda total_per_day: total_per_day.date_day == i), first=True)

            if not total_per_day:
                total_per_day = Total_per_day()
                total_per_day_data.append(total_per_day)

                total_per_day.date_day = i

            if incl_comp:
                room_list.room[i - 1] = nationstat.logerwachs + nationstat.logkind1 + nationstat.logkind2 + nationstat.loggratis
                room_list.summe = room_list.summe + nationstat.logerwachs + nationstat.logkind1 + nationstat.logkind2 + nationstat.loggratis
                total_per_day.total_nat = total_per_day.total_nat + nationstat.logerwachs + nationstat.logkind1 + nationstat.logkind2 + nationstat.loggratis
            else:
                room_list.room[i - 1] = nationstat.logerwachs + nationstat.logkind1 + nationstat.logkind2
                room_list.summe = room_list.summe + nationstat.logerwachs + nationstat.logkind1 + nationstat.logkind2
                total_per_day.total_nat = total_per_day.total_nat + nationstat.logerwachs + nationstat.logkind1 + nationstat.logkind2

        for room_list in query(room_list_data, filters=(lambda room_list: room_list.summe != 0)):
            tot_all = tot_all + room_list.summe

            if mi_show_d_percent:

                for total_per_day in query(total_per_day_data):
                    i = total_per_day.date_day
                    room_list.d_percent[i - 1] = (room_list.room[i - 1] / total_per_day.total_nat) * 100

        if tot_all > 0:

            for room_list in query(room_list_data, filters=(lambda room_list: room_list.summe != 0)):
                room_list.proz =  to_decimal(room_list.summe) / to_decimal(tot_all) * to_decimal("100")

    def create_browse1():

        nonlocal room_list_data, tot_all, from_date, to_date, ci_date, curr_day, diff_one, ok, htparam, nation, nationstat
        nonlocal printer_nr, call_from, txt_file, from_month, hide_zero, mi_arrival, mi_comp, mi_show_d_percent


        nonlocal room_list, total_per_day
        nonlocal room_list_data, total_per_day_data

        mm:int = 0
        yy:int = 0
        curr_datum:date = None
        i:int = 0
        incl_comp:bool = True
        bezeich:string = ""
        incl_comp = not mi_comp
        room_list_data.clear()
        tot_all = 0
        mm = to_int(substring(from_month, 0, 2))
        yy = to_int(substring(from_month, 2, 4))
        from_date = date_mdy(mm, 1, yy)
        mm = mm + 1

        if mm == 13:
            mm = 1
            yy = yy + 1
        to_date = date_mdy(mm, 1, yy) - timedelta(days=1)

        if to_date > ci_date:
            to_date = ci_date

        for nation in db_session.query(Nation).filter(
                 (Nation.natcode == 0)).order_by(Nation.bezeich).all():
            room_list = Room_list()
            room_list_data.append(room_list)

            room_list.name = entry(0, nation.bezeich , ";")
            room_list.bezeich = nation.kurzbez
            room_list.nationnr = nation.nationnr

        for nationstat in db_session.query(Nationstat).filter(
                 ((Nationstat.nationnr.in_(list(set([room_list.nationnr for room_list in room_list_data])))) & (Nationstat.datum >= from_date) & (Nationstat.datum <= to_date))).order_by(room_list.bezeich, Nationstat.datum).all():            
            
            # Rd, 29/7/2025
            # indentation error
            room_list = query(room_list_data, (lambda room_list: (nationstat.nationnr == room_list.nationnr)), first=True)
            i = get_day(nationstat.datum)

            total_per_day = query(total_per_day_data, filters=(lambda total_per_day: total_per_day.date_day == i), first=True)

            if not total_per_day:
                total_per_day = Total_per_day()
                total_per_day_data.append(total_per_day)

                total_per_day.date_day = i

            if incl_comp:
                room_list.room[i - 1] = nationstat.logerwachs + nationstat.logkind1 + nationstat.logkind2 + nationstat.loggratis
                room_list.summe = room_list.summe + nationstat.logerwachs + nationstat.logkind1 + nationstat.logkind2 + nationstat.loggratis
                total_per_day.total_nat = total_per_day.total_nat + nationstat.logerwachs + nationstat.logkind1 + nationstat.logkind2 + nationstat.loggratis
            else:
                room_list.room[i - 1] = nationstat.logerwachs + nationstat.logkind1 + nationstat.logkind2
                room_list.summe = room_list.summe + nationstat.logerwachs + nationstat.logkind1 + nationstat.logkind2
                total_per_day.total_nat = total_per_day.total_nat + nationstat.logerwachs + nationstat.logkind1 + nationstat.logkind2

        for room_list in query(room_list_data, filters=(lambda room_list: room_list.summe != 0)):
            tot_all = tot_all + room_list.summe

            if mi_show_d_percent:

                for total_per_day in query(total_per_day_data):
                    i = total_per_day.date_day
                    room_list.d_percent[i - 1] = (room_list.room[i - 1] / total_per_day.total_nat) * 100

        if tot_all > 0:

            for room_list in query(room_list_data, filters=(lambda room_list: room_list.summe != 0)):
                room_list.proz =  to_decimal(room_list.summe) / to_decimal(tot_all) * to_decimal("100")


    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
    ci_date = htparam.fdate

    if not mi_arrival:
        create_browse()
    else:
        create_browse1()

    if hide_zero:

        for room_list in query(room_list_data, filters=(lambda room_list: room_list.summe == 0)):
            room_list_data.remove(room_list)


    return generate_output()

"""
 "error": "Traceback (most recent call last):\n  File \"/usr1/serverless/src/venv/lib/python3.13/site-packages/sqlalchemy/sql/compiler.py\", line 2500, in visit_textual_label_reference\n    col = with_cols[element.element]\n          ~~~~~~~~~^^^^^^^^^^^^^^^^^\nKeyError: 'ZWE'\n\nThe above exception was the direct cause of the following exception:\n\nTraceback (most recent call last):\n  File \"/usr1/serverless/src/main.py\", line 1723, in handle_dynamic_data\n    output_data =  obj(**input_data)\n  File \"/usr1/serverless/src/functions/nationstat_webbl.py\", line 232, in nationstat_webbl\n    create_browse1()\n    ~~~~~~~~~~~~~~^^\n  File \"/usr1/serverless/src/functions/nationstat_webbl.py\", line 187, in create_browse1\n    ((Nationstat.nationnr.in_(list(set([room_list.nationnr for room_list in room_list_data])))) & (Nationstat.datum >= from_date) & (Nationstat.datum <= to_date))).order_by(room_list.bezeich, Nationstat.datum).all():\n                                                                                                                                                                                                                  ~~~^^\n  File \"/usr1/serverless/src/venv/lib/python3.13/site-packages/sqlalchemy/orm/query.py\", line 2704, in all\n    return self._iter().all()  # type: ignore\n           ~~~~~~~~~~^^\n  File \"/usr1/serverless/src/venv/lib/python3.13/site-packages/sqlalchemy/orm/query.py\", line 2858, in _iter\n    result: Union[ScalarResult[_T], Result[_T]] = self.session.execute(\n                                                  ~~~~~~~~~~~~~~~~~~~~^\n        statement,\n        ^^^^^^^^^^\n        params,\n        ^^^^^^^\n        execution_options={\"_sa_orm_load_options\": self.load_options},\n        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n    )\n    ^\n  File \"/usr1/serverless/src/venv/lib/python3.13/site-packages/sqlalchemy/orm/session.py\", line 2365, in execute\n    return self._execute_internal(\n           ~~~~~~~~~~~~~~~~~~~~~~^\n        statement,\n        ^^^^^^^^^^\n    ...<4 lines>...\n        _add_event=_add_event,\n        ^^^^^^^^^^^^^^^^^^^^^^\n    )\n    ^\n  File \"/usr1/serverless/src/venv/lib/python3.13/site-packages/sqlalchemy/orm/session.py\", line 2251, in _execute_internal\n    result: Result[Any] = compile_state_cls.orm_execute_statement(\n                          ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^\n        self,\n        ^^^^^\n    ...<4 lines>...\n        conn,\n        ^^^^^\n    )\n    ^\n  File \"/usr1/serverless/src/venv/lib/python3.13/site-packages/sqlalchemy/orm/context.py\", line 306, in orm_execute_statement\n    result = conn.execute(\n        statement, params or {}, execution_options=execution_options\n    )\n  File \"/usr1/serverless/src/venv/lib/python3.13/site-packages/sqlalchemy/engine/base.py\", line 1416, in execute\n    return meth(\n        self,\n        distilled_parameters,\n        execution_options or NO_OPTIONS,\n    )\n  File \"/usr1/serverless/src/venv/lib/python3.13/site-packages/sqlalchemy/sql/elements.py\", line 523, in _execute_on_connection\n    return connection._execute_clauseelement(\n           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^\n        self, distilled_params, execution_options\n        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n    )\n    ^\n  File \"/usr1/serverless/src/venv/lib/python3.13/site-packages/sqlalchemy/engine/base.py\", line 1630, in _execute_clauseelement\n    compiled_sql, extracted_params, cache_hit = elem._compile_w_cache(\n                                                ~~~~~~~~~~~~~~~~~~~~~^\n        dialect=dialect,\n        ^^^^^^^^^^^^^^^^\n    ...<4 lines>...\n        linting=self.dialect.compiler_linting | compiler.WARN_LINTING,\n        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n    )\n    ^\n  File \"/usr1/serverless/src/venv/lib/python3.13/site-packages/sqlalchemy/sql/elements.py\", line 711, in _compile_w_cache\n    compiled_sql = self._compiler(\n        dialect,\n    ...<4 lines>...\n        **kw,\n    )\n  File \"/usr1/serverless/src/venv/lib/python3.13/site-packages/sqlalchemy/sql/elements.py\", line 320, in _compiler\n    return dialect.statement_compiler(dialect, self, **kw)\n           ~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^\n  File \"/usr1/serverless/src/venv/lib/python3.13/site-packages/sqlalchemy/sql/compiler.py\", line 1429, in __init__\n    Compiled.__init__(self, dialect, statement, **kwargs)\n    ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/usr1/serverless/src/venv/lib/python3.13/site-packages/sqlalchemy/sql/compiler.py\", line 870, in __init__\n    self.string = self.process(self.statement, **compile_kwargs)\n                  ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/usr1/serverless/src/venv/lib/python3.13/site-packages/sqlalchemy/sql/compiler.py\", line 915, in process\n    return obj._compiler_dispatch(self, **kwargs)\n           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^\n  File \"/usr1/serverless/src/venv/lib/python3.13/site-packages/sqlalchemy/sql/visitors.py\", line 141, in _compiler_dispatch\n    return meth(self, **kw)  # type: ignore  # noqa: E501\n  File \"/usr1/serverless/src/venv/lib/python3.13/site-packages/sqlalchemy/sql/compiler.py\", line 4838, in visit_select\n    text = self._compose_select_body(\n        text,\n    ...<6 lines>...\n        kwargs,\n    )\n  File \"/usr1/serverless/src/venv/lib/python3.13/site-packages/sqlalchemy/sql/compiler.py\", line 5021, in _compose_select_body\n    text += self.order_by_clause(select, **kwargs)\n            ~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^\n  File \"/usr1/serverless/src/venv/lib/python3.13/site-packages/sqlalchemy/sql/compiler.py\", line 5130, in order_by_clause\n    order_by = self._generate_delimited_list(\n        select._order_by_clauses, OPERATORS[operators.comma_op], **kw\n    )\n  File \"/usr1/serverless/src/venv/lib/python3.13/site-packages/sqlalchemy/sql/compiler.py\", line 2753, in _generate_delimited_list\n    return separator.join(\n           ~~~~~~~~~~~~~~^\n        s\n        ^\n        for s in (c._compiler_dispatch(self, **kw) for c in elements)\n        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n        if s\n        ^^^^\n    )\n    ^\n  File \"/usr1/serverless/src/venv/lib/python3.13/site-packages/sqlalchemy/sql/compiler.py\", line 2755, in <genexpr>\n    for s in (c._compiler_dispatch(self, **kw) for c in elements)\n             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/usr1/serverless/src/venv/lib/python3.13/site-packages/sqlalchemy/sql/compiler.py\", line 2755, in <genexpr>\n    for s in (c._compiler_dispatch(self, **kw) for c in elements)\n              ~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^\n  File \"/usr1/serverless/src/venv/lib/python3.13/site-packages/sqlalchemy/sql/visitors.py\", line 141, in _compiler_dispatch\n    return meth(self, **kw)  # type: ignore  # noqa: E501\n  File \"/usr1/serverless/src/venv/lib/python3.13/site-packages/sqlalchemy/sql/compiler.py\", line 2502, in visit_textual_label_reference\n    coercions._no_text_coercion(\n    ~~~~~~~~~~~~~~~~~~~~~~~~~~~^\n        element.element,\n        ^^^^^^^^^^^^^^^^\n    ...<5 lines>...\n        err=err,\n        ^^^^^^^^\n    )\n    ^\n  File \"/usr1/serverless/src/venv/lib/python3.13/site-packages/sqlalchemy/sql/coercions.py\", line 584, in _no_text_coercion\n    raise exc_cls(\n    ...<7 lines>...\n    ) from err\nsqlalchemy.exc.CompileError: Can't resolve label reference for ORDER BY / GROUP BY / DISTINCT etc. Textual SQL expression 'ZWE' should be explicitly declared as text('ZWE')\n",
       
       """