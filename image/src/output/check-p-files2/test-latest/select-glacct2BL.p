
DEF TEMP-TABLE q1-list
    FIELD fibukonto   LIKE gl-acct.fibukonto
    FIELD bezeich     LIKE gl-acct.bezeich
    FIELD fibukonto2  LIKE gl-acct.fibukonto.

DEF OUTPUT PARAMETER TABLE FOR q1-list.

DEFINE buffer gl-acct2 FOR gl-acct. 

FOR EACH queasy WHERE queasy.key = 108
    /*MTAND queasy.char1 GE fibu*/ NO-LOCK,
    FIRST gl-acct WHERE gl-acct.fibukonto = queasy.char1
    AND gl-acct.activeflag NO-LOCK,
    FIRST gl-acct2 WHERE gl-acct2.fibukonto = queasy.char2
    AND gl-acct2.activeflag NO-LOCK BY gl-acct.fibukonto:
    RUN assign-it.
END.

PROCEDURE assign-it:
    CREATE q1-list.
    ASSIGN
    q1-list.fibukonto   = gl-acct.fibukonto
    q1-list.bezeich     = gl-acct.bezeich
    q1-list.fibukonto2  = gl-acct.fibukonto.
END.
