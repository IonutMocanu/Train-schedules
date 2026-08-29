import xml.etree.ElementTree as ET
import datetime
from django.core.management.base import BaseCommand
from NetworkBackend.models import Train, Station, Cursa, Stop

class Command(BaseCommand):
    help = 'Importă datele reale CFR Călători și generează orarul pentru următoarele 7 zile'

    def sec_to_time(self, seconds_str):
        """Transformă secundele de la miezul nopții în format orar HH:MM:SS"""
        if not seconds_str:
            return None
        sec = int(seconds_str)
        sec = sec % 86400 
        m, s = divmod(sec, 60)
        h, m = divmod(m, 60)
        return datetime.time(h, m, s)

    def curata_nume_oras(self, nume_gara):
        oras = nume_gara
        sufixe = [' hc.', ' Hm.', ' h.', ' Nord', ' Sud', ' Est', ' Vest', ' Ramificaţia']
        for sufix in sufixe:
            oras = oras.replace(sufix, '')
        return oras.strip()

    def handle(self, *args, **kwargs):
        file_path = 'date_cfr.xml' 

        try:
            self.stdout.write("Începe citirea fișierului XML...")
            tree = ET.parse(file_path)
            root = tree.getroot()
            count_opriri = 0
            
            # Generăm orarul pentru ziua de azi + următoarele 6 zile
            zile_de_generat = [datetime.datetime.today().date() + datetime.timedelta(days=x) for x in range(7)]

            for tren in root.findall('.//Tren'):
                nr_tren = tren.get('Numar')
                categorie = tren.get('CategorieTren') 
                
                # 1. Salvăm Trenul (e entitate statică, se face o singură dată)
                train_obj, _ = Train.objects.get_or_create(
                    train_number=nr_tren,
                    defaults={'company': 'CFR Călători', 'train_type': categorie}
                )

                # Pre-extragem elementele trasei ca să nu le citim din XML de 7 ori
                trase_elements = tren.findall('.//ElementTrasa')

                # Pentru fiecare zi din cele 7, creăm cursa și opririle
                for data_curenta in zile_de_generat:
                    # 2. Creăm Cursa pentru această zi anume
                    cursa_obj, _ = Cursa.objects.get_or_create(
                        train=train_obj,
                        date=data_curenta,
                        defaults={'status': 'Activ'}
                    )

                    prev_ora_s = None 
                    
                    for i, trasa in enumerate(trase_elements):
                        nume_gara = trasa.get('DenStaOrigine')
                        ora_p_sec = trasa.get('OraP') 
                        ora_s_sec = trasa.get('OraS') 
                        secventa = int(trasa.get('Secventa'))

                        nume_oras_curatat = self.curata_nume_oras(nume_gara)

                        # 3. Gara (get_or_create se asigură că nu o dublăm în zile diferite)
                        station_obj, _ = Station.objects.get_or_create(
                            name=nume_gara,
                            defaults={
                                'city': nume_oras_curatat, 
                                'longitude': 0.0, 
                                'latitude': 0.0
                            }
                        )

                        arr_time = self.sec_to_time(prev_ora_s) if i > 0 else None
                        dep_time = self.sec_to_time(ora_p_sec)
                        
                        is_last_station = (i == len(trase_elements) - 1)
                        if is_last_station:
                            arr_time = self.sec_to_time(ora_s_sec)
                            dep_time = None 
                        
                        # 4. Salvăm oprirea atașată la cursa DE AZI
                        Stop.objects.update_or_create(
                            cursa=cursa_obj,
                            sequence_number=secventa,
                            defaults={
                                'station': station_obj,
                                'arrival_time': arr_time,
                                'departure_time': dep_time,
                                'delay_minutes': 0
                            }
                        )
                        
                        prev_ora_s = ora_s_sec 
                        count_opriri += 1

            self.stdout.write(self.style.SUCCESS(f'SUCCES! Au fost importate {count_opriri} opriri pentru următoarele 7 zile!'))

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'Fișierul {file_path} nu a fost găsit!'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'A apărut o eroare: {str(e)}'))