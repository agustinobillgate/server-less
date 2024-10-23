DEF TEMP-TABLE t-h-artikel LIKE h-artikel
    FIELD rec-id AS INT.

DEF INPUT PARAMETER h-bline-rec-id AS INT.
DEF INPUT PARAMETER zugriff AS LOGICAL.

DEF OUTPUT PARAMETER fl-code AS INT INIT 0.
DEF OUTPUT PARAMETER fl-code1 AS INT INIT 0.
DEF OUTPUT PARAMETER fl-code2 AS INT INIT 0.
DEF OUTPUT PARAMETER fl-code3 AS INT INIT 0.
DEF OUTPUT PARAMETER qty AS INT.
DEF OUTPUT PARAMETER answer AS LOGICAL.
DEF OUTPUT PARAMETER cancel-flag AS LOGICAL.
DEF OUTPUT PARAMETER billart AS INT.
DEF OUTPUT PARAMETER description AS CHAR.
DEF OUTPUT PARAMETER price AS DECIMAL.
DEF OUTPUT PARAMETER rec-id-h-art AS INT.
DEF OUTPUT PARAMETER anz AS INT.
DEF OUTPUT PARAMETER TABLE FOR t-h-artikel.

DEFINE buffer h-art FOR vhp.h-artikel.
DEF BUFFER hbline FOR vhp.h-bill-line. 
FIND FIRST h-bill-line WHERE RECID(h-bill-line) = h-bline-rec-id.

FIND FIRST h-art WHERE h-art.artnr = vhp.h-bill-line.artnr 
  AND h-art.departement = vhp.h-bill-line.departement NO-LOCK.
rec-id-h-art = RECID(h-art).
IF h-art.artart = 0 THEN 
DO: 
  FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 261 NO-LOCK. 
  IF htparam.flogical THEN 
  DO: 
    IF NOT zugriff THEN 
    DO: 
      fl-code3 = 1.
      /*MTAPPLY "entry" TO billart. */
      RETURN. 
    END. 
  END. 

  FOR EACH hbline WHERE hbline.rechnr = vhp.h-bill-line.rechnr 
      AND hbline.bill-datum = vhp.h-bill-line.bill-datum 
      AND hbline.departement = vhp.h-bill-line.departement 
      AND hbline.artnr = vhp.h-bill-line.artnr 
      AND hbline.bezeich = vhp.h-bill-line.bezeich 
      AND hbline.epreis = vhp.h-bill-line.epreis NO-LOCK: 
      anz = anz + hbline.anzahl. 
  END. 
  IF anz = 0 THEN 
  DO: 
      fl-code = 1.
      /*MTIF billart:SENSITIVE IN FRAME frame1 THEN APPLY "entry" TO billart. 
      ELSE APPLY "entry" TO tischnr.*/
      RETURN. 
  END. 

  IF vhp.h-bill-line.anzahl GT 1 THEN 
  DO:
    fl-code1 = 1.
    RETURN.
    /*MT
    RUN TS-voidqtyUI.p (vhp.h-bill-line.anzahl, OUTPUT qty). 
    IF qty = 0 THEN 
    DO: 
      APPLY "entry" TO billart. 
      RETURN. 
    END. 
    qty = - qty.
    */
  END. 
  ELSE qty = - vhp.h-bill-line.anzahl.
  answer = NO. 
  cancel-flag = YES. 
  DO: 
    FIND FIRST vhp.h-artikel WHERE RECID(vhp.h-artikel) 
      = RECID(h-art) NO-LOCK. 
    billart = vhp.h-bill-line.artnr. 
    description = vhp.h-bill-line.bezeich. 
    price = vhp.h-bill-line.epreis. 
    fl-code2 = 1.
    /*MTRUN return-qty.*/
    CREATE t-h-artikel.
    BUFFER-COPY h-artikel TO t-h-artikel.
    ASSIGN t-h-artikel.rec-id = RECID(h-artikel).
  END.
END.
