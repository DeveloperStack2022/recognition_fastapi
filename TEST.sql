-- Query Numero 1
$query1 = SELECT date_format(datepresentation, '%Y-%m-%d') as datepresentation FROM reclutamiento.rcl_note note JOIN reclutamiento.rcl_exam exam ON note.exam_id = exam.id AND exam.exam_type_id = 1 where inscription_id = 862--

-- Query Numero 2 
-- DISTINCT -> 'Selecioaname registros distintos' 
$query2 = SELECT DISTINCT concat(lastname1,' ',lastname2) as apellidos, firstnames as nombres, identitynumber as cedula,iddactiloscopica,email, c.id, c.dob FROM rcl_citizen c, rcl_note n WHERE c.id = $query1 and n.summon_id = 17-- and c.id = n.citizen_id



-- Query Total 
SELECT id FROM reclutamiento.rcl_inscription where citizen_id = $query1 and summon_id = $query2

-- Query Total 
SELECT DISTINCT concat(lastname1,' ',lastname2) as apellidos, firstnames as nombres, identitynumber as cedula,iddactiloscopica,email, c.id, c.dob FROM rcl_citizen c, rcl_note n WHERE c.id = 862-- and n.summon_id = 17-- and c.id = n.citizen_id

-- https://reclutamiento.policia.gob.ec/reclutamiento3/forms/pdf_Control_Confianza.php?ida=862--&ids=17--
