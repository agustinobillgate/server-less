DEFINE TEMP-TABLE t-guest LIKE guest.

DEFINE INPUT-OUTPUT PARAMETER akt-line-gastnr  AS INTEGER.
DEFINE INPUT PARAMETER akt-line-bemerk  AS CHARACTER.
DEFINE OUTPUT PARAMETER lname           AS CHARACTER.
DEFINE OUTPUT PARAMETER comment         AS CHARACTER.
DEFINE OUTPUT PARAMETER zeit            AS CHARACTER.

RUN read-guestbl.p(1, akt-line-gastnr, "", "", OUTPUT TABLE t-guest).  
FIND FIRST t-guest NO-ERROR.  
IF AVAILABLE t-guest THEN  
DO:  
    lname = t-guest.NAME + ", " + t-guest.anredefirma.  
    akt-line-gastnr = t-guest.gastnr.  
END.  
ELSE lname = "".  

comment = akt-line-bemerk.   
/*zeit = SUBSTR(STRING(TIME, "HH:MM"), 1, 2)   
     + SUBSTR(STRING(TIME, "HH:MM"), 4, 2). */
zeit = STRING(TIME, "HH:MM").
