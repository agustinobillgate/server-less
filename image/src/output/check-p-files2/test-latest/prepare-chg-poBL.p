DEFINE TEMP-TABLE disc-list 
  FIELD l-recid     AS INTEGER 
  FIELD price0      AS DECIMAL FORMAT ">,>>>,>>>,>>9.999"   LABEL "Unit-Price" 
  FIELD brutto      AS DECIMAL FORMAT "->,>>>,>>>,>>9.999"  LABEL "Gross Amount" 
  FIELD disc        AS DECIMAL FORMAT ">9.99"               LABEL "Disc" 
  FIELD disc2       AS DECIMAL FORMAT ">9.99"               LABEL "Disc2" 
  FIELD vat         AS DECIMAL FORMAT ">9.99"               LABEL "VAT"
  FIELD disc-val    AS DECIMAL FORMAT ">,>>>,>>>,>>9.999"   LABEL "Disc Value" 
  FIELD disc2-val   AS DECIMAL FORMAT ">,>>>,>>>,>>9.999"   LABEL "Disc2 Value"
  FIELD vat-val     AS DECIMAL FORMAT ">,>>>,>>>,>>9.999"   LABEL "VAT-Value". 

DEFINE buffer l-art FOR l-artikel.
DEFINE TEMP-TABLE s-order LIKE l-order
    FIELD rec-id       AS INTEGER
    FIELD lief-einheit AS DECIMAL FORMAT ">>>,>>9.999". 
DEFINE TEMP-TABLE t-l-art LIKE l-artikel.
DEFINE TEMP-TABLE t-l-orderhdr LIKE l-orderhdr
    FIELD rec-id AS INT.
DEFINE TEMP-TABLE t-l-order LIKE l-order
    FIELD rec-id AS INT.
DEFINE TEMP-TABLE t-waehrung LIKE waehrung.
DEFINE TEMP-TABLE t-parameters
    FIELD varname AS CHARACTER FORMAT "x(20)"
    FIELD vstring AS CHARACTER FORMAT "x(64)".

DEF INPUT  PARAMETER pvILanguage    AS INTEGER  NO-UNDO.
DEF INPUT  PARAMETER docu-nr        AS CHAR.
DEF INPUT  PARAMETER lief-nr        AS INTEGER.
DEF OUTPUT PARAMETER local-nr       AS INTEGER.
DEF OUTPUT PARAMETER potype         AS INTEGER.
DEF OUTPUT PARAMETER enforce-rflag  AS LOGICAL.
DEF OUTPUT PARAMETER release-flag   AS LOGICAL.
DEF OUTPUT PARAMETER prev-flag      AS LOGICAL.
DEF OUTPUT PARAMETER pr             AS CHAR.
DEF OUTPUT PARAMETER crterm         AS INTEGER INIT 30.
DEF OUTPUT PARAMETER lieferdatum    AS DATE.
DEF OUTPUT PARAMETER bestellart     AS CHARACTER.
DEF OUTPUT PARAMETER comments       AS CHAR.
DEF OUTPUT PARAMETER supplier       AS CHAR.
DEF OUTPUT PARAMETER curr-liefnr    AS INTEGER.
DEF OUTPUT PARAMETER deptnr         AS INTEGER.
DEF OUTPUT PARAMETER ordername      AS CHARACTER.
DEF OUTPUT PARAMETER deptname       AS CHAR.
DEF OUTPUT PARAMETER billdate       AS DATE.
DEF OUTPUT PARAMETER t-amount       AS DECIMAL.
DEF OUTPUT PARAMETER msg-str        AS CHAR.
DEF OUTPUT PARAMETER p-1093         AS INT.
DEF OUTPUT PARAMETER p-464          AS INT.
DEF OUTPUT PARAMETER p-220          AS INT.
DEF OUTPUT PARAMETER p-266          AS DECIMAL.
DEF OUTPUT PARAMETER p-app          AS LOGICAL.
DEF OUTPUT PARAMETER TABLE FOR t-l-art.
DEF OUTPUT PARAMETER TABLE FOR s-order.
DEF OUTPUT PARAMETER TABLE FOR disc-list.
DEF OUTPUT PARAMETER TABLE FOR t-l-orderhdr.
DEF OUTPUT PARAMETER TABLE FOR t-waehrung.
DEF OUTPUT PARAMETER TABLE FOR t-l-order.
DEF OUTPUT PARAMETER TABLE FOR t-parameters.

{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "chg-po".

RUN htpint.p (266, OUTPUT p-266).

FIND FIRST htparam WHERE htparam.paramnr = 71 NO-LOCK.
p-app = htparam.flogical.

FIND FIRST htparam WHERE htparam.paramnr = 152 NO-LOCK. 
FIND FIRST waehrung WHERE waehrung.wabkurz = htparam.fchar NO-LOCK NO-ERROR. 
IF NOT AVAILABLE waehrung THEN 
DO: 
  msg-str = msg-str + CHR(2)
          + translateExtended ("Local Currency Code incorrect! (Param 152 / Grp 7)",lvCAREA,"").
  RETURN. 
END. 
local-nr = waehrung.waehrungsnr.

FIND FIRST l-lieferant WHERE l-lieferant.lief-nr = lief-nr NO-LOCK. 
FIND FIRST l-orderhdr WHERE l-orderhdr.docu-nr = docu-nr EXCLUSIVE-LOCK. 
IF l-orderhdr.betriebsnr = 1 THEN potype = 2. 

CREATE t-l-orderhdr.
BUFFER-COPY l-orderhdr TO t-l-orderhdr.
ASSIGN t-l-orderhdr.rec-id = RECID(l-orderhdr).
 
FIND FIRST htparam WHERE paramnr = 222 NO-LOCK. 
enforce-rflag = flogical. 
 
release-flag = (l-orderhdr.gedruckt NE ?). 
prev-flag = release-flag. 

FIND FIRST l-order WHERE l-order.docu-nr = docu-nr 
  AND l-order.lief-nr = lief-nr AND l-order.pos = 0 NO-LOCK. 
ASSIGN
  pr            = l-order.lief-fax[1]
  crterm        = l-orderhdr.angebot-lief[2]
  lieferdatum   = l-orderhdr.lieferdatum 
  bestellart    = l-orderhdr.bestellart
  comments      = l-orderhdr.lief-fax[3] 
  supplier      = l-lieferant.firma + " - " + l-lieferant.wohnort
  curr-liefnr   = lief-nr
  deptnr        = l-orderhdr.angebot-lief[1]
  ordername     = l-orderhdr.lief-fax[2]
.

CREATE t-l-order.
BUFFER-COPY l-order TO t-l-order.
ASSIGN t-l-order.rec-id = RECID(l-order).

IF deptnr GT 0 THEN 
DO: 
  FIND FIRST parameters WHERE parameters.progname = "CostCenter" 
    AND parameters.SECTION = "Name" 
    AND parameters.varname EQ STRING(deptnr) NO-LOCK. 
  deptname = parameters.vstring.
END.

FIND FIRST htparam WHERE paramnr = 975 NO-LOCK. 
IF htparam.finteger NE 1 AND htparam.finteger NE 2 THEN 
DO: 
  FIND FIRST htparam WHERE paramnr = 110 NO-LOCK. 
  billdate = htparam.fdate. 
END. 
ELSE billdate = today.

RUN cal-tamount.
FOR EACH s-order:
    FIND FIRST l-art WHERE l-art.artnr = s-order.artnr NO-LOCK NO-ERROR.
    IF AVAILABLE l-art THEN
    DO:
        CREATE t-l-art.
        BUFFER-COPY l-art TO t-l-art.
    END.
END.

FOR EACH waehrung:
    CREATE t-waehrung.
    BUFFER-COPY waehrung TO t-waehrung.
END.
/*MTRUN disp-q1.
RUN currency-list.*/


FOR EACH parameters WHERE parameters.progname = "CostCenter" 
    AND parameters.section = "Name" :
    CREATE t-parameters.
    ASSIGN
    t-parameters.varname = parameters.varname
    t-parameters.vstring = parameters.vstring.
END.
RUN htpint.p (1093, OUTPUT p-1093).
RUN htpint.p (464, OUTPUT p-464).
RUN htpint.p (220, OUTPUT p-220).

PROCEDURE cal-tamount: 
  t-amount = 0. 
  FOR EACH l-order WHERE l-order.docu-nr = docu-nr AND 
    l-order.pos GT 0 AND l-order.loeschflag = 0 NO-LOCK, 
    FIRST l-art WHERE l-art.artnr = l-order.artnr NO-LOCK: 
    t-amount = t-amount + l-order.warenwert. 
    create s-order. 
    ASSIGN 
      s-order.docu-nr = l-order.docu-nr 
      s-order.betriebsnr = RECID(l-order) 
      s-order.lief-fax[3] = l-order.lief-fax[3] 
      s-order.artnr = l-order.artnr 
      s-order.geliefert = l-order.geliefert 
      s-order.txtnr = l-order.txt 
      s-order.anzahl = l-order.anzahl 
      s-order.flag = l-order.flag 
      s-order.quality = l-order.quality 
      s-order.besteller = l-order.besteller
      s-order.einzelpreis = l-order.einzelpreis 
      s-order.warenwert = l-order.warenwert 
      s-order.stornogrund = l-order.stornogrund 
      s-order.pos = l-order.pos
      s-order.rec-id = RECID(l-order).

    FIND FIRST l-artikel WHERE l-artikel.artnr = l-order.artnr NO-LOCK.
    ASSIGN s-order.lief-einheit = l-artikel.lief-einheit.

    create disc-list. 
    ASSIGN 
      disc-list.l-recid = s-order.rec-id
      disc-list.disc = INTEGER(SUBSTR(s-order.quality,1,2)) 
        + INTEGER(SUBSTR(s-order.quality,4,2)) * 0.01 
      disc-list.vat = INTEGER(SUBSTR(s-order.quality,7,2)) 
        + INTEGER(SUBSTR(s-order.quality,10,2)) * 0.01 
      disc-list.disc2 = INTEGER(SUBSTR(s-order.quality,13,2)) 
        + INTEGER(SUBSTR(s-order.quality,16,2)) * 0.01 
      /*disc-list.price0 = s-order.einzelpreis / (1 - disc-list.disc * 0.01) 
        / (1 - disc-list.disc2 * 0.01) / (1 + disc-list.vat * 0.01) 
      disc-list.brutto = disc-list.price0 * s-order.anzahl*/
      disc-list.disc-val = INTEGER(SUBSTR(s-order.quality,19,18))
      disc-list.disc2-val = INTEGER(SUBSTR(s-order.quality,37,18))
      disc-list.vat-val = INTEGER(SUBSTR(s-order.quality,55)). 
      
      disc-list.brutto = (s-order.warenwert + disc-list.disc-val + disc-list.disc2-val) - disc-list.vat-val.
      disc-list.price0 = disc-list.brutto / s-order.anzahl.
  END. 
END. 

/*MT
PROCEDURE currency-list: 
  IF l-orderhdr.angebot-lief[3] = 0 THEN 
    l-orderhdr.angebot-lief[3] = local-nr. 
  FIND FIRST waehrung WHERE waehrung.waehrungsnr = 
    l-orderhdr.angebot-lief[3] NO-LOCK. 
  currency:add-first(waehrung.wabkurz) IN FRAME frame1. 
  ASSIGN currency:screen-value = waehrung.wabkurz. 
  IF l-orderhdr.angebot-lief[3] NE local-nr THEN 
  DO: 
    FIND FIRST waehrung WHERE waehrung.waehrungsnr = local-nr NO-LOCK. 
    IF waehrung.betriebsnr = 0 THEN 
      currency:add-last(waehrung.wabkurz) IN FRAME frame1. 
  END. 
  FOR EACH waehrung WHERE waehrung.waehrungsnr NE l-orderhdr.angebot-lief[3] 
    AND waehrung.ankauf GT 0 AND waehrung.betriebsnr NE 0 NO-LOCK 
    BY waehrung.wabkurz: 
    currency:add-last(waehrung.wabkurz) IN FRAME frame1. 
  END. 
END. 
*/
