#MenuTitle: Smooth2Sharp
# -*- coding: utf-8 -*-
__doc__ = """
1. Quiebres menores a UMBRAL_GRADOS: alinea las manijas y deja el nodo suave.
   Quiebres mayores: los deja como esquina.
2. (Opcional) Simplifica: elimina nodos suaves redundantes reajustando la curva,
   siempre que el contorno no se desvíe más de TOLERANCIA_UNIDADES.
Funciona sobre las capas seleccionadas. Si hay nodos seleccionados en una capa,
solo trabaja con esos.
"""

import math
from GlyphsApp import Glyphs, Message
try:
	from Foundation import NSPoint
except ImportError:
	NSPoint = lambda x, y: (x, y)

# ---------------- Ajustes ----------------
UMBRAL_GRADOS = 10.0          # quiebres menores → nodo suave con manijas alineadas;
                              # quiebres mayores → esquina (se conservan)
SIMPLIFICAR = True            # eliminar nodos suaves redundantes
TOLERANCIA_UNIDADES = 4.0     # separación máxima (unidades) entre contorno nuevo y original
PROTEGER_EXTREMOS = True      # no borrar nodos en extremos horizontales/verticales
# -----------------------------------------


# ---------- utilidades de nodos ----------

def es_offcurve(nodo):
	return str(nodo.type).lower() == "offcurve"

def es_curva(nodo):
	return str(nodo.type).lower() == "curve"

def es_suave(nodo):
	if hasattr(nodo, "smooth"):
		return bool(nodo.smooth)
	return nodo.connection != 0

def hacer_esquina(nodo):
	if hasattr(nodo, "smooth"):
		nodo.smooth = False
	else:
		nodo.connection = 0

def xy(nodo):
	return (float(nodo.position.x), float(nodo.position.y))


# ---------- 1. alinear quiebres pequeños / marcar esquinas ----------

def direcciones(prev, nodo, sig):
	pin = unitario((nodo[0] - prev[0], nodo[1] - prev[1]))
	pout = unitario((sig[0] - nodo[0], sig[1] - nodo[1]))
	return pin, pout

def angulo(u, v):
	return abs(math.degrees(math.atan2(u[0] * v[1] - u[1] * v[0], u[0] * v[0] + u[1] * v[1])))

def hacer_suave(nodo):
	if hasattr(nodo, "smooth"):
		nodo.smooth = True
	else:
		nodo.connection = 100

def alinear_o_esquina(layer, path, hay_seleccion):
	alineados = esquinas = 0
	nodos = list(path.nodes)
	n = len(nodos)
	for i, nodo in enumerate(nodos):
		if es_offcurve(nodo):
			continue
		if hay_seleccion and not nodo.selected:
			continue
		if not path.closed and (i == 0 or i == n - 1):
			continue
		prev, sig = nodos[(i - 1) % n], nodos[(i + 1) % n]
		pP, pN, pS = xy(prev), xy(nodo), xy(sig)
		# si una manija está retraída, mirar el siguiente punto del contorno
		if pP == pN:
			pP = xy(nodos[(i - 2) % n])
		if pS == pN:
			pS = xy(nodos[(i + 2) % n])
		u, v = direcciones(pP, pN, pS)
		if not u or not v:
			continue
		d = angulo(u, v)
		if d >= UMBRAL_GRADOS:
			if es_suave(nodo):
				hacer_esquina(nodo)
				esquinas += 1
				print("%s: (%g, %g) quiebre %.1f° → esquina" % (layer.parent.name, pN[0], pN[1], d))
			continue
		# quiebre pequeño: alinear las manijas sobre la bisectriz
		eje = unitario((u[0] + v[0], u[1] + v[1]))
		if not eje:
			continue
		movido = False
		if es_offcurve(prev) and xy(prev) != pN:
			l = math.hypot(pN[0] - xy(prev)[0], pN[1] - xy(prev)[1])
			nuevo = (round(pN[0] - eje[0] * l), round(pN[1] - eje[1] * l))
			if nuevo != xy(prev):
				prev.position = NSPoint(nuevo[0], nuevo[1]); movido = True
		if es_offcurve(sig) and xy(sig) != pN:
			l = math.hypot(xy(sig)[0] - pN[0], xy(sig)[1] - pN[1])
			nuevo = (round(pN[0] + eje[0] * l), round(pN[1] + eje[1] * l))
			if nuevo != xy(sig):
				sig.position = NSPoint(nuevo[0], nuevo[1]); movido = True
		if es_offcurve(prev) and es_offcurve(sig) and (movido or not es_suave(nodo)):
			hacer_suave(nodo)
			alineados += 1
			print("%s: (%g, %g) quiebre %.1f° → suave alineado" % (layer.parent.name, pN[0], pN[1], d))
	return alineados, esquinas


# ---------- 2. simplificación ----------

def bez(p0, p1, p2, p3, t):
	mt = 1 - t
	a, b, c, d = mt * mt * mt, 3 * mt * mt * t, 3 * mt * t * t, t * t * t
	return (a * p0[0] + b * p1[0] + c * p2[0] + d * p3[0],
	        a * p0[1] + b * p1[1] + c * p2[1] + d * p3[1])

def muestras(segs, por_seg=24):
	pts = []
	for s in segs:
		for k in range(por_seg):
			pts.append(bez(s[0], s[1], s[2], s[3], k / float(por_seg)))
	pts.append(segs[-1][3])
	return pts

def unitario(v):
	l = math.hypot(v[0], v[1])
	return (v[0] / l, v[1] / l) if l > 1e-9 else None

def ajustar(p0, p3, t0, t1, pts):
	"""Ajuste por mínimos cuadrados de las longitudes de manija (método de Schneider)."""
	# parametrización por longitud de cuerda
	d = [0.0]
	for i in range(1, len(pts)):
		d.append(d[-1] + math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]))
	if d[-1] <= 0:
		return None
	us = [x / d[-1] for x in d]
	c00 = c01 = c11 = x0 = x1 = 0.0
	for u, p in zip(us, pts):
		mt = 1 - u
		b0, b1, b2, b3 = mt ** 3, 3 * mt * mt * u, 3 * mt * u * u, u ** 3
		a1 = (t0[0] * b1, t0[1] * b1)
		a2 = (t1[0] * b2, t1[1] * b2)
		c00 += a1[0] * a1[0] + a1[1] * a1[1]
		c01 += a1[0] * a2[0] + a1[1] * a2[1]
		c11 += a2[0] * a2[0] + a2[1] * a2[1]
		r = (p[0] - (p0[0] * (b0 + b1) + p3[0] * (b2 + b3)),
		     p[1] - (p0[1] * (b0 + b1) + p3[1] * (b2 + b3)))
		x0 += a1[0] * r[0] + a1[1] * r[1]
		x1 += a2[0] * r[0] + a2[1] * r[1]
	det = c00 * c11 - c01 * c01
	if abs(det) < 1e-12:
		return None
	alfa = (x0 * c11 - x1 * c01) / det
	beta = (c00 * x1 - c01 * x0) / det
	if alfa <= 0 or beta <= 0:
		return None
	h1 = (round(p0[0] + t0[0] * alfa), round(p0[1] + t0[1] * alfa))
	h2 = (round(p3[0] + t1[0] * beta), round(p3[1] + t1[1] * beta))
	return h1, h2

def distancia_max(a, b):
	"""Distancia de Hausdorff aproximada entre dos polilíneas densas."""
	def una(p, q):
		m = 0.0
		for x in p:
			best = min((x[0] - y[0]) ** 2 + (x[1] - y[1]) ** 2 for y in q)
			m = max(m, best)
		return math.sqrt(m)
	return max(una(a, b), una(b, a))

def es_extremo(hin, nodo, hout):
	return ((hin[0] == nodo[0] and hout[0] == nodo[0]) or
	        (hin[1] == nodo[1] and hout[1] == nodo[1]))

def candidato(path, i):
	"""Devuelve (error, índices a borrar, h1, h4, nuevas posiciones) o None."""
	nodos = path.nodes
	n = len(nodos)
	if n < 9:
		return None
	idx = [(i + k) % n for k in range(-3, 4)]  # A h1 h2 N h3 h4 B
	A, H1, H2, N, H3, H4, B = [nodos[k] for k in idx]
	if not (es_offcurve(H1) and es_offcurve(H2) and es_offcurve(H3) and es_offcurve(H4)):
		return None
	if es_offcurve(A) or es_offcurve(B) or not es_curva(B):
		return None
	if not path.closed and (i - 3 < 0 or i + 3 >= n):
		return None
	pA, p1, p2, pN, p3, p4, pB = [xy(x) for x in (A, H1, H2, N, H3, H4, B)]
	if PROTEGER_EXTREMOS and es_extremo(p2, pN, p3):
		return None
	t0 = unitario((p1[0] - pA[0], p1[1] - pA[1])) or unitario((p2[0] - pA[0], p2[1] - pA[1]))
	t1 = unitario((p4[0] - pB[0], p4[1] - pB[1])) or unitario((p3[0] - pB[0], p3[1] - pB[1]))
	if not t0 or not t1:
		return None
	orig = muestras([(pA, p1, p2, pN), (pN, p3, p4, pB)], por_seg=20)
	res = ajustar(pA, pB, t0, t1, orig)
	if not res:
		return None
	q1, q2 = res
	nueva = muestras([(pA, q1, q2, pB)], por_seg=60)
	orig_densa = muestras([(pA, p1, p2, pN), (pN, p3, p4, pB)], por_seg=30)
	err = distancia_max(orig_densa, nueva)
	if err > TOLERANCIA_UNIDADES:
		return None
	return err, [idx[2], idx[3], idx[4]], H1, H4, q1, q2

def simplificar(layer, path, hay_seleccion):
	quitados = 0
	while True:
		mejor = None
		for i, nodo in enumerate(path.nodes):
			if es_offcurve(nodo) or not es_suave(nodo):
				continue
			if hay_seleccion and not nodo.selected:
				continue
			c = candidato(path, i)
			if c and (mejor is None or c[0] < mejor[0]):
				mejor = c
		if not mejor:
			return quitados
		err, borrar, H1, H4, q1, q2 = mejor
		print("%s: nodo en (%g, %g) eliminado (error %.2f u)" % (
			layer.parent.name, path.nodes[borrar[1]].position.x,
			path.nodes[borrar[1]].position.y, err))
		H1.position = NSPoint(q1[0], q1[1])
		H4.position = NSPoint(q2[0], q2[1])
		for k in sorted(borrar, reverse=True):
			del path.nodes[k]
		quitados += 1


# ---------------- principal ----------------

font = Glyphs.font
if font is None:
	Message("Smooth2Sharp", "No hay ninguna fuente abierta.")
else:
	alineados = esquinas = quitados = 0
	font.disableUpdateInterface()
	try:
		for layer in font.selectedLayers:
			hay_seleccion = any(n.selected for p in layer.paths for n in p.nodes)
			layer.beginChanges()
			for path in layer.paths:
				a, e = alinear_o_esquina(layer, path, hay_seleccion)
				alineados += a
				esquinas += e
				if SIMPLIFICAR:
					quitados += simplificar(layer, path, hay_seleccion)
			layer.endChanges()
	finally:
		font.enableUpdateInterface()
	resumen = "%d quiebres alineados, %d nodos a esquina, %d nodos eliminados." % (
		alineados, esquinas, quitados)
	print("Smooth2Sharp: " + resumen)
	Glyphs.showNotification("Smooth2Sharp", resumen)
