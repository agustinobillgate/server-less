
/*040719 tidak ada perubahan hanya untuk pengecekakn*/

DEFINE TEMP-TABLE ar-list
    FIELD arRecid AS INTEGER.

DEFINE TEMP-TABLE age-list 
  FIELD nr              AS INTEGER 
  FIELD paint-it        AS LOGICAL INITIAL NO 
  FIELD rechnr          AS INTEGER FORMAT ">>>>>>>>9" 
  FIELD refno           AS INTEGER FORMAT ">>>>>>>>>" 
  FIELD rechnr2         AS INTEGER FORMAT ">>>>>>>>>"
  FIELD opart           AS INTEGER 
  FIELD zahlkonto       AS INTEGER
  FIELD counter         AS INTEGER
  FIELD gastnr          AS INTEGER 
  FIELD company         AS CHAR
  FIELD billname        AS CHAR FORMAT "x(36)" 
  FIELD gastnrmember    AS INTEGER 
  FIELD zinr            LIKE zimmer.zinr		/*MT 25/07/12 */
  FIELD datum           AS DATE
  FIELD rgdatum         AS DATE 
  FIELD paydatum        AS DATE 
  FIELD user-init       AS CHAR FORMAT "x(2)" 
  FIELD bezeich         AS CHARACTER FORMAT "x(16)" 
  FIELD wabkurz         AS CHAR FORMAT "x(4)" 
  FIELD debt            AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99" INITIAL 0 
  FIELD credit          AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99" INITIAL 0 
  FIELD fdebt           AS DECIMAL LABEL "Foreign-Amt" 
                           FORMAT "->>>,>>>,>>>,>>9.99" INITIAL 0 
  FIELD t-debt          AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99" INITIAL 0   /*MT 20/07/12 */
  FIELD tot-debt        AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99" INITIAL 0   /*MT 20/07/12 */
  FIELD rid             AS INTEGER INITIAL 0
  FIELD dept            AS INTEGER INITIAL 0
  FIELD gname           AS CHAR    FORMAT "x(36)"
  FIELD voucher         AS CHAR    FORMAT "x(12)"
  FIELD ankunft         AS DATE    FORMAT "99/99/99"
  FIELD abreise         AS DATE    FORMAT "99/99/99"
  FIELD stay            AS INTEGER FORMAT ">>9"
  FIELD remarks         AS CHAR    FORMAT "x(50)" /*MT 130812 */
  FIELD ttl             AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99" INITIAL 0   /*MT 20/07/12 */

  FIELD resname         AS CHAR
  FIELD comp-name       AS CHAR
  FIELD comp-add        AS CHAR
  FIELD comp-fax        AS CHAR
  FIELD comp-phone      AS CHAR
  INDEX idx1 rechnr dept gastnr
    . 

DEFINE TEMP-TABLE t-age-list LIKE age-list.

DEF INPUT  PARAMETER incl       AS LOGICAL.
DEF INPUT  PARAMETER t-artnr    AS INT.
DEF INPUT  PARAMETER t-dept     AS INT.
DEF INPUT  PARAMETER from-name  AS CHAR.
DEF INPUT  PARAMETER to-name    AS CHAR.
DEF INPUT  PARAMETER fr-date    AS DATE.
DEF INPUT  PARAMETER to-date    AS DATE.
DEF INPUT  PARAMETER Bdate      AS DATE.
DEF INPUT  PARAMETER gastnr     AS INT.
DEF OUTPUT PARAMETER tot-debt   AS DECIMAL.
DEF OUTPUT PARAMETER tot-paid   AS DECIMAL.
DEF OUTPUT PARAMETER TABLE FOR t-age-list.

DEFINE VARIABLE curr-rechnr   AS INTEGER.
DEFINE VARIABLE opart         AS INTEGER INITIAL 0. 
DEFINE VARIABLE opart1        AS INTEGER INITIAL 1. 
DEFINE VARIABLE opart2        AS INTEGER INITIAL 1. 
DEFINE VARIABLE rechnr        AS INTEGER. 
DEFINE VARIABLE nr            AS INTEGER. 
DEFINE VARIABLE curr-saldo    AS DECIMAL. 


DEFINE VARIABLE ankunft       AS DATE.
DEFINE VARIABLE abreise       AS DATE.
DEFINE VARIABLE voucherno     AS CHAR.
DEFINE VARIABLE gname         AS CHAR.
DEFINE VARIABLE do-it         AS LOGICAL.

DEF VAR t-resnr AS INT.   /*MT 130812 */
DEF VAR t-name AS CHAR.   /*MT 130812 */

DEFINE BUFFER guest1    FOR guest.
DEFINE BUFFER artikel1  FOR artikel. 
DEFINE BUFFER debt      FOR debitor.
DEFINE BUFFER gast      FOR guest. 


FOR EACH age-list: 
  DELETE age-list. 
END.
FOR EACH ar-list: 
  DELETE ar-list. 
END.

curr-rechnr = 0. 
IF incl THEN 
ASSIGN opart2 = 2.
ELSE ASSIGN opart2 = 0.

ASSIGN
    tot-debt = 0
    tot-paid = 0
    nr = 0.

FIND FIRST artikel WHERE artikel.artnr = t-artnr 
    AND artikel.departement = t-dept NO-LOCK.
FOR EACH debitor WHERE debitor.artnr = artikel.artnr 
  /*AND debitor.name GE from-name AND debitor.name LE to-name*/
  AND debitor.gastnr = gastnr
  AND debitor.opart GE opart AND debitor.opart LE opart2
  AND debitor.rgdatum GE fr-date 
  AND debitor.rgdatum LE to-date AND debitor.zahlkonto = 0 NO-LOCK, 
  FIRST gast WHERE gast.gastnr = debitor.gastnr NO-LOCK 
  BY gast.NAME BY debitor.gastnr BY debitor.debref 
  BY debitor.rgdatum BY debitor.rechnr:   

   ASSIGN do-it = YES.

   IF debitor.opart = 2 AND bDate NE ? AND debitor.rgdatum LT bDate THEN
   DO:
      FIND FIRST debt WHERE debt.rechnr = debitor.rechnr 
        AND debt.counter = debitor.counter 
        AND debt.artnr = debitor.artnr 
        AND debt.zahlkonto GT 0 
        AND debt.rgdatum GE bDate NO-LOCK NO-ERROR.
      do-it = AVAILABLE debt.
   END.
   
   IF do-it THEN DO:
      gname = "".
      ankunft = ?.
      abreise = ?.
    
      
      IF debitor.betriebsnr = 0 THEN
      DO:
        IF debitor.rechnr NE 0 THEN
        DO:
            FIND FIRST bill WHERE bill.rechnr = debitor.rechnr NO-LOCK NO-ERROR.
            IF AVAILABLE bill THEN
            DO:
               FIND FIRST reservation WHERE reservation.resnr = bill.resnr NO-LOCK 
                NO-ERROR.
               IF AVAILABLE reservation THEN
               DO:
                 ASSIGN voucherno = reservation.vesrdepot.
               END.

               FIND FIRST res-line WHERE res-line.resnr = bill.resnr
                   AND res-line.reslinnr = bill.parent-nr AND res-line.zipreis GT 0 NO-LOCK NO-ERROR.
               IF AVAILABLE res-line THEN DO:
                   ASSIGN
                       gname   = res-line.NAME
                       ankunft = res-line.ankunft
                       abreise = res-line.abreise.
               END.   
            END. 
        END.
        ELSE
        DO: 
            /*MT 130812 */
            IF debitor.vesrcod MATCHES "*resno:*" THEN
            DO:
                IF NUM-ENTRIES(debitor.vesrcod, ";") = 1 THEN
                t-resnr = INT(SUBSTR(debitor.vesrcod, 26, LENGTH(debitor.vesrcod) - 1)).
                ELSE
                    ASSIGN
                        t-name = TRIM(ENTRY(1, debitor.vesrcod, ";"))
                        t-resnr = INT(SUBSTR(t-name, 26, LENGTH(t-name) - 1)).
                    
                FIND FIRST reservation WHERE reservation.resnr = t-resnr NO-LOCK 
                    NO-ERROR.
                IF AVAILABLE reservation THEN
                DO:
                  ASSIGN voucherno = reservation.vesrdepot.
                END.

                FIND FIRST res-line WHERE res-line.resnr = t-resnr NO-LOCK NO-ERROR.
                IF AVAILABLE res-line THEN
                DO:
                    FIND FIRST guest WHERE guest.gastnr = res-line.gastnrmember.
                    gname = guest.name + ", " + guest.vorname1 + guest.anredefirma 
                          + " " + guest.anrede1 .
                END.
            END.
        END.
      END.
      ELSE
      DO:
        FIND FIRST h-bill WHERE h-bill.rechnr = debitor.rechnr
          AND h-bill.departement = debitor.betriebsnr NO-LOCK NO-ERROR.
        IF AVAILABLE h-bill AND h-bill.bilname NE "" 
            THEN gname = h-bill.bilname.
        ELSE IF debitor.NAME NE "" THEN gname = debitor.NAME.
      END.
      
      nr = nr + 1.
      CREATE age-list. 
      ASSIGN 
        age-list.nr           = nr 
        age-list.rechnr       = debitor.rechnr 
        age-list.refno        = debitor.debref 
        age-list.opart        = debitor.opart 
        age-list.counter      = debitor.counter
        age-list.gastnr       = debitor.gastnr 
        age-list.gastnrmember = debitor.gastnrmember 
        age-list.zinr         = debitor.zinr 
        age-list.tot-debt     = debitor.saldo
        age-list.dept         = debitor.betriebsnr
        age-list.rid          = RECID(debitor)
        age-list.gname        = gname
        age-list.ankunft      = ankunft
        age-list.abreise      = abreise
        age-list.ttl          = debitor.vesrdep
        age-list.stay         = abreise - ankunft
        age-list.voucher      = voucherno 
        age-list.remarks      = debitor.vesrcod
        age-list.company      = gast.name + ", " + gast.vorname1 
                              + gast.anredefirma + " " + gast.anrede1
        age-list.billname     = age-list.company
        age-list.datum        = debitor.rgdatum
        age-list.rgdatum      = debitor.rgdatum
        age-list.debt         = debitor.saldo
        age-list.fdebt        = debitor.vesrdep 
      .
    
      IF AVAILABLE bill THEN ASSIGN age-list.rechnr2 = bill.rechnr2.
    
      IF debitor.betrieb-gastmem NE 0 THEN 
      DO: 
        FIND FIRST waehrung WHERE waehrung.waehrungsnr = debitor.betrieb-gastmem 
          NO-LOCK NO-ERROR. 
        IF AVAILABLE waehrung THEN age-list.wabkurz = waehrung.wabkurz. 
      END. 
    
      FIND FIRST bediener WHERE bediener.nr = debitor.bediener-nr 
        NO-LOCK NO-ERROR. 
      IF AVAILABLE bediener THEN age-list.user-init = bediener.userinit. 
    
      curr-saldo = debitor.saldo. 
      tot-debt = tot-debt + debitor.saldo.   
    
      
      IF debitor.counter GT 0 THEN 
      FOR EACH debt WHERE debt.rechnr = debitor.rechnr 
        AND debt.counter = debitor.counter 
        AND debt.artnr = debitor.artnr 
        AND debt.zahlkonto GT 0 
        AND debt.rgdatum LE to-date NO-LOCK BY debt.rgdatum: 
        nr = nr + 1. 
    
        CREATE age-list.
        ASSIGN
          age-list.nr           = nr
          age-list.rechnr       = debt.rechnr 
          age-list.opart        = debt.opart 
          age-list.counter      = debt.counter
          age-list.zahlkonto    = debt.zahlkonto
          age-list.gastnr       = debt.gastnr 
          age-list.gastnrmember = debt.gastnrmember
          age-list.datum        = debitor.rgdatum
          age-list.rgdatum      = debt.rgdatum
          age-list.paydatum     = debt.rgdatum
          age-list.credit       = - debt.saldo 
          age-list.dept         = debitor.betriebsnr
          age-list.fdebt        = - debt.vesrdep
          age-list.rid          = RECID(debitor)
          age-list.company      = gast.name + ", " + gast.vorname1 
                                + gast.anredefirma + " " + gast.anrede1
        .
    
        tot-paid = tot-paid - debt.saldo. 
        FIND FIRST artikel1 WHERE artikel1.artnr = debt.zahlkonto 
          AND artikel1.departement = 0 NO-LOCK NO-ERROR. 
        IF AVAILABLE artikel1 THEN age-list.bezeich = artikel1.bezeich. 
        FIND FIRST bediener WHERE bediener.nr = debt.bediener-nr 
          NO-LOCK NO-ERROR. 
        IF AVAILABLE bediener THEN age-list.user-init = bediener.userinit. 
        curr-saldo = curr-saldo + debt.saldo. 
        age-list.tot-debt = curr-saldo. 
    
        IF debt.betrieb-gastmem NE 0 THEN 
        DO: 
          FIND FIRST waehrung WHERE waehrung.waehrungsnr 
            = debt.betrieb-gastmem NO-LOCK NO-ERROR. 
          IF AVAILABLE waehrung THEN age-list.wabkurz = waehrung.wabkurz. 
        END. 
      END.
   END. 
END. /* for each */

FOR EACH age-list,
    FIRST guest1 WHERE guest1.gastnr = age-list.gastnrmember NO-LOCK 
      BY age-list.company BY age-list.datum BY age-list.counter 
      BY age-list.billname DESCENDING:
    FIND FIRST guest WHERE guest.gastnr = age-list.gastnr NO-LOCK.

    CREATE t-age-list.
    BUFFER-COPY age-list TO t-age-list.
    t-age-list.resname = guest.name + ", " + guest.vorname1 + guest.anredefirma 
            + " " + guest.anrede1 
            + chr(10) + guest.adresse1 
            + chr(10) + guest.wohnort + " " + guest.plz 
            + chr(10) + guest.land. 
    t-age-list.comp-name = guest.name + ", " + guest.vorname1 + guest.anredefirma 
            + " " + guest.anrede1 .
    t-age-list.comp-add = guest.adresse1 + " " + guest.wohnort + " " + guest.plz
        + " " + guest.land.
    t-age-list.comp-fax = guest.fax.
    t-age-list.comp-phone = guest.telefon.
END.



