DEFINE INPUT PARAMETER curr-mode        AS CHAR NO-UNDO.
DEFINE INPUT PARAMETER docu-nr          AS CHAR NO-UNDO.
DEFINE INPUT PARAMETER bill-date        AS DATE NO-UNDO.
DEFINE INPUT-OUTPUT PARAMETER comments  AS CHAR NO-UNDO.

/*DEF VAR curr-mode   AS CHAR INIT "save".
DEF VAR docu-nr     AS CHAR INIT "FA211110001".
DEF VAR bill-date   AS DATE INIT 11/10/21.
DEF VAR comments    AS CHAR.*/

IF curr-mode = "save" THEN RUN create-queasy.
ELSE RUN load-queasy.

PROCEDURE create-queasy:
    FIND FIRST l-kredit WHERE l-kredit.rgdatum EQ bill-date AND l-kredit.opart LT 2 
        AND l-kredit.counter GE 0 AND l-kredit.name EQ docu-nr NO-LOCK NO-ERROR.
    FIND FIRST queasy WHERE queasy.KEY EQ 263 AND queasy.char1 EQ l-kredit.NAME NO-ERROR.
    IF AVAILABLE queasy THEN
    DO:
        ASSIGN
            queasy.char2 = comments.
    END.
    ELSE
    DO:
        CREATE queasy.
        ASSIGN
            queasy.KEY      = 263
            queasy.char1    = l-kredit.name
            queasy.char2    = comments.
    END.
END.

PROCEDURE load-queasy:
    FIND FIRST l-kredit WHERE l-kredit.rgdatum EQ bill-date AND l-kredit.opart LT 2 
        AND l-kredit.counter GE 0 AND l-kredit.name EQ docu-nr NO-LOCK NO-ERROR.
    FIND FIRST queasy WHERE queasy.KEY EQ 263 AND queasy.char1 EQ l-kredit.NAME NO-ERROR.
    IF AVAILABLE queasy THEN
    DO:
        ASSIGN
            comments = queasy.char2.
    END.
    ELSE
    DO:
        ASSIGN
            comments = " ".
    END.
END.
