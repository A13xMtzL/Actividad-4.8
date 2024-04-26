import datetime
import numpy as np
import pandas as pd

def generate_client(
  num_client, prev_arrival_time, prev_service_end, max_arrival_time, max_service_time
):
  
  inter_arrival_time = np.random.randint(1, max_arrival_time+1)
  arrival_time = prev_arrival_time + datetime.timedelta(minutes=inter_arrival_time)
  
  service_time = np.random.randint(1, max_service_time+1)
  service_start = max(arrival_time, prev_service_end)
  service_end = service_start + datetime.timedelta(minutes=service_time)

  client_wait_time = max(0, (service_start - arrival_time).total_seconds() / 60)
  atm_inactive_time = max(0, (arrival_time - prev_service_end).total_seconds() / 60)

  return {
    "Cliente": num_client,
    "Tiempo entre llegadas": inter_arrival_time,
    "Hora llegada": arrival_time.strftime("%I:%M %p").lstrip("0"),
    "Tiempo del trámite": service_time,
    "Inicia servicio": service_start.strftime("%I:%M %p").lstrip("0"),
    "Termina Servicio": service_end.strftime("%I:%M %p").lstrip("0"),
    "Tiempo de espera cliente": client_wait_time,
    "Tiempo inactividad del ATM": atm_inactive_time,
    "service_end": service_end,
    "arrival_time": arrival_time,
  }


def generate_clients(
  num_clients, max_arrival_time, max_service_time
):
  clients = []
  t = datetime.datetime.now()
  prev_arrival_time = t
  prev_service_end = t

  for i in range(1, num_clients + 1):
    client = generate_client(i, prev_arrival_time, prev_service_end, max_arrival_time, max_service_time)
    clients.append(client)
    prev_arrival_time = client["arrival_time"]
    prev_service_end = client["service_end"]

  df = pd.DataFrame(clients)
  df = df.drop(columns=["service_end", "arrival_time"])
  return df


def calculate_stats(df):
  # Tiempo de espera promedio por cliente
  avg_wait_time = df["Tiempo de espera cliente"].mean()

  # Probabilidad de que un cliente espera en la fila
  prob_wait = (df["Tiempo de espera cliente"] > 0).mean()

  # Porcentaje de tiempo en que el ATM estuvo inactivo
  df["Termina Servicio"] = pd.to_datetime(df["Termina Servicio"])
  df["Hora llegada"] = pd.to_datetime(df["Hora llegada"])

  total_time = (df["Termina Servicio"].max() - df["Hora llegada"].min()).total_seconds() / 60
  total_inactive_time = df["Tiempo inactividad del ATM"].sum()
  percent_inactive = (total_inactive_time / total_time) * 100

  # Tiempo promedio de servicio
  avg_service_time = df["Tiempo del trámite"].mean()

  return avg_wait_time, prob_wait, percent_inactive, avg_service_time


import re
def write_report(
  df, filename, avg_wait_time, prob_wait, percent_inactive, avg_service_time
):
  number = re.search(r'\d+', filename)
  report_number = number.group() if number else ''
  
  with open(filename, 'w') as f:   
    f.write(f"------------------\n   Reporte {report_number}:\n------------------\n\n")

    f.write(df.to_string(index=False))
    f.write('\n\n')

    f.write("--------------------------------------------------\n")
    f.write(f"Tiempo de espera promedio por cliente: {avg_wait_time:.2f} minutos\n")
    f.write(f"Probabilidad de que un cliente espera en la fila: {prob_wait * 100:.3f}%\n")
    f.write(f"Porcentaje de tiempo en que el ATM estuvo inactivo: {percent_inactive:.3f}%\n")
    f.write(f"Tiempo promedio de servicio: {avg_service_time:.2f} minutos\n")
    f.write("--------------------------------------------------\n")
  


# Función Principal
num_clients = 18  # Se cambia por el usuario
max_arrival_time = 12  # Se cambia por el usuario
max_service_time = 15  # Se cambia por el usuario

df = generate_clients(num_clients, max_arrival_time, max_service_time)
avg_wait_time, prob_wait, percent_inactive, avg_service_time = calculate_stats(df)

# Convert to datetime format and then format as 'HH:MM'
df['Hora llegada'] = pd.to_datetime(df['Hora llegada']).dt.strftime('%H:%M')
df['Inicia servicio'] = pd.to_datetime(df['Inicia servicio']).dt.strftime('%H:%M')
df['Termina Servicio'] = pd.to_datetime(df['Termina Servicio']).dt.strftime('%H:%M')

write_report(df, 'report03.txt', avg_wait_time, prob_wait, percent_inactive, avg_service_time)


# Impresión de los reportes generados
for i in range(1, 4):
    with open(f"report0{i}.txt", "r") as file:
        for line in file:
            print(line, end="")
        print("\n\n")
