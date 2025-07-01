DEFINE TEMP-TABLE s-list 
    FIELD datum     AS DATE LABEL "Date" 
    FIELD ftime     LIKE bk-reser.von-zeit 
    FIELD ttime     LIKE bk-reser.bis-zeit
    FIELD raum      LIKE bk-raum.bezeich
    FIELD wday      AS CHAR FORMAT "x(10)" LABEL "WeekDay"
    FIELD raum1     LIKE bk-raum.raum
    FIELD resstatus AS INTEGER
. 

DEFINE INPUT  PARAMETER TABLE FOR s-list.
DEFINE INPUT  PARAMETER resnr       AS INTEGER. 
DEFINE INPUT  PARAMETER reslinnr    AS INTEGER. 
DEFINE INPUT  PARAMETER res-flag    AS LOGICAL.
DEFINE INPUT  PARAMETER user-init   AS CHAR.

DEFINE VARIABLE von-i         AS INTEGER NO-UNDO. 
DEFINE VARIABLE bis-i         AS INTEGER NO-UNDO. 
DEFINE VARIABLE tmp-usernr    AS INTEGER NO-UNDO.        /* Rulita 200225 | Fixing temp user nr serverless issue git 620 */

DEFINE VARIABLE week-list AS CHAR EXTENT 7 FORMAT "x(19)" 
  INITIAL ["Monday   ", "Tuesday  ", "Wednesday", "Thursday  ", 
           "Friday    ", "Saturday  ", "Sunday   "]. 

DEFINE VARIABLE rstat-chr AS CHAR EXTENT 3 INITIAL ["F", "T", "W"].

FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK NO-ERROR. 
IF AVAILABLE bediener THEN tmp-usernr = bediener.nr.            /* Rulita 200225 | Fixing chg from bediener.nr to tmp-usernr serverless issue git 620 */

FIND FIRST bk-veran WHERE bk-veran.veran-nr = resnr NO-LOCK NO-ERROR.
IF AVAILABLE bk-veran THEN 
DO:
    FIND FIRST bk-reser WHERE bk-reser.veran-nr = resnr 
    AND bk-reser.veran-resnr = reslinnr NO-LOCK NO-ERROR. 
    IF AVAILABLE bk-reser THEN
    DO:
        FIND FIRST bk-func WHERE bk-func.veran-nr = resnr 
          AND bk-func.veran-seite = reslinnr NO-LOCK NO-ERROR. 
        IF AVAILABLE bk-func THEN
        DO:
            FIND FIRST bk-raum WHERE bk-raum.raum = bk-reser.raum NO-LOCK NO-ERROR.
            RUN create-resline.
        END. 
    END.
END.

/* RUN create-resline. */        /* Rulita 200225 | Fixing move to if avail bk-func serverless issue git 620 */

PROCEDURE create-resline: 
DEF VAR curr-resnr  AS INTEGER.
DEF VAR reslin-nr   AS INTEGER INITIAL 1.
DEF BUFFER bk-main  FOR bk-veran.
DEF BUFFER bk-res1  FOR bk-reser. 
DEF BUFFER bk-func1 FOR bk-func. 
  curr-resnr = resnr. 
  DO TRANSACTION: 
    FOR EACH s-list:
      IF NOT res-flag THEN RUN get-reslinnr(OUTPUT reslin-nr). 
      ELSE
      DO:
        FIND FIRST counters WHERE counters.counter-no = 16 EXCLUSIVE-LOCK 
          NO-ERROR. 
        IF NOT AVAILABLE counters THEN
        DO: 
          CREATE counters. 
          ASSIGN
            counters.counter-no = 16
            counters.counter-bez = "Banquet Reservation No.". 
        END. 
        ASSIGN counters.counter = counters.counter + 1. 
        FIND CURRENT counter NO-LOCK. 
        curr-resnr = counters.counter.
        CREATE bk-main.
        BUFFER-COPY bk-veran EXCEPT bk-veran.veran-nr bk-veran.rechnr TO bk-main.
        ASSIGN
            bk-main.veran-nr    = curr-resnr
            bk-main.resnr       = 1
            bk-main.bediener-nr = tmp-usernr                /* Rulita 200225 | Fixing chg from bediener.nr to tmp-usernr serverless issue git 620 */
        .
        FIND CURRENT bk-main NO-LOCK.
      END.
      von-i = INTEGER(SUBSTR(s-list.ftime,1,2)) * 2 + INTEGER(SUBSTR(s-list.ftime,3,2)) / 30 + 1. 
      bis-i = INTEGER(SUBSTR(s-list.ttime,1,2)) * 2 + INTEGER(SUBSTR(s-list.ttime,3,2)) / 30 + 1. 

      CREATE bk-res1. 
      BUFFER-COPY bk-reser EXCEPT bk-reser.datum bk-reser.veran-resnr bk-reser.resstatus TO bk-res1. 
      ASSIGN 
        bk-res1.datum       = s-list.datum 
        bk-res1.bis-datum   = s-list.datum 
        bk-res1.veran-nr    = curr-resnr
        bk-res1.veran-resnr = reslin-nr 
        bk-res1.veran-seite = reslin-nr 
        bk-res1.resstatus   = s-list.resstatus
        bk-res1.von-zeit    = s-list.ftime 
        bk-res1.bis-zeit    = s-list.ttime 
        bk-res1.von-i       = von-i 
        bk-res1.bis-i       = bis-i 
        bk-res1.bediener-nr = tmp-usernr                /* Rulita 200225 | Fixing chg from bediener.nr to tmp-usernr serverless issue git 620 */
        bk-res1.raum        = s-list.raum1

      . 

      FIND CURRENT bk-res1 NO-LOCK. 
      RELEASE bk-res1. 

      CREATE bk-func1. 
      BUFFER-COPY bk-func EXCEPT bk-func.datum bk-func.veran-seite /*bk-func.ape_getraenke*/ /*FDL Comment Ticket DBE9D0*/
          bk-func.resstatus TO bk-func1. 
      ASSIGN 
        bk-func1.datum              = s-list.datum 
        bk-func1.bis-datum          = s-list.datum 
        bk-func1.veran-nr           = curr-resnr
        bk-func1.veran-seite        = reslin-nr 
        bk-func1.resstatus          = s-list.resstatus
        bk-func1.wochentag          = week-list[WEEKDAY(s-list.datum - 1)] /* Mulyadi 11/10/11 date's index not same*/
        bk-func1.resnr[1]           = reslin-nr 
        bk-func1.vgeschrieben       = user-init 
        bk-func1.vkontrolliert      = user-init
        bk-func1.c-resstatus[1]     = rstat-chr[s-list.resstatus]
        bk-func1.r-resstatus[1]     = s-list.resstatus
        bk-func1.raeume[1]          = s-list.raum1
        bk-func1.uhrzeit            = STRING(s-list.ftime,"99:99" ) + " - " + STRING(s-list.ttime,"99:99")        
      . 
       FIND CURRENT bk-func1 NO-LOCK. 
      RELEASE bk-func1. 
     END. 
  END. 
END. 

PROCEDURE get-reslinnr: 
DEFINE OUTPUT PARAMETER reslin-nr AS INTEGER INITIAL 1. 
DEFINE BUFFER bk-res1 FOR bk-reser. 
  FOR EACH bk-res1 WHERE bk-res1.veran-nr = resnr NO-LOCK 
    BY bk-res1.veran-resnr DESCENDING: 
    reslin-nr = bk-res1.veran-resnr + 1. 
    RETURN. 
  END. 
END. 

