DEFINE TEMP-TABLE fcasthist-detail-list 
    FIELD flag                AS INTEGER   
    FIELD res-number          AS CHARACTER
    FIELD display-value       AS CHARACTER
    FIELD avrg-roomrev        AS CHAR    
    FIELD reserve-name        AS CHAR 
    FIELD guest-name          AS CHAR    
    FIELD pax                 AS INT
    FIELD room                AS INT   
    FIELD expected-revenue    AS CHAR 
    FIELD currency            AS CHAR 
    FIELD total-revenue       AS CHAR 
    FIELD room-revenue        AS CHAR 
    FIELD bfast-amount        AS CHAR 
    FIELD lunch-amount        AS CHAR 
    FIELD dinneramount        AS CHAR 
    FIELD other-revenue       AS CHAR 
    FIELD fix-cost            AS CHAR
    .

DEFINE TEMP-TABLE t-list
    FIELD resnr AS INT
    FIELD reslinnr AS INT
    FIELD logis-guaranteed  AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99"
    FIELD bfast-guaranteed  AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99"
    FIELD lunch-guaranteed  AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99"
    FIELD dinner-guaranteed AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99"
    FIELD misc-guaranteed   AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99"
    FIELD pax-guaranteed    AS INT
    FIELD room-guaranteed   AS INT

    FIELD logis-tentative   AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99"
    FIELD bfast-tentative   AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99"
    FIELD lunch-tentative   AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99"
    FIELD dinner-tentative  AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99"
    FIELD misc-tentative    AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99"
    FIELD pax-tentative     AS INT
    FIELD room-tentative    AS INT

    FIELD rsv-karteityp     AS INT
    FIELD rsv-name          AS CHAR
    FIELD rsv-nationnr      AS INT

    FIELD guest-karteityp   AS INT
    FIELD guest-name        AS CHAR
    FIELD guest-nationnr    AS INT

    FIELD sob               AS INT
    FIELD resstatus         AS INT
    FIELD currency          AS CHAR
    FIELD zipreis           AS DECIMAL
    FIELD flag-history      AS LOGICAL INIT NO

    FIELD firmen-nr         AS INT
    FIELD steuernr          LIKE guest.steuernr

    /* Add by Michael for Sol Beach Benoa request per segment */
    FIELD segmentcode       AS INT
    FIELD segmentbez        AS CHAR
    /* End of add */
    FIELD fcost             AS DECIMAL
    /* add by damen 15/05/23  DCB8A3*/
    FIELD argtcode          AS CHARACTER
    FIELD argtbez           AS CHARACTER
    .

DEFINE INPUT PARAMETER v-key            AS CHARACTER.   /*SOB;NATION;GUEST;SEGMENT;ARGT etc*/
DEFINE INPUT PARAMETER v-value          AS CHARACTER.
DEFINE INPUT PARAMETER cardtype         AS INTEGER.
DEFINE INPUT PARAMETER stattype         AS INTEGER.
DEFINE INPUT PARAMETER fr-date          AS DATE.
DEFINE INPUT PARAMETER to-date          AS DATE.
DEFINE INPUT PARAMETER excl-comp        AS LOGICAL.
DEFINE INPUT PARAMETER vhp-limited      AS LOGICAL.
DEFINE INPUT PARAMETER scin             AS LOGICAL.
DEFINE OUTPUT PARAMETER TABLE FOR fcasthist-detail-list.

DEFINE VARIABLE qh AS HANDLE.

DEFINE VARIABLE query-string    AS CHARACTER.
DEFINE VARIABLE sob-number      AS INTEGER.
DEFINE VARIABLE tot-room        AS INTEGER.
DEFINE VARIABLE tot-pax         AS INTEGER.
DEFINE VARIABLE tot-rev         AS DECIMAL.
DEFINE VARIABLE tot-expectrev   AS DECIMAL.
DEFINE VARIABLE tot-rmrev       AS DECIMAL.
DEFINE VARIABLE tot-bfast       AS DECIMAL.
DEFINE VARIABLE tot-lunch       AS DECIMAL.
DEFINE VARIABLE tot-dinner      AS DECIMAL.
DEFINE VARIABLE tot-othrev      AS DECIMAL.
DEFINE VARIABLE tot-fix-cost    AS DECIMAL.


RUN create-forecast-history-detail-cldbl.p(fr-date, to-date, excl-comp,vhp-limited, scin, OUTPUT TABLE t-list).

IF v-key EQ "SOB" THEN
DO:
    FIND FIRST sourccod WHERE sourccod.bezeich EQ v-value NO-LOCK NO-ERROR.
    IF AVAILABLE sourccod THEN sob-number = sourccod.source-code.

    IF stattype EQ 0 THEN query-string = "FOR EACH t-list WHERE t-list.sob EQ " + STRING(sob-number) + "NO-LOCK BY t-list.guest-name:".
    ELSE IF stattype EQ 1 THEN query-string = "FOR EACH t-list WHERE t-list.sob EQ " + STRING(sob-number) + " AND t-list.resstatus NE 3 NO-LOCK BY t-list.guest-name:".
    ELSE IF stattype EQ 3 THEN query-string = "FOR EACH t-list WHERE t-list.sob EQ " + STRING(sob-number) + " AND t-list.resstatus EQ 3 NO-LOCK BY t-list.guest-name:".

    CREATE QUERY qh.
    qh:SET-BUFFERS(BUFFER t-list:HANDLE).
    qh:QUERY-PREPARE(query-string).
    qh:QUERY-OPEN.

    REPEAT:
        qh:GET-NEXT().
        IF NOT AVAILABLE t-list THEN LEAVE.

        CREATE fcasthist-detail-list.
        ASSIGN
            fcasthist-detail-list.res-number        = STRING(t-list.resnr) + "/" + STRING(t-list.reslinnr)
            fcasthist-detail-list.display-value     = v-value            
            fcasthist-detail-list.reserve-name      = t-list.rsv-name
            fcasthist-detail-list.guest-name        = t-list.guest-name 
            fcasthist-detail-list.currency          = t-list.currency
            .

        IF stattype EQ 0 THEN /*ALL*/
        DO:
            ASSIGN
                fcasthist-detail-list.pax               = t-list.pax-guaranteed    + t-list.pax-tentative     
                fcasthist-detail-list.room              = t-list.room-guaranteed   + t-list.room-tentative
                fcasthist-detail-list.expected-revenue  = STRING(t-list.zipreis, "->>,>>>,>>>,>>>,>>9.99")                
                fcasthist-detail-list.total-revenue     = STRING(t-list.logis-guaranteed  + t-list.logis-tentative + t-list.bfast-guaranteed + t-list.bfast-tentative 
                                                        + t-list.lunch-guaranteed + t-list.lunch-tentative + t-list.dinner-guaranteed + t-list.dinner-tentative 
                                                        + t-list.misc-tentative + t-list.misc-guaranteed, "->>,>>>,>>>,>>>,>>9.99")
                fcasthist-detail-list.room-revenue      = STRING(t-list.logis-guaranteed  + t-list.logis-tentative, "->>,>>>,>>>,>>>,>>9.99")
                fcasthist-detail-list.bfast-amount      = STRING(t-list.bfast-guaranteed  + t-list.bfast-tentative, "->>,>>>,>>>,>>>,>>9.99")
                fcasthist-detail-list.lunch-amount      = STRING(t-list.lunch-guaranteed  + t-list.lunch-tentative, "->>,>>>,>>>,>>>,>>9.99")
                fcasthist-detail-list.dinneramount      = STRING(t-list.dinner-guaranteed + t-list.dinner-tentative, "->>,>>>,>>>,>>>,>>9.99")
                fcasthist-detail-list.other-revenue     = STRING(t-list.misc-guaranteed   + t-list.misc-tentative, "->>,>>>,>>>,>>>,>>9.99") 
                fcasthist-detail-list.fix-cost          = STRING(t-list.fcost, "->>,>>>,>>>,>>>,>>9.99")
                .

            ASSIGN
                tot-room        = tot-room      + t-list.pax-guaranteed    + t-list.pax-tentative   
                tot-pax         = tot-pax       + t-list.room-guaranteed   + t-list.room-tentative
                tot-rev         = tot-rev       + t-list.zipreis
                tot-expectrev   = tot-expectrev + t-list.logis-guaranteed  + t-list.logis-tentative + t-list.bfast-guaranteed 
                                + t-list.bfast-tentative + t-list.lunch-guaranteed + t-list.lunch-tentative + t-list.dinner-guaranteed 
                                + t-list.dinner-tentative + t-list.misc-tentative + t-list.misc-guaranteed
                tot-rmrev       = tot-rmrev     + t-list.logis-guaranteed  + t-list.logis-tentative
                tot-bfast       = tot-bfast     + t-list.bfast-guaranteed  + t-list.bfast-tentative
                tot-lunch       = tot-lunch     + t-list.lunch-guaranteed  + t-list.lunch-tentative
                tot-dinner      = tot-dinner    + t-list.dinner-guaranteed + t-list.dinner-tentative
                tot-othrev      = tot-othrev    + t-list.misc-guaranteed   + t-list.misc-tentative 
                tot-fix-cost    = tot-fix-cost  + t-list.fcost
                .
        END.
        ELSE IF stattype EQ 1 THEN /*guaranteed*/
        DO:
            ASSIGN
                fcasthist-detail-list.pax               = t-list.pax-guaranteed   
                fcasthist-detail-list.room              = t-list.room-guaranteed
                fcasthist-detail-list.expected-revenue  = STRING(t-list.zipreis, "->>,>>>,>>>,>>>,>>9.99")
                fcasthist-detail-list.total-revenue     = STRING(t-list.logis-guaranteed + t-list.bfast-guaranteed + t-list.lunch-guaranteed  
                                                        + t-list.dinner-guaranteed + t-list.misc-guaranteed, "->>,>>>,>>>,>>>,>>9.99")                                                                                                         
                fcasthist-detail-list.room-revenue      = STRING(t-list.logis-guaranteed, "->>,>>>,>>>,>>>,>>9.99")
                fcasthist-detail-list.bfast-amount      = STRING(t-list.bfast-guaranteed, "->>,>>>,>>>,>>>,>>9.99") 
                fcasthist-detail-list.lunch-amount      = STRING(t-list.lunch-guaranteed, "->>,>>>,>>>,>>>,>>9.99") 
                fcasthist-detail-list.dinneramount      = STRING(t-list.dinner-guaranteed, "->>,>>>,>>>,>>>,>>9.99")
                fcasthist-detail-list.other-revenue     = STRING(t-list.misc-guaranteed, "->>,>>>,>>>,>>>,>>9.99")  
                fcasthist-detail-list.fix-cost          = STRING(t-list.fcost, "->>,>>>,>>>,>>>,>>9.99")
                .            

            ASSIGN
                tot-room        = tot-room      + t-list.pax-guaranteed 
                tot-pax         = tot-pax       + t-list.room-guaranteed
                tot-rev         = tot-rev       + t-list.zipreis
                tot-expectrev   = tot-expectrev + t-list.logis-guaranteed + t-list.bfast-guaranteed + t-list.lunch-guaranteed  
                                + t-list.dinner-guaranteed + t-list.misc-guaranteed                               
                tot-rmrev       = tot-rmrev     + t-list.logis-guaranteed
                tot-bfast       = tot-bfast     + t-list.bfast-guaranteed
                tot-lunch       = tot-lunch     + t-list.lunch-guaranteed
                tot-dinner      = tot-dinner    + t-list.dinner-guaranteed
                tot-othrev      = tot-othrev    + t-list.misc-guaranteed
                tot-fix-cost    = tot-fix-cost  + t-list.fcost
                .
        END.
        ELSE IF stattype EQ 3 THEN /*tentative*/
        DO:
            ASSIGN                                    
                fcasthist-detail-list.pax               = t-list.pax-tentative  
                fcasthist-detail-list.room              = t-list.room-tentative 
                fcasthist-detail-list.expected-revenue  = STRING(t-list.zipreis, "->>,>>>,>>>,>>>,>>9.99")
                fcasthist-detail-list.total-revenue     = STRING(t-list.logis-tentative + t-list.bfast-tentative + t-list.lunch-tentative 
                                                        + t-list.dinner-tentative + t-list.misc-tentative, "->>,>>>,>>>,>>>,>>9.99")                                                    
                fcasthist-detail-list.room-revenue      = STRING(t-list.logis-tentative, "->>,>>>,>>>,>>>,>>9.99") 
                fcasthist-detail-list.bfast-amount      = STRING(t-list.bfast-tentative, "->>,>>>,>>>,>>>,>>9.99") 
                fcasthist-detail-list.lunch-amount      = STRING(t-list.lunch-tentative, "->>,>>>,>>>,>>>,>>9.99") 
                fcasthist-detail-list.dinneramount      = STRING(t-list.dinner-tentative, "->>,>>>,>>>,>>>,>>9.99")
                fcasthist-detail-list.other-revenue     = STRING(t-list.misc-tentative, "->>,>>>,>>>,>>>,>>9.99") 
                fcasthist-detail-list.fix-cost          = STRING(t-list.fcost, "->>,>>>,>>>,>>>,>>9.99")
                .             

            ASSIGN
                tot-room        = tot-room      + t-list.pax-tentative 
                tot-pax         = tot-pax       + t-list.room-tentative
                tot-rev         = tot-rev       + t-list.zipreis
                tot-expectrev   = tot-expectrev + t-list.logis-tentative + t-list.bfast-tentative + t-list.lunch-tentative 
                                + t-list.dinner-tentative + t-list.misc-tentative                                
                tot-rmrev       = tot-rmrev     + t-list.logis-tentative
                tot-bfast       = tot-bfast     + t-list.bfast-tentative
                tot-lunch       = tot-lunch     + t-list.lunch-tentative
                tot-dinner      = tot-dinner    + t-list.dinner-tentative
                tot-othrev      = tot-othrev    + t-list.misc-tentative
                tot-fix-cost    = tot-fix-cost  + t-list.fcost
                .
        END.            
    END.
    qh:QUERY-CLOSE().
    DELETE OBJECT qh.    

    FIND FIRST fcasthist-detail-list NO-LOCK NO-ERROR.
    IF AVAILABLE fcasthist-detail-list THEN
    DO:
        CREATE fcasthist-detail-list.
        ASSIGN
            fcasthist-detail-list.reserve-name      = "T O T A L"
            fcasthist-detail-list.pax               = tot-room  
            fcasthist-detail-list.room              = tot-pax 
            fcasthist-detail-list.expected-revenue  = STRING(tot-rev      , "->>,>>>,>>>,>>>,>>9.99")
            fcasthist-detail-list.total-revenue     = STRING(tot-expectrev, "->>,>>>,>>>,>>>,>>9.99")                                               
            fcasthist-detail-list.room-revenue      = STRING(tot-rmrev    , "->>,>>>,>>>,>>>,>>9.99")
            fcasthist-detail-list.bfast-amount      = STRING(tot-bfast    , "->>,>>>,>>>,>>>,>>9.99")
            fcasthist-detail-list.lunch-amount      = STRING(tot-lunch    , "->>,>>>,>>>,>>>,>>9.99")
            fcasthist-detail-list.dinneramount      = STRING(tot-dinner   , "->>,>>>,>>>,>>>,>>9.99")
            fcasthist-detail-list.other-revenue     = STRING(tot-othrev   , "->>,>>>,>>>,>>>,>>9.99")
            fcasthist-detail-list.fix-cost          = STRING(tot-fix-cost , "->>,>>>,>>>,>>>,>>9.99")
            .
    END.
END.


             






