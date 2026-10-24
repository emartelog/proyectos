from radar_energia.datos_abiertos import ClienteDatosAbiertos
from tests.test_simem import _Resp, _SesionFalsa


def test_pagina_hasta_agotar_registros():
    sesion = _SesionFalsa([_Resp(200, [{"a": 1}, {"a": 2}]), _Resp(200, [{"a": 3}])])
    cliente = ClienteDatosAbiertos(sesion=sesion, espera_base=0, tamano_pagina=2)
    paginas = list(cliente.registros("ytme-6qnu"))
    assert [len(p) for p in paginas] == [2, 1]
    _, url, _ = sesion.llamadas[0]
    assert url.endswith("/resource/ytme-6qnu.json")


def test_respeta_limite():
    sesion = _SesionFalsa([_Resp(200, [{"a": 1}, {"a": 2}])])
    cliente = ClienteDatosAbiertos(sesion=sesion, espera_base=0, tamano_pagina=5)
    assert sum(len(p) for p in cliente.registros("x", limite=2)) == 2
    assert len(sesion.llamadas) == 1
