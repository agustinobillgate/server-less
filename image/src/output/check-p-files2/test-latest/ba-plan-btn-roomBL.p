
DEF INPUT  PARAMETER resnr          AS INT.
DEF INPUT  PARAMETER reslinnr       AS INT.
DEF INPUT  PARAMETER chg-room       AS CHAR.
DEF INPUT  PARAMETER user-init      AS CHAR.
DEF INPUT  PARAMETER chg-table      AS CHAR.

DEFINE VARIABLE room-desc1 AS CHAR.
DEFINE VARIABLE room-desc2 AS CHAR.
FIND FIRST bk-reser WHERE bk-reser.veran-nr = resnr 
  AND bk-reser.veran-resnr = reslinnr NO-LOCK NO-ERROR.
/* Rulita 200225 | Fixing if avail serverless git 611 */
IF AVAILABLE bk-reser THEN
DO:
    DO TRANSACTION:
        FIND CURRENT bk-reser EXCLUSIVE-LOCK. 
        bk-reser.raum = chg-room. 
        FIND CURRENT bk-reser NO-LOCK. 
    
        FIND FIRST bk-func WHERE bk-func.veran-nr = bk-reser.veran-nr 
        AND bk-func.veran-seite = bk-reser.veran-seite NO-LOCK NO-ERROR. 
        IF AVAILABLE bk-func THEN 
        DO: 
            /* FIND CURRENT bk-func NO-LOCK. */                                                /* Rulita 200225 | unused code serverless git 611 */
            FIND FIRST bk-raum WHERE bk-raum.raum = bk-func.raeume[1].
            IF AVAILABLE bk-raum THEN room-desc1 = bk-raum.bezeich.                            /* Rulita 200225 | Fixing if avail serverless git 611 */
            FIND FIRST bk-raum WHERE bk-raum.raum = chg-room.
            IF AVAILABLE bk-raum THEN room-desc2 = bk-raum.bezeich.                            /* Rulita 200225 | Fixing if avail serverless git 611 */
            IF bk-func.tischform[1] = "" THEN
            DO:
                FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK. 
                CREATE res-history. 
                ASSIGN 
                  res-history.nr = bediener.nr 
                  res-history.datum = TODAY 
                  res-history.zeit = TIME 
                  res-history.aenderung = "Room Changes From " + room-desc1
                    + " To " + room-desc2 + " Table Setup From Not Defined" + 
                    " To " + chg-table
                  res-history.action = "Banquet"
                . 
                FIND CURRENT res-history NO-LOCK. 
                RELEASE res-history. 
            END.
            ELSE
            DO:
                FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK. 
                CREATE res-history. 
                ASSIGN 
                  res-history.nr = bediener.nr 
                  res-history.datum = TODAY 
                  res-history.zeit = TIME 
                  res-history.aenderung = "Room Changes From " + bk-func.raeume[1]
                    + " To " + chg-room + " Table Setup From " + bk-func.tischform[1] + 
                    " To " + chg-table
                  res-history.action = "Banquet"
                . 
                FIND CURRENT res-history NO-LOCK. 
                RELEASE res-history. 
            END.
    
          FIND CURRENT bk-func EXCLUSIVE-LOCK.
          bk-func.raeume[1] = chg-room.
          bk-func.tischform[1] = chg-table.
          FIND CURRENT bk-func NO-LOCK. 
          RELEASE bk-func.                                                 /* Rulita 200225 | added release serverless git 611 */
        END. 
        RELEASE bk-reser.                                                /* Rulita 200225 | added release serverless git 611 */
    END.
END.
/* End Rulita */
