DEFINE TEMP-TABLE temp 
    FIELD pos AS int 
    FIELD bezeich AS CHAR 
    FIELD artnr AS int. 

DEFINE TEMP-TABLE Rhbline 
  FIELD nr AS INTEGER 
  FIELD rid AS INTEGER. 

DEF INPUT PARAMETER rec-id AS INT.
DEF INPUT PARAMETER dept AS INT.
DEF INPUT PARAMETER curr-select AS INT.

DEF OUTPUT PARAMETER max-Rapos AS INT INIT 0.
DEF OUTPUT PARAMETER TABLE FOR temp.
DEF OUTPUT PARAMETER TABLE FOR Rhbline.


FIND FIRST h-bill WHERE RECID(h-bill) = rec-id.
RUN build-Rmenu.

PROCEDURE build-Rmenu: 
DEFINE VARIABLE curr-Rapos AS INTEGER INITIAL 1. 
DEFINE VARIABLE i AS INTEGER INITIAL 0. 
  FOR EACH temp: 
    DELETE temp. 
  END. 
  FOR EACH Rhbline: 
    DELETE Rhbline. 
  END. 
 
  curr-Rapos = 1. 
  max-Rapos = 0. 
  
  FOR EACH vhp.h-bill-line WHERE  vhp.h-bill-line.rechnr = vhp.h-bill.rechnr AND 
    vhp.h-bill-line.departement = dept 
    AND vhp.h-bill-line.waehrungsnr = curr-select 
    /* AND vhp.h-bill-line.paid-flag = 0 */ NO-LOCK BY vhp.h-bill-line.bezeich: 
    FIND FIRST vhp.h-artikel WHERE vhp.h-artikel.artnr = vhp.h-bill-line.artnr 
      AND vhp.h-artikel.departement = vhp.h-bill-line.departement 
      NO-LOCK NO-ERROR. 
    i = i + 1. 
    CREATE temp. 
    temp.pos = i. 
    temp.artnr = vhp.h-bill-line.artnr. 
    IF AVAILABLE vhp.h-artikel AND (h-artikel.artart = 0 OR artart = 1) THEN 
      temp.bezeich = STRING(vhp.h-bill-line.anzahl) + " " 
      + vhp.h-bill-line.bezeich. 
    ELSE temp.bezeich = vhp.h-bill-line.bezeich. 
    CREATE Rhbline. 
    Rhbline.nr = i. 
    Rhbline.rid = RECID(vhp.h-bill-line). 
  END.
  max-Rapos = i.
END. 
