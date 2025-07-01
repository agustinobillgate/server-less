
DEF INPUT PARAMETER inv-type  AS INTEGER    NO-UNDO.
DEF INPUT PARAMETER m-endkum  AS INTEGER    NO-UNDO.
DEF INPUT PARAMETER closeDate AS DATE       NO-UNDO.

DEF VARIABLE firstDate        AS DATE       NO-UNDO.
DEF VARIABLE delete-oph       AS LOGICAL    NO-UNDO INITIAL NO. 
DEF VARIABLE m-datum          AS DATE       NO-UNDO. 
DEF VARIABLE fb-datum         AS DATE       NO-UNDO. 

DEF BUFFER l-opbuff           FOR l-op.
DEF BUFFER l-ophbuff          FOR l-ophdr.

ASSIGN firstDate = DATE(MONTH(closeDate), 1, YEAR(closeDate)).

FIND FIRST htparam WHERE paramnr = 221 NO-LOCK. 
m-datum  = htparam.fdate. 
FIND FIRST htparam WHERE paramnr = 224 NO-LOCK. 
fb-datum = htparam.fdate. 

FIND FIRST l-op WHERE l-op.datum GE firstDate 
    AND l-op.datum LE closeDate 
    AND l-op.op-art LE 4 NO-LOCK NO-ERROR. 
DO WHILE AVAILABLE l-op: 
    DO TRANSACTION:
      FIND FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr 
        NO-LOCK NO-ERROR. 
      IF AVAILABLE l-artikel 
        AND ((inv-type = 1 AND l-artikel.endkum LT m-endkum) 
          OR (inv-type = 2 AND l-artikel.endkum GE m-endkum) 
          OR (inv-type = 3)) THEN 
      DO: 
        /*IF l-op.loeschflag LE 1 THEN*/ /* Modify by Michael @ 06/09/2018 to preserve cancel inventory history */
        IF l-op.loeschflag LE 2 THEN
        DO:
          CREATE l-ophis.
          BUFFER-COPY l-op TO l-ophis.
          IF l-op.op-art = 3 AND l-op.stornogrund NE "" THEN 
              l-ophis.fibukonto = l-op.stornogrund.
          IF l-op.loeschflag EQ 2 THEN ASSIGN l-ophis.fibukonto = l-op.stornogrund + ";CANCELLED". /* Add by Michael @ 06/09/2018 to preserve cancel inventory history */
          IF (l-op.op-art = 2 OR l-op.op-art = 4) THEN l-ophis.lief-nr = l-op.pos. 
          FIND CURRENT l-ophis NO-LOCK.
        END.
        FIND FIRST l-opbuff WHERE RECID(l-opbuff) = RECID(l-op).
        DELETE l-opbuff. 
        RELEASE l-opbuff.
      END.
      ELSE IF NOT AVAILABLE l-artikel THEN
      DO:
          FIND FIRST l-opbuff WHERE RECID(l-opbuff) = RECID(l-op).
          DELETE l-opbuff. 
          RELEASE l-opbuff.
      END.
    END.
    FIND NEXT l-op WHERE l-op.datum GE firstDate 
        AND l-op.datum LE closeDate 
        AND l-op.op-art LE 4 NO-LOCK NO-ERROR. 
END. 

IF inv-type = 1 AND fb-datum LT m-datum THEN delete-oph = YES. 
ELSE IF inv-type = 2 AND m-datum LT fb-datum THEN delete-oph = YES. 
ELSE IF inv-type = 3 THEN delete-oph = YES.
IF NOT delete-oph THEN RETURN.

FIND FIRST l-ophdr WHERE (l-ophdr.op-typ = "STI" 
   OR l-ophdr.op-typ = "STT" OR l-ophdr.op-typ = "WIP") 
  AND l-ophdr.datum GE firstDate
  AND l-ophdr.datum LE closeDate NO-LOCK NO-ERROR. 
DO WHILE AVAILABLE l-ophdr: 
    DO TRANSACTION:
        CREATE l-ophhis.
        BUFFER-COPY l-ophdr TO l-ophhis.
        FIND FIRST l-ophbuff WHERE RECID(l-ophbuff) = RECID(l-ophdr).
        DELETE l-ophbuff.
        RELEASE l-ophbuff.
    END.
    FIND NEXT l-ophdr WHERE (l-ophdr.op-typ = "STI" 
       OR l-ophdr.op-typ = "STT" OR l-ophdr.op-typ = "WIP") 
      AND l-ophdr.datum GE firstDate
      AND l-ophdr.datum LE closeDate NO-LOCK NO-ERROR. 
END. 
