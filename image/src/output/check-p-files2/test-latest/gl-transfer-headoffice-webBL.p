DEFINE INPUT PARAMETER close-month      AS DATE NO-UNDO.
DEFINE INPUT PARAMETER close-year       AS DATE NO-UNDO.
DEFINE INPUT PARAMETER user-init        AS CHARACTER.
DEFINE INPUT PARAMETER language-code    AS INTEGER NO-UNDO.
DEFINE OUTPUT PARAMETER msg-str         AS CHARACTER.
DEFINE OUTPUT PARAMETER success-flag    AS LOGICAL NO-UNDO INIT NO.

DEFINE TEMP-TABLE t-htparam    LIKE htparam.
DEFINE TEMP-TABLE t-gl-jouhdr  LIKE gl-jouhdr.
DEFINE TEMP-TABLE t-gl-journal LIKE gl-journal.

RUN read-htparambl.p(3, 2843, 38, OUTPUT TABLE t-htparam).
FIND FIRST t-htparam NO-ERROR.
IF NOT AVAILABLE t-htparam THEN
DO:
    msg-str = "Param No [2843] was not available.".
    RETURN.
END.    

IF AVAILABLE t-htparam AND t-htparam.fchar EQ "" THEN
DO:
    msg-str = "Param No [2843] is empty value.".
    RETURN.
END.
    
IF NOT t-htparam.fchar MATCHES ("*:*") THEN
DO:
    msg-str = "Wrong Head Office IP:Port format" + " " + t-htparam.fchar.
    RETURN.
END.

IF NUM-ENTRIES(t-htparam.fchar, ":") EQ 2 THEN
DO:
    RUN gl-transf-headoffice1bl.p(language-code, close-month, OUTPUT success-flag, OUTPUT msg-str).
END.
ELSE IF NUM-ENTRIES(t-htparam.fchar, ":") EQ 3 THEN
DO:
    RUN gl-transf-headoffice11bl.p(language-code, close-month, close-year, OUTPUT success-flag, OUTPUT msg-str).
END.

