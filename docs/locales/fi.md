# Osoiteparseri

Tämä osoiteparseri tukee valideja nykymuotoisia suomalaisia osoitteita.

Esimerkin tapauksessa:
```
Iso Maantie 12b B 7
65220 Vaasa
```

| Osa              | Attribuutin nimi | Selite                                                                           | Esimerkin arvo | Muita mahdollisia arvoja |
| ---------------- | ---------------- | -------------------------------------------------------------------------------- | -------------- | ------------------------ |
| Osoitenimi       | street_name      | Tien, kadun tai aukion nimi tai muu sovittu nimi                                 | Iso Maantie    | Vasikkasaari             |
| Osoitenumero     | house_number     | Osoitenimeen liitettävä numero ja mahdollinen jakokirjain                        | 12b            | 7, 12-14                 |
| Porraskirjain    | entrance         | Porrashuoneen yksilöivä, osoitenumeroon liitettävä kirjain                       | B              | A, C                     |
| Huoneistonumero  | apartment        | Huoneiston yksilöivä numero ja mahdollinen jakokirjain                           | 7              | 1, 12a                   |
| Postilokero      | post_office_box  | Postinlajittelussa käytetty tunnus, jolla posti jaellaan asiakkaan postilokeroon |                | PL154                    |
| Postinumero      | zip_number       | Postinlajittelussa käytetty numeromuotoinen aluetunnus                           | 65220          | 02200, 65100             |
| Postitoimipaikka | zip_name         | Postinlajittelussa käytetty lajittelualueen nimi                                 | Vaasa          | Espoo                    |
