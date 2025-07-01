
DEFINE TEMP-TABLE t-list 
    FIELD s-recid     AS INTEGER
    FIELD t-status    AS INTEGER
    FIELD datum       AS DATE 
    FIELD deptNo      AS INTEGER
    FIELD lager-nr    AS INTEGER
    FIELD to-stock    AS INTEGER
    FIELD anzahl      AS DECIMAL
    FIELD einzelpreis AS DECIMAL
    FIELD warenwert   AS DECIMAL
    FIELD deptName    AS CHAR FORMAT "x(24)"
    FIELD lscheinnr   AS CHAR FORMAT "x(11)" 
    FIELD f-bezeich   AS CHAR FORMAT "x(16)" 
    FIELD t-bezeich   AS CHAR FORMAT "x(16)" 
    FIELD artnr       AS CHAR FORMAT "x(7)" 
    FIELD bezeich     AS CHAR FORMAT "x(24)" 
    FIELD einheit     AS CHAR FORMAT "x(3)" 
    FIELD content     AS DECIMAL FORMAT ">>>,>>9" 
    FIELD price       AS CHAR FORMAT "x(20)" 
    FIELD qty         AS DECIMAL FORMAT ">>>,>>9.999" 
    FIELD qty1        AS DECIMAL FORMAT ">>>,>>9.999" 
    FIELD val         AS DECIMAL FORMAT ">>,>>>,>>>,>>9.99"
    FIELD fibukonto   AS CHAR FORMAT "x(12)" LABEL "AcctNo"
    FIELD ID          AS CHAR FORMAT "x(4)"
    FIELD appStr      AS CHAR FORMAT "x(3)" LABEL "APP" INIT ""
    FIELD appFlag     AS LOGICAL INIT NO

    FIELD stornogrund AS CHARACTER
    FIELD gl-bezeich  AS CHARACTER
    FIELD art-bezeich AS CHARACTER
    FIELD art-lief-einheit AS INT
    FIELD art-traubensort  AS CHAR
    FIELD zwkum            LIKE l-artikel.zwkum
    FIELD endkum           LIKE l-artikel.endkum
    FIELD centername       AS CHAR
    FIELD stock-oh         AS DECIMAL /*FD August 10, 2020*/
    FIELD total            AS DECIMAL FORMAT ">>,>>>,>>>,>>9.99" /* add by damen 29/03/23 371A40 */
    FIELD issue-date       AS DATE /* Naufal Afthar - CA7568 -> add issuing date field*/
    FIELD approved-by      AS CHAR
. 

/* Oscar (14/03/25) - 3E510E - save sr-remark to new table */
DEFINE TEMP-TABLE sr-remark-list
    FIELD lscheinnr AS CHARACTER
    FIELD sr-remark  AS CHARACTER
.

/*
DEFINE TEMP-TABLE t-list 
    FIELD s-recid     AS INTEGER
    FIELD t-status    AS INTEGER
    FIELD datum       AS DATE 
    FIELD deptNo      AS INTEGER
    FIELD lager-nr    AS INTEGER
    FIELD to-stock    AS INTEGER
    FIELD anzahl      AS DECIMAL
    FIELD einzelpreis AS DECIMAL
    FIELD warenwert   AS DECIMAL
    FIELD deptName    AS CHAR FORMAT "x(24)"
    FIELD lscheinnr   AS CHAR FORMAT "x(11)" 
    FIELD f-bezeich   AS CHAR FORMAT "x(16)" 
    FIELD t-bezeich   AS CHAR FORMAT "x(16)" 
    FIELD artnr       AS CHAR FORMAT "x(7)" 
    FIELD bezeich     AS CHAR FORMAT "x(24)" 
    FIELD einheit     AS CHAR FORMAT "x(3)" 
    FIELD content     AS DECIMAL FORMAT ">>>,>>>" 
    FIELD price       AS CHAR FORMAT "x(13)" 
    FIELD qty         AS DECIMAL FORMAT ">>>,>>9.999" 
    FIELD qty1        AS DECIMAL FORMAT ">>>,>>9.999" 
    FIELD val         AS DECIMAL FORMAT ">>,>>>,>>>,>>9.99"
    FIELD fibukonto   AS CHAR FORMAT "x(12)" LABEL "AcctNo"
    FIELD gl-bezeich  AS CHAR 
    FIELD ID          AS CHAR FORMAT "x(4)"
    FIELD appStr      AS CHAR FORMAT "x(3)" LABEL "APP" INIT ""
    FIELD appFlag     AS LOGICAL INIT NO

    FIELD lief-einheit AS INT
    FIELD traubensort AS CHAR
    FIELD stornogrund AS CHAR
. 
*/

DEF INPUT PARAMETER from-date       AS DATE.
DEF INPUT PARAMETER to-date         AS DATE.
DEF INPUT PARAMETER from-dept       AS INT.
DEF INPUT PARAMETER to-dept         AS INT.
DEF INPUT PARAMETER curr-lschein    AS CHAR.
DEF INPUT PARAMETER show-price      AS LOGICAL.
DEF INPUT PARAMETER filter          AS CHARACTER.

DEF OUTPUT PARAMETER it-exist       AS LOGICAL.
DEF OUTPUT PARAMETER TABLE FOR t-list.
DEF OUTPUT PARAMETER TABLE FOR sr-remark-list. /* Oscar (05/03/25) - 3E510E - add SR Remark to print */

DEFINE VARIABLE appFLag     AS LOGICAL NO-UNDO.
DEFINE VARIABLE long-digit  AS LOGICAL. 
FIND FIRST htparam WHERE paramnr = 246 NO-LOCK. 
long-digit = htparam.flogical.

RUN create-list.


PROCEDURE create-list: 
    DEFINE VARIABLE lscheinnr       AS CHARACTER. 
    DEFINE VARIABLE qty             AS DECIMAL FORMAT "->>,>>>,>>9.999". 
    DEFINE VARIABLE qty1            AS DECIMAL FORMAT "->>,>>>,>>9.999". 
    DEFINE VARIABLE val             AS DECIMAL. 
    DEFINE VARIABLE amount          AS DECIMAL FORMAT "->>>,>>>,>>9.999" INITIAL 0. /* add by damen 29/03/23 371A40 */
    DEFINE VARIABLE t-qty           AS DECIMAL FORMAT "->>>,>>>,>>9.999" INITIAL 0.
    DEFINE VARIABLE t-qty1          AS DECIMAL FORMAT "->>>,>>>,>>9.999" INITIAL 0. 
    DEFINE VARIABLE t-val           AS DECIMAL INITIAL 0. 
    DEFINE VARIABLE t-amount        AS DECIMAL FORMAT "->>>,>>>,>>9.999" INITIAL 0. /* add by damen 29/03/23 371A40 */
    DEFINE VARIABLE appFlag         AS LOGICAL.
    DEFINE VARIABLE deptNo          AS INTEGER.
    DEFINE VARIABLE curr-centername AS CHARACTER. /* Oscar (16/04/25) - C7BC31 - Fix department name not showing correctly on insert, modify, outgoing pop-up */

    DEFINE BUFFER tl-op FOR l-op.

    it-exist = NO. 
    FOR EACH t-list: 
        DELETE t-list. 
    END. 
 
    ASSIGN
        qty  = 0 
        val  = 0
        qty1 = 0
        amount = 0
        lscheinnr = "".

    IF filter EQ "ALL" THEN
    DO:
      FOR EACH l-op WHERE l-op.datum GE from-date AND l-op.datum LE to-date 
          AND l-op.reorgflag GE from-dept AND l-op.reorgflag LE to-dept
          AND l-op.op-art GE 13 AND l-op.op-art LE 14 
          AND l-op.herkunftflag LE 2 AND l-op.loeschflag LE 1 
          NO-LOCK USE-INDEX artopart_ix, 
          FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr 
          NO-LOCK BY l-op.reorgflag BY l-op.lscheinnr BY l-op.zeit: 

          appFlag = NO.
          FIND FIRST l-ophdr WHERE l-ophdr.op-typ = "REQ"
              AND l-ophdr.lscheinnr = l-op.lscheinnr
              AND l-ophdr.docu-nr = l-op.lscheinnr NO-LOCK NO-ERROR.
          IF AVAILABLE l-ophdr THEN appFlag = l-ophdr.betriebsnr NE 0.

          RUN create-list-data(INPUT-OUTPUT lscheinnr, INPUT-OUTPUT qty, INPUT-OUTPUT qty1, 
                               INPUT-OUTPUT val, INPUT-OUTPUT amount, INPUT-OUTPUT t-qty, 
                               INPUT-OUTPUT t-qty1, INPUT-OUTPUT t-val, INPUT-OUTPUT t-amount,
                               INPUT-OUTPUT appFlag, INPUT-OUTPUT deptNo, INPUT-OUTPUT curr-centername). /* Oscar (16/04/25) - C7BC31 - Fix department name not showing correctly on insert, modify, outgoing pop-up */
      END.
    END.
    ELSE IF filter EQ "NO-APPROVE" THEN
    DO:
      FOR EACH l-op WHERE l-op.datum GE from-date AND l-op.datum LE to-date 
          AND l-op.reorgflag GE from-dept AND l-op.reorgflag LE to-dept
          AND l-op.op-art GE 13 AND l-op.op-art LE 14 
          AND l-op.herkunftflag LE 2 AND l-op.loeschflag LE 1 
          NO-LOCK USE-INDEX artopart_ix, 
          FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr 
          NO-LOCK BY l-op.reorgflag BY l-op.lscheinnr BY l-op.zeit: 

          appFlag = NO.
          FIND FIRST l-ophdr WHERE l-ophdr.op-typ = "REQ"
              AND l-ophdr.lscheinnr = l-op.lscheinnr
              AND l-ophdr.docu-nr = l-op.lscheinnr NO-LOCK NO-ERROR.
          IF AVAILABLE l-ophdr THEN appFlag = l-ophdr.betriebsnr NE 0.

          IF appFlag EQ NO THEN
            RUN create-list-data(INPUT-OUTPUT lscheinnr, INPUT-OUTPUT qty, INPUT-OUTPUT qty1, 
                                 INPUT-OUTPUT val, INPUT-OUTPUT amount, INPUT-OUTPUT t-qty, 
                                 INPUT-OUTPUT t-qty1, INPUT-OUTPUT t-val, INPUT-OUTPUT t-amount,
                                 INPUT-OUTPUT appFlag, INPUT-OUTPUT deptNo, INPUT-OUTPUT curr-centername). /* Oscar (16/04/25) - C7BC31 - Fix department name not showing correctly on insert, modify, outgoing pop-up */
      END.
    END.
    ELSE IF filter EQ "APPROVE" THEN
    DO:
      FOR EACH l-op WHERE l-op.datum GE from-date AND l-op.datum LE to-date 
          AND l-op.reorgflag GE from-dept AND l-op.reorgflag LE to-dept
          AND l-op.op-art GE 13 AND l-op.op-art LE 14 
          AND l-op.herkunftflag LE 2 AND l-op.loeschflag LE 1 
          NO-LOCK USE-INDEX artopart_ix, 
          FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr 
          NO-LOCK BY l-op.reorgflag BY l-op.lscheinnr BY l-op.zeit: 

          appFlag = NO.
          FIND FIRST l-ophdr WHERE l-ophdr.op-typ = "REQ"
              AND l-ophdr.lscheinnr = l-op.lscheinnr
              AND l-ophdr.docu-nr = l-op.lscheinnr NO-LOCK NO-ERROR.
          IF AVAILABLE l-ophdr THEN appFlag = l-ophdr.betriebsnr NE 0.

          IF appFlag EQ YES THEN
            RUN create-list-data(INPUT-OUTPUT lscheinnr, INPUT-OUTPUT qty, INPUT-OUTPUT qty1, 
                                 INPUT-OUTPUT val, INPUT-OUTPUT amount, INPUT-OUTPUT t-qty, 
                                 INPUT-OUTPUT t-qty1, INPUT-OUTPUT t-val, INPUT-OUTPUT t-amount,
                                 INPUT-OUTPUT appFlag, INPUT-OUTPUT deptNo, INPUT-OUTPUT curr-centername). /* Oscar (16/04/25) - C7BC31 - Fix department name not showing correctly on insert, modify, outgoing pop-up */
      END.
    END.
    ELSE IF filter EQ "OUTGOING" THEN
    DO:
      FOR EACH l-op WHERE l-op.datum GE from-date AND l-op.datum LE to-date 
          AND l-op.reorgflag GE from-dept AND l-op.reorgflag LE to-dept
          AND l-op.op-art GE 13 AND l-op.op-art LE 14 
          AND l-op.herkunftflag LE 2 AND l-op.loeschflag LE 1 
          NO-LOCK USE-INDEX artopart_ix, 
          FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr 
          NO-LOCK BY l-op.reorgflag BY l-op.lscheinnr BY l-op.zeit: 

          appFlag = NO.
          FIND FIRST l-ophdr WHERE l-ophdr.op-typ = "REQ"
              AND l-ophdr.lscheinnr = l-op.lscheinnr
              AND l-ophdr.docu-nr = l-op.lscheinnr NO-LOCK NO-ERROR.
          IF AVAILABLE l-ophdr THEN appFlag = l-ophdr.betriebsnr NE 0.

          FIND FIRST tl-op WHERE tl-op.lscheinnr EQ l-op.lscheinnr
              AND (tl-op.op-art EQ 3
                   OR tl-op.op-art EQ 4)
              AND tl-op.loeschflag LE 1 NO-LOCK NO-ERROR.
          
          IF AVAILABLE tl-op THEN
          DO:
            RELEASE tl-op.
            RUN create-list-data(INPUT-OUTPUT lscheinnr, INPUT-OUTPUT qty, INPUT-OUTPUT qty1, 
                                INPUT-OUTPUT val, INPUT-OUTPUT amount, INPUT-OUTPUT t-qty, 
                                INPUT-OUTPUT t-qty1, INPUT-OUTPUT t-val, INPUT-OUTPUT t-amount,
                                INPUT-OUTPUT appFlag, INPUT-OUTPUT deptNo, INPUT-OUTPUT curr-centername). /* Oscar (16/04/25) - C7BC31 - Fix department name not showing correctly on insert, modify, outgoing pop-up */
          END.
      END.
    END.
    ELSE IF filter EQ "DELETE" THEN
    DO:
      FOR EACH l-op WHERE l-op.datum GE from-date AND l-op.datum LE to-date 
          AND l-op.reorgflag GE from-dept AND l-op.reorgflag LE to-dept
          AND l-op.op-art GE 13 AND l-op.op-art LE 14 
          AND l-op.herkunftflag LE 2 AND l-op.loeschflag EQ 2 
          NO-LOCK USE-INDEX artopart_ix, 
          FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr 
          NO-LOCK BY l-op.reorgflag BY l-op.lscheinnr BY l-op.zeit: 

          appFlag = NO.
          FIND FIRST l-ophdr WHERE l-ophdr.op-typ = "REQ"
              AND l-ophdr.lscheinnr = l-op.lscheinnr
              AND l-ophdr.docu-nr = l-op.lscheinnr NO-LOCK NO-ERROR.
          IF AVAILABLE l-ophdr THEN appFlag = l-ophdr.betriebsnr NE 0.

          RUN create-list-data(INPUT-OUTPUT lscheinnr, INPUT-OUTPUT qty, INPUT-OUTPUT qty1, 
                                INPUT-OUTPUT val, INPUT-OUTPUT amount, INPUT-OUTPUT t-qty, 
                                INPUT-OUTPUT t-qty1, INPUT-OUTPUT t-val, INPUT-OUTPUT t-amount,
                                INPUT-OUTPUT appFlag, INPUT-OUTPUT deptNo, INPUT-OUTPUT curr-centername). /* Oscar (16/04/25) - C7BC31 - Fix department name not showing correctly on insert, modify, outgoing pop-up */
      END.
    END.

    IF qty NE 0 THEN 
    DO: 
        CREATE t-list.
        ASSIGN
            t-list.price = "Total" 
            t-list.qty   = qty
            t-list.qty1  = qty1
            t-list.val   = val
            t-list.total = amount /* add by damen 29/03/23 371A40 */
        . 
    END. 
    IF t-qty NE 0 THEN 
    DO: 
        CREATE t-list. 
        ASSIGN
            t-list.price = "Grand Total"
            t-list.qty  = t-qty
            t-list.qty1 = t-qty1
            t-list.val  = t-val
            t-list.total = t-amount /* add by damen 29/03/23 371A40 */
        . 
    END. 
    RELEASE t-list.
END. 

PROCEDURE create-list-data:
  DEFINE INPUT-OUTPUT PARAMETER lscheinnr       AS CHAR. 
  DEFINE INPUT-OUTPUT PARAMETER qty             AS DECIMAL FORMAT "->>,>>>,>>9.999". 
  DEFINE INPUT-OUTPUT PARAMETER qty1            AS DECIMAL FORMAT "->>,>>>,>>9.999". 
  DEFINE INPUT-OUTPUT PARAMETER val             AS DECIMAL. 
  DEFINE INPUT-OUTPUT PARAMETER amount          AS DECIMAL FORMAT "->>>,>>>,>>9.999" INITIAL 0.
  DEFINE INPUT-OUTPUT PARAMETER t-qty           AS DECIMAL FORMAT "->>>,>>>,>>9.999" INITIAL 0.
  DEFINE INPUT-OUTPUT PARAMETER t-qty1          AS DECIMAL FORMAT "->>>,>>>,>>9.999" INITIAL 0. 
  DEFINE INPUT-OUTPUT PARAMETER t-val           AS DECIMAL INITIAL 0. 
  DEFINE INPUT-OUTPUT PARAMETER t-amount        AS DECIMAL FORMAT "->>>,>>>,>>9.999" INITIAL 0.
  DEFINE INPUT-OUTPUT PARAMETER appFlag         AS LOGICAL.
  DEFINE INPUT-OUTPUT PARAMETER deptNo          AS INTEGER INITIAL 0.
  DEFINE INPUT-OUTPUT PARAMETER curr-centername AS CHARACTER INITIAL "". /* Oscar (16/04/25) - C7BC31 - Fix department name not showing correctly on insert, modify, outgoing pop-up */

  DEFINE VARIABLE do-it           AS LOGICAL.
  DEFINE VARIABLE deptName        AS CHAR.

  DEFINE BUFFER l-store FOR l-lager. 
  DEFINE BUFFER tl-op FOR l-op. /* Naufal Afthar - CA7568*/
  DEFINE BUFFER b-l-op FOR l-op.

  do-it = YES.
  IF curr-lschein NE "" THEN do-it = l-op.lscheinnr = curr-lschein.
  IF do-it THEN
  DO:
      it-exist = YES. 
      RELEASE l-store.
      FIND FIRST l-lager WHERE l-lager.lager-nr = l-op.lager-nr NO-LOCK. 
      IF l-op.op-art = 14 THEN 
          FIND FIRST l-store WHERE l-store.lager-nr = l-op.pos NO-LOCK NO-ERROR. 

      IF lscheinnr NE l-op.lscheinnr AND qty NE 0 THEN 
      DO: 
          CREATE t-list. 
          t-list.price = "Total". 
          t-list.qty = qty. 
          t-list.val = val. 
          t-list.qty1 = qty1.
          t-list.total = amount. /* add by damen 29/03/23 371A40 */
          qty  = 0. 
          val  = 0. 
          qty1 = 0.
          amount = 0. /* add by damen 29/03/23 371A40 */
      END. 
      lscheinnr = l-op.lscheinnr. 

      IF l-op.reorgflag NE deptNo THEN
      DO:
          deptNo = l-op.reorgflag.
          FIND FIRST parameters WHERE parameters.progname = "CostCenter" 
              AND parameters.section = "Name" 
              AND INTEGER(parameters.varname) = deptNo NO-LOCK NO-ERROR. 
          CREATE t-list.
          ASSIGN t-list.deptNo = deptNo.
          IF AVAILABLE parameters THEN 
          DO:
              ASSIGN
                  t-list.bezeich = parameters.vstring
                  curr-centername = parameters.vstring.
          END.
          ELSE 
              ASSIGN
                  t-list.bezeich = "???"
                  curr-centername = "???".
      END.

      CREATE t-list. 
      RUN add-id.
      ASSIGN
          t-list.s-recid          = RECID(l-op)
          t-list.deptNo           = deptNo
          t-list.t-status         = l-op.herkunftflag
          t-list.datum            = l-op.datum 
          t-list.lager-nr         = l-op.lager-nr
          t-list.to-stock         = l-op.pos
          t-list.anzahl           = l-op.anzahl
          t-list.qty1             = l-op.deci1[1]
          t-list.qty              = l-op.anzahl
          t-list.einzelpreis      = l-op.einzelpreis
          t-list.warenwert        = l-op.warenwert
          t-list.lscheinnr        = lscheinnr 
          t-list.f-bezeich        = l-lager.bezeich 
          t-list.artnr            = STRING(l-op.artnr, "9999999")
          t-list.bezeich          = l-artikel.bezeich
          t-list.einheit          = l-artikel.masseinheit 
          t-list.content          = l-artikel.inhalt
          t-list.appFlag          = appFlag
          t-list.stornogrund      = l-op.stornogrund
          t-list.art-bezeich      = l-artikel.bezeich
          t-list.art-lief-einheit = l-artikel.lief-einheit
          t-list.art-traubensort  = l-artikel.traubensort
          t-list.zwkum            = l-artikel.zwkum
          t-list.endkum           = l-artikel.endkum
          t-list.centername       = curr-centername
      .

      /* Naufal Afthar - CA7568*/
      FIND FIRST tl-op WHERE tl-op.lscheinnr EQ l-op.lscheinnr
          AND tl-op.op-art EQ 3
          AND tl-op.loeschflag LE 1 NO-LOCK NO-ERROR.
      IF AVAILABLE tl-op THEN
          ASSIGN t-list.issue-date = tl-op.datum.
      /* end Naufal Afthar*/

      FIND FIRST l-bestand WHERE l-bestand.artnr = l-op.artnr
          AND l-bestand.lager-nr = l-op.lager-nr NO-LOCK NO-ERROR.
      IF AVAILABLE l-bestand THEN t-list.stock-oh = l-bestand.anz-anf-best
                                                  + l-bestand.anz-eingang - l-bestand.anz-ausgang.

      /* Oscar (13/04/25) - ACE54F - adjust for user story 1  */
      FIND FIRST b-l-op WHERE b-l-op.lscheinnr EQ l-op.lscheinnr
          AND b-l-op.artnr EQ l-op.artnr
          AND b-l-op.op-art GE 3
          AND b-l-op.op-art LE 4 NO-LOCK NO-ERROR.
      IF NOT AVAILABLE b-l-op THEN
      DO:
        IF t-list.t-status EQ 2 THEN
        DO:
            t-list.t-status = 3.
        END.
      END.

      t-list.deptName    = l-lager.bezeich.  /*ITA 040417*/
      IF l-op.op-art = 14 THEN t-list.deptName    = l-store.bezeich.
  
      IF appFlag THEN 
      DO:
          t-list.appStr = "Y".

          IF AVAILABLE l-ophdr THEN
          DO:
            FIND FIRST bediener WHERE bediener.nr EQ l-ophdr.betriebsnr NO-LOCK.
            IF AVAILABLE bediener THEN 
            DO:
                t-list.approved-by = STRING(bediener.userinit) + ", " +  bediener.username. /*bernatd 220B12*/
            END.
          END.
      END.
      IF AVAILABLE l-store THEN t-list.t-bezeich = l-store.bezeich. 

      IF l-op.op-art EQ 13 THEN t-list.to-stock = 0.
      IF l-op.op-art EQ 13 AND TRIM(l-op.stornogrund) NE "" THEN
      DO:
          FIND FIRST gl-acct WHERE gl-acct.fibukonto = l-op.stornogrund
              NO-LOCK NO-ERROR.
          /*FT 11/02/15*/
          IF NOT AVAILABLE gl-acct THEN
              FIND FIRST gl-acct WHERE gl-acct.bezeich = l-op.stornogrund
              NO-LOCK NO-ERROR. /*endFT*/
          IF AVAILABLE gl-acct THEN 
              ASSIGN t-list.fibukonto = gl-acct.fibukonto
                  t-list.gl-bezeich = gl-acct.bezeich.
      END.

      IF l-op.anzahl NE 0 AND show-price THEN 
      DO: 
          IF NOT long-digit THEN 
              t-list.price = STRING((l-op.warenwert / l-op.anzahl), ">>,>>>,>>9.99"). 
          ELSE 
              t-list.price = STRING((l-op.warenwert / l-op.anzahl), ">,>>>,>>>,>>9"). 
      END.
      ASSIGN
          qty  = qty + l-op.anzahl
          qty1 = qty1 + l-op.deci1[1]
          /* t-list.qty  = l-op.anzahl
          t-list.qty1 = l-op.deci1[1] */
          t-qty = t-qty + l-op.anzahl
          t-qty1 = t-qty1 + l-op.deci1[1]
          t-list.total = decimal(t-list.price) * t-list.qty /* add by damen 29/03/23 371A40 */
          amount   = amount + t-list.total /* add by damen 29/03/23 371A40 */
          t-amount = t-amount + t-list.total /* add by damen 29/03/23 371A40 */
      . 
      IF show-price THEN 
          ASSIGN 
              t-list.val = l-op.warenwert 
              val = val + l-op.warenwert 
              t-val = t-val + l-op.warenwert
          . 

      /* Oscar (05/03/25) - 3E510E - add SR Remark to print */
      FIND FIRST sr-remark-list WHERE sr-remark-list.lscheinnr EQ l-op.lscheinnr NO-LOCK NO-ERROR.
      IF NOT AVAILABLE sr-remark-list THEN
      DO:
          CREATE sr-remark-list.

          FIND FIRST queasy WHERE queasy.KEY EQ 343 
              AND queasy.char1 EQ l-op.lscheinnr NO-LOCK NO-ERROR.
          IF AVAILABLE queasy THEN
          DO:
              ASSIGN 
                  sr-remark-list.lscheinnr = l-op.lscheinnr
                  sr-remark-list.sr-remark = queasy.char2
              .
          END.
          ELSE
          DO:
              ASSIGN 
                  sr-remark-list.lscheinnr = l-op.lscheinnr
                  sr-remark-list.sr-remark = ""
              .
          END.
      END.
  END.
END.

/*MT
PROCEDURE create-list: 
DEFINE VARIABLE lscheinnr   AS CHAR. 
DEFINE VARIABLE qty         AS DECIMAL FORMAT "->>,>>>,>>9.999". 
DEFINE VARIABLE val         AS DECIMAL. 
DEFINE VARIABLE t-qty       AS DECIMAL FORMAT "->>>,>>>,>>9.999" INITIAL 0. 
DEFINE VARIABLE t-val       AS DECIMAL INITIAL 0. 
DEFINE VARIABLE do-it       AS LOGICAL.
DEFINE VARIABLE deptNo      AS INTEGER INITIAL 0.
DEFINE VARIABLE deptName    AS CHAR.
DEFINE VARIABLE appFLag     AS LOGICAL NO-UNDO.
DEFINE BUFFER l-store FOR l-lager. 

  STATUS DEFAULT "Processing...". 

  it-exist = NO. 
  FOR EACH t-list: 
    DELETE t-list. 
  END. 
 
  qty = 0. 
  val= 0. 
  lscheinnr = "". 
  FOR EACH l-op WHERE l-op.datum GE from-date AND l-op.datum LE to-date 
    AND l-op.reorgflag GE from-dept AND l-op.reorgflag LE to-dept
    AND l-op.op-art GE 13 AND l-op.op-art LE 14 
    AND l-op.herkunftflag LE 2 AND l-op.loeschflag LE 1 
    NO-LOCK USE-INDEX artopart_ix, 
    FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr 
    NO-LOCK BY l-op.reorgflag BY l-op.lscheinnr BY l-op.zeit: 
    
    appFLag = NO.
    FIND FIRST l-ophdr WHERE l-ophdr.op-typ = "REQ"
      AND l-ophdr.lscheinnr = l-op.lscheinnr
      AND l-ophdr.docu-nr = l-op.lscheinnr NO-LOCK NO-ERROR.
    IF AVAILABLE l-ophdr THEN appFLag = l-ophdr.betriebsnr NE 0.

    do-it = YES.
    IF curr-lschein NE "" THEN do-it = l-op.lscheinnr = curr-lschein.
    IF do-it THEN
    DO:
      it-exist = YES. 
      RELEASE l-store.
      FIND FIRST l-lager WHERE l-lager.lager-nr = l-op.lager-nr NO-LOCK. 
      IF l-op.op-art = 14 THEN 
        FIND FIRST l-store WHERE l-store.lager-nr = l-op.pos NO-LOCK NO-ERROR. 
 
      IF lscheinnr NE l-op.lscheinnr AND qty NE 0 THEN 
      DO: 
        CREATE t-list. 
        t-list.price = "Total". 
        t-list.qty = qty. 
        t-list.val = val. 
        qty = 0. 
        val = 0. 
      END. 
      lscheinnr = l-op.lscheinnr. 
 
      IF l-op.reorgflag NE deptNo THEN
      DO:
        deptNo = l-op.reorgflag.
        FIND FIRST parameters WHERE parameters.progname = "CostCenter" 
          AND parameters.section = "Name" 
          AND INTEGER(parameters.varname) = deptNo NO-LOCK NO-ERROR. 
        CREATE t-list.
        ASSIGN t-list.deptNo = deptNo.
        IF AVAILABLE parameters THEN t-list.bezeich = parameters.vstring.
        ELSE t-list.bezeich = "???".
      END.

      CREATE t-list. 
      RUN add-id.
      ASSIGN
        t-list.s-recid     = RECID(l-op)
        t-list.deptNo      = deptNo
        t-list.t-status    = l-op.herkunftflag
        t-list.datum       = l-op.datum 
        t-list.lager-nr    = l-op.lager-nr
        t-list.to-stock    = l-op.pos
        t-list.anzahl      = l-op.anzahl
        t-list.qty1        = l-op.deci1[1]
        t-list.einzelpreis = l-op.einzelpreis
        t-list.warenwert   = l-op.warenwert
        t-list.lscheinnr   = lscheinnr 
        t-list.f-bezeich   = l-lager.bezeich 
        t-list.artnr       = STRING(l-op.artnr, "9999999")
        t-list.bezeich     = l-artikel.bezeich
        t-list.einheit     = l-artikel.masseinheit 
        t-list.content     = l-artikel.inhalt
        t-list.appFlag     = appFlag
        t-list.stornogrund = l-op.stornogrund
      . 
      IF appFlag THEN t-list.appStr = "Y".
      IF AVAILABLE l-store THEN t-list.t-bezeich = l-store.bezeich. 

      IF l-op.op-art EQ 13 THEN t-list.to-stock = 0.
      IF l-op.op-art EQ 13 AND TRIM(l-op.stornogrund) NE "" THEN
      DO:
        FIND FIRST gl-acct WHERE gl-acct.fibukonto = l-op.stornogrund
          NO-LOCK NO-ERROR.
        IF AVAILABLE gl-acct THEN ASSIGN t-list.fibukonto = gl-acct.fibukonto.
      END.

      IF l-op.anzahl NE 0 AND show-price THEN 
      DO: 
        IF NOT long-digit THEN 
          t-list.price = STRING((l-op.warenwert / l-op.anzahl), ">>,>>>,>>9.99"). 
        ELSE 
        t-list.price = STRING((l-op.warenwert / l-op.anzahl), ">,>>>,>>>,>>9"). 
      END.
      ASSIGN
        qty = qty + l-op.anzahl
        t-list.qty = l-op.anzahl 
        t-qty = t-qty + l-op.anzahl
      . 
      IF show-price THEN 
      ASSIGN 
        t-list.val = l-op.warenwert 
        val = val + l-op.warenwert 
        t-val = t-val + l-op.warenwert
      . 
    END.
  END.

  IF qty NE 0 THEN 
  DO: 
    CREATE t-list.
    ASSIGN
      t-list.price = "Total" 
      t-list.qty = qty
      t-list.val = val
    . 
  END. 
  IF t-qty NE 0 THEN 
  DO: 
    CREATE t-list. 
    ASSIGN
      t-list.price = "Grand Total"
      t-list.qty = t-qty
      t-list.val = t-val
    . 
  END. 
  RELEASE t-list.
END. 
*/

/*MT
PROCEDURE create-list: 
DEFINE VARIABLE lscheinnr   AS CHAR. 
DEFINE VARIABLE qty         AS DECIMAL FORMAT "->>,>>>,>>9.999". 
DEFINE VARIABLE val         AS DECIMAL. 
DEFINE VARIABLE t-qty       AS DECIMAL FORMAT "->>>,>>>,>>9.999" INITIAL 0. 
DEFINE VARIABLE t-val       AS DECIMAL INITIAL 0. 
DEFINE VARIABLE do-it       AS LOGICAL.
DEFINE VARIABLE deptNo      AS INTEGER INITIAL 0.
DEFINE VARIABLE deptName    AS CHAR.

DEFINE BUFFER l-store FOR l-lager. 

  /*MTSTATUS DEFAULT "Processing...".*/

  it-exist = NO. 
  FOR EACH t-list: 
    DELETE t-list. 
  END. 
 
  qty = 0. 
  val= 0. 
  lscheinnr = "". 
  FOR EACH l-op WHERE l-op.datum GE from-date AND l-op.datum LE to-date 
    AND l-op.reorgflag GE from-dept AND l-op.reorgflag LE to-dept
    AND l-op.op-art GE 13 AND l-op.op-art LE 14 
    AND l-op.herkunftflag LE 2 AND l-op.loeschflag LE 1 
    NO-LOCK USE-INDEX artopart_ix, 
    FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr 
    NO-LOCK BY l-op.reorgflag BY l-op.lscheinnr BY l-op.zeit: 
    
    appFLag = NO.
    FIND FIRST l-ophdr WHERE l-ophdr.op-typ = "REQ"
      AND l-ophdr.lscheinnr = l-op.lscheinnr
      AND l-ophdr.docu-nr = l-op.lscheinnr NO-LOCK NO-ERROR.
    IF AVAILABLE l-ophdr THEN appFLag = l-ophdr.betriebsnr NE 0.

    do-it = YES.
    IF curr-lschein NE "" THEN do-it = l-op.lscheinnr = curr-lschein.
    IF do-it THEN
    DO:
      it-exist = YES. 
      RELEASE l-store.
      FIND FIRST l-lager WHERE l-lager.lager-nr = l-op.lager-nr NO-LOCK. 
      IF l-op.op-art = 14 THEN 
        FIND FIRST l-store WHERE l-store.lager-nr = l-op.pos NO-LOCK NO-ERROR. 
 
      IF lscheinnr NE l-op.lscheinnr AND qty NE 0 THEN 
      DO: 
        CREATE t-list. 
        t-list.price = "Total". 
        t-list.qty = qty. 
        t-list.val = val. 
        qty = 0. 
        val = 0. 
      END. 
      lscheinnr = l-op.lscheinnr. 
 
      IF l-op.reorgflag NE deptNo THEN
      DO:
        deptNo = l-op.reorgflag.
        FIND FIRST parameters WHERE parameters.progname = "CostCenter" 
          AND parameters.section = "Name" 
          AND INTEGER(parameters.varname) = deptNo NO-LOCK NO-ERROR. 
        CREATE t-list.
        ASSIGN t-list.deptNo = deptNo.
        IF AVAILABLE parameters THEN t-list.bezeich = parameters.vstring.
        ELSE t-list.bezeich = "???".
      END.

      CREATE t-list. 
      RUN add-id.
      ASSIGN
        t-list.s-recid     = RECID(l-op)
        t-list.deptNo      = deptNo
        t-list.t-status    = l-op.herkunftflag
        t-list.datum       = l-op.datum 
        t-list.lager-nr    = l-op.lager-nr
        t-list.to-stock    = l-op.pos
        t-list.anzahl      = l-op.anzahl
        t-list.einzelpreis = l-op.einzelpreis
        t-list.warenwert   = l-op.warenwert
        t-list.lscheinnr   = lscheinnr 
        t-list.f-bezeich   = l-lager.bezeich 
        t-list.artnr       = STRING(l-op.artnr, "9999999")
        t-list.bezeich     = l-artikel.bezeich
        t-list.einheit     = l-artikel.masseinheit 
        t-list.content     = l-artikel.inhalt
        t-list.appFlag     = appFlag
        t-list.lief-einheit = l-artikel.lief-einheit
        t-list.traubensort = l-artikel.traubensort
      . 
      IF appFlag THEN t-list.appStr = "Y".
      IF AVAILABLE l-store THEN t-list.t-bezeich = l-store.bezeich. 

      IF l-op.op-art EQ 13 THEN t-list.to-stock = 0.
      IF l-op.op-art EQ 13 AND TRIM(l-op.stornogrund) NE "" THEN
      DO:
        FIND FIRST gl-acct WHERE gl-acct.fibukonto = l-op.stornogrund
          NO-LOCK NO-ERROR.
        IF AVAILABLE gl-acct THEN 
            ASSIGN t-list.fibukonto  = gl-acct.fibukonto
                   t-list.gl-bezeich = gl-acct.bezeich.
      END.

      IF l-op.anzahl NE 0 AND show-price THEN 
      DO: 
        IF NOT long-digit THEN 
          t-list.price = STRING((l-op.warenwert / l-op.anzahl), ">>,>>>,>>9.99"). 
        ELSE 
        t-list.price = STRING((l-op.warenwert / l-op.anzahl), ">,>>>,>>>,>>9"). 
      END.
      ASSIGN
        qty = qty + l-op.anzahl
        t-list.qty = l-op.anzahl 
        t-qty = t-qty + l-op.anzahl
      . 
      IF show-price THEN 
      ASSIGN 
        t-list.val = l-op.warenwert 
        val = val + l-op.warenwert 
        t-val = t-val + l-op.warenwert
      . 
    END.
  END.

  IF qty NE 0 THEN 
  DO: 
    CREATE t-list.
    ASSIGN
      t-list.price = "Total" 
      t-list.qty = qty
      t-list.val = val
    . 
  END. 
  IF t-qty NE 0 THEN 
  DO: 
    CREATE t-list. 
    ASSIGN
      t-list.price = "Grand Total"
      t-list.qty = t-qty
      t-list.val = t-val
    . 
  END. 
  RELEASE t-list.
END. 
*/

PROCEDURE add-id:
    DEFINE BUFFER usr FOR bediener.

    FIND FIRST usr WHERE usr.nr = l-op.fuellflag NO-LOCK NO-ERROR.
    IF AVAILABLE usr THEN
        t-list.id = usr.userinit.
    ELSE t-list.id = "??".
END.

