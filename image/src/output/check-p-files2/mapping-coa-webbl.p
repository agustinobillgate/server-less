  DEF TEMP-TABLE coa-list
    FIELD old-fibu AS CHAR FORMAT "x(12)"
    FIELD new-fibu AS CHAR FORMAT "x(12)"
    FIELD bezeich AS CHAR FORMAT "x(48)"  /**/
    FIELD coaStat  AS INTEGER INITIAL -1
    FIELD old-main AS INTEGER
    FIELD new-main AS INTEGER
    FIELD bezeichM AS CHAR
    FIELD old-dept AS INTEGER
    FIELD new-dept AS INTEGER
    FIELD bezeichD AS CHAR
    FIELD catno    AS INTEGER
    FIELD acct     AS INTEGER
    FIELD old-acct AS INTEGER
    INDEX coa-ix old-fibu
.

  DEFINE INPUT PARAMETER TABLE FOR coa-list.


  RUN mapping-coa-1bl.p (INPUT TABLE coa-list).
  RUN mapping-coa-2bl.p (INPUT TABLE coa-list).
  RUN mapping-coa-3bl.p (INPUT TABLE coa-list).
  RUN mapping-coa-4bl.p (INPUT TABLE coa-list).
