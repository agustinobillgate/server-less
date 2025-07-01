
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
    .

DEFINE TEMP-TABLE fibu-list
    FIELD flag      AS   INTEGER INITIAL 0
    FIELD fibukonto LIKE gl-acct.fibukonto
    FIELD bezeich   LIKE gl-acct.bezeich
    FIELD credit    LIKE gl-journal.credit
    FIELD debit     LIKE gl-journal.debit.

DEFINE TEMP-TABLE sortir-list
    FIELD from-date LIKE mathis.datum
    FIELD to-date   LIKE mathis.datum 
    FIELD location  LIKE fa-lager.lager-nr
    FIELD show-all  AS LOGICAL.

DEF INPUT PARAMETER TABLE FOR sortir-list.
DEF OUTPUT PARAMETER p-881 AS DATE.
DEF OUTPUT PARAMETER TABLE FOR q1-list.
DEF OUTPUT PARAMETER TABLE FOR fibu-list.

DEFINE BUFFER bfa-grup FOR fa-grup.
DEFINE VARIABLE sort-loc AS CHAR. 


RUN htpdate.p (881, OUTPUT p-881).   /* LAST Dep'n DATE */
FIND FIRST sortir-list.

/* By date and location */
IF sortir-list.location NE ? AND sortir-list.show-all EQ NO THEN
DO:
    FOR EACH mathis WHERE mathis.datum GE sortir-list.from-date
        AND mathis.datum LE sortir-list.to-date NO-LOCK, 
        FIRST fa-artikel WHERE fa-artikel.nr = mathis.nr 
        AND fa-artikel.loeschflag = 0 NO-LOCK,
        FIRST fa-grup WHERE fa-grup.gnr = fa-artikel.subgrp AND fa-grup.flag = 1
        NO-LOCK BY mathis.name:
        FIND FIRST fa-lager WHERE fa-lager.lager-nr = sortir-list.location AND fa-lager.bezeich = mathis.location NO-LOCK NO-ERROR.
        IF AVAILABLE fa-lager THEN
        DO:
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
                q1-list.category    = fa-artikel.katnr
                q1-list.lager-nr    = fa-lager.lager-nr.

                FIND FIRST bfa-grup WHERE bfa-grup.gnr = fa-artikel.gnr AND bfa-grup.flag = 0 NO-LOCK NO-ERROR.
                IF AVAILABLE bfa-grup THEN ASSIGN q1-list.grp-bez = bfa-grup.bezeich.

                FIND FIRST bfa-grup WHERE bfa-grup.gnr = fa-artikel.subgrp AND bfa-grup.flag GT 0 NO-LOCK NO-ERROR.
                IF AVAILABLE bfa-grup THEN ASSIGN q1-list.sgrp-bez = bfa-grup.bezeich.

                FIND FIRST fa-kateg WHERE fa-kateg.katnr = fa-artikel.katnr NO-LOCK NO-ERROR.
                IF AVAILABLE fa-kateg THEN q1-list.rate = fa-kateg.rate.

                /*ITA 290115*/
                FIND FIRST fibu-list WHERE fibu-list.fibukonto = fa-grup.fibukonto NO-ERROR.
                IF NOT AVAILABLE fibu-list THEN
                DO:
                    FIND FIRST gl-acct WHERE gl-acct.fibukonto = fa-grup.fibukonto NO-LOCK
                        NO-ERROR.
                    IF NOT AVAILABLE gl-acct THEN 
                    DO: 
                        ASSIGN q1-list.avail-glacct1 = YES.
                    END.
                    ELSE 
                    DO:
                        CREATE fibu-list.
                        ASSIGN fibu-list.fibukonto = fa-grup.fibukonto
                                    fibu-list.bezeich   = gl-acct.bezeich
                                    fibu-list.flag      = 1.
                    END.
                END.

                IF q1-list.avail-glacct1 = NO THEN 
                    ASSIGN fibu-list.debit = fibu-list.debit + fa-artikel.warenwert.
                    
                FIND FIRST fibu-list WHERE fibu-list.fibukonto = fa-grup.credit-fibu NO-ERROR.
                IF NOT AVAILABLE fibu-list THEN
                DO:
                    FIND FIRST gl-acct WHERE gl-acct.fibukonto = fa-grup.credit-fibu NO-LOCK NO-ERROR.
                    IF NOT AVAILABLE gl-acct THEN 
                    DO: 
                        ASSIGN q1-list.avail-glacct2 = YES.
                    END.
                    ELSE 
                    DO:
                        CREATE fibu-list.
                        ASSIGN fibu-list.fibukonto = fa-grup.credit-fibu
                                fibu-list.bezeich   = gl-acct.bezeich
                                fibu-list.flag      = 2.
                    END.
                END.
                IF q1-list.avail-glacct2 = NO THEN 
                    ASSIGN fibu-list.credit = fibu-list.credit + fa-artikel.depn-wert.
                    
                FIND FIRST fibu-list WHERE fibu-list.fibukonto = fa-grup.debit-fibu NO-ERROR.
                IF NOT AVAILABLE fibu-list THEN
                DO:
                    FIND FIRST gl-acct WHERE gl-acct.fibukonto = fa-grup.debit-fibu NO-LOCK NO-ERROR.
                    IF NOT AVAILABLE gl-acct THEN 
                    DO: 
                        ASSIGN q1-list.avail-glacct3 = YES.
                    END.
                    ELSE 
                    DO:
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
    END.
END.
/* By date */
ELSE IF sortir-list.location EQ ? AND sortir-list.show-all EQ NO THEN
DO:
    FOR EACH mathis WHERE mathis.datum GE sortir-list.from-date
        AND mathis.datum LE sortir-list.to-date NO-LOCK, 
        FIRST fa-artikel WHERE fa-artikel.nr = mathis.nr 
        AND fa-artikel.loeschflag = 0 NO-LOCK,
        FIRST fa-grup WHERE fa-grup.gnr = fa-artikel.subgrp AND fa-grup.flag = 1
        NO-LOCK BY mathis.name:
            
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

        FIND FIRST bfa-grup WHERE bfa-grup.gnr = fa-artikel.gnr AND bfa-grup.flag = 0 NO-LOCK NO-ERROR.
        IF AVAILABLE bfa-grup THEN ASSIGN q1-list.grp-bez = bfa-grup.bezeich.

        FIND FIRST bfa-grup WHERE bfa-grup.gnr = fa-artikel.subgrp AND bfa-grup.flag GT 0 NO-LOCK NO-ERROR.
        IF AVAILABLE bfa-grup THEN ASSIGN q1-list.sgrp-bez = bfa-grup.bezeich.

        FIND FIRST fa-kateg WHERE fa-kateg.katnr = fa-artikel.katnr NO-LOCK NO-ERROR.
        IF AVAILABLE fa-kateg THEN q1-list.rate = fa-kateg.rate.

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
END.
ELSE
DO:
    FOR EACH mathis NO-LOCK, 
        FIRST fa-artikel WHERE fa-artikel.nr = mathis.nr 
        AND fa-artikel.loeschflag = 0 NO-LOCK,
        FIRST fa-grup WHERE fa-grup.gnr = fa-artikel.subgrp AND fa-grup.flag = 1
        NO-LOCK BY mathis.name:
        FIND FIRST fa-lager WHERE fa-lager.bezeich = mathis.location NO-LOCK NO-ERROR.
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
            q1-list.category    = fa-artikel.katnr
            q1-list.lager-nr    = fa-lager.lager-nr.

        FIND FIRST bfa-grup WHERE bfa-grup.gnr = fa-artikel.gnr AND bfa-grup.flag = 0 NO-LOCK NO-ERROR.
        IF AVAILABLE bfa-grup THEN ASSIGN q1-list.grp-bez = bfa-grup.bezeich.

        FIND FIRST bfa-grup WHERE bfa-grup.gnr = fa-artikel.subgrp AND bfa-grup.flag GT 0 NO-LOCK NO-ERROR.
        IF AVAILABLE bfa-grup THEN ASSIGN q1-list.sgrp-bez = bfa-grup.bezeich.

        FIND FIRST fa-kateg WHERE fa-kateg.katnr = fa-artikel.katnr NO-LOCK NO-ERROR.
        IF AVAILABLE fa-kateg THEN q1-list.rate = fa-kateg.rate.

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
END.
