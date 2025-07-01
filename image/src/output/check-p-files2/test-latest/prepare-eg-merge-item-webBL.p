
DEFINE TEMP-TABLE merge-list LIKE eg-property      
    FIELD object-nm AS CHARACTER   
    FIELD loc-nm    AS CHARACTER
.

DEFINE INPUT PARAMETER item-nr AS INTEGER.
DEFINE OUTPUT PARAMETER TABLE FOR merge-list.
/*DEFINE VARIABLE item-nr AS INTEGER INITIAL 1.*/

DEFINE VARIABLE object-no   AS INTEGER.
DEFINE VARIABLE loc-no      AS INTEGER.
DEFINE VARIABLE room-no     AS CHARACTER.

FIND FIRST eg-property WHERE eg-property.nr EQ item-nr NO-LOCK NO-ERROR.
IF AVAILABLE eg-property THEN
DO:
    ASSIGN
        object-no   = eg-property.maintask
        loc-no      = eg-property.location
        room-no     = eg-property.zinr
    .
END.

FOR EACH eg-property WHERE eg-property.nr NE item-nr
    AND eg-property.maintask EQ object-no 
    AND eg-property.location EQ loc-no
    AND eg-property.zinr EQ room-no NO-LOCK:
    
    CREATE merge-list.
    BUFFER-COPY eg-property TO merge-list.

    FIND FIRST eg-location WHERE eg-location.nr = eg-property.location NO-LOCK NO-ERROR.
    IF AVAILABLE eg-location THEN merge-list.loc-nm = eg-location.bezeich.

    FIND FIRST queasy WHERE queasy.KEY = 133 
        AND queasy.number1 = eg-property.maintask NO-LOCK NO-ERROR.
    IF AVAILABLE queasy THEN merge-list.object-nm = queasy.char1.    
END.

