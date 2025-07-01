{supertrans.i}   

DEFINE INPUT-OUTPUT PARAMETER zeit AS CHARACTER.
DEFINE OUTPUT PARAMETER akt-line-zeit AS INTEGER.
DEFINE OUTPUT PARAMETER msg-str AS CHARACTER INITIAL "".

DEF VAR lvCAREA AS CHAR INITIAL "clear-aktline".

IF SUBSTR(zeit, 1, 2) GT "24" OR SUBSTR(zeit, 3, 2) GT "59" THEN 
DO: 
  msg-str = translateExtended ("Incorrect time input.",lvCAREA,""). 
  zeit = "0000". 
  RETURN NO-APPLY.
END.

akt-line-zeit = INTEGER(SUBSTR(zeit, 1, 2)) * 3600 
                + INTEGER(SUBSTR(zeit, 3, 2)) * 60.

IF akt-line-zeit = 0 THEN
DO:
    msg-str = translateExtended ("Incorrect time input.",lvCAREA,"").
    RETURN NO-APPLY.
END.
