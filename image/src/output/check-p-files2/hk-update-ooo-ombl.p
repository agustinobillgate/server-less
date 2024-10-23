DEFINE TEMP-TABLE t-outorder LIKE outorder.

DEFINE INPUT  PARAMETER case-type    AS INTEGER.
DEFINE INPUT  PARAMETER user-init    AS CHAR.
DEFINE INPUT  PARAMETER rec-id       AS INT.
DEFINE INPUT  PARAMETER from-date    AS DATE.
DEFINE INPUT  PARAMETER to-date      AS DATE.
DEFINE INPUT  PARAMETER service-flag AS LOGICAL.
DEFINE INPUT  PARAMETER reason       AS CHAR.
DEFINE INPUT  PARAMETER dept         AS INTEGER.
DEFINE OUTPUT PARAMETER msg-int      AS INTEGER INIT 0.
DEFINE OUTPUT PARAMETER resno        AS INTEGER INIT 0.
DEFINE OUTPUT PARAMETER resname      AS CHAR INIT "".
DEFINE OUTPUT PARAMETER ankunft      AS DATE INIT ?.
DEFINE OUTPUT PARAMETER abreise      AS DATE INIT ?.

DEFINE VARIABLE ooo-list-ind AS INT.
DEFINE VARIABLE user-nr AS INTEGER.

DEFINE VARIABLE prev-from-date AS DATE.
DEFINE VARIABLE prev-to-date AS DATE.

IF dept EQ ? THEN 
DO:
  dept = 0.
END.
IF service-flag EQ ? THEN
DO:
  service-flag = FALSE.
END.


FIND FIRST outorder WHERE RECID(outorder) EQ rec-id NO-LOCK NO-ERROR.
prev-from-date = outorder.gespstart.
prev-to-date = outorder.gespende. /* malik serverless: outorder.gespend -> outorder.gespende */

CREATE t-outorder.
BUFFER-COPY outorder TO t-outorder.

FIND FIRST bediener WHERE bediener.userinit EQ user-init NO-LOCK NO-ERROR.

user-nr = bediener.nr.

RUN hk-ooo1bl.p (case-type, INPUT TABLE t-outorder, from-date, to-date, service-flag,   
               t-outorder.zinr, user-nr, reason, dept,user-init, OUTPUT msg-int, OUTPUT resno,  
               OUTPUT resname, OUTPUT ankunft, OUTPUT abreise, OUTPUT ooo-list-ind).  


IF msg-int EQ 0 THEN
DO:
  FOR EACH queasy WHERE queasy.KEY EQ 195 AND
    queasy.char1 EQ "ooo;room=" + outorder.zinr + 
    ";from=" + STRING(DAY(prev-from-date),"99") + "/" + 
               STRING(MONTH(prev-from-date),"99") + "/" +
               STRING(YEAR(prev-from-date),"9999") +
    ";to=" +   STRING(DAY(prev-to-date),"99") + "/" + 
               STRING(MONTH(prev-to-date),"99") + "/" +
               STRING(YEAR(prev-to-date),"9999") EXCLUSIVE-LOCK.

    IF AVAILABLE queasy THEN
    DO:
      queasy.char1 = "ooo;room=" + outorder.zinr + 
      ";from=" + STRING(DAY(from-date),"99") + "/" + 
                 STRING(MONTH(from-date),"99") + "/" +
                 STRING(YEAR(from-date),"9999") +
      ";to=" +   STRING(DAY(to-date),"99") + "/" + 
                 STRING(MONTH(to-date),"99") + "/" +
                 STRING(YEAR(to-date),"9999").
      
    END.
  END.
END.


