DEF TEMP-TABLE t-reservation LIKE reservation.
DEF TEMP-TABLE t-master      LIKE master.

DEF TEMP-TABLE f-mainres
    FIELD groupname         AS CHAR
    FIELD comments          AS CHAR
    FIELD voucherno         AS CHAR
    FIELD contact           AS CHAR
    FIELD origin            AS CHAR
    FIELD ta-comm           AS CHAR
    FIELD segmstr           AS CHAR
    FIELD resart-str        AS CHAR
    FIELD letter-str        AS CHAR
    FIELD bill-receiver     AS CHAR

    FIELD fixrate-flag      AS LOGICAL
    FIELD fixed-rate        AS LOGICAL
    FIELD invno-flag        AS LOGICAL
    FIELD double-currency   AS LOGICAL
    FIELD deposit-readonly  AS LOGICAL
    FIELD deposit-disabled  AS LOGICAL
    FIELD master-exist      AS LOGICAL
    FIELD umsatz1           AS LOGICAL
    FIELD umsatz3           AS LOGICAL
    FIELD umsatz4           AS LOGICAL

    FIELD karteityp         AS INTEGER
    FIELD gastnrherk        AS INTEGER
    FIELD gastnrcom         AS INTEGER
    FIELD gastnrpay         AS INTEGER
    FIELD l-grpnr           AS INTEGER
    FIELD resart            AS INTEGER
    FIELD letterno          AS INTEGER
    FIELD contact-nr        AS INTEGER
    FIELD curr-segm         AS INTEGER

    FIELD ci-date           AS DATE
    FIELD limitdate         AS DATE INIT ?
    FIELD cutoff-date       AS DATE INIT ?
    FIELD res-ankunft       AS DATE INIT ?

    FIELD depositgef        AS DECIMAL
    FIELD depositres        AS DECIMAL
.

DEF INPUT PARAMETER gastnr      AS INTEGER  NO-UNDO.
DEF INPUT PARAMETER resnr       AS INTEGER  NO-UNDO.
DEF INPUT PARAMETER res-mode    AS CHAR     NO-UNDO.
DEF INPUT PARAMETER user-init   AS CHAR     NO-UNDO.
DEF INPUT PARAMETER grpflag     AS LOGICAL  NO-UNDO.

DEF OUTPUT PARAMETER record-use AS LOGICAL INIT NO.
DEF OUTPUT PARAMETER init-time AS INT.
DEF OUTPUT PARAMETER init-date AS DATE.
DEF OUTPUT PARAMETER bill-receiver AS CHAR  NO-UNDO INIT "".
DEF OUTPUT PARAMETER TABLE FOR f-mainres.
DEF OUTPUT PARAMETER TABLE FOR t-reservation.
DEF OUTPUT PARAMETER TABLE FOR t-master.

DEF VAR flag-ok AS LOGICAL.
RUN check-timebl.p(1, resnr, ?, "reservation", ?, ?, OUTPUT flag-ok,
                   OUTPUT init-time, OUTPUT init-date).
IF NOT flag-ok THEN
DO:
    record-use = YES.
    RETURN NO-APPLY.
END.
CREATE f-mainres.

/* group 7: fixed exchange rate during whole stay --> YES */ 
FIND FIRST htparam WHERE htparam.paramnr = 264 NO-LOCK. 
f-mainres.fixrate-flag = htparam.flogical. 
 
FIND FIRST htparam WHERE paramnr = 87 NO-LOCK. 
f-mainres.ci-date = htparam.fdate. 
 
FIND FIRST htparam WHERE paramnr = 391 NO-LOCK. 
f-mainres.invno-flag = htparam.flogical. 
 
FIND FIRST htparam WHERE paramnr = 440 NO-LOCK. 
f-mainres.l-grpnr = htparam.finteger. 
 
FIND FIRST htparam WHERE paramnr = 240 NO-LOCK. 
f-mainres.double-currency = htparam.flogical. 
 
FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK. 
FIND FIRST guest WHERE guest.gastnr = gastnr NO-LOCK. 

/* Malik Serverless 696 Comment 
FIND FIRST reservation WHERE reservation.resnr = resnr EXCLUSIVE-LOCK.  
IF res-mode EQ "New" THEN reservation.insurance = f-mainres.fixrate-flag. 
IF f-mainres.fixrate-flag THEN f-mainres.fixed-rate = f-mainres.fixrate-flag. 
ELSE f-mainres.fixed-rate = reservation.insurance. 
 
IF res-mode = "new" THEN 
DO: 
  FIND FIRST guestseg WHERE guestseg.gastnr = guest.gastnr 
    AND guestseg.reihenfolge = 1 NO-LOCK NO-ERROR. 
  IF AVAILABLE guestseg THEN reservation.segmentcode = guestseg.segmentcode. 
  ASSIGN 
    reservation.gastnr          = guest.gastnr 
    reservation.gastnrherk      = guest.gastnr 
    reservation.useridanlage    = user-init 
    reservation.name            = guest.name + ", " 
       + guest.vorname1 + guest.anredefirma 
    reservation.grpflag         = grpflag 
    reservation.resart          = 1 
    reservation.resdat          = f-mainres.ci-date
  . 
END.

FIND FIRST res-line WHERE res-line.resnr = reservation.resnr 
  AND res-line.resstatus NE 9 AND res-line.resstatus NE 10 NO-LOCK NO-ERROR. 
IF AVAILABLE res-line THEN 
ASSIGN
  f-mainres.cutoff-date = res-line.ankunft - reservation.point-resnr
  f-mainres.res-ankunft = res-line.ankunft
.  
  
ASSIGN
  f-mainres.groupname   = reservation.groupname
  f-mainres.resart      = reservation.resart
  f-mainres.limitdate   = reservation.limitdate 
  f-mainres.depositgef  = reservation.depositgef 
  f-mainres.gastnrherk  = reservation.gastnrherk 
  f-mainres.gastnrcom   = reservation.guestnrcom[1] 
  f-mainres.comments    = reservation.bemerk 
  f-mainres.letterno    = reservation.briefnr 
  f-mainres.voucherno   = reservation.vesrdepot
. 

FIND FIRST guest WHERE guest.gastnr = reservation.gastnrherk NO-LOCK NO-ERROR. 
IF NOT AVAILABLE guest THEN 
DO: 
  f-mainres.gastnrherk = reservation.gastnr. 
  FIND FIRST guest WHERE guest.gastnr = f-mainres.gastnrherk NO-LOCK. 
END. 
ASSIGN 
  f-mainres.origin    = guest.name + ", " + guest.vorname1 
                      + guest.anredefirma
  f-mainres.karteityp = guest.karteityp
.
 
IF reservation.kontakt-nr NE 0 THEN 
DO: 
  FIND FIRST akt-kont WHERE akt-kont.gastnr = reservation.gastnr 
      AND akt-kont.kontakt-nr = reservation.kontakt-nr NO-LOCK NO-ERROR. 
  IF AVAILABLE akt-kont THEN 
  ASSIGN 
    f-mainres.contact    = akt-kont.NAME + ", " + akt-kont.vorname
    f-mainres.contact-nr = akt-kont.kontakt-nr
  . 
END. 
 
IF reservation.guestnrcom[1] > 0 THEN 
DO: 
  FIND FIRST guest WHERE guest.gastnr = reservation.guestnrcom[1] NO-LOCK. 
  ASSIGN f-mainres.ta-comm = guest.name + ", " + guest.vorname1 
    + guest.anredefirma. 
END. 

FIND FIRST guest WHERE guest.gastnr = gastnr NO-LOCK. 
FIND FIRST segment WHERE segment.segmentcode = reservation.segmentcode 
  NO-LOCK NO-ERROR. 
IF AVAILABLE segment THEN 
ASSIGN 
  f-mainres.curr-segm = segment.segmentcode
  f-mainres.segmstr   = ENTRY(1, segment.bezeich, "$$0")
. 
 
ASSIGN f-mainres.depositres = reservation.depositgef 
  - reservation.depositbez - reservation.depositbez2. 
 
FIND FIRST sourccod WHERE sourccod.source-code = f-mainres.resart 
  NO-LOCK NO-ERROR. 
IF AVAILABLE sourccod THEN f-mainres.resart-str = sourccod.bezeich. 

FIND FIRST brief WHERE brief.briefkateg = f-mainres.l-grpnr 
  AND brief.briefnr = f-mainres.letterno NO-LOCK NO-ERROR. 
IF AVAILABLE brief THEN f-mainres.letter-str = brief.briefbezeich. 

FIND FIRST res-line WHERE res-line.resnr = reservation.resnr 
  AND (res-line.resstatus = 6 OR res-line.resstatus = 8 
       OR res-line.resstatus = 3) NO-LOCK NO-ERROR. 
IF AVAILABLE res-line THEN
DO:
    f-mainres.deposit-readonly = YES.
    f-mainres.deposit-disabled = YES.
END.
ELSE IF reservation.depositgef GT 0 AND f-mainres.depositres = 0 THEN /* Malik Serverless 471 : depositres -> f-mainres.depositres */
DO:
    f-mainres.deposit-disabled = YES.
END.
/*MT 24/06/15
ASSIGN
  f-mainres.deposit-readonly = AVAILABLE res-line
  f-mainres.deposit-disabled = reservation.depositgef GT 0 
    AND f-mainres.depositres = 0
.
*/

FIND FIRST master WHERE master.resnr = reservation.resnr NO-LOCK NO-ERROR. 
IF AVAILABLE master THEN 
DO: 
  FIND FIRST guest WHERE guest.gastnr = master.gastnrpay NO-LOCK. 
  ASSIGN
    f-mainres.master-exist      = YES
    f-mainres.gastnrpay         = master.gastnrpay
    f-mainres.umsatz1           = master.umsatzart[1]
    f-mainres.umsatz3           = master.umsatzart[3] 
    f-mainres.umsatz4           = master.umsatzart[4] 
    f-mainres.bill-receiver     = guest.name + ", " + guest.vorname1 
      + " " + guest.anrede1 + guest.anredefirma
  .
END. 

CREATE t-reservation.
BUFFER-COPY reservation TO t-reservation.

FIND FIRST master WHERE master.resnr = resnr NO-LOCK NO-ERROR.
IF AVAILABLE master THEN
DO:
  CREATE t-master.
  BUFFER-COPY master TO t-master.
  FIND FIRST guest WHERE guest.gastnr = master.gastnrpay NO-LOCK. 
  bill-receiver = guest.name + ", " + guest.vorname1 + " " + guest.anrede1 
    + guest.anredefirma. 
END. */

/* Malik Serverless 696 fix exclusive lock */
FIND FIRST reservation WHERE reservation.resnr = resnr NO-LOCK NO-ERROR.   
IF AVAILABLE reservation THEN
DO:
  FIND CURRENT reservation EXCLUSIVE-LOCK.
  IF res-mode EQ "New" THEN reservation.insurance = f-mainres.fixrate-flag. 
  IF f-mainres.fixrate-flag THEN f-mainres.fixed-rate = f-mainres.fixrate-flag. 
  ELSE f-mainres.fixed-rate = reservation.insurance. 
  
  IF res-mode = "new" THEN 
  DO: 
    FIND FIRST guestseg WHERE guestseg.gastnr = guest.gastnr 
      AND guestseg.reihenfolge = 1 NO-LOCK NO-ERROR. 
    IF AVAILABLE guestseg THEN reservation.segmentcode = guestseg.segmentcode. 
    ASSIGN 
      reservation.gastnr          = guest.gastnr 
      reservation.gastnrherk      = guest.gastnr 
      reservation.useridanlage    = user-init 
      reservation.name            = guest.name + ", " 
        + guest.vorname1 + guest.anredefirma 
      reservation.grpflag         = grpflag 
      reservation.resart          = 1 
      reservation.resdat          = f-mainres.ci-date
    . 
  END.
  FIND CURRENT reservation NO-LOCK. 

  FIND FIRST res-line WHERE res-line.resnr = reservation.resnr 
    AND res-line.resstatus NE 9 AND res-line.resstatus NE 10 NO-LOCK NO-ERROR. 
  IF AVAILABLE res-line THEN 
  ASSIGN
    f-mainres.cutoff-date = res-line.ankunft - reservation.point-resnr
    f-mainres.res-ankunft = res-line.ankunft
  .  
    
  ASSIGN
    f-mainres.groupname   = reservation.groupname
    f-mainres.resart      = reservation.resart
    f-mainres.limitdate   = reservation.limitdate 
    f-mainres.depositgef  = reservation.depositgef 
    f-mainres.gastnrherk  = reservation.gastnrherk 
    f-mainres.gastnrcom   = reservation.guestnrcom[1] 
    f-mainres.comments    = reservation.bemerk 
    f-mainres.letterno    = reservation.briefnr 
    f-mainres.voucherno   = reservation.vesrdepot
  .
  

  FIND FIRST guest WHERE guest.gastnr = reservation.gastnrherk NO-LOCK NO-ERROR. 
  IF NOT AVAILABLE guest THEN 
  DO: 
    f-mainres.gastnrherk = reservation.gastnr. 
    FIND FIRST guest WHERE guest.gastnr = f-mainres.gastnrherk NO-LOCK. 
  END. 
  ASSIGN 
    f-mainres.origin    = guest.name + ", " + guest.vorname1 
                        + guest.anredefirma
    f-mainres.karteityp = guest.karteityp
  .
  
  IF reservation.kontakt-nr NE 0 THEN 
  DO: 
    FIND FIRST akt-kont WHERE akt-kont.gastnr = reservation.gastnr 
        AND akt-kont.kontakt-nr = reservation.kontakt-nr NO-LOCK NO-ERROR. 
    IF AVAILABLE akt-kont THEN 
    ASSIGN 
      f-mainres.contact    = akt-kont.NAME + ", " + akt-kont.vorname
      f-mainres.contact-nr = akt-kont.kontakt-nr
    . 
  END. 
  
  IF reservation.guestnrcom[1] > 0 THEN 
  DO: 
    FIND FIRST guest WHERE guest.gastnr = reservation.guestnrcom[1] NO-LOCK. 
    ASSIGN f-mainres.ta-comm = guest.name + ", " + guest.vorname1 
      + guest.anredefirma. 
  END. 

  FIND FIRST guest WHERE guest.gastnr = gastnr NO-LOCK. 
  FIND FIRST segment WHERE segment.segmentcode = reservation.segmentcode 
    NO-LOCK NO-ERROR. 
  IF AVAILABLE segment THEN 
  ASSIGN 
    f-mainres.curr-segm = segment.segmentcode
    f-mainres.segmstr   = ENTRY(1, segment.bezeich, "$$0")
  . 
  
  ASSIGN f-mainres.depositres = reservation.depositgef 
    - reservation.depositbez - reservation.depositbez2. 
  
  FIND FIRST sourccod WHERE sourccod.source-code = f-mainres.resart 
    NO-LOCK NO-ERROR. 
  IF AVAILABLE sourccod THEN f-mainres.resart-str = sourccod.bezeich. 

  FIND FIRST brief WHERE brief.briefkateg = f-mainres.l-grpnr 
    AND brief.briefnr = f-mainres.letterno NO-LOCK NO-ERROR. 
  IF AVAILABLE brief THEN f-mainres.letter-str = brief.briefbezeich. 

  FIND FIRST res-line WHERE res-line.resnr = reservation.resnr 
    AND (res-line.resstatus = 6 OR res-line.resstatus = 8 
        OR res-line.resstatus = 3) NO-LOCK NO-ERROR. 
  IF AVAILABLE res-line THEN
  DO:
      f-mainres.deposit-readonly = YES.
      f-mainres.deposit-disabled = YES.
  END.
  ELSE IF reservation.depositgef GT 0 AND f-mainres.depositres = 0 THEN /* Malik Serverless 471 : depositres -> f-mainres.depositres */
  DO:
      f-mainres.deposit-disabled = YES.
  END.
  /*MT 24/06/15
  ASSIGN
    f-mainres.deposit-readonly = AVAILABLE res-line
    f-mainres.deposit-disabled = reservation.depositgef GT 0 
      AND f-mainres.depositres = 0
  .
  */

  FIND FIRST master WHERE master.resnr = reservation.resnr NO-LOCK NO-ERROR. 
  IF AVAILABLE master THEN 
  DO: 
    FIND FIRST guest WHERE guest.gastnr = master.gastnrpay NO-LOCK. 
    ASSIGN
      f-mainres.master-exist      = YES
      f-mainres.gastnrpay         = master.gastnrpay
      f-mainres.umsatz1           = master.umsatzart[1]
      f-mainres.umsatz3           = master.umsatzart[3] 
      f-mainres.umsatz4           = master.umsatzart[4] 
      f-mainres.bill-receiver     = guest.name + ", " + guest.vorname1 
        + " " + guest.anrede1 + guest.anredefirma
    .
  END. 

  CREATE t-reservation.
  BUFFER-COPY reservation TO t-reservation.

  FIND FIRST master WHERE master.resnr = resnr NO-LOCK NO-ERROR.
  IF AVAILABLE master THEN
  DO:
    CREATE t-master.
    BUFFER-COPY master TO t-master.
    FIND FIRST guest WHERE guest.gastnr = master.gastnrpay NO-LOCK. 
    bill-receiver = guest.name + ", " + guest.vorname1 + " " + guest.anrede1 
      + guest.anredefirma. 
  END.
  
  RELEASE reservation.
END.


