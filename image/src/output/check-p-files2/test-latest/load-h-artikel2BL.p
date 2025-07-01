DEF TEMP-TABLE t-h-artikel LIKE h-artikel.
DEF TEMP-TABLE t-wgrpdep   LIKE wgrpdep.
DEF TEMP-TABLE t-h-menu    LIKE h-menu.

DEF INPUT  PARAMETER case-type AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER dept      AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER artType   AS INTEGER NO-UNDO. 
DEF OUTPUT PARAMETER TABLE     FOR t-h-artikel.
DEF OUTPUT PARAMETER TABLE     FOR t-wgrpdep.
DEF OUTPUT PARAMETER TABLE     FOR t-h-menu.

DEFINE BUFFER hart FOR h-artikel.

IF case-type = 1 THEN
DO:
    FOR EACH h-artikel WHERE h-artikel.departement = dept 
        AND h-artikel.artart = artType 
        AND h-artikel.activeflag NO-LOCK:
        IF h-artikel.artnr = 0 THEN
        DO:
            FIND FIRST hart WHERE RECID(hart) = RECID(h-artikel).
            DELETE hart.
            RELEASE hart.
        END.
        ELSE
        DO:
            CREATE t-h-artikel.
            BUFFER-COPY h-artikel TO t-h-artikel.
            FIND FIRST wgrpdep WHERE wgrpdep.departement = dept
            AND wgrpdep.zknr = h-artikel.zwkum NO-LOCK NO-ERROR.
            IF AVAILABLE wgrpdep THEN
            DO:
              FIND FIRST t-wgrpdep WHERE t-wgrpdep.zknr = wgrpdep.zknr
                NO-ERROR.
              IF NOT AVAILABLE t-wgrpdep THEN
              DO:
                CREATE t-wgrpdep.
                BUFFER-COPY wgrpdep TO t-wgrpdep.
              END.
            END.
            ELSE
            DO:
                FIND FIRST t-wgrpdep WHERE t-wgrpdep.zknr = h-artikel.zwkum
                  NO-ERROR.
                IF NOT AVAILABLE t-wgrpdep THEN
                DO:
                  CREATE t-wgrpdep.
                  ASSIGN 
                      t-wgrpdep.zknr      = h-artikel.zwkum
                      t-wgrpdep.bezeich   = STRING(h-artikel.zwkum) 
                      + " - NOT DEFINED!!"
                  .
                END.
            END.
        END.
    END.

    FOR EACH h-menu NO-LOCK:
        CREATE t-h-menu.
        BUFFER-COPY h-menu TO t-h-menu.
    END.    
END.

