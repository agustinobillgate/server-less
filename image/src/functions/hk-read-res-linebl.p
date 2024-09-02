DEFINE INPUT PARAMETER pvILanguage  AS INT.
DEFINE INPUT PARAMETER zinr         AS CHAR.
DEFINE OUTPUT PARAMETER guest-name  AS CHAR.
DEFINE OUTPUT PARAMETER msg-str     AS CHAR.

DEFINE TEMP-TABLE t-res-line    LIKE res-line.
{ SupertransBL.i } 

DEFINE VARIABLE lvCAREA AS CHAR.

RUN read-res-linebl.p (7, 0,?,?,1, zinr, ?,?,?,?,"", OUTPUT TABLE t-res-line).
FIND FIRST t-res-line NO-ERROR. 
IF NOT AVAILABLE t-res-line THEN 
DO: 
    msg-str = translateExtended ("Room / Inhouse Guest not found.",lvCAREA,"").
    RETURN. 
END. 
ELSE guest-name = t-res-line.NAME. 
