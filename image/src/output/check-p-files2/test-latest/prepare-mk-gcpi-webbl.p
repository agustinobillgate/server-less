DEFINE TEMP-TABLE t-gc-PIbline LIKE gc-PIbline
    FIELD rec-id AS INT.
DEFINE TEMP-TABLE pbuff LIKE gc-pi.
DEFINE TEMP-TABLE t-gc-pitype LIKE gc-pitype.
DEFINE TEMP-TABLE s-list
    FIELD reihe   AS INTEGER
    FIELD bezeich AS CHAR FORMAT "x(24)" LABEL "Description"
    FIELD amount  AS DECIMAL FORMAT ">>>,>>>,>>9.99" LABEL "Amount"
.

DEF INPUT  PARAMETER pvILanguage    AS INTEGER          NO-UNDO.
DEF INPUT  PARAMETER pi-number      AS CHAR.
DEF INPUT  PARAMETER user-init      AS CHAR.
DEF OUTPUT PARAMETER pi-acctNo      AS CHAR.
DEF OUTPUT PARAMETER giro-tempAcct  AS CHAR.
DEF OUTPUT PARAMETER pi-mode        AS CHAR.
DEF OUTPUT PARAMETER pi-status      AS CHAR.
DEF OUTPUT PARAMETER pi-type1       AS CHAR.
DEF OUTPUT PARAMETER fl-temp        AS INT INIT 0.
DEF OUTPUT PARAMETER fl-err         AS LOGICAL INIT NO.
DEF OUTPUT PARAMETER p-110          AS DATE.
DEF OUTPUT PARAMETER bemerk         AS CHAR.
DEF OUTPUT PARAMETER rcvName        AS CHAR.
DEF OUTPUT PARAMETER pay-acctNo     AS CHAR.
DEF OUTPUT PARAMETER department     AS CHAR.
DEF OUTPUT PARAMETER pay-amount     LIKE gc-pi.betrag.
DEF OUTPUT PARAMETER TABLE FOR pbuff.
DEF OUTPUT PARAMETER TABLE FOR t-gc-pitype.
DEF OUTPUT PARAMETER TABLE FOR t-gc-PIbline.
DEF OUTPUT PARAMETER TABLE FOR s-list.
DEF OUTPUT PARAMETER bankName AS CHARACTER.

DEFINE VARIABLE i   AS INTEGER  NO-UNDO.

{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "mk-gcPI".

FIND FIRST htparam WHERE htparam.paramnr = 931 NO-LOCK.
FIND FIRST gl-acct WHERE gl-acct.fibukonto = htparam.fchar NO-LOCK NO-ERROR.
IF NOT AVAILABLE gl-acct THEN
DO:
    fl-err = YES.
    RETURN.
END.

ASSIGN pi-acctNo = htparam.fchar.
FIND FIRST htparam WHERE htparam.paramnr = 1018 NO-LOCK.
FIND FIRST gl-acct WHERE gl-acct.fibukonto = htparam.fchar NO-LOCK NO-ERROR.
IF AVAILABLE gl-acct THEN ASSIGN giro-tempAcct = htparam.fchar.


CREATE pbuff.

DO i = 1 TO 10:
  CREATE s-list.
  ASSIGN s-list.reihe = i.
END.

IF pi-number = "" THEN pi-mode = "new".
ELSE
DO:
  FIND FIRST gc-pi WHERE gc-pi.docu-nr = pi-number NO-LOCK NO-ERROR. /* Malik Serverless 710 handle if available adding NO-ERROR */
  IF AVAILABLE gc-pi THEN
  DO:
    BUFFER-COPY gc-pi TO pbuff.

    FIND FIRST gc-giro WHERE gc-giro.gironum = gc-pi.chequeNo NO-LOCK NO-ERROR.
    IF AVAILABLE gc-giro THEN bankName = gc-giro.bankName.

    DO i = 1 TO 10:
      FIND FIRST s-list WHERE s-list.reihe = i.
        ASSIGN 
            s-list.bezeich = pbuff.bez-array[i]
            s-list.amount  = pbuff.amount-array[i]
        .
    END.
    IF gc-pi.pi-status = 0 THEN
    DO:
      ASSIGN
        pi-status = "0 - " + translateExtended ("APPLY",lvCAREA,"") /*FD*/
        pi-mode = "new1"
      .
    END.      
    ELSE IF gc-pi.pi-status = 1 THEN 
    DO:
      ASSIGN
        pi-status = "1 - " + translateExtended ("POSTED",lvCAREA,"")
        pi-mode = "open"
      .
    END.
    ELSE IF gc-pi.pi-status = 2 THEN 
    DO:
      ASSIGN
        pi-status = "2 - " + translateExtended ("CLOSED",lvCAREA,"")
        pi-mode = "closed"
      .
    END.
    ELSE IF gc-pi.pi-status = 9 THEN 
    DO:
      ASSIGN
        pi-status = "9 - " + translateExtended ("CANCELLED",lvCAREA,"")
        pi-mode = "cancelled"
      .
    END.
  END.
  /* Malik Serverless 710 before if available     
  BUFFER-COPY gc-pi TO pbuff.

  FIND FIRST gc-giro WHERE gc-giro.gironum = gc-pi.chequeNo NO-LOCK NO-ERROR.
  IF AVAILABLE gc-giro THEN bankName = gc-giro.bankName.
  DO i = 1 TO 10:
    FIND FIRST s-list WHERE s-list.reihe = i.
      ASSIGN 
          s-list.bezeich = pbuff.bez-array[i]
          s-list.amount  = pbuff.amount-array[i]
      .
  END.
  IF gc-pi.pi-status = 0 THEN
  DO:
    ASSIGN
      pi-status = "0 - " + translateExtended ("APPLY",lvCAREA,"") /*FD*/
      pi-mode = "new1"
    .
  END.      
  ELSE IF gc-pi.pi-status = 1 THEN 
  DO:
    ASSIGN
      pi-status = "1 - " + translateExtended ("POSTED",lvCAREA,"")
      pi-mode = "open"
    .
  END.
  ELSE IF gc-pi.pi-status = 2 THEN 
  DO:
    ASSIGN
      pi-status = "2 - " + translateExtended ("CLOSED",lvCAREA,"")
      pi-mode = "closed"
    .
  END.
  ELSE IF gc-pi.pi-status = 9 THEN 
  DO:
    ASSIGN
      pi-status = "9 - " + translateExtended ("CANCELLED",lvCAREA,"")
      pi-mode = "cancelled"
    .
  END.*/
END.



FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK. 

IF NOT AVAILABLE gc-pi OR (AVAILABLE gc-pi AND gc-pi.pi-type = 0 ) THEN
DO:
    fl-temp = 1.
    FOR EACH gc-pitype NO-LOCK BY gc-pitype.nr:
        CREATE t-gc-pitype.
        BUFFER-COPY gc-pitype TO t-gc-pitype.
    END.
END.
ELSE
DO:
    fl-temp = 2.
    FIND FIRST gc-pitype WHERE gc-pitype.nr = gc-pi.pi-type NO-LOCK.
    pi-type1 = gc-pitype.bezeich.
    FOR EACH gc-pitype WHERE gc-pitype.nr NE gc-pi.pi-type 
        NO-LOCK BY gc-pitype.nr:
        CREATE t-gc-pitype.
        BUFFER-COPY gc-pitype TO t-gc-pitype.
    END.
END.

FIND FIRST htparam WHERE htparam.paramnr = 110 NO-LOCK.
p-110 = htparam.fdate.

IF pi-mode = "new1" THEN RUN enable1A.
ELSE IF pi-mode = "open" THEN RUN enable2.
ELSE IF pi-mode = "closed" THEN RUN enable3.


PROCEDURE enable1A:
  FIND FIRST gc-piacct WHERE gc-piacct.fibukonto = gc-pi.credit-fibu 
      NO-LOCK NO-ERROR.
  IF AVAILABLE gc-piacct THEN pay-acctNo = gc-piacct.fibukonto.

  FIND FIRST bediener WHERE bediener.userinit = gc-pi.rcvID NO-LOCK.
  FIND FIRST queasy WHERE queasy.KEY = 19
      AND queasy.number1 = bediener.user-group NO-LOCK NO-ERROR.
  IF AVAILABLE queasy THEN department = queasy.char3.
  ASSIGN
      bemerk        = pbuff.bemerk
      rcvName       = bediener.username
  .
END.

PROCEDURE enable2:
    FOR EACH gc-PIbline WHERE gc-PIbline.docu-nr = pbuff.docu-nr NO-LOCK:
        CREATE t-gc-PIbline.
        BUFFER-COPY gc-PIbline TO t-gc-PIbline.
        ASSIGN t-gc-PIbline.rec-id = RECID(gc-PIbline).
    END.

    FIND FIRST gc-piacct WHERE gc-piacct.fibukonto = gc-pi.credit-fibu 
        NO-LOCK NO-ERROR.
    IF AVAILABLE gc-piacct THEN pay-acctNo = gc-piacct.fibukonto.
    FIND FIRST bediener WHERE bediener.userinit = gc-pi.rcvID NO-LOCK.
    FIND FIRST queasy WHERE queasy.KEY = 19
        AND queasy.number1 = bediener.user-group NO-LOCK NO-ERROR.
    IF AVAILABLE queasy THEN department = queasy.char3.
    ASSIGN
        bemerk        = pbuff.bemerk
        rcvName       = bediener.username
        pay-amount    = pbuff.betrag
    .
END.

PROCEDURE enable3:
    FOR EACH gc-PIbline WHERE gc-PIbline.docu-nr = pbuff.docu-nr NO-LOCK:
        CREATE t-gc-PIbline.
        BUFFER-COPY gc-PIbline TO t-gc-PIbline.
        ASSIGN t-gc-PIbline.rec-id = RECID(gc-PIbline).
    END.

    FIND FIRST gc-piacct WHERE gc-piacct.fibukonto = gc-pi.credit-fibu 
        NO-LOCK NO-ERROR.
    IF AVAILABLE gc-piacct THEN pay-acctNo = gc-piacct.fibukonto.
   
    FIND FIRST bediener WHERE bediener.userinit = gc-pi.rcvID NO-LOCK.
    FIND FIRST queasy WHERE queasy.KEY = 19
        AND queasy.number1 = bediener.user-group NO-LOCK NO-ERROR.
    IF AVAILABLE queasy THEN department = queasy.char3.
    ASSIGN
        bemerk        = pbuff.bemerk
        rcvName       = bediener.username
        pay-amount    = pbuff.betrag
    .
END.
