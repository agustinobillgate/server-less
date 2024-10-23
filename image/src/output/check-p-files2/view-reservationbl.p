
DEFINE TEMP-TABLE s-list 
  FIELD flag AS INTEGER INITIAL 0 
  FIELD pos AS INTEGER INITIAL 0 
  FIELD s-ankunft AS CHAR FORMAT "x(8)" LABEL " Arrival" 
  FIELD ankunft AS DATE LABEL "Arrival" 
  FIELD abreise AS DATE LABEL "Departure" INITIAL ? 
  FIELD rmcat AS CHAR FORMAT "x(6)" LABEL "RmCat" 
  FIELD zimmeranz AS INTEGER FORMAT ">>>" LABEL "Qty" 
  FIELD erwachs AS INTEGER FORMAT ">>>" LABEL "Adult" 
  FIELD gratis AS INTEGER FORMAT ">>>" LABEL "Com" 
  FIELD kind1 AS INTEGER FORMAT ">>>" LABEL "Ch1" 
  FIELD kind2 AS INTEGER FORMAT ">>>" LABEL "Ch2" 
  FIELD STR AS CHAR FORMAT "x(68)". 
 
 
DEFINE INPUT  PARAMETER     resnr       AS INTEGER.
DEFINE OUTPUT PARAMETER     tot-pax     AS INTEGER.
DEFINE OUTPUT PARAMETER     tot-com     AS INTEGER.
DEFINE OUTPUT PARAMETER     tot-ch1     AS INTEGER.
DEFINE OUTPUT PARAMETER     tot-ch2     AS INTEGER.
DEFINE OUTPUT PARAMETER     tot-rm      AS INTEGER.
DEFINE OUTPUT PARAMETER     do-it1      AS LOGICAL INIT NO.
DEFINE OUTPUT PARAMETER TABLE FOR s-list.

 
RUN cal-revenue. 
 
/************************  PROCEDURE  ***************************/ 
 
PROCEDURE cal-revenue: 
DEFINE buffer s1-list FOR s-list. 
DEFINE VARIABLE pos AS INTEGER INITIAL 0. 
DEFINE VARIABLE l-ankunft AS DATE INITIAL ?. 
DEFINE VARIABLE l-abreise AS DATE INITIAL ?. 
DEFINE VARIABLE l-rmcat AS CHAR INITIAL "". 
DEFINE VARIABLE do-it AS LOGICAL INITIAL NO. 
DEFINE VARIABLE t-qty AS INTEGER INITIAL 0. 
DEFINE VARIABLE t-pax AS INTEGER INITIAL 0. 
DEFINE VARIABLE t-ch1 AS INTEGER INITIAL 0. 
DEFINE VARIABLE t-ch2 AS INTEGER INITIAL 0. 
  FOR EACH s-list: 
    delete s-list. 
  END. 
  FOR EACH res-line WHERE res-line.resnr = resnr AND res-line.active-flag LE 1 
    AND res-line.resstatus NE 12 NO-LOCK BY res-line.zikatnr 
    BY res-line.ankunft BY res-line.abreise BY res-line.resstatus: 
    FIND FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK. 
    FIND FIRST s-list WHERE s-list.flag = 0 AND s-list.rmcat = zimkateg.kurzbez 
      AND s-list.ankunft = res-line.ankunft AND s-list.abreise = res-line.abreise 
      AND s-list.erwachs = res-line.erwachs AND s-list.gratis = res-line.gratis 
      AND s-list.kind1 = res-line.kind1 AND s-list.kind2 = res-line.kind2 
      NO-ERROR. 
    
    ASSIGN
      tot-pax = tot-pax + res-line.zimmeranz * res-line.erwachs
      tot-com = tot-com + res-line.zimmeranz * res-line.gratis
      tot-ch1 = tot-ch1 + res-line.zimmeranz * res-line.kind1
      tot-ch2 = tot-ch2 + res-line.zimmeranz * res-line.kind2.
    IF res-line.resstatus NE 11 AND res-line.resstatus NE 13 THEN
      tot-rm = tot-rm + res-line.zimmeranz.

    IF res-line.resstatus NE 11 AND res-line.resstatus NE 13 THEN
    IF NOT AVAILABLE s-list AND res-line.resstatus LE 6 THEN 
    DO: 
      pos = pos + 1. 
      create s-list. 
      s-list.pos = pos. 
      s-list.ankunft = res-line.ankunft. 
      s-list.s-ankunft = STRING(s-list.ankunft). 
      s-list.abreise = res-line.abreise. 
      s-list.rmcat = zimkateg.kurzbez. 
    END. 
    IF res-line.resstatus LE 6 AND AVAILABLE s-list THEN 
      s-list.zimmeranz = s-list.zimmeranz + res-line.zimmeranz. 
    t-pax = t-pax + (res-line.erwachs + res-line.gratis) * res-line.zimmeranz. 
    t-ch1 = t-ch1 + res-line.kind1 * res-line.zimmeranz. 
    t-ch2 = t-ch2 + res-line.kind2 * res-line.zimmeranz. 
    IF AVAILABLE s-list THEN 
    DO: 
      s-list.erwachs = res-line.erwachs. 
      s-list.gratis = res-line.gratis. 
      s-list.kind1 = res-line.kind1. 
      s-list.kind2 = res-line.kind2. 
    END. 
  END. 
 
  FOR EACH s-list: 
    IF l-ankunft = ? THEN 
    DO: 
      l-ankunft = s-list.ankunft. 
      l-abreise = s-list.abreise. 
      l-rmcat = s-list.rmcat. 
    END. 
    ELSE 
    DO: 
      IF l-ankunft = s-list.ankunft AND l-abreise = s-list.abreise 
        AND l-rmcat = s-list.rmcat THEN do-it = YES. 
      ELSE 
      DO: 
        l-ankunft = s-list.ankunft. 
        l-abreise = s-list.abreise. 
        l-rmcat = s-list.rmcat. 
      END. 
    END. 
  END. 
 
  IF NOT do-it THEN 
  DO: 
    /*OPEN QUERY q1 FOR EACH s-list NO-LOCK BY s-list.flag 
      BY s-list.rmcat BY s-list.ankunft BY s-list.pos. */
    do-it1 = YES.
    RETURN. 
  END. 
 
  create s-list. 
  pos = pos + 1. 
  s-list.pos = pos. 
  s-list.flag = 1. 
 
  create s-list. 
  pos = pos + 1. 
  s-list.pos = pos. 
  s-list.flag = 1. 
  s-list.s-ankunft = "SUMMARY". 
 
  FOR EACH s-list WHERE s-list.flag = 0 BY s-list.pos: 
    t-qty = t-qty + s-list.zimmeranz. 
    FIND FIRST s1-list WHERE s1-list.flag = 2 AND s1-list.rmcat = s-list.rmcat 
      AND s1-list.ankunft = s-list.ankunft AND s1-list.abreise = s-list.abreise 
      NO-ERROR. 
    IF NOT AVAILABLE s1-list THEN 
    DO: 
      pos = pos + 1. 
      create s1-list. 
      s1-list.pos = pos. 
      s1-list.flag = 2. 
      s1-list.ankunft = s-list.ankunft. 
      s1-list.s-ankunft = STRING(s1-list.ankunft). 
      s1-list.abreise = s-list.abreise. 
      s1-list.rmcat = s-list.rmcat. 
    END. 
    s1-list.zimmeranz = s1-list.zimmeranz + s-list.zimmeranz. 
  END. 
  pos = pos + 1. 
  create s1-list. 
  s1-list.pos = pos. 
  s1-list.flag = 2. 
  s1-list.s-ankunft = "TOT ROOM". 
  s1-list.zimmeranz = t-qty. 
  pos = pos + 1. 
  create s1-list. 
  s1-list.pos = pos. 
  s1-list.flag = 3. 
  s1-list.s-ankunft = "TOT PAX". 
  s1-list.zimmeranz = t-pax. 
  IF t-ch1 GT 0 THEN 
  DO: 
    pos = pos + 1. 
    create s1-list. 
    s1-list.pos = pos. 
    s1-list.flag = 4. 
    s1-list.s-ankunft = "TOT CH1". 
    s1-list.zimmeranz = t-ch1. 
  END. 
  IF t-ch2 GT 0 THEN 
  DO: 
    pos = pos + 1. 
    create s1-list. 
    s1-list.pos = pos. 
    s1-list.flag = 5. 
    s1-list.s-ankunft = "TOT CH2". 
    s1-list.zimmeranz = t-ch2. 
  END. 
 
  /*OPEN QUERY q1 FOR EACH s-list NO-LOCK BY s-list.flag 
     BY s-list.ankunft BY s-list.pos. */
END. 
