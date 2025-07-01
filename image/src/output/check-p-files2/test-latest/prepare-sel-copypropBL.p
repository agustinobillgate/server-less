
DEFINE TEMP-TABLE location 
    FIELD loc-nr AS INTEGER
    FIELD loc-nm AS CHAR      FORMAT "x(24)"
    FIELD loc-Selected AS LOGICAL INITIAL NO.

DEFINE TEMP-TABLE room
    FIELD room-nm AS CHAR     format "x(20)"
    FIELD room-Selected AS LOGICAL INITIAL NO.

DEF OUTPUT PARAMETER TABLE FOR location.
DEF OUTPUT PARAMETER TABLE FOR room.

RUN loc.
run room.

PROCEDURE loc:
    DEF VAR i AS INTEGER NO-UNDO.
    DEF BUFFER qbuff FOR eg-location.
    
    FOR EACH location:
        DELETE location.
    END.
    
    FOR EACH eg-location WHERE eg-location.guestflag = NO NO-LOCK :
    CREATE location.
        ASSIGN 
            location.loc-nr = eg-location.nr
            location.loc-nm = eg-location.bezeich
            location.loc-SELECTED = NO.
    END.
END.

PROCEDURE room:
    DEF VAR i AS INTEGER NO-UNDO.
    DEF BUFFER qbuff FOR zimmer.
    
    FOR EACH room:
        DELETE room.
    END.
    
    
    FOR EACH zimmer NO-LOCK BY zimmer.zinr :
        CREATE room.
        ASSIGN 
            room.room-nm = zimmer.zinr
            room.room-SELECTED = NO.
    END.
END.

