
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
DEFINE TEMP-TABLE buf-s-list LIKE s-list.

DEFINE INPUT PARAMETER casetype  AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER comments  AS CHAR NO-UNDO.
DEFINE INPUT PARAMETER sorttype  AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER fr-date   AS DATE NO-UNDO.
DEFINE INPUT PARAMETER to-date   AS DATE NO-UNDO.
DEFINE INPUT PARAMETER user-init AS CHAR NO-UNDO.
DEFINE INPUT PARAMETER rec-id    AS INT NO-UNDO.
DEFINE OUTPUT PARAMETER TABLE FOR buf-s-list.


IF casetype = 1 THEN
DO:
    FOR EACH s-list:
        DELETE s-list.
    END.
    RUN create-list.
    RUN disp-it.
END.
ELSE IF casetype = 2 THEN
DO:
    RUN del-lostfound.
    FOR EACH s-list:
        DELETE s-list.
    END.
    RUN create-list.
    RUN disp-it.
END.


PROCEDURE create-list:
  DEF VAR i AS INTEGER NO-UNDO.

  FOR EACH queasy WHERE queasy.key = 7 NO-LOCK, 
    FIRST bediener WHERE bediener.nr = queasy.number2 NO-LOCK 
    BY queasy.date1 BY queasy.char1 BY queasy.number1: 
    CREATE s-list. 
    
    ASSIGN 
      s-list.nr         = queasy.number3 
      s-list.date1      = queasy.date1 
      s-list.zeit       = STRING(queasy.number1,"HH:MM:SS") 
      s-list.zinr       = queasy.char1 
      s-list.userinit   = bediener.userinit 
      s-list.bezeich    = ENTRY(1, queasy.char2, CHR(2)) 
      s-list.betriebsnr = queasy.betriebsnr
      s-list.s-recid    = RECID(queasy).
      
    IF NUM-ENTRIES(queasy.char2, CHR(2)) GT 1 THEN
        s-list.bemerk = ENTRY(2, queasy.char2, CHR(2)).

    DO i = 1 TO NUM-ENTRIES(queasy.char3, "|"):
      CASE i:
        WHEN 1 THEN
          s-list.foundby = ENTRY(1, queasy.char3, "|").
        WHEN 2 THEN
          s-list.submitted = ENTRY(2, queasy.char3, "|").
        WHEN 3 THEN
          s-list.reportBy = ENTRY(3, queasy.char3, "|") .
        WHEN 4 THEN
          s-list.report-date = DATE(ENTRY(4, queasy.char3, "|")) NO-ERROR.
        WHEN 5 THEN
          s-list.phoneNo = ENTRY(5, queasy.char3, "|").
        WHEN 6 THEN
          s-list.RefNo = ENTRY(6, queasy.char3, "|").
        WHEN 7 THEN
          s-list.Location = ENTRY(7, queasy.char3, "|").
        WHEN 8 THEN
          s-list.claimby = ENTRY(8, queasy.char3, "|").
        WHEN 9 THEN
          s-list.claim-date = DATE(ENTRY(9, queasy.char3, "|")) NO-ERROR.
        WHEN 10 THEN
          s-list.expired = DATE(ENTRY(10, queasy.char3, "|")) NO-ERROR.
      END CASE.
    END.  
  END. 
END. 

PROCEDURE disp-it:
    DEF VAR s AS CHAR.
    s = "*" + comments + "*".
    IF comments = "" THEN
    FOR EACH s-list WHERE s-list.betriebsnr = sorttype
          AND s-list.date1 GE fr-date
          AND s-list.date1 LE to-date NO-LOCK, 
        FIRST queasy WHERE RECID(queasy) = s-list.s-recid NO-LOCK 
        BY s-list.date1 BY s-list.zinr BY s-list.nr:
        RUN assign-it.
    END.
    ELSE
    FOR EACH s-list WHERE s-list.betriebsnr = sorttype
          AND s-list.date1 GE fr-date
          AND s-list.date1 LE to-date
          AND s-list.bezeich MATCHES s NO-LOCK,
        FIRST queasy WHERE RECID(queasy) = s-list.s-recid NO-LOCK
        BY s-list.date1 BY s-list.zinr BY s-list.nr:
        RUN assign-it.
    END.
END PROCEDURE.

PROCEDURE assign-it:
    CREATE buf-s-list.
    BUFFER-COPY s-list TO buf-s-list.
END.

PROCEDURE del-lostfound:
FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK. 
CREATE res-history. 
ASSIGN 
  res-history.nr = bediener.nr 
  res-history.datum = TODAY 
  res-history.zeit = TIME 
  res-history.aenderung = "Delete LostFound No" 
    + STRING(sorttype,">>>9") 
    + " Room " + comments.
  res-history.action = "HouseKeeping". 
FIND CURRENT res-history NO-LOCK. 
RELEASE res-history. 
FIND FIRST queasy WHERE RECID(queasy) = rec-id EXCLUSIVE-LOCK.
delete queasy. 
END.
