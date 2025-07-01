DEFINE TEMP-TABLE q1-list
    FIELD rec-id         AS INT
    FIELD argtnr         LIKE arrangement.argtnr
    FIELD arrangement    LIKE arrangement.arrangement
    FIELD argt-bez       LIKE arrangement.argt-bez
    FIELD artnr-logis    LIKE arrangement.artnr-logis
    FIELD intervall      LIKE arrangement.intervall
    FIELD argt-artikelnr LIKE arrangement.argt-artikelnr
    FIELD zuordnung      LIKE arrangement.zuordnung.

DEFINE TEMP-TABLE q2-list
    FIELD rec-id        AS INT
    FIELD argtnr        LIKE argt-line.argtnr
    FIELD departement   LIKE argt-line.departement
    FIELD argt-artnr    LIKE argt-line.argt-artnr
    FIELD bezeich       LIKE artikel.bezeich
    FIELD artnr         LIKE artikel.artnr
    FIELD betrag        LIKE argt-line.betrag
    FIELD vt-percnt     LIKE argt-line.vt-percnt.

DEFINE TEMP-TABLE t-hoteldpt
    FIELD num LIKE hoteldpt.num.

DEF OUTPUT PARAMETER TABLE FOR q1-list.
DEF OUTPUT PARAMETER TABLE FOR q2-list.
DEF OUTPUT PARAMETER TABLE FOR t-hoteldpt.

FOR EACH arrangement WHERE arrangement.segmentcode = 1
    NO-LOCK BY arrangement.argtnr:
    CREATE q1-list.
    ASSIGN
    q1-list.rec-id         = RECID(arrangement)
    q1-list.argtnr         = arrangement.argtnr
    q1-list.arrangement    = arrangement.arrangement
    q1-list.argt-bez       = arrangement.argt-bez
    q1-list.artnr-logis    = arrangement.artnr-logis
    q1-list.intervall      = arrangement.intervall
    q1-list.argt-artikelnr = arrangement.argt-artikelnr
    q1-list.zuordnung      = arrangement.zuordnung.
END.

FOR EACH q1-list:
    FOR EACH argt-line WHERE argt-line.argtnr = q1-list.argtnr NO-LOCK, 
        FIRST artikel WHERE artikel.artnr = argt-line.argt-artnr 
        AND artikel.departement = argt-line.departement NO-LOCK 
        BY argt-line.departement BY artikel.bezeich:
        CREATE q2-list.
        ASSIGN
        q2-list.rec-id        = RECID(argt-line)
        q2-list.argtnr        = argt-line.argtnr
        q2-list.departement   = argt-line.departement
        q2-list.argt-artnr    = argt-line.argt-artnr
        q2-list.bezeich       = artikel.bezeich
        q2-list.artnr         = artikel.artnr
        q2-list.betrag        = argt-line.betrag
        q2-list.vt-percnt     = argt-line.vt-percnt.
    END.
END.

FOR EACH hoteldpt:
    CREATE t-hoteldpt.
    ASSIGN t-hoteldpt.num = hoteldpt.num.
END.
