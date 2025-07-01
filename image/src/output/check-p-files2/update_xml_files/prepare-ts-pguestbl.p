
DEF TEMP-TABLE pguest-list
    FIELD ankunft       LIKE res-line.ankunft
    FIELD abreise       LIKE res-line.abreise
    FIELD nation1       LIKE guest.nation1
    FIELD zinr          LIKE res-line.zinr         FORMAT "x(5)"
    FIELD gname         AS CHAR LABEL "Guest Name" FORMAT "x(29)"
    FIELD pin-code      AS CHAR
    FIELD kreditlimit   AS DECIMAL
    FIELD saldo         AS DECIMAL
    FIELD s-recid       AS INTEGER
.

DEFINE OUTPUT PARAMETER TABLE FOR pguest-list.

DEF VARIABLE d-klimit AS DECIMAL NO-UNDO.
RUN htpdec.p (68, OUTPUT d-klimit).

FOR EACH res-line WHERE res-line.active-flag = 1 
  AND res-line.resstatus NE 12 
  AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
  FIRST guest WHERE guest.gastnr = res-line.gastnrmember NO-LOCK,
  FIRST bill WHERE bill.resnr = res-line.resnr
  AND bill.reslinnr = res-line.reslinnr NO-LOCK
  BY res-line.zinr BY res-line.NAME:
  CREATE pguest-list.
  ASSIGN
      pguest-list.zinr          = res-line.zinr
      pguest-list.ankunft       = res-line.ankunft
      pguest-list.abreise       = res-line.abreise
      pguest-list.gname         = res-line.NAME
      pguest-list.nation1       = guest.nation1
      pguest-list.kreditlimit   = guest.kreditlimit
      pguest-list.pin-code      = ";" + res-line.pin-code + ";"
      pguest-list.s-recid       = INTEGER(RECID(res-line))
  .
  IF pguest-list.kreditlimit = 0 THEN pguest-list.kreditlimit = d-klimit.

  FOR EACH queasy WHERE queasy.key = 16 
    AND queasy.number1 = res-line.resnr 
    AND queasy.number2 = res-line.reslinnr NO-LOCK:
    pguest-list.pin-code = pguest-list.pin-code + ";" + queasy.char1 + ";".
  END.

END.
