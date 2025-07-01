
DEFINE TEMP-TABLE output-list2 
  FIELD flag        AS INTEGER 
  FIELD firmen-nr   AS INTEGER FORMAT ">>>>>>>>>>"
  FIELD refNo       AS CHAR    FORMAT "x(16)" LABEL "RefNo"
  FIELD avrg-amount AS CHAR    FORMAT "x(15)"
  FIELD name        AS CHAR 
  FIELD str2        AS CHAR
  FIELD str4        AS CHAR
  FIELD fcost       AS CHAR
  FIELD name1       AS CHAR 
  FIELD zinr        AS CHAR 
  FIELD pax         AS CHAR 
  FIELD exp-rev     AS CHAR 
  FIELD curr        AS CHAR 
  FIELD loc-curr    AS CHAR 
  FIELD lodg        AS CHAR 
  FIELD bfast       AS CHAR 
  FIELD lunch       AS CHAR 
  FIELD dinner      AS CHAR 
  FIELD oth-rev     AS CHAR .

DEFINE TEMP-TABLE output-list1 LIKE output-list2.

DEF INPUT PARAMETER pvILanguage         AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER op-type          AS INTEGER.
/*0 create list, 1 design lnl, 2 print lnl, 3 print txt*/
DEFINE INPUT PARAMETER printer-nr       AS INTEGER.
DEFINE INPUT PARAMETER call-from        AS INTEGER.
DEFINE INPUT PARAMETER txt-file         AS CHAR.

DEFINE INPUT PARAMETER fr-date          AS DATE.
DEFINE INPUT PARAMETER to-date          AS DATE.
DEFINE INPUT PARAMETER disptype         AS INTEGER.
/* 1 guest type, 2 nationality, 3 source of booking, 4 segment */
DEFINE INPUT PARAMETER cardtype         AS INTEGER.
DEFINE INPUT PARAMETER stattype         AS INTEGER.
/* 0 All, 1 guaranteed, 3 tentative */

DEFINE INPUT PARAMETER rev-calc         AS INTEGER.
DEFINE INPUT PARAMETER exc-oral6PM      AS LOGICAL.
DEFINE INPUT PARAMETER excl-comp        AS LOGICAL.
DEFINE INPUT PARAMETER vhp-limited      AS LOGICAL.
DEFINE INPUT PARAMETER scin             AS LOGICAL.

DEFINE OUTPUT PARAMETER TABLE FOR output-list1.
DEFINE OUTPUT PARAMETER TABLE FOR output-list2.

/*MT
DEFINE NEW SHARED VAR vhp-limited    AS LOGICAL INIT NO.
DEFINE VARIABLE op-type AS INTEGER INITIAL 0.
DEFINE VARIABLE printer-nr AS INTEGER .
DEFINE VARIABLE call-from AS INTEGER.
DEFINE VARIABLE txt-file   AS CHAR.
DEFINE VARIABLE disptype AS INTEGER INITIAL 1 
       VIEW-AS RADIO-SET TOOLTIP "Output Sources" 
       VERTICAL RADIO-BUTTONS "&Guest Type", 1, "&Nationality", 2, 
       "&Source of Booking", 3 SIZE 20 BY 2.9. 
 
DEFINE VARIABLE cardtype AS INTEGER INITIAL 1 
       VIEW-AS RADIO-SET TOOLTIP "Type of Guest File" 
       VERTICAL RADIO-BUTTONS "&Individual", 0, "&Company", 1, 
       "&Travel Agent", 2, "&ALL", 3  SIZE 20 BY 2.9. 

 
DEFINE VARIABLE stattype AS INTEGER INITIAL 0 
       VIEW-AS RADIO-SET TOOLTIP "Status of Reservation" 
       VERTICAL RADIO-BUTTONS "G&uaranteed", 1, "T&entative", 3, 
       "A&LL", 0 SIZE 15 BY 2.9. 

DEFINE VARIABLE rev-calc         AS INTEGER INITIAL 0. /* 0 Room Rev, 1 Arrangement Rev*/
DEFINE VARIABLE exc-oral6PM      AS LOGICAL INITIAL NO.
DEFINE VARIABLE fr-date          AS DATE  INITIAL 03/11/13.
DEFINE VARIABLE to-date          AS DATE  INITIAL 03/11/13.
RUN add-persist-procedure. 
PROCEDURE add-persist-procedure: 
    DEFINE VARIABLE lvHS AS HANDLE              NO-UNDO. 
    DEFINE VARIABLE lvI AS INTEGER              NO-UNDO. 
    DEFINE VARIABLE lFound AS LOGICAL INIT FALSE    NO-UNDO. 
 
    DO lvI = 1 TO NUM-ENTRIES(SESSION:SUPER-PROCEDURES): 
        lvHS = WIDGET-HANDLE(ENTRY(lvI, SESSION:SUPER-PROCEDURES)). 
        IF VALID-HANDLE(lvHS) THEN DO: 
            IF lvHS:NAME BEGINS "supertrans" THEN 
                lFound = TRUE. 
        END. 
    END. 
 
    IF NOT lFound THEN DO: 
        RUN supertrans.p PERSISTENT SET lvHS. 
        SESSION:ADD-SUPER-PROCEDURE(lvHS). 
    END. 
END. 
DEFINE NEW SHARED VARIABLE LnLDelimeter AS CHAR.
LnLDelimeter = CHR(2).
DEFINE NEW SHARED TEMP-TABLE output-list2 
  FIELD flag        AS INTEGER 
  FIELD firmen-nr   AS INTEGER FORMAT ">>>>>>>>>>"
  FIELD refNo       AS CHAR    FORMAT "x(16)" LABEL "RefNo"
  FIELD avrg-amount AS CHAR    FORMAT "x(9)"
  FIELD name        AS CHAR 
  FIELD str2        AS CHAR
  FIELD str4        AS CHAR.
DEFINE NEW SHARED TEMP-TABLE output-list1 LIKE output-list2.
*/

{ supertransbl.i } 
DEF VAR lvCAREA AS CHAR INITIAL "rm-fproduct". 

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
    .

DEFINE TEMP-TABLE to-list 
  FIELD nationnr         AS INTEGER
  FIELD sob              AS INTEGER
  FIELD resnr            AS INTEGER
  FIELD gastnr           AS INTEGER
  FIELD firmen-nr        AS INTEGER
  FIELD refNo            AS CHAR
  FIELD name             AS CHAR FORMAT "x(24)" 
 
  FIELD room             AS INTEGER FORMAT ">>9" INITIAL 0 
  FIELD pax              AS INTEGER FORMAT ">>9" INITIAL 0 
  FIELD zipreis          AS DECIMAL FORMAT ">,>>>,>>9.99" INITIAL 0       /* Expected Rev */
  
  FIELD curr             AS CHAR    FORMAT "x(3)" INITIAL ""
  FIELD logis            AS DECIMAL FORMAT ">>,>>>,>>9" INITIAL 0         /* In Local Currency */
  FIELD rmonly           AS DECIMAL FORMAT ">>,>>>,>>>,>>9.99" INITIAL 0  /* Lodging */
  FIELD bfast            AS DECIMAL FORMAT ">,>>>,>>>,>>9.99" INITIAL 0
  FIELD lunch            AS DECIMAL FORMAT ">,>>>,>>>,>>9.99" INITIAL 0
  FIELD dinner           AS DECIMAL FORMAT ">,>>>,>>>,>>9.99" INITIAL 0
  FIELD misc             AS DECIMAL FORMAT ">,>>>,>>>,>>9.99" INITIAL 0
  FIELD proz             AS DECIMAL FORMAT ">>9.99" INITIAL 0 
  FIELD avrgrate         AS DECIMAL FORMAT ">>>,>>>,>>9"
  FIELD guest-nationnr   AS INTEGER

  /* Add by Michael for Sol Beach Benoa request per segment */
  FIELD segmentcode       AS INT
  FIELD segmentbez        AS CHAR
  /* End of add */
  FIELD fcost             AS DECIMAL
 . 
 
DEFINE TEMP-TABLE tot-list
  FIELD curr       AS CHAR FORMAT "x(3)"
  FIELD zipreis    AS DECIMAL FORMAT ">,>>>,>>9.99" INITIAL 0
  FIELD room       AS INTEGER FORMAT ">>9"
  FIELD pax        AS INTEGER FORMAT ">>9"
  FIELD logis      AS DECIMAL FORMAT ">>9"
  FIELD rmonly     AS DECIMAL FORMAT ">>,>>>,>>>,>>9.99" INITIAL 0
  FIELD bfast      AS DECIMAL FORMAT ">,>>>,>>>,>>9.99" INITIAL 0
  FIELD lunch      AS DECIMAL FORMAT ">,>>>,>>>,>>9.99" INITIAL 0
  FIELD dinner     AS DECIMAL FORMAT ">,>>>,>>>,>>9.99" INITIAL 0
  FIELD misc       AS DECIMAL FORMAT ">,>>>,>>>,>>9.99" INITIAL 0
  FIELD proz       AS DECIMAL FORMAT ">>9.99" INITIAL 0 
  FIELD fcost      AS DECIMAL FORMAT ">,>>>,>>>,>>9.99" INITIAL 0 .


DEFINE STREAM s1.

DEF VAR report-title AS CHAR.

DEF VAR tot-room     AS INT.
DEF VAR tot-pax      AS INT.
DEF VAR tot-logis    AS DECIMAL.
DEF VAR tot-bfast    AS DECIMAL.
DEF VAR tot-lunch    AS DECIMAL.
DEF VAR tot-dinner   AS DECIMAL.
DEF VAR tot-misc     AS DECIMAL.
DEF VAR tot-rmonly   AS DECIMAL.
DEF VAR tot-zipreis  AS DECIMAL INITIAL 0.
DEF VAR tot-fcost    AS DECIMAL INITIAL 0.


/****************** MAIN LOGIC ******************/
RUN create-forecast-history_1bl.p(fr-date, to-date, excl-comp,vhp-limited, scin, OUTPUT TABLE t-list).
CASE op-type:
    WHEN 0 THEN
    DO:
        RUN query-to-list.
        FOR EACH to-list: 
            IF to-list.room NE 0 THEN 
              to-list.avrgrate = to-list.logis / to-list.room. 
            IF tot-logis NE 0 THEN 
              to-list.proz = to-list.logis / tot-logis * 100.
        END. 
        RUN create-tot-list.
        RUN create-browse.
    END.
    /*
    WHEN 1 THEN
    DO:
        RUN design-lnl.
    END.
    WHEN 2 THEN
    DO:
        RUN print-lnl.
    END.
    WHEN 3 THEN
    DO:
        RUN print-txt.
    END.
    WHEN 4 THEN
        RUN clear-shared1.
    */
END.

/****************** PROCEDURE ******************/
PROCEDURE query-to-list:
    FOR EACH to-list:
        DELETE to-list.
    END.

    FIND FIRST t-list WHERE t-list.flag-history NO-LOCK NO-ERROR.
    IF AVAILABLE t-list THEN
    DO: 
        /*FOR EACH t-list WHERE t-list.flag-history BY t-list.rsv-name:
            IF disptype EQ 1 AND cardtype NE 3 THEN DO:
                RUN create-to-list1.
            END.
            ELSE RUN create-to-list2.
        END.*/
        
        /*ITA 051216*/
        /* display by guest type and not all cardtype */
            IF disptype EQ 1 AND cardtype NE 3 THEN
            DO: 
                IF stattype = 0 THEN        /* all status*/
                FOR EACH t-list WHERE t-list.flag-history AND 
                    t-list.rsv-karteityp = cardtype BY t-list.rsv-name:
                    RUN create-to-list1.
                END.
        
                ELSE IF stattype = 1 THEN      /* guaranteed status*/
                FOR EACH t-list WHERE t-list.flag-history AND 
                    t-list.rsv-karteityp = cardtype 
                    AND t-list.resstatus NE 3 BY t-list.rsv-name:
                    RUN create-to-list1.
                END.
        
                ELSE IF stattype = 3 THEN      /* tentative status*/
                FOR EACH t-list WHERE t-list.flag-history AND 
                    t-list.rsv-karteityp = cardtype 
                    AND t-list.resstatus EQ 3 BY t-list.rsv-name:
                    RUN create-to-list1.
                END.
            END.
            /* display by nationality or sob or all guest type*/
            ELSE
            DO: 
                IF stattype = 0 THEN        /* all status */
                FOR EACH t-list WHERE t-list.flag-history BY t-list.rsv-name:
                    RUN create-to-list2.
                END.
        
                ELSE IF stattype = 1 THEN   /* guaranteed status */
                FOR EACH t-list WHERE t-list.flag-history AND 
                    t-list.resstatus NE 3 BY t-list.rsv-name:
                    RUN create-to-list2.
                END.
        
                ELSE IF stattype = 3 THEN   /* tentative status */
                FOR EACH t-list WHERE t-list.flag-history AND 
                    t-list.resstatus EQ 3 BY t-list.rsv-name:
                    RUN create-to-list2.
                END.
            END.

    END.
    
    /* display by guest type and not all cardtype */
    IF disptype EQ 1 AND cardtype NE 3 THEN
    DO: 
        IF stattype = 0 THEN        /* all status*/
        FOR EACH t-list WHERE NOT t-list.flag-history AND 
            t-list.rsv-karteityp = cardtype BY t-list.rsv-name:
            RUN create-to-list1.
        END.

        ELSE IF stattype = 1 THEN      /* guaranteed status*/
        FOR EACH t-list WHERE NOT t-list.flag-history AND 
            t-list.rsv-karteityp = cardtype 
            AND t-list.resstatus NE 3 BY t-list.rsv-name:
            RUN create-to-list1.
        END.

        ELSE IF stattype = 3 THEN      /* tentative status*/
        FOR EACH t-list WHERE NOT t-list.flag-history AND 
            t-list.rsv-karteityp = cardtype 
            AND t-list.resstatus EQ 3 BY t-list.rsv-name:
            RUN create-to-list1.
        END.
    END.
    /* display by nationality or sob or all guest type*/
    ELSE
    DO: 
        IF stattype = 0 THEN        /* all status */
        FOR EACH t-list WHERE NOT t-list.flag-history BY t-list.rsv-name:
            RUN create-to-list2.
        END.

        ELSE IF stattype = 1 THEN   /* guaranteed status */
        FOR EACH t-list WHERE NOT t-list.flag-history AND 
            t-list.resstatus NE 3 BY t-list.rsv-name:
            RUN create-to-list2.
        END.

        ELSE IF stattype = 3 THEN   /* tentative status */
        FOR EACH t-list WHERE NOT t-list.flag-history AND 
            t-list.resstatus EQ 3 BY t-list.rsv-name:
            RUN create-to-list2.
        END.
    END.
END.

PROCEDURE create-to-list1:
    FIND FIRST to-list WHERE to-list.name = t-list.rsv-name
        AND to-list.curr = t-list.currency
        NO-LOCK NO-ERROR.
    IF NOT AVAILABLE to-list THEN
    DO: 
        CREATE to-list.
        ASSIGN to-list.firmen-nr  = t-list.firmen-nr
               to-list.refNo      = t-list.steuernr
               to-list.name       = t-list.rsv-name
               to-list.curr       = t-list.currency
               to-list.resnr      = t-list.resnr.
    END.
    RUN assign-to-list.
END.

PROCEDURE create-to-list2:
    IF disptype EQ 1 THEN   /* disp by guest */
    FIND FIRST to-list WHERE to-list.name = t-list.rsv-name
        AND to-list.curr = t-list.currency
        NO-LOCK NO-ERROR.

    ELSE IF disptype EQ 2 THEN   /* disp by nationality */
    FIND FIRST to-list WHERE /*to-list.nationnr = t-list.rsv-nationnr*/
        to-list.guest-nationnr = t-list.guest-nationnr
        AND to-list.curr = t-list.currency NO-LOCK NO-ERROR.

    ELSE IF disptype EQ 3 THEN   /* disp by sob */
    FIND FIRST to-list WHERE to-list.sob = t-list.sob
        AND to-list.curr = t-list.currency NO-LOCK NO-ERROR.

     /* Add by Michael for Sol Beach Benoa request per Segment - ticket no 3D424D */
    ELSE IF disptype EQ 4 THEN   /* disp by segment */
    FIND FIRST to-list WHERE /*to-list.nationnr = t-list.rsv-nationnr*/
        to-list.segmentcode = t-list.segmentcode
        AND to-list.curr = t-list.currency NO-LOCK NO-ERROR.
    /* End of add */

    IF NOT AVAILABLE to-list THEN
    DO: 
        CREATE to-list.
        ASSIGN to-list.name       = t-list.rsv-name
               to-list.nationnr   = t-list.rsv-nationnr
               to-list.sob        = t-list.sob
               to-list.curr       = t-list.currency
               to-list.firmen-nr  = t-list.firmen-nr
               to-list.refNo      = t-list.steuernr
               to-list.resnr      = t-list.resnr
               to-list.guest-nationnr = t-list.guest-nationnr
               to-list.segmentcode = t-list.segmentcode /* Add by Michael for Sol Beach Benoa request per Segment - ticket no 3D424D */
            .

        IF disptype EQ 2 THEN
        DO:
            /*
            IF t-list.rsv-nationnr NE 999 THEN
            DO:
                FIND FIRST nation WHERE nation.nationnr = t-list.rsv-nationnr NO-ERROR.
                IF nation.bezeich MATCHES(";") THEN ASSIGN to-list.NAME = ENTRY(1, nation.bezeich, ";").
                ELSE ASSIGN to-list.name = nation.bezeich.
            END.
            ELSE ASSIGN to-list.name = "UNKNOWN".*/

            IF t-list.guest-nationnr NE 999 THEN
            DO:
                FIND FIRST nation WHERE nation.nationnr = t-list.guest-nationnr NO-ERROR.
                IF nation.bezeich MATCHES(";") THEN ASSIGN to-list.NAME = ENTRY(1, nation.bezeich, ";").
                ELSE ASSIGN to-list.name = nation.bezeich.
            END.
            ELSE ASSIGN to-list.name = "UNKNOWN".
        END.
        ELSE IF disptype EQ 3 THEN
        DO:
            IF t-list.sob NE 999 THEN
            DO:
                FIND FIRST sourccod WHERE sourccod.source-code = t-list.sob.
                ASSIGN to-list.name = sourccod.bezeich.
            END.
            ELSE ASSIGN to-list.name = "UNKNOWN".
        END.
        ELSE IF disptype EQ 4 THEN
        DO:
            IF t-list.segmentcode GT 0 THEN
            DO:
                FIND FIRST segment WHERE segment.segmentcode = t-list.segmentcode NO-ERROR.
                IF AVAILABLE segment THEN ASSIGN to-list.NAME = segment.bezeich.
                ELSE ASSIGN to-list.NAME = "UNKNOWN".
            END.
            ELSE ASSIGN to-list.NAME = "UNKNOWN".
        END.
    END.

    RUN assign-to-list.
END.

PROCEDURE assign-to-list:
    IF NOT t-list.flag-history THEN
    DO: 
        IF stattype = 1 THEN        /* guaranteed */
        DO: 
            IF t-list.resstatus NE 3 THEN
            DO: 
                ASSIGN
                    to-list.bfast   = to-list.bfast   + t-list.bfast-guaranteed  
                    to-list.lunch   = to-list.lunch   + t-list.lunch-guaranteed  
                    to-list.dinner  = to-list.dinner  + t-list.dinner-guaranteed 
                    to-list.misc    = to-list.misc    + t-list.misc-guaranteed   
                    to-list.room    = to-list.room    + t-list.room-guaranteed   
                    to-list.pax     = to-list.pax     + t-list.pax-guaranteed    
                    to-list.rmonly  = to-list.rmonly  + t-list.logis-guaranteed  
                    to-list.logis   = to-list.logis   + t-list.logis-guaranteed + t-list.bfast-guaranteed + t-list.lunch-guaranteed  
                                    + t-list.dinner-guaranteed + t-list.misc-guaranteed                    
                    to-list.zipreis = to-list.zipreis + t-list.zipreis
                    to-list.fcost   = to-list.fcost   + t-list.fcost.
            END.
        END.
        ELSE IF stattype = 3 THEN   /* tentative */
        DO: 
            IF t-list.resstatus = 3 THEN
            DO:
                ASSIGN
                    to-list.bfast   = to-list.bfast   + t-list.bfast-tentative
                    to-list.lunch   = to-list.lunch   + t-list.lunch-tentative
                    to-list.dinner  = to-list.dinner  + t-list.dinner-tentative
                    to-list.misc    = to-list.misc    + t-list.misc-tentative
                    to-list.room    = to-list.room    + t-list.room-tentative
                    to-list.pax     = to-list.pax     + t-list.pax-tentative
                    to-list.rmonly  = to-list.rmonly  + t-list.logis-tentative
                    to-list.logis   = to-list.logis   + t-list.logis-tentative + t-list.bfast-tentative + t-list.lunch-tentative 
                                    + t-list.dinner-tentative + t-list.misc-tentative                     
                    to-list.zipreis = to-list.zipreis + t-list.zipreis
                    to-list.fcost   = to-list.fcost   + t-list.fcost.
            END.
        END.
        ELSE IF stattype = 0 THEN   /* all */ /*01/08/16*/
        DO:
            ASSIGN
                to-list.bfast   = to-list.bfast   + t-list.bfast-guaranteed  + t-list.bfast-tentative
                to-list.lunch   = to-list.lunch   + t-list.lunch-guaranteed  + t-list.lunch-tentative
                to-list.dinner  = to-list.dinner  + t-list.dinner-guaranteed + t-list.dinner-tentative
                to-list.misc    = to-list.misc    + t-list.misc-guaranteed   + t-list.misc-tentative
                to-list.room    = to-list.room    + t-list.room-guaranteed   + t-list.room-tentative
                to-list.pax     = to-list.pax     + t-list.pax-guaranteed    + t-list.pax-tentative
                to-list.rmonly  = to-list.rmonly  + t-list.logis-guaranteed  + t-list.logis-tentative
                to-list.logis   = to-list.logis   + t-list.logis-guaranteed  + t-list.logis-tentative + t-list.bfast-guaranteed  + t-list.bfast-tentative + t-list.lunch-guaranteed 
                                + t-list.lunch-tentative + t-list.dinner-guaranteed + t-list.dinner-tentative + t-list.misc-tentative + t-list.misc-guaranteed                
                to-list.zipreis = to-list.zipreis + t-list.zipreis
                to-list.fcost   = to-list.fcost   + t-list.fcost.
        END.
    END.
    ELSE
    DO: 
        ASSIGN
            to-list.bfast   = to-list.bfast   + t-list.bfast-guaranteed  
            to-list.lunch   = to-list.lunch   + t-list.lunch-guaranteed  
            to-list.dinner  = to-list.dinner  + t-list.dinner-guaranteed 
            to-list.misc    = to-list.misc    + t-list.misc-guaranteed   
            to-list.room    = to-list.room    + t-list.room-guaranteed
            to-list.pax     = to-list.pax     + t-list.pax-guaranteed    
            to-list.rmonly  = to-list.rmonly  + t-list.logis-guaranteed  
            to-list.logis   = to-list.logis   + t-list.logis-guaranteed + t-list.bfast-guaranteed + t-list.lunch-guaranteed 
                            + t-list.dinner-guaranteed + t-list.misc-guaranteed           
            to-list.zipreis = to-list.zipreis + t-list.zipreis
            to-list.fcost   = to-list.fcost   + t-list.fcost. 

    END.
END.

PROCEDURE create-tot-list:

    FOR EACH tot-list:
        DELETE tot-list.
    END.

    FOR EACH to-list:
        FIND FIRST tot-list WHERE tot-list.curr = to-list.curr
            NO-LOCK NO-ERROR.
        IF NOT AVAILABLE tot-list THEN
        DO:
            CREATE tot-list.
            ASSIGN tot-list.curr = to-list.curr.
        END.
        ASSIGN tot-list.logis   = tot-list.logis   + to-list.logis
               tot-list.zipreis = tot-list.zipreis + to-list.zipreis
               tot-list.rmonly  = tot-list.rmonly  + to-list.rmonly
               tot-list.bfast   = tot-list.bfast   + to-list.bfast
               tot-list.lunch   = tot-list.lunch   + to-list.lunch
               tot-list.dinner  = tot-list.dinner  + to-list.dinner
               tot-list.misc    = tot-list.misc    + to-list.misc
               tot-list.proz    = tot-list.proz    + to-list.proz
               tot-list.room    = tot-list.room    + to-list.room
               tot-list.pax     = tot-list.pax     + to-list.pax
               tot-list.fcost   = tot-list.fcost   + to-list.fcost
               tot-room         = tot-room + to-list.room
               tot-pax          = tot-pax  + to-list.pax
               tot-logis        = tot-logis + to-list.logis
               tot-bfast        = tot-bfast + to-list.bfast
               tot-lunch        = tot-lunch + to-list.lunch
               tot-dinner       = tot-dinner + to-list.dinner
               tot-misc         = tot-misc + to-list.misc
               tot-rmonly       = tot-rmonly + to-list.rmonly
               tot-zipreis      = tot-zipreis + to-list.zipreis
               tot-fcost        = tot-fcost + to-list.fcost.
    END.

END.

PROCEDURE create-browse:
    FOR EACH output-list1:
        DELETE output-list1.
    END.
    
    FOR EACH output-list2:
        DELETE output-list2.
    END.

    
    IF rev-calc = 1 THEN
    DO:
        FOR EACH to-list:            
            CREATE output-list1.
            ASSIGN 
              output-list1.firmen-nr = to-list.firmen-nr
              output-list1.refNo = to-list.refNo
              /*output-list1.str2 = STRING(to-list.name, "x(32)")
                + STRING(to-list.room, ">>,>>9")           /*38*/
                + STRING(to-list.pax, ">>,>>9")            /*44*/
                + STRING(to-list.zipreis, ">>>,>>>,>>>,>>9.99")
                + STRING(to-list.curr, "x(4)")
                + STRING(to-list.logis, ">>>,>>>,>>>,>>9.99") /*62*/
                + STRING(to-list.rmonly, ">>,>>>,>>>,>>9.99") /*79*/
                + STRING(to-list.bfast, ">,>>>,>>>,>>9.99") /*95*/
                + STRING(to-list.lunch, ">,>>>,>>>,>>9.99") /*111*/
                + STRING(to-list.dinner, ">,>>>,>>>,>>9.99") /*127*/
                + STRING(to-list.misc, ">,>>>,>>>,>>9.99")   /*143*/ */
              output-list1.avrg-amount  = STRING(to-list.rmonly / to-list.room, "->>>,>>>,>>9.99")
              output-list1.fcost        = STRING(to-list.fcost, "->>>,>>>,>>9.99") 
              output-list1.name1        = STRING(to-list.name, "x(32)")
              output-list1.zinr         = STRING(to-list.room, ">>,>>9")
              output-list1.pax          = STRING(to-list.pax, ">>,>>9")
              output-list1.exp-rev      = STRING(to-list.zipreis, ">>>,>>>,>>>,>>9.99")
              output-list1.curr         = STRING(to-list.curr, "x(4)")
              output-list1.loc-curr     = STRING(to-list.logis, ">>>,>>>,>>>,>>9.99")
              output-list1.lodg         = STRING(to-list.rmonly, ">>,>>>,>>>,>>9.99")
              output-list1.bfast        = STRING(to-list.bfast, ">,>>>,>>>,>>9.99")
              output-list1.lunch        = STRING(to-list.lunch, ">,>>>,>>>,>>9.99")
              output-list1.dinner       = STRING(to-list.dinner, ">,>>>,>>>,>>9.99")
              output-list1.oth-rev      = STRING(to-list.misc, ">,>>>,>>>,>>9.99").
              
        END.

        CREATE output-list1.
        output-list1.avrg-amount = FILL("-", 15).
        output-list1.fcost       = FILL("-", 15).
        output-list1.name1       = FILL("-", 32).
        output-list1.zinr        = FILL("-", 6).
        output-list1.pax         = FILL("-", 6).
        output-list1.exp-rev     = FILL("-", 18).
        output-list1.curr        = FILL("-", 4).
        output-list1.loc-curr    = FILL("-", 18).
        output-list1.lodg        = FILL("-", 17).
        output-list1.bfast       = FILL("-", 16).
        output-list1.lunch       = FILL("-", 16).
        output-list1.dinner      = FILL("-", 16).
        output-list1.oth-rev     = FILL("-", 16).

        FOR EACH tot-list BY tot-list.curr:
            /*create output-list1. 
            output-list1.str2        = FILL("-", 167). 
            output-list1.avrg-amount = FILL("-", 14).
            output-list1.fcost       = FILL("-", 15).*/
            
            create output-list1. 
            ASSIGN
              /*output-list1.str2 = STRING("T o t a l  " + tot-list.curr, "x(32)") 
                + STRING(tot-list.room, ">>,>>9") 
                + STRING(tot-list.pax, ">>,>>9") 
                + STRING(tot-list.zipreis, ">>>,>>>,>>>,>>9.99")
                + "    "
                + STRING(tot-list.logis, ">>>,>>>,>>>,>>9.99") /*62*/
                + STRING(tot-list.rmonly, ">>,>>>,>>>,>>9.99")  /* Expected RmRev */ 
                + STRING(tot-list.bfast, ">,>>>,>>>,>>9.99") 
                + STRING(tot-list.lunch, ">,>>>,>>>,>>9.99") 
                + STRING(tot-list.dinner, ">,>>>,>>>,>>9.99") 
                + STRING(tot-list.misc, ">,>>>,>>>,>>9.99")*/
              output-list1.avrg-amount  = STRING(tot-list.rmonly / tot-list.room,"->>>,>>>,>>9.99")
              output-list1.fcost        = STRING(tot-list.fcost, "->>>,>>>,>>9.99")
              output-list1.name1        = STRING("T o t a l  " + tot-list.curr, "x(32)")
              output-list1.zinr         = STRING(tot-list.room, ">>,>>9")                 
              output-list1.pax          = STRING(tot-list.pax, ">>,>>9")                  
              output-list1.exp-rev      = STRING(tot-list.zipreis, ">>>,>>>,>>>,>>9.99")  
              output-list1.curr         = "    "                                          
              output-list1.loc-curr     = STRING(tot-list.logis, ">>>,>>>,>>>,>>9.99")
              output-list1.lodg         = STRING(tot-list.rmonly, ">>,>>>,>>>,>>9.99")
              output-list1.bfast        = STRING(tot-list.bfast, ">,>>>,>>>,>>9.99")  
              output-list1.lunch        = STRING(tot-list.lunch, ">,>>>,>>>,>>9.99")  
              output-list1.dinner       = STRING(tot-list.dinner, ">,>>>,>>>,>>9.99") 
              output-list1.oth-rev      = STRING(tot-list.misc, ">,>>>,>>>,>>9.99"). 
        END.

        /*create output-list1. 
        output-list1.str2        = FILL("-", 167).
        output-list1.avrg-amount = FILL("-", 14).
        output-list1.fcost       = FILL("-", 15).*/

        CREATE output-list1.
        output-list1.avrg-amount = FILL("-", 15).
        output-list1.fcost       = FILL("-", 15).
        output-list1.name1       = FILL("-", 32).
        output-list1.zinr        = FILL("-", 6).
        output-list1.pax         = FILL("-", 6).
        output-list1.exp-rev     = FILL("-", 18).
        output-list1.curr        = FILL("-", 4).
        output-list1.loc-curr    = FILL("-", 18).
        output-list1.lodg        = FILL("-", 17).
        output-list1.bfast       = FILL("-", 16).
        output-list1.lunch       = FILL("-", 16).
        output-list1.dinner      = FILL("-", 16).
        output-list1.oth-rev     = FILL("-", 16).

        create output-list1. 
        ASSIGN
          /*output-list1.str2 = STRING("T o t a l", "x(32)") 
            + STRING(tot-room, ">>,>>9") 
            + STRING(tot-pax, ">>,>>9") 
            /*+ STRING(tot-zipreis, ">>>,>>>,>>>,>>9.99")*/
            + "                  "
            + "    "
            + STRING(tot-logis, ">>>,>>>,>>>,>>9.99") /*62*/
            + STRING(tot-rmonly, ">>,>>>,>>>,>>9.99")  /* Expected RmRev */ 
            + STRING(tot-bfast, ">,>>>,>>>,>>9.99") 
            + STRING(tot-lunch, ">,>>>,>>>,>>9.99") 
            + STRING(tot-dinner, ">,>>>,>>>,>>9.99") 
            + STRING(tot-misc, ">,>>>,>>>,>>9.99")   */
          output-list1.avrg-amount  = STRING(tot-rmonly / tot-room,"->>>,>>>,>>9.99")
          output-list1.fcost        = STRING(tot-fcost, "->>>,>>>,>>9.99")
          output-list1.name1        = STRING("T o t a l", "x(32)") 
          output-list1.zinr         = STRING(tot-room, ">>,>>9") 
          output-list1.pax          = STRING(tot-pax, ">>,>>9")  
          output-list1.exp-rev      = "                  "                   
          output-list1.curr         = "    "                                 
          output-list1.loc-curr     = STRING(tot-logis, ">>>,>>>,>>>,>>9.99")
          output-list1.lodg         = STRING(tot-rmonly, ">>,>>>,>>>,>>9.99")
          output-list1.bfast        = STRING(tot-bfast, ">,>>>,>>>,>>9.99")  
          output-list1.lunch        = STRING(tot-lunch, ">,>>>,>>>,>>9.99")  
          output-list1.dinner       = STRING(tot-dinner, ">,>>>,>>>,>>9.99") 
          output-list1.oth-rev      = STRING(tot-misc, ">,>>>,>>>,>>9.99").  
    END.
    ELSE
    DO:
        FOR EACH to-list:                   
            CREATE output-list2.
            ASSIGN
                output-list2.firmen-nr = to-list.firmen-nr
                output-list2.refNo = to-list.refNo
                /*output-list2.str2 = STRING(to-list.name, "x(32)")
                  + STRING(to-list.room, ">>,>>9")             /*39*/
                  + STRING(to-list.pax, ">>,>>9")              /*44*/
                  + STRING(to-list.zipreis, ">>>,>>>,>>>,>>9.99") /*62*/
                  + STRING(to-list.curr, "x(4)")
                  + STRING(to-list.logis, ">>>,>>>,>>>,>>9.99")*/
                output-list2.avrg-amount    = STRING(to-list.rmonly / to-list.room,"->>>,>>>,>>9.99")
                output-list2.fcost          = STRING(to-list.fcost, "->>>,>>>,>>9.99")
                output-list2.name1          = STRING(to-list.name, "x(32)")
                output-list2.zinr           = STRING(to-list.room, ">>,>>9")                
                output-list2.pax            = STRING(to-list.pax, ">>,>>9")                 
                output-list2.exp-rev        = STRING(to-list.zipreis, ">>>,>>>,>>>,>>9.99")  
                output-list2.curr           = STRING(to-list.curr, "x(4)")                         
                output-list2.loc-curr       = STRING(to-list.logis, ">>>,>>>,>>>,>>9.99") 
                output-list2.lodg           = STRING(to-list.rmonly, ">>,>>>,>>>,>>9.99").         
        END.
        
        CREATE output-list2.
        output-list2.avrg-amount    = FILL("-", 15).
        output-list2.fcost          = FILL("-", 15).
        output-list2.name1          = FILL("-", 32).
        output-list2.zinr           = FILL("-", 6).
        output-list2.pax            = FILL("-", 6).
        output-list2.exp-rev        = FILL("-", 18).
        output-list2.curr           = FILL("-", 4).
        output-list2.loc-curr       = FILL("-", 18).
        output-list2.lodg           = FILL("-", 17).

        FOR EACH tot-list BY tot-list.curr:
            /*create output-list2. 
            output-list2.str2        = FILL("-", 84). 
            output-list2.str4        = FILL("-", 110). 
            output-list2.avrg-amount = FILL("-", 14).
            output-list2.fcost       = FILL("-", 15).*/
                        
            create output-list2. 
            ASSIGN
              /*output-list2.str2 = STRING("T o t a l  " + tot-list.curr, "x(32)") 
                + STRING(tot-list.room, ">>,>>9") 
                + STRING(tot-list.pax, ">>,>>9") 
                + STRING(tot-list.zipreis, ">>>,>>>,>>>,>>9.99")
                + "    "
                + STRING(tot-list.logis, ">>>,>>>,>>>,>>9.99") /*62*/
                /*+ STRING(rmonly, ">>,>>>,>>>,>>9.99")  /* Expected RmRev */ 
                + STRING(bfast, ">,>>>,>>>,>>9.99") 
                + STRING(lunch, ">,>>>,>>>,>>9.99") 
                + STRING(dinner, ">,>>>,>>>,>>9.99") 
                + STRING(misc, ">,>>>,>>>,>>9.99")   */ */
              output-list2.avrg-amount  = STRING(tot-list.rmonly / tot-list.room,"->>>,>>>,>>9.99")
              output-list2.fcost        = STRING(tot-list.fcost, "->>>,>>>,>>9.99")
              output-list2.name1        = STRING("T o t a l  " + tot-list.curr, "x(32)")
              output-list2.zinr         = STRING(tot-list.room, ">>,>>9")                             
              output-list2.pax          = STRING(tot-list.pax, ">>,>>9")                              
              output-list2.exp-rev      = STRING(tot-list.zipreis, ">>>,>>>,>>>,>>9.99")              
              output-list2.curr         = "    "                                                      
              output-list2.loc-curr     = STRING(tot-list.logis, ">>>,>>>,>>>,>>9.99")
              output-list2.lodg         = STRING(tot-list.rmonly, ">>,>>>,>>>,>>9.99").       
        END.
        /*create output-list2. 
        output-list2.str2        = FILL("-", 84). 
        output-list2.str4        = FILL("-", 110). 
        output-list2.avrg-amount = FILL("-", 14).
        output-list2.fcost       = FILL("-", 15).*/
        
        CREATE output-list2.
        output-list2.avrg-amount    = FILL("-", 15).
        output-list2.fcost          = FILL("-", 15).
        output-list2.name1          = FILL("-", 32).
        output-list2.zinr           = FILL("-", 6).
        output-list2.pax            = FILL("-", 6).
        output-list2.exp-rev        = FILL("-", 18).
        output-list2.curr           = FILL("-", 4).
        output-list2.loc-curr       = FILL("-", 18).
        output-list2.lodg           = FILL("-", 17).

        create output-list2. 
        ASSIGN
          /*output-list2.str2 = STRING("T o t a l", "x(32)") 
            + STRING(tot-room, ">>,>>9") 
            + STRING(tot-pax, ">>,>>9") 
            /*+ STRING(tot-zipreis, ">>>,>>>,>>>,>>9.99")  /* Expected RmRev */ */
            + "                  "
            + "    "
            + STRING(tot-logis, ">>>,>>>,>>>,>>9.99")*/
          output-list2.avrg-amount  = STRING(tot-rmonly / tot-room, "->>>,>>>,>>9.99")
          output-list2.fcost        = STRING(tot-fcost, "->>>,>>>,>>9.99")
          output-list2.name1        = STRING("T o t a l", "x(32)") 
          output-list2.zinr         = STRING(tot-room, ">>,>>9")    
          output-list2.pax          = STRING(tot-pax, ">>,>>9")     
          output-list2.exp-rev      = "                  "                        
          output-list2.curr         = "    "                                      
          output-list2.loc-curr     = STRING(tot-logis, ">>>,>>>,>>>,>>9.99")
          output-list2.lodg         = STRING(tot-rmonly, ">>,>>>,>>>,>>9.99").   
    END.
END.
