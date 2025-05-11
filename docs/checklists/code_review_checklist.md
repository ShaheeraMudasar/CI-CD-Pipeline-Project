# Kodgransknings­checklista

Denna checklista används av **granskaren** när du går igenom en PR. Gå igenom alla punkter och lämna en kommentar om något saknas.

För alla kommenterar du ger, utgå från följande principer:

- **Konstruktiv feedback**: Kommentar ska vara användbar och hjälpsam.
- **Pedagogisk fokus**: Kommentarer ska hjälpa utvecklaren att lära sig och växa.
- **Empati och trygghet**: Kommentarerna ska formuleras så att utvecklaren efter denna granskning vågar visa sin kod och ställa frågor.
- **Tydlighet kring "varför"**: Lösningar och förslag ska utäver att vara tekniskt konkreta också förklara varför du föreslår det.

## Funktionalitet

- [ ] Koden implementerar den **funktionalitet som beskrivs tydligt i PR\:n eller issue**, inklusive referenser för kontext.
- [ ] Edge-cases och felaktig input hanteras tydligt, och beslut kring undantag är explicit dokumenterade.
- [ ] Felmeddelanden är **tydliga, empatiska och användbara** för användaren eller utvecklaren som felsöker.

## Kvalitet och läsbarhet

- [ ] Funktioner/metoder är **korta, fokuserade och gör en sak tydligt**.
- [ ] Namngivning av variabler, metoder och klasser är **självförklarande och kontextspecifika**.
- [ ] Duplicerad kod undviks genom **abstraktion och återanvändbara komponenter** snarare än ren kopiering.

## Tester och robusthet

- [ ] Ny logik täcks av **unit-tester som är pedagogiska**, hjälper andra utvecklare att förstå avsikten med koden.
- [ ] Tester är **snabba, stabila och tydliga**, utan beroenden på instabila externa resurser.
- [ ] Lämpliga integrationstester är tydliga, enkla att förstå, och **ger vägledning** vid fel.

## Prestanda och säkerhet

- [ ] Koden optimerar resursanvändning (inga onödiga anrop).
- [ ] Säkerhet är en tydlig prioritet: input är alltid **validerad och sanerad**.
- [ ] Känsliga konfigurationsvärden (secrets) är aldrig hårdkodade, utan **hanteras konsekvent** med konfigurationsfiler eller secrets-hantering.

## Stil och konventioner

- [ ] Koden följer den överenskomna kodstandarden **utan undantag**.
- [ ] Typanvisningar och kommentarer används där de ger **klart pedagogiskt värde**, inte bara för formalitetens skull.
- [ ] Katalogstruktur och filnamn är **logiska och intuitiva**, och följer tydligt projektets övergripande struktur.

## Dokumentation och kommentarer

- [ ] Publika funktioner och klasser har docstrings som tydligt beskriver **"varför"**, inte bara "vad" eller "hur".
- [ ] Komplex logik är kommenterad för att hjälpa utvecklare förstå **avsikten och resonemangen bakom lösningen**.
- [ ] README eller dokumentation uppdateras med **kontextuell information** som gör det enklare att ta beslut och förstå ändringar i framtiden.

## CI/CD och automatisering

- [ ] PR\:ns automatiska kontroller (lint, test, etc) är gröna och hjälper aktivt till att upptäcka problem tidigt.
- [ ] Branch-skydd används för att säkerställa en **säker och pålitlig kodintegration**.

## Mänskliga aspekter

- [ ] Mina kommentarer är **konstruktiva, empatiska och ger förbättringsförslag**, snarare än kritik utan förslag.
- [ ] Tonen i mina kommentarerna uppmuntrar till lärande och gör det lättare för författaren att ta till sig feedbacken.
- [ ] Det finns utrymme för diskussion kring beslut och **det är okej att ställa frågor eller invända**.
