DEFINE TEMP-TABLE supply-list
    FIELD lief-nr  AS INTEGER
    FIELD supplier AS CHAR
    FIELD telefon  LIKE l-lieferant.telefon           /*MT 01/07/12 */
    FIELD fax      LIKE l-lieferant.fax               /*MT 01/07/12 */
    FIELD namekontakt LIKE l-lieferant.namekontakt.   /*MT 01/07/12 */

DEFINE TEMP-TABLE c-list 
    FIELD zwkum    AS INTEGER INITIAL 0 
    FIELD grp      AS CHAR    FORMAT "x(22)" COLUMN-LABEL "Group" 
    FIELD artnr    LIKE l-artikel.artnr 
    FIELD bezeich  AS CHAR    FORMAT "x(38)" COLUMN-LABEL "Description" 
    FIELD qty      AS DECIMAL FORMAT ">>,>>9.99" LABEL "Ordered Qty" 
    FIELD a-qty    AS DECIMAL FORMAT "->>,>>9.99" LABEL "Add Qty" 
    FIELD price    AS DECIMAL FORMAT ">>>,>>>,>>9.99" LABEL "Unit Price"
    FIELD l-price  AS DECIMAL FORMAT ">>>,>>>,>>9.99" LABEL "Last Purchase Price" /*Naufal*/
    FIELD unit     AS CHAR    FORMAT "x(3)" LABEL "D-Unit" /*SIS 05/12/12 */
    FIELD content  AS DECIMAL FORMAT ">>,>>9.99" LABEL "Content" 
    FIELD amount   AS DECIMAL FORMAT ">,>>>,>>>,>>9.99" LABEL "Amount" 
    FIELD deliver  AS DECIMAL FORMAT ">>,>>9.99" LABEL "Delivered" 
    FIELD dept     AS INTEGER FORMAT ">>" LABEL "Dept" 
    FIELD supplier AS CHAR    FORMAT "x(32)" LABEL "Supplier"
    FIELD id       AS CHAR    FORMAT "x(4)" LABEL "ID" 
    FIELD cid      AS CHAR    FORMAT "x(4)" LABEL "CID" 
    FIELD price1   AS DECIMAL 
    FIELD qty1     AS DECIMAL
    FIELD lief-nr  AS INTEGER
    FIELD approved AS LOGICAL INIT NO
    FIELD remark   AS CHAR    FORMAT "x(180)" LABEL "Remark"
    /*NAUFAL 120321 - Testing add field for stock oh value*/
    FIELD soh      AS DECIMAL FORMAT ">>,>>9.99" LABEL "Actual Qty"
    FIELD dml-nr   AS CHARACTER
    FIELD qty2     AS DECIMAL.

DEFINE TEMP-TABLE qlist
    FIELD datum   AS DATE
    FIELD depart  AS INTEGER
    FIELD number1 AS INTEGER
.

DEFINE INPUT-OUTPUT PARAMETER TABLE FOR c-list.
DEFINE INPUT PARAMETER user-init AS CHARACTER.
DEFINE INPUT PARAMETER curr-dept AS INTEGER.
DEFINE INPUT PARAMETER selected-date AS DATE.
DEFINE INPUT PARAMETER curr-select AS CHARACTER.

DEFINE BUFFER breslin FOR reslin-queasy.

DEFINE VARIABLE dml-no  AS CHARACTER.
DEFINE VARIABLE counter AS INT.
DEFINE VARIABLE temp-nr AS CHAR.

FOR EACH qlist:
    DELETE qlist.
END.

temp-nr = "D" + STRING(curr-dept, "99") + SUBSTR(STRING(YEAR(selected-date)),3,2) 
      + STRING(MONTH(selected-date), "99") + STRING(DAY(selected-date), "99").
counter = 1.

FIND FIRST dml-artdep WHERE dml-artdep.datum EQ selected-date
    AND dml-artdep.departement EQ curr-dept EXCLUSIVE-LOCK NO-ERROR. /* add new validation so DML no 1 not skipped after removed and added again by Oscar */
IF AVAILABLE dml-artdep THEN
DO:
    counter = counter + 1.
END.

FIND FIRST reslin-queasy WHERE reslin-queasy.KEY EQ "DML"
    AND reslin-queasy.date1 EQ selected-date
    AND INT(ENTRY(2,reslin-queasy.char1,";")) EQ curr-dept NO-LOCK NO-ERROR.
DO WHILE AVAILABLE reslin-queasy:
    ASSIGN
        counter = reslin-queasy.number2.

    FIND NEXT reslin-queasy WHERE reslin-queasy.KEY EQ "DML"
        AND reslin-queasy.date1 EQ selected-date
        AND INT(ENTRY(2,reslin-queasy.char1,";")) EQ curr-dept NO-LOCK NO-ERROR.
END.

FIND FIRST breslin WHERE breslin.KEY EQ "DML"
    AND breslin.date1 EQ selected-date
    AND INT(ENTRY(2,breslin.char1,";")) EQ curr-dept 
    AND breslin.number2 EQ counter NO-LOCK NO-ERROR.
IF AVAILABLE breslin THEN
DO:
    counter = counter + 1.
END.

dml-no = temp-nr + STRING(counter, "999").

FOR EACH c-list : 
    c-list.qty = c-list.qty + c-list.a-qty. 
    IF c-list.qty LT 0 THEN c-list.qty = 0. 
    c-list.a-qty = 0. 
    c-list.amount = c-list.qty * c-list.price. 
    c-list.cid = user-init.
    IF curr-select EQ "chg" THEN
    DO:
        dml-no  = c-list.dml-nr.
        counter = INT(SUBSTRING(c-list.dml-nr, 11, 2)).
    END. 

    RUN dml-list-save-it_3bl.p(curr-dept, c-list.artnr, c-list.qty, selected-date, user-init,
    c-list.price, c-list.lief-nr, c-list.approved, c-list.remark, curr-select, dml-no, counter).
    
    IF c-list.approved THEN DO:
        FIND FIRST qlist WHERE qlist.datum = selected-date
        AND qlist.depart = curr-dept AND qlist.number1 = counter NO-ERROR.
        IF NOT AVAILABLE qlist THEN 
        DO:
            CREATE qlist.
            ASSIGN qlist.datum = selected-date
                   qlist.depart = curr-dept.

            IF counter = 1 THEN qlist.number1 = 0.
            ELSE qlist.number1 = counter.

            FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK NO-ERROR.
            CREATE res-history. 
            ASSIGN 
              res-history.nr        = bediener.nr 
              res-history.datum     = TODAY 
              res-history.zeit      = TIME 
              res-history.action    = "DML"
              res-history.aenderung = "Approved DML By :"  + bediener.username + " DML Number : " 
                                      + dml-no + " Departement : " + STRING(curr-dept)
            . 
            RELEASE res-line.
        END.
    END.
   
END.

FOR EACH c-list:
    DELETE c-list.
END.

FIND FIRST queasy WHERE queasy.KEY = 253 NO-LOCK NO-ERROR.
IF AVAILABLE queasy THEN 
DO:
    FOR EACH qlist BY qlist.datum BY qlist.depart:
        DO:
            DISP qlist.depart qlist.datum qlist.number1.  
            FIND FIRST queasy WHERE queasy.KEY = 254 AND queasy.number1 = qlist.depart 
                AND queasy.date1 = qlist.datum  AND queasy.logi1 = YES 
                AND queasy.number3 = qlist.number1 NO-LOCK NO-ERROR.
            IF NOT AVAILABLE queasy THEN DO:
                CREATE queasy.
                ASSIGN 
                    queasy.KEY      = 254 
                    queasy.number1  = qlist.depart
                    queasy.date1    = qlist.datum
                    queasy.logi1    = YES 
                    queasy.logi2    = NO
                    queasy.number3  = qlist.number1.  
            END.
        END.
        DELETE qlist.
    END.
END.

/* cleaning data if there is item with qty LE 0 for item created before new update by Oscar */
/* FOR EACH dml-artdep WHERE dml-artdep.anzahl LE 0
AND dml-artdep.datum EQ selected-date
AND dml-artdep.departement EQ curr-dept EXCLUSIVE-LOCK:
    DELETE dml-artdep.
    RELEASE dml-artdep.

END.
FIND FIRST breslin WHERE breslin.KEY EQ "DML"
AND ENTRY(2, breslin.char3, ";") EQ dml-no NO-LOCK NO-ERROR.
IF AVAILABLE breslin THEN
DO:
    FOR EACH reslin-queasy WHERE reslin-queasy.KEY EQ "DML"
    AND reslin-queasy.date1 EQ selected-date
    AND INT(ENTRY(2,reslin-queasy.char1,";")) EQ curr-dept
    AND ENTRY(2, reslin-queasy.char3, ";") EQ dml-no
    AND reslin-queasy.deci2 LE 0 EXCLUSIVE-LOCK:
        DELETE reslin-queasy.
        RELEASE reslin-queasy.
    END.
END. */

/*NAUFAL 070621 - move from UI*/
/* RUN dml-list-create-it_2bl.p(curr-dept, selected-date, dml-no, OUTPUT TABLE supply-list,
        OUTPUT TABLE c-list). */
