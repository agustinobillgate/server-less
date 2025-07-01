DEF TEMP-TABLE t-brief LIKE brief
    FIELD rec-id        AS INTEGER
    FIELD category      AS INTEGER
    FIELD category-str  AS CHARACTER.

DEFINE OUTPUT PARAMETER TABLE FOR t-brief.

DEFINE VARIABLE kateg AS INTEGER.

FOR EACH paramtext WHERE  paramtext.txtnr GE 601
    AND paramtext.txtnr LE 699 AND paramtext.ptexte NE "" NO-LOCK:
    
    kateg = (paramtext.txtnr - 600).
    FOR EACH brief WHERE brief.briefkateg EQ kateg NO-LOCK BY brief.briefkateg BY brief.briefnr:
        CREATE t-brief.
        BUFFER-COPY brief TO t-brief.
        ASSIGN 
            t-brief.rec-id          = RECID(brief)
            t-brief.category        = kateg
            t-brief.category-str    = paramtext.ptexte
            .
    END.
END.
