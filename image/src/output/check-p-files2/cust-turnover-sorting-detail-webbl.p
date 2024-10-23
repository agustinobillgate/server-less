DEFINE TEMP-TABLE b-list
    FIELD gastnr            LIKE guest.gastnr
    FIELD cust-name         AS CHAR    
    FIELD gname             AS CHAR
    FIELD gesamtumsatz      AS CHAR
    FIELD logiernachte      AS CHAR  
    FIELD argtumsatz        AS CHAR 
    FIELD f-b-umsatz        AS CHAR 
    FIELD sonst-umsatz      AS CHAR 
    FIELD wohnort           LIKE guest.wohnort 
    FIELD plz               LIKE guest.plz 
    FIELD land              LIKE guest.land
    FIELD sales-id          LIKE guest.phonetik3
    FIELD ba-umsatz         AS CHAR 
    FIELD ly-rev            AS CHAR 
    FIELD region            AS CHAR
    FIELD region1           AS CHAR
    FIELD stayno            AS CHAR 
    FIELD resnr             AS CHAR
    FIELD counter           AS INT
    FIELD counterall        AS INT
    FIELD resno             AS INTEGER
    FIELD reslinnr          AS INTEGER
    FIELD curr-pos          AS INTEGER
    FIELD count-room        AS CHAR
    FIELD rm-sharer         AS CHAR
    FIELD arrival           AS DATE
    FIELD depart            AS DATE
    FIELD gastnrmember      AS INTEGER
 .

DEFINE INPUT PARAMETER cardtype             AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER sort-type            AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER fdate                AS DATE    NO-UNDO.
DEFINE INPUT PARAMETER tdate                AS DATE    NO-UNDO.
DEFINE INPUT PARAMETER check-ftd            AS LOGICAL NO-UNDO.
DEFINE INPUT PARAMETER currency             AS CHAR    NO-UNDO.
DEFINE INPUT PARAMETER excl-other           AS LOGICAL NO-UNDO.
DEFINE INPUT PARAMETER curr-sort2           AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER idFlag               AS CHAR    NO-UNDO. 

DEFINE VARIABLE arrive-date AS CHAR NO-UNDO.
DEFINE VARIABLE depart-date AS CHAR NO-UNDO.
DEFINE VARIABLE counter     AS INTEGER NO-UNDO.

DEFINE BUFFER bqueasy FOR queasy.
DEFINE BUFFER pqueasy FOR queasy.

CREATE queasy.
ASSIGN queasy.KEY      = 285
       queasy.char1    = "Guest Turnover Detail"
       queasy.number1  = 1
       queasy.char2    = idFlag.
RELEASE queasy.

RUN cust-turnover-sorting-detail-cldbl.p(cardtype, sort-type, 
                        fdate, tdate,check-ftd, currency, excl-other,
                        INPUT-OUTPUT curr-sort2, OUTPUT TABLE b-list).

FOR EACH b-list NO-LOCK:
 
    CREATE pqueasy.
    ASSIGN counter          = counter + 1
           pqueasy.KEY      = 280
           pqueasy.char1    = "Guest Turnover Detail"
           pqueasy.char3    = idFlag
           pqueasy.number1  = counter
     .

    IF b-list.arrival = ? THEN ASSIGN arrive-date = "".
    ELSE ASSIGN arrive-date = STRING(b-list.arrival).

    IF b-list.depart = ? THEN ASSIGN depart-date = "".
    ELSE ASSIGN depart-date = STRING(b-list.depart).


    IF b-list.gastnr = ? THEN DO:
        ASSIGN
            pqueasy.char2 = STRING(" ") + "|" + 
                            STRING(b-list.cust-name) + "|" +
                            STRING(b-list.gesamtumsatz) + "|" +
                            STRING(b-list.logiernachte) + "|" +
                            STRING(b-list.argtumsatz) + "|" +
                            STRING(b-list.f-b-umsatz) + "|" +
                            STRING(b-list.sonst-umsatz) + "|" +
                            STRING(b-list.wohnort) + "|" +
                            STRING(b-list.plz) + "|" +
                            STRING(b-list.land) + "|" +
                            STRING(b-list.sales-id) + "|" +
                            STRING(b-list.ba-umsatz) + "|" +
                            STRING(b-list.ly-rev) + "|" +
                            STRING(b-list.region) + "|" +
                            STRING(b-list.region1) + "|" +
                            STRING(b-list.stayno) + "|" +
                            /*STRING(cust-list.resnr) + "|" +*/
                            STRING("0") + "|" +
                            STRING(b-list.counter) + "|" +
                            STRING(b-list.counterall) + "|" +
                            STRING(b-list.resno) + "|" +
                            STRING(b-list.reslinnr) + "|" +
                            STRING(b-list.curr-pos) + "|" +
                            STRING(b-list.count-room) + "|" +
                            STRING(b-list.rm-sharer) + "|" +
                            STRING(arrive-date) + "|" +
                            STRING(depart-date).

    END.
    ELSE IF b-list.gastnr = ? AND b-list.cust-name = " " THEN DO:
        ASSIGN
            pqueasy.char2 = STRING(" ") + "|" + 
                            STRING("") + "|" +
                            STRING("") + "|" +
                            STRING("") + "|" +
                            STRING("") + "|" +
                            STRING("") + "|" +
                            STRING("") + "|" +
                            STRING("") + "|" +
                            STRING("") + "|" +
                            STRING("") + "|" +
                            STRING("") + "|" +
                            STRING("") + "|" +
                            STRING("") + "|" +
                            STRING("") + "|" +
                            STRING("") + "|" +
                            STRING("") + "|" +
                            STRING("") + "|" +
                            STRING("") + "|" +
                            STRING("") + "|" +
                            STRING("") + "|" +
                            STRING("") + "|" +
                            STRING("") + "|" +
                            STRING("") + "|" +
                            STRING("") + "|" +
                            STRING("") + "|" +
                            STRING("").
    END.
    ELSE DO:
        ASSIGN
            pqueasy.char2 = STRING(b-list.gastnr) + "|" + 
                            STRING(b-list.cust-name) + "|" +
                            STRING(b-list.gesamtumsatz) + "|" +
                            STRING(b-list.logiernachte) + "|" +
                            STRING(b-list.argtumsatz) + "|" +
                            STRING(b-list.f-b-umsatz) + "|" +
                            STRING(b-list.sonst-umsatz) + "|" +
                            STRING(b-list.wohnort) + "|" +
                            STRING(b-list.plz) + "|" +
                            STRING(b-list.land) + "|" +
                            STRING(b-list.sales-id) + "|" +
                            STRING(b-list.ba-umsatz) + "|" +
                            STRING(b-list.ly-rev) + "|" +
                            STRING(b-list.region) + "|" +
                            STRING(b-list.region1) + "|" +
                            STRING(b-list.stayno) + "|" +
                            /*STRING(cust-list.resnr) + "|" +*/
                            STRING("0") + "|" +
                            STRING(b-list.counter) + "|" +
                            STRING(b-list.counterall) + "|" +
                            STRING(b-list.resno) + "|" +
                            STRING(b-list.reslinnr) + "|" +
                            STRING(b-list.curr-pos) + "|" +
                            STRING(b-list.count-room) + "|" +
                            STRING(b-list.rm-sharer) + "|" +
                            STRING(arrive-date) + "|" +
                            STRING(depart-date).

    END.           
    RELEASE pqueasy.
END.


FIND FIRST bqueasy WHERE bqueasy.KEY = 285
    AND bqueasy.char1 = "Guest Turnover Detail"
    AND bqueasy.char2 = idFlag NO-LOCK NO-ERROR.
IF AVAILABLE bqueasy THEN DO:
    FIND CURRENT bqueasy EXCLUSIVE-LOCK.
    ASSIGN bqueasy.number1 = 0.
    FIND CURRENT bqueasy NO-LOCK.
    RELEASE bqueasy.
END.


