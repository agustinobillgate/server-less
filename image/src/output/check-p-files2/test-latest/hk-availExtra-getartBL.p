
DEFINE TEMP-TABLE temp-art 
    FIELD art-nr    AS INTEGER
    FIELD art-nm    AS CHAR FORMAT "x(50)".

DEFINE TEMP-TABLE t-artikel     LIKE artikel.
DEFINE TEMP-TABLE t-htparam     LIKE htparam.

DEFINE OUTPUT PARAMETER TABLE FOR temp-art.

DEF VAR i       AS INTEGER.
DEF VAR int-art AS CHAR.

FOR EACH temp-art :
    DELETE temp-art.
END.

RUN read-htparambl.p (3, 2999, 5, OUTPUT TABLE t-htparam).
FIND FIRST t-htparam.
IF AVAILABLE t-htparam THEN
DO:
    DO i = 1 TO NUM-ENTRIES(t-htparam.fchar , ";" ) :
        int-art  = ENTRY(i,t-htparam.fchar,";").
        IF int-art NE "" THEN
        DO:
            CREATE temp-art.
            ASSIGN temp-art.art-nr = int(int-art).
        END.
    END.
END.

FOR EACH temp-art :
    RUN read-artikelbl.p (temp-art.art-nr, 0, "", OUTPUT TABLE t-artikel).
    FIND FIRST t-artikel.
    IF AVAILABLE t-artikel THEN
    DO:
        ASSIGN temp-art.art-nm = t-artikel.bezeich.
    END.
END.

