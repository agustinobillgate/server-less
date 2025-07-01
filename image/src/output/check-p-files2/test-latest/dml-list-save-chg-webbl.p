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
    FIELD soh      AS DECIMAL FORMAT ">>,>>9.99" LABEL "Actual Qty".

DEFINE INPUT-OUTPUT PARAMETER TABLE FOR c-list.
DEFINE INPUT PARAMETER user-init AS CHARACTER.
DEFINE INPUT PARAMETER curr-dept AS INTEGER.
DEFINE INPUT PARAMETER selected-date AS DATE.

FOR EACH c-list: 
    c-list.qty = c-list.qty + c-list.a-qty. 
    IF c-list.qty LT 0 THEN c-list.qty = 0. 
    c-list.a-qty = 0. 
    c-list.amount = c-list.qty * c-list.price. 
    c-list.cid = user-init. 
    RUN dml-list-save-it_1bl.p(curr-dept, c-list.artnr, c-list.qty, selected-date, user-init,
        c-list.price, c-list.lief-nr, c-list.approved, c-list.remark).
END.

FOR EACH c-list:
    DELETE c-list.
END.

/*NAUFAL 070621 - move from UI*/
RUN dml-list-create-it_11bl.p(curr-dept, selected-date, OUTPUT TABLE supply-list,
        OUTPUT TABLE c-list).
