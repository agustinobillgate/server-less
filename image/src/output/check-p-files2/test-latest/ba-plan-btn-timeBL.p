
DEF INPUT  PARAMETER resnr          AS INT.
DEF INPUT  PARAMETER reslinnr       AS INT.
DEF INPUT  PARAMETER user-init      AS CHAR.
DEF INPUT  PARAMETER chg-date       AS DATE.
DEF INPUT  PARAMETER begin-time     LIKE bk-reser.von-zeit. 
DEF INPUT  PARAMETER ending-time    LIKE bk-reser.bis-zeit. 
DEF INPUT  PARAMETER begin-i        LIKE bk-reser.von-i. 
DEF INPUT  PARAMETER ending-i       LIKE bk-reser.bis-i. 

DEFINE VARIABLE week-list AS CHAR EXTENT 7 FORMAT "x(19)" 
  INITIAL ["Sunday   ", "Monday   ", "Tuesday  ", "Wednesday", "Thursday  ", 
           "Friday    ", "Saturday  "]. 

FIND FIRST bk-reser WHERE bk-reser.veran-nr = resnr 
  AND bk-reser.veran-resnr = reslinnr NO-LOCK NO-ERROR. 
/* Rulita 200225 | Fixing for serverless 611 git */
IF AVAILABLE bk-reser THEN 
DO:
    DO TRANSACTION :
        /* FIND CURRENT bk-reser NO-LOCK. */                                                /* Rulita 200225 | unused code serverless git 611 */
        IF bk-reser.von-zeit NE begin-time OR bk-reser.bis-zeit NE ending-time
           THEN
        DO:
            FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK. 
            CREATE res-history. 
            ASSIGN 
              res-history.nr = bediener.nr 
              res-history.datum = TODAY 
              res-history.zeit = TIME 
              res-history.aenderung = "Time Changes from " 
                + string(bk-reser.von-zeit,"99:99" ) + " - " + string(bk-reser.bis-zeit,"99:99" ) +  " To "
                + string(begin-time,"99:99" ) + " - " + string(ending-time,"99:99" )
              res-history.action = "Banquet"
                  . 
            FIND CURRENT res-history NO-LOCK. 
            RELEASE res-history. 
        END.
        IF bk-reser.datum NE chg-date THEN
        DO:
            FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK. 
            CREATE res-history. 
            ASSIGN 
              res-history.nr = bediener.nr 
              res-history.datum = TODAY 
              res-history.zeit = TIME 
              res-history.aenderung = "Date Changes from " 
                + string(bk-reser.datum)  +  " To " + STRING(chg-date)
              res-history.action = "Banquet"
            . 
            FIND CURRENT res-history NO-LOCK. 
            RELEASE res-history. 
        END.
    
        FIND CURRENT bk-reser EXCLUSIVE-LOCK. 
        bk-reser.von-zeit = begin-time. 
        bk-reser.von-i = begin-i. 
        bk-reser.bis-zeit = ending-time. 
        bk-reser.bis-i = ending-i. 
        bk-reser.datum = chg-date.
        bk-reser.bis-datum = chg-date.
        FIND CURRENT bk-reser NO-LOCK. 
        
        FIND FIRST bk-func WHERE bk-func.veran-nr = bk-reser.veran-nr 
          AND bk-func.veran-seite = bk-reser.veran-seite NO-LOCK NO-ERROR. 
        IF AVAILABLE bk-func THEN 
        DO: 
          FIND CURRENT bk-func EXCLUSIVE-LOCK. 
          bk-func.datum = chg-date.
          bk-func.bis-datum = chg-date.
          bk-func.uhrzeit = STRING(bk-reser.von-zeit,"99:99" ) + " - " 
            + STRING(bk-reser.bis-zeit,"99:99"). 
          bk-func.wochentag = week-list[WEEKDAY(bk-reser.datum)]. /* Mulyadi before added bk-func.wochentag not exist in this procedure */
          bk-func.uhrzeiten[1] = STRING(bk-reser.von-zeit,"99:99" ) + " - " + STRING(bk-reser.bis-zeit,"99:99"). 
          FIND CURRENT bk-func NO-LOCK. 
        END. 
        RELEASE bk-reser.                                                 /* Rulita 200225 | added release serverless git 611 */
    END.
END.
/* End Rulita */
