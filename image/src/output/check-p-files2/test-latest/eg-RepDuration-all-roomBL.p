DEFINE TEMP-TABLE tMaintask
    FIELD Main-nr  AS INTEGER 
    FIELD Main-nm  AS CHAR FORMAT "x(24)" COLUMN-LABEL "Object"
    FIELD main-selected AS LOGICAL INITIAL NO.

DEFINE TEMP-TABLE troom
    FIELD room-nm AS CHAR FORMAT "x(24)" COLUMN-LABEL "Room"
    FIELD room-Selected AS LOGICAL INITIAL NO.

DEFINE TEMP-TABLE tproperty
    FIELD prop-nr AS INTEGER
    FIELD prop-nm AS CHAR FORMAT "x(24)" COLUMN-LABEL "Object Item"
    FIELD prop-selected AS LOGICAL INITIAL NO
    FIELD pcateg-nr AS INTEGER
    FIELD pcateg AS CHAR
    FIELD pmain-nr AS INTEGER
    FIELD pmain AS CHAR
    FIELD ploc-nr AS INTEGER
    FIELD ploc  AS CHAR
    FIELD pzinr    AS CHAR.

DEFINE TEMP-TABLE tLocation
    FIELD loc-nr  AS INTEGER 
    FIELD loc-nm  AS CHAR FORMAT "x(24)" COLUMN-LABEL "Location"
    FIELD loc-selected AS LOGICAL INITIAL NO
    FIELD loc-guest    AS LOGICAL INITIAL NO.

DEF INPUT PARAMETER all-room AS LOGICAL.
DEF INPUT PARAMETER TABLE FOR tLocation.
DEF INPUT PARAMETER TABLE FOR tmaintask.
DEF INPUT PARAMETER TABLE FOR troom.
DEF OUTPUT PARAMETER TABLE FOR tproperty.

RUN create-property.

PROCEDURE create-property:
    DEF BUFFER qbuff FOR eg-property.
    DEF BUFFER comlocat FOR tlocation.
    DEF BUFFER comMain FOR tmaintask.
    DEF BUFFER comRoom FOR troom.
    DEF BUFFER ques FOR queasy.

    FOR EACH tproperty:
        DELETE tproperty.
    END.

    IF all-room THEN
        FOR EACH troom:
            ASSIGN troom.room-selected = YES.
        END.

    CREATE tproperty.
    ASSIGN tproperty.prop-nr = 0
        tproperty.prop-nm = "Undefine".

    FOR EACH comlocat WHERE comlocat.loc-selected NO-LOCK:
        IF comlocat.loc-guest = YES THEN
        DO:
            FOR EACH qbuff WHERE qbuff.location = comlocat.loc-nr USE-INDEX mtloczin_x NO-LOCK,
                FIRST commain WHERE commain.main-nr = qbuff.maintask AND commain.main-selected NO-LOCK,
                FIRST comroom WHERE comroom.room-nm = qbuff.zinr AND comroom.room-selected NO-LOCK:
                CREATE tproperty.
    
                ASSIGN tproperty.prop-nr = qbuff.nr
                       tproperty.prop-nm = qbuff.bezeich + "(" + trim(string(qbuff.nr , ">>>>>>9")) + ")"
                       tproperty.pzinr   = qbuff.zinr 
                       tproperty.pmain-nr = qbuff.maintask
                       tproperty.ploc-nr  = qbuff.location.
            
                FIND FIRST queasy WHERE queasy.KEY= 133 AND queasy.number1 = qbuff.maintask NO-LOCK NO-ERROR.
                IF AVAILABLE queasy THEN
                DO:
                    ASSIGN tproperty.pmain = queasy.char1
                           tproperty.pcateg-nr = queasy.number2.

                    FIND FIRST ques WHERE ques.KEY = 132 AND ques.number1 = queasy.number2 NO-LOCK NO-ERROR.
                    IF AVAILABLE ques THEN
                    DO:
                        ASSIGN tproperty.pcateg = ques.char1.
                    END.
                END.
                ELSE
                DO:
                    ASSIGN tproperty.pmain = ""
                           tproperty.pcateg-nr = 0
                           tproperty.pcateg = "".
                END.
            
                FIND FIRST eg-location WHERE eg-location.nr = qbuff.location NO-LOCK NO-ERROR.
                IF AVAILABLE eg-location THEN
                    ASSIGN tproperty.ploc = eg-location.bezeich.
                ELSE
                    ASSIGN  tproperty.ploc = "".
            END.
        END.
        ELSE
        DO:

            FOR EACH qbuff WHERE qbuff.location = comlocat.loc-nr USE-INDEX location_ix NO-LOCK,
                FIRST commain WHERE commain.main-nr = qbuff.maintask AND commain.main-selected NO-LOCK:

                CREATE tproperty.
                ASSIGN tproperty.prop-nr = qbuff.nr
                       tproperty.prop-nm = qbuff.bezeich + "(" + trim(string(qbuff.nr , ">>>>>>9")) + ")"
                       tproperty.pzinr   = qbuff.zinr 
                       tproperty.pmain-nr = qbuff.maintask
                       tproperty.ploc-nr  = qbuff.location.
            
                FIND FIRST queasy WHERE queasy.KEY= 133 AND queasy.number1 = qbuff.maintask NO-LOCK NO-ERROR.
                IF AVAILABLE queasy THEN
                DO:
                    ASSIGN tproperty.pmain = queasy.char1
                           tproperty.pcateg-nr = queasy.number2.

                    FIND FIRST ques WHERE ques.KEY = 132 AND ques.number1 = queasy.number2 NO-LOCK NO-ERROR.
                    IF AVAILABLE ques THEN
                    DO:
                        ASSIGN tproperty.pcateg = ques.char1.
                    END.

                END.
                ELSE
                DO:
                    ASSIGN tproperty.pmain = ""
                           tproperty.pcateg-nr = 0
                           tproperty.pcateg = "".
                END.
            
                FIND FIRST eg-location WHERE eg-location.nr = qbuff.location NO-LOCK NO-ERROR.
                IF AVAILABLE eg-location THEN
                    ASSIGN tproperty.ploc = eg-location.bezeich.
                ELSE
                    ASSIGN  tproperty.ploc = "".
            END.
        END.
    END.
END.

