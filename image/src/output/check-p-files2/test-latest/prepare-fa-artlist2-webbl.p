
DEFINE TEMP-TABLE q1-list
    FIELD name              LIKE mathis.name
    FIELD asset             LIKE mathis.asset
    FIELD datum             LIKE mathis.datum
    FIELD price             LIKE mathis.price
    FIELD anzahl            LIKE fa-artikel.anzahl
    FIELD warenwert         LIKE fa-artikel.warenwert
    FIELD depn-wert         LIKE fa-artikel.depn-wert
    FIELD book-wert         LIKE fa-artikel.book-wert
    FIELD katnr             LIKE fa-artikel.katnr
    FIELD bezeich           LIKE fa-grup.bezeich
    FIELD location          LIKE mathis.location
    FIELD first-depn        LIKE fa-artikel.first-depn
    FIELD next-depn         LIKE fa-artikel.next-depn
    FIELD last-depn         LIKE fa-artikel.last-depn
    FIELD id                LIKE fa-artikel.id
    FIELD created           LIKE fa-artikel.created
    FIELD cid               LIKE fa-artikel.cid
    FIELD changed           LIKE fa-artikel.changed
    FIELD remark            LIKE mathis.remark
    
    FIELD mathis-nr         LIKE mathis.nr
    FIELD fname             LIKE mathis.fname
    FIELD supplier          LIKE mathis.supplier
    FIELD posted            LIKE fa-artikel.posted
    FIELD fibukonto         LIKE fa-artikel.fibukonto
    FIELD faartikel-nr      LIKE fa-artikel.nr
    FIELD credit-fibu       LIKE fa-artikel.credit-fibu
    FIELD debit-fibu        LIKE fa-artikel.debit-fibu
    FIELD recid-fa-artikel  AS INT
    FIELD recid-mathis      AS INT
    FIELD avail-glacct1     AS LOGICAL   /*ITA 290115*/
    FIELD avail-glacct2     AS LOGICAL   /*ITA 290115*/
    FIELD avail-glacct3     AS LOGICAL    /*ITA 290115*/
    FIELD subgroup          LIKE fa-artikel.subgrp
    FIELD model             LIKE mathis.model       /*MG D5CC23*/
    FIELD gnr               LIKE fa-artikel.gnr     /*MG D5CC23*/
    FIELD flag              LIKE mathis.flag        /*MG D5CC23*/
    FIELD grp-bez           AS CHAR       /*MG D5CC23*/ 
    FIELD sgrp-bez          AS CHAR       /*MG D5CC23*/ 
    FIELD rate              AS DECIMAL    /*MG D5CC23*/ 
    FIELD mark              LIKE mathis.mark  /*MG D5CC23*/ 
    FIELD spec              LIKE mathis.spec  /*MG D5CC23*/ 
    FIELD anz-depn          LIKE fa-artikel.anz-depn  /*MG D5CC23*/ 
    FIELD category          LIKE fa-artikel.katnr  /*Malik*/ 
    FIELD lager-nr          LIKE fa-lager.lager-nr  /*7B132B*/ 

    /* Testing only */
    FIELD isUpgrade         AS CHAR
    .
/**/
DEFINE TEMP-TABLE fibu-list
    FIELD flag      AS   INTEGER INITIAL 0
    FIELD fibukonto LIKE gl-acct.fibukonto
    FIELD bezeich   LIKE gl-acct.bezeich
    FIELD credit    LIKE gl-journal.credit
    FIELD debit     LIKE gl-journal.debit.

DEFINE TEMP-TABLE payload-list
    FIELD from-date             LIKE mathis.datum
    FIELD to-date               LIKE mathis.datum 
    FIELD location              LIKE fa-lager.lager-nr
    FIELD show-all              AS LOGICAL
    FIELD asset-name            AS CHAR
    FIELD remark                AS CHAR
    FIELD asset-number          AS CHAR
    FIELD sorttype              AS INTEGER
    FIELD last-nr               AS INTEGER
    FIELD last-artname          AS CHAR
    FIELD last-remark           AS CHAR
    FIELD last-asset-number     AS CHAR
    FIELD mode                  AS INT
    FIELD num-data              AS INT
    .

DEFINE TEMP-TABLE output-list
    FIELD curr-nr           AS INTEGER
    FIELD curr-loc          AS INTEGER
    FIELD curr-artname      AS CHAR
    FIELD curr-remark       AS CHAR
    FIELD curr-asset-number AS CHAR
    FIELD is-already-six-digit AS LOGICAL.

/* Output temp-table for different modal */
DEFINE TEMP-TABLE t-moving LIKE mathis /* for moving report fix asset */
    FIELD curr-nr           AS INTEGER
    FIELD curr-loc          AS INTEGER
    FIELD curr-artname      AS CHAR
    FIELD curr-remark       AS CHAR
    FIELD curr-asset-number AS CHAR.

DEFINE TEMP-TABLE t-upgrade /* Upgrade Parts - keknya gaperlu*/
    FIELD curr-nr           AS INTEGER
    FIELD curr-loc          AS INTEGER
    FIELD curr-artname      AS CHAR
    FIELD curr-remark       AS CHAR
    FIELD curr-asset-number AS CHAR.

DEFINE TEMP-TABLE t-prepare-creatPO /* prepare Create PO*/
    FIELD curr-nr           AS INTEGER
    FIELD curr-loc          AS INTEGER
    FIELD curr-artname      AS CHAR
    FIELD curr-remark       AS CHAR
    FIELD curr-asset-number AS CHAR.
    

DEF INPUT PARAMETER TABLE FOR payload-list.
DEF OUTPUT PARAMETER p-881 AS DATE.
DEF OUTPUT PARAMETER TABLE FOR q1-list.
DEF OUTPUT PARAMETER TABLE FOR fibu-list.

DEF OUTPUT PARAMETER TABLE FOR output-list.
DEF OUTPUT PARAMETER TABLE FOR t-moving.
DEF OUTPUT PARAMETER TABLE FOR t-upgrade.
DEF OUTPUT PARAMETER TABLE FOR t-prepare-creatPO.


DEFINE BUFFER bfa-grup FOR fa-grup.
DEFINE VARIABLE sort-loc AS CHAR. 
DEFINE VARIABLE counter AS INTEGER INITIAL 0.
DEFINE VARIABLE counter-num-data AS INTEGER INITIAL 0.



RUN htpdate.p (881, OUTPUT p-881).   /* LAST Dep'n DATE */
FIND FIRST payload-list.
CREATE output-list. 

IF payload-list.num-data NE ? AND payload-list.num-data NE 0 THEN
DO:
    counter-num-data = payload-list.num-data.
END.
ELSE
DO:
    counter-num-data = 30.
END.

IF payload-list.mode EQ 1 THEN /* Fixed Asset item List */
DO:
    /* Period */
    IF payload-list.show-all EQ NO THEN
    DO:
        /* asset name */
        IF payload-list.sorttype EQ 1 THEN
        DO:
            IF payload-list.asset-name NE ? AND payload-list.asset-name NE "" THEN
            DO:
                FOR EACH mathis WHERE mathis.datum GE payload-list.from-date
                    AND mathis.datum LE payload-list.to-date AND mathis.name MATCHES("*" + payload-list.asset-name + "*") NO-LOCK, 
                    FIRST fa-artikel WHERE fa-artikel.nr = mathis.nr 
                    AND fa-artikel.loeschflag = 0 NO-LOCK,
                    FIRST fa-grup WHERE fa-grup.gnr = fa-artikel.subgrp AND fa-grup.flag = 1
                    NO-LOCK BY mathis.name:
                    IF (counter GE counter-num-data) AND (output-list.curr-artname NE mathis.name) THEN LEAVE.
                    RUN cr-asset-list.
                    counter = counter + 1.
                    output-list.curr-artname = mathis.name.
                END.
            END.
            ELSE
            DO:
                FOR EACH mathis WHERE mathis.datum GE payload-list.from-date
                    AND mathis.datum LE payload-list.to-date AND mathis.name GE payload-list.asset-name  /*MATCHES("*" + payload-list.asset-name + "*")*/ NO-LOCK, 
                    FIRST fa-artikel WHERE fa-artikel.nr = mathis.nr 
                    AND fa-artikel.loeschflag = 0 NO-LOCK,
                    FIRST fa-grup WHERE fa-grup.gnr = fa-artikel.subgrp AND fa-grup.flag = 1
                    NO-LOCK BY mathis.name:
                    IF (counter GE counter-num-data) AND (output-list.curr-artname NE mathis.name) THEN LEAVE.
                    RUN cr-asset-list.
                    counter = counter + 1.
                    output-list.curr-artname = mathis.name.
                END.
            END.
        END.
        /* remark */
        ELSE IF payload-list.sorttype EQ 2 THEN
        DO:
            IF payload-list.remark NE ? AND payload-list.remark NE "" THEN
            DO:
                FOR EACH mathis WHERE mathis.datum GE payload-list.from-date
                    AND mathis.datum LE payload-list.to-date AND mathis.remark MATCHES("*" + payload-list.remark + "*") NO-LOCK, 
                    FIRST fa-artikel WHERE fa-artikel.nr = mathis.nr 
                    AND fa-artikel.loeschflag = 0 NO-LOCK,
                    FIRST fa-grup WHERE fa-grup.gnr = fa-artikel.subgrp AND fa-grup.flag = 1
                    NO-LOCK BY mathis.remark:
                    IF (counter GE counter-num-data) AND (output-list.curr-remark NE mathis.remark) THEN LEAVE.
                    RUN cr-asset-list.
                    counter = counter + 1.
                    output-list.curr-remark = mathis.remark.
                END.
            END.
            ELSE
            DO:
                /*  
                FOR EACH mathis WHERE mathis.remark GE payload-list.remark /* MATCHES("*" + payload-list.remark + "*") */ NO-LOCK, 
                    FIRST fa-artikel WHERE fa-artikel.nr = mathis.nr 
                    AND fa-artikel.loeschflag = 0 NO-LOCK,
                    FIRST fa-grup WHERE fa-grup.gnr = fa-artikel.subgrp AND fa-grup.flag = 1
                    NO-LOCK BY mathis.remark:
                    /* RUN cr-remark. */
                END. */
                FOR EACH mathis WHERE mathis.datum GE payload-list.from-date
                    AND mathis.datum LE payload-list.to-date AND mathis.remark GE payload-list.remark /* MATCHES("*" + payload-list.remark + "*") */ NO-LOCK, 
                    FIRST fa-artikel WHERE fa-artikel.nr = mathis.nr 
                    AND fa-artikel.loeschflag = 0 NO-LOCK,
                    FIRST fa-grup WHERE fa-grup.gnr = fa-artikel.subgrp AND fa-grup.flag = 1
                    NO-LOCK BY mathis.name:
                    IF (counter GE counter-num-data) AND (output-list.curr-artname NE mathis.name) THEN LEAVE.
                    RUN cr-asset-list.
                    counter = counter + 1.
                    output-list.curr-artname = mathis.name.
                END.
            END.
        END.
        /* location */
        ELSE IF payload-list.sorttype EQ 3 THEN
        DO:
            IF payload-list.location NE ? AND payload-list.location NE 0 THEN
            DO:
                FOR EACH mathis WHERE mathis.datum GE payload-list.from-date
                    AND mathis.datum LE payload-list.to-date NO-LOCK, 
                    FIRST fa-artikel WHERE fa-artikel.nr = mathis.nr 
                    AND fa-artikel.loeschflag = 0 NO-LOCK,
                    FIRST fa-grup WHERE fa-grup.gnr = fa-artikel.subgrp AND fa-grup.flag = 1
                    NO-LOCK BY mathis.nr:
                    FIND FIRST fa-lager WHERE fa-lager.lager-nr = payload-list.location AND fa-lager.bezeich = mathis.location NO-LOCK NO-ERROR.
                    IF AVAILABLE fa-lager THEN
                    DO:
                        IF (counter GE counter-num-data)  AND (output-list.curr-nr NE mathis.nr) /**/ THEN LEAVE.
                        RUN cr-asset-list.
                        counter = counter + 1. 
                        output-list.curr-nr = mathis.nr.
                        output-list.curr-loc = fa-lager.lager-nr.
                    END.
                END.
            END.
            ELSE
            DO:
                FOR EACH mathis WHERE mathis.datum GE payload-list.from-date
                    AND mathis.datum LE payload-list.to-date NO-LOCK, 
                    FIRST fa-artikel WHERE fa-artikel.nr = mathis.nr 
                    AND fa-artikel.loeschflag = 0 NO-LOCK,
                    FIRST fa-grup WHERE fa-grup.gnr = fa-artikel.subgrp AND fa-grup.flag = 1
                    NO-LOCK BY mathis.nr:
                    IF (counter GE counter-num-data)  AND (output-list.curr-nr NE mathis.nr) /**/ THEN LEAVE.
                    RUN cr-asset-list.
                    counter = counter + 1. 
                    output-list.curr-nr = mathis.nr.
                    output-list.curr-loc = fa-lager.lager-nr.
                END.
            END.
        END.
        /* Asset Number */
        ELSE IF payload-list.sorttype EQ 4 THEN
        DO:
            IF payload-list.asset-number NE ? AND payload-list.asset-number NE "" THEN
            DO:
                FOR EACH mathis WHERE mathis.datum GE payload-list.from-date
                    AND mathis.datum LE payload-list.to-date AND mathis.asset MATCHES("*" + TRIM(payload-list.asset-number) + "*") NO-LOCK, 
                    FIRST fa-artikel WHERE fa-artikel.nr = mathis.nr 
                    AND fa-artikel.loeschflag = 0 NO-LOCK,
                    FIRST fa-grup WHERE fa-grup.gnr = fa-artikel.subgrp AND fa-grup.flag = 1
                    NO-LOCK BY mathis.asset:

                    IF (counter GE counter-num-data)  AND (output-list.curr-asset-number NE mathis.asset) /**/ THEN LEAVE.
                    RUN cr-asset-list.
                    counter = counter + 1.
                    output-list.curr-asset-number = mathis.asset.
                END.
            END.
            ELSE
            DO:
                FOR EACH mathis WHERE mathis.datum GE payload-list.from-date
                    AND mathis.datum LE payload-list.to-date AND mathis.asset GT TRIM(payload-list.asset-number) NO-LOCK, 
                    FIRST fa-artikel WHERE fa-artikel.nr = mathis.nr 
                    AND fa-artikel.loeschflag = 0 NO-LOCK,
                    FIRST fa-grup WHERE fa-grup.gnr = fa-artikel.subgrp AND fa-grup.flag = 1
                    NO-LOCK BY mathis.asset:

                    IF (counter GE counter-num-data)  AND (output-list.curr-asset-number NE mathis.asset) /**/ THEN LEAVE.
                    RUN cr-asset-list.
                    counter = counter + 1.
                    output-list.curr-asset-number = mathis.asset.
                END.
            END.
        END.
        /* Api for pagination */
        ELSE
        DO:
            /* Asset Name */
            IF payload-list.last-artname NE "" AND payload-list.last-artname NE ? THEN
            DO:
                IF payload-list.asset-name NE ? AND payload-list.asset-name NE "" THEN
                DO:
                    FOR EACH mathis WHERE mathis.datum GE payload-list.from-date
                        AND mathis.datum LE payload-list.to-date AND mathis.name MATCHES("*" + payload-list.asset-name + "*") AND mathis.name GT payload-list.last-artname NO-LOCK, 
                        FIRST fa-artikel WHERE fa-artikel.nr = mathis.nr 
                        AND fa-artikel.loeschflag = 0 NO-LOCK,
                        FIRST fa-grup WHERE fa-grup.gnr = fa-artikel.subgrp AND fa-grup.flag = 1
                        NO-LOCK BY mathis.name:
                        IF (counter GE counter-num-data) AND (output-list.curr-artname NE mathis.name) THEN LEAVE.
                        RUN cr-asset-list.
                        counter = counter + 1.
                        output-list.curr-artname = mathis.name.
                    END.
                END.
                ELSE
                DO:
                    FOR EACH mathis WHERE mathis.datum GE payload-list.from-date
                        AND mathis.datum LE payload-list.to-date AND mathis.name GT payload-list.last-artname /*MATCHES("*" + payload-list.asset-name + "*")*/ NO-LOCK, 
                        FIRST fa-artikel WHERE fa-artikel.nr = mathis.nr 
                        AND fa-artikel.loeschflag = 0 NO-LOCK,
                        FIRST fa-grup WHERE fa-grup.gnr = fa-artikel.subgrp AND fa-grup.flag = 1
                        NO-LOCK BY mathis.name:
                        IF (counter GE counter-num-data) AND (output-list.curr-artname NE mathis.name) THEN LEAVE.
                        RUN cr-asset-list.
                        counter = counter + 1.
                        output-list.curr-artname = mathis.name.    
                    END.
                END.

            END.

            /* Remark -> mathis.remark GT payload-list.last-remark (Pagination for remark using asset name pagination) */
            IF payload-list.last-remark NE "" AND payload-list.last-remark NE ? THEN
            DO:
                FOR EACH mathis WHERE mathis.remark GT payload-list.last-remark /* MATCHES("*" + payload-list.remark + "*") */ NO-LOCK, 
                    FIRST fa-artikel WHERE fa-artikel.nr = mathis.nr 
                    AND fa-artikel.loeschflag = 0 NO-LOCK,
                    FIRST fa-grup WHERE fa-grup.gnr = fa-artikel.subgrp AND fa-grup.flag = 1
                    NO-LOCK BY mathis.remark:
                    /* FIND FIRST fa-lager WHERE fa-lager.bezeich = mathis.location NO-LOCK NO-ERROR. 
                    RUN cr-remark. 
                    IF counter GE 100 THEN LEAVE.*/
                    IF (counter GE counter-num-data) AND (output-list.curr-artname NE mathis.name) THEN LEAVE.
                    RUN cr-asset-list.
                    counter = counter + 1.
                    output-list.curr-artname = mathis.name. 
                END.
            END. 

            /* Location -> mathis.nr GT payload-list.last-nr, and then check based on location */
            IF payload-list.last-nr NE ? AND payload-list.last-nr NE 0 THEN
            DO:
                IF payload-list.location NE ? AND payload-list.location NE 0 THEN
                DO:
                    FOR EACH mathis WHERE mathis.datum GE payload-list.from-date
                        AND mathis.datum LE payload-list.to-date AND mathis.nr GT payload-list.last-nr NO-LOCK, 
                        FIRST fa-artikel WHERE fa-artikel.nr = mathis.nr 
                        AND fa-artikel.loeschflag = 0 NO-LOCK,
                        FIRST fa-grup WHERE fa-grup.gnr = fa-artikel.subgrp AND fa-grup.flag = 1
                        NO-LOCK BY mathis.nr:
                        FIND FIRST fa-lager WHERE fa-lager.lager-nr = payload-list.location AND fa-lager.bezeich = mathis.location NO-LOCK NO-ERROR.
                        IF AVAILABLE fa-lager THEN
                        DO:
                            IF (counter GE counter-num-data)  AND (output-list.curr-nr NE mathis.nr) /**/ THEN LEAVE.
                            RUN cr-asset-list.
                            counter = counter + 1. 
                            output-list.curr-nr = mathis.nr.
                            output-list.curr-loc = fa-lager.lager-nr.
                        END.
                    END.
                END.
                ELSE
                DO:
                    FOR EACH mathis WHERE mathis.datum GE payload-list.from-date
                        AND mathis.datum LE payload-list.to-date AND mathis.nr GT payload-list.last-nr NO-LOCK, 
                        FIRST fa-artikel WHERE fa-artikel.nr = mathis.nr 
                        AND fa-artikel.loeschflag = 0 NO-LOCK,
                        FIRST fa-grup WHERE fa-grup.gnr = fa-artikel.subgrp AND fa-grup.flag = 1
                        NO-LOCK BY mathis.nr:                      
                        IF (counter GE counter-num-data)  AND (output-list.curr-nr NE mathis.nr) /**/ THEN LEAVE.
                        RUN cr-asset-list.
                        counter = counter + 1. 
                        output-list.curr-nr = mathis.nr.
                        output-list.curr-loc = fa-lager.lager-nr.
                    END.
                END.
            END.

            /* Asset Number */
            IF payload-list.last-asset-number NE ? AND payload-list.last-asset-number NE "" THEN
            DO:
                IF TRIM(payload-list.asset-number) NE ? AND TRIM(payload-list.asset-number) NE "" THEN
                DO:
                    FOR EACH mathis WHERE mathis.datum GE payload-list.from-date
                        AND mathis.datum LE payload-list.to-date 
                        AND mathis.asset GT payload-list.last-asset-number 
                        AND mathis.asset MATCHES("*" + TRIM(payload-list.asset-number) + "*") NO-LOCK, 
                        FIRST fa-artikel WHERE fa-artikel.nr = mathis.nr 
                        AND fa-artikel.loeschflag = 0 NO-LOCK,
                        FIRST fa-grup WHERE fa-grup.gnr = fa-artikel.subgrp AND fa-grup.flag = 1
                        NO-LOCK BY mathis.asset:
                            IF (counter GE counter-num-data)  AND (output-list.curr-asset-number NE mathis.asset) /**/ THEN LEAVE.
                            RUN cr-asset-list.
                            counter = counter + 1.
                            output-list.curr-asset-number = mathis.asset.
                    END.
                END.
                ELSE
                DO:
                    FOR EACH mathis WHERE mathis.datum GE payload-list.from-date
                        AND mathis.datum LE payload-list.to-date AND mathis.asset GT payload-list.last-asset-number NO-LOCK, 
                        FIRST fa-artikel WHERE fa-artikel.nr = mathis.nr 
                        AND fa-artikel.loeschflag = 0 NO-LOCK,
                        FIRST fa-grup WHERE fa-grup.gnr = fa-artikel.subgrp AND fa-grup.flag = 1
                        NO-LOCK BY mathis.asset:
                        IF (counter GE counter-num-data)  AND (output-list.curr-asset-number NE mathis.asset) /**/ THEN LEAVE.
                        RUN cr-asset-list.
                        counter = counter + 1.
                        output-list.curr-asset-number = mathis.asset.
                    END.
                END.
            END.


        END.
    END.
    ELSE
    DO:
        
        /* asset name */
        IF payload-list.sorttype EQ 1 THEN
        DO:
            IF payload-list.asset-name NE ? AND payload-list.asset-name NE "" THEN
            DO:
                FOR EACH mathis WHERE mathis.name MATCHES("*" + payload-list.asset-name + "*") NO-LOCK, 
                    FIRST fa-artikel WHERE fa-artikel.nr = mathis.nr 
                    AND fa-artikel.loeschflag = 0 NO-LOCK,
                    FIRST fa-grup WHERE fa-grup.gnr = fa-artikel.subgrp AND fa-grup.flag = 1
                    NO-LOCK BY mathis.name:
                    IF (counter GE counter-num-data) AND (output-list.curr-artname NE mathis.name) THEN LEAVE.
                    RUN cr-asset-list.
                    counter = counter + 1.
                    output-list.curr-artname = mathis.name.
                END.
            END.
            ELSE
            DO:
                FOR EACH mathis WHERE mathis.name GE payload-list.asset-name  /*MATCHES("*" + payload-list.asset-name + "*")*/ NO-LOCK, 
                    FIRST fa-artikel WHERE fa-artikel.nr = mathis.nr 
                    AND fa-artikel.loeschflag = 0 NO-LOCK,
                    FIRST fa-grup WHERE fa-grup.gnr = fa-artikel.subgrp AND fa-grup.flag = 1
                    NO-LOCK BY mathis.name:
                    IF (counter GE counter-num-data) AND (output-list.curr-artname NE mathis.name) THEN LEAVE.
                    RUN cr-asset-list.
                    counter = counter + 1.
                    output-list.curr-artname = mathis.name.
                END.
            END.
        END.
        /* remark */
        ELSE IF payload-list.sorttype EQ 2 THEN
        DO:
            IF payload-list.remark NE ? AND payload-list.remark NE "" THEN
            DO:
                FOR EACH mathis WHERE mathis.remark MATCHES("*" + payload-list.remark + "*") NO-LOCK, 
                    FIRST fa-artikel WHERE fa-artikel.nr = mathis.nr 
                    AND fa-artikel.loeschflag = 0 NO-LOCK,
                    FIRST fa-grup WHERE fa-grup.gnr = fa-artikel.subgrp AND fa-grup.flag = 1
                    NO-LOCK BY mathis.remark:
                    IF counter GE 100 THEN LEAVE.
                    IF (counter GE counter-num-data) AND (output-list.curr-remark NE mathis.remark) THEN LEAVE.
                    RUN cr-asset-list.
                    counter = counter + 1.
                    output-list.curr-remark = mathis.remark.
                END.
            END.
            ELSE
            DO:
                /*  
                FOR EACH mathis WHERE mathis.remark GE payload-list.remark /* MATCHES("*" + payload-list.remark + "*") */ NO-LOCK, 
                    FIRST fa-artikel WHERE fa-artikel.nr = mathis.nr 
                    AND fa-artikel.loeschflag = 0 NO-LOCK,
                    FIRST fa-grup WHERE fa-grup.gnr = fa-artikel.subgrp AND fa-grup.flag = 1
                    NO-LOCK BY mathis.remark:
                    /* RUN cr-remark. */
                END. */
                FOR EACH mathis WHERE mathis.remark GE payload-list.remark /* MATCHES("*" + payload-list.remark + "*") */ NO-LOCK, 
                    FIRST fa-artikel WHERE fa-artikel.nr = mathis.nr 
                    AND fa-artikel.loeschflag = 0 NO-LOCK,
                    FIRST fa-grup WHERE fa-grup.gnr = fa-artikel.subgrp AND fa-grup.flag = 1
                    NO-LOCK BY mathis.name:
                    IF (counter GE counter-num-data) AND (output-list.curr-artname NE mathis.name) THEN LEAVE.
                    RUN cr-asset-list.
                    counter = counter + 1.
                    output-list.curr-artname = mathis.name.
                END.
            END.
        END.
        /* location */
        ELSE IF payload-list.sorttype EQ 3 THEN
        DO:
            IF payload-list.location NE ? AND payload-list.location NE 0 THEN
            DO:
                FOR EACH mathis NO-LOCK, 
                    FIRST fa-artikel WHERE fa-artikel.nr = mathis.nr 
                    AND fa-artikel.loeschflag = 0 NO-LOCK,
                    FIRST fa-grup WHERE fa-grup.gnr = fa-artikel.subgrp AND fa-grup.flag = 1
                    NO-LOCK BY mathis.nr:
                    FIND FIRST fa-lager WHERE fa-lager.lager-nr = payload-list.location AND fa-lager.bezeich = mathis.location NO-LOCK NO-ERROR.
                    IF AVAILABLE fa-lager THEN
                    DO:
                        IF (counter GE counter-num-data)  AND (output-list.curr-nr NE mathis.nr) /**/ THEN LEAVE.
                        RUN cr-asset-list.
                        counter = counter + 1. 
                        output-list.curr-nr = mathis.nr.
                        output-list.curr-loc = fa-lager.lager-nr.
                    END.
                END.
            END.
            ELSE
            DO:
                FOR EACH mathis NO-LOCK, 
                    FIRST fa-artikel WHERE fa-artikel.nr = mathis.nr 
                    AND fa-artikel.loeschflag = 0 NO-LOCK,
                    FIRST fa-grup WHERE fa-grup.gnr = fa-artikel.subgrp AND fa-grup.flag = 1
                    NO-LOCK BY mathis.nr:
                    IF (counter GE counter-num-data)  AND (output-list.curr-nr NE mathis.nr) /**/ THEN LEAVE.
                    RUN cr-asset-list.
                    counter = counter + 1. 
                    output-list.curr-nr = mathis.nr.
                    output-list.curr-loc = fa-lager.lager-nr.
                END.
            END.
        END.
        /* Asset Number */
        ELSE IF payload-list.sorttype EQ 4 THEN
        DO:
            IF payload-list.asset-number NE ? AND payload-list.asset-number NE "" THEN
            DO:
                FOR EACH mathis WHERE mathis.asset MATCHES("*" + TRIM(payload-list.asset-number) + "*") NO-LOCK, 
                    FIRST fa-artikel WHERE fa-artikel.nr = mathis.nr 
                    AND fa-artikel.loeschflag = 0 NO-LOCK,
                    FIRST fa-grup WHERE fa-grup.gnr = fa-artikel.subgrp AND fa-grup.flag = 1
                    NO-LOCK BY mathis.asset /*INTEGER(mathis.asset)*/:

                    IF (counter GE counter-num-data)  AND (output-list.curr-asset-number NE mathis.asset) /**/ THEN LEAVE.
                    RUN cr-asset-list.
                    counter = counter + 1.
                    output-list.curr-asset-number = mathis.asset.
                END.
            END.
            ELSE
            DO:
                FOR EACH mathis WHERE mathis.asset GT TRIM(payload-list.asset-number) NO-LOCK, 
                    FIRST fa-artikel WHERE fa-artikel.nr = mathis.nr 
                    AND fa-artikel.loeschflag = 0 NO-LOCK,
                    FIRST fa-grup WHERE fa-grup.gnr = fa-artikel.subgrp AND fa-grup.flag = 1
                    NO-LOCK BY mathis.asset /*INTEGER(mathis.asset)*/:

                    IF (counter GE counter-num-data)  AND (output-list.curr-asset-number NE mathis.asset) /**/ THEN LEAVE.
                    RUN cr-asset-list.
                    counter = counter + 1.
                    output-list.curr-asset-number = mathis.asset.
                END.
            END.
        END.
        /* All Assets */
        ELSE IF payload-list.sorttype EQ 6 THEN
        DO:
            FOR EACH mathis NO-LOCK, 
                FIRST fa-artikel WHERE fa-artikel.nr = mathis.nr 
                AND fa-artikel.loeschflag = 0 NO-LOCK,
                FIRST fa-grup WHERE fa-grup.gnr = fa-artikel.subgrp AND fa-grup.flag = 1
                NO-LOCK BY mathis.name:
                    RUN cr-asset-list.
            END.
        END.
        /* Api for pagination */
        ELSE
        DO:
            /* Asset Name */
            IF payload-list.last-artname NE "" AND payload-list.last-artname NE ? THEN
            DO:
                IF payload-list.asset-name NE ? AND payload-list.asset-name NE "" THEN
                DO:
                    FOR EACH mathis WHERE mathis.name MATCHES("*" + payload-list.asset-name + "*") AND mathis.name GT payload-list.last-artname NO-LOCK, 
                        FIRST fa-artikel WHERE fa-artikel.nr = mathis.nr 
                        AND fa-artikel.loeschflag = 0 NO-LOCK,
                        FIRST fa-grup WHERE fa-grup.gnr = fa-artikel.subgrp AND fa-grup.flag = 1
                        NO-LOCK BY mathis.name:
                        IF (counter GE counter-num-data) AND (output-list.curr-artname NE mathis.name) THEN LEAVE.
                        RUN cr-asset-list.
                        counter = counter + 1.
                        output-list.curr-artname = mathis.name.
                    END.
                END.
                ELSE
                DO:
                    FOR EACH mathis WHERE mathis.name GT payload-list.last-artname /*MATCHES("*" + payload-list.asset-name + "*")*/ NO-LOCK, 
                        FIRST fa-artikel WHERE fa-artikel.nr = mathis.nr 
                        AND fa-artikel.loeschflag = 0 NO-LOCK,
                        FIRST fa-grup WHERE fa-grup.gnr = fa-artikel.subgrp AND fa-grup.flag = 1
                        NO-LOCK BY mathis.name:
                        IF (counter GE counter-num-data) AND (output-list.curr-artname NE mathis.name) THEN LEAVE.
                        RUN cr-asset-list.
                        counter = counter + 1.
                        output-list.curr-artname = mathis.name.    
                    END.
                END.

            END.

            /* Remark -> mathis.remark GT payload-list.last-remark (Pagination for remark using asset name pagination) */
            IF payload-list.last-remark NE "" AND payload-list.last-remark NE ? THEN
            DO:
                FOR EACH mathis WHERE mathis.remark GT payload-list.last-remark /* MATCHES("*" + payload-list.remark + "*") */ NO-LOCK, 
                    FIRST fa-artikel WHERE fa-artikel.nr = mathis.nr 
                    AND fa-artikel.loeschflag = 0 NO-LOCK,
                    FIRST fa-grup WHERE fa-grup.gnr = fa-artikel.subgrp AND fa-grup.flag = 1
                    NO-LOCK BY mathis.remark:
                   /* FIND FIRST fa-lager WHERE fa-lager.bezeich = mathis.location NO-LOCK NO-ERROR. 
                    RUN cr-remark. 
                    IF counter GE 100 THEN LEAVE.*/
                    IF (counter GE counter-num-data) AND (output-list.curr-artname NE mathis.name) THEN LEAVE.
                    RUN cr-asset-list.
                    counter = counter + 1.
                    output-list.curr-artname = mathis.name. 
                END.
            END. 

            /* Location -> mathis.nr GT payload-list.last-nr, and then check based on location */
            IF payload-list.last-nr NE ? AND payload-list.last-nr NE 0 THEN
            DO:
                IF payload-list.location NE ? AND payload-list.location NE 0 THEN
                DO:
                    FOR EACH mathis WHERE mathis.nr GT payload-list.last-nr NO-LOCK, 
                        FIRST fa-artikel WHERE fa-artikel.nr = mathis.nr 
                        AND fa-artikel.loeschflag = 0 NO-LOCK,
                        FIRST fa-grup WHERE fa-grup.gnr = fa-artikel.subgrp AND fa-grup.flag = 1
                        NO-LOCK BY mathis.nr:
                        FIND FIRST fa-lager WHERE fa-lager.lager-nr = payload-list.location AND fa-lager.bezeich = mathis.location NO-LOCK NO-ERROR.
                        IF AVAILABLE fa-lager THEN
                        DO:
                            IF (counter GE counter-num-data)  AND (output-list.curr-nr NE mathis.nr) /**/ THEN LEAVE.
                            RUN cr-asset-list.
                            counter = counter + 1. 
                            output-list.curr-nr = mathis.nr.
                            output-list.curr-loc = fa-lager.lager-nr.
                        END.
                    END.
                END.
                ELSE
                DO:
                    FOR EACH mathis WHERE mathis.nr GT payload-list.last-nr NO-LOCK, 
                        FIRST fa-artikel WHERE fa-artikel.nr = mathis.nr 
                        AND fa-artikel.loeschflag = 0 NO-LOCK,
                        FIRST fa-grup WHERE fa-grup.gnr = fa-artikel.subgrp AND fa-grup.flag = 1
                        NO-LOCK BY mathis.nr:                      
                        IF (counter GE counter-num-data)  AND (output-list.curr-nr NE mathis.nr) /**/ THEN LEAVE.
                        RUN cr-asset-list.
                        counter = counter + 1. 
                        output-list.curr-nr = mathis.nr.
                        output-list.curr-loc = fa-lager.lager-nr.
                    END.
                END.
            END.

            /* Asset Number */
            IF payload-list.last-asset-number NE ? AND payload-list.last-asset-number NE "" THEN
            DO:
                IF TRIM(payload-list.asset-number) NE ? AND TRIM(payload-list.asset-number) NE "" THEN
                DO:
                    FOR EACH mathis WHERE mathis.asset GT payload-list.last-asset-number AND mathis.asset MATCHES("*" + TRIM(payload-list.asset-number) + "*") /*INTEGER(mathis.asset) GT INTEGER(payload-list.last-asset-number)*/ NO-LOCK, 
                        FIRST fa-artikel WHERE fa-artikel.nr = mathis.nr 
                        AND fa-artikel.loeschflag = 0 NO-LOCK,
                        FIRST fa-grup WHERE fa-grup.gnr = fa-artikel.subgrp AND fa-grup.flag = 1
                        NO-LOCK BY mathis.asset /*INTEGER(mathis.asset)*/:
                        IF (counter GE counter-num-data)  AND (output-list.curr-asset-number NE mathis.asset) /**/ THEN LEAVE.
                        RUN cr-asset-list.
                        counter = counter + 1.
                        output-list.curr-asset-number = mathis.asset.
                    END.
                END.
                ELSE
                DO:
                    FOR EACH mathis WHERE mathis.asset GT payload-list.last-asset-number /*INTEGER(mathis.asset) GT INTEGER(payload-list.last-asset-number)*/ NO-LOCK, 
                        FIRST fa-artikel WHERE fa-artikel.nr = mathis.nr 
                        AND fa-artikel.loeschflag = 0 NO-LOCK,
                        FIRST fa-grup WHERE fa-grup.gnr = fa-artikel.subgrp AND fa-grup.flag = 1
                        NO-LOCK BY mathis.asset /*INTEGER(mathis.asset)*/:
                        IF (counter GE counter-num-data)  AND (output-list.curr-asset-number NE mathis.asset) /**/ THEN LEAVE.
                        RUN cr-asset-list.
                        counter = counter + 1.
                        output-list.curr-asset-number = mathis.asset.
                    END.
                END.
            END.
        END.
    END.
END.
ELSE IF payload-list.mode EQ 2 THEN /* Dialog Copy Fix asset */
DO:
    /* asset name */
    IF payload-list.sorttype EQ 1 THEN
    DO:
        IF payload-list.asset-name NE ? AND payload-list.asset-name NE "" THEN
        DO:
            FOR EACH mathis WHERE mathis.name MATCHES("*" + payload-list.asset-name + "*") NO-LOCK, 
                FIRST fa-artikel WHERE fa-artikel.nr = mathis.nr 
                AND fa-artikel.loeschflag = 0 NO-LOCK,
                FIRST fa-grup WHERE fa-grup.gnr = fa-artikel.subgrp AND fa-grup.flag = 1
                NO-LOCK BY mathis.name:
                IF (counter GE counter-num-data) AND (output-list.curr-artname NE mathis.name) THEN LEAVE.
                RUN cr-asset-list.
                counter = counter + 1.
                output-list.curr-artname = mathis.name.   
            END.
        END.
        ELSE
        DO:
            FOR EACH mathis WHERE mathis.name GE payload-list.asset-name  /*MATCHES("*" + payload-list.asset-name + "*")*/ NO-LOCK, 
                FIRST fa-artikel WHERE fa-artikel.nr = mathis.nr 
                AND fa-artikel.loeschflag = 0 NO-LOCK,
                FIRST fa-grup WHERE fa-grup.gnr = fa-artikel.subgrp AND fa-grup.flag = 1
                NO-LOCK BY mathis.name:
                IF (counter GE counter-num-data) AND (output-list.curr-artname NE mathis.name) THEN LEAVE.
                RUN cr-asset-list.
                counter = counter + 1.
                output-list.curr-artname = mathis.name.   
            END.
        END.
    END.
    ELSE
    DO:
        IF payload-list.last-artname NE "" AND payload-list.last-artname NE ? THEN
        DO:
            IF payload-list.asset-name NE ? AND payload-list.asset-name NE "" THEN
            DO:
                FOR EACH mathis WHERE mathis.name MATCHES("*" + payload-list.asset-name + "*") AND mathis.name GT payload-list.last-artname NO-LOCK, 
                    FIRST fa-artikel WHERE fa-artikel.nr = mathis.nr 
                    AND fa-artikel.loeschflag = 0 NO-LOCK,
                    FIRST fa-grup WHERE fa-grup.gnr = fa-artikel.subgrp AND fa-grup.flag = 1
                    NO-LOCK BY mathis.name:
                    IF (counter GE counter-num-data) AND (output-list.curr-artname NE mathis.name) THEN LEAVE.
                    RUN cr-asset-list.
                    counter = counter + 1.
                    output-list.curr-artname = mathis.name.
                END.
            END.
            ELSE
            DO:
                FOR EACH mathis WHERE mathis.name GT payload-list.last-artname /*MATCHES("*" + payload-list.asset-name + "*")*/ NO-LOCK, 
                    FIRST fa-artikel WHERE fa-artikel.nr = mathis.nr 
                    AND fa-artikel.loeschflag = 0 NO-LOCK,
                    FIRST fa-grup WHERE fa-grup.gnr = fa-artikel.subgrp AND fa-grup.flag = 1
                    NO-LOCK BY mathis.name:
                    IF (counter GE counter-num-data) AND (output-list.curr-artname NE mathis.name) THEN LEAVE.
                    RUN cr-asset-list.
                    counter = counter + 1.
                    output-list.curr-artname = mathis.name.    
                END.
            END.
        END.
    END.

   
END.
ELSE IF payload-list.mode EQ 3 THEN /* Dialog Moving Asset */
DO:
    /* asset name */
    IF payload-list.sorttype EQ 1 THEN
    DO:
        IF payload-list.asset-name NE ? AND payload-list.asset-name NE "" THEN
        DO:
            FOR EACH mathis WHERE mathis.name MATCHES("*" + payload-list.asset-name + "*") NO-LOCK BY mathis.name: 
                IF (counter GE counter-num-data) AND (output-list.curr-artname NE mathis.name) THEN LEAVE.
                CREATE t-moving.
                BUFFER-COPY mathis TO t-moving.
                counter = counter + 1.
                output-list.curr-artname = mathis.name.
            END.
        END.
        ELSE
        DO:
            FOR EACH mathis WHERE mathis.name GE payload-list.asset-name NO-LOCK BY mathis.name:
                IF (counter GE counter-num-data) AND (output-list.curr-artname NE mathis.name) THEN LEAVE.
                CREATE t-moving.
                BUFFER-COPY mathis TO t-moving.
                counter = counter + 1.
                output-list.curr-artname = mathis.name.
            END.
        END.
    END.
    ELSE
    DO:
        IF payload-list.last-artname NE "" AND payload-list.last-artname NE ? THEN
        DO:
            IF payload-list.asset-name NE ? AND payload-list.asset-name NE "" THEN
            DO:
                FOR EACH mathis WHERE mathis.name MATCHES("*" + payload-list.asset-name + "*") 
                    AND mathis.name GT payload-list.last-artname NO-LOCK BY mathis.name: 
                    IF (counter GE counter-num-data) AND (output-list.curr-artname NE mathis.name) THEN LEAVE.
                    CREATE t-moving.
                    BUFFER-COPY mathis TO t-moving.
                    counter = counter + 1.
                    output-list.curr-artname = mathis.name.
                END.
            END.
            ELSE
            DO:
                FOR EACH mathis WHERE mathis.name GT payload-list.last-artname NO-LOCK BY mathis.name: 
                    IF (counter GE counter-num-data) AND (output-list.curr-artname NE mathis.name) THEN LEAVE.
                    CREATE t-moving.
                    BUFFER-COPY mathis TO t-moving.
                    counter = counter + 1.
                    output-list.curr-artname = mathis.name.
                END.
            END.
        END.
    END.
END.
ELSE IF payload-list.mode EQ 4 THEN /* Validation for digit number once 6 cant go to 4 digit */
DO:
    FIND FIRST mathis WHERE mathis.flag NE 0 AND LENGTH(TRIM(mathis.asset)) GT 10 NO-LOCK NO-ERROR.
    IF AVAILABLE mathis THEN
    DO:
        ASSIGN
            output-list.is-already-six-digit = YES.
    END.
END.
ELSE IF payload-list.mode EQ 5 THEN /* Query All Asset and enable filter without pagination */
DO:
    /* Period */
    IF payload-list.show-all EQ NO THEN
    DO:
        /* asset name */
        IF payload-list.sorttype EQ 1 THEN
        DO:
            IF payload-list.asset-name NE ? AND payload-list.asset-name NE "" THEN
            DO:
                FOR EACH mathis WHERE mathis.datum GE payload-list.from-date
                    AND mathis.datum LE payload-list.to-date AND mathis.name MATCHES("*" + payload-list.asset-name + "*") NO-LOCK, 
                    FIRST fa-artikel WHERE fa-artikel.nr = mathis.nr 
                    AND fa-artikel.loeschflag = 0 NO-LOCK,
                    FIRST fa-grup WHERE fa-grup.gnr = fa-artikel.subgrp AND fa-grup.flag = 1
                    NO-LOCK BY mathis.name:
                    RUN cr-asset-list.
                END.
            END.
            ELSE
            DO:
                FOR EACH mathis WHERE mathis.datum GE payload-list.from-date
                    AND mathis.datum LE payload-list.to-date AND mathis.name GE payload-list.asset-name  /*MATCHES("*" + payload-list.asset-name + "*")*/ NO-LOCK, 
                    FIRST fa-artikel WHERE fa-artikel.nr = mathis.nr 
                    AND fa-artikel.loeschflag = 0 NO-LOCK,
                    FIRST fa-grup WHERE fa-grup.gnr = fa-artikel.subgrp AND fa-grup.flag = 1
                    NO-LOCK BY mathis.name:
                    RUN cr-asset-list.
                END.
            END.
        END.
        /* remark */
        ELSE IF payload-list.sorttype EQ 2 THEN
        DO:
            IF payload-list.remark NE ? AND payload-list.remark NE "" THEN
            DO:
                FOR EACH mathis WHERE mathis.datum GE payload-list.from-date
                    AND mathis.datum LE payload-list.to-date AND mathis.remark MATCHES("*" + payload-list.remark + "*") NO-LOCK, 
                    FIRST fa-artikel WHERE fa-artikel.nr = mathis.nr 
                    AND fa-artikel.loeschflag = 0 NO-LOCK,
                    FIRST fa-grup WHERE fa-grup.gnr = fa-artikel.subgrp AND fa-grup.flag = 1
                    NO-LOCK BY mathis.remark:
                    RUN cr-asset-list.
                END.
            END.
            ELSE
            DO:
                /*  
                FOR EACH mathis WHERE mathis.remark GE payload-list.remark /* MATCHES("*" + payload-list.remark + "*") */ NO-LOCK, 
                    FIRST fa-artikel WHERE fa-artikel.nr = mathis.nr 
                    AND fa-artikel.loeschflag = 0 NO-LOCK,
                    FIRST fa-grup WHERE fa-grup.gnr = fa-artikel.subgrp AND fa-grup.flag = 1
                    NO-LOCK BY mathis.remark:
                    /* RUN cr-remark. */
                END. */
                FOR EACH mathis WHERE mathis.datum GE payload-list.from-date
                    AND mathis.datum LE payload-list.to-date AND mathis.remark GE payload-list.remark /* MATCHES("*" + payload-list.remark + "*") */ NO-LOCK, 
                    FIRST fa-artikel WHERE fa-artikel.nr = mathis.nr 
                    AND fa-artikel.loeschflag = 0 NO-LOCK,
                    FIRST fa-grup WHERE fa-grup.gnr = fa-artikel.subgrp AND fa-grup.flag = 1
                    NO-LOCK BY mathis.name:
                    RUN cr-asset-list.
                END.
            END.
        END.
        /* location */
        ELSE IF payload-list.sorttype EQ 3 THEN
        DO:
            IF payload-list.location NE ? AND payload-list.location NE 0 THEN
            DO:
                FOR EACH mathis WHERE mathis.datum GE payload-list.from-date
                    AND mathis.datum LE payload-list.to-date NO-LOCK, 
                    FIRST fa-artikel WHERE fa-artikel.nr = mathis.nr 
                    AND fa-artikel.loeschflag = 0 NO-LOCK,
                    FIRST fa-grup WHERE fa-grup.gnr = fa-artikel.subgrp AND fa-grup.flag = 1
                    NO-LOCK BY mathis.nr:
                    FIND FIRST fa-lager WHERE fa-lager.lager-nr = payload-list.location AND fa-lager.bezeich = mathis.location NO-LOCK NO-ERROR.
                    IF AVAILABLE fa-lager THEN
                    DO:
                        RUN cr-asset-list.
                    END.
                END.
            END.
            ELSE
            DO:
                FOR EACH mathis WHERE mathis.datum GE payload-list.from-date
                    AND mathis.datum LE payload-list.to-date NO-LOCK, 
                    FIRST fa-artikel WHERE fa-artikel.nr = mathis.nr 
                    AND fa-artikel.loeschflag = 0 NO-LOCK,
                    FIRST fa-grup WHERE fa-grup.gnr = fa-artikel.subgrp AND fa-grup.flag = 1
                    NO-LOCK BY mathis.nr:
                    RUN cr-asset-list.
                END.
            END.
        END.
        /* Asset Number */
        ELSE IF payload-list.sorttype EQ 4 THEN
        DO:
            IF payload-list.asset-number NE ? AND payload-list.asset-number NE "" THEN
            DO:
                FOR EACH mathis WHERE mathis.datum GE payload-list.from-date
                    AND mathis.datum LE payload-list.to-date AND mathis.asset MATCHES("*" + TRIM(payload-list.asset-number) + "*") NO-LOCK, 
                    FIRST fa-artikel WHERE fa-artikel.nr = mathis.nr 
                    AND fa-artikel.loeschflag = 0 NO-LOCK,
                    FIRST fa-grup WHERE fa-grup.gnr = fa-artikel.subgrp AND fa-grup.flag = 1
                    NO-LOCK BY mathis.asset:
                    RUN cr-asset-list.
                END.
            END.
            ELSE
            DO:
                FOR EACH mathis WHERE mathis.datum GE payload-list.from-date
                    AND mathis.datum LE payload-list.to-date AND mathis.asset GT TRIM(payload-list.asset-number) NO-LOCK, 
                    FIRST fa-artikel WHERE fa-artikel.nr = mathis.nr 
                    AND fa-artikel.loeschflag = 0 NO-LOCK,
                    FIRST fa-grup WHERE fa-grup.gnr = fa-artikel.subgrp AND fa-grup.flag = 1
                    NO-LOCK BY mathis.asset:
                    RUN cr-asset-list.
                END.
            END.
        END.
    END.
    ELSE
    DO:
        /* asset name */
        IF payload-list.sorttype EQ 1 THEN
        DO:
            IF payload-list.asset-name NE ? AND payload-list.asset-name NE "" THEN
            DO:
                FOR EACH mathis WHERE mathis.name MATCHES("*" + payload-list.asset-name + "*") NO-LOCK, 
                    FIRST fa-artikel WHERE fa-artikel.nr = mathis.nr 
                    AND fa-artikel.loeschflag = 0 NO-LOCK,
                    FIRST fa-grup WHERE fa-grup.gnr = fa-artikel.subgrp AND fa-grup.flag = 1
                    NO-LOCK BY mathis.name:
                    RUN cr-asset-list.
                END.
            END.
            ELSE
            DO:
                FOR EACH mathis WHERE mathis.name GE payload-list.asset-name  /*MATCHES("*" + payload-list.asset-name + "*")*/ NO-LOCK, 
                    FIRST fa-artikel WHERE fa-artikel.nr = mathis.nr 
                    AND fa-artikel.loeschflag = 0 NO-LOCK,
                    FIRST fa-grup WHERE fa-grup.gnr = fa-artikel.subgrp AND fa-grup.flag = 1
                    NO-LOCK BY mathis.name:
                    RUN cr-asset-list.
                END.
            END.
        END.
        /* remark */
        ELSE IF payload-list.sorttype EQ 2 THEN
        DO:
            IF payload-list.remark NE ? AND payload-list.remark NE "" THEN
            DO:
                FOR EACH mathis WHERE mathis.remark MATCHES("*" + payload-list.remark + "*") NO-LOCK, 
                    FIRST fa-artikel WHERE fa-artikel.nr = mathis.nr 
                    AND fa-artikel.loeschflag = 0 NO-LOCK,
                    FIRST fa-grup WHERE fa-grup.gnr = fa-artikel.subgrp AND fa-grup.flag = 1
                    NO-LOCK BY mathis.remark:
                    RUN cr-asset-list.
                END.
            END.
            ELSE
            DO:
                /*  
                FOR EACH mathis WHERE mathis.remark GE payload-list.remark /* MATCHES("*" + payload-list.remark + "*") */ NO-LOCK, 
                    FIRST fa-artikel WHERE fa-artikel.nr = mathis.nr 
                    AND fa-artikel.loeschflag = 0 NO-LOCK,
                    FIRST fa-grup WHERE fa-grup.gnr = fa-artikel.subgrp AND fa-grup.flag = 1
                    NO-LOCK BY mathis.remark:
                    /* RUN cr-remark. */
                END. */
                FOR EACH mathis WHERE mathis.remark GE payload-list.remark /* MATCHES("*" + payload-list.remark + "*") */ NO-LOCK, 
                    FIRST fa-artikel WHERE fa-artikel.nr = mathis.nr 
                    AND fa-artikel.loeschflag = 0 NO-LOCK,
                    FIRST fa-grup WHERE fa-grup.gnr = fa-artikel.subgrp AND fa-grup.flag = 1
                    NO-LOCK BY mathis.name:
                    RUN cr-asset-list.
                END.
            END.
        END.
        /* location */
        ELSE IF payload-list.sorttype EQ 3 THEN
        DO:
            IF payload-list.location NE ? AND payload-list.location NE 0 THEN
            DO:
                FOR EACH mathis NO-LOCK, 
                    FIRST fa-artikel WHERE fa-artikel.nr = mathis.nr 
                    AND fa-artikel.loeschflag = 0 NO-LOCK,
                    FIRST fa-grup WHERE fa-grup.gnr = fa-artikel.subgrp AND fa-grup.flag = 1
                    NO-LOCK BY mathis.nr:
                    FIND FIRST fa-lager WHERE fa-lager.lager-nr = payload-list.location AND fa-lager.bezeich = mathis.location NO-LOCK NO-ERROR.
                    IF AVAILABLE fa-lager THEN
                    DO:
                        RUN cr-asset-list.
                    END.
                END.
            END.
            ELSE
            DO:
                FOR EACH mathis NO-LOCK, 
                    FIRST fa-artikel WHERE fa-artikel.nr = mathis.nr 
                    AND fa-artikel.loeschflag = 0 NO-LOCK,
                    FIRST fa-grup WHERE fa-grup.gnr = fa-artikel.subgrp AND fa-grup.flag = 1
                    NO-LOCK BY mathis.nr:
                    RUN cr-asset-list.
                END.
            END.
        END.
        /* Asset Number */
        ELSE IF payload-list.sorttype EQ 4 THEN
        DO:
            IF payload-list.asset-number NE ? AND payload-list.asset-number NE "" THEN
            DO:
                FOR EACH mathis WHERE mathis.asset MATCHES("*" + TRIM(payload-list.asset-number) + "*") NO-LOCK, 
                    FIRST fa-artikel WHERE fa-artikel.nr = mathis.nr 
                    AND fa-artikel.loeschflag = 0 NO-LOCK,
                    FIRST fa-grup WHERE fa-grup.gnr = fa-artikel.subgrp AND fa-grup.flag = 1
                    NO-LOCK BY mathis.asset /*INTEGER(mathis.asset)*/:
                    RUN cr-asset-list.
                END.
            END.
            ELSE
            DO:
                FOR EACH mathis WHERE mathis.asset GT TRIM(payload-list.asset-number) NO-LOCK, 
                    FIRST fa-artikel WHERE fa-artikel.nr = mathis.nr 
                    AND fa-artikel.loeschflag = 0 NO-LOCK,
                    FIRST fa-grup WHERE fa-grup.gnr = fa-artikel.subgrp AND fa-grup.flag = 1
                    NO-LOCK BY mathis.asset /*INTEGER(mathis.asset)*/:
                    RUN cr-asset-list.
                END.
            END.
        END.
        /* All Assets */
        ELSE IF payload-list.sorttype EQ 5 THEN
        DO:
            FOR EACH mathis NO-LOCK, 
                FIRST fa-artikel WHERE fa-artikel.nr = mathis.nr 
                AND fa-artikel.loeschflag = 0 NO-LOCK,
                FIRST fa-grup WHERE fa-grup.gnr = fa-artikel.subgrp AND fa-grup.flag = 1
                NO-LOCK BY mathis.name:
                    RUN cr-asset-list.
            END.
        END.
    END.   

END.

PROCEDURE cr-assetname :
    CREATE q1-list.
    ASSIGN
        q1-list.name       = mathis.name
        q1-list.asset      = mathis.asset
        q1-list.datum      = mathis.datum
        q1-list.price      = mathis.price
        q1-list.anzahl     = fa-artikel.anzahl
        q1-list.warenwert  = fa-artikel.warenwert
        q1-list.depn-wert  = fa-artikel.depn-wert
        q1-list.book-wert  = fa-artikel.book-wert
        q1-list.katnr      = fa-artikel.katnr
        q1-list.bezeich    = fa-grup.bezeich
        q1-list.location   = mathis.location
        q1-list.first-depn = fa-artikel.first-depn
        q1-list.next-depn  = fa-artikel.next-depn
        q1-list.last-depn  = fa-artikel.last-depn
        q1-list.id         = fa-artikel.id
        q1-list.created    = fa-artikel.created
        q1-list.cid        = fa-artikel.cid
        q1-list.changed    = fa-artikel.changed
        q1-list.remark     = mathis.remark
            
        q1-list.mathis-nr  = mathis.nr
        q1-list.fname      = mathis.fname
        q1-list.supplier   = mathis.supplier
        q1-list.posted     = fa-artikel.posted
        q1-list.fibukonto  = fa-artikel.fibukonto
        q1-list.faartikel-nr  = fa-artikel.nr
        q1-list.credit-fibu = fa-artikel.credit-fibu
        q1-list.debit-fibu  = fa-artikel.debit-fibu
        q1-list.recid-fa-artikel = RECID(fa-artikel)
        q1-list.recid-mathis     = RECID(mathis)
        q1-list.subgroup    = fa-artikel.subgrp
        q1-list.gnr         = fa-artikel.gnr
        q1-list.model       = mathis.model
        q1-list.flag        = mathis.flag
        q1-list.mark        = mathis.mark
        q1-list.spec        = mathis.spec
        q1-list.anz-depn    = fa-artikel.anz-depn
        q1-list.category    = fa-artikel.katnr.
        /*q1-list.curr-artname-q1 = 
         q1-list.lager-nr    = fa-lager.lager-nr. */
    FIND FIRST bfa-grup WHERE bfa-grup.gnr = fa-artikel.gnr AND bfa-grup.flag = 0 NO-LOCK NO-ERROR.
    IF AVAILABLE bfa-grup THEN ASSIGN q1-list.grp-bez = bfa-grup.bezeic.
    FIND FIRST bfa-grup WHERE bfa-grup.gnr = fa-artikel.subgrp AND bfa-grup.flag GT 0 NO-LOCK NO-ERROR.
    IF AVAILABLE bfa-grup THEN ASSIGN q1-list.sgrp-bez = bfa-grup.bezeic.
    FIND FIRST fa-kateg WHERE fa-kateg.katnr = fa-artikel.katnr NO-LOCK NO-ERROR.
    IF AVAILABLE fa-kateg THEN q1-list.rate = fa-kateg.rat.
    /*ITA 290115*/
    FIND FIRST fibu-list WHERE fibu-list.fibukonto = fa-grup.fibukonto
        NO-ERROR.
    IF NOT AVAILABLE fibu-list THEN
    DO:
        FIND FIRST gl-acct WHERE gl-acct.fibukonto = fa-grup.fibukonto NO-LOCK
            NO-ERROR.
        IF NOT AVAILABLE gl-acct THEN 
        DO: 
            ASSIGN q1-list.avail-glacct1 = YES.
        END.
        ELSE DO:
            CREATE fibu-list.
            ASSIGN fibu-list.fibukonto = fa-grup.fibukonto
                    fibu-list.bezeich   = gl-acct.bezeich
                    fibu-list.flag      = 1.
        END.
    END.
    IF q1-list.avail-glacct1 = NO THEN 
        ASSIGN fibu-list.debit = fibu-list.debit + fa-artikel.warenwert.
    
    FIND FIRST fibu-list WHERE fibu-list.fibukonto = fa-grup.credit-fibu
        NO-ERROR.
    IF NOT AVAILABLE fibu-list THEN
    DO:
        FIND FIRST gl-acct WHERE gl-acct.fibukonto = fa-grup.credit-fibu NO-LOCK
            NO-ERROR.
        IF NOT AVAILABLE gl-acct THEN 
        DO: 
            ASSIGN q1-list.avail-glacct2 = YES.
        END.
        ELSE DO:
            CREATE fibu-list.
            ASSIGN fibu-list.fibukonto = fa-grup.credit-fibu
                    fibu-list.bezeich   = gl-acct.bezeich
                    fibu-list.flag      = 2.
        END.
    END.
    IF q1-list.avail-glacct2 = NO THEN 
        ASSIGN fibu-list.credit = fibu-list.credit + fa-artikel.depn-wert.
    
    FIND FIRST fibu-list WHERE fibu-list.fibukonto = fa-grup.debit-fibu
        NO-ERROR.
    IF NOT AVAILABLE fibu-list THEN
    DO:
        FIND FIRST gl-acct WHERE gl-acct.fibukonto = fa-grup.debit-fibu NO-LOCK
            NO-ERROR.
        IF NOT AVAILABLE gl-acct THEN 
        DO: 
            ASSIGN q1-list.avail-glacct3 = YES.
        END.
        ELSE DO:
            CREATE fibu-list.
            ASSIGN fibu-list.fibukonto = fa-grup.debit-fibu
                    fibu-list.bezeich   = gl-acct.bezeich
                    fibu-list.flag      = 3.
        END.
    END.
    IF q1-list.avail-glacct3 = NO THEN 
        ASSIGN fibu-list.debit = fibu-list.debit + fa-artikel.depn-wert.
    /**end*/   
END.

PROCEDURE cr-remark :
    CREATE q1-list.
    ASSIGN
        q1-list.name       = mathis.name
        q1-list.asset      = mathis.asset
        q1-list.datum      = mathis.datum
        q1-list.price      = mathis.price
        q1-list.anzahl     = fa-artikel.anzahl
        q1-list.warenwert  = fa-artikel.warenwert
        q1-list.depn-wert  = fa-artikel.depn-wert
        q1-list.book-wert  = fa-artikel.book-wert
        q1-list.katnr      = fa-artikel.katnr
        q1-list.bezeich    = fa-grup.bezeich
        q1-list.location   = mathis.location
        q1-list.first-depn = fa-artikel.first-depn
        q1-list.next-depn  = fa-artikel.next-depn
        q1-list.last-depn  = fa-artikel.last-depn
        q1-list.id         = fa-artikel.id
        q1-list.created    = fa-artikel.created
        q1-list.cid        = fa-artikel.cid
        q1-list.changed    = fa-artikel.changed
        q1-list.remark     = mathis.remark
            
        q1-list.mathis-nr  = mathis.nr
        q1-list.fname      = mathis.fname
        q1-list.supplier   = mathis.supplier
        q1-list.posted     = fa-artikel.posted
        q1-list.fibukonto  = fa-artikel.fibukonto
        q1-list.faartikel-nr  = fa-artikel.nr
        q1-list.credit-fibu = fa-artikel.credit-fibu
        q1-list.debit-fibu  = fa-artikel.debit-fibu
        q1-list.recid-fa-artikel = RECID(fa-artikel)
        q1-list.recid-mathis     = RECID(mathis)
        q1-list.subgroup    = fa-artikel.subgrp
        q1-list.gnr         = fa-artikel.gnr
        q1-list.model       = mathis.model
        q1-list.flag        = mathis.flag
        q1-list.mark        = mathis.mark
        q1-list.spec        = mathis.spec
        q1-list.anz-depn    = fa-artikel.anz-depn
        q1-list.category    = fa-artikel.katnr.
        /* q1-list.lager-nr    = fa-lager.lager-nr. */
    FIND FIRST bfa-grup WHERE bfa-grup.gnr = fa-artikel.gnr AND bfa-grup.flag = 0 NO-LOCK NO-ERROR.
    IF AVAILABLE bfa-grup THEN ASSIGN q1-list.grp-bez = bfa-grup.bezeic.
    FIND FIRST bfa-grup WHERE bfa-grup.gnr = fa-artikel.subgrp AND bfa-grup.flag GT 0 NO-LOCK NO-ERROR.
    IF AVAILABLE bfa-grup THEN ASSIGN q1-list.sgrp-bez = bfa-grup.bezeic.
    FIND FIRST fa-kateg WHERE fa-kateg.katnr = fa-artikel.katnr NO-LOCK NO-ERROR.
    IF AVAILABLE fa-kateg THEN q1-list.rate = fa-kateg.rat.
    /*ITA 290115*/
    FIND FIRST fibu-list WHERE fibu-list.fibukonto = fa-grup.fibukonto
        NO-ERROR.
    IF NOT AVAILABLE fibu-list THEN
    DO:
        FIND FIRST gl-acct WHERE gl-acct.fibukonto = fa-grup.fibukonto NO-LOCK
            NO-ERROR.
        IF NOT AVAILABLE gl-acct THEN 
        DO: 
            ASSIGN q1-list.avail-glacct1 = YES.
        END.
        ELSE DO:
            CREATE fibu-list.
            ASSIGN fibu-list.fibukonto = fa-grup.fibukonto
                    fibu-list.bezeich   = gl-acct.bezeich
                    fibu-list.flag      = 1.
        END.
    END.
    IF q1-list.avail-glacct1 = NO THEN 
        ASSIGN fibu-list.debit = fibu-list.debit + fa-artikel.warenwert.
    
    FIND FIRST fibu-list WHERE fibu-list.fibukonto = fa-grup.credit-fibu
        NO-ERROR.
    IF NOT AVAILABLE fibu-list THEN
    DO:
        FIND FIRST gl-acct WHERE gl-acct.fibukonto = fa-grup.credit-fibu NO-LOCK
            NO-ERROR.
        IF NOT AVAILABLE gl-acct THEN 
        DO: 
            ASSIGN q1-list.avail-glacct2 = YES.
        END.
        ELSE DO:
            CREATE fibu-list.
            ASSIGN fibu-list.fibukonto = fa-grup.credit-fibu
                    fibu-list.bezeich   = gl-acct.bezeich
                    fibu-list.flag      = 2.
        END.
    END.
    IF q1-list.avail-glacct2 = NO THEN 
        ASSIGN fibu-list.credit = fibu-list.credit + fa-artikel.depn-wert.
    
    FIND FIRST fibu-list WHERE fibu-list.fibukonto = fa-grup.debit-fibu
        NO-ERROR.
    IF NOT AVAILABLE fibu-list THEN
    DO:
        FIND FIRST gl-acct WHERE gl-acct.fibukonto = fa-grup.debit-fibu NO-LOCK
            NO-ERROR.
        IF NOT AVAILABLE gl-acct THEN 
        DO: 
            ASSIGN q1-list.avail-glacct3 = YES.
        END.
        ELSE DO:
            CREATE fibu-list.
            ASSIGN fibu-list.fibukonto = fa-grup.debit-fibu
                    fibu-list.bezeich   = gl-acct.bezeich
                    fibu-list.flag      = 3.
        END.
    END.
    IF q1-list.avail-glacct3 = NO THEN 
        ASSIGN fibu-list.debit = fibu-list.debit + fa-artikel.depn-wert.
    /**end*/   
END.

PROCEDURE cr-location :
    CREATE q1-list.
    ASSIGN
        q1-list.name       = mathis.name
        q1-list.asset      = mathis.asset
        q1-list.datum      = mathis.datum
        q1-list.price      = mathis.price
        q1-list.anzahl     = fa-artikel.anzahl
        q1-list.warenwert  = fa-artikel.warenwert
        q1-list.depn-wert  = fa-artikel.depn-wert
        q1-list.book-wert  = fa-artikel.book-wert
        q1-list.katnr      = fa-artikel.katnr
        q1-list.bezeich    = fa-grup.bezeich
        q1-list.location   = mathis.location
        q1-list.first-depn = fa-artikel.first-depn
        q1-list.next-depn  = fa-artikel.next-depn
        q1-list.last-depn  = fa-artikel.last-depn
        q1-list.id         = fa-artikel.id
        q1-list.created    = fa-artikel.created
        q1-list.cid        = fa-artikel.cid
        q1-list.changed    = fa-artikel.changed
        q1-list.remark     = mathis.remark
            
        q1-list.mathis-nr  = mathis.nr
        q1-list.fname      = mathis.fname
        q1-list.supplier   = mathis.supplier
        q1-list.posted     = fa-artikel.posted
        q1-list.fibukonto  = fa-artikel.fibukonto
        q1-list.faartikel-nr  = fa-artikel.nr
        q1-list.credit-fibu = fa-artikel.credit-fibu
        q1-list.debit-fibu  = fa-artikel.debit-fibu
        q1-list.recid-fa-artikel = RECID(fa-artikel)
        q1-list.recid-mathis     = RECID(mathis)
        q1-list.subgroup    = fa-artikel.subgrp
        q1-list.gnr         = fa-artikel.gnr
        q1-list.model       = mathis.model
        q1-list.flag        = mathis.flag
        q1-list.mark        = mathis.mark
        q1-list.spec        = mathis.spec
        q1-list.anz-depn    = fa-artikel.anz-depn
        q1-list.category    = fa-artikel.katnr.
        /* q1-list.lager-nr    = fa-lager.lager-nr. */
    FIND FIRST bfa-grup WHERE bfa-grup.gnr = fa-artikel.gnr AND bfa-grup.flag = 0 NO-LOCK NO-ERROR.
    IF AVAILABLE bfa-grup THEN ASSIGN q1-list.grp-bez = bfa-grup.bezeic.
    FIND FIRST bfa-grup WHERE bfa-grup.gnr = fa-artikel.subgrp AND bfa-grup.flag GT 0 NO-LOCK NO-ERROR.
    IF AVAILABLE bfa-grup THEN ASSIGN q1-list.sgrp-bez = bfa-grup.bezeic.
    FIND FIRST fa-kateg WHERE fa-kateg.katnr = fa-artikel.katnr NO-LOCK NO-ERROR.
    IF AVAILABLE fa-kateg THEN q1-list.rate = fa-kateg.rat.
    /*ITA 290115*/
    FIND FIRST fibu-list WHERE fibu-list.fibukonto = fa-grup.fibukonto
        NO-ERROR.
    IF NOT AVAILABLE fibu-list THEN
    DO:
        FIND FIRST gl-acct WHERE gl-acct.fibukonto = fa-grup.fibukonto NO-LOCK
            NO-ERROR.
        IF NOT AVAILABLE gl-acct THEN 
        DO: 
            ASSIGN q1-list.avail-glacct1 = YES.
        END.
        ELSE DO:
            CREATE fibu-list.
            ASSIGN fibu-list.fibukonto = fa-grup.fibukonto
                    fibu-list.bezeich   = gl-acct.bezeich
                    fibu-list.flag      = 1.
        END.
    END.
    IF q1-list.avail-glacct1 = NO THEN 
        ASSIGN fibu-list.debit = fibu-list.debit + fa-artikel.warenwert.
    
    FIND FIRST fibu-list WHERE fibu-list.fibukonto = fa-grup.credit-fibu
        NO-ERROR.
    IF NOT AVAILABLE fibu-list THEN
    DO:
        FIND FIRST gl-acct WHERE gl-acct.fibukonto = fa-grup.credit-fibu NO-LOCK
            NO-ERROR.
        IF NOT AVAILABLE gl-acct THEN 
        DO: 
            ASSIGN q1-list.avail-glacct2 = YES.
        END.
        ELSE DO:
            CREATE fibu-list.
            ASSIGN fibu-list.fibukonto = fa-grup.credit-fibu
                    fibu-list.bezeich   = gl-acct.bezeich
                    fibu-list.flag      = 2.
        END.
    END.
    IF q1-list.avail-glacct2 = NO THEN 
        ASSIGN fibu-list.credit = fibu-list.credit + fa-artikel.depn-wert.
    
    FIND FIRST fibu-list WHERE fibu-list.fibukonto = fa-grup.debit-fibu
        NO-ERROR.
    IF NOT AVAILABLE fibu-list THEN
    DO:
        FIND FIRST gl-acct WHERE gl-acct.fibukonto = fa-grup.debit-fibu NO-LOCK
            NO-ERROR.
        IF NOT AVAILABLE gl-acct THEN 
        DO: 
            ASSIGN q1-list.avail-glacct3 = YES.
        END.
        ELSE DO:
            CREATE fibu-list.
            ASSIGN fibu-list.fibukonto = fa-grup.debit-fibu
                    fibu-list.bezeich   = gl-acct.bezeich
                    fibu-list.flag      = 3.
        END.
    END.
    IF q1-list.avail-glacct3 = NO THEN 
        ASSIGN fibu-list.debit = fibu-list.debit + fa-artikel.depn-wert.
    /**end*/   
END.

PROCEDURE cr-asset-number :
    CREATE q1-list.
    ASSIGN
        q1-list.name       = mathis.name
        q1-list.asset      = mathis.asset
        q1-list.datum      = mathis.datum
        q1-list.price      = mathis.price
        q1-list.anzahl     = fa-artikel.anzahl
        q1-list.warenwert  = fa-artikel.warenwert
        q1-list.depn-wert  = fa-artikel.depn-wert
        q1-list.book-wert  = fa-artikel.book-wert
        q1-list.katnr      = fa-artikel.katnr
        q1-list.bezeich    = fa-grup.bezeich
        q1-list.location   = mathis.location
        q1-list.first-depn = fa-artikel.first-depn
        q1-list.next-depn  = fa-artikel.next-depn
        q1-list.last-depn  = fa-artikel.last-depn
        q1-list.id         = fa-artikel.id
        q1-list.created    = fa-artikel.created
        q1-list.cid        = fa-artikel.cid
        q1-list.changed    = fa-artikel.changed
        q1-list.remark     = mathis.remark
            
        q1-list.mathis-nr  = mathis.nr
        q1-list.fname      = mathis.fname
        q1-list.supplier   = mathis.supplier
        q1-list.posted     = fa-artikel.posted
        q1-list.fibukonto  = fa-artikel.fibukonto
        q1-list.faartikel-nr  = fa-artikel.nr
        q1-list.credit-fibu = fa-artikel.credit-fibu
        q1-list.debit-fibu  = fa-artikel.debit-fibu
        q1-list.recid-fa-artikel = RECID(fa-artikel)
        q1-list.recid-mathis     = RECID(mathis)
        q1-list.subgroup    = fa-artikel.subgrp
        q1-list.gnr         = fa-artikel.gnr
        q1-list.model       = mathis.model
        q1-list.flag        = mathis.flag
        q1-list.mark        = mathis.mark
        q1-list.spec        = mathis.spec
        q1-list.anz-depn    = fa-artikel.anz-depn
        q1-list.category    = fa-artikel.katnr.
        /* q1-list.lager-nr    = fa-lager.lager-nr. */
    FIND FIRST bfa-grup WHERE bfa-grup.gnr = fa-artikel.gnr AND bfa-grup.flag = 0 NO-LOCK NO-ERROR.
    IF AVAILABLE bfa-grup THEN ASSIGN q1-list.grp-bez = bfa-grup.bezeic.
    FIND FIRST bfa-grup WHERE bfa-grup.gnr = fa-artikel.subgrp AND bfa-grup.flag GT 0 NO-LOCK NO-ERROR.
    IF AVAILABLE bfa-grup THEN ASSIGN q1-list.sgrp-bez = bfa-grup.bezeic.
    FIND FIRST fa-kateg WHERE fa-kateg.katnr = fa-artikel.katnr NO-LOCK NO-ERROR.
    IF AVAILABLE fa-kateg THEN q1-list.rate = fa-kateg.rat.
    /*ITA 290115*/
    FIND FIRST fibu-list WHERE fibu-list.fibukonto = fa-grup.fibukonto
        NO-ERROR.
    IF NOT AVAILABLE fibu-list THEN
    DO:
        FIND FIRST gl-acct WHERE gl-acct.fibukonto = fa-grup.fibukonto NO-LOCK
            NO-ERROR.
        IF NOT AVAILABLE gl-acct THEN 
        DO: 
            ASSIGN q1-list.avail-glacct1 = YES.
        END.
        ELSE DO:
            CREATE fibu-list.
            ASSIGN fibu-list.fibukonto = fa-grup.fibukonto
                    fibu-list.bezeich   = gl-acct.bezeich
                    fibu-list.flag      = 1.
        END.
    END.
    IF q1-list.avail-glacct1 = NO THEN 
        ASSIGN fibu-list.debit = fibu-list.debit + fa-artikel.warenwert.
    
    FIND FIRST fibu-list WHERE fibu-list.fibukonto = fa-grup.credit-fibu
        NO-ERROR.
    IF NOT AVAILABLE fibu-list THEN
    DO:
        FIND FIRST gl-acct WHERE gl-acct.fibukonto = fa-grup.credit-fibu NO-LOCK
            NO-ERROR.
        IF NOT AVAILABLE gl-acct THEN 
        DO: 
            ASSIGN q1-list.avail-glacct2 = YES.
        END.
        ELSE DO:
            CREATE fibu-list.
            ASSIGN fibu-list.fibukonto = fa-grup.credit-fibu
                    fibu-list.bezeich   = gl-acct.bezeich
                    fibu-list.flag      = 2.
        END.
    END.
    IF q1-list.avail-glacct2 = NO THEN 
        ASSIGN fibu-list.credit = fibu-list.credit + fa-artikel.depn-wert.
    
    FIND FIRST fibu-list WHERE fibu-list.fibukonto = fa-grup.debit-fibu
        NO-ERROR.
    IF NOT AVAILABLE fibu-list THEN
    DO:
        FIND FIRST gl-acct WHERE gl-acct.fibukonto = fa-grup.debit-fibu NO-LOCK
            NO-ERROR.
        IF NOT AVAILABLE gl-acct THEN 
        DO: 
            ASSIGN q1-list.avail-glacct3 = YES.
        END.
        ELSE DO:
            CREATE fibu-list.
            ASSIGN fibu-list.fibukonto = fa-grup.debit-fibu
                    fibu-list.bezeich   = gl-acct.bezeich
                    fibu-list.flag      = 3.
        END.
    END.
    IF q1-list.avail-glacct3 = NO THEN 
        ASSIGN fibu-list.debit = fibu-list.debit + fa-artikel.depn-wert.
    /**end*/   
END.

PROCEDURE cr-asset-list :
    CREATE q1-list.
    ASSIGN
        q1-list.name       = mathis.name
        q1-list.asset      = mathis.asset
        q1-list.datum      = mathis.datum
        q1-list.price      = mathis.price
        q1-list.anzahl     = fa-artikel.anzahl
        q1-list.warenwert  = fa-artikel.warenwert
        q1-list.depn-wert  = fa-artikel.depn-wert
        q1-list.book-wert  = fa-artikel.book-wert
        q1-list.katnr      = fa-artikel.katnr
        q1-list.bezeich    = fa-grup.bezeich
        q1-list.location   = mathis.location
        q1-list.first-depn = fa-artikel.first-depn
        q1-list.next-depn  = fa-artikel.next-depn
        q1-list.last-depn  = fa-artikel.last-depn
        q1-list.id         = fa-artikel.id
        q1-list.created    = fa-artikel.created
        q1-list.cid        = fa-artikel.cid
        q1-list.changed    = fa-artikel.changed
        q1-list.remark     = mathis.remark
            
        q1-list.mathis-nr  = mathis.nr
        q1-list.fname      = mathis.fname
        q1-list.supplier   = mathis.supplier
        q1-list.posted     = fa-artikel.posted
        q1-list.fibukonto  = fa-artikel.fibukonto
        q1-list.faartikel-nr  = fa-artikel.nr
        q1-list.credit-fibu = fa-artikel.credit-fibu
        q1-list.debit-fibu  = fa-artikel.debit-fibu
        q1-list.recid-fa-artikel = RECID(fa-artikel)
        q1-list.recid-mathis     = RECID(mathis)
        q1-list.subgroup    = fa-artikel.subgrp
        q1-list.gnr         = fa-artikel.gnr
        q1-list.model       = mathis.model
        q1-list.flag        = mathis.flag
        q1-list.mark        = mathis.mark
        q1-list.spec        = mathis.spec
        q1-list.anz-depn    = fa-artikel.anz-depn
        q1-list.category    = fa-artikel.katnr.
        /* q1-list.lager-nr    = fa-lager.lager-nr. */
    IF mathis.flag = 2 THEN
    DO:
        ASSIGN
            q1-list.isUpgrade = "Yes".
    END.
    ELSE
    DO:
        ASSIGN
            q1-list.isUpgrade = "No".
    END.

    FIND FIRST bfa-grup WHERE bfa-grup.gnr = fa-artikel.gnr AND bfa-grup.flag = 0 NO-LOCK NO-ERROR.
    IF AVAILABLE bfa-grup THEN ASSIGN q1-list.grp-bez = bfa-grup.bezeic.
    FIND FIRST bfa-grup WHERE bfa-grup.gnr = fa-artikel.subgrp AND bfa-grup.flag GT 0 NO-LOCK NO-ERROR.
    IF AVAILABLE bfa-grup THEN ASSIGN q1-list.sgrp-bez = bfa-grup.bezeic.
    FIND FIRST fa-kateg WHERE fa-kateg.katnr = fa-artikel.katnr NO-LOCK NO-ERROR.
    IF AVAILABLE fa-kateg THEN q1-list.rate = fa-kateg.rat.
    /*ITA 290115*/
    FIND FIRST fibu-list WHERE fibu-list.fibukonto = fa-grup.fibukonto
        NO-ERROR.
    IF NOT AVAILABLE fibu-list THEN
    DO:
        FIND FIRST gl-acct WHERE gl-acct.fibukonto = fa-grup.fibukonto NO-LOCK
            NO-ERROR.
        IF NOT AVAILABLE gl-acct THEN 
        DO: 
            ASSIGN q1-list.avail-glacct1 = YES.
        END.
        ELSE DO:
            CREATE fibu-list.
            ASSIGN fibu-list.fibukonto = fa-grup.fibukonto
                    fibu-list.bezeich   = gl-acct.bezeich
                    fibu-list.flag      = 1.
        END.
    END.
    IF q1-list.avail-glacct1 = NO THEN 
        ASSIGN fibu-list.debit = fibu-list.debit + fa-artikel.warenwert.
    
    FIND FIRST fibu-list WHERE fibu-list.fibukonto = fa-grup.credit-fibu
        NO-ERROR.
    IF NOT AVAILABLE fibu-list THEN
    DO:
        FIND FIRST gl-acct WHERE gl-acct.fibukonto = fa-grup.credit-fibu NO-LOCK
            NO-ERROR.
        IF NOT AVAILABLE gl-acct THEN 
        DO: 
            ASSIGN q1-list.avail-glacct2 = YES.
        END.
        ELSE DO:
            CREATE fibu-list.
            ASSIGN fibu-list.fibukonto = fa-grup.credit-fibu
                    fibu-list.bezeich   = gl-acct.bezeich
                    fibu-list.flag      = 2.
        END.
    END.
    IF q1-list.avail-glacct2 = NO THEN 
        ASSIGN fibu-list.credit = fibu-list.credit + fa-artikel.depn-wert.
    
    FIND FIRST fibu-list WHERE fibu-list.fibukonto = fa-grup.debit-fibu
        NO-ERROR.
    IF NOT AVAILABLE fibu-list THEN
    DO:
        FIND FIRST gl-acct WHERE gl-acct.fibukonto = fa-grup.debit-fibu NO-LOCK
            NO-ERROR.
        IF NOT AVAILABLE gl-acct THEN 
        DO: 
            ASSIGN q1-list.avail-glacct3 = YES.
        END.
        ELSE DO:
            CREATE fibu-list.
            ASSIGN fibu-list.fibukonto = fa-grup.debit-fibu
                    fibu-list.bezeich   = gl-acct.bezeich
                    fibu-list.flag      = 3.
        END.
    END.
    IF q1-list.avail-glacct3 = NO THEN 
        ASSIGN fibu-list.debit = fibu-list.debit + fa-artikel.depn-wert.
    /**end*/   
END.
