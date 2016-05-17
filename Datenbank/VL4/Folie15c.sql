select gelesenVon, Name, sum(SWS)
from Vorlesungen, Professoren
where gelesenVon = PersNr and Rang = 'C4'
group by 	gelesenVon, Name
				having avg(SWS) >= 3;