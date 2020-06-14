# CyberFraM
Dashboard realizzata in python come ipotesi di studio per l'applicazione del CyberSecurity Framework nazionale ad una piccola impresa

# Descrizione
CyberFraM sta per Cybersecurity Framework Monitoring, ed è una dashboard ([disponibile a questo link](https://cyberfram.herokuapp.com/)) che ho relizzato in python usando plotly e dash.  
La dashboard nasce dall'ipotesi di applicazione - ad una piccola organizzazione/impresa - del [Framework Nazionale per la CyberSecurity e la Data Protection](https://www.cybersecurityframework.it/) realizzato dal CIS Sapienza e dal Cini.  
Il framework, ispirato da quello del [NIST](https://www.nist.gov/cyberframework) e suddiviso in funzioni, categorie e sottocategorie, consiste sostanzialmente in un insieme di risultati e *guidelines* da implementare per gestire e mitigare correttamente il rischio cyber.  
Inoltre tale framework è opportunamente integrato dai controlli necessari per adempiere al GDPR in materia di protezione dei dati personali.  
Pertanto ho ipotizzato che una piccola impresa decida di implementare il framework e inizi quindi a fotografare lo stato attuale dei propri *security controls*. Una volta determinato il **profilo corrente**, ossia appunto l'insieme delle misure del framework che l'impresa ritiene già implementate (segnalando il relativo livello di maturità), si passa ad elaborare il **profilo target**, ovvero a selezionare quelle funzioni, categorie e sottocategorie ritenute necessarie ed applicabili al caso concreto per gestire adeguatamente il rischio cyber.  
Questa selezione, accompagnata dall'individuazione dei maggiori livelli di maturità a cui devono giungere le misure già implementate, porta al **profilo target**, ossia quello da raggiungere in un determinato arco di tempo.  
Stabiliti quindi i tempi ed i costi previsti/auspicati di implementazione delle varie misure (mediante la predisposizione di un gantt chart), occorrerà con il passare dei mesi monitorare l'andamento dell'implementazione, per verificare se i tempi vengono rispettati.  
Da qui l'idea della dashboard di monitoraggio interattiva e costantemente aggiornabile.  

# Il codice
Nel repository è presente l'app (CyberFraM.py), accompagnata dal file excel del framework (precedentemente elaborato con vari processi casuali) e dalla cartella «assets» nella quale è presente il file .css per lo stile dell'app.  
L'applicazione finale è ospitata su Heroku al link [https://cyberfram.herokuapp.com/](https://cyberfram.herokuapp.com/).  

# Autore
*Dario Brocato*
