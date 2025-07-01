DEFINE INPUT PARAMETER resnr AS INTEGER NO-UNDO.
DEFINE VARIABLE exchg-rate AS DECIMAL INITIAL 0. 
  
FIND FIRST reservation WHERE reservation.resnr = resnr NO-LOCK.

IF NOT reservation.insurance THEN 
DO: 
  FOR EACH res-line WHERE res-line.resnr = reservation.resnr 
    AND (res-line.resstatus = 6 OR res-line.resstatus = 13) 
    AND res-line.reserve-dec NE 0: 
    res-line.reserve-dec = 0. 
  END. 
  RETURN. 
END. 
 
FIND FIRST htparam WHERE htparam.paramnr = 144 NO-LOCK. 
FIND FIRST waehrung WHERE waehrung.wabkurz = htparam.fchar NO-LOCK NO-ERROR. 
IF AVAILABLE waehrung THEN exchg-rate = waehrung.ankauf / waehrung.einheit. 

IF exchg-rate NE 0 THEN 
FOR EACH res-line WHERE res-line.resnr = reservation.resnr 
  AND (res-line.resstatus = 6 OR res-line.resstatus = 13) 
  AND res-line.reserve-dec = 0: 
  res-line.reserve-dec = exchg-rate. 
END. 
