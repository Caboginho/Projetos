from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Configuração do Google Sheets
def setup_google_sheets():
    # Escopo necessário para acesso ao Google Sheets e Drive
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    
    # Substitua 'credentials.json' pelo nome correto do arquivo, caso tenha outro nome
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    
    # Autoriza o cliente do Google Sheets
    client = gspread.authorize(creds)
    
    # Abre a primeira aba da planilha
    sheet = client.open("IrrigationData").sheet1  
    return sheet

# Função para atualizar os dados no Google Sheets
def update_google_sheets(sheet, Argumentos, maximo, minimo):   
    DataHora = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    #atualiza sem salvar
    #ultimos vaslores
    sheet.update_cell(2, 1, str(DataHora))
    sheet.update_cell(2, 2, str(Argumentos))
    #Maximos e Minimos
    sheet.update_cell(4, 1, str(maximo))
    sheet.update_cell(4, 2, str(minimo))
    #Atualiza e salva
    sheet.append_row([DataHora,Argumentos])
    #sheet.append_row([DataHora, Argumentos])
    print(f"Dados enviados: {DataHora}, {Argumentos},{str(maximo)},{str(minimo)}")
# Configuração do Selenium
def setup_selenium(url):
    driver = webdriver.Chrome()  # Substitua por webdriver.Firefox() se usar o Firefox
    driver.get(url)
    return driver
# Monitoramento e atualização dos dados
def monitor_and_update(xpath, url, interval_ms=1000):
    # Configurações
    sheet = setup_google_sheets()
    driver = setup_selenium(url)
    ValorAntigo = None
    maximo = None
    minimo = None
    minU = 1000.0
    maxU = -1000.0
    minT = 1000.0
    maxT = -1000.0
    try:    
        while True:
            try:
                # Captura o elemento pelo XPath e lê o texto
                element = driver.find_element(By.XPATH, xpath)
                current_value = element.text.strip()  # Remove espaços em branco
                value = current_value[-11:]
                # Atualiza o Google Sheets apenas para novos valores
                if  value != ValorAntigo :
                    p1 = value[-5:]
                    p2 = value[:5]       
                    if ValorAntigo != None:                    
                        if float(p1)<= minU:
                            minU = float(p1)
                        if float(p2)<= minT:
                            minT = float(p2)
                        if float(p1)>= maxU:
                            maxU = float(p1)
                        if float(p2)>= maxT:
                            maxT = float(p2)
                        maximo = str("minU: " + str(minU) + '%' +'\n' + "minT: " + str(minT) + 'c°')
                        minimo = str("maxU: " + str(maxU) + '%' +'\n' + "maxT: " + str(maxT) + 'c°')
                    else:
                        maximo = p1
                        minimo = p2                  
                    ValorAntigo = value
                    value = str("Umidade: " + p1 + '%' + '\n' + "Temperatura: " + p2 + 'c°')
                    update_google_sheets(sheet, value, maximo,minimo)   
            except Exception as e:
                print(f"Erro ao ler o valor: {e}")
            time.sleep(interval_ms / 1000.0)  # Intervalo entre as verificações
    except KeyboardInterrupt:
        print("Monitoramento encerrado.")
    finally:
        driver.quit()

# Configurações do programa
url = "https://wokwi.com/projects/415541390577662977"
xpath = '//*[@id="simple-tabpanel-0"]/div/div[1]/pre'
monitor_and_update(xpath, url)
