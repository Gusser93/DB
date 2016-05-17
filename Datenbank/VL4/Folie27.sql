select h.VorlNr, h.AnzProVorl, g.GesamtAnz, cast(h.AnzProVorl as float) / g.GesamtAnz as Marktanteil
from ( 	select VorlNr, count(*) as AnzProVorl
			from hören
			group by VorlNr) h,
			( select count(*) as GesamtAnz
			from Studenten) g;