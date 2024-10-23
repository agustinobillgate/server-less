
DEF TEMP-TABLE t-briefzei       LIKE briefzei.
DEF INPUT  PARAMETER case-type  AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER briefno    AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER zeileNo    AS INTEGER NO-UNDO.
DEF OUTPUT PARAMETER TABLE FOR t-briefzei.

CASE case-type :
    WHEN 1 THEN
    DO:
        FIND FIRST briefzei WHERE briefzei.briefnr = briefno 
            AND briefzei.briefzeilnr = zeileNo NO-LOCK NO-ERROR.

        IF AVAILABLE briefzei THEN
        DO:
          CREATE t-briefzei.
          BUFFER-COPY briefzei TO t-briefzei.
        END.
    END.
    WHEN 2 THEN
    DO:
        FOR EACH briefzei WHERE briefzei.briefnr = briefno NO-LOCK :
            CREATE t-briefzei.
            BUFFER-COPY briefzei TO t-briefzei. 
        END.
    END.
END CASE.
