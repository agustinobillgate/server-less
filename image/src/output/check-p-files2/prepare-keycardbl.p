
DEF OUTPUT PARAMETER ci-date             AS DATE.
DEF OUTPUT PARAMETER finTimeTo           AS CHAR.
DEF OUTPUT PARAMETER t-ch-gvCCardProgram AS CHAR.

RUN htpdate.p (87,  OUTPUT ci-date).
RUN htpchar.p (925, OUTPUT finTimeTo).
RUN htpchar.p (921, OUTPUT t-ch-gvCCardProgram).
