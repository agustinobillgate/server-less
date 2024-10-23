DEFINE TEMP-TABLE op-list LIKE l-op 
  FIELD bezeich  AS CHAR FORMAT "x(36)"             COLUMN-LABEL "Description" 
  FIELD username AS CHAR FORMAT "x(16)"             COLUMN-LABEL "Created by" 
  FIELD onhand   AS DECIMAL FORMAT "->,>>>,>>9.99"  COLUMN-LABEL "On-Hand"
  FIELD anzahl0  AS DECIMAL
  FIELD fibu     AS CHAR
  FIELD fibu10   AS CHAR
  FIELD s-recid  AS INTEGER
  FIELD einheit  AS CHAR FORMAT "x(3)".

DEF INPUT  PARAMETER TABLE FOR op-list.
DEF INPUT-OUTPUT PARAMETER s-recid AS INT.
DEF INPUT  PARAMETER user-init      AS CHAR.
DEF INPUT  PARAMETER t-lschein      AS CHAR.
DEF INPUT  PARAMETER release-flag   AS LOGICAL.
DEF INPUT  PARAMETER transfered     AS LOGICAL.
DEF INPUT  PARAMETER show-price     AS LOGICAL.
DEF OUTPUT PARAMETER changed        AS LOGICAL.
DEF OUTPUT PARAMETER approved       AS LOGICAL.
DEF OUTPUT PARAMETER flag           AS INT INIT 0.

FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK. 
IF  NOT transfered AND show-price THEN
DO:
    FIND FIRST op-list.
    DO WHILE AVAILABLE op-list:
      FIND FIRST gl-acct WHERE gl-acct.fibukonto = op-list.fibu
        NO-LOCK NO-ERROR.
      IF NOT AVAILABLE gl-acct THEN
      DO:
        flag = 1.
        RETURN NO-APPLY.
      END.
      /*geral 7E68C2*/
      IF AVAILABLE gl-acct THEN
      DO:
        FIND FIRST parameters WHERE progname = "CostCenter" 
            AND section = "Alloc" AND varname GT "" 
            AND parameters.vstring = gl-acct.fibukonto NO-LOCK NO-ERROR. 
        IF NOT AVAILABLE parameters THEN
        DO:
           flag = 2.
           RETURN NO-APPLY.    
        END.
      END.

      IF s-recid = 0 THEN s-recid = RECID(op-list).
      ELSE
      DO:     
        IF RECID(op-list) = s-recid THEN LEAVE.
        ELSE s-recid = RECID(op-list).
      END.
      FIND NEXT op-list NO-ERROR.
    END.
END.
ELSE IF NOT transfered AND NOT show-price THEN
DO:
    FIND FIRST op-list.
    DO WHILE AVAILABLE op-list:
      FIND FIRST gl-acct WHERE gl-acct.fibukonto = op-list.fibu
        NO-LOCK NO-ERROR.
      IF NOT AVAILABLE gl-acct THEN
      DO:
        flag = 1.
        RETURN NO-APPLY.
      END.
      /*geral 7E68C2*/
      IF AVAILABLE gl-acct THEN
      DO:
        FIND FIRST parameters WHERE progname = "CostCenter" 
            AND section = "Alloc" AND varname GT "" 
            AND parameters.vstring = gl-acct.fibukonto NO-LOCK NO-ERROR. 
        IF NOT AVAILABLE parameters THEN
        DO:
           flag = 2.
           RETURN NO-APPLY.    
        END.
      END.

      IF s-recid = 0 THEN s-recid = RECID(op-list).
      ELSE
      DO:     
        IF RECID(op-list) = s-recid THEN LEAVE.
        ELSE s-recid = RECID(op-list).
      END.
      FIND NEXT op-list NO-ERROR.
    END.
END.

FOR EACH op-list WHERE op-list.anzahl NE op-list.anzahl0
    OR op-list.fibu NE op-list.fibu10 :
    FIND FIRST l-op WHERE RECID(l-op) = op-list.s-recid EXCLUSIVE-LOCK.
    ASSIGN
        l-op.anzahl      = op-list.anzahl
        l-op.stornogrund = op-list.fibu
        l-op.fuellflag   = bediener.nr
        l-op.warenwert   = op-list.warenwert /*IT 150513*/
        changed          = YES
     .
    FIND CURRENT l-op NO-LOCK.
END.

IF release-flag THEN
DO:
    FIND FIRST l-ophdr WHERE l-ophdr.op-typ = "REQ"
      AND l-ophdr.lscheinnr = t-lschein
      AND l-ophdr.docu-nr = t-lschein NO-ERROR.
    IF AVAILABLE l-ophdr THEN
    DO:
      ASSIGN l-ophdr.betriebsnr = bediener.nr.
      FIND CURRENT l-ophdr NO-LOCK.
      approved = YES.
    END.
END.
