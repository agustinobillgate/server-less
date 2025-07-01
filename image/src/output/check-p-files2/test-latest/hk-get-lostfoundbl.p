
DEF TEMP-TABLE s-list 
     FIELD nr         AS INTEGER LABEL "Number" FORMAT ">,>>>,>>9" 
     FIELD betriebsnr AS INTEGER 
     FIELD s-recid    AS INTEGER
     FIELD date1      AS DATE LABEL "Date" 
     FIELD zeit       AS CHAR FORMAT "x(8)"     LABEL "Time" 
     FIELD zinr       AS CHAR FORMAT "x(5)"     LABEL "RmNo" 
     FIELD userinit   AS CHAR FORMAT "x(3)"     LABEL "ID" 
     FIELD bezeich    AS CHAR FORMAT "x(32)"    LABEL "Description" 
     FIELD foundby    AS CHAR FORMAT "x(24)"    LABEL "Found by" 
     FIELD submitted  AS CHAR FORMAT "x(24)"    LABEL "Submitted to" 
     FIELD reportBy   AS CHAR FORMAT "x(24)"    LABEL "Claimed By"
     FIELD report-date AS DATE FORMAT "99/99/99" LABEL "ClaimedDate"
     FIELD location   AS CHAR FORMAT "x(24)"    LABEL "Location"
     FIELD refNo      AS CHAR FORMAT "x(16)"    LABEL "Reference No"
     FIELD PhoneNo    AS CHAR FORMAT "x(20)"    LABEL "Phone No"
     FIELD claimBy    AS CHAR FORMAT "x(24)"    LABEL "Claimed By"  
     FIELD claim-date AS DATE FORMAT "99/99/99" LABEL "ClaimDate"  
     FIELD expired    AS DATE FORMAT "99/99/99" LABEL "Expired"     
     FIELD bemerk     AS CHAR FORMAT "x(32)"    LABEL "remark"
.

DEFINE INPUT PARAMETER comments  AS CHAR NO-UNDO.
DEFINE INPUT PARAMETER sorttype  AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER fr-date   AS DATE NO-UNDO.
DEFINE INPUT PARAMETER to-date   AS DATE NO-UNDO.
DEFINE OUTPUT PARAMETER TABLE FOR s-list.

IF comments EQ ? THEN 
DO:
  comments = "".
END.

RUN hk-lostfound_1bl.p(1, comments, sorttype, fr-date,
                     to-date,"",?, OUTPUT TABLE s-list).
