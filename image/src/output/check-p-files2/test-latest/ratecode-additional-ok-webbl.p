/*FD Oct 27, 2020 => BL for vhp web based*/
DEF TEMP-TABLE t-queasy  LIKE queasy.

DEF TEMP-TABLE g-list
    FIELD rcode AS CHAR FORMAT "x(45)"
.
DEFINE INPUT PARAMETER TABLE FOR g-list.
DEFINE INPUT PARAMETER TABLE FOR t-queasy.

DEFINE VARIABLE success-flag AS LOGICAL NO-UNDO INITIAL NO.

/* create-pr in ratecode-adminUI.p */
FIND FIRST t-queasy NO-ERROR.

IF t-queasy.char3 MATCHES ("*;*") THEN     
ASSIGN t-queasy.char3 = ENTRY(1, t-queasy.char3, ";") + ";".
ELSE t-queasy.char3 = ";".
FOR EACH g-list:
  t-queasy.char3 = t-queasy.char3 + g-list.rcode + ",".
END.
t-queasy.char3 = t-queasy.char3 + ";".
RUN write-queasybl.p(6, TABLE t-queasy, TABLE t-queasy, OUTPUT success-flag).
