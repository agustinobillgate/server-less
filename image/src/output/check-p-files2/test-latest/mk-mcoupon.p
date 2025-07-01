 
DEFINE INPUT PARAMETER resnr AS INTEGER. 
DEFINE INPUT PARAMETER zinr AS CHAR. 
DEFINE VARIABLE anzahl AS INTEGER. 
DEFINE VARIABLE eknr AS INTEGER. 
DEFINE VARIABLE i AS INTEGER. 
DEFINE VARIABLE depart AS DATE. 
DEFINE VARIABLE gname AS CHAR. 
 
FIND FIRST htparam WHERE paramnr = 274 NO-LOCK. 
IF NOT flogical THEN RETURN. 
 
FIND FIRST htparam WHERE paramnr = 273 NO-LOCK. 
eknr = finteger. 
IF eknr = 0 THEN RETURN. 
 
anzahl = 0. 
FOR EACH res-line WHERE res-line.resnr = resnr 
  AND res-line.resstatus NE 8 
  AND res-line.resstatus NE 9 AND res-line.resstatus NE 10 
  AND res-line.resstatus NE 12 NO-LOCK: 
  depart = res-line.abreise. 
  IF res-line.resstatus = 6 THEN gname = res-line.name. 
  FIND FIRST arrangement WHERE arrangement.arrangement 
    = res-line.arrangement NO-LOCK. 
  FOR EACH argt-line WHERE argt-line.argtnr = arrangement.argtnr NO-LOCK: 
    FIND FIRST artikel WHERE artikel.artnr = argt-line.argt-artnr 
      AND artikel.departement = argt-line.departement NO-LOCK NO-ERROR. 
    IF AVAILABLE artikel AND artikel.endkum = eknr THEN 
      anzahl = anzahl + (res-line.erwachs + res-line.kind1 + res-line.gratis) 
        * (res-line.abreise - res-line.ankunft). 
  END. 
END. 
 
IF anzahl GT 0 THEN 
DO: 
  create mealcoup. 
  mealcoup.resnr = resnr. 
  mealcoup.zinr = zinr. 
  mealcoup.name = gname. 
  mealcoup.anzahl = anzahl. 
  mealcoup.abreise = depart. 
END. 
 
