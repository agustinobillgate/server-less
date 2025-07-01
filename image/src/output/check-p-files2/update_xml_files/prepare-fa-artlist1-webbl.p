DEFINE TEMP-TABLE q1-list
    FIELD name              LIKE mathis.name /* Malik :  */
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
    FIELD from-date     LIKE mathis.datum
    FIELD to-date       LIKE mathis.datum 
    FIELD location      LIKE fa-lager.lager-nr
    FIELD show-all      AS LOGICAL
    FIELD asset-name    AS CHAR
    FIELD remark        AS CHAR.

DEF INPUT PARAMETER TABLE FOR sortir-list.
DEFINE INPUT PARAMETER idFlag      AS CHAR.
/**/
DEF OUTPUT PARAMETER p-881 AS DATE.
/**/
DEF OUTPUT PARAMETER TABLE FOR q1-list.
DEF OUTPUT PARAMETER TABLE FOR fibu-list.


DEFINE BUFFER bfa-grup FOR fa-grup.
DEFINE VARIABLE sort-loc AS CHAR. 
DEFINE VARIABLE mark AS CHAR. 
DEFINE VARIABLE htl-no AS CHAR NO-UNDO.
DEFINE VARIABLE counter AS INTEGER NO-UNDO INITIAL 0.

DEFINE VARIABLE q1-list-datum AS CHAR. 
DEFINE VARIABLE q1-list-first-depn AS CHAR. 
DEFINE VARIABLE q1-list-next-depn AS CHAR. 
DEFINE VARIABLE q1-list-last-depn AS CHAR. 
DEFINE VARIABLE q1-list-created AS CHAR. 
DEFINE VARIABLE q1-list-changed AS CHAR. 
DEFINE VARIABLE q1-list-supplier AS CHAR. 
DEFINE VARIABLE q1-list-price AS CHAR. 
DEFINE VARIABLE q1-list-mark AS CHAR. 
DEFINE VARIABLE q1-list-model AS CHAR. 
DEFINE VARIABLE q1-list-spec AS CHAR. 
DEFINE VARIABLE q1-list-remark AS CHAR. 



DEFINE BUFFER bqueasy FOR queasy.
DEFINE BUFFER tqueasy FOR queasy.

CREATE queasy.
ASSIGN queasy.KEY     = 285
       queasy.char1   = "Fixed Asset List Report"
       queasy.number1 = 1
       queasy.char2   = idFlag.
RELEASE queasy.
RUN prepare-fa-artlist-cldbl.p(INPUT TABLE sortir-list, OUTPUT p-881, OUTPUT TABLE q1-list, OUTPUT TABLE fibu-list).                                  
FIND FIRST q1-list NO-ERROR.
DO WHILE AVAILABLE q1-list:
    IF q1-list.datum EQ ? THEN q1-list-datum = "".
    ELSE q1-list-datum = STRING(q1-list.datum).
    IF q1-list.first-depn EQ ? THEN q1-list-first-depn = "".
    ELSE q1-list-first-depn = STRING(q1-list.first-depn).
    IF q1-list.next-depn EQ ? THEN q1-list-next-depn = "".
    ELSE q1-list-next-depn = STRING(q1-list.next-depn).
    IF q1-list.last-depn EQ ? THEN q1-list-last-depn = "".
    ELSE q1-list-last-depn = STRING(q1-list.last-depn).
    IF q1-list.created EQ ? THEN q1-list-created = "".
    ELSE q1-list-created = STRING(q1-list.created).
    IF q1-list.changed EQ ? THEN q1-list-changed = "".
    ELSE q1-list-changed = STRING(q1-list.changed).
    IF q1-list.supplier EQ ? THEN q1-list-supplier = "".
    ELSE q1-list-supplier = STRING(q1-list.supplier).
    IF q1-list.mark EQ ? THEN q1-list-mark = "".
    ELSE q1-list-mark = STRING(q1-list.mark).
    IF q1-list.model EQ ? THEN q1-list-model = "".
    ELSE q1-list-model = STRING(q1-list.model).
    IF q1-list.spec EQ ? THEN q1-list-spec = "".
    ELSE q1-list-spec = STRING(q1-list.spec).
    IF q1-list.remark EQ ? THEN q1-list-remark = "".
    ELSE q1-list-remark = STRING(q1-list.remark).
    IF q1-list.price EQ ? THEN q1-list-price = "".
    ELSE q1-list-price = STRING(q1-list.price).

    IF q1-list.fname EQ ? THEN q1-list.fname = "".
    IF q1-list.id EQ ? THEN q1-list.id = "".
    IF q1-list.cid EQ ? THEN q1-list.cid = "".

    IF q1-list.name MATCHES "*|*" THEN q1-list.name = REPLACE(q1-list.name,"|"," ").
    IF q1-list.bezeich MATCHES "*|*" THEN q1-list.bezeich = REPLACE(q1-list.bezeich,"|"," ").
    IF q1-list.location MATCHES "*|*" THEN q1-list.location = REPLACE(q1-list.location,"|"," ").
    IF q1-list.id MATCHES "*|*" THEN q1-list.id = REPLACE(q1-list.id,"|"," ").
    IF q1-list-remark MATCHES "*|*" THEN q1-list-remark = REPLACE(q1-list-remark,"|"," ").
    IF q1-list-supplier MATCHES "*|*" THEN q1-list-supplier = REPLACE(q1-list-supplier,"|"," ").
    IF q1-list.grp-bez MATCHES "*|*" THEN q1-list.grp-bez = REPLACE(q1-list.grp-bez,"|"," ").
    IF q1-list.sgrp-bez MATCHES "*|*" THEN q1-list.sgrp-bez = REPLACE(q1-list.sgrp-bez,"|"," ").
    IF q1-list-mark MATCHES "*|*" THEN q1-list-mark = REPLACE(q1-list-mark,"|"," ").
    IF q1-list-spec MATCHES "*|*" THEN q1-list-spec = REPLACE(q1-list-spec,"|"," ").


    mark = "article".
    CREATE queasy.
    ASSIGN 
           counter = counter + 1
           queasy.KEY   = 280
           queasy.char1 = "Fixed Asset List Report"
           queasy.char3 = idFlag
           queasy.char2 = STRING(mark)                         + "|" +
                          STRING(q1-list.name)                 + "|" +  
                          STRING(q1-list.asset)                + "|" +  
                          STRING(q1-list-datum)                + "|" + /* ini double cek lagi dah */ 
                          STRING(q1-list-price)                + "|" +  
                          STRING(q1-list.anzahl)               + "|" +  
                          STRING(q1-list.warenwert)            + "|" +  
                          STRING(q1-list.depn-wert)            + "|" +  
                          STRING(q1-list.book-wert)            + "|" +  
                          STRING(q1-list.katnr)                + "|" +  
                          STRING(q1-list.bezeich)              + "|" +  
                          STRING(q1-list.location)             + "|" +  
                          STRING(q1-list-first-depn)           + "|" +  
                          STRING(q1-list-next-depn)            + "|" +  
                          STRING(q1-list-last-depn)            + "|" +  
                          STRING(q1-list.id)                   + "|" +  
                          STRING(q1-list-created)              + "|" +  
                          STRING(q1-list.cid)                  + "|" +  
                          STRING(q1-list-changed)              + "|" +  
                          STRING(q1-list-remark)               + "|" +  
                          STRING(q1-list.mathis-nr)            + "|" +  
                          STRING(q1-list.fname)                + "|" +  
                          STRING(q1-list-supplier)             + "|" +  
                          STRING(q1-list.posted)               + "|" +  
                          STRING(q1-list.fibukonto)            + "|" +  
                          STRING(q1-list.faartikel-nr)         + "|" +  
                          STRING(q1-list.credit-fibu)          + "|" +  
                          STRING(q1-list.debit-fibu)           + "|" +  
                          STRING(q1-list.recid-fa-artikel)     + "|" +  
                          STRING(q1-list.recid-mathis)         + "|" +  
                          STRING(q1-list.avail-glacct1)        + "|" +  
                          STRING(q1-list.avail-glacct2)        + "|" +  
                          STRING(q1-list.avail-glacct3)        + "|" +  
                          STRING(q1-list.subgroup)             + "|" +  
                          STRING(q1-list-model)                + "|" +  
                          STRING(q1-list.gnr)                  + "|" +  
                          STRING(q1-list.flag)                 + "|" +  
                          STRING(q1-list.grp-bez)              + "|" +  
                          STRING(q1-list.sgrp-bez)             + "|" +  
                          STRING(q1-list.rate)                 + "|" +  
                          STRING(q1-list-mark)                 + "|" +  
                          STRING(q1-list-spec)                 + "|" +  
                          STRING(q1-list.anz-depn)             + "|" +  
                          STRING(q1-list.category)             + "|" +  
                          STRING(q1-list.lager-nr) 
                 queasy.number1 = counter.
    DELETE q1-list.
    FIND NEXT q1-list NO-ERROR.
END.

FIND FIRST fibu-list NO-ERROR.
DO WHILE AVAILABLE fibu-list:
    IF fibu-list.bezeich MATCHES "*|*" THEN fibu-list.bezeich = REPLACE(fibu-list.bezeich,"|"," ").
    mark = "fibu".
    CREATE queasy.
    ASSIGN 
           counter = counter + 1
           queasy.KEY   = 280
           queasy.char1 = "Fixed Asset List Report"
           queasy.char3 = idFlag
           queasy.char2 = STRING(mark)                         + "|" +
                          STRING(fibu-list.flag)               + "|" +  
                          STRING(fibu-list.fibukonto)          + "|" +
                          STRING(fibu-list.bezeich)            + "|" +  
                          STRING(fibu-list.credit)             + "|" +  
                          STRING(fibu-list.debit)  
            queasy.number1 = counter.
    DELETE fibu-list.
    FIND NEXT fibu-list NO-ERROR.
END.

FIND FIRST bqueasy WHERE bqueasy.KEY = 285
    AND bqueasy.char1 = "Fixed Asset List Report"
    AND bqueasy.char2 = idFlag NO-LOCK NO-ERROR.
IF AVAILABLE bqueasy THEN DO:
    FIND CURRENT bqueasy EXCLUSIVE-LOCK.
    ASSIGN bqueasy.number1 = 0.
    FIND CURRENT bqueasy NO-LOCK.
    RELEASE bqueasy.
END.
 

   
    
    







