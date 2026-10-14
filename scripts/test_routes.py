import urllib.request

routes = [
    ('/', 200),
    ('/cadastro/', 200),
    ('/entrar/', 200),
    ('/perfil/', 200),
    ('/avisos/', 200),
    ('/mensagens-e-ao-vivo/', 200),
    ('/mensagens-e-ao-vivo/culto-mlp-11-out-26-dom/', 200),
    ('/agenda-cultos/', 200),
    ('/acervo-fotografico/', 200),
    ('/legado-pastor-leonel/', 200),
    ('/nossa-historia/', 200),
    ('/contato-e-horarios/', 200),
]

for path, expected_status in routes:
    url = f"http://127.0.0.1:8000{path}"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as resp:
            status = resp.status
            print(f"[OK] {path} -> HTTP {status}")
    except Exception as e:
        print(f"[ERROR] {path} -> {e}")
