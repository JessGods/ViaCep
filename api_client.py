import requests
import re

class ViaCepClient:
    def __init__(self, cep: str):
        self.base_url = "https://viacep.com.br"
        self.cep_original = cep
        self.cep_limpo = self._limpar_cep(cep)
        self.valido = False
        self.erro_mensagem = None

        self.logradouro = None
        self.bairro = None
        self.localidade = None
        self.uf = None
        self.ddd = None

        if self._validar_cep():
            self._buscar_dados()

    def _limpar_cep(self, cep):
        #Adicionando regex para limpar o cep (Indicação de um comentario no linkedin)
        numeros = re.findall(r'\d+', str(cep))
        return "".join(numeros)

        #return str(cep).replace("-", "").replace(".", "").strip()

    def _validar_cep(self):
        if len(self.cep_limpo) != 8 or not self.cep_limpo.isdigit():
            self.erro_mensagem = "Cep inválido. Deve conter 8 dígitos numéricos."
            return False
        return True
    def _buscar_dados(self):
        
        url = f"https://viacep.com.br/ws/{self.cep_limpo}/json/"

        try:
            resposta = requests.get(url, timeout=5)
            if resposta.status_code == 200:
                dados = resposta.json()
                if "erro" in dados:
                    self.erro_mensagem = "Cep não encontrado na base de dados."
                else:
                    self.logradouro = dados.get("logradouro")
                    self.bairro = dados.get("bairro")
                    self.localidade = dados.get("localidade")
                    self.uf = dados.get("uf")
                    self.ddd = dados.get("ddd")
                    self.valido = True
            else:
                self.erro_mensagem = f"Erro na requisição. Status code: {resposta.status_code}"
        except requests.exceptions.RequestException as e:
            self.erro_mensagem = f"Erro de conexão: {e}"
