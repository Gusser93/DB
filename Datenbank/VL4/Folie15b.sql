select gelesenVon, sum (SWS)
from Vorlesungen
group by gelesenVon;