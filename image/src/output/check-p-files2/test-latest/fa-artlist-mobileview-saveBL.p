
DEFINE TEMP-TABLE fa-article-list
    FIELD mathis-number     AS INTEGER
    FIELD fa-art-name       AS CHARACTER
    FIELD fa-art-group      AS INTEGER
    FIELD fa-art-subgroup   AS INTEGER
    FIELD fa-art-category   AS INTEGER
    FIELD fa-art-mark       AS CHARACTER
    FIELD fa-art-model      AS CHARACTER
    FIELD fa-art-spec       AS CHARACTER
    FIELD fa-art-remark     AS CHARACTER
    .

DEFINE INPUT PARAMETER v-key        AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER TABLE FOR fa-article-list.
DEFINE OUTPUT PARAMETER v-success   AS LOGICAL INITIAL NO.
DEFINE OUTPUT PARAMETER v-result    AS CHARACTER NO-UNDO.

FIND FIRST fa-article-list NO-LOCK NO-ERROR.
IF NOT AVAILABLE fa-article-list THEN
DO:
    v-result = "Asset List not found.".
    RETURN.
END.

FIND FIRST mathis WHERE mathis.nr EQ fa-article-list.mathis-number NO-LOCK NO-ERROR.
IF NOT AVAILABLE mathis THEN
DO:
    v-result = "Asset not found.".
    RETURN.
END.
FIND FIRST fa-artikel WHERE fa-artikel.nr EQ fa-article-list.mathis-number NO-LOCK NO-ERROR. 
IF NOT AVAILABLE fa-artikel THEN
DO:
    v-result = "Asset not found.".
    RETURN.
END.

IF v-key EQ 1 THEN /*Modify*/
DO:
    FIND FIRST mathis WHERE mathis.nr EQ fa-article-list.mathis-number NO-LOCK NO-ERROR.
    IF AVAILABLE mathis THEN
    DO:
        FIND CURRENT mathis EXCLUSIVE-LOCK.
        ASSIGN
            mathis.NAME     = fa-article-list.fa-art-name
            mathis.mark     = fa-article-list.fa-art-mark  
            mathis.model    = fa-article-list.fa-art-model 
            mathis.spec     = fa-article-list.fa-art-spec  
            mathis.remark   = fa-article-list.fa-art-remark
            .
        FIND CURRENT mathis NO-LOCK.
        RELEASE mathis.
    END.

    FIND FIRST fa-artikel WHERE fa-artikel.nr EQ fa-article-list.mathis-number NO-LOCK NO-ERROR. 
    IF AVAILABLE fa-artikel THEN
    DO:
        FIND CURRENT fa-artikel EXCLUSIVE-LOCK.
        ASSIGN
            fa-artikel.gnr      = fa-article-list.fa-art-group   
            fa-artikel.subgrp   = fa-article-list.fa-art-subgroup
            fa-artikel.katnr    = fa-article-list.fa-art-category
            .
        FIND CURRENT fa-artikel NO-LOCK.
        RELEASE fa-artikel.
    END.
END.
v-success = YES.


