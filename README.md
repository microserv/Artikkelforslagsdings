# Artikkelforslagsdings
Foreslår artikler til brukeren basert på hvilke ord brukeren ønsker å finne.

python -m nltk.downloader stopwords


QUERY FRA SØKEFRONTEND TIL SØKESERVER:
curl -i -H "Content-Type: application/json" -X POST -d '{"Partial":true, "Query":"forskrifter om utdanninger "}' 127.0.0.1:8000

Sender for øyeblikket indeksforespørsler til 127.0.0.1:8001 

En separat testserver for indeks (som ikke gjør noe som helst annet enn å motta) `finnes i index_testserver'.


Format på input er en jsondict {'Partial': true|false, 'Query': str}
Der Partial er true dersom queriet er delvis ferdig, og man ønsker forslag til utfylling.

===

Format på output (til indeks) er en jsondict {'Partial': true|false, 'Query': str}
Med samme betydning, men queriet har blitt preprossesert, og er kun et komplett enkeltord, 
eller et delvis ord. 

Dersom queriet er et komplett ord, ønskes det returnert en liste over artikler der ordet forekommer.
Dersom queriet er et delvis ord, ønskes det returnert en liste over mulige utfyllinger.
