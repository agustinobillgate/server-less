
DEFINE TEMP-TABLE akt-line1 LIKE akt-line.
DEFINE TEMP-TABLE t-akt-code LIKE akt-code.
DEFINE TEMP-TABLE t-guest    LIKE guest.

DEFINE INPUT-OUTPUT PARAMETER akt-line-gastnr AS INTEGER.
DEFINE INPUT PARAMETER akt-line-aktionscode AS INTEGER.
DEFINE INPUT PARAMETER akt-line-prioritaet AS INTEGER.
DEFINE INPUT PARAMETER akt-line-zeit AS INTEGER.
DEFINE INPUT PARAMETER akt-line-dauer AS INTEGER.
DEFINE INPUT PARAMETER akt-line-bemerk AS CHARACTER.
DEFINE OUTPUT PARAMETER lname   AS CHARACTER.
DEFINE OUTPUT PARAMETER aktion  AS CHARACTER.
DEFINE OUTPUT PARAMETER prior   AS CHARACTER.
DEFINE OUTPUT PARAMETER zeit    AS CHARACTER.
DEFINE OUTPUT PARAMETER dauer   AS CHARACTER.
DEFINE OUTPUT PARAMETER comment AS CHARACTER.
DEFINE OUTPUT PARAMETER TABLE FOR t-akt-code.

IF akt-line-gastnr > 0  THEN  
DO:  
    RUN read-guestbl.p(1, akt-line-gastnr, "", "", OUTPUT TABLE t-guest).  
    FIND FIRST t-guest NO-ERROR.  
    IF AVAILABLE t-guest THEN  
    DO:  
        lname = t-guest.NAME + ", " + t-guest.anredefirma.  
        akt-line-gastnr = t-guest.gastnr.  
    END.   
END.  

RUN read-akt-codebl.p(1, "", ?, OUTPUT TABLE t-akt-code). 

FIND FIRST t-akt-code WHERE t-akt-code.aktiongrup = 1   
    AND t-akt-code.aktionscode = akt-line-aktionscode NO-LOCK NO-ERROR.   
IF AVAILABLE t-akt-code THEN  
    ASSIGN aktion = t-akt-code.bezeich.

IF akt-line-prioritaet = 1 THEN prior = "Low".  
ELSE IF akt-line-prioritaet = 2 THEN prior = "Medium" .  
ELSE IF akt-line-prioritaet = 3 THEN prior = "High" .  

zeit = SUBSTR(STRING(akt-line-zeit, "HH:MM"), 1, 2)   
     + SUBSTR(STRING(akt-line-zeit, "HH:MM"), 4, 2).   
dauer = SUBSTR(STRING(akt-line-dauer, "HH:MM"), 1, 2)   
      + SUBSTR(STRING(akt-line-dauer, "HH:MM"), 4, 2).   
comment = akt-line-bemerk.


