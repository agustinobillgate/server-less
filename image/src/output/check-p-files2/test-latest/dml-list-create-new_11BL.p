DEFINE TEMP-TABLE c-list 
    FIELD zwkum    AS INTEGER INITIAL 0 
    FIELD grp      AS CHAR FORMAT "x(22)" COLUMN-LABEL "Group" 
    FIELD artnr    LIKE l-artikel.artnr 
    FIELD bezeich  AS CHAR FORMAT "x(38)" COLUMN-LABEL "Description" 
    FIELD qty      AS DECIMAL  FORMAT ">>,>>9.99" LABEL "Ordered Qty" 
    FIELD a-qty    AS DECIMAL  FORMAT "->>,>>9.99" LABEL "Add Qty" 
    FIELD price    AS DECIMAL FORMAT ">>>,>>>,>>9.99" LABEL "Unit Price"
    FIELD l-price  AS DECIMAL FORMAT ">>>,>>>,>>9.99" LABEL "Last Purchase Price" /*Naufal*/
    FIELD unit     AS CHAR FORMAT "x(3)" LABEL "Unit" 
    FIELD content  AS DECIMAL FORMAT ">>,>>9.99" LABEL "Content" 
    FIELD amount   AS DECIMAL FORMAT ">,>>>,>>>,>>9.99" LABEL "Amount" 
    FIELD deliver  AS DECIMAL FORMAT ">>,>>9.99" LABEL "Delivered" 
    FIELD dept     AS INTEGER FORMAT ">>" LABEL "Dept" 
    FIELD supplier AS CHAR FORMAT "x(32)" LABEL "Supplier"
    FIELD id       AS CHAR FORMAT "x(4)" LABEL "ID" 
    FIELD cid      AS CHAR FORMAT "x(4)" LABEL "CID" 
    FIELD price1   AS DECIMAL 
    FIELD qty1     AS DECIMAL
    FIELD lief-nr  AS INTEGER
    FIELD approved AS LOGICAL INIT NO
    FIELD remark   AS CHAR
    /*NAUFAL 150321 - add field for stock oh value*/
    FIELD soh      AS DECIMAL FORMAT ">,>>>,>>9.99" LABEL "Actual Qty"
    /*end*/
    FIELD dml-nr   AS CHARACTER
    FIELD qty2     AS DECIMAL.


DEF INPUT PARAMETER user-init AS CHAR.
DEF INPUT PARAMETER curr-dept AS INT.
DEF OUTPUT PARAMETER TABLE FOR c-list.

FOR EACH c-list.
    DELETE c-list.
END.

RUN create-new.

PROCEDURE create-new: 
    FOR EACH l-artikel WHERE l-artikel.bestellt USE-INDEX artnr_ix NO-LOCK,
     FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum NO-LOCK:
      CREATE c-list. 
      ASSIGN
      c-list.artnr 	 = l-artikel.artnr 
      c-list.grp 	 = l-untergrup.bezeich 
      c-list.zwkum 	 = l-untergrup.zwkum 
      c-list.bezeich = l-artikel.bezeich 
      c-list.price 	 = l-artikel.ek-aktuell
      c-list.l-price = l-artikel.ek-letzter /*Naufal*/
      c-list.unit 	 = l-artikel.traubensorte 
      c-list.content = l-artikel.inhalt 
      c-list.price1  = c-list.price 
      c-list.id 	 = user-init
      c-list.dept 	 = curr-dept
      .

      /*NAUFAL 150321 - add validation for add stock oh value*/
      FIND FIRST l-bestand WHERE l-bestand.artnr = l-artikel.artnr
          AND l-bestand.lager-nr = 0 NO-LOCK NO-ERROR.
      IF AVAILABLE l-bestand THEN
      DO:
        c-list.soh = l-bestand.anz-anf-best + l-bestand.anz-eingang
                   - l-bestand.anz-ausgang.
      END. 
    END.
END. 
