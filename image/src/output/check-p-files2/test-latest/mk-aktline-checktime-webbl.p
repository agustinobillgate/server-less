{Supertrans.i}

DEFINE INPUT-OUTPUT PARAMETER zeit AS CHARACTER.
DEFINE INPUT-OUTPUT PARAMETER dauer AS CHARACTER.
DEFINE OUTPUT PARAMETER akt-line1-zeit AS INTEGER.
DEFINE OUTPUT PARAMETER akt-line1-dauer AS INTEGER.
DEFINE OUTPUT PARAMETER msg-str AS CHARACTER.

DEF VAR lvCAREA AS CHAR INITIAL "mk-aktline".

IF SUBSTR(zeit, 1, 2) GT "24" OR SUBSTR(zeit, 3, 2) GT "59" THEN 
DO: 
  msg-str = translateExtended ("Incorrect start time input.",lvCAREA,""). 
  zeit = "0000". 
  RETURN NO-APPLY.
END.

IF SUBSTR(dauer, 1, 2) GT "24" OR SUBSTR(dauer, 3, 2) GT "59" THEN 
DO: 
  msg-str = translateExtended ("Incorrect end time input.",lvCAREA,"").
  dauer = "0000".
  RETURN NO-APPLY.
END.

akt-line1-zeit = INTEGER(SUBSTR(zeit, 1, 2)) * 3600 
                + INTEGER(SUBSTR(zeit, 3, 2)) * 60.

akt-line1-dauer = INTEGER(SUBSTR(dauer, 1, 2)) * 3600 
                + INTEGER(SUBSTR(dauer, 3, 2)) * 60.



