
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
  FIELD qty         AS DECIMAL FORMAT ">>>,>>9.99" 
  FIELD qty1        AS DECIMAL FORMAT ">>>,>>9.99" 
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

DEF OUTPUT PARAMETER it-exist       AS LOGICAL.
DEF OUTPUT PARAMETER TABLE FOR t-list.

DEFINE VARIABLE appFLag     AS LOGICAL NO-UNDO.
DEFINE VARIABLE long-digit  AS LOGICAL. 
FIND FIRST htparam WHERE paramnr = 246 NO-LOCK. 
long-digit = htparam.flogical.

RUN create-list.


PROCEDURE create-list: 
DEFINE VARIABLE lscheinnr   AS CHAR. 
DEFINE VARIABLE qty         AS DECIMAL FORMAT "->>,>>>,>>9.999". 
DEFINE VARIABLE qty1        AS DECIMAL FORMAT "->>,>>>,>>9.999". 
DEFINE VARIABLE val         AS DECIMAL. 
DEFINE VARIABLE t-qty       AS DECIMAL FORMAT "->>>,>>>,>>9.999" INITIAL 0.
DEFINE VARIABLE t-qty1      AS DECIMAL FORMAT "->>>,>>>,>>9.999" INITIAL 0. 
DEFINE VARIABLE t-val       AS DECIMAL INITIAL 0. 
DEFINE VARIABLE do-it       AS LOGICAL.
DEFINE VARIABLE deptNo      AS INTEGER INITIAL 0.
DEFINE VARIABLE deptName    AS CHAR.
DEFINE VARIABLE appFLag     AS LOGICAL NO-UNDO.
DEFINE VARIABLE curr-centername AS CHAR NO-UNDO.
DEFINE BUFFER l-store FOR l-lager. 

  it-exist = NO. 
  FOR EACH t-list: 
    DELETE t-list. 
  END. 
 
  ASSIGN
      qty  = 0 
      val  = 0
      qty1 = 0
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
        t-list.qty1 = qty1.
        qty  = 0. 
        val  = 0. 
        qty1 = 0.
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
        t-list.art-traubensort  = l-artikel.traubensorte /* Malik Serverless 681 change l-artikel.traubensort -> l-artikel.traubensort */
        t-list.zwkum            = l-artikel.zwkum
        t-list.endkum           = l-artikel.endkum
        t-list.centername       = curr-centername
        .

      t-list.deptName    = l-lager.bezeich.  /*ITA 040417*/
      IF l-op.op-art = 14 THEN t-list.deptName    = l-store.bezeich.

      IF appFlag THEN t-list.appStr = "Y".
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
        t-list.qty  = l-op.anzahl
        t-list.qty1 = l-op.deci1[1]
        t-qty = t-qty + l-op.anzahl
        t-qty1 = t-qty1 + l-op.deci1[1]
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
      t-list.qty   = qty
      t-list.qty1  = qty1
      t-list.val   = val
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
    . 
  END. 
  RELEASE t-list.
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
