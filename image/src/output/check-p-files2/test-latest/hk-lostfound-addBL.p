DEF TEMP-TABLE s-list 
     FIELD nr         AS INTEGER LABEL "Number" FORMAT ">,>>>,>>9" 
     FIELD betriebsnr AS INTEGER 
     FIELD s-recid    AS INTEGER
     FIELD date1      AS DATE LABEL "Date" 
     FIELD zeit       AS CHAR FORMAT "x(8)"     LABEL "Time" 
     FIELD zinr       AS CHAR FORMAT "x(5)"     LABEL "RmNo" 
     FIELD userinit   AS CHAR FORMAT "x(3)"     LABEL "ID" 
     FIELD bezeich    AS CHAR FORMAT "x(60)"    LABEL "Description" 
     FIELD foundby    AS CHAR FORMAT "x(24)"    LABEL "Found by" 
     FIELD submitted  AS CHAR FORMAT "x(24)"    LABEL "Submitted to" 
     FIELD reportby    AS CHAR FORMAT "x(24)"    LABEL "Claimed By"
     FIELD claim-date AS DATE FORMAT "99/99/99" LABEL "ClaimedDate"
     FIELD location   AS CHAR FORMAT "x(24)"    LABEL "Location"
     FIELD refNo      AS CHAR FORMAT "x(16)"    LABEL "Reference No"
     FIELD PhoneNo    AS CHAR FORMAT "x(20)"    LABEL "Phone No"
.

DEF INPUT PARAMETER zinr        AS CHAR     NO-UNDO.
DEF INPUT PARAMETER from-date   AS DATE     NO-UNDO.
DEF INPUT PARAMETER zeit        AS CHAR     NO-UNDO.
DEF INPUT PARAMETER dept        AS INTEGER  NO-UNDO.
DEF INPUT PARAMETER reason      AS CHAR     NO-UNDO.
DEF INPUT PARAMETER reportby     AS CHAR     NO-UNDO.
DEF INPUT PARAMETER claim-date  AS DATE     NO-UNDO.
DEF INPUT PARAMETER phoneNo     AS CHAR     NO-UNDO.
DEF INPUT PARAMETER refNo       AS CHAR     NO-UNDO.
DEF INPUT PARAMETER foundby     AS CHAR     NO-UNDO.
DEF INPUT PARAMETER location    AS CHAR     NO-UNDO.
DEF INPUT PARAMETER submitted   AS CHAR     NO-UNDO.
DEF INPUT PARAMETER user-init   AS CHAR     NO-UNDO.

DEF OUTPUT PARAMETER TABLE FOR s-list.

DEF VARIABLE num AS INTEGER NO-UNDO. 
DEFINE VARIABLE claim-date-str AS CHAR NO-UNDO.

FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK.

ASSIGN
  num = INTEGER(SUBSTR(zeit,1,2)) * 3600 
      + INTEGER(SUBSTR(zeit,3,2)) * 60 + INTEGER(SUBSTR(zeit,5,2)). 

FIND FIRST counters WHERE counters.counter-no = 11 EXCLUSIVE-LOCK NO-ERROR.
IF NOT AVAILABLE counters THEN
DO:
  CREATE counters.
  ASSIGN
    counters.counter-no = 11
    counters.counter-bez = "Lost+Found Counter"
  . 
END.
counters.counter = counters.counter + 1. 
FIND CURRENT counter NO-LOCK. 
/*FDL Dec 29, 2023 => Ticket 055944*/
IF claim-date EQ ? THEN claim-date-str = "".
ELSE claim-date-str = STRING(claim-date).

CREATE queasy. 
ASSIGN
  queasy.key        = 7
  queasy.date1      = from-date 
  queasy.number1    = num
  queasy.char1      = zinr 
  queasy.number2    = bediener.nr
  queasy.char2      = reason
  queasy.betriebsnr = dept 
  queasy.number3    = counters.counter 
  foundBy           = REPLACE(foundBy, "|", "")     
  submitted         = REPLACE(submitted, "|", "")     
  reportby          = REPLACE(reportby, "|", "")     
  phoneNo           = REPLACE(phoneNo, "|", "")     
  RefNo             = REPLACE(RefNo, "|", "")     
  Location          = REPLACE(location, "|", "")
  queasy.char3      = foundby
              + "|" + submitted 
              + "|" + ENTRY(1, reportby, CHR(2))
              + "|" + STRING(claim-date-str)
              + "|" + phoneNo
              + "|" + RefNo
              + "|" + Location
.
IF NUM-ENTRIES(reportby, CHR(2)) GT 1 THEN
    queasy.char3 = queasy.char3 + "|" + "|" 
                 + "|" + ENTRY(2, reportby, CHR(2))
    .
FIND CURRENT queasy NO-LOCK. 

CREATE s-list. 
ASSIGN 
  s-list.nr         = queasy.number3 
  s-list.date1      = queasy.date1 
  s-list.zeit       = STRING(queasy.number1,"HH:MM:SS") 
  s-list.zinr       = queasy.char1 
  s-list.userinit   = bediener.userinit 
  s-list.bezeich    = queasy.char2 
  s-list.betriebsnr = queasy.betriebsnr 
  s-list.foundby    = foundby 
  s-list.submitted  = submitted 
  s-list.reportby    = reportby
  s-list.claim-date = claim-date
  s-list.s-recid    = RECID(queasy)
  s-list.phoneNo    = phoneNo
  s-list.refNo      = refNo
  s-list.location   = location
. 
