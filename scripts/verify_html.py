import urllib.request

html = urllib.request.urlopen('http://127.0.0.1:8000/').read().decode('utf-8')
checks = [
    ('site-header', 'site-header' in html),
    ('logo-mlp.png', 'logo-mlp.png' in html),
    ('id="transmissoes"', 'id="transmissoes"' in html),
    ('id="avisos"', 'id="avisos"' in html),
    ('id="ministerio"', 'id="ministerio"' in html),
    ('id="cultos"', 'id="cultos"' in html),
    ('id="galeria"', 'id="galeria"' in html),
    ('id="contato"', 'id="contato"' in html),
    ('stream-player-container', 'stream-player-container' in html),
    ('strict-origin-when-cross-origin', 'referrerpolicy="strict-origin-when-cross-origin"' in html),
]

for name, res in checks:
    print(f"Check {name}: {'PASS' if res else 'FAIL'}")
