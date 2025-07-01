
DEFINE TEMP-TABLE property
    FIELD prop-nr       AS INTEGER
    FIELD prop-nm       AS CHAR     FORMAT "x(30)"
    FIELD prop-loc      AS INTEGER
    FIELD prop-loc-nm   AS CHAR     FORMAT "x(30)"
    FIELD prop-zinr     AS CHAR
    FIELD prop-Selected AS LOGICAL INITIAL NO
    FIELD str           AS CHAR     FORMAT "x(1)" INITIAL "".

DEF INPUT PARAMETER maintain-nr AS INT.
DEF OUTPUT PARAMETER TABLE FOR property.

run prop.

PROCEDURE prop:
    DEF VAR i AS INTEGER NO-UNDO.
    DEF VAR a AS INTEGER NO-UNDO.
    DEF VAR loc-nm AS CHAR FORMAT "x(30)".
    DEF BUFFER qbuff1 FOR eg-property.

    FOR EACH property:
        DELETE property.
    END.

    FIND FIRST eg-maintain WHERE eg-maintain.maintainnr = maintain-nr NO-LOCK NO-ERROR.
    IF AVAILABLE eg-maintain THEN
    DO:
        i =  eg-maintain.propertynr.

        FIND FIRST eg-property WHERE eg-property.nr = eg-maintain.propertynr NO-LOCK NO-ERROR.
        IF AVAILABLE eg-property THEN a = eg-property.maintask.

        FOR EACH eg-property WHERE eg-property.maintask = a 
            AND eg-property.nr NE i 
            NO-LOCK BY eg-property.location BY eg-property.zinr :
            FIND FIRST eg-location WHERE eg-location.nr = eg-property.location 
                NO-LOCK NO-ERROR.
            IF AVAILABLE eg-location THEN loc-nm = eg-location.bezeich.
            ELSE loc-nm = "".
            CREATE property.
            ASSIGN 
                property.prop-nr        = eg-property.nr
                property.prop-nm        = eg-property.bezeich
                property.prop-loc       = eg-property.location
                property.prop-loc-nm    = loc-nm
                property.prop-zinr      = eg-property.zinr
                property.prop-SELECTED  = NO.
        END.
    END.
END.
