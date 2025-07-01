DEF TEMP-TABLE t-brief          LIKE brief.

DEF OUTPUT PARAMETER TABLE FOR t-brief.

DEFINE VARIABLE fo-nr AS INTEGER. 

FIND FIRST htparam WHERE paramnr = 433 NO-LOCK. 
fo-nr = htparam.finteger.

FOR EACH brief WHERE  brief.briefkateg = fo-nr  NO-LOCK BY brief.briefnr:
    CREATE t-brief.
    BUFFER-COPY brief TO t-brief.
END.
