DEF TEMP-TABLE t-brief LIKE brief
    FIELD rec-id AS INT.

DEF INPUT  PARAMETER kateg          AS INTEGER. 
DEF INPUT  PARAMETER b-list-briefnr AS INT.
DEF INPUT  PARAMETER recid-brief    AS INT.
DEF OUTPUT PARAMETER TABLE FOR t-brief.

FIND FIRST brief WHERE RECID(brief) = recid-brief NO-LOCK NO-ERROR.
IF AVAILABLE brief THEN
DO:
    FIND FIRST briefzei WHERE briefzei.briefnr = b-list-briefnr 
       AND briefzei.briefzeilnr = 1 EXCLUSIVE-LOCK NO-ERROR. 
    IF AVAILABLE briefzei THEN 
    DO:
        delete briefzei. 
        RELEASE briefzei.
    END.     
    FIND CURRENT brief EXCLUSIVE-LOCK. 
    DELETE brief. 
    RELEASE brief.
END.

FOR EACH brief WHERE brief.briefkateg = kateg NO-LOCK BY brief.briefnr:
    CREATE t-brief.
    BUFFER-COPY brief TO t-brief.
    ASSIGN 
        t-brief.rec-id = RECID(brief).
END.
