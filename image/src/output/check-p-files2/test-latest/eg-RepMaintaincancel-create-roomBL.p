DEFINE TEMP-TABLE troom
    FIELD room-nm AS CHAR FORMAT "x(24)" COLUMN-LABEL "Room"
    FIELD room-Selected AS LOGICAL INITIAL NO.

DEFINE TEMP-TABLE tLocation
    FIELD loc-nr  AS INTEGER 
    FIELD loc-nm  AS CHAR       FORMAT "x(24)" COLUMN-LABEL "Location"
    FIELD loc-selected AS LOGICAL INITIAL NO
    FIELD loc-guest AS LOGICAL INITIAL NO.

DEF INPUT PARAMETER TABLE FOR tlocation.
DEF OUTPUT PARAMETER TABLE FOR troom.

RUN create-room.

PROCEDURE create-room:
    DEF VAR i AS INTEGER NO-UNDO.
    DEF BUFFER qbuff FOR zimmer.
    DEF BUFFER qbuff1 FOR tlocation.

    FOR EACH troom:
        DELETE troom.
    END.    

    FIND FIRST qbuff1 WHERE qbuff1.loc-selected = YES AND qbuff1.loc-guest = YES NO-LOCK NO-ERROR.

        IF AVAILABLE qbuff1 THEN
        DO:
            FOR EACH qbuff NO-LOCK:
                CREATE troom.
                ASSIGN 
                    troom.room-nm = qbuff.zinr
                    troom.room-SELECTED = NO.
            END.
        END.
  
END.
