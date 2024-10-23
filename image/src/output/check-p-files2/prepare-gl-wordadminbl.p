
DEF TEMP-TABLE t-brief LIKE brief.

DEF OUTPUT PARAMETER kateg          AS INT.
DEF OUTPUT PARAMETER kategbezeich   AS CHAR.
DEF OUTPUT PARAMETER glcoa-flag     AS LOGICAL.
DEF OUTPUT PARAMETER briefnr        AS INTEGER.
DEF OUTPUT PARAMETER TABLE FOR t-brief.

/*Define Function*/
FUNCTION createGuestno RETURNS CHARACTER(INPUT letterNo AS INTEGER):
    DEFINE VARIABLE outStr AS CHARACTER.

    DEFINE VARIABLE i AS INTEGER.
    outStr = STRING(letterNo).
    DO i = 1 TO 8 - LENGTH(STRING(letterNo)):
        outStr = "0" + outStr.
    END.
    outStr = "-2" + outStr.
    RETURN outStr.
END FUNCTION.

FIND FIRST htparam WHERE paramnr = 987 NO-LOCK.
kateg = htparam.finteger.
FIND FIRST paramtext WHERE paramtext.txtnr =  (kateg + 600) NO-LOCK.
kategbezeich = paramtext.ptexte.


briefnr = 0. 
FOR EACH brief WHERE brief.briefkateg = kateg NO-LOCK BY brief.briefnr:
    CREATE t-brief.
    FIND FIRST guestbook WHERE guestbook.gastnr = int(createGuestno(brief.briefnr)) NO-LOCK NO-ERROR.
    IF NOT AVAILABLE guestbook THEN
        BUFFER-COPY brief TO t-brief.
    ELSE DO:
        BUFFER-COPY brief TO t-brief.
        ASSIGN t-brief.FNAME = "(CLOUD) " + brief.fname.
    END.
    IF brief.briefnr GT briefnr THEN 
        briefnr = brief.briefnr.
END.

FIND FIRST htparam WHERE paramnr = 967 NO-LOCK. 
glcoa-flag = htparam.flogical. 

FOR EACH brief NO-LOCK BY brief.briefnr:
   IF brief.briefnr GT briefnr THEN 
     briefnr = brief.briefnr. 
END.
briefnr = briefnr + 1. 

