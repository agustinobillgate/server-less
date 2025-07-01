DEFINE INPUT PARAMETER bill-date AS DATE.
DEFINE OUTPUT PARAMETER fdate AS DATE.
DEFINE OUTPUT PARAMETER tdate AS DATE.

DEFINE TEMP-TABLE t-mathis LIKE mathis.
DEFINE TEMP-TABLE t-fa-grup LIKE fa-grup.

DEFINE OUTPUT PARAMETER TABLE FOR t-fa-grup.
DEFINE OUTPUT PARAMETER TABLE FOR t-mathis.

FIND FIRST htparam WHERE paramnr = 110 NO-LOCK NO-ERROR.
IF AVAILABLE htparam THEN bill-date = htparam.fdate.
    fdate = DATE(MONTH(bill-date),1,YEAR(bill-date)).
    tdate = fdate - 1. 



FOR EACH fa-grup:
    CREATE t-fa-grup.
    BUFFER-COPY fa-grup TO t-fa-grup.
END.

FOR EACH mathis:
    CREATE t-mathis.
    BUFFER-COPY mathis TO t-mathis.
    LEAVE.
END.
