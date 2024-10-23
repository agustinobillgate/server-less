DEF TEMP-TABLE t-hoteldpt LIKE hoteldpt.

DEF OUTPUT PARAMETER licStr     AS CHAR NO-UNDO INIT "".
DEF OUTPUT PARAMETER coa-format AS CHAR NO-UNDO.
DEF OUTPUT PARAMETER TABLE FOR t-hoteldpt.

DEF VARIABLE licFlag AS LOGICAL NO-UNDO.

RUN htpchar.p(977, OUTPUT coa-format).

RUN htplogic.p(2000, OUTPUT licFlag).       /* GL License */
IF licFlag THEN licStr = licStr + "2000;".
RUN htplogic.p(988, OUTPUT licFlag).        /* INV License */
IF licFlag THEN licStr = licStr + "988;". 

FOR EACH hoteldpt NO-LOCK:
    CREATE t-hoteldpt.
    BUFFER-COPY hoteldpt TO t-hoteldpt.
END.
