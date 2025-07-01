DEFINE TEMP-TABLE sMove
    FIELD Object-nr      AS INTEGER     FORMAT ">>>>>>9"
    FIELD Object-nm      AS CHAR     FORMAT "x(30)"
    FIELD datum          AS DATE
    FIELD fLocation-str  AS CHAR     FORMAT "x(30)"
    FIELD fRoom          AS CHAR
    FIELD tLocation-str  AS CHAR     FORMAT "x(30)"
    FIELD tRoom          AS CHAR
    .
DEFINE BUFFER movement  FOR eg-moveproperty.
DEFINE BUFFER maintask  FOR queasy.
DEFINE BUFFER location  FOR eg-location.

DEF INPUT PARAMETER pvILanguage AS INTEGER          NO-UNDO.
DEF INPUT PARAMETER main-nr AS INT.
DEF INPUT PARAMETER fdate AS DATE.
DEF INPUT PARAMETER tdate AS DATE.
DEF OUTPUT PARAMETER TABLE FOR sMove.

DEFINE VAR nr AS INTEGER.
DEFINE VAR nm AS CHAR FORMAT "x(30)".

{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "eg-rephistorymoveAll". 

RUN create-browse.

PROCEDURE create-browse:
    FOR EACH sMove:
        DELETE sMove.
    END.

    FOR EACH eg-property WHERE eg-property.maintask = main-nr NO-LOCK BY eg-property.nr :
        nr = eg-property.nr.
        nm = eg-property.bezeich.

        FOR EACH movement WHERE movement.property-nr = eg-property.nr AND movement.datum >= fdate AND movement.datum <= tdate NO-LOCK:
            RUN add-line.
        END.

        nr = 0.
        nm = "".
    END.
END.


PROCEDURE add-line:
    DEFINE VARIABLE unknown AS CHAR FORMAT "x(24)".
    
    unknown = translateExtended("UNKNOWN", lvCAREA, "").
    
    CREATE smove.
    ASSIGN
        smove.object-nr      = nr /*movement.property-nr*/
        smove.Object-nm      = nm /*eg-property.bezeich*/
        smove.datum          = movement.datum
        smove.fRoom          = movement.fr-room
        smove.tRoom          = movement.to-room.

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
