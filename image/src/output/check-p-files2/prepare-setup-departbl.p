
DEFINE TEMP-TABLE dept-list   LIKE hoteldpt
    FIELD dpttype AS CHAR.

DEFINE OUTPUT PARAMETER max-dept AS INTEGER NO-UNDO.
DEFINE OUTPUT PARAMETER TABLE FOR dept-list.


FIND FIRST htparam WHERE htparam.paramnr = 989 NO-LOCK NO-ERROR.
IF AVAILABLE htparam THEN max-dept = htparam.finteger + 1.


FOR EACH hoteldpt NO-LOCK:
    CREATE dept-list.
    BUFFER-COPY hoteldpt TO dept-list.        
END.
