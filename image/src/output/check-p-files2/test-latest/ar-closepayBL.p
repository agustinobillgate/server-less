
DEFINE TEMP-TABLE b2-list
    FIELD name          LIKE guest.name
    FIELD vorname1      LIKE guest.vorname1
    FIELD anrede1       LIKE guest.anrede1
    FIELD anredefirma   LIKE guest.anredefirma
    FIELD rechnr        LIKE debitor.rechnr
    FIELD artnr         LIKE debitor.artnr
    FIELD bezeich       LIKE artikel.bezeich
    FIELD rgdatum       LIKE debitor.rgdatum
    FIELD saldo         LIKE debitor.saldo
    FIELD counter       LIKE debitor.counter
    FIELD b-resname     AS CHAR
    FIELD b-comments    AS CHAR.

DEFINE TEMP-TABLE b3-list
    FIELD rgdatum   LIKE debitor.rgdatum
    FIELD zahlkonto LIKE debitor.zahlkonto
    FIELD bezeich   LIKE artikel.bezeich
    FIELD saldo     LIKE debitor.saldo
    FIELD vesrdep   LIKE debitor.vesrdep
    FIELD userinit  LIKE bediener.userinit.

DEFINE TEMP-TABLE artikel2
    FIELD artnr LIKE artikel.artnr 
    FIELD bezeich LIKE artikel.bezeich .

DEFINE INPUT PARAMETER case-type AS INTEGER.
DEFINE INPUT PARAMETER bill-name AS CHAR.
DEFINE INPUT PARAMETER bill-nr AS INTEGER.
DEFINE INPUT PARAMETER bill-artnr AS INTEGER.
DEFINE INPUT PARAMETER counter AS INTEGER.
DEFINE INPUT-OUTPUT PARAMETER balance AS DECIMAL.
DEFINE OUTPUT PARAMETER TABLE FOR b2-list.
DEFINE OUTPUT PARAMETER TABLE FOR b3-list.
DEFINE OUTPUT PARAMETER TABLE FOR artikel2.

DEFINE buffer artikel0 FOR artikel. 
DEFINE buffer artikel1 FOR artikel. 

DEFINE buffer debitor3 FOR debitor. 
DEFINE buffer bediener1 FOR bediener. 

IF case-type = 2 THEN RUN open-q2.
ELSE IF case-type = 3 THEN RUN open-q3.

PROCEDURE open-q2: 
  DEFINE buffer artikel1 FOR artikel. 
  DEFINE VARIABLE curr-rechnr AS INTEGER. 
  DEFINE VARIABLE curr-saldo AS DECIMAL. 
  DEFINE VARIABLE opart AS INTEGER INITIAL 1. 
  DEFINE VARIABLE to-name AS CHAR. 
 
  curr-rechnr = 0. 
 
  to-name = chr(asc(SUBSTR(bill-name,1,1)) + 1). 
  IF bill-nr GT 0 THEN
  FOR EACH debitor WHERE 
    debitor.artnr = bill-artnr AND debitor.opart EQ 2 
    AND debitor.rechnr EQ bill-nr AND debitor.zahlkonto = 0 NO-LOCK, 
    FIRST guest WHERE guest.gastnr = debitor.gastnr NO-LOCK, 
    FIRST artikel0 WHERE artikel0.artnr = debitor.artnr 
    AND artikel0.departement = 0 NO-LOCK BY guest.name BY debitor.rgdatum:
      RUN create-b2-list.
  END.
  ELSE 
  FOR EACH debitor WHERE 
    debitor.artnr = bill-artnr AND debitor.opart EQ 2 
    AND debitor.name GE bill-name AND debitor.name LE to-name 
    AND debitor.zahlkonto = 0 NO-LOCK, 
    FIRST guest WHERE guest.gastnr = debitor.gastnr NO-LOCK, 
    FIRST artikel0 WHERE artikel0.artnr = debitor.artnr 
    AND artikel0.departement = 0 NO-LOCK BY guest.name BY debitor.rechnr:
      RUN create-b2-list.
  END.

END. 


PROCEDURE open-q3:
    DEFINE buffer debitor1 FOR debitor. 
    FOR EACH debitor3 WHERE debitor3.counter = counter 
        AND debitor3.zahlkonto GT 0 NO-LOCK, 
      FIRST artikel1 WHERE artikel1.departement = 0 
        AND artikel1.artnr = debitor3.zahlkonto NO-LOCK, 
      FIRST bediener1 WHERE bediener1.nr = debitor3.bediener-nr 
         BY debitor3.rgdatum BY debitor3.zahlkonto:
        RUN create-b3-list.
    END.

    FOR EACH artikel WHERE artikel.departement = 0
        AND (artikel.artart = 4 OR artikel.artart = 6) 
        AND artikel.activeflag = YES NO-LOCK :
        CREATE artikel2.
        ASSIGN
          artikel2.artnr   = artikel.artnr 
          artikel2.bezeich = artikel.bezeich .
    END.
      
    FOR EACH debitor1 WHERE debitor1.counter = counter
        AND debitor1.opart = 2 AND debitor1.zahlkonto GT 0 NO-LOCK:
        balance = balance + debitor1.saldo. 
    END.
END.


PROCEDURE create-b3-list:
    CREATE b3-list.
    ASSIGN
      b3-list.rgdatum   = debitor3.rgdatum
      b3-list.zahlkonto = debitor3.zahlkonto
      b3-list.bezeich   = artikel1.bezeich
      b3-list.saldo     = debitor3.saldo
      b3-list.vesrdep   = debitor3.vesrdep
      b3-list.userinit  = bediener1.userinit.
END.


PROCEDURE create-b2-list:
    CREATE b2-list.
    ASSIGN
        b2-list.name          = guest.name
        b2-list.vorname1      = guest.vorname1
        b2-list.anrede1       = guest.anrede1
        b2-list.anredefirma   = guest.anredefirma
        b2-list.rechnr        = debitor.rechnr
        b2-list.artnr         = debitor.artnr
        b2-list.bezeich       = artikel0.bezeich
        b2-list.rgdatum       = debitor.rgdatum
        b2-list.saldo         = debitor.saldo
        b2-list.counter       = debitor.counter.
        
    IF AVAILABLE debitor THEN 
    DO: 
       RUN disp-guest-debt. 
    END. 
END.

PROCEDURE disp-guest-debt: 
  IF AVAILABLE debitor THEN 
  DO: 
    ASSIGN b2-list.b-resname = guest.name + " " + guest.vorname1 + ", " + guest.anrede1 + guest.anredefirma 
            + chr(10) + guest.adresse1 
            + chr(10) + guest.wohnort + " " + guest.plz
    b2-list.b-comments = guest.bemerk. 
    
  END. 
END. 
