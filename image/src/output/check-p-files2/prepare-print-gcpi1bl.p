
DEF TEMP-TABLE output-list
    FIELD docu-nr       LIKE gc-pi.docu-nr
    FIELD bemerk        LIKE gc-pi.bemerk
    FIELD betrag        LIKE gc-pi.betrag
    FIELD amount-array  LIKE gc-pi.amount-array
    FIELD bez-array     LIKE gc-pi.bez-array
    FIELD b-username    LIKE bediener.username
    FIELD u-username    LIKE bediener.username
    FIELD bezeich       LIKE gc-pitype.bezeich
    FIELD avail-gc-pitype AS LOGICAL.

DEF INPUT  PARAMETER docu-nr AS CHAR.
DEF INPUT  PARAMETER user-init AS CHAR.
DEF INPUT  PARAMETER printer-nr AS INT.
DEF OUTPUT PARAMETER outstanding AS DECIMAL.
DEF OUTPUT PARAMETER path AS CHAR.
DEF OUTPUT PARAMETER TABLE FOR output-list.


DEFINE BUFFER ubuff  FOR bediener.
DEFINE BUFFER pibuff FOR gc-pi.

FIND FIRST gc-pi WHERE gc-pi.docu-nr = docu-nr NO-LOCK.
FIND FIRST gc-pitype WHERE gc-pitype.nr = gc-pi.pi-type NO-LOCK NO-ERROR.
FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK.
FIND FIRST ubuff WHERE ubuff.userinit = gc-pi.rcvID NO-LOCK.


FOR EACH pibuff WHERE pibuff.rcvID = gc-pi.rcvID
    AND pibuff.pi-status = 1 NO-LOCK:
    outstanding = outstanding + pibuff.betrag.
END.

DO:
    DEF VAR i AS INT.
    CREATE output-list.
    ASSIGN
        output-list.docu-nr       = gc-pi.docu-nr
        output-list.bemerk        = gc-pi.bemerk
        output-list.betrag        = gc-pi.betrag
        output-list.b-username    = bediener.username
        output-list.u-username    = ubuff.username
        output-list.bezeich       = gc-pitype.bezeich.

    DO i = 1 TO 10: 
      ASSIGN
        output-list.amount-array[i]  = gc-pi.amount-array[i]
        output-list.bez-array[i]     = gc-pi.bez-array[i]
        .
    END. 
END.
IF AVAILABLE gc-pitype THEN output-list.avail-gc-pitype = YES.
ELSE output-list.avail-gc-pitype = NO.


FIND FIRST PRINTER WHERE PRINTER.nr = printer-nr NO-LOCK.
path = PRINTER.path.
