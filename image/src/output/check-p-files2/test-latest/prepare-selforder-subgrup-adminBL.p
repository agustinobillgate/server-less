DEFINE TEMP-TABLE t-subgrp
  FIELD KEY           AS INTEGER
  FIELD subgrp-no     AS INTEGER
  FIELD subgrp        AS CHARACTER
  FIELD maingrp-no    AS INTEGER
  FIELD maingrp       AS CHARACTER
  FIELD dept          AS INTEGER
  FIELD dept-str      AS CHARACTER
  FIELD prior         AS INTEGER
.
DEFINE TEMP-TABLE t-maingrp LIKE queasy.

DEFINE TEMP-TABLE t-dept
    FIELD nr    AS INTEGER FORMAT   ">9"
    FIELD dept  AS CHARACTER FORMAT "x(30)".

DEFINE OUTPUT PARAMETER TABLE FOR t-subgrp.
DEFINE OUTPUT PARAMETER TABLE FOR t-maingrp.
DEFINE OUTPUT PARAMETER TABLE FOR t-dept.

DEFINE BUFFER buf-queasy FOR queasy.

FOR EACH wgrpdep NO-LOCK,
  FIRST hoteldpt WHERE hoteldpt.num EQ wgrpdep.departement NO-LOCK 
  BY departement BY wgrpdep.zknr:
  CREATE t-subgrp.
  ASSIGN
    t-subgrp.dept       = wgrpdep.departement
    t-subgrp.subgrp-no  = wgrpdep.zknr
    t-subgrp.subgrp     = wgrpdep.bezeich
    t-subgrp.prior      = wgrpdep.betriebsnr
    t-subgrp.dept-str   = hoteldpt.depart
  .

  FIND FIRST queasy WHERE queasy.KEY EQ 229 
    AND queasy.number1 EQ wgrpdep.zknr 
    AND queasy.number2 EQ wgrpdep.departement NO-LOCK NO-ERROR.
  IF AVAILABLE queasy THEN
  DO:
    ASSIGN
      t-subgrp.KEY        = queasy.KEY
      t-subgrp.maingrp-no = queasy.number3
    .

    FIND FIRST buf-queasy WHERE buf-queasy.KEY EQ 228
      AND buf-queasy.number1 EQ queasy.number3 NO-LOCK NO-ERROR.
    IF AVAILABLE buf-queasy THEN
    DO:
      t-subgrp.maingrp = buf-queasy.char1.
    END.
  END.
END.

FOR EACH queasy WHERE queasy.KEY = 228:
    CREATE t-maingrp.
    BUFFER-COPY queasy TO t-maingrp.
END.
FOR EACH hoteldpt WHERE hoteldpt.num GT 0 NO-LOCK:
    CREATE t-dept.
    ASSIGN
        t-dept.nr   = hoteldpt.num
        t-dept.dept = CAPS(hoteldpt.depart).
END.
