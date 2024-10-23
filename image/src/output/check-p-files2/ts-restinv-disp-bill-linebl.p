DEF TEMP-TABLE t-h-bill-line LIKE h-bill-line  
    FIELD rec-id AS INT  
    FIELD request-str AS CHAR  
    FIELD flag-code AS INT INIT 0.  
  
DEF INPUT PARAMETER double-currency AS LOGICAL.  
DEF INPUT PARAMETER rechnr AS INT.  
DEF INPUT PARAMETER curr-dept AS INT.  
DEF INPUT PARAMETER avail-t-h-bill AS LOGICAL.  
DEF OUTPUT PARAMETER TABLE FOR t-h-bill-line.  
  
IF double-currency THEN   
FOR EACH vhp.h-bill-line WHERE vhp.h-bill-line.rechnr = rechnr  
    AND vhp.h-bill-line.departement = curr-dept NO-LOCK   
    BY vhp.h-bill-line.bill-datum descending BY vhp.h-bill-line.zeit descending:  
    CREATE t-h-bill-line.  
    BUFFER-COPY h-bill-line TO t-h-bill-line.  
    ASSIGN t-h-bill-line.rec-id = RECID(h-bill-line).  
    RUN show-submenu.  
    RUN ts-restinv-disp-requestbl.p(RECID(h-bill-line), OUTPUT request-str).  
    ASSIGN t-h-bill-line.request-str = request-str.  
END.  
ELSE   
FOR EACH vhp.h-bill-line WHERE vhp.h-bill-line.rechnr = rechnr  
    AND vhp.h-bill-line.departement = curr-dept NO-LOCK  
    BY vhp.h-bill-line.bill-datum descending BY vhp.h-bill-line.zeit descending:  
    CREATE t-h-bill-line.  
    BUFFER-COPY h-bill-line TO t-h-bill-line.  
    ASSIGN t-h-bill-line.rec-id = RECID(h-bill-line).  
    RUN show-submenu.  
    RUN ts-restinv-disp-requestbl.p(RECID(h-bill-line), OUTPUT request-str).  
    ASSIGN t-h-bill-line.request-str = request-str.  

END.  
  
  
  
  
PROCEDURE show-submenu:  
DEFINE buffer h-art2 FOR vhp.h-artikel.  
  
  FIND FIRST h-art2 WHERE h-art2.departement = vhp.h-bill-line.departement   
    AND h-art2.artnr = vhp.h-bill-line.artnr NO-LOCK NO-ERROR.   
  IF NOT AVAILABLE h-art2 OR NOT avail-t-h-bill THEN   
  DO:  
    t-h-bill-line.flag-code = 0.  
    /*MTIF tischnr = 0 THEN APPLY "entry" TO tischnr IN FRAME frame1.   
    ELSE APPLY "entry" TO billart IN FRAME frame1.   
    RETURN.*/  
  END.   
  ELSE IF h-art2.artart = 0 AND h-art2.betriebsnr GT 0 THEN   
  DO:  
    t-h-bill-line.flag-code = 1.  
    /*MT  
    FIND FIRST vhp.h-journal WHERE vhp.h-journal.artnr = vhp.h-bill-line.artnr   
      AND vhp.h-journal.departement = vhp.h-bill-line.departement   
        AND vhp.h-journal.rechnr = vhp.h-bill-line.rechnr   
        AND vhp.h-journal.bill-datum = vhp.h-bill-line.bill-datum   
        AND vhp.h-journal.zeit = vhp.h-bill-line.zeit   
        AND vhp.h-journal.sysdate = vhp.h-bill-line.sysdate NO-LOCK NO-ERROR.   
    IF AVAILABLE vhp.h-journal THEN   
    DO:  
      t-h-bill-line.flag-code = 1.  
      /*MThide b1 b11 IN FRAME frame1.   
      ENABLE b2 WITH FRAME frame1. */  
      OPEN QUERY q2 FOR EACH h-mjourn WHERE   
        h-mjourn.departement = vhp.h-journal.departement   
        AND h-mjourn.h-artnr = vhp.h-journal.artnr   
        AND h-mjourn.rechnr = vhp.h-journal.rechnr   
        AND h-mjourn.bill-datum = vhp.h-journal.bill-datum   
        AND h-mjourn.sysdate = vhp.h-journal.sysdate   
        AND h-mjourn.zeit = vhp.h-journal.zeit,   
        FIRST h-art2 WHERE h-art2.artnr = h-mjourn.artnr   
          AND h-art2.departement = h-mjourn.departement NO-LOCK   
          BY h-art2.zwkum BY h-art2.bezeich.   
    END.*/  
  END.  
  
END.  
