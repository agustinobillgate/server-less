
DEFINE TEMP-TABLE sum-list 
  FIELD bezeich    AS CHAR FORMAT "x(27)" INITIAL "In Local Currency" 
  FIELD pax        AS INTEGER 
  FIELD adult      AS INTEGER INITIAL 0 COLUMN-LABEL "Adult"
  FIELD ch1        AS INTEGER INITIAL 0 COLUMN-LABEL "Ch1"
  FIELD ch2        AS INTEGER INITIAL 0 COLUMN-LABEL "Ch2"
  FIELD comch      AS INTEGER INITIAL 0 COLUMN-LABEL "ComCh"
  FIELD com        AS INTEGER FORMAT ">>9" 
  FIELD lodging    AS DECIMAL 
  FIELD bfast      AS DECIMAL 
  FIELD lunch      AS DECIMAL 
  FIELD dinner     AS DECIMAL 
  FIELD misc       AS DECIMAL 
  FIELD fixcost    AS DECIMAL 
  FIELD t-rev      AS DECIMAL
. 

DEFINE TEMP-TABLE currency-list 
  FIELD code AS CHAR
. 

DEFINE TEMP-TABLE cl-list 
  FIELD zipreis    AS DECIMAL FORMAT ">>>,>>>,>>>,>>9.99" COLUMN-LABEL "Room Rate"     
  FIELD localrate  AS DECIMAL FORMAT ">>,>>>,>>>,>>>,>>9" COLUMN-LABEL "Local Currency"
  FIELD lodging    AS DECIMAL FORMAT ">>>,>>>,>>>,>>9.99" COLUMN-LABEL "Lodging"       
  FIELD bfast      AS DECIMAL FORMAT ">>,>>>,>>>,>>9.99" COLUMN-LABEL "Breakfast"      
  FIELD lunch      AS DECIMAL FORMAT ">>,>>>,>>>,>>9.99" COLUMN-LABEL "Lunch"          
  FIELD dinner     AS DECIMAL FORMAT ">>,>>>,>>>,>>9.99" COLUMN-LABEL "Dinner"         
  FIELD misc       AS DECIMAL FORMAT "->,>>>,>>>,>>9.99" COLUMN-LABEL "Other Rev"      
  FIELD fixcost    AS DECIMAL FORMAT "->>>,>>>,>>9.99" COLUMN-LABEL "FixCost"          
  FIELD t-rev      AS DECIMAL FORMAT ">>>,>>>,>>>,>>9.99" COLUMN-LABEL "Total Rate"    
 
  FIELD c-zipreis    AS CHAR FORMAT "x(18)" LABEL "         Room Rate" 
  FIELD c-localrate  AS CHAR FORMAT "x(18)" LABEL "    Local Currency" 
  FIELD c-lodging    AS CHAR FORMAT "x(18)" LABEL "           Lodging" 
  FIELD c-bfast      AS CHAR FORMAT "x(17)" LABEL "        Breakfast" 
  FIELD c-lunch      AS CHAR FORMAT "x(17)" LABEL "            Lunch" 
  FIELD c-dinner     AS CHAR FORMAT "x(17)" LABEL "           Dinner" 
  FIELD c-misc       AS CHAR FORMAT "x(17)" LABEL "        Other Rev" 
  FIELD c-fixcost    AS CHAR FORMAT "x(15)" LABEL "        FixCost"   
  FIELD ct-rev       AS CHAR FORMAT "x(18)" LABEL "        Total Rate" 
 
  FIELD res-recid  AS INTEGER 
  FIELD sleeping   AS LOGICAL INITIAL YES 
  FIELD row-disp   AS INTEGER INITIAL 0 
  FIELD flag       AS CHAR 
  FIELD zinr       LIKE zimmer.zinr 
  FIELD rstatus    AS INTEGER 
  FIELD argt       AS CHAR FORMAT "x(5)" COLUMN-LABEL "Argt" 
  FIELD currency   AS CHAR FORMAT "x(4)" COLUMN-LABEL "Curr" 
  FIELD ratecode   AS CHAR FORMAT "x(4)" COLUMN-LABEL "RCode"
  FIELD pax        AS INTEGER FORMAT ">>,>>>"        COLUMN-LABEL "Pax" 
  FIELD com        AS INTEGER FORMAT ">>,>>>"        COLUMN-LABEL "Com" 
  FIELD ankunft    AS DATE                           COLUMN-LABEL "Arrival" 
  FIELD abreise    AS DATE                           COLUMN-LABEL "Depart" 
  FIELD rechnr     AS INTEGER FORMAT ">>>>>>>"       COLUMN-LABEL "BillNum" 
  FIELD name       LIKE res-line.name FORMAT "x(19)" COLUMN-LABEL "Guest Name" 
  FIELD ex-rate    AS CHAR FORMAT "x(9)"             COLUMN-LABEL "   ExRate"
  FIELD fix-rate   AS CHAR FORMAT "x(1)"             COLUMN-LABEL "F"
  
  FIELD adult      AS INTEGER INITIAL 0 COLUMN-LABEL "Adult"
  FIELD ch1        AS INTEGER INITIAL 0 COLUMN-LABEL "Ch1"
  FIELD ch2        AS INTEGER INITIAL 0 COLUMN-LABEL "Ch2"
  FIELD comch      AS INTEGER INITIAL 0 COLUMN-LABEL "ComCh"
  
  FIELD age1       AS INTEGER INITIAL 0 COLUMN-LABEL "Age"
  FIELD age2       AS CHAR FORMAT "x(10)" COLUMN-LABEL "Age"
  
  FIELD rmtype     AS CHAR FORMAT "x(6)" COLUMN-LABEL "RmType"
  
  FIELD resnr      LIKE res-line.resnr COLUMN-LABEL "Resnr" 
  FIELD resname    LIKE res-line.resname    COLUMN-LABEL "Reserve Name" 
  FIELD segm-desc  AS CHARACTER
  FIELD nation     AS CHARACTER
. 
 
DEFINE TEMP-TABLE s-list 
  FIELD artnr AS INTEGER 
  FIELD dept AS INTEGER 
  FIELD bezeich  AS CHAR FORMAT "x(24)" 
  FIELD curr AS CHAR FORMAT "x(4)" 
  FIELD anzahl AS INTEGER FORMAT ">>>>9" INITIAL 0 
  FIELD betrag AS DECIMAL FORMAT "->,>>>,>>>,>>9.99" INITIAL 0 
  FIELD l-betrag AS DECIMAL FORMAT "->,>>>,>>>,>>9.99" INITIAL 0 
  FIELD f-betrag AS DECIMAL FORMAT "->>>,>>9.99" INITIAL 0
. 

DEFINE TEMP-TABLE argt-list
  FIELD argtnr    AS INTEGER
  FIELD argtcode  AS CHARACTER
  FIELD bezeich   AS CHAR
  FIELD room      AS INTEGER
  FIELD pax       AS INTEGER
  FIELD qty       AS INTEGER
  FIELD bfast     AS DECIMAL
.

DEFINE INPUT PARAMETER id-flag    AS CHARACTER.
DEFINE OUTPUT PARAMETER TABLE FOR cl-list.
DEFINE OUTPUT PARAMETER TABLE FOR currency-list.
DEFINE OUTPUT PARAMETER TABLE FOR sum-list.
DEFINE OUTPUT PARAMETER TABLE FOR s-list.
DEFINE OUTPUT PARAMETER TABLE FOR argt-list.
DEFINE OUTPUT PARAMETER done-flag    AS LOGICAL NO-UNDO INITIAL NO.


DEFINE VARIABLE tbl-name   AS CHARACTER.
DEFINE VARIABLE counter   AS INTEGER NO-UNDO INITIAL 0.
DEFINE BUFFER bqueasy FOR queasy.
DEFINE BUFFER pqueasy FOR queasy.
DEFINE BUFFER tqueasy FOR queasy.
/*
DEF VAR id-flag         AS CHARACTER.
id-flag = "1Q2W3E!q@w#e".
 */
FOR EACH queasy WHERE queasy.KEY EQ 280 AND queasy.char1 EQ "RRB Period"
    AND queasy.char2 EQ id-flag NO-LOCK BY queasy.number1:
        tbl-name = ENTRY(1, queasy.char3, "|").
        counter = counter + 1.
        IF counter GT 500 THEN LEAVE.

        IF tbl-name EQ "cl-list" THEN 
        DO:
            CREATE cl-list.
            ASSIGN 
                cl-list.zipreis     = DECIMAL(ENTRY(2, queasy.char3, "|"))
                cl-list.localrate   = DECIMAL(ENTRY(3, queasy.char3, "|"))
                cl-list.lodging     = DECIMAL(ENTRY(4, queasy.char3, "|"))
                cl-list.bfast       = DECIMAL(ENTRY(5, queasy.char3, "|"))
                cl-list.lunch       = DECIMAL(ENTRY(6, queasy.char3, "|"))
                cl-list.dinner      = DECIMAL(ENTRY(7, queasy.char3, "|"))
                cl-list.misc        = DECIMAL(ENTRY(8, queasy.char3, "|"))
                cl-list.fixcost     = DECIMAL(ENTRY(9, queasy.char3, "|"))
                cl-list.t-rev       = DECIMAL(ENTRY(10, queasy.char3, "|"))

                cl-list.c-zipreis   = ENTRY(11, queasy.char3, "|")
                cl-list.c-localrate = ENTRY(12, queasy.char3, "|")
                cl-list.c-lodging   = ENTRY(13, queasy.char3, "|")
                cl-list.c-bfast     = ENTRY(14, queasy.char3, "|")
                cl-list.c-lunch     = ENTRY(15, queasy.char3, "|")
                cl-list.c-dinner    = ENTRY(16, queasy.char3, "|")
                cl-list.c-misc      = ENTRY(17, queasy.char3, "|")
                cl-list.c-fixcost   = ENTRY(18, queasy.char3, "|")
                cl-list.ct-rev      = ENTRY(19, queasy.char3, "|")

                cl-list.res-recid   = INTEGER(ENTRY(20, queasy.char3, "|"))
                cl-list.sleeping    = ENTRY(21, queasy.char3, "|") EQ "YES"
                cl-list.row-disp    = INTEGER(ENTRY(22, queasy.char3, "|"))
                cl-list.flag        = ENTRY(23, queasy.char3, "|")
                cl-list.zinr        = ENTRY(24, queasy.char3, "|")
                cl-list.rstatus     = INTEGER(ENTRY(25, queasy.char3, "|"))
                cl-list.argt        = ENTRY(26, queasy.char3, "|")
                cl-list.currency    = ENTRY(27, queasy.char3, "|")
                cl-list.ratecode    = ENTRY(28, queasy.char3, "|")
                cl-list.pax         = INTEGER(ENTRY(29, queasy.char3, "|"))
                cl-list.com         = INTEGER(ENTRY(30, queasy.char3, "|"))
                cl-list.ankunft     = DATE(ENTRY(31, queasy.char3, "|"))
                cl-list.abreise     = DATE(ENTRY(32, queasy.char3, "|"))
                cl-list.rechnr      = INTEGER(ENTRY(33, queasy.char3, "|"))
                cl-list.name        = ENTRY(34, queasy.char3, "|")
                cl-list.ex-rate     = ENTRY(35, queasy.char3, "|")
                cl-list.fix-rate    = ENTRY(36, queasy.char3, "|")
                cl-list.adult       = INTEGER(ENTRY(37, queasy.char3, "|"))
                cl-list.ch1         = INTEGER(ENTRY(38, queasy.char3, "|"))
                cl-list.ch2         = INTEGER(ENTRY(39, queasy.char3, "|"))
                cl-list.comch       = INTEGER(ENTRY(40, queasy.char3, "|"))
                cl-list.age1        = INTEGER(ENTRY(41, queasy.char3, "|"))
                cl-list.age2        = ENTRY(42, queasy.char3, "|")
                cl-list.rmtype      = ENTRY(43, queasy.char3, "|")
                cl-list.resnr       = INTEGER(ENTRY(44, queasy.char3, "|"))
                cl-list.resname     = ENTRY(45, queasy.char3, "|")
                cl-list.segm-desc   = ENTRY(46, queasy.char3, "|")
                cl-list.nation      = ENTRY(47, queasy.char3, "|")
            .
        END.
        ELSE IF tbl-name EQ "sum-list" THEN
        DO:
            CREATE sum-list.
            ASSIGN 
                sum-list.bezeich    = ENTRY(2, queasy.char3, "|")
                sum-list.pax        = INTEGER(ENTRY(3, queasy.char3, "|"))
                sum-list.adult      = INTEGER(ENTRY(4, queasy.char3, "|"))
                sum-list.ch1        = INTEGER(ENTRY(5, queasy.char3, "|"))
                sum-list.ch2        = INTEGER(ENTRY(6, queasy.char3, "|"))
                sum-list.comch      = INTEGER(ENTRY(7, queasy.char3, "|"))
                sum-list.com        = INTEGER(ENTRY(8, queasy.char3, "|"))
                sum-list.lodging    = DECIMAL(ENTRY(9, queasy.char3, "|"))
                sum-list.bfast      = DECIMAL(ENTRY(10, queasy.char3, "|"))
                sum-list.lunch      = DECIMAL(ENTRY(11, queasy.char3, "|"))
                sum-list.dinner     = DECIMAL(ENTRY(12, queasy.char3, "|"))
                sum-list.misc       = DECIMAL(ENTRY(13, queasy.char3, "|"))
                sum-list.fixcost    = DECIMAL(ENTRY(14, queasy.char3, "|"))
                sum-list.t-rev      = DECIMAL(ENTRY(15, queasy.char3, "|"))
            .
        END.
        ELSE IF tbl-name EQ "currency-list" THEN 
        DO:
            CREATE currency-list.
            ASSIGN 
                currency-list.code = ENTRY(2, queasy.char3, "|")
            .
        END.
        ELSE IF tbl-name EQ "s-list" THEN
        DO:
            CREATE s-list.
            ASSIGN 
                s-list.artnr   = INTEGER(ENTRY(2, queasy.char3, "|"))
                s-list.dept    = INTEGER(ENTRY(3, queasy.char3, "|"))
                s-list.bezeich = ENTRY(4, queasy.char3, "|")
                s-list.curr    = ENTRY(5, queasy.char3, "|")
                s-list.anzahl  = INTEGER(ENTRY(6, queasy.char3, "|"))
                s-list.betrag  = DECIMAL(ENTRY(7, queasy.char3, "|"))
                s-list.l-betrag= DECIMAL(ENTRY(8, queasy.char3, "|"))
                s-list.f-betrag= DECIMAL(ENTRY(9, queasy.char3, "|"))
            .
        END.
        ELSE IF tbl-name EQ "argt-list" THEN 
        DO:
            CREATE argt-list.
            ASSIGN 
                argt-list.argtnr    = INTEGER(ENTRY(2, queasy.char3, "|"))
                argt-list.argtcode  = ENTRY(3, queasy.char3, "|")
                argt-list.bezeich   = ENTRY(4, queasy.char3, "|")
                argt-list.room      = INTEGER(ENTRY(5, queasy.char3, "|"))
                argt-list.pax       = INTEGER(ENTRY(6, queasy.char3, "|"))
                argt-list.qty       = INTEGER(ENTRY(7, queasy.char3, "|"))
                argt-list.bfast     = DECIMAL(ENTRY(8, queasy.char3, "|"))
            .
        END.

        FIND FIRST bqueasy WHERE RECID(bqueasy) EQ RECID(queasy) EXCLUSIVE-LOCK.
        DELETE bqueasy.
        RELEASE bqueasy. 
END. 

FIND FIRST pqueasy WHERE pqueasy.KEY = 280
    AND pqueasy.char1 EQ "RRB Period"
    AND pqueasy.char2 EQ id-flag NO-LOCK NO-ERROR.
IF AVAILABLE pqueasy THEN DO:
    ASSIGN done-flag = NO.
END.
ELSE DO:
    FIND FIRST tqueasy WHERE tqueasy.KEY = 285
        AND tqueasy.char1 = "RRB Period"
        AND tqueasy.number1 = 1
        AND tqueasy.char2 = id-flag NO-LOCK NO-ERROR.
    IF AVAILABLE tqueasy THEN DO:
        ASSIGN done-flag = NO.
    END.
    ELSE DO:
        ASSIGN done-flag = YES.
    END.
END.

FIND FIRST tqueasy WHERE tqueasy.KEY = 285
    AND tqueasy.char1 = "RRB Period"
    AND tqueasy.number1 = 0
    AND tqueasy.char2 = id-flag NO-LOCK NO-ERROR.
IF AVAILABLE tqueasy THEN DO:
    FIND CURRENT tqueasy EXCLUSIVE-LOCK.
    DELETE tqueasy.
    RELEASE tqueasy.
END.



