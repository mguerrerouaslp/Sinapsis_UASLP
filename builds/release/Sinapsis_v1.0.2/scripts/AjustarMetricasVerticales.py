#MenuTitle: Ajustar métricas verticales (fontbakery)
# -*- coding: utf-8 -*-
__doc__ = """
1. Ajusta las métricas de cada master (ascender, cap height, x-height,
   descender y overshoots) midiendo glifos de referencia.
2. Ajusta typo / hhea / win de todos los masters según el esquema de vertical
metrics de Google Fonts, que es lo que revisa fontbakery:
- typo = hhea, con lineGap 0 en ambos            (linegaps, os2_metrics_match_hhea,
                                                    googlefonts/vertical_metrics)
- typoAscender ≥ yMax de Abreveacute (o Agrave)  (typoascender_exceeds_Agrave)
- typoDescender más profundo que la descendente más baja del alfabeto básico
- suma entre 120 % y 130 % del UPM               (googlefonts/vertical_metrics)
- winAscent/winDescent cubren el yMax/yMin de toda la familia
                                                   (family/win_ascent_and_descent)
- Use Typo Metrics activado                      (googlefonts/use_typo_metrics)
Los mismos valores se escriben en todos los masters.
"""

import math
import GlyphsApp
from GlyphsApp import Glyphs, Message

# ---------- 1. métricas del master ----------
AJUSTAR_METRICAS = True
# glifos de referencia: se usa la mediana de su altura (o profundidad)
REF_PLANAS = {
	"capHeight": "H E F I L T Z",   # tope de mayúsculas rectas
	"xHeight":   "x z v w",         # tope de minúsculas rectas
	"ascender":  "b d h k l",       # astas ascendentes
	"descender": "p q",             # astas descendentes
}
REF_REDONDAS = {
	"capHeight": "O C G Q S",       # para el overshoot de mayúsculas
	"xHeight":   "o c e s",         # para el overshoot de altura x
	"baseline":  "o c e s O C G S", # para el overshoot bajo la línea base
}
OVERSHOOT_MIN = 10   # si la medición da menos, se conserva el overshoot actual

REDONDEO = 5            # redondear ascender/descender hacia afuera a múltiplos de esto
MARGEN_WIN = 2          # la conversión a cuadráticas puede mover el bbox 1–2 u
DESCENDENTES = ["p", "q", "g", "j", "y"]
SUMA_MIN, SUMA_MAX = 1.20, 1.30


def bounds(glyph, master):
	layer = glyph.layers[master.id]
	if layer is None or (not layer.paths and not layer.components):
		return None
	b = layer.bounds
	return b.origin.y, b.origin.y + b.size.height

def hacia_arriba(v):
	return int(math.ceil(v / float(REDONDEO)) * REDONDEO)

def hacia_abajo(v):
	return int(math.floor(v / float(REDONDEO)) * REDONDEO)


def mediana(valores):
	v = sorted(valores)
	n = len(v)
	if not n:
		return None
	return v[n // 2] if n % 2 else (v[n // 2 - 1] + v[n // 2]) / 2.0

def medir(font, master, nombres, arriba=True):
	vals = []
	for nombre in nombres.split():
		g = font.glyphs[nombre]
		b = bounds(g, master) if g else None
		if b:
			vals.append(b[1] if arriba else b[0])
	return mediana(vals)

TIPOS = {
	"ascender": "GSMetricsTypeAscender",
	"capHeight": "GSMetricsTypeCapHeight",
	"xHeight": "GSMetricsTypexHeight",
	"baseline": "GSMetricsTypeBaseline",
	"descender": "GSMetricsTypeDescender",
}

def valor_metrica(font, master, clave):
	"""Devuelve el GSMetricStore (position/overshoot) de una métrica, o None."""
	tipo = getattr(GlyphsApp, TIPOS[clave], None)
	if tipo is None or not hasattr(font, "metrics"):
		return None
	for m in font.metrics:
		if m.type == tipo and getattr(m, "filter", None) is None:
			try:
				return master.metrics[m.id]
			except Exception:
				return None
	return None

def ajustar_metricas(font, master):
	print("\nMétricas del master %s" % master.name)
	nuevas = {}
	for clave, nombres in REF_PLANAS.items():
		v = medir(font, master, nombres, arriba=(clave != "descender"))
		if v is None:
			print("  %-10s sin glifos de referencia, no se cambia" % clave)
			continue
		v = int(round(v))
		anterior = getattr(master, clave)
		# en Glyphs 3/4 la posición vive en el metric store; master.<clave> solo es atajo
		store = valor_metrica(font, master, clave)
		if store is not None:
			store.position = v
		else:
			setattr(master, clave, v)
		nuevas[clave] = v
		print("  %-10s %5d   (antes: %g)   ref: %s" % (clave, v, anterior, nombres))
	# overshoots
	for clave, nombres in REF_REDONDAS.items():
		store = valor_metrica(font, master, clave)
		if store is None:
			print("  overshoot %-10s no se pudo leer desde la API; revísalo en Font Info" % clave)
			continue
		if clave == "baseline":
			med = medir(font, master, nombres, arriba=False)
			medido = -int(round(-med)) if med is not None else None
			ok = medido is not None and medido <= -OVERSHOOT_MIN
		else:
			med = medir(font, master, nombres, arriba=True)
			base = nuevas.get(clave, getattr(master, clave))
			medido = int(round(med - base)) if med is not None else None
			ok = medido is not None and medido >= OVERSHOOT_MIN
		anterior = store.overshoot
		if ok:
			store.overshoot = medido
			print("  overshoot %-10s %4d   (antes: %g)" % (clave, medido, anterior))
		else:
			print("  overshoot %-10s se conserva en %g (medido: %s)" % (clave, anterior, medido))


font = Glyphs.font
if font is not None and AJUSTAR_METRICAS:
	for master in font.masters:
		ajustar_metricas(font, master)

if font is None:
	Message("Métricas verticales", "No hay ninguna fuente abierta.")
else:
	upm = font.upm
	ref_alta = "Abreveacute" if font.glyphs["Abreveacute"] else "Agrave"

	alto_ref = bajo_desc = None
	y_max = y_min = None
	g_max = g_min = None
	cap = max(m.capHeight for m in font.masters)

	for master in font.masters:
		g = font.glyphs[ref_alta]
		if g:
			b = bounds(g, master)
			if b and (alto_ref is None or b[1] > alto_ref):
				alto_ref = b[1]
		for nombre in DESCENDENTES:
			g = font.glyphs[nombre]
			b = bounds(g, master) if g else None
			if b and (bajo_desc is None or b[0] < bajo_desc):
				bajo_desc = b[0]
		for glyph in font.glyphs:
			if not glyph.export:
				continue
			b = bounds(glyph, master)
			if not b:
				continue
			if y_max is None or b[1] > y_max:
				y_max, g_max = b[1], glyph.name
			if y_min is None or b[0] < y_min:
				y_min, g_min = b[0], glyph.name

	if alto_ref is None:
		alto_ref = max(m.ascender for m in font.masters)
	if bajo_desc is None:
		bajo_desc = min(m.descender for m in font.masters)

	asc = hacia_arriba(alto_ref)
	# mayúsculas centradas en la línea, pero sin quedar arriba de la descendente más baja
	desc = min(-(asc - cap), hacia_abajo(bajo_desc))
	suma = asc - desc
	if suma < upm * SUMA_MIN:
		desc -= int(math.ceil(upm * SUMA_MIN)) - suma
		suma = asc - desc

	win_asc = int(math.ceil(y_max)) + MARGEN_WIN
	win_desc = int(math.ceil(-y_min)) + MARGEN_WIN

	valores = [
		("typoAscender", asc), ("typoDescender", desc), ("typoLineGap", 0),
		("hheaAscender", asc), ("hheaDescender", desc), ("hheaLineGap", 0),
		("winAscent", win_asc), ("winDescent", win_desc),
	]
	for master in font.masters:
		print("\nMaster %s" % master.name)
		for nombre, valor in valores:
			anterior = master.customParameters[nombre]
			master.customParameters[nombre] = valor
			marca = "" if anterior == valor else "   (antes: %s)" % anterior
			print("  %-14s %6d%s" % (nombre, valor, marca))
	font.customParameters["Use Typo Metrics"] = True

	print("\nReferencias:")
	print("  %s yMax: %d   →  typo/hhea ascender %d" % (ref_alta, alto_ref, asc))
	print("  descendente más baja (%s): %d  →  typo/hhea descender %d" % (", ".join(DESCENDENTES), bajo_desc, desc))
	print("  suma: %d = %.0f %% del UPM" % (suma, 100.0 * suma / upm))
	print("  glifo más alto: %s (%d)   más bajo: %s (%d)" % (g_max, y_max, g_min, y_min))
	if suma > upm * SUMA_MAX:
		print("  AVISO: la suma pasa de %d %%. fontbakery solo da WARN arriba de 150 %%," % (SUMA_MAX * 100))
		print("  pero la guía de Google Fonts recomienda 120–130 %.")
	Glyphs.showNotification("Métricas verticales", "Listo. Detalle en el Panel de Macros.")
