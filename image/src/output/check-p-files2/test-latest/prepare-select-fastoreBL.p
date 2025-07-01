
DEFINE TEMP-TABLE q1-list
    FIELD lager-nr LIKE fa-lager.lager-nr
    FIELD bezeich  LIKE fa-lager.bezeich.

DEF OUTPUT PARAMETER TABLE FOR q1-list.

FOR EACH fa-lager NO-LOCK BY fa-lager.lager-nr:
    CREATE q1-list.
    ASSIGN
    q1-list.lager-nr = fa-lager.lager-nr
    q1-list.bezeich  = fa-lager.bezeich.
END.
