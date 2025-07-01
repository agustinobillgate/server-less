
DEFINE TEMP-TABLE q1-list
    FIELD katnr   LIKE fa-kateg.katnr
    FIELD bezeich LIKE fa-kateg.bezeich
    FIELD rate    LIKE fa-kateg.rate.

DEF OUTPUT PARAMETER TABLE FOR q1-list.

FOR EACH fa-kateg NO-LOCK BY fa-kateg.katnr:
    CREATE q1-list.
    ASSIGN
    q1-list.katnr   = fa-kateg.katnr
    q1-list.bezeich = fa-kateg.bezeich
    q1-list.rate    = fa-kateg.rate.
END.
