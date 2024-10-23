DEFINE TEMP-TABLE t-dept
    FIELD nr    AS INTEGER FORMAT   ">9"
    FIELD dept  AS CHARACTER FORMAT "x(30)".

DEFINE TEMP-TABLE t-status
    FIELD nr    AS INTEGER FORMAT   ">9"
    FIELD status-str  AS CHARACTER FORMAT "x(30)"
    .

DEFINE TEMP-TABLE t-queasy270 LIKE queasy.

DEFINE INPUT PARAMETER dept AS INT.
DEFINE OUTPUT PARAMETER TABLE FOR t-dept.
DEFINE OUTPUT PARAMETER TABLE FOR t-queasy270.
DEFINE OUTPUT PARAMETER licenseNr     AS CHAR.
DEFINE OUTPUT PARAMETER interval-time AS INT.
DEFINE OUTPUT PARAMETER cancel-exist AS LOGICAL INIT NO.
DEFINE OUTPUT PARAMETER TABLE FOR t-status.

DEFINE VARIABLE pax           AS INT.
DEFINE VARIABLE orderdatetime AS CHAR.
DEFINE VARIABLE gname         AS CHAR.
DEFINE VARIABLE room          AS CHAR.
DEFINE VARIABLE gastnr        AS INT.
DEFINE VARIABLE resnr         AS INT.
DEFINE VARIABLE reslinnr      AS INT.

DEFINE VARIABLE mess-str AS CHAR.
DEFINE VARIABLE i-str AS INT.
DEFINE VARIABLE mess-token AS CHAR.
DEFINE VARIABLE mess-keyword AS CHAR.
DEFINE VARIABLE mess-value AS CHAR.
DEFINE BUFFER qsy230 FOR queasy.
DEFINE BUFFER session-table FOR queasy.
DEFINE BUFFER posted-item FOR queasy.
DEFINE VARIABLE table-no   AS INT.
DEFINE VARIABLE dtime   AS DATETIME.


FIND FIRST queasy WHERE queasy.key = 11 NO-LOCK NO-ERROR. 
cancel-exist = AVAILABLE queasy. 

FOR EACH hoteldpt WHERE hoteldpt.num GT 0 NO-LOCK:
    CREATE t-dept.
    ASSIGN
        t-dept.nr   = hoteldpt.num
        t-dept.dept = CAPS(hoteldpt.depart).
END.

FOR EACH queasy WHERE queasy.KEY EQ 270 
    AND queasy.number1 EQ 1 
    AND queasy.betriebsnr EQ dept NO-LOCK:
    IF queasy.number2 EQ 3 THEN interval-time = INT(queasy.char2).
END.

FOR EACH queasy WHERE queasy.KEY EQ 270 AND queasy.number1 EQ 1 
    NO-LOCK BY queasy.betriebsnr BY queasy.number2:
    CREATE t-queasy270.
    BUFFER-COPY queasy TO t-queasy270.
END.

FIND FIRST paramtext WHERE txtnr = 243 NO-LOCK NO-ERROR. 
IF AVAILABLE paramtext AND paramtext.ptexte NE "" THEN 
RUN decode-string(ptexte, OUTPUT licenseNr).

CREATE t-status.
ASSIGN 
    t-status.nr = 1
    t-status.status-str = "NEW".
CREATE t-status.
ASSIGN 
    t-status.nr = 2
    t-status.status-str = "ON PROCESS".
CREATE t-status.
ASSIGN 
    t-status.nr = 3
    t-status.status-str = "READY".
CREATE t-status.
ASSIGN 
    t-status.nr = 4
    t-status.status-str = "COMPLETED".
CREATE t-status.
ASSIGN 
    t-status.nr = 5
    t-status.status-str = "DECLINED".
CREATE t-status.
ASSIGN 
    t-status.nr = 6
    t-status.status-str = "UNPAID".
CREATE t-status.
ASSIGN 
    t-status.nr = 7
    t-status.status-str = "ON DELIVERY".
CREATE t-status.
ASSIGN 
    t-status.nr = 8
    t-status.status-str = "DELIVERED".


PROCEDURE decode-string: 
DEFINE INPUT PARAMETER in-str   AS CHAR. 
DEFINE OUTPUT PARAMETER out-str AS CHAR INITIAL "". 
DEFINE VARIABLE s   AS CHAR. 
DEFINE VARIABLE j   AS INTEGER. 
DEFINE VARIABLE len AS INTEGER. 
  s = in-str. 
  j = ASC(SUBSTR(s, 1, 1)) - 70. 
  len = LENGTH(in-str) - 1. 
  s = SUBSTR(in-str, 2, len). 
  DO len = 1 TO LENGTH(s): 
    out-str = out-str + chr(asc(SUBSTR(s,len,1)) - j). 
  END. 
END. 
