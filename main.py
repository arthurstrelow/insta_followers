"""
    Projeto Criado Por: Arthur Strelow - TADS MODULO I (IFPI) - 04/2022
    "Podem Copiar o que eu faço, mas não podem copiar o que sei fazer"
"""
import os
from selenium import webdriver
from time import sleep
from getpass import getpass
import sys

# PARAR DE MOSTRAR ERROS DE DEPRECATION
if not sys.warnoptions:
    import warnings
    warnings.simplefilter("ignore")


def titulo(txt):
    print()
    print('-=' * 25)
    print(txt.center(50))
    print('-=' * 25)


titulo('BOT p/ o INSTAGRAM [V1.0]')

while True:
    resp = str(input('Gostaria de ver as funcionalidades do BOT? [S/N] => ')).upper()
    if resp not in 'SN':
        print('\033[31mOpção inválida!\033[m')
        sleep(1)
    if resp == 'N':
        break
    if resp == 'S':
        print('''\033[33mCom esse bot você poderá ver as pessoas que não estão te seguindo de volta.
Além da possibilidade de forma automática parar de seguir todas esses otários,
e se caso ter pessoas que você não queira parar de seguir
pode "falar" com o bot para ele pular essas pessoas.\033[m''')
        sleep(3)
        break
usuario = str(input('Digite o nome do seu usuário => '))
senha = getpass('Digite sua senha => ')


class Instabot:
    def __init__(self, username, pw):
        self.username = usuario
        self.driver = webdriver.Chrome(f"{os.path.dirname(os.path.abspath(__file__))}/chromedriver")
        self.driver.get('https://www.instagram.com')
        titulo('Abrindo o Instagram e Logando...')
        sleep(3)
        # Insere o nome de usuário
        self.driver.find_element_by_xpath('//input[@name=\"username\"]') \
            .send_keys(username)
        # Insere a senha
        self.driver.find_element_by_xpath('//input[@name=\"password\"]') \
            .send_keys(senha)
        # Clicar no botão de login
        self.driver.find_element_by_xpath('//button[@type="submit"]') \
            .click()
        sleep(6)
        titulo('Logado no Instagram...Entrando no Perfil.')
        self.driver.find_element_by_xpath("//button[contains(text(), 'Agora não')]") \
            .click()
        sleep(4)
        self.driver.find_element_by_xpath("//button[contains(text(), 'Agora não')]") \
            .click()
        sleep(2)

    def get_unfollowers(self):
        self.driver.find_element_by_xpath("//a[contains(@href, '/{}/')]".format(self.username)) \
            .click()
        sleep(3)
        titulo('Comparando "Seguindo" e "Seguidores"...')
        self.driver.find_element_by_xpath("//a[contains(@href, '/following')]") \
            .click()
        following = self._get_names()
        self.driver.find_element_by_xpath("//a[contains(@href, '/followers')]") \
            .click()
        followers = self._get_names(following=False)
        not_following_back = [user for user in following if user not in followers]
        cont = 0
        for uuu in not_following_back:
            try:
                a = open(usuario + '.txt', 'at+')
            except:
                print("Houve um problema na hora de abrir o arquivo")
            else:
                try:
                    a.write(f'{uuu}\n')
                    cont += 1
                except:
                    print('Problema na hora de escrever os nomes')
                else:
                    print(f'=> [{uuu}] NÃO TE SEGUE')
                    a.close()
        titulo(f'O Total de pessoas que não te seguem de voltas são: {cont}')

    def _get_names(self, following=True):
        sleep(3)
        if following:
            scroll_box = self.driver.find_element_by_xpath("/html/body/div[1]/div/div[1]/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div/div[3]")
        else:
            scroll_box = self.driver.find_element_by_xpath("/html/body/div[1]/div/div[1]/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div/div[2]")

        last_ht, ht = 0, 1

        while last_ht != ht:
            last_ht = ht
            sleep(1)
            ht = self.driver.execute_script("""
                arguments[0].scrollTo(0, arguments[0].scrollHeight);
                return arguments[0].scrollHeight
            """, scroll_box)
        links = scroll_box.find_elements_by_tag_name('a')
        names = [name.text for name in links if name != '']
        self.driver.find_element_by_xpath("/html/body/div[1]/div/div[1]/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div/div[1]/div/div[3]/div/button") \
            .click()
        return names

    def pararSeguir(self, nomedoarquivo=usuario + '.txt'):
        arq = open(nomedoarquivo)
        linhas = arq.readlines()
        for linha in linhas:
            linha.replace('\n', '')
            self.driver.get(f'https://www.instagram.com/{linha}/')
            sleep(2)
            try:
                self.driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[1]/section/main/div/header/section/div[1]/div[1]/div/div[2]/button').click()
            except:
                self.driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[1]/section/main/div/header/section/div[1]/div[2]/div/div[2]/button').click()
            sleep(.5)
            self.driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div/div[3]/button[1]').click()
            print(f'Você parou de seguir => {linha}')
        arq.close()


Botzin = Instabot(usuario, senha)
Botzin.get_unfollowers()
try:
    f = open(usuario + '.txt')
    f.close()
except:
    titulo('BOT ENCERRADO!')
else:
    while True:
        resp = str(input('Você deseja alterar a lista das pessoas que você quer parar de seguir? [S/N] => ')).upper()
        if resp not in 'SN':
            print('\033[31mOpção inválida!\033[m')
            sleep(1)
        if resp == 'N':
            print(Botzin.pararSeguir())
            break
        if resp == 'S':
            arq2 = open(usuario + '.txt')
            linhas2 = arq2.readlines()
            lista = [linhas2][0]
            while True:
                print('\033[33mDIGITE [N] PARA PARAR DE DIGITAR AS PESSOAS QUE VOCÊ QUER CONTINUAR SEGUINDO\033[m')
                print('Digite a palavra VERIFICADO (PARA A QUANTIDADE DE VERIFICADOS QUE TIVER) para impedir BUGS!')
                resp = str(input('Qual usuário você gostaria de continuar seguindo? => '))
                if resp in 'Nn':
                    break
                try:
                    lista.remove(f'{resp}\n')
                except:
                    print('\033[31mVocê digitou o usuário errado\033[m')
                    sleep(.3)
            print('As pessoas que você parará de seguir é: ')
            for aa in lista:
                print(f'=> {aa}', end='')
            arq2.close()
            sleep(5)
            arquivo = open(f"{usuario}_novo.txt", "a")
            for linhaa in lista:
                arquivo.write(linhaa)
            arquivo.close()
        Botzin.pararSeguir(f'{usuario}_novo.txt')
        os.remove(f'{usuario}_novo.txt')
        break
    os.remove(usuario + '.txt')
