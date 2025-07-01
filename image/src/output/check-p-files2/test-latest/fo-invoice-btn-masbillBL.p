
DEF INPUT  PARAMETER case-type          AS INT.
DEF INPUT  PARAMETER bill-resnr         AS INT.
DEF INPUT  PARAMETER bill-reslinnr      AS INT.
DEF OUTPUT PARAMETER master-str         AS CHAR     NO-UNDO.
DEF OUTPUT PARAMETER master-rechnr      AS CHAR     NO-UNDO.
DEF OUTPUT PARAMETER mbill-resnr        AS INT      NO-UNDO.
DEF OUTPUT PARAMETER mbill-rechnr       AS INT      .
DEF OUTPUT PARAMETER mbill-gastnr       AS INT      NO-UNDO.
DEF OUTPUT PARAMETER mbill-segmentcode  AS INT      NO-UNDO.
DEF OUTPUT PARAMETER task               AS INT      NO-UNDO INIT 0.

DEFINE BUFFER resline FOR res-line.
DEFINE BUFFER mbill   FOR bill.

IF case-type = 1 THEN
DO:
    FIND FIRST resline WHERE resline.resnr = bill-resnr 
        AND resline.reslinnr = bill-reslinnr NO-LOCK.
    /* Rulita 021224 | Fixing serverless git issue 225 */
    IF AVAILABLE resline THEN 
    DO:
      IF resline.l-zuordnung[5] NE 0 THEN
      DO:
          FIND FIRST mbill WHERE mbill.resnr = resline.l-zuordnung[5]
              AND mbill.reslinnr = 0 NO-LOCK NO-ERROR.
          IF AVAILABLE mbill THEN 
          DO:
              ASSIGN
                  task                = 1
                  mbill-resnr         = mbill.resnr
                  mbill-gastnr        = mbill.gastnr
                  mbill-segmentcode   = mbill.segmentcode
                  mbill-rechnr        = mbill.rechnr.
          END.
          ELSE task = 2.
      END.
      ELSE task = 3.
    END.
    /* End Rulita */
END.
ELSE IF case-type = 2 THEN
DO:
    FIND FIRST mbill WHERE mbill.resnr = bill-resnr AND 
      mbill.reslinnr = 0 AND mbill.zinr = "" NO-LOCK NO-ERROR. 
    IF AVAILABLE mbill THEN 
    DO: 
      master-str = "Master Bill". 
      master-rechnr = STRING(mbill.rechnr) + " - " + mbill.NAME. 
    END. 
    ELSE 
    DO: 
      master-str = "". 
      master-rechnr = "". 
    END. 
END.
