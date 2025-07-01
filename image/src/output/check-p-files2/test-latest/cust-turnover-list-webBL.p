DEFINE TEMP-TABLE cust-list
    FIELD gastnr            LIKE guest.gastnr
    FIELD cust-name         AS CHAR     
    FIELD gesamtumsatz      LIKE guest.gesamtumsatz 
    FIELD logiernachte      LIKE guest.logiernachte 
    FIELD argtumsatz        LIKE guest.argtumsatz 
    FIELD f-b-umsatz        LIKE guest.f-b-umsatz 
    FIELD sonst-umsatz      LIKE guest.sonst-umsatz 
    FIELD wohnort           LIKE guest.wohnort 
    FIELD plz               LIKE guest.plz 
    FIELD land              LIKE guest.land
    FIELD sales-id          LIKE guest.phonetik3
    FIELD ba-umsatz         AS DECIMAL
    FIELD ly-rev            AS DECIMAL
    FIELD region            AS CHAR
    FIELD region1           AS CHAR
    FIELD stayno            AS INT
    FIELD resnr             AS CHAR
    FIELD counter           AS INT
    FIELD counterall        AS INT
    FIELD resno             AS INTEGER
    FIELD reslinnr          AS INTEGER
    FIELD curr-pos          AS INTEGER.


DEFINE INPUT PARAMETER cardtype             AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER sort-type            AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER curr-sort1           AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER fdate                AS DATE    NO-UNDO.
DEFINE INPUT PARAMETER tdate                AS DATE    NO-UNDO.
DEFINE INPUT PARAMETER check-ftd            AS LOGICAL NO-UNDO.
DEFINE INPUT PARAMETER currency             AS CHAR    NO-UNDO.
DEFINE INPUT PARAMETER excl-other           AS LOGICAL NO-UNDO.
DEFINE INPUT PARAMETER curr-sort2           AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER idFlag               AS CHAR    NO-UNDO. 

DEFINE VARIABLE sort1       AS INTEGER NO-UNDO.
DEFINE VARIABLE tmp-counter AS INTEGER NO-UNDO.                              /* Rulita 150525 | Fixing serverless rename var counter git issue 608 */
DEFINE BUFFER bqueasy FOR queasy.
DEFINE BUFFER pqueasy FOR queasy.

CREATE queasy.
ASSIGN queasy.KEY      = 285
       queasy.char1    = "Guest Turnover"
       queasy.number1  = 1
       queasy.char2    = idFlag.
RELEASE queasy.



RUN cust-turnover-listbl.p (cardtype, sort-type, curr-sort1, 
                        fdate, tdate,check-ftd, currency, excl-other,
                        INPUT-OUTPUT curr-sort2, OUTPUT sort1,
                        OUTPUT TABLE cust-list).

FOR EACH cust-list NO-LOCK:

    ASSIGN tmp-counter  = tmp-counter + 1.

    CREATE pqueasy.
    ASSIGN pqueasy.KEY   = 280
           pqueasy.char1 = "Guest Turnover"
           pqueasy.char3 = idFlag
           pqueasy.number1 = tmp-counter.

    IF cust-list.gastnr = ? OR
       cust-list.sales-id = ? THEN DO: /* Naufal Afthar - 04233b -> add validation to ? on sales-id*/
        ASSIGN
            pqueasy.char2 = STRING(" ") + "|" + 
                          STRING(cust-list.cust-name) + "|" +
                          STRING(cust-list.gesamtumsatz) + "|" +
                          STRING(cust-list.logiernachte) + "|" +
                          STRING(cust-list.argtumsatz) + "|" +
                          STRING(cust-list.f-b-umsatz) + "|" +
                          STRING(cust-list.sonst-umsatz) + "|" +
                          STRING(cust-list.wohnort) + "|" +
                          STRING(cust-list.plz) + "|" +
                          STRING(cust-list.land) + "|" +
                          STRING(" ") + "|" + /* Naufal Afthar - 04233b -> add validation to ? on sales-id*/
                          STRING(cust-list.ba-umsatz) + "|" +
                          STRING(cust-list.ly-rev) + "|" +
                          STRING(cust-list.region) + "|" +
                          STRING(cust-list.region1) + "|" +
                          STRING(cust-list.stayno) + "|" +
                          /*STRING(cust-list.resnr) + "|" +*/
                          STRING("0") + "|" +
                          STRING(cust-list.counter) + "|" +
                          STRING(cust-list.counterall) + "|" +
                          STRING(cust-list.resno) + "|" +
                          STRING(cust-list.reslinnr) + "|" +
                          STRING(cust-list.curr-pos) 
            .
    END.
    ELSE DO:
        ASSIGN
            pqueasy.char2 = STRING(cust-list.gastnr) + "|" + 
                              STRING(cust-list.cust-name) + "|" +
                              STRING(cust-list.gesamtumsatz) + "|" +
                              STRING(cust-list.logiernachte) + "|" +
                              STRING(cust-list.argtumsatz) + "|" +
                              STRING(cust-list.f-b-umsatz) + "|" +
                              STRING(cust-list.sonst-umsatz) + "|" +
                              STRING(cust-list.wohnort) + "|" +
                              STRING(cust-list.plz) + "|" +
                              STRING(cust-list.land) + "|" +
                              STRING(cust-list.sales-id) + "|" +
                              STRING(cust-list.ba-umsatz) + "|" +
                              STRING(cust-list.ly-rev) + "|" +
                              STRING(cust-list.region) + "|" +
                              STRING(cust-list.region1) + "|" +
                              STRING(cust-list.stayno) + "|" +
                              /*STRING(cust-list.resnr) + "|" +*/
                              STRING("0") + "|" +
                              STRING(cust-list.counter) + "|" +
                              STRING(cust-list.counterall) + "|" +
                              STRING(cust-list.resno) + "|" +
                              STRING(cust-list.reslinnr) + "|" +
                              STRING(cust-list.curr-pos) 
            .
    END.
    RELEASE pqueasy.
END.


FIND FIRST bqueasy WHERE bqueasy.KEY = 285
    AND bqueasy.char1 = "Guest Turnover"
    AND bqueasy.char2 = idFlag NO-LOCK NO-ERROR.
IF AVAILABLE bqueasy THEN DO:
    FIND CURRENT bqueasy EXCLUSIVE-LOCK.
    ASSIGN bqueasy.number1 = 0.
    FIND CURRENT bqueasy NO-LOCK.
    RELEASE bqueasy.
END.

