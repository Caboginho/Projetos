App DW Moodle - Pacote de Distribuição

Conteúdo:
- app_dw_moodle.py      (script principal)
- app_dw_moodle.spec    (PyInstaller SPEC)
- .env                  (configurações de banco)
- README.txt            (instruções)

Execute:
1. pip install pyinstaller python-dotenv mysql-connector-python matplotlib numpy
2. pyinstaller app_dw_moodle.spec
3. dist/app_dw_moodle/app_dw_moodle.exe

Para executar o script:

 - executar xampp server/mySql: 3306
 - tabela "educacional" deve ser o nome da tablea disponibilizada
 - ecutar app_dw_moodle.py

Dependencias:

 - tkinter
 - mysql.connector
 - matplotlib.pyplot
 - numpy
 - dotenv 
 - os
