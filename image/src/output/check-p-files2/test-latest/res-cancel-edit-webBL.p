DEF INPUT  PARAMETER res-mode       AS CHAR                 NO-UNDO.
DEF INPUT  PARAMETER done           AS LOGICAL              NO-UNDO.
DEF INPUT  PARAMETER inp-resNo      AS INTEGER              NO-UNDO.
DEF INPUT  PARAMETER tot-qty        AS INTEGER              NO-UNDO.
DEF INPUT-OUTPUT PARAMETER reslinNo AS INTEGER              NO-UNDO.
DEF INPUT-OUTPUT PARAMETER grpFlag  AS LOGICAL              NO-UNDO.
DEF OUTPUT PARAMETER successFlag    AS LOGICAL INITIAL NO   NO-UNDO.

DEF VARIABLE delete-it              AS LOGICAL INITIAL NO   NO-UNDO.
DEF VARIABLE found                  AS LOGICAL INITIAL NO   NO-UNDO.
DEF VARIABLE gastNo                 AS INTEGER              NO-UNDO.
DEF BUFFER rline FOR res-line.

/*MASDOD 040723 trap log issue delete res-line*/
MESSAGE "TrapLog " + 
        " res-mode: " +  res-mode + 
        " done: " + string(done) +     
        " inp-resNo: " + string(inp-resNo) +
        " tot-qty: " + string(tot-qty)   
    VIEW-AS ALERT-BOX INFO BUTTONS OK.

RUN cancel-edit.

PROCEDURE cancel-edit: 
  IF (res-mode = "new" OR res-mode = "insert" OR res-mode = "qci") AND NOT done THEN 
  DO TRANSACTION:
      FIND FIRST res-line WHERE res-line.resnr = inp-resNo 
          AND res-line.reslinnr NE reslinNo NO-LOCK NO-ERROR. 
      IF NOT AVAILABLE res-line THEN
      DO:
          FIND FIRST rline WHERE rline.resnr = inp-resNo 
            AND rline.reslinnr = reslinNo
            AND rline.resstatus = 12 EXCLUSIVE-LOCK. 
          IF AVAILABLE rline THEN
          DO:
              ASSIGN gastNo = rline.gastnr.
              DELETE rline. 
              RELEASE rline.
              found = YES.
          END.
          
          IF found THEN
          DO:
              FIND FIRST reservation WHERE reservation.resnr = inp-resNo EXCLUSIVE-LOCK.
              DELETE reservation.
              RELEASE reservation.

              delete-it = YES.
          END.                    
      END.

/* SY 15 AUG 2015 */
      IF res-mode = "new" OR res-mode = "insert" THEN
      DO:
        FIND FIRST res-line WHERE res-line.resnr = inp-resNo 
          AND res-line.reslinnr = reslinNo
          AND res-line.resstatus = 12 EXCLUSIVE-LOCK NO-ERROR.
        IF AVAILABLE res-line THEN
        DO:
          ASSIGN gastNo = res-line.gastnr.
          DELETE res-line. 
          RELEASE res-line.
          delete-it = YES.
        END.
      END.

      /*MT
      FIND FIRST res-line WHERE res-line.resnr = inp-resNo 
        AND res-line.reslinnr = reslinNo EXCLUSIVE-LOCK. 
      ASSIGN gastNo = res-line.gastnr.
      DELETE res-line. 
      RELEASE res-line.

      IF res-mode NE "insert" THEN
      DO:
          IF res-mode = "qci" THEN
          DO: 
              FIND FIRST res-line WHERE res-line.resnr = inp-resNo 
                  AND res-line.active-flag EQ 1 NO-LOCK NO-ERROR. 
          END.
          IF res-mode = "qci" AND NOT AVAILABLE res-line THEN
          DO:
              FIND FIRST reservation WHERE reservation.resnr = inp-resNo EXCLUSIVE-LOCK.
              DELETE reservation.
              RELEASE reservation.
          END.
      END.
      */
      
      IF delete-it THEN
      DO:
          FOR EACH fixleist WHERE fixleist.resnr = inp-resNo 
            AND fixleist.reslinnr = reslinNo: 
            DELETE fixleist. 
          END. 

          FIND FIRST reslin-queasy WHERE reslin-queasy.key = "arrangement" 
            AND reslin-queasy.resnr = inp-resNo AND reslin-queasy.reslinnr = reslinNo 
            NO-LOCK NO-ERROR. 
          DO WHILE AVAILABLE reslin-queasy: 
            FIND CURRENT reslin-queasy EXCLUSIVE-LOCK. 
            DELETE reslin-queasy. 
            FIND NEXT reslin-queasy WHERE reslin-queasy.key = "arrangement" 
              AND reslin-queasy.resnr = inp-resNo AND reslin-queasy.reslinnr = reslinNo 
              NO-LOCK NO-ERROR. 
          END. 

          FOR EACH reslin-queasy WHERE reslin-queasy.key = "flag" 
             AND reslin-queasy.resnr = inp-resNo 
             AND reslin-queasy.reslinnr = reslinNo:
             DELETE reslin-queasy.
          END.

          IF res-mode = "new" OR res-mode = "qci" THEN 
          DO: 
            FIND FIRST reslin-queasy WHERE reslin-queasy.key = "rate-prog" 
              AND reslin-queasy.number1 = inp-resNo AND reslin-queasy.number2 = 0 
              AND reslin-queasy.char1 = "" AND reslin-queasy.reslinnr = 1 
              USE-INDEX argt_ix EXCLUSIVE-LOCK NO-ERROR. 
            IF AVAILABLE reslin-queasy THEN delete reslin-queasy. 
          END. 

          /*FDL June 13, 2024 => Ticket 71CA90*/
          FIND FIRST reslin-queasy WHERE reslin-queasy.key = "ResChanges" 
            AND reslin-queasy.resnr = inp-resNo AND reslin-queasy.reslinnr = reslinNo NO-LOCK NO-ERROR. 
          DO WHILE AVAILABLE reslin-queasy: 
            FIND CURRENT reslin-queasy EXCLUSIVE-LOCK. 
            DELETE reslin-queasy. 
            FIND NEXT reslin-queasy WHERE reslin-queasy.key = "ResChanges" 
              AND reslin-queasy.resnr = inp-resNo AND reslin-queasy.reslinnr = reslinNo NO-LOCK NO-ERROR. 
          END. 
          RELEASE reslin-queasy.
          reslinNo = reslinNo - 1. 
      END.
  END. 

  IF (res-mode = "new" OR res-mode = "insert" OR res-mode = "qci") AND done 
    AND (tot-qty > 1) THEN 
  DO TRANSACTION: 
    FOR EACH res-line WHERE res-line.resnr = inp-resNo 
        AND res-line.gastnr = gastNo EXCLUSIVE-LOCK: 
      res-line.grpflag = YES. 
      RELEASE res-line. 
    END. 
  END. 
  IF tot-qty > 1 THEN grpflag = YES. 
  successFlag = YES.
END. 

