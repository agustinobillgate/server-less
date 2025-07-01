
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

DEFINE TEMP-TABLE t-argt-line LIKE argt-line.
DEFINE TEMP-TABLE input-list
    FIELD exc-taxserv   AS LOGICAL
    FIELD pvILanguage   AS INTEGER
    FIELD new-contrate  AS LOGICAL
    FIELD foreign-rate  AS LOGICAL
    FIELD price-decimal AS INTEGER
    FIELD fdate         AS DATE
    FIELD tdate         AS DATE
    FIELD srttype       AS INTEGER
    FIELD id-flag       AS CHARACTER
.
/*
DEFINE INPUT PARAMETER exc-taxserv     AS LOGICAL NO-UNDO.
DEFINE INPUT PARAMETER pvILanguage     AS INTEGER  NO-UNDO.
DEFINE INPUT PARAMETER new-contrate    AS LOGICAL.
DEFINE INPUT PARAMETER foreign-rate    AS LOGICAL.
DEFINE INPUT PARAMETER price-decimal   AS INT.
DEFINE INPUT PARAMETER fdate           AS DATE.
DEFINE INPUT PARAMETER tdate           AS DATE.
DEFINE INPUT PARAMETER srttype         AS INTEGER. /* add sorttype by damen 07/03/23 485054 */
*/

DEFINE INPUT PARAMETER TABLE FOR input-list.
DEFINE OUTPUT PARAMETER TABLE FOR cl-list.
DEFINE OUTPUT PARAMETER TABLE FOR currency-list.
DEFINE OUTPUT PARAMETER TABLE FOR sum-list.
DEFINE OUTPUT PARAMETER TABLE FOR s-list.
DEFINE OUTPUT PARAMETER TABLE FOR argt-list.
DEFINE OUTPUT PARAMETER done-flag      AS LOGICAL NO-UNDO INITIAL NO.

DEFINE VARIABLE exchg-rate          AS DECIMAL INITIAL 1. 
DEFINE VARIABLE frate               AS DECIMAL FORMAT ">,>>>,>>9.9999". 
DEFINE VARIABLE post-it             AS LOGICAL. 
DEFINE VARIABLE total-rev           AS DECIMAL.

DEFINE BUFFER waehrung1 FOR waehrung. 
DEFINE BUFFER cc-list FOR cl-list. 
DEFINE BUFFER bqueasy FOR queasy.

FIND FIRST input-list NO-LOCK NO-ERROR.
IF NOT AVAILABLE input-list THEN RETURN.

CREATE queasy.
ASSIGN queasy.KEY = 285
       queasy.char1 = "RRB Period"
       queasy.number1 = 1
       queasy.char2 = input-list.id-flag.
RELEASE queasy.

RUN rmrev-bdown-create-billbalance5-cldbl.p
    (input-list.exc-taxserv, input-list.pvILanguage, input-list.new-contrate, input-list.foreign-rate, 
     input-list.price-decimal, input-list.fdate, input-list.tdate, input-list.srttype, input-list.id-flag,
     OUTPUT TABLE cl-list, OUTPUT TABLE currency-list, OUTPUT TABLE sum-list, OUTPUT TABLE s-list,  OUTPUT TABLE argt-list).

FIND FIRST bqueasy WHERE bqueasy.KEY = 285
    AND bqueasy.char1 = "RRB Period"
    AND bqueasy.char2 = input-list.id-flag NO-LOCK NO-ERROR.
IF AVAILABLE bqueasy THEN DO:
    done-flag = YES.
    FIND CURRENT bqueasy EXCLUSIVE-LOCK.
    ASSIGN bqueasy.number1 = 0.
    FIND CURRENT bqueasy NO-LOCK.
    RELEASE bqueasy.
END.

