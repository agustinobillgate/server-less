
DEFINE TEMP-TABLE hmenu-list LIKE h-menu. 
DEFINE TEMP-TABLE menu-list  LIKE h-menu.

DEF INPUT-OUTPUT PARAMETER TABLE FOR hmenu-list.
DEF INPUT-OUTPUT PARAMETER TABLE FOR menu-list.
DEF INPUT-OUTPUT PARAMETER menu-nr  AS INTEGER. 
DEF INPUT        PARAMETER dept     AS INT.
DEF INPUT        PARAMETER h-artnr  AS INT.
DEF OUTPUT       PARAMETER done     AS LOGICAL INITIAL NO. 

DEFINE buffer h-art FOR h-artikel.

FIND FIRST h-art WHERE h-art.departement = dept AND h-art.artnr = h-artnr 
NO-LOCK NO-ERROR. 

RUN create-menu.

PROCEDURE create-menu: 
DEFINE VARIABLE nr AS INTEGER. 
DEFINE VARIABLE created AS LOGICAL INITIAL NO.

  IF NOT AVAILABLE h-art OR h-art.betriebsnr = 0 THEN RUN get-nr(OUTPUT nr). 
  ELSE nr = h-art.betriebsnr. 
  menu-nr = nr. 
  IF AVAILABLE h-art AND h-art.betriebsnr NE 0 THEN 
  FOR EACH h-menu WHERE h-menu.departement = dept 
      AND h-menu.nr = h-art.betriebsnr: 
      delete h-menu. 
  END. 
  FOR EACH menu-list: 
      create h-menu. 
      ASSIGN 
        h-menu.departement = dept 
        h-menu.nr = nr 
        h-menu.artnr = menu-list.artnr. 
      release h-menu. 
      created = YES. 
      delete menu-list. 
  END. 
  done = YES. 
  IF NOT AVAILABLE h-art THEN RETURN. 
  IF created AND h-art.betriebsnr = 0 THEN 
  DO: 
    FIND CURRENT h-art EXCLUSIVE-LOCK. 
    h-art.betriebsnr = nr. 
    FIND CURRENT h-art NO-LOCK. 
  END. 
  ELSE IF NOT created AND h-art.betriebsnr NE 0 THEN 
  DO: 
    FIND CURRENT h-art EXCLUSIVE-LOCK. 
    h-art.betriebsnr = 0. 
    FIND CURRENT h-art NO-LOCK. 
    menu-nr = 0. 
  END. 
END. 


PROCEDURE get-nr: 
DEFINE OUTPUT PARAMETER nr AS INTEGER INITIAL 0. 
DEFINE buffer h-art FOR h-artikel. 
  FOR EACH h-art WHERE h-art.departement = dept 
      AND h-art.betriebsnr NE 0 NO-LOCK: 
      IF nr LT h-art.betriebsnr THEN nr = h-art.betriebsnr. 
  END. 
  nr = nr + 1. 
END. 
