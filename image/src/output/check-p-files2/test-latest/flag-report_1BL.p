DEFINE TEMP-TABLE s-list 
  FIELD newflag AS LOGICAL INITIAL YES
  FIELD id      AS CHAR FORMAT "x(3)"   LABEL "ID"
  FIELD frdate  AS DATE LABEL "FrDate" 
  FIELD datum   AS DATE LABEL "ToDate" 
  FIELD note    AS CHAR FORMAT "x(158)" LABEL "Note"
  FIELD urgent  AS LOGICAL INITIAL NO   LABEL "Urgent" 
  FIELD done    AS LOGICAL INITIAL NO   LABEL "Done" 
  FIELD dept    AS CHAR FORMAT "x(32)"  LABEL "Department"
  FIELD ciflag  AS LOGICAL LABEL "Disp C/I"
  FIELD coflag  AS LOGICAL LABEL "Disp C/O"
  FIELD rsv-detail AS LOGICAL LABEL "Disp Reservation Detail"
  FIELD bill-flag  AS LOGICAL LABEL "Disp Bill". 

DEFINE TEMP-TABLE sbuff LIKE s-list.

DEF INPUT  PARAMETER case-type   AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER n           AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER resnr       AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER reslinnr    AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER user-init   AS CHAR    NO-UNDO.
DEF INPUT  PARAMETER TABLE FOR s-list.

DEF VARIABLE i AS INTEGER NO-UNDO.
DEF VARIABLE k AS INTEGER NO-UNDO.

FIND FIRST res-line WHERE res-line.resnr = resnr 
    AND res-line.reslinnr = reslinnr NO-LOCK NO-ERROR.
FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK.
FIND FIRST s-list.

CASE case-type:
    WHEN 1 THEN
    DO:
      IF AVAILABLE res-line THEN
      DO:
        CREATE res-history.
        ASSIGN
            res-history.nr = bediener.nr
            res-history.datum = TODAY
            res-history.zeit = TIME
            res-history.aenderung = "Flag Report deleted: " + res-line.NAME
               + " ResNo: " + STRING(res-line.resnr)
               + " RmNo: " + res-line.zinr
               + " Date: " + STRING(s-list.datum)
               + " Note: " + s-list.note
            res-history.action = "Flag Report".
        FIND CURRENT res-history NO-LOCK.
        RELEASE res-history.
      END.
    END.
    WHEN 2 THEN
    DO:
        FIND FIRST s-list WHERE s-list.datum NE ? NO-ERROR.
        IF NOT AVAILABLE s-list THEN                                          
        DO: 
            FIND FIRST reslin-queasy WHERE reslin-queasy.key = "flag" 
              AND reslin-queasy.resnr = resnr 
              AND reslin-queasy.reslinnr = reslinnr 
              AND reslin-queasy.betriebsnr = n EXCLUSIVE-LOCK NO-ERROR. 
            IF AVAILABLE reslin-queasy THEN DELETE reslin-queasy. 
        END. 
        ELSE                                                                  
        DO: 
            FIND FIRST reslin-queasy WHERE reslin-queasy.key = "flag" 
              AND reslin-queasy.resnr = resnr 
              AND reslin-queasy.reslinnr = reslinnr 
              AND reslin-queasy.betriebsnr = n EXCLUSIVE-LOCK NO-ERROR. 
            IF NOT AVAILABLE reslin-queasy THEN                                 
            DO: 
                create reslin-queasy. 
                ASSIGN 
                  reslin-queasy.key = "flag" 
                  reslin-queasy.resnr = resnr 
                  reslin-queasy.reslinnr = reslinnr
                  reslin-queasy.betriebsnr = n. 
            END. 
            DO:                                                                 
                ASSIGN 
                  reslin-queasy.date1   = ? 
                  reslin-queasy.char1   = "" 
                  reslin-queasy.number1 = 0 
                  reslin-queasy.deci1   = 0 
                  reslin-queasy.date2   = ? 
                  reslin-queasy.char2   = "" 
                  reslin-queasy.number2 = 0 
                  reslin-queasy.deci2   = 0 
                  reslin-queasy.date3   = ? 
                  reslin-queasy.char3   = "" 
                  reslin-queasy.number3 = 0 
                  reslin-queasy.deci3   = 0 
                . 
            END. 


            k = (reslin-queasy.betriebsnr * 3) + 1.
            i = 0.
            FOR EACH s-list WHERE s-list.datum NE ? AND i LT (k + 3) 
                BY s-list.datum :    
                i = i + 1.  
                IF i = k THEN  
                DO: 
                    ASSIGN 
                      reslin-queasy.date1   = s-list.datum 
                      reslin-queasy.char1   = s-list.note 
                                            + CHR(2) + s-list.id.
                    IF s-list.id = "" AND s-list.newflag 
                      THEN reslin-queasy.char1 = reslin-queasy.char1 + bediener.userinit.
                    ASSIGN
                      reslin-queasy.char1   = reslin-queasy.char1
                                            + CHR(2) + STRING(MONTH(s-list.frdate),"99") 
                                                     + STRING(DAY(s-list.frdate),"99")
                                                     + STRING(YEAR(s-list.frdate))
                                            + CHR(2) + s-list.dept
                                            + CHR(2) + STRING(INTEGER(s-list.ciflag))
                                            + CHR(2) + STRING(INTEGER(s-list.rsv-detail))
                                            + CHR(2) + STRING(INTEGER(s-list.bill-flag))
                      reslin-queasy.logi1   = s-list.coflag 
                      reslin-queasy.number1 = INTEGER(s-list.urgent) 
                      reslin-queasy.deci1   = INTEGER(s-list.done) 
                    . 
                END.

                IF i = (k + 1) THEN 
                DO: 
                    ASSIGN 
                      reslin-queasy.date2   = s-list.datum 
                      reslin-queasy.char2   = s-list.note 
                                            + CHR(2) + s-list.id.
                    IF s-list.id = "" THEN reslin-queasy.char2 = reslin-queasy.char2
                        + bediener.userinit.
                    ASSIGN
                      reslin-queasy.char2   = reslin-queasy.char2
                                            + CHR(2) + STRING(MONTH(s-list.frdate),"99") 
                                                     + STRING(DAY(s-list.frdate),"99")
                                                     + STRING(YEAR(s-list.frdate))
                                            + CHR(2) + s-list.dept
                                            + CHR(2) + STRING(INTEGER(s-list.ciflag))
                                            + CHR(2) + STRING(INTEGER(s-list.rsv-detail))
                                            + CHR(2) + STRING(INTEGER(s-list.bill-flag))
                      reslin-queasy.logi2   = s-list.coflag 
                      reslin-queasy.number2 = INTEGER(s-list.urgent) 
                      reslin-queasy.deci2   = INTEGER(s-list.done) 
                    . 
                END. 
                IF i = (k + 2) THEN 
                DO: 
                    ASSIGN 
                      reslin-queasy.date3   = s-list.datum 
                      reslin-queasy.char3   = s-list.note 
                                            + CHR(2) + s-list.id.
                    IF s-list.id = "" THEN reslin-queasy.char3 = reslin-queasy.char3
                        + bediener.userinit.
                    ASSIGN
                      reslin-queasy.char3   = reslin-queasy.char3
                                            + CHR(2) + STRING(MONTH(s-list.frdate),"99") 
                                                     + STRING(DAY(s-list.frdate),"99")
                                                     + STRING(YEAR(s-list.frdate))
                                            + CHR(2) + s-list.dept
                                            + CHR(2) + STRING(INTEGER(s-list.ciflag))
                                            + CHR(2) + STRING(INTEGER(s-list.rsv-detail))
                                            + CHR(2) + STRING(INTEGER(s-list.bill-flag))
                      reslin-queasy.logi3   = s-list.coflag 
                      reslin-queasy.number3 = INTEGER(s-list.urgent) 
                      reslin-queasy.deci3   = INTEGER(s-list.done) 
                    . 
                END.
            END.
        END.
    END.
END CASE.

/*MT
CASE case-type:
  WHEN 1 THEN
  REPEAT n = 0 TO 2. 
    FIND FIRST reslin-queasy WHERE reslin-queasy.key = "flag" 
      AND reslin-queasy.resnr = resnr 
      AND reslin-queasy.reslinnr = reslinnr 
      AND reslin-queasy.betriebsnr = n NO-LOCK NO-ERROR. 
     
    CREATE s-list. 
    IF AVAILABLE reslin-queasy THEN 
    DO: 
      ASSIGN
        s-list.datum  = reslin-queasy.date1
        s-list.coflag = reslin-queasy.logi1
        s-list.urgent = (reslin-queasy.number1 = 1)
        s-list.done   = (reslin-queasy.deci1 = 1)
      .
      IF s-list.datum NE ? THEN 
          ASSIGN s-list.newflag = NO
                 s-list.note    = ENTRY(1, reslin-queasy.char1, CHR(2)) .
      IF INDEX(reslin-queasy.char1,CHR(2)) GT 0 THEN
          s-list.id = ENTRY(2, reslin-queasy.char1, CHR(2)).    
    END.
    
    CREATE s-list. 
    IF AVAILABLE reslin-queasy THEN 
    DO: 
      ASSIGN
        s-list.datum  = reslin-queasy.date2
        s-list.coflag = reslin-queasy.logi2
        s-list.urgent = (reslin-queasy.number2 = 1)
        s-list.done   = (reslin-queasy.deci2 = 1)
      .
      IF s-list.datum NE ? THEN 
          ASSIGN s-list.newflag = NO
                 s-list.note    = ENTRY(1, reslin-queasy.char2, CHR(2)) .
      IF INDEX(reslin-queasy.char2,CHR(2)) GT 0 THEN
          s-list.id = ENTRY(2, reslin-queasy.char2, CHR(2)).
    END.
    
    CREATE s-list. 
    IF AVAILABLE reslin-queasy THEN 
    DO: 
      ASSIGN
        s-list.datum  = reslin-queasy.date3
        s-list.coflag = reslin-queasy.logi3
        s-list.urgent = (reslin-queasy.number3 = 1)
        s-list.done   = (reslin-queasy.deci3 = 1)
      .
      IF s-list.datum NE ? THEN 
          ASSIGN s-list.newflag = NO         
                 s-list.note    = ENTRY(1, reslin-queasy.char3, CHR(2)) .
      IF INDEX(reslin-queasy.char3,CHR(2)) GT 0 THEN
          s-list.id = ENTRY(2, reslin-queasy.char3, CHR(2)).
    END.
  END. 
 
  WHEN 2 THEN
  DO:
    FIND FIRST sbuff NO-ERROR.
    FIND FIRST res-line WHERE res-line.resnr = resnr 
      AND res-line.reslinnr = reslinnr NO-LOCK.
    CREATE res-history. 
    ASSIGN 
      res-history.nr          = bediener.nr 
      res-history.datum       = TODAY 
      res-history.zeit        = TIME 
      res-history.aenderung   = "Flag Report deleted: " + res-line.NAME 
         + " ResNo: " + STRING(res-line.resnr) 
         + " RmNo: "  + res-line.zinr
         + " Date: "  + STRING(sbuff.datum)
         + " Note: "  + sbuff.note
      res-history.action = "Flag Report". 
    FIND CURRENT res-history NO-LOCK. 
    RELEASE res-history. 
  END.

  WHEN 3 THEN
  DO:
    FIND FIRST sbuff NO-ERROR.
    DO WHILE AVAILABLE sbuff:
      FIND NEXT sbuff NO-ERROR.
    END.
    REPEAT n = 0 TO 2.
      FIND FIRST sbuff WHERE sbuff.datum NE ? NO-ERROR. 
      IF NOT AVAILABLE sbuff THEN                                          
      DO: 
        FIND FIRST reslin-queasy WHERE reslin-queasy.key = "flag" 
          AND reslin-queasy.resnr = resnr 
          AND reslin-queasy.reslinnr = reslinnr 
          AND reslin-queasy.betriebsnr = n EXCLUSIVE-LOCK NO-ERROR. 
        IF AVAILABLE reslin-queasy THEN DELETE reslin-queasy. 
      END. 
      ELSE                                                                  
      DO: 
        FIND FIRST reslin-queasy WHERE reslin-queasy.key = "flag" 
          AND reslin-queasy.resnr = resnr 
          AND reslin-queasy.reslinnr = reslinnr 
          AND reslin-queasy.betriebsnr = n EXCLUSIVE-LOCK NO-ERROR. 
        IF NOT AVAILABLE reslin-queasy THEN                                 
        DO: 
          CREATE reslin-queasy. 
          ASSIGN 
            reslin-queasy.key = "flag" 
            reslin-queasy.resnr = resnr 
            reslin-queasy.reslinnr = reslinnr
            reslin-queasy.betriebsnr = n. 
        END. 
        DO:                                                                 
          ASSIGN 
            reslin-queasy.date1   = ? 
            reslin-queasy.char1   = "" 
            reslin-queasy.number1 = 0 
            reslin-queasy.deci1   = 0 
            reslin-queasy.date2   = ? 
            reslin-queasy.char2   = "" 
            reslin-queasy.number2 = 0 
            reslin-queasy.deci2   = 0 
            reslin-queasy.date3   = ? 
            reslin-queasy.char3   = "" 
            reslin-queasy.number3 = 0 
            reslin-queasy.deci3   = 0 
          . 
        END. 
        k = (reslin-queasy.betriebsnr * 3) + 1.
        i = 0.
        FOR EACH sbuff WHERE sbuff.datum NE ? AND i LT (k + 3) BY sbuff.datum :    
          i = i + 1.  
          IF i = k THEN  
          DO: 
            ASSIGN 
              reslin-queasy.date1   = sbuff.datum 
              reslin-queasy.char1   = sbuff.note + CHR(2) + sbuff.id
              reslin-queasy.logi1   = sbuff.coflag 
              reslin-queasy.number1 = INTEGER(sbuff.urgent) 
              reslin-queasy.deci1   = INTEGER(sbuff.done) 
            . 
            IF sbuff.id = "" AND sbuff.newflag 
              THEN reslin-queasy.char1 = reslin-queasy.char1 + bediener.userinit.
          END.
          IF i = (k + 1) THEN 
          DO: 
            ASSIGN 
              reslin-queasy.date2   = sbuff.datum 
              reslin-queasy.char2   = sbuff.note + CHR(2) + sbuff.id
              reslin-queasy.logi2   = sbuff.coflag 
              reslin-queasy.number2 = INTEGER(sbuff.urgent) 
              reslin-queasy.deci2   = INTEGER(sbuff.done) 
            . 
            IF sbuff.id = "" THEN reslin-queasy.char2 = reslin-queasy.char2
                + bediener.userinit.
          END. 
          IF i = (k + 2) THEN 
          DO: 
            ASSIGN 
              reslin-queasy.date3   = sbuff.datum 
              reslin-queasy.char3   = sbuff.note + CHR(2) + sbuff.id
              reslin-queasy.logi3   = sbuff.coflag 
              reslin-queasy.number3 = INTEGER(sbuff.urgent) 
              reslin-queasy.deci3   = INTEGER(sbuff.done) 
            . 
            IF sbuff.id = "" THEN reslin-queasy.char3 = reslin-queasy.char3
                + bediener.userinit.
          END.
        END.
      END.
    END. 
  END.

END CASE.
*/
