DEF TEMP-TABLE p-list
    FIELD rechnr       AS INTEGER 
    FIELD dept         AS INTEGER 
    FIELD billno       AS INTEGER 
    FIELD printed-line AS INTEGER 
    FIELD b-recid      AS INTEGER 
    FIELD last-amount  AS DECIMAL 
    FIELD last-famount AS DECIMAL. 

DEF INPUT-OUTPUT PARAMETER TABLE FOR p-list.
DEF INPUT PARAMETER rec-id AS INT.
DEF INPUT PARAMETER use-h-queasy AS LOGICAL.

FIND FIRST h-bill WHERE RECID(h-bill) = rec-id.
RUN del-queasy.

PROCEDURE del-queasy:
/* number2: vhp.billrecid, deci2: vhp.billnr */ 
  IF NOT use-h-queasy THEN
  DO:
      FOR EACH vhp.queasy WHERE vhp.queasy.key = 4 
        AND vhp.queasy.number1 = (vhp.h-bill.departement + vhp.h-bill.rechnr * 100) 
        AND vhp.queasy.number2 GE 0 AND vhp.queasy.deci2 GE 0 EXCLUSIVE-LOCK: 
        DELETE vhp.queasy. 
      END. 
      RELEASE queasy.
  END.  
  ELSE
  DO:
      FOR EACH h-queasy WHERE 
        h-queasy.number1 = (h-bill.departement + h-bill.rechnr * 100) EXCLUSIVE-LOCK: 
        DELETE h-queasy. 
      END. 
      RELEASE h-queasy.
  END.
  
  FOR EACH p-list WHERE p-list.rechnr = vhp.h-bill.rechnr 
    AND p-list.dept = vhp.h-bill.departement: 
    DELETE p-list. 
  END. 
END. 
