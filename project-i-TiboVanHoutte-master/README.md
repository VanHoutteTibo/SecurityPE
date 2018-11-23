Manual

Stop de adapter van de Raspberry Pi en de motor in het stopcontact.
Het duurt even voor de Raspberry Pi is opgestart.(~100s)

Surf naar het ip van de Pi en voeg :5000 toe aan het einde van het ip. (Geen statisch ip dus moet op voorhand gekend zijn. Dit kan door een sniffer of een ssh verbinding te maken.)

Start een nieuw spel.
Geef de namen van de spelers in. Je moet de voornaam en achternaam invullen. Het spel kan met 1 speler gespeeld worden.
Via start ga je naar de pagina van het spel zelf.

Voor je kan beginnen moet je eerst ongeveer 5 seconden wachten tot de verbinding tussen de Pi en de website voor de live data is opgezet.
Je krijgt een melding wanneer je kan beginnen.
Om de aan de draaischijf te draaien ga je met een voet of een hand over de sensor op de behuizing.
Wanneer de motor stopt met draaien, komt de zet op de website.
Voer de zet uit en ga weer over de sensor om naar de volgende ronde te gaan.

Wanneer iemand afvalt moet zijn of haar naam aangeklikt worden op de website.
De laatste die overblijft is gewonnen.

In het tablad historiek zijn alle winnaars van de voorbije spellen te zien.
Op de about page staan de instructies in het kort en een link naar mijn portfolio.

Mogelijke bug: Tijdens het spelen beginnen bijna alle bollen op te lichten. Dit is een probleem met de live data verbinding. De oplossing hiervoor is de service waarin het programma draait heropstarten via ssh.
