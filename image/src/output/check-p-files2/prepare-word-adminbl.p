DEF TEMP-TABLE t-brief LIKE brief
    FIELD rec-id AS INT.

DEF INPUT  PARAMETER kateg          AS INTEGER. 
DEF OUTPUT PARAMETER kategbezeich   AS CHAR.
DEF OUTPUT PARAMETER TABLE FOR t-brief.

FIND FIRST paramtext WHERE paramtext.txtnr = (kateg + 600) NO-LOCK. 
kategbezeich = paramtext.ptexte. 

FOR EACH brief WHERE brief.briefkateg = kateg NO-LOCK BY brief.briefnr:
    CREATE t-brief.
    BUFFER-COPY brief TO t-brief.
    ASSIGN t-brief.rec-id = RECID(brief).
END.
