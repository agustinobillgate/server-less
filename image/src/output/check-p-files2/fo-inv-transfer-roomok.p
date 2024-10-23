DEFINE TEMP-TABLE t-zimmer    LIKE zimmer.
DEFINE TEMP-TABLE t-res-line  LIKE res-line.

DEFINE INPUT PARAMETER pvILanguage  AS INTEGER  NO-UNDO.
DEFINE INPUT PARAMETER currRoom     AS CHARACTER.

{SupertransBL.i}
DEFINE OUTPUT PARAMETER gname       AS CHARACTER.
DEFINE OUTPUT PARAMETER msgStr      AS CHARACTER.

DEFINE VARIABLE lvCAREA         AS CHAR INITIAL "fo-inv-transfer-roomok". 

IF currRoom NE "" THEN 
DO:
    RUN read-zimmerbl.p(1, currRoom, ?,?, OUTPUT TABLE t-zimmer).
    FIND FIRST t-zimmer NO-ERROR.
    IF NOT AVAILABLE t-zimmer THEN 
    DO: 
        msgStr = translateExtended ("No such room number.",lvCAREA,"").
    END.
    RUN read-res-linebl.p(35, ?,?,?,?, currRoom, ?,?,?,?, "", OUTPUT TABLE t-res-line).
    FIND FIRST t-res-line NO-ERROR.
    IF NOT AVAILABLE t-res-line THEN 
    DO: 
        msgStr = translateExtended ("Room not occupied.",lvCAREA,"").
    END.
    gname = t-res-line.name.
END.


