DEFINE TEMP-TABLE sMove
    FIELD datum          AS DATE
    FIELD fLocation-str  AS CHAR    FORMAT "x(30)"
    FIELD fRoom      AS CHAR
    FIELD tLocation-str  AS CHAR    FORMAT "x(30)"
    FIELD tRoom     AS CHAR
    .
DEFINE BUFFER movement  FOR eg-moveproperty.
DEFINE BUFFER location  FOR eg-location.

DEF INPUT PARAMETER pvILanguage AS INTEGER          NO-UNDO.
DEF INPUT PARAMETER prop-nr AS INT.
DEF INPUT PARAMETER fdate AS DATE.
DEF INPUT PARAMETER tdate AS DATE.
DEF OUTPUT PARAMETER TABLE FOR sMove.

{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "eg-RepHistoryMove". 

RUN create-browse.

PROCEDURE create-browse:
    FOR EACH sMove:
        DELETE sMove.
    END.

    FOR EACH movement WHERE movement.property-nr = prop-nr AND movement.datum >= fdate AND movement.datum <= tdate NO-LOCK:
        RUN add-line.
    END.
END.

PROCEDURE add-line:
    DEFINE VARIABLE unknown AS CHAR FORMAT "x(24)".
    
    unknown = translateExtended("UNKNOWN", lvCAREA, "").

    CREATE smove.
    ASSIGN
        smove.datum          = movement.datum
        smove.fRoom          = movement.fr-room
        smove.tRoom          = movement.to-room     
        .

        FIND FIRST location WHERE location.nr = movement.fr-location NO-LOCK NO-ERROR.
        IF AVAILABLE location THEN
            smove.flocation-str = location.bezeich.
        ELSE
            smove.flocation-str = unknown.

        FIND FIRST location WHERE location.nr = movement.to-location NO-LOCK NO-ERROR.
        IF AVAILABLE location THEN
            smove.tlocation-str = location.bezeich.
        ELSE
            smove.tlocation-str = unknown.

END.
