from django.shortcuts import render, redirect
from  NetworkBackend.models import Train, Station, Cursa, Stop
import datetime

def search(request):
    if request.method == 'POST':
        plecare = request.POST.get('departure', '').strip()
        destinație = request.POST.get('arrival', '').strip()
        data_string = request.POST.get('date', '')
        
        opriri_plecare = Stop.objects.filter(station__city__icontains=plecare, cursa__date=data_string)
        opriri_destinație = Stop.objects.filter(station__city__icontains=destinație, cursa__date=data_string)

        # --- COD DE DIAGNOSTICARE (Afișează în terminal) ---
        print("--- START DEBUG CĂUTARE ---")
        print(f"Data căutată: {data_string}")
        print(f"Plecare '{plecare}': a găsit {opriri_plecare.count()} opriri")
        print(f"Destinație '{destinație}': a găsit {opriri_destinație.count()} opriri")

        dict_plecare = {oprire.cursa.id: oprire for oprire in opriri_plecare}
        dict_destinație = {oprire.cursa.id: oprire for oprire in opriri_destinație}
        
        intersectii = dict_plecare.keys() & dict_destinație.keys()
        print(f"Trenuri comune (Intersecții): {len(intersectii)}")
        print("--- END DEBUG ---")

        rezultate = []

        for cursa_id in dict_plecare.keys() & dict_destinație.keys():
            oprire_plecare = dict_plecare[cursa_id]
            oprire_destinație = dict_destinație[cursa_id]
            
            if oprire_plecare.sequence_number < oprire_destinație.sequence_number:
                
                # --- CALCUL DURATĂ ---
                dep_time = oprire_plecare.departure_time
                arr_time = oprire_destinație.arrival_time
                durata_str = "-"
                
                if dep_time and arr_time:
                    # Combinăm cu data de azi doar pentru a putea face scăderea matematică
                    dt_plecare = datetime.datetime.combine(datetime.date.today(), dep_time)
                    dt_sosire = datetime.datetime.combine(datetime.date.today(), arr_time)
                    
                    # Dacă trenul ajunge a doua zi (după miezul nopții)
                    if dt_sosire < dt_plecare:
                        dt_sosire += datetime.timedelta(days=1)
                        
                    durata = dt_sosire - dt_plecare
                    ore, rest = divmod(durata.seconds, 3600)
                    minute = rest // 60
                    durata_str = f"{ore} ore {minute} min" if ore > 0 else f"{minute} min"


                    rezultate.append({
                        'train_number': oprire_plecare.cursa.train.train_number,
                        'train_type': oprire_plecare.cursa.train.train_type,
                        'duration': durata_str,
                        'company': oprire_plecare.cursa.train.company,
                        'departure_station': oprire_plecare.station.name,
                        'departure_time': oprire_plecare.departure_time,
                        'arrival_station': oprire_destinație.station.name,
                        'arrival_time': oprire_destinație.arrival_time,
                    })
        
        # Sortează rezultatele în funcție de ora plecării (opțional, dar foarte util pentru utilizator)
        rezultate = sorted(rezultate, key=lambda k: k['departure_time'] if k['departure_time'] else datetime.time.max)

        return render(request, 'results.html', {'rezultate': rezultate, 'data': data_string, 'plecare': plecare, 'destinație': destinație} )
    orase = Station.objects.values_list('city', flat=True).distinct().order_by('city')
    return render(request, 'search.html', {'orase': orase})