
DEF INPUT PARAMETER pvILanguage  AS INTEGER  NO-UNDO.
DEF INPUT PARAMETER currency     AS CHAR     NO-UNDO.
DEF INPUT PARAMETER zipreis      AS DECIMAL  NO-UNDO.
DEF OUTPUT PARAMETER msg-str     AS CHAR     NO-UNDO INIT "".
DEF OUTPUT PARAMETER curr-number AS INTEGER  NO-UNDO INIT 0.
DEF OUTPUT PARAMETER curr-amount AS DECIMAL  NO-UNDO INIT 1.

DEF VARIABLE max-rate AS DECIMAL NO-UNDO. 

{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "mk-resline". 

FIND FIRST waehrung WHERE waehrung.wabkurz = currency NO-LOCK. 
ASSIGN 
  curr-number = waehrung.waehrungsnr
  curr-amount = waehrung.ankauf / waehrung.einheit
. 

RUN htpdec.p (1108, OUTPUT max-rate).
IF max-rate NE 0 AND zipreis GT 0 
  AND (zipreis * curr-amount) GT max-rate THEN 
  msg-str = translateExtended ("Room Rate too large, currency NOT changed.", lvCAREA, "":U).
