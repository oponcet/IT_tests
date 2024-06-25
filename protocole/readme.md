# Setup CROC 


- Turn on the FC7 and the fan (multiprise a droite du frigo). Les led doivent clignoter.

- Turn on sbgat166.
- Connect to xtaldad account with the pwd.
- Open a terminal 
```
sudo ./startRarpd.sh
```
Output should be:
```
[sudo] Mot de passe de xtaldaq rarpd [23869] : rarpd: listening on enp3s0
Scanning /etc/ethers..
>> 08:00:30:00:22:83
192.168.0.122
Found 192.168.0.122.
rarpd[23869]: rarp who is 8:0:30:0:22:83 tell 3:0:30:0:22:83 answer 192.168.0.122
```
- Let this run, open a new tab and run
```
ping 192.168.0.122
```
Ouput should be 
```
PING 192.168.0.122 (192.168.0.122) 56(84) octets de données.
64 octets de 192.168.0.122 : icmp_seq=1 ttl-64 temps-0.191 ms
```
The connexion is etablished ! 

- Load the firmware on FMC7

```
cd IT_test/Ph2_ACF
source setuph.sh
fpgaconfig -c settings/CMSIT_RD53A.xml -i IT-uDTC_L12_KSU_CROC.bit 
```

- The firmware is ready on the FMC7. Now it's time to connect the chip.

- Penser à se mettre à la masse avec le bracelet.

- Mettre la CROC sur son support et pas directement sur la paroi du congèle. Brancher les cables comme sur la photo. Ainsi que la pince croco sur le support pour mettre la CROC à la masse (si le support est conducteur).

- Vérifier le fonctionnement des sondes sur : http://sbgpcs76:8086/orgs/05acd015717e3072/dashboards/09491c2ff2c7b000?lower=now%28%29%20-%2012h

- Allumer les petits ventilateurs 12V. 

- Fermer le frigo avec le scotch et descendre en air sec en mettant un débit de 50L/min

- Attendre d'atteindre 2-3%

- Allumer le frigo en mode "super" et descendre l'air sec à pas moin de 10L/min. La temperatrue du frigo devrait se stabilise autour de -25°C minimum  et l'humidité relative autour de 10%. On doit etre au dessus du dew point.

- Une fois la température atteinte, on peut allumer la CROC. :warning: :warning: On allume le LV avant le HV.

- Allumer le LV de la CROC selon les recommandation : 1.8 V and max current output 1.5 A 

- Allumer le HV progressivement selon le cas
    - Non irradié : 20 V for a 3D module max compliance current 10uA.
    - Post irradiation : 100 V for a 3D module max compliance current 10uA.


- Etablir la connexion avec la FMC7:
    - Set up the xml file for Hardware description : https://croc-testing-user-guide.docs.cern.ch/Software/Configuration/
    ```
    SET IP
    CROC ID
    BoardType
    ```
    - Set up the Chip configuration (.toml) file https://docs.google.com/spreadsheets/d/1Gpl-JAMNmP0ptnrrdEOHit5j4pc7nAd4J_Z8solMxo8/edit#gid=1394811518
    - Each time a FW image is booted on the FC7 board :
    ```
    RD53BminiDAQ -f CMSIT_CROC.xml -r
    ```
Follow the instruction of standard calibration : 
- https://www.overleaf.com/project/645509df6974e43cab141f26
- or in the google sheet: https://docs.google.com/document/d/1g8dkvUHCYAr9CzcT9leuKsN8csjxHXIOQ-76sBtNU8Q/edit


- When test are done turn off the HV then the LW. Turn off the fridge and increase the air flux to 50L/min.

- On peut ouvrir le frigo seulement quand on est au dessus du dew point de la pièce. Attention cette valeur est très souvent haute! Parfois 15°C!







