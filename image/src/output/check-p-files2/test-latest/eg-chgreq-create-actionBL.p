DEFINE TEMP-TABLE treqdetail
    FIELD reqnr AS INTEGER
    FIELD actionnr AS INTEGER
    FIELD action AS CHAR FORMAT "x(256)"
    FIELD create-date AS DATE
    FIELD create-time AS INTEGER
    FIELD create-str  AS CHAR
    FIELD create-by AS CHAR
    FIELD flag AS LOGICAL.

DEFINE TEMP-TABLE taction
    FIELD act-nr    AS INTEGER  FORMAT ">>>>>>9"
    FIELD act-nm    AS CHAR     FORMAT "x(39)"
    FIELD SELECTED  AS LOGICAL  INITIAL NO
    FIELD str-sel   AS CHAR     FORMAT "x(2)".

DEFINE INPUT PARAMETER intMaintask AS INTEGER NO-UNDO.
DEF INPUT PARAMETER TABLE FOR treqdetail.
DEF OUTPUT PARAMETER TABLE FOR taction.

RUN create-action.

PROCEDURE create-action:
    DEF BUFFER qbuff FOR eg-action.
    /*
    FOR EACH taction:
        DELETE taction.
    END.
    */

    IF intMaintask GT 0 THEN
    DO:
        FOR EACH qbuff WHERE qbuff.maintask = intMaintask /*AND qbuff.usefor NE 2*/
            USE-INDEX maintask_ix NO-LOCK BY qbuff.bezeich : 

            FIND FIRST taction WHERE taction.act-nr = qbuff.actionnr NO-LOCK NO-ERROR.
            IF AVAILABLE taction THEN
            DO:
                ASSIGN taction.act-nm = qbuff.bezeich.
            END.
            ELSE
            DO:
                FIND FIRST treqdetail WHERE treqdetail.actionnr = qbuff.actionnr NO-LOCK NO-ERROR.
                IF AVAILABLE treqdetail THEN
                DO:
                
                END.
                ELSE
                DO:
                    CREATE taction.
                    ASSIGN taction.act-nr = qbuff.actionnr
                           taction.act-nm = qbuff.bezeich.
                END.
            END.
        END.
    END.
    ELSE
    DO:
        FOR EACH qbuff USE-INDEX maintask_ix NO-LOCK BY qbuff.bezeich :             
            CREATE taction.
            ASSIGN taction.act-nr = qbuff.actionnr
                   taction.act-nm = qbuff.bezeich.            
        END.
    END.
END.
