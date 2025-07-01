
DEFINE TEMP-TABLE q1-list
    FIELD gnr     LIKE fa-grup.gnr
    FIELD bezeich LIKE fa-grup.bezeich
    FIELD flag    LIKE fa-grup.flag.

DEF OUTPUT PARAMETER TABLE FOR q1-list.

FOR EACH fa-grup WHERE fa-grup.flag GT 0 NO-LOCK BY fa-grup.gnr:
    CREATE q1-list.
    ASSIGN
    q1-list.gnr     = fa-grup.gnr
    q1-list.bezeich = fa-grup.bezeich
    q1-list.flag    = fa-grup.flag.
END.
