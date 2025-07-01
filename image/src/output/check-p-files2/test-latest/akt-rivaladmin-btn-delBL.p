
DEF INPUT  PARAMETER pvILanguage    AS INTEGER  NO-UNDO.
DEF INPUT  PARAMETER aktionscode    AS INTEGER.
DEF INPUT  PARAMETER aktiongrup     AS INTEGER.
DEF INPUT  PARAMETER bezeich        AS CHAR.
DEF OUTPUT PARAMETER msg-str        AS CHAR.
DEF OUTPUT PARAMETER success-flag   AS LOGICAL INIT NO.

{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "akt-rivaladmin". 

FIND FIRST akthdr WHERE akthdr.mitbewerber[1] = aktionscode OR akthdr.mitbewerber[2] = aktionscode
   OR akthdr.mitbewerber[3] = aktionscode NO-LOCK NO-ERROR. 
IF AVAILABLE akthdr THEN 
DO: 
 msg-str = msg-str + CHR(2)
         + translateExtended ("Open sales action exists, deleting not possible.",lvCAREA,"").
END. 
ELSE 
DO:
 FIND FIRST akt-code WHERE akt-code.aktiongrup = aktiongrup AND 
     akt-code.aktionscode = aktionscode
     AND akt-code.bezeich = bezeich EXCLUSIVE-LOCK NO-ERROR.
 IF AVAILABLE akt-code THEN
 DO:
     delete akt-code.
     success-flag = YES.
 END.
 /*MTOPEN QUERY q1 FOR EACH akt-code WHERE akt-code.aktiongrup = 4 NO-LOCK BY akt-code.aktionscode. 
 IF AVAILABLE akt-code THEN 
 DO: 
    selected = YES. 
    RUN fill-akt-code-list. 
    RUN disp-akt-code-list. 
 END.*/ 
END. 
