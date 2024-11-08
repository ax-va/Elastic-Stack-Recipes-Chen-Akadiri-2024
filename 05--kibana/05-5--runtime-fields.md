# Runtime fields

A *runtime field* is used to include a field derived from the values of other fields
so that the index schema can be defined and enriched at runtime without altering your source data.

**Kibana** -> **Analytics** -> **Discover** -> Select a data view -> **Add a field** (at the bottom of the left panel)

**Type**: Keyword

**Set value**: On

Write code in the *Painless* scripting language like this

```painless
ZonedDateTime date = doc['@timestamp'].value;
ZonedDateTime cet = date.withZoneSameInstant(ZoneId.of('Europe/Paris'));
int hour = cet.getHour();
if (hour < 10) {
    emit ('0' + String.valueOf(hour));
} else {
    emit (String.valueOf(hour));
}
```

-> 

**Save**