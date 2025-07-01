
DEF INPUT  PARAMETER bill-resnr     AS INT.
DEF INPUT  PARAMETER bill-reslinnr  AS INT.
DEF INPUT  PARAMETER billdatum      AS DATE.
DEF OUTPUT PARAMETER skip-it        AS LOGICAL  NO-UNDO INIT NO.
DEF OUTPUT PARAMETER buff-rechnr    AS INTEGER  NO-UNDO INIT -1. /* SY */

DEF VARIABLE na-running  AS LOGICAL NO-UNDO. 
DEF BUFFER buf-artikel   FOR artikel.
DEF BUFFER buf-bill-line FOR bill-line.

skip-it = YES.
/* SY: room charge not allowed when night audit is running */
FIND FIRST htparam WHERE paramnr = 253 NO-LOCK. 
na-running = htparam.flogical. 
IF na-running THEN RETURN.

FIND FIRST res-line WHERE res-line.resnr = bill-resnr
  AND res-line.reslinnr = bill-reslinnr NO-LOCK NO-ERROR. 
FIND FIRST arrangement WHERE arrangement.arrangement = res-line.arrangement 
  NO-LOCK. 
FIND FIRST buf-artikel WHERE buf-artikel.artnr = arrangement.argt-artikelnr 
  AND buf-artikel.departement = 0 NO-LOCK. 

FIND FIRST buf-bill-line WHERE buf-bill-line.departement = 0
  AND buf-bill-line.artnr = buf-artikel.artnr
  AND buf-bill-line.bill-datum = billdatum
  AND buf-bill-line.zinr NE ""
  AND buf-bill-line.massnr = res-line.resnr
  AND buf-bill-line.billin-nr = res-line.reslinnr
  USE-INDEX dep-art-dat_ix NO-LOCK NO-ERROR.
skip-it = AVAILABLE buf-bill-line.
IF skip-it THEN buff-rechnr = buf-bill-line.rechnr.
