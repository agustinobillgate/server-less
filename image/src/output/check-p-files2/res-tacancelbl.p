/******************** DEFINE TEMP TABLE *************************/ 
DEFINE TEMP-TABLE res-tacancel 
  FIELD resnr AS INTEGER 
  FIELD name AS CHAR FORMAT "x(30)" COLUMN-LABEL "Travel Agents" 
  FIELD mnite AS INTEGER FORMAT ">>,>>9" COLUMN-LABEL "MTD RmNite" 
  FIELD pmnite AS INTEGER FORMAT ">>9.9" COLUMN-LABEL "(%)" 
  FIELD ynite AS INTEGER FORMAT ">>,>>9" COLUMN-LABEL "YTD RmNite" 
  FIELD pynite AS INTEGER FORMAT ">>9.9" COLUMN-LABEL "(%)" 
  FIELD mtu AS DECIMAL FORMAT ">>,>>>,>>>,>>9" COLUMN-LABEL "MTD Expect Rev" 
  FIELD pmtu AS INTEGER FORMAT ">>9.9" COLUMN-LABEL "(%)" 
  FIELD ytu AS DECIMAL FORMAT ">>>,>>>,>>>,>>9" COLUMN-LABEL "YTD Expect Rev" 
  FIELD pytu AS INTEGER FORMAT ">>9.9" COLUMN-LABEL "(%)" 
  FIELD wohnort AS CHAR FORMAT "x(36)" COLUMN-LABEL "City - Land". 


DEFINE INPUT PARAMETER pvILanguage  AS INTEGER           NO-UNDO.
DEFINE INPUT PARAMETER stattype  AS INTEGER.
DEFINE INPUT PARAMETER sorttype  AS INTEGER.
DEFINE INPUT PARAMETER fdate       AS DATE. 
DEFINE INPUT PARAMETER fname       AS CHAR. 
DEFINE INPUT PARAMETER tname       AS CHAR. 
DEFINE OUTPUT PARAMETER t-mnite AS INTEGER.
DEFINE OUTPUT PARAMETER t-ynite AS INTEGER.
DEFINE OUTPUT PARAMETER t-mtu AS DECIMAL.
DEFINE OUTPUT PARAMETER t-ytu AS DECIMAL.
DEFINE OUTPUT PARAMETER TABLE FOR res-tacancel.


{supertransBL.i} 
DEFINE VARIABLE lvCAREA AS CHARACTER INITIAL "res-tacancel". 

/******************** MAIN LOGIC *************************/ 
IF stattype = 1 THEN RUN disp-noshow.
ELSE RUN disp-noshow1.


/******************** PROCEDURE *************************/ 
PROCEDURE disp-noshow: 
DEFINE VARIABLE gastnr AS INTEGER INITIAL 0. 
DEFINE VARIABLE rmnite AS INTEGER. 
DEFINE VARIABLE bdate AS DATE. 
 
  /*ENABLE b1 WITH FRAME frame1. */
  /*DISP fdate fname tname WITH FRAME frame1. */
 
  FOR EACH res-tacancel: 
    delete res-tacancel. 
  END. 
 
  bdate = DATE(1, 1, year(fdate)). 
  t-mnite = 0. 
  t-mtu = 0. 
  t-ynite = 0. 
  t-ytu = 0. 
  IF sorttype = 1 THEN 
  FOR EACH res-line WHERE active-flag = 2 
    AND resstatus = 9 AND res-line.ankunft GE bdate 
    AND res-line.ankunft LE fdate 
    AND res-line.resname GE fname AND res-line.resname LE tname 
    AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
    FIRST guest WHERE guest.gastnr = res-line.gastnr 
    AND guest.karteityp = 2 NO-LOCK, 
    FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK 
    BY res-line.resname BY res-line.ankunft BY res-line.name: 
    FIND FIRST res-tacancel WHERE res-tacancel.resnr = res-line.resnr NO-ERROR. 
    IF NOT AVAILABLE res-tacancel THEN 
    DO: 
      create res-tacancel. 
      res-tacancel.resnr = res-line.resnr. 
      res-tacancel.name = guest.name + ", " + guest.anredefirma. 
      res-tacancel.wohnort = guest.wohnort + " " + STRING(guest.plz) 
        + " - " + guest.land. 
      gastnr = res-line.gastnr. 
    END. 
    rmnite = (res-line.abreise - res-line.ankunft) * res-line.zimmeranz. 
    IF month(res-line.ankunft) = month(fdate) THEN 
    DO: 
      res-tacancel.mnite = res-tacancel.mnite + rmnite. 
      res-tacancel.mtu = res-tacancel.mtu + rmnite * res-line.zipreis. 
      t-mnite = t-mnite + rmnite. 
      t-mtu = t-mtu + rmnite * res-line.zipreis. 
    END. 
    res-tacancel.ynite = res-tacancel.ynite + rmnite. 
    res-tacancel.ytu = res-tacancel.ytu + rmnite * res-line.zipreis. 
    t-ynite = t-ynite + rmnite. 
    t-ytu = t-ytu + rmnite * res-line.zipreis. 
  END. 
  ELSE 
  FOR EACH res-line WHERE active-flag = 2 
    AND resstatus = 9 AND res-line.ankunft GE bdate 
    AND res-line.ankunft LE fdate 
    AND res-line.resname GE fname AND res-line.resname LE tname NO-LOCK, 
    FIRST guest WHERE guest.gastnr = res-line.gastnr 
    AND guest.karteityp = 1 NO-LOCK, 
    FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK 
    BY res-line.resname BY res-line.ankunft BY res-line.name: 
    FIND FIRST res-tacancel WHERE res-tacancel.resnr = res-line.resnr NO-ERROR. 
    IF NOT AVAILABLE res-tacancel THEN 
    DO: 
      create res-tacancel. 
      res-tacancel.resnr = res-line.resnr. 
      res-tacancel.name = guest.name + ", " + guest.anredefirma. 
      res-tacancel.wohnort = guest.wohnort + " " + STRING(guest.plz) 
        + " - " + guest.land. 
      gastnr = res-line.gastnr. 
    END. 
    rmnite = (res-line.abreise - res-line.ankunft) * res-line.zimmeranz. 
    IF month(res-line.ankunft) = month(fdate) THEN 
    DO: 
      res-tacancel.mnite = res-tacancel.mnite + rmnite. 
      res-tacancel.mtu = res-tacancel.mtu + rmnite * res-line.zipreis. 
      t-mnite = t-mnite + rmnite. 
      t-mtu = t-mtu + rmnite * res-line.zipreis. 
    END. 
    res-tacancel.ynite = res-tacancel.ynite + rmnite. 
    res-tacancel.ytu = res-tacancel.ytu + rmnite * res-line.zipreis. 
    t-ynite = t-ynite + rmnite. 
    t-ytu = t-ytu + rmnite * res-line.zipreis. 
  END. 
 
  FOR EACH res-tacancel: 
    IF t-mnite NE 0 THEN 
    DO: 
      res-tacancel.pmnite = res-tacancel.mnite / t-mnite * 100. 
      res-tacancel.pmtu = res-tacancel.mtu / t-mtu * 100. 
    END. 
    IF t-ynite NE 0 THEN 
    DO: 
      res-tacancel.pynite = res-tacancel.ynite / t-ynite * 100. 
      res-tacancel.pytu = res-tacancel.ytu / t-ytu * 100. 
    END. 
  END. 
END. 
 
PROCEDURE disp-noshow1: 
DEFINE VARIABLE gastnr AS INTEGER INITIAL 0. 
DEFINE VARIABLE rmnite AS INTEGER. 
DEFINE VARIABLE bdate AS DATE. 
 
  /*ENABLE b1 WITH FRAME frame1. 
  DISP fdate fname tname WITH FRAME frame1. */
 
  FOR EACH res-tacancel: 
    delete res-tacancel. 
  END. 
 
  bdate = DATE(1, 1, year(fdate)). 
  t-mnite = 0. 
  t-mtu = 0. 
  t-ynite = 0. 
  t-ytu = 0. 
  IF sorttype = 1 THEN 
  FOR EACH res-line WHERE active-flag = 2 
    AND resstatus = 9 AND res-line.cancelled GE bdate 
    AND res-line.cancelled LE fdate 
    AND res-line.resname GE fname AND res-line.resname LE tname 
    AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
    FIRST guest WHERE guest.gastnr = res-line.gastnr 
    AND guest.karteityp = 2 NO-LOCK, 
    FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK 
    BY res-line.resname BY res-line.cancelled BY res-line.name: 
    FIND FIRST res-tacancel WHERE res-tacancel.resnr = res-line.resnr NO-ERROR. 
    IF NOT AVAILABLE res-tacancel THEN 
    DO: 
      create res-tacancel. 
      res-tacancel.resnr = res-line.resnr. 
      res-tacancel.name = guest.name + ", " + guest.anredefirma. 
      res-tacancel.wohnort = guest.wohnort + " " + STRING(guest.plz) 
        + " - " + guest.land. 
      gastnr = res-line.gastnr. 
    END. 
    rmnite = (res-line.abreise - res-line.ankunft) * res-line.zimmeranz. 
    IF month(res-line.cancelled) = month(fdate) THEN 
    DO: 
      res-tacancel.mnite = res-tacancel.mnite + rmnite. 
      res-tacancel.mtu = res-tacancel.mtu + rmnite * res-line.zipreis. 
      t-mnite = t-mnite + rmnite. 
      t-mtu = t-mtu + rmnite * res-line.zipreis. 
    END. 
    res-tacancel.ynite = res-tacancel.ynite + rmnite. 
    res-tacancel.ytu = res-tacancel.ytu + rmnite * res-line.zipreis. 
    t-ynite = t-ynite + rmnite. 
    t-ytu = t-ytu + rmnite * res-line.zipreis. 
  END. 
  ELSE 
  FOR EACH res-line WHERE active-flag = 2 
    AND resstatus = 9 AND res-line.cancelled GE bdate 
    AND res-line.cancelled LE fdate 
    AND res-line.resname GE fname AND res-line.resname LE tname 
    AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
    FIRST guest WHERE guest.gastnr = res-line.gastnr 
    AND guest.karteityp = 1 NO-LOCK, 
    FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK 
    BY res-line.resname BY res-line.cancelled BY res-line.name: 
    FIND FIRST res-tacancel WHERE res-tacancel.resnr = res-line.resnr NO-ERROR. 
    IF NOT AVAILABLE res-tacancel THEN 
    DO: 
      create res-tacancel. 
      res-tacancel.resnr = res-line.resnr. 
      res-tacancel.name = guest.name + ", " + guest.anredefirma. 
      res-tacancel.wohnort = guest.wohnort + " " + STRING(guest.plz) 
        + " - " + guest.land. 
      gastnr = res-line.gastnr. 
    END. 
    rmnite = (res-line.abreise - res-line.ankunft) * res-line.zimmeranz. 
    IF month(res-line.cancelled) = month(fdate) THEN 
    DO: 
      res-tacancel.mnite = res-tacancel.mnite + rmnite. 
      res-tacancel.mtu = res-tacancel.mtu + rmnite * res-line.zipreis. 
      t-mnite = t-mnite + rmnite. 
      t-mtu = t-mtu + rmnite * res-line.zipreis. 
    END. 
    res-tacancel.ynite = res-tacancel.ynite + rmnite. 
    res-tacancel.ytu = res-tacancel.ytu + rmnite * res-line.zipreis. 
    t-ynite = t-ynite + rmnite. 
    t-ytu = t-ytu + rmnite * res-line.zipreis. 
  END. 
 
  FOR EACH res-tacancel: 
    IF t-mnite NE 0 THEN 
    DO: 
      res-tacancel.pmnite = res-tacancel.mnite / t-mnite * 100. 
      res-tacancel.pmtu = res-tacancel.mtu / t-mtu * 100. 
    END. 
    IF t-ynite NE 0 THEN 
    DO: 
      res-tacancel.pynite = res-tacancel.ynite / t-ynite * 100. 
      res-tacancel.pytu = res-tacancel.ytu / t-ytu * 100. 
    END. 
  END. 
END. 

