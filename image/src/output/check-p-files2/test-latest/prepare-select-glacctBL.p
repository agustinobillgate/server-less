
DEF TEMP-TABLE t-queasy LIKE queasy.

DEF TEMP-TABLE glacct-list
    FIELD fibukonto   LIKE gl-acct.fibukonto
    FIELD bezeich     LIKE gl-acct.bezeich
    FIELD acc-type    LIKE gl-acct.acc-type
    FIELD deptnr      LIKE gl-acct.deptnr
    FIELD subdept-nr  AS   INTEGER FORMAT ">>9" INIT 0
    FIELD subdept-bez AS   CHAR FORMAT "x(24)"
    FIELD main-nr     LIKE gl-acct.main-nr
    FIELD activeflag  LIKE gl-acct.activeflag
.
DEF TEMP-TABLE gl-depart-list LIKE gl-department.

DEF INPUT  PARAMETER curr-dept AS INTEGER.
DEF OUTPUT PARAMETER from-fibu AS CHAR.
DEF OUTPUT PARAMETER TABLE FOR glacct-list.
DEF OUTPUT PARAMETER TABLE FOR gl-depart-list.
DEF OUTPUT PARAMETER TABLE FOR t-queasy.

FIND FIRST htparam WHERE paramnr = 551 NO-LOCK. 
IF htparam.paramgr = 38 AND htparam.fchar NE "" THEN 
  from-fibu = htparam.fchar.

IF curr-dept = 0 THEN
  FOR EACH gl-acct 
      WHERE gl-acct.fibukonto GE from-fibu 
      AND gl-acct.activeflag NO-LOCK BY gl-acct.fibukonto:
      CREATE glacct-list.
      ASSIGN
        glacct-list.fibukonto  = gl-acct.fibukonto
        glacct-list.bezeich    = gl-acct.bezeich
        glacct-list.acc-type   = gl-acct.acc-type
        glacct-list.deptnr     = gl-acct.deptnr
        glacct-list.main-nr    = gl-acct.main-nr
        glacct-list.activeflag = gl-acct.activeflag.
  END.
ELSE
  FOR EACH gl-acct WHERE gl-acct.deptnr = curr-dept
      AND gl-acct.fibukonto GE from-fibu
      AND gl-acct.activeflag NO-LOCK BY gl-acct.fibukonto:
      CREATE glacct-list.
      ASSIGN
        glacct-list.fibukonto  = gl-acct.fibukonto
        glacct-list.bezeich    = gl-acct.bezeich
        glacct-list.acc-type   = gl-acct.acc-type
        glacct-list.deptnr     = gl-acct.deptnr
        glacct-list.main-nr    = gl-acct.main-nr
        glacct-list.activeflag = gl-acct.activeflag.
  END.

FOR EACH gl-depart NO-LOCK:
    CREATE gl-depart-list.
    BUFFER-COPY gl-department TO gl-depart-list.
END.


FOR EACH queasy WHERE queasy.KEY = 155 NO-LOCK:
    CREATE t-queasy.
    BUFFER-COPY queasy TO t-queasy.
END.
