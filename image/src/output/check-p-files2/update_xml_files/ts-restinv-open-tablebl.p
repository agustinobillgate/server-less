DEF TEMP-TABLE t-h-bill LIKE h-bill
    FIELD rec-id AS INT.

DEF INPUT-OUTPUT  PARAMETER balance AS DECIMAL.
DEF INPUT  PARAMETER curr-dept      AS INT.
DEF INPUT  PARAMETER tischnr        AS INT.
DEF INPUT  PARAMETER curedept-flag  AS LOGICAL.
DEF INPUT  PARAMETER user-init      AS CHAR.
DEF INPUT  PARAMETER user-name      AS CHAR.
DEF INPUT  PARAMETER from-acct      AS LOGICAL.
DEF INPUT-OUTPUT PARAMETER room     AS CHAR.
DEF INPUT-OUTPUT PARAMETER gname    AS CHAR.
DEF OUTPUT PARAMETER resrecid       AS INT.
DEF OUTPUT PARAMETER kreditlimit    AS DECIMAL.
DEF OUTPUT PARAMETER curr-room      AS CHAR.
DEF OUTPUT PARAMETER rescomment     AS CHAR.
DEF OUTPUT PARAMETER curr-gname     AS CHAR.
DEF OUTPUT PARAMETER bcol           AS INT.
DEF OUTPUT PARAMETER balance-foreign AS DECIMAL.
DEF OUTPUT PARAMETER printed        AS CHAR.
DEF OUTPUT PARAMETER curr-user      AS CHAR.
DEF OUTPUT PARAMETER order-taker    AS INT.
DEF OUTPUT PARAMETER order-id       AS CHAR.
DEF OUTPUT PARAMETER found          AS LOGICAL INITIAL NO. 
DEF OUTPUT PARAMETER rechnr         AS INT.
DEF OUTPUT PARAMETER avail-queasy   AS LOGICAL INIT NO.
DEF OUTPUT PARAMETER fl-code        AS INT INIT 0 NO-UNDO.
DEF OUTPUT PARAMETER TABLE FOR t-h-bill.

DEFINE BUFFER bill-guest FOR vhp.guest. 

  FIND FIRST vhp.htparam WHERE htpara.paramnr = 867 NO-LOCK. 
  FIND FIRST bill-guest WHERE bill-guest.gastnr = vhp.htparam.finteger NO-LOCK 
    NO-ERROR. 
  IF AVAILABLE bill-guest THEN kreditlimit = bill-guest.kreditlimit. 
  FIND FIRST vhp.h-bill WHERE vhp.h-bill.departement = curr-dept
    AND vhp.h-bill.tischnr = tischnr AND vhp.h-bill.flag = 0 NO-LOCK NO-ERROR. 
  IF AVAILABLE vhp.h-bill THEN 
  DO:
    ASSIGN fl-code = 1.
    CREATE t-h-bill.
    BUFFER-COPY h-bill TO t-h-bill.
    ASSIGN t-h-bill.rec-id = RECID(h-bill).
    rechnr = vhp.h-bill.rechnr. 
    
      room = "". 
      gname = "". 
      IF vhp.h-bill.resnr GT 0 AND vhp.h-bill.reslinnr GT 0 THEN 
      DO:
        FIND FIRST vhp.res-line WHERE vhp.res-line.resnr = vhp.h-bill.resnr 
         AND vhp.res-line.reslinnr = vhp.h-bill.reslinnr NO-LOCK NO-ERROR. 
        IF  AVAILABLE vhp.res-line THEN 
        DO: 
          resrecid = RECID(res-line). 
          FIND FIRST vhp.guest WHERE vhp.guest.gastnr 
            = vhp.res-line.gastnrpay NO-LOCK. 
          IF vhp.guest.kreditlimit NE 0 THEN kreditlimit = vhp.guest.kreditlimit. 
          room = vhp.res-line.zinr. 
          curr-room = room. 
          rescomment = vhp.res-line.bemerk.
        END. 
      END. 
 
      gname = vhp.h-bill.bilname. 
      curr-gname = gname. 
 
    /* Malik Serverless 517 */
    IF balance NE ? AND kreditlimit NE  ? THEN
    DO:
      IF balance LE kreditlimit THEN bcol = 2. 
    END.
    /* IF balance LE kreditlimit THEN bcol = 2. */ 
    /* END Malik */
/*    ELSE bcol = 12. */ 
 
    balance = vhp.h-bill.saldo. 
    balance-foreign = vhp.h-bill.mwst[99]. 
    IF vhp.h-bill.rgdruck = 0 THEN printed = "". 
    ELSE printed = "*". 

    IF NOT curedept-flag THEN RUN check-kitchenprint. 
    curr-user = user-init + " " + user-name. 
    IF vhp.h-bill.betriebsnr NE 0 THEN 
    DO: 
      FIND FIRST vhp.queasy WHERE vhp.queasy.key = 10 
        AND vhp.queasy.number1 = vhp.h-bill.betriebsnr NO-LOCK NO-ERROR. 
      IF AVAILABLE vhp.queasy THEN 
      DO: 
        order-taker = vhp.queasy.number1. 
        order-id = vhp.queasy.char1. 
        curr-user = curr-user + " - " + order-id. 
      END. 
    END. 
  END. 
  ELSE DO:
    fl-code = 2.
    IF AVAILABLE vhp.res-line THEN release vhp.res-line. 
    IF AVAILABLE vhp.h-bill THEN release vhp.h-bill.
    resrecid = 0. 
    balance = 0. 
/* 
    room = "". 
    gname = "". 
    curr-room = "". 
    curr-gname = "". 
    rescomment = "". 
    persons = vhp.tisch.normalbeleg. 
    t-bezeich = vhp.tisch.bezeich. 
*/ 
    rechnr = 0. 
    printed = "". 
    bcol = 2. 
 
/* select order taker IF DEFINEd */ 
    curr-user = user-init + " " + user-name. 
    FIND FIRST vhp.queasy WHERE vhp.queasy.key = 10 NO-LOCK NO-ERROR.
    IF AVAILABLE vhp.queasy THEN avail-queasy = YES.
  END. 


PROCEDURE check-kitchenprint: 
  DEFINE BUFFER h-bline  FOR vhp.h-bill-line. 
  DEFINE BUFFER h-art    FOR vhp.h-artikel. 
  
  DEFINE VARIABLE use-it AS LOGICAL INITIAL NO. /* always as no longer used */

  IF NOT use-it OR curedept-flag THEN RETURN.
  IF AVAILABLE vhp.h-bill AND NOT from-acct THEN 
  DO: 
    found = NO. 
    FOR EACH h-bline WHERE h-bline.departement = vhp.h-bill.departement 
      AND h-bline.rechnr = vhp.h-bill.rechnr AND h-bline.steuercode GT 0
      AND h-bline.steuercode LT 9999
      AND found = NO NO-LOCK: 
      FIND FIRST h-art WHERE h-art.departement = h-bline.departement 
        AND h-art.artnr = h-bline.artnr AND h-art.bondruckernr[1] NE 0 
        AND h-art.artart = 0 NO-LOCK NO-ERROR. 
      IF AVAILABLE h-art THEN found = YES. 
    END. 
  END. 
END. 
