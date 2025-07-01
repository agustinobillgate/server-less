DEFINE TEMP-TABLE t-kellner LIKE kellner.  
DEFINE TEMP-TABLE q1-list  
    FIELD kellner-nr    LIKE kellner.kellner-nr  
    FIELD kellnername   LIKE kellner.kellnername  
    FIELD kumsatz-nr    LIKE kellner.kumsatz-nr  
    FIELD kumsatz-nr1   LIKE kellne1.kumsatz-nr  
    FIELD kcredit-nr    LIKE kellner.kcredit-nr  
    FIELD kzahl-nr      LIKE kellner.kzahl-nr  
    FIELD kzahl-nr1     LIKE kellne1.kzahl-nr  
    FIELD masterkey     LIKE kellner.masterkey  
    FIELD sprachcode    LIKE kellner.sprachcode  
    FIELD r-kellner AS INT  
    FIELD r-kellne1 AS INT.  
  
DEFINE TEMP-TABLE t-list LIKE kellner.  
  
DEF INPUT PARAMETER TABLE FOR t-list.  
DEF INPUT PARAMETER case-type AS INT.  
DEF INPUT PARAMETER dept AS INT.  
DEF INPUT PARAMETER curr-mode AS CHAR.  
DEF INPUT PARAMETER kzahl-nr1 AS INT.  
DEF INPUT PARAMETER kumsatz-nr1 AS INT.  
DEF INPUT PARAMETER r-kellner AS INT.  
DEF INPUT PARAMETER r-kellne1 AS INT.  
DEF OUTPUT PARAMETER TABLE FOR q1-list.  
DEF OUTPUT PARAMETER TABLE FOR t-kellner.  

DEFINE VARIABLE dept-number AS INT.

dept-number = dept.
  
FIND FIRST t-list.  
IF case-type = 1 THEN /*MT add */  
DO:  
    CREATE kellner.   
    RUN fill-new-kellner.  
END.  
ELSE IF case-type = 2 THEN /*MT chg */  
DO:  
    FIND FIRST kellner WHERE RECID(kellner) = r-kellner NO-LOCK NO-ERROR.  
    IF AVAILABLE kellner THEN
    DO:

      FIND FIRST kellne1 WHERE RECID(kellne1) = r-kellne1 NO-LOCK NO-ERROR.  
      IF AVAILABLE kellne1 THEN
      DO:
          FIND CURRENT kellner EXCLUSIVE-LOCK.   
          FIND CURRENT kellne1 EXCLUSIVE-LOCK.   
          RUN fill-new-kellner. 
          FIND CURRENT kellner NO-LOCK.
          RELEASE kellner.
          FIND CURRENT kellne1 NO-LOCK.
          RELEASE kellne1.
      END.
    END.
END.  
RUN prepare-rwaiter-adminbl.p  
    (dept-number, OUTPUT TABLE q1-list, OUTPUT TABLE t-kellner).  
  
PROCEDURE fill-new-kellner:   
DEFINE buffer waiter1 FOR kellne1.   
  kellner.departement = dept-number.   
  kellner.kellner-nr = t-list.kellner-nr.   
  kellner.kellnername = t-list.kellnername.   
  kellner.kumsatz-nr = t-list.kumsatz-nr.   
  kellner.kcredit-nr = t-list.kcredit-nr.   
  kellner.kzahl-nr = t-list.kzahl-nr.   
  kellner.masterkey = t-list.masterkey.   
  kellner.sprachcode = t-list.sprachcode.   
  IF curr-mode = "chg" THEN   
  DO:   
    kellne1.kzahl-nr = kzahl-nr1.   
    kellne1.kumsatz-nr = kumsatz-nr1.   
  END.   
  ELSE IF curr-mode = "add" THEN   
  DO:   
    create waiter1.   
    waiter1.departement = dept-number.   
    waiter1.kellner-nr = t-list.kellner-nr.   
    waiter1.kzahl-nr = kzahl-nr1.   
    waiter1.kumsatz-nr = kumsatz-nr1.   
  END.   
END.   
  
