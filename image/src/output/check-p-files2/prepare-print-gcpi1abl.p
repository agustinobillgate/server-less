
DEF TEMP-TABLE output-list
    FIELD docu-nr   LIKE gc-pi.docu-nr
    FIELD chequeNo  LIKE gc-pi.chequeNo
    FIELD pay-datum LIKE gc-pi.pay-datum
    FIELD username  LIKE bediener.username
    FIELD dueDate   LIKE gc-pi.dueDate
    FIELD bemerk    LIKE gc-pi.bemerk
    FIELD betrag    LIKE gc-pi.betrag
    FIELD path      LIKE PRINTER.path.

DEF INPUT PARAMETER docu-nr     AS CHAR.
DEF INPUT PARAMETER user-init   AS CHAR.
DEF INPUT PARAMETER printer-nr  AS INT.
DEF OUTPUT PARAMETER TABLE FOR output-list.

DEFINE BUFFER ubuff FOR bediener.

FIND FIRST gc-pi WHERE gc-pi.docu-nr = docu-nr NO-LOCK.
FIND FIRST gc-pitype WHERE gc-pitype.nr = gc-pi.pi-type NO-LOCK NO-ERROR.
FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK.
FIND FIRST ubuff WHERE ubuff.userinit = gc-pi.rcvID NO-LOCK.

FIND FIRST PRINTER WHERE PRINTER.nr = printer-nr NO-LOCK.

CREATE output-list.
ASSIGN
  output-list.docu-nr   = gc-pi.docu-nr
  output-list.chequeNo  = gc-pi.chequeNo
  output-list.pay-datum = gc-pi.pay-datum
  output-list.username  = bediener.username
  output-list.dueDate   = gc-pi.dueDate
  output-list.bemerk    = gc-pi.bemerk
  output-list.betrag    = gc-pi.betrag
  output-list.path      = PRINTER.path.
