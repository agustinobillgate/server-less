DEFINE TEMP-TABLE sduration
    FIELD Duration-nr  AS INTEGER
    FIELD time-str AS CHAR FORMAT "X(100)".

/*DEFINE TEMP-TABLE q-list
    FIELD Duration-nr LIKE eg-Duration.Duration-nr
    FIELD time-str    LIKE sduration.time-str.*/

DEFINE TEMP-TABLE q-list
    FIELD Duration-nr AS INTEGER
    FIELD time-str    AS CHAR FORMAT "X(100)".

DEF OUTPUT PARAMETER TABLE FOR q-list.

RUN create-duration.

FOR EACH eg-Duration NO-LOCK ,FIRST sduration WHERE 
    sduration.Duration-nr = eg-Duration.Duration-nr BY eg-Duration.Duration-nr:
    CREATE q-list.
    ASSIGN
    q-list.Duration-nr = eg-Duration.Duration-nr
    q-list.time-str    = sduration.time-str.
END.

PROCEDURE create-duration:
    DEF BUFFER qbuff FOR eg-Duration.
    DEF VAR str AS CHAR NO-UNDO.

    FOR EACH sduration:
        DELETE sduration.
    END.

    FOR EACH qbuff NO-LOCK BY qbuff.Duration-nr:
        IF qbuff.DAY = 0 THEN
        DO:
            str = "".
        END.
        ELSE 
        DO:
            str = string(qbuff.DAY).
            IF qbuff.DAY > 1 THEN str = str + " days ".
            ELSE str = str + " day ".
        END.

        IF qbuff.hour = 0 THEN
        DO:
            str = str.
        END.
        ELSE 
        DO:
            str = str + string(qbuff.hour).
            IF qbuff.hour > 1 THEN str = str + " hrs ".
            ELSE str = str + " hour ".
        END.

        IF qbuff.minute = 0 THEN
        DO:
            str = str.
        END.
        ELSE 
        DO:
            str = str + string(qbuff.minute) + " min ".
        END.

        CREATE sduration.
        ASSIGN sduration.Duration-nr  = qbuff.Duration-nr
               sduration.time-str = str.
    END.
END.
 

