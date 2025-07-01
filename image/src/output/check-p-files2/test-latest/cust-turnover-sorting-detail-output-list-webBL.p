DEFINE TEMP-TABLE b-list
    FIELD gastnr            LIKE guest.gastnr
    FIELD cust-name         AS CHAR    
    FIELD gname             AS CHAR
    FIELD gesamtumsatz      AS DECIMAL
    FIELD logiernachte      AS DECIMAL  
    FIELD argtumsatz        AS DECIMAL 
    FIELD f-b-umsatz        AS DECIMAL 
    FIELD sonst-umsatz      AS DECIMAL 
    FIELD wohnort           LIKE guest.wohnort 
    FIELD plz               LIKE guest.plz 
    FIELD land              LIKE guest.land
    FIELD sales-id          LIKE guest.phonetik3
    FIELD ba-umsatz         AS DECIMAL 
    FIELD ly-rev            AS DECIMAL 
    FIELD region            AS CHAR
    FIELD region1           AS CHAR
    FIELD stayno            AS INTEGER 
    FIELD resnr             AS CHAR
    FIELD counter           AS INT
    FIELD counterall        AS INT
    FIELD resno             AS INTEGER
    FIELD reslinnr          AS INTEGER
    FIELD curr-pos          AS INTEGER
    FIELD count-room        AS CHAR
    FIELD rm-sharer         AS CHAR
    FIELD arrival           AS CHAR
    FIELD depart            AS CHAR
 .


DEFINE INPUT PARAMETER idFlag       AS CHAR.
DEFINE OUTPUT PARAMETER doneFlag    AS LOGICAL NO-UNDO INITIAL NO.
DEFINE INPUT-OUTPUT PARAMETER TABLE FOR b-list.


DEFINE VARIABLE counter   AS INTEGER NO-UNDO INITIAL 0.
DEFINE BUFFER bqueasy FOR queasy.
DEFINE BUFFER pqueasy FOR queasy.
DEFINE BUFFER tqueasy FOR queasy.

FOR EACH queasy WHERE queasy.KEY = 280 AND queasy.char1 = "Guest Turnover Detail" 
    AND queasy.char3 = idFlag NO-LOCK BY queasy.number1:
    
     ASSIGN counter = counter + 1.
     IF counter GT 1000 THEN LEAVE.

     CREATE b-list.
     ASSIGN  
        b-list.gastnr        = INTEGER(ENTRY(1, queasy.char2, "|"))
        b-list.cust-name     = ENTRY(2, queasy.char2, "|")
        b-list.gesamtumsatz  = DECIMAL(ENTRY(3, queasy.char2, "|"))
        b-list.logiernachte  = DECIMAL(ENTRY(4, queasy.char2, "|"))
        b-list.argtumsatz    = DECIMAL(ENTRY(5, queasy.char2, "|"))
        b-list.f-b-umsatz    = DECIMAL(ENTRY(6, queasy.char2, "|"))
        b-list.sonst-umsatz  = DECIMAL(ENTRY(7, queasy.char2, "|"))
        b-list.wohnort       = ENTRY(8, queasy.char2, "|")
        b-list.plz           = ENTRY(9, queasy.char2, "|")
        b-list.land          = ENTRY(10, queasy.char2, "|")
        b-list.sales-id      = ENTRY(11, queasy.char2, "|")
        b-list.ba-umsatz     = DECIMAL(ENTRY(12, queasy.char2, "|"))
        b-list.ly-rev        = DECIMAL(ENTRY(13, queasy.char2, "|"))
        b-list.region        = ENTRY(14, queasy.char2, "|")
        b-list.region1       = ENTRY(15, queasy.char2, "|")
        b-list.stayno        = INTEGER(ENTRY(16, queasy.char2, "|"))
        b-list.resnr         = ENTRY(17, queasy.char2, "|")
        b-list.counter       = INTEGER(ENTRY(18, queasy.char2, "|"))
        b-list.counterall    = INTEGER(ENTRY(19, queasy.char2, "|"))
        b-list.resno         = INTEGER(ENTRY(20, queasy.char2, "|"))
        b-list.reslinnr      = INTEGER(ENTRY(21, queasy.char2, "|"))
        b-list.curr-pos      = INTEGER(ENTRY(22, queasy.char2, "|"))
        b-list.count-room    = ENTRY(23, queasy.char2, "|")
        b-list.rm-sharer     = ENTRY(24, queasy.char2, "|")
        b-list.arrival       = ENTRY(25, queasy.char2, "|")
        b-list.depart        = ENTRY(26, queasy.char2, "|")
     .
    
     FIND FIRST bqueasy WHERE RECID(bqueasy) = RECID(queasy) EXCLUSIVE-LOCK.
     DELETE bqueasy.
     RELEASE bqueasy.
END.


FIND FIRST pqueasy WHERE pqueasy.KEY = 280 
    AND pqueasy.char1 = "Guest Turnover Detail"
    AND pqueasy.char3 = idFlag NO-LOCK NO-ERROR.
IF AVAILABLE pqueasy THEN DO:
    ASSIGN doneFlag = NO.
END.
ELSE DO:
    FIND FIRST tqueasy WHERE tqueasy.KEY = 285 
        AND tqueasy.char1 = "Guest Turnover Detail" 
        AND tqueasy.number1 = 1
        AND tqueasy.char2 = idFlag NO-LOCK NO-ERROR.
    IF AVAILABLE tqueasy THEN DO:
        ASSIGN doneFlag = NO.
    END.
    ELSE DO: 
        ASSIGN doneFlag = YES.
    END.
END.

FIND FIRST tqueasy WHERE tqueasy.KEY = 285 
      AND tqueasy.char1 = "Guest Turnover Detail" 
      AND tqueasy.number1 = 0
      AND tqueasy.char2 = idFlag NO-LOCK NO-ERROR.
IF AVAILABLE tqueasy THEN DO:
    FIND CURRENT tqueasy EXCLUSIVE-LOCK.
    DELETE tqueasy.
    RELEASE tqueasy.
END.


