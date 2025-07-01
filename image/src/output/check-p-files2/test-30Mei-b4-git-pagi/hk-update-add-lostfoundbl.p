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
     FIELD claimby    AS CHAR FORMAT "x(24)"    LABEL "Claimed By"
     FIELD claim-date AS DATE FORMAT "99/99/99" LABEL "ClaimedDate"
     FIELD location   AS CHAR FORMAT "x(24)"    LABEL "Location"
     FIELD refno      AS CHAR FORMAT "x(16)"    LABEL "Reference No"
     FIELD PhoneNo    AS CHAR FORMAT "x(20)"    LABEL "Phone No"
.

DEF INPUT PARAMETER rec-id       AS INTEGER  NO-UNDO.
DEF INPUT PARAMETER zinr         AS CHAR     NO-UNDO.
DEF INPUT PARAMETER item-description AS CHAR NO-UNDO.
DEF INPUT PARAMETER from-date    AS DATE     NO-UNDO.
DEF INPUT PARAMETER zeit         AS CHAR     NO-UNDO.
DEF INPUT PARAMETER dept         AS INTEGER  NO-UNDO.
DEF INPUT PARAMETER remark       AS CHAR     NO-UNDO.
DEF INPUT PARAMETER claimby      AS CHAR     NO-UNDO.
DEF INPUT PARAMETER claim-date   AS DATE     NO-UNDO.
DEF INPUT PARAMETER expired-date AS DATE     NO-UNDO.
DEF INPUT PARAMETER reportedBy   AS CHAR     NO-UNDO.
DEF INPUT PARAMETER report-date  AS DATE     NO-UNDO.
DEF INPUT PARAMETER phoneNo      AS CHAR     NO-UNDO.
DEF INPUT PARAMETER refno        AS CHAR     NO-UNDO.
DEF INPUT PARAMETER foundby      AS CHAR     NO-UNDO.
DEF INPUT PARAMETER location     AS CHAR     NO-UNDO.
DEF INPUT PARAMETER submitted    AS CHAR     NO-UNDO.
DEF INPUT PARAMETER user-init    AS CHAR     NO-UNDO.
DEF OUTPUT PARAMETER TABLE FOR s-list.

DEFINE VARIABLE expired-str AS CHAR NO-UNDO.
DEFINE VARIABLE claim-date-str AS CHAR NO-UNDO.

IF rec-id NE ? AND rec-id NE 0 THEN
DO:
  CREATE s-list.
  s-list.s-recid = rec-id.
END.

IF zinr EQ ? THEN zinr = "".
IF from-date EQ ? THEN from-date = TODAY.

IF zeit EQ ? THEN 
DO:
  zeit = SUBSTR(STRING(time, "HH:MM:SS"),1,2)   
         + SUBSTR(STRING(time, "HH:MM:SS"),4,2)   
         + SUBSTR(STRING(time, "HH:MM:SS"),7,2) .
END.

IF remark    EQ ? THEN remark    = "".
IF claimby   EQ ? THEN claimby   = "".
IF phoneNo   EQ ? THEN phoneNo   = "".
IF reportedBy EQ ? THEN reportedBy = "".
IF refno     EQ ? THEN refno     = "".
IF foundby   EQ ? THEN foundby   = "".
IF location  EQ ? THEN location  = "".
IF submitted EQ ? THEN submitted = "".
IF item-description EQ ? THEN item-description = "".

IF expired-date   EQ ? THEN 
DO:
  expired-str = "99/99/99".
END.
ELSE
DO:
  expired-str = STRING(expired-date).
END.

IF claim-date EQ ? THEN
DO:
  claim-date-str = "99/99/99".
END.
ELSE
DO:
  claim-date-str = STRING(claim-date).
END.


IF AVAILABLE s-list THEN
DO:
  RUN hk-lostfound-chgbl.p (zinr, 
                            from-date, 
                            zeit, 
                            dept,   
                            item-description + CHR(2) + remark, 
                            reportedBy + CHR(2) + claimby + CHR(2) + claim-date-str + CHR(2) + expired-str, 
                            report-date, 
                            phoneNo, 
                            refno, 
                            foundby, 
                            location,   
                            submitted, 
                            user-init, 
                            INPUT-OUTPUT TABLE s-list).  


END.
ELSE 
DO:
  RUN hk-lostfound-addbl.p (zinr, 
                            from-date, 
                            zeit, 
                            dept,   
                            item-description + CHR(2) + remark, 
                            reportedBy + CHR(2) + expired-str, 
                            report-date, 
                            phoneNo, 
                            refno, 
                            foundby, 
                            location,   
                            submitted, 
                            user-init, 
                            OUTPUT TABLE s-list).  

END.

