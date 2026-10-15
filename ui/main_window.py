from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel
from PySide6.QtCore import Qt
from api_client import ViaCepClient

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Busca CEP")
        self.resize(500,450)

        widget_central = QWidget()
        self.setCentralWidget(widget_central)
        layout_principal = QVBoxLayout()
        
        widget_central.setLayout(layout_principal)

        self.label_titulo = QLabel("Consulte seu CEP:")
        self.label_titulo.setObjectName("label_titulo")

        self.campo_cep = QLineEdit()
        self.campo_cep.setPlaceholderText("Ex: 30690-750")
        self.campo_cep.setObjectName("campo_cep")

        self.botao_buscar = QPushButton("Buscar")
        self.botao_buscar.setObjectName("botao_buscar")
        self.botao_limpar = QPushButton("Limpar")
        self.botao_limpar.setObjectName("botao_limpar")
        
        

        # O Qlabel para exibir os resultados
        self.label_resultado = QLabel("Os resultados aparecerão aqui.")
        self.label_resultado.setWordWrap(True)
        self.label_resultado.setAlignment(Qt.AlignTop)

        
        layout_principal.addWidget(self.label_titulo)
        layout_principal.addWidget(self.campo_cep)
        layout_principal.addWidget(self.botao_buscar)
        layout_principal.addWidget(self.botao_limpar)
        layout_principal.addWidget(self.label_resultado)
        layout_principal.addStretch()

        # Conectando o botao Colocando a função "onClick"
        self.botao_buscar.clicked.connect(self.executa_busca)
        self.botao_limpar.clicked.connect(self.limpa_campo)

        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f6fa;
            }
            QLabel#label_titulo {
                font-size: 18px; 
                font-weight: bold; 
                margin-bottom: 2px;
                margin-top: 2px;
                
                }
            QLabel {
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 16px;
                color: #2f3640;
                
            }
            QLineEdit {
                padding: 8px;
                border: 2px solid #dcdde1;
                border-radius: 6px;
                background-color: white;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 2px solid #35de7b; /* Borda verde quando clica no campo */
            }
            QPushButton#botao_limpar {
                background-color: #f70000;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton#botao_buscar {
                background-color: #35de7b;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #3e4f45; /* Cor muda ao passar o mouse */
            }
            QLineEdit#campo_cep{
                margin-top: 0px;
                margin-bottom: 2px;
            }

        """)


    def executa_busca(self):
            cep_digitado = self.campo_cep.text()

            self.label_resultado.setText("Buscando...")

            resultado = ViaCepClient(cep_digitado)

            if resultado.valido:
                """texto_resultado = (
                    f"CEP: {resultado.cep_original}\n"
                    f"Rua: {resultado.logradouro}\n"
                    f"Bairro: {resultado.bairro}\n"
                    f"Cidade: {resultado.localidade} - {resultado.uf}\n"
                    f"DDD: {resultado.ddd}"
                )"""
                texto_formatado = (
                    f"<b>CEP:</b> {resultado.cep_original}<br>"
                    f"<b>Rua:</b> {resultado.logradouro}<br>"
                    f"<b>Bairro:</b> {resultado.bairro}<br>"
                    f"<b>Cidade:</b> {resultado.localidade} - {resultado.uf}<br>"
                    f"<b>DDD:</b> {resultado.ddd}"
                )
                self.label_resultado.setText(texto_formatado)

            else:
                self.label_resultado.setText(f"<span style='color:red;'>Erro: {resultado.erro_mensagem}</span>")

    def limpa_campo(self):
         self.campo_cep.clear()
         self.label_resultado.setText("Os resultados aparecerão aqui.")