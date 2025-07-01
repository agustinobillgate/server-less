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


DEFINE INPUT PARAMETER idFlag AS CHAR.
DEFINE OUTPUT PARAMETER doneFlag AS LOGICAL NO-UNDO INITIAL NO.
DEFINE INPUT-OUTPUT PARAMETER TABLE FOR q1-list.
DEFINE INPUT-OUTPUT PARAMETER TABLE FOR fibu-list.

DEFINE VARIABLE counter AS INTEGER NO-UNDO INITIAL 0.
DEFINE VARIABLE htl-no AS CHAR NO-UNDO.
DEFINE VARIABLE temp-char AS CHAR NO-UNDO.
DEFINE VARIABLE ankunft AS CHAR.
DEFINE VARIABLE bill-datum AS CHAR.
DEFINE VARIABLE depart AS CHAR.

DEFINE VARIABLE isPosted AS LOGICAL.
DEFINE VARIABLE isavail-glacct1 AS LOGICAL.
DEFINE VARIABLE isavail-glacct2 AS LOGICAL.
DEFINE VARIABLE isavail-glacct3 AS LOGICAL.



DEFINE BUFFER bqueasy FOR queasy.
DEFINE BUFFER pqueasy FOR queasy.
DEFINE BUFFER tqueasy FOR queasy.
    

FOR EACH queasy WHERE queasy.KEY = 280 AND queasy.char1 = "Fixed Asset List Report"
    AND queasy.char3 = idFlag NO-LOCK BY queasy.number1:


    ASSIGN counter = counter + 1.
    IF counter GT 500 THEN LEAVE.
    IF ENTRY(1, queasy.char2, "|") EQ "article" THEN
    DO:
        IF ENTRY(24, queasy.char2, "|") EQ "YES" THEN 
        DO:
            isPosted = YES.
        END.
        ELSE IF ENTRY(24, queasy.char2, "|") EQ "NO" THEN
        DO:
            isPosted = NO.
        END.

        IF ENTRY(31, queasy.char2, "|") EQ "YES" THEN
        DO:
            isavail-glacct1 = YES.
        END.
        ELSE isavail-glacct1 = NO.

        IF ENTRY(32, queasy.char2, "|") EQ "YES" THEN
        DO:
            isavail-glacct2 = YES.
        END.
        ELSE isavail-glacct2 = NO.

        IF ENTRY(33, queasy.char2, "|") EQ "YES" THEN
        DO:
            isavail-glacct3 = YES.
        END.
        ELSE isavail-glacct3 = NO.
        
        CREATE q1-list.
        ASSIGN
            q1-list.name       = ENTRY(2, queasy.char2, "|")
            q1-list.asset      = ENTRY(3, queasy.char2, "|")
            q1-list.datum      = DATE(ENTRY(4, queasy.char2, "|"))
            q1-list.price      = DECIMAL(ENTRY(5, queasy.char2, "|"))
            q1-list.anzahl     = INTEGER(ENTRY(6, queasy.char2, "|"))
            q1-list.warenwert  = DECIMAL(ENTRY(7, queasy.char2, "|"))
            q1-list.depn-wert  = DECIMAL(ENTRY(8, queasy.char2, "|"))
            q1-list.book-wert  = DECIMAL(ENTRY(9, queasy.char2, "|"))
            q1-list.katnr      = INTEGER(ENTRY(10, queasy.char2, "|"))
            q1-list.bezeich    = ENTRY(11, queasy.char2, "|")
            q1-list.location   = ENTRY(12, queasy.char2, "|")
            q1-list.first-depn = DATE(ENTRY(13, queasy.char2, "|"))
            q1-list.next-depn  = DATE(ENTRY(14, queasy.char2, "|"))
            q1-list.last-depn  = DATE(ENTRY(15, queasy.char2, "|"))
            q1-list.id         = ENTRY(16, queasy.char2, "|")
            q1-list.created    = DATE(ENTRY(17, queasy.char2, "|"))
            q1-list.cid        = ENTRY(18, queasy.char2, "|")
            q1-list.changed    = DATE(ENTRY(19, queasy.char2, "|"))
            q1-list.remark     = ENTRY(20, queasy.char2, "|")
            q1-list.mathis-nr  = INTEGER(ENTRY(21, queasy.char2, "|"))
            q1-list.fname      = ENTRY(22, queasy.char2, "|")
            q1-list.supplier   = ENTRY(23, queasy.char2, "|")
            q1-list.posted     = isPosted
            q1-list.fibukonto  = ENTRY(25, queasy.char2, "|")
            q1-list.faartikel-nr  = INTEGER(ENTRY(26, queasy.char2, "|"))
            q1-list.credit-fibu = ENTRY(27, queasy.char2, "|")
            q1-list.debit-fibu  = ENTRY(28, queasy.char2, "|")
            q1-list.recid-fa-artikel = INTEGER(ENTRY(29, queasy.char2, "|"))
            q1-list.recid-mathis     = INTEGER(ENTRY(30, queasy.char2, "|"))
            q1-list.avail-glacct1 = isavail-glacct1
            q1-list.avail-glacct2 = isavail-glacct2
            q1-list.avail-glacct3 = isavail-glacct3
            q1-list.subgroup    = INTEGER(ENTRY(34, queasy.char2, "|"))
            q1-list.model       = ENTRY(35, queasy.char2, "|")
            q1-list.gnr         = INTEGER(ENTRY(36, queasy.char2, "|"))
            q1-list.flag        = INTEGER(ENTRY(37, queasy.char2, "|"))
            q1-list.grp-bez     = ENTRY(38, queasy.char2, "|")
            q1-list.sgrp-bez    = ENTRY(39, queasy.char2, "|")
            q1-list.rate        = DECIMAL(ENTRY(40, queasy.char2, "|"))
            q1-list.mark        = ENTRY(41, queasy.char2, "|")
            q1-list.spec        = ENTRY(42, queasy.char2, "|")
            q1-list.anz-depn    = INTEGER(ENTRY(43, queasy.char2, "|"))
            q1-list.category    = INTEGER(ENTRY(44, queasy.char2, "|"))
            q1-list.lager-nr    = INTEGER(ENTRY(45, queasy.char2, "|")).
    END.
    ELSE IF ENTRY(1, queasy.char2, "|") EQ "fibu" THEN
    DO:
        CREATE fibu-list.
        ASSIGN
            fibu-list.flag = INTEGER(ENTRY(2, queasy.char2, "|"))
            fibu-list.fibukonto = ENTRY(3, queasy.char2, "|")
            fibu-list.bezeich = ENTRY(4, queasy.char2, "|")
            fibu-list.credit = DECIMAL(ENTRY(5, queasy.char2, "|"))
            fibu-list.debit = DECIMAL(ENTRY(6, queasy.char2, "|")).
    END.

   FIND FIRST bqueasy WHERE RECID(bqueasy) = RECID(queasy) EXCLUSIVE-LOCK.
   DELETE bqueasy.
   RELEASE bqueasy.
END. 


FIND FIRST pqueasy WHERE pqueasy.KEY = 280
    AND pqueasy.char1 = "Fixed Asset List Report" 
    AND pqueasy.char3 = idFlag NO-LOCK NO-ERROR.
IF AVAILABLE pqueasy THEN 
DO:
    ASSIGN doneFlag = NO.
END.
ELSE 
DO:
    FIND FIRST tqueasy WHERE tqueasy.KEY = 285
        AND tqueasy.char1 = "Fixed Asset List Report"
        AND tqueasy.number1 = 1 
        AND tqueasy.char2 = idFlag NO-LOCK NO-ERROR.
    IF AVAILABLE tqueasy THEN
    DO:
        ASSIGN doneFlag = NO.
    END.
    ELSE 
    DO:
        ASSIGN doneFlag = YES.
    END.
END.

FIND FIRST tqueasy WHERE tqueasy.KEY = 285
    AND tqueasy.char1 = "Fixed Asset List Report"
    AND tqueasy.number1 = 0 
    AND tqueasy.char2 = idFlag NO-LOCK NO-ERROR.

IF AVAILABLE tqueasy THEN 
DO:
    FIND CURRENT tqueasy EXCLUSIVE-LOCK.
    DELETE tqueasy.
    RELEASE tqueasy.
END.



