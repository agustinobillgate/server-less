
DEF TEMP-TABLE t-gl-jouhdr LIKE gl-jouhdr.

DEF TEMP-TABLE b2-list
    FIELD jnr       LIKE gl-journal.jnr
    FIELD fibukonto LIKE gl-acct.fibukonto
    FIELD debit     LIKE gl-journal.debit
    FIELD credit    LIKE gl-journal.credit
    FIELD bemerk    AS CHAR
    FIELD userinit  LIKE gl-journal.userinit
    FIELD sysdate   LIKE gl-journal.sysdate
    FIELD zeit      LIKE gl-journal.zeit
    FIELD chginit   LIKE gl-journal.chginit
    FIELD chgdate   LIKE gl-journal.chgdate
    FIELD bezeich   LIKE gl-acct.bezeich.

DEF INPUT  PARAMETER sorttype  AS INT.
DEF OUTPUT PARAMETER from-date AS DATE.
DEF OUTPUT PARAMETER param-983 AS LOGICAL.
DEF OUTPUT PARAMETER TABLE FOR t-gl-jouhdr.
DEF OUTPUT PARAMETER TABLE FOR b2-list.

DEF VAR to-date AS DATE.

FIND FIRST htparam WHERE paramnr = 795 NO-LOCK.
from-date = htparam.fdate.
to-date = from-date. 

RUN display-it0.
FIND FIRST htparam WHERE paramnr = 983 NO-LOCK.
param-983 = htparam.flogical.

PROCEDURE display-it0:
  FOR EACH gl-jouhdr WHERE gl-jouhdr.activeflag = sorttype
      AND gl-jouhdr.batch = NO 
      AND gl-jouhdr.datum EQ to-date NO-LOCK 
      BY gl-jouhdr.datum BY gl-jouhdr.refno BY gl-jouhdr.bezeich:
      CREATE t-gl-jouhdr.
      BUFFER-COPY gl-jouhdr TO t-gl-jouhdr.
      FOR EACH gl-journal WHERE gl-journal.jnr = gl-jouhdr.jnr NO-LOCK
          BY gl-journal.sysdate BY gl-journal.zeit:
          FIND FIRST gl-acct WHERE gl-acct.fibukonto = gl-journal.fibukonto
              NO-LOCK.
          CREATE b2-list.
          BUFFER-COPY gl-journal TO b2-list.
          ASSIGN b2-list.bezeich = gl-acct.bezeich.
      END.
  END.
END. 
