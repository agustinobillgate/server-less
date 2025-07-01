DEFINE TEMP-TABLE table-list 
    FIELD rechnr     AS INTEGER 
    FIELD tischnr    AS INTEGER 
    FIELD saldo      AS DECIMAL 
    FIELD belong     AS CHAR INITIAL "L". 

DEF INPUT PARAMETER curr-dept AS INT.
DEF INPUT PARAMETER curr-waiter AS INT.
DEF OUTPUT PARAMETER TABLE FOR table-list.

DEF BUFFER hbill FOR vhp.h-bill.

FOR EACH table-list: 
    DELETE table-list. 
END. 
FOR EACH hbill WHERE  hbill.departement = curr-dept 
    AND hbill.flag = 0 AND hbill.kellner-nr = curr-waiter 
    NO-LOCK BY hbill.tischnr: 
    CREATE table-list. 
    ASSIGN 
      table-list.rechnr = hbill.rechnr 
      table-list.saldo = hbill.saldo 
      table-list.tischnr = hbill.tischnr 
    . 
END. 
