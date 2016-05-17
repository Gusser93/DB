select tmp.MatrNr, tmp.Name, tmp.VorlAnzahl
from ( 	select s.MatrNr, s.Name, count(*) as VorlAnzahl
			from Studenten s, hören h
			where s.MatrNr = h.MatrNr
			group by s.MatrNr, s.Name) tmp
where tmp.VorlAnzahl > 2;