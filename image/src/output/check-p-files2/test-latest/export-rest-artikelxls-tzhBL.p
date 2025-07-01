DEFINE TEMP-TABLE rest-article-list
    FIELD dept-no           AS INTEGER
    FIELD dept-name         AS CHARACTER
    FIELD artnr             AS INTEGER
    FIELD art-desc          AS CHARACTER
    FIELD main-group        AS INTEGER
    FIELD sub-group         AS INTEGER
    FIELD main-group-desc   AS CHARACTER
    FIELD sub-group-desc    AS CHARACTER
    FIELD art-type          AS INTEGER
    FIELD price             AS DECIMAL
    FIELD cost%             AS DECIMAL
    FIELD fo-artnr          AS INTEGER
    FIELD foart-desc        AS CHARACTER
    FIELD recipe-no         AS INTEGER
    FIELD recipe-desc       AS CHARACTER
    FIELD kp-no             AS INTEGER
    FIELD kp-desc           AS CHARACTER
    FIELD active-art        AS LOGICAL
    .

DEFINE TEMP-TABLE rest-maingroup-list
    FIELD maingroup-no      AS INTEGER
    FIELD maingroup-desc    AS CHARACTER
    .

DEFINE TEMP-TABLE rest-subgroup-list
    FIELD dept-no           AS INTEGER
    FIELD dept-name         AS CHARACTER
    FIELD subgroup-no       AS INTEGER
    FIELD subgroup-desc     AS CHARACTER
    FIELD subgroup-prior    AS INTEGER
    FIELD subgroup-bgcol    AS INTEGER
    .

DEFINE OUTPUT PARAMETER TABLE FOR rest-article-list.
DEFINE OUTPUT PARAMETER TABLE FOR rest-maingroup-list.
DEFINE OUTPUT PARAMETER TABLE FOR rest-subgroup-list.

DEFINE VARIABLE disc-art1 AS INTEGER.
DEFINE VARIABLE disc-art2 AS INTEGER.
DEFINE VARIABLE disc-art3 AS INTEGER.

FIND FIRST htparam WHERE htparam.paramnr EQ 557 NO-LOCK NO-ERROR. 
IF AVAILABLE htparam THEN disc-art1 = htparam.finteger.
FIND FIRST htparam WHERE htparam.paramnr EQ 596 NO-LOCK NO-ERROR. 
IF AVAILABLE htparam THEN disc-art2 = htparam.finteger.
FIND FIRST htparam WHERE htparam.paramnr EQ 556 NO-LOCK NO-ERROR. 
IF AVAILABLE htparam THEN disc-art3 = htparam.finteger.

RUN create-rest-maingroup.
RUN create-rest-subgroup.
RUN create-rest-art.

PROCEDURE create-rest-maingroup:
    FOR EACH rest-maingroup-list:
        DELETE rest-maingroup-list.
    END.

    FIND FIRST wgrpgen NO-LOCK NO-ERROR.
    DO WHILE AVAILABLE wgrpgen:
        CREATE rest-maingroup-list.
        ASSIGN
            rest-maingroup-list.maingroup-no    = wgrpgen.eknr
            rest-maingroup-list.maingroup-desc  = wgrpgen.bezeich
            .

        FIND NEXT wgrpgen NO-LOCK NO-ERROR.
    END.
END PROCEDURE.

PROCEDURE create-rest-subgroup:
    FOR EACH rest-subgroup-list:
        DELETE rest-subgroup-list.
    END.

    FOR EACH hoteldpt WHERE hoteldpt.num GT 0 NO-LOCK BY hoteldpt.num:
        FIND FIRST wgrpdep WHERE wgrpdep.departement EQ hoteldpt.num NO-LOCK NO-ERROR.
        DO WHILE AVAILABLE wgrpdep:
            CREATE rest-subgroup-list.
            ASSIGN
                rest-subgroup-list.dept-no          = hoteldpt.num
                rest-subgroup-list.dept-name        = hoteldpt.depart
                rest-subgroup-list.subgroup-no      = wgrpdep.zknr   
                rest-subgroup-list.subgroup-desc    = wgrpdep.bezeich
                rest-subgroup-list.subgroup-prior   = wgrpdep.betriebsnr
                rest-subgroup-list.subgroup-bgcol   = INTEGER(ENTRY(1, wgrpdep.fibukonto,";"))
                .
            FIND NEXT wgrpdep WHERE wgrpdep.departement EQ hoteldpt.num NO-LOCK NO-ERROR.
        END.
    END.
END PROCEDURE.

PROCEDURE create-rest-art:
    FOR EACH rest-article-list:
        DELETE rest-article-list.
    END.

    FOR EACH hoteldpt WHERE hoteldpt.num GT 0 NO-LOCK BY hoteldpt.num:
        FIND FIRST h-artikel WHERE h-artikel.departement EQ hoteldpt.num
            AND h-artikel.artart EQ 0 
            AND h-artikel.artnr NE disc-art1
            AND h-artikel.artnr NE disc-art2 
            AND h-artikel.artnr NE disc-art3 NO-LOCK NO-ERROR.
        DO WHILE AVAILABLE h-artikel:
            CREATE rest-article-list.
            ASSIGN
                rest-article-list.dept-no       = h-artikel.departement
                rest-article-list.dept-name     = hoteldpt.depart
                rest-article-list.artnr         = h-artikel.artnr
                rest-article-list.art-desc      = h-artikel.bezeich
                rest-article-list.main-group    = h-artikel.endkum
                rest-article-list.sub-group     = h-artikel.zwkum
                rest-article-list.art-type      = h-artikel.artart
                rest-article-list.price         = h-artikel.epreis1
                rest-article-list.cost%         = h-artikel.prozent
                rest-article-list.fo-artnr      = h-artikel.artnrfront
                rest-article-list.recipe-no     = h-artikel.artnrrezept 
                rest-article-list.kp-no         = h-artikel.bondruckernr[1]
                rest-article-list.active-art    = h-artikel.activeflag
                .

            FIND FIRST artikel WHERE artikel.artnr EQ h-artikel.artnrfront
                AND artikel.departement EQ h-artikel.departement NO-LOCK NO-ERROR.
            IF AVAILABLE artikel THEN
            DO:
                rest-article-list.foart-desc = artikel.bezeich.
            END.

            FIND FIRST h-rezept WHERE h-rezept.artnrrezept EQ h-artikel.artnrrezept NO-LOCK NO-ERROR.
            IF AVAILABLE h-rezept THEN
            DO:
                rest-article-list.recipe-desc = SUBSTR(h-rezept.bezeich,1,24).
            END.

            FIND FIRST wgrpgen WHERE wgrpgen.eknr EQ h-artikel.endkum NO-LOCK NO-ERROR.
            IF AVAILABLE wgrpgen THEN
            DO:
                rest-article-list.main-group-desc = wgrpgen.bezeich.
            END.

            FIND FIRST wgrpdep WHERE wgrpdep.departement EQ h-artikel.departement
                AND wgrpdep.zknr EQ h-artikel.zwkum NO-LOCK NO-ERROR.
            IF AVAILABLE wgrpdep THEN
            DO:
                rest-article-list.sub-group-desc = wgrpdep.bezeich.
            END.

            FIND FIRST printer WHERE printer.nr EQ h-artikel.bondruckernr[1] NO-LOCK NO-ERROR.
            IF AVAILABLE printer THEN
            DO:
                rest-article-list.kp-desc = printer.position.
            END.

            FIND NEXT h-artikel WHERE h-artikel.departement EQ hoteldpt.num
                AND h-artikel.artart EQ 0 
                AND h-artikel.artnr NE disc-art1
                AND h-artikel.artnr NE disc-art2 
                AND h-artikel.artnr NE disc-art3 NO-LOCK NO-ERROR.
        END.
    END.
END PROCEDURE.
