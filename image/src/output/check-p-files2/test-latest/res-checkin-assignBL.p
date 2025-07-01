
DEF INPUT PARAMETER case-type   AS INT.
DEF INPUT PARAMETER resnr       AS INTEGER. 
DEF INPUT PARAMETER reslinnr    AS INTEGER. 
DEF INPUT PARAMETER nat-bez     AS CHAR.
DEF INPUT PARAMETER purNo       AS INT.

DEFINE BUFFER gast          FOR guest. 
DEFINE BUFFER res-line1     FOR res-line. 
DEFINE BUFFER rline         FOR res-line. 
DEFINE BUFFER res-sharer    FOR res-line. 

FIND FIRST res-line WHERE res-line.resnr = resnr 
  AND res-line.reslinnr = reslinnr NO-LOCK. 

IF case-type = 1 THEN
DO:
    FIND FIRST gast WHERE gast.gastnr = res-line.gastnrmember NO-LOCK.
    DO TRANSACTION:
        FIND CURRENT gast EXCLUSIVE-LOCK.
        gast.land = nat-bez.
        FIND CURRENT gast NO-LOCK.
    END.
END.
ELSE IF case-type = 2 THEN
DO:
    FIND FIRST gast WHERE gast.gastnr = res-line.gastnrmember NO-LOCK.
    DO TRANSACTION:
        FIND CURRENT gast EXCLUSIVE-LOCK.
        gast.nation1 = nat-bez.
        FIND CURRENT gast NO-LOCK.
    END.
END.
ELSE IF case-type = 3 THEN
DO:
    DO TRANSACTION:
        FIND CURRENT res-line EXCLUSIVE-LOCK.
        ASSIGN res-line.zimmer-wunsch = res-line.zimmer-wunsch +
          "SEGM_PUR" + STRING(purNo) + ";".
        FIND CURRENT res-line NO-LOCK.
        FIND FIRST res-line1 WHERE res-line1.resnr = res-line.resnr
          AND res-line1.reslinnr NE res-line.reslinnr
          AND res-line1.active-flag LE 1
          AND res-line1.resstatus NE 12
          AND res-line1.l-zuordnung[3] = 0 NO-LOCK NO-ERROR.
        DO WHILE AVAILABLE res-line1:
          IF NOT res-line1.zimmer-wunsch MATCHES("*SEGM_PUR*") THEN
          DO:
              FIND FIRST rline WHERE RECID(rline) = RECID(res-line1)
                EXCLUSIVE-LOCK NO-ERROR NO-WAIT.
              IF AVAILABLE rline THEN
              DO:
                ASSIGN rline.zimmer-wunsch = rline.zimmer-wunsch +
                  "SEGM_PUR" + STRING(purNo) + ";".
                FIND CURRENT rline NO-LOCK.
              END.
          END.
          FIND NEXT res-line1 WHERE res-line1.resnr = res-line.resnr
            AND res-line1.reslinnr NE res-line.reslinnr
            AND res-line1.active-flag LE 1
            AND res-line1.resstatus NE 12
            AND res-line1.l-zuordnung[3] = 0 NO-LOCK NO-ERROR.
        END.
    END.
END.
ELSE IF case-type = 4 THEN
DO:
    FIND CURRENT res-line NO-LOCK.
    FOR EACH res-sharer WHERE res-sharer.resnr = resnr
      AND res-sharer.kontakt-nr = reslinnr
      AND res-sharer.l-zuordnung[3] = 1:
      ASSIGN
        res-sharer.zinr        = res-line.zinr
        res-sharer.zikatnr     = res-line.zikatnr
        res-sharer.setup       = res-line.setup
      .
    END.
END.
