
/*MI 12/05/14 -> update pada waiter2 dengan field kcredit-nr dan departement*/

DEF INPUT PARAMETER r-kellner AS INT.
DEF INPUT PARAMETER dept2 AS INT.
DEF INPUT PARAMETER dept AS INT.
DEF INPUT PARAMETER crart2 AS INT.

DEF BUFFER toart1 FOR artikel. 
DEF BUFFER toart2 FOR artikel.
DEF BUFFER waiter1 FOR kellne1.
DEF BUFFER waiter2 FOR kellner. 

FIND FIRST kellner WHERE RECID(kellner) = r-kellner.

FIND FIRST toart2 WHERE toart2.artnr = kellner.kumsatz-nr 
    AND toart2.departement = dept2 NO-LOCK NO-ERROR. 
IF NOT AVAILABLE toart2 THEN 
DO: 
  FIND FIRST toart1 WHERE toart1.artnr = kellner.kumsatz-nr 
      AND toart1.departement = dept NO-LOCK. 
  BUFFER-COPY toart1 EXCEPT departement TO toart2. 
  ASSIGN toart2.departement = dept2. 
END. 

FIND FIRST toart2 WHERE toart2.artnr = kellner.kzahl-nr 
    AND toart2.departement = dept2 NO-LOCK NO-ERROR. 
IF NOT AVAILABLE toart2 THEN 
DO: 
  CREATE toart2. 
  FIND FIRST toart1 WHERE toart1.artnr = kellner.kzahl-nr 
      AND toart1.departement = dept NO-LOCK. 
  BUFFER-COPY toart1 EXCEPT departement TO toart2. 
  ASSIGN toart2.departement = dept2. 
END. 

/*MI 12/05/14*/
FIND FIRST waiter2 WHERE waiter2.departement = dept2 AND 
    waiter2.kumsatz-nr = kellner.kumsatz-nr NO-LOCK NO-ERROR.
IF AVAILABLE waiter2 THEN 
DO: 
    FIND CURRENT waiter2 EXCLUSIVE-LOCK.
    BUFFER-COPY kellner EXCEPT kcredit-nr departement TO waiter2. 
    ASSIGN 
        waiter2.kcredit-nr = crart2 
        waiter2.departement = dept2. 
END.
ELSE 
DO: 
    FIND FIRST kellner WHERE RECID(kellner) = r-kellner.
    CREATE waiter2.
    BUFFER-COPY kellner EXCEPT kcredit-nr departement TO waiter2. 
    ASSIGN 
        waiter2.kcredit-nr = crart2 
        waiter2.departement = dept2.
END.
FIND CURRENT waiter2 NO-LOCK. 
RELEASE waiter2. 

FIND FIRST waiter1 WHERE waiter1.kellner-nr = kellner.kellner-nr 
    AND waiter1.departement = dept2 NO-LOCK NO-ERROR. 
IF NOT AVAILABLE waiter1 THEN 
DO: 
  CREATE waiter1. 
  BUFFER-COPY kellner EXCEPT departement TO waiter1. 
  ASSIGN waiter1.departement = dept2. 
  RELEASE waiter1.
END. 
