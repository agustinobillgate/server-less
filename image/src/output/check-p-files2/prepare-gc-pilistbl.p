DEFINE TEMP-TABLE b1-list
    FIELD username  LIKE bediener.username
    FIELD userinit  LIKE bediener.userinit
    FIELD datum     LIKE gc-pi.datum
    FIELD bezeich   LIKE gc-pitype.bezeich
    FIELD docu-nr   LIKE gc-pi.docu-nr
    FIELD betrag    LIKE gc-pi.betrag
    FIELD pay-datum LIKE gc-pi.pay-datum
    FIELD postDate  LIKE gc-pi.postDate
    FIELD chequeNo  LIKE gc-pi.chequeNo
    FIELD datum2    LIKE gc-pi.datum2
    FIELD pay-type  LIKE gc-pi.pay-type
    FIELD returnAmt LIKE gc-pi.returnAmt
    FIELD bemerk    LIKE gc-pi.bemerk
    FIELD pi-status LIKE gc-pi.pi-status
    FIELD rcvID     LIKE gc-pi.rcvID.

DEF INPUT  PARAMETER sorttype       AS INTEGER.
DEF INPUT  PARAMETER notClearing    AS LOGICAL.
DEF INPUT  PARAMETER fromName       AS CHAR.
DEF INPUT  PARAMETER toName         AS CHAR.
DEF OUTPUT PARAMETER billDate       AS DATE.
DEF OUTPUT PARAMETER fromDate       AS DATE.
DEF OUTPUT PARAMETER toDate         AS DATE.
DEF OUTPUT PARAMETER TABLE FOR b1-list.

DEFINE BUFFER ubuff FOR bediener.

FIND FIRST htparam WHERE htparam.paramnr = 110 NO-LOCK.
ASSIGN billDate = htparam.fdate
       fromDate = billDate - 30
       toDate   = billDate.

RUN check-rcvName.
RUN disp-it.


PROCEDURE check-rcvName:
DEF BUFFER gbuff FOR gc-pi.
    FIND FIRST gc-pi WHERE gc-pi.rcvName = "" NO-LOCK NO-ERROR.
    DO WHILE AVAILABLE gc-pi:
       FIND FIRST bediener WHERE bediener.userinit = gc-pi.rcvID
           NO-LOCK NO-ERROR.
       IF AVAILABLE bediener THEN
       DO TRANSACTION:
           FIND FIRST gbuff WHERE RECID(gbuff) = RECID(gc-pi) EXCLUSIVE-LOCK.
           ASSIGN gbuff.rcvName = bediener.username.
           FIND CURRENT gbuff NO-LOCK.
           RELEASE gbuff.
       END.
       FIND NEXT gc-pi WHERE gc-pi.rcvName = "" NO-LOCK NO-ERROR.
    END.
END.


PROCEDURE disp-it:
  /*MTASSIGN curr-select = "".*/
  IF sorttype = 1 THEN
  DO:
    /*MTASSIGN curr-select = "pay-datum".*/
    IF notClearing THEN
    FOR EACH gc-pi WHERE gc-pi.pay-datum GE fromDate
        AND gc-pi.pay-datum LE toDate 
        AND gc-pi.pi-status = sorttype AND pay-type = 2 AND gc-pi.chequeNo NE "" 
        AND gc-pi.postDate = ? NO-LOCK,
        FIRST ubuff WHERE ubuff.userinit = gc-pi.rcvID 
        AND ubuff.username GE fromName AND ubuff.username LE toName NO-LOCK,
        FIRST gc-pitype WHERE gc-pitype.nr = gc-pi.pi-type NO-LOCK
        BY gc-pi.pay-datum BY ubuff.username BY gc-pi.docu-nr:
        RUN assign-it.
    END.
    ELSE
    FOR EACH gc-pi WHERE gc-pi.pay-datum GE fromDate
        AND gc-pi.pay-datum LE toDate 
        AND gc-pi.pi-status = sorttype NO-LOCK,
        FIRST ubuff WHERE ubuff.userinit = gc-pi.rcvID 
        AND ubuff.username GE fromName AND ubuff.username LE toName NO-LOCK,
        FIRST gc-pitype WHERE gc-pitype.nr = gc-pi.pi-type NO-LOCK
        BY gc-pi.pay-datum BY ubuff.username BY gc-pi.docu-nr:
        RUN assign-it.
    END.
  END.
  ELSE IF sorttype = 2 THEN
  DO:
    /*MTASSIGN curr-select = "datum2".*/
    IF notClearing THEN
    FOR EACH gc-pi WHERE gc-pi.datum2 GE fromDate
        AND gc-pi.datum2 LE toDate 
        AND gc-pi.pi-status = sorttype AND pay-type = 2 AND gc-pi.chequeNo NE "" 
        AND gc-pi.postDate = ? NO-LOCK,
        FIRST ubuff WHERE ubuff.userinit = gc-pi.rcvID 
        AND ubuff.username GE fromName AND ubuff.username LE toName NO-LOCK,
        FIRST gc-pitype WHERE gc-pitype.nr = gc-pi.pi-type NO-LOCK
        BY gc-pi.datum2 BY ubuff.username BY gc-pi.docu-nr:
        RUN assign-it.
    END.
    ELSE
    FOR EACH gc-pi WHERE gc-pi.datum2 GE fromDate
        AND gc-pi.datum2 LE toDate 
        AND gc-pi.pi-status = sorttype NO-LOCK,
        FIRST ubuff WHERE ubuff.userinit = gc-pi.rcvID 
        AND ubuff.username GE fromName AND ubuff.username LE toName NO-LOCK,
        FIRST gc-pitype WHERE gc-pitype.nr = gc-pi.pi-type NO-LOCK
        BY gc-pi.datum2 BY ubuff.username BY gc-pi.docu-nr:
        RUN assign-it.
    END.
  END.
  ELSE IF sorttype = 9 OR sorttype = 10 THEN
  DO:
    /*MTASSIGN curr-select = "username".*/
    FOR EACH gc-pi WHERE gc-pi.datum GE fromDate
        AND gc-pi.datum LE toDate 
        AND gc-pi.pi-status = 9 NO-LOCK,
        FIRST ubuff WHERE ubuff.userinit = gc-pi.rcvID 
        AND ubuff.username GE fromName AND ubuff.username LE toName NO-LOCK,
        FIRST gc-pitype WHERE gc-pitype.nr = gc-pi.pi-type NO-LOCK
        BY ubuff.username BY gc-pi.pi-status BY gc-pi.docu-nr:
        RUN assign-it.
    END.
  END.
  ELSE 
  DO:
    /*MTASSIGN curr-select = "username".*/
    FOR EACH gc-pi WHERE gc-pi.datum GE fromDate
        AND gc-pi.datum LE toDate 
        AND gc-pi.pi-status = sorttype NO-LOCK,
        FIRST ubuff WHERE ubuff.userinit = gc-pi.rcvID 
        AND ubuff.username GE fromName AND ubuff.username LE toName NO-LOCK,
        FIRST gc-pitype WHERE gc-pitype.nr = gc-pi.pi-type NO-LOCK
        BY ubuff.username BY gc-pi.pi-status BY gc-pi.docu-nr:
        RUN assign-it.
    END.
  END.
END.


PROCEDURE assign-it:
    CREATE b1-list.
    ASSIGN
    b1-list.username  = ubuff.username
    b1-list.userinit  = ubuff.userinit
    b1-list.datum     = gc-pi.datum
    b1-list.bezeich   = gc-pitype.bezeich
    b1-list.docu-nr   = gc-pi.docu-nr
    b1-list.betrag    = gc-pi.betrag
    b1-list.pay-datum = gc-pi.pay-datum
    b1-list.postDate  = gc-pi.postDate
    b1-list.chequeNo  = gc-pi.chequeNo
    b1-list.datum2    = gc-pi.datum2
    b1-list.pay-type  = gc-pi.pay-type
    b1-list.returnAmt = gc-pi.returnAmt
    b1-list.bemerk    = gc-pi.bemerk
    b1-list.pi-status = gc-pi.pi-status
    b1-list.rcvID     = gc-pi.rcvID.
END.
