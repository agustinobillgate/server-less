DEFINE TEMP-TABLE t-artikel        LIKE artikel.
DEFINE TEMP-TABLE t-hoteldpt       LIKE hoteldpt.
DEFINE TEMP-TABLE t-argt-line      LIKE argt-line.

DEFINE INPUT PARAMETER TABLE FOR t-argt-line.
DEFINE OUTPUT PARAMETER TABLE FOR t-artikel.
DEFINE OUTPUT PARAMETER TABLE FOR t-hoteldpt.

FIND FIRST t-argt-line NO-LOCK NO-ERROR.
DO WHILE AVAILABLE t-argt-line:
    FIND FIRST t-artikel WHERE t-artikel.artnr = t-argt-line.argt-artnr
      AND t-artikel.departement = t-argt-line.departement NO-ERROR.
    IF NOT AVAILABLE t-artikel THEN
    DO:
      RUN read-artikelbl.p (t-argt-line.argt-artnr, 
        t-argt-line.departement, "", OUTPUT TABLE t-artikel).
    END.
    FIND FIRST t-hoteldpt WHERE t-hoteldpt.num = t-argt-line.departement NO-ERROR.
    IF NOT AVAILABLE t-hoteldpt THEN
    DO:
      RUN read-hoteldptbl.p(t-argt-line.departement, 
        OUTPUT TABLE t-hoteldpt).
    END.
    FIND NEXT t-argt-line NO-LOCK NO-ERROR.
END.
