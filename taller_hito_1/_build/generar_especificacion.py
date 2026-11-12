# -*- coding: utf-8 -*-
"""Genera la especificación de requerimientos del motor NLU en Word."""

from pathlib import Path

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor, Twips
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
TALLER = ROOT / "taller_hito_1"
BUILD = TALLER / "_build"
OUT = TALLER / "especificacion_requerimientos_motor_nlu.docx"

NAVY = RGBColor(0x1B, 0x3A, 0x4B)
TEAL = RGBColor(0x0F, 0x76, 0x6E)
INK = RGBColor(0x1E, 0x29, 0x3B)
MUTED = RGBColor(0x47, 0x55, 0x69)

MERMAID_ER = """erDiagram
    Request ||--o{ Interpretation : "acumula"
    Interpretation ||--|| Decision : "produce"

    Request {
        string id PK
        string status "RECEIVED | INCOMPLETE | FORWARDED | ESCALATED"
        string correlationId
        datetime createdAt
    }

    Interpretation {
        string id PK
        string requestId FK
        string intentType
        float confidence
        string entities
        string identifiers
        string missingFields
        string summary
        string ambiguities
        boolean sufficient
    }

    Decision {
        string id PK
        string interpretationId FK
        string action "FORWARD_TO_PROCESS | REQUEST_INFORMATION | ESCALATE_TO_OPERATOR"
        boolean meetsRequirements
        string reason
        string questions
    }
"""


def set_run_font(run, name="Calibri", size=11, bold=False, italic=False, color=INK):
    run.font.name = name
    run.font.size = Pt(size)
    run.bold = bold
    run.italic = italic
    run.font.color.rgb = color
    rpr = run._element.get_or_add_rPr()
    rfonts = rpr.find(qn("w:rFonts"))
    if rfonts is None:
        rfonts = OxmlElement("w:rFonts")
        rpr.append(rfonts)
    rfonts.set(qn("w:ascii"), name)
    rfonts.set(qn("w:hAnsi"), name)
    rfonts.set(qn("w:cs"), name)


def shade_cell(cell, fill):
    tc = cell._tc
    tc_pr = tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), fill)
    tc_pr.append(shd)


def set_cell_margins(cell, top=40, bottom=40, left=80, right=80):
    tc = cell._tc
    tc_pr = tc.get_or_add_tcPr()
    tc_mar = OxmlElement("w:tcMar")
    for name, value in (("top", top), ("left", left), ("bottom", bottom), ("right", right)):
        node = OxmlElement(f"w:{name}")
        node.set(qn("w:w"), str(value))
        node.set(qn("w:type"), "dxa")
        tc_mar.append(node)
    tc_pr.append(tc_mar)


def prevent_row_split(row):
    tr_pr = row._tr.get_or_add_trPr()
    cant = OxmlElement("w:cantSplit")
    tr_pr.append(cant)


def shade_paragraph(paragraph, fill):
    p_pr = paragraph._p.get_or_add_pPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), fill)
    p_pr.append(shd)


def add_page_field(paragraph):
    run = paragraph.add_run()
    set_run_font(run, size=9, color=MUTED)
    begin = OxmlElement("w:fldChar")
    begin.set(qn("w:fldCharType"), "begin")
    instr = OxmlElement("w:instrText")
    instr.set(qn("xml:space"), "preserve")
    instr.text = " PAGE "
    separate = OxmlElement("w:fldChar")
    separate.set(qn("w:fldCharType"), "separate")
    text = OxmlElement("w:t")
    text.text = "1"
    end = OxmlElement("w:fldChar")
    end.set(qn("w:fldCharType"), "end")
    run._r.append(begin)
    run._r.append(instr)
    run._r.append(separate)
    run2 = paragraph.add_run("1")
    set_run_font(run2, size=9, color=MUTED)
    run2._r.append(end)


def configure(doc):
    section = doc.sections[0]
    section.page_width = Cm(21.0)
    section.page_height = Cm(29.7)
    section.left_margin = Cm(1.8)
    section.right_margin = Cm(1.8)
    section.top_margin = Cm(1.7)
    section.bottom_margin = Cm(1.7)
    section.header_distance = Cm(0.5)
    section.footer_distance = Cm(0.4)
    section.different_first_page_header_footer = True

    normal = doc.styles["Normal"]
    normal.font.name = "Calibri"
    normal.font.size = Pt(11)
    normal.font.color.rgb = INK
    normal.paragraph_format.space_after = Pt(8)
    normal.paragraph_format.space_before = Pt(0)
    normal.paragraph_format.line_spacing = 1.12
    rpr = normal.element.get_or_add_rPr()
    rfonts = rpr.find(qn("w:rFonts"))
    if rfonts is None:
        rfonts = OxmlElement("w:rFonts")
        rpr.append(rfonts)
    rfonts.set(qn("w:ascii"), "Calibri")
    rfonts.set(qn("w:hAnsi"), "Calibri")
    lang = rpr.find(qn("w:lang"))
    if lang is None:
        lang = OxmlElement("w:lang")
        rpr.append(lang)
    lang.set(qn("w:val"), "es-CO")

    for style_name, size, color, before, after in (
        ("Heading 1", 16, NAVY, 16, 6),
        ("Heading 2", 13, NAVY, 12, 4),
        ("Heading 3", 12, TEAL, 10, 3),
    ):
        style = doc.styles[style_name]
        style.font.name = "Calibri"
        style.font.size = Pt(size)
        style.font.bold = True
        style.font.color.rgb = color
        style.paragraph_format.space_before = Pt(before)
        style.paragraph_format.space_after = Pt(after)
        style.paragraph_format.keep_with_next = True
        style.paragraph_format.line_spacing = 1.08

    header = section.header
    header.is_linked_to_previous = False
    hp = header.paragraphs[0]
    hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    hp.paragraph_format.space_after = Pt(2)
    run = hp.add_run("Banco Andino  ·  Especificación de requerimientos del motor NLU")
    set_run_font(run, size=9, color=MUTED)

    footer = section.footer
    footer.is_linked_to_previous = False
    fp = footer.paragraphs[0]
    fp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    fp.paragraph_format.space_before = Pt(2)
    left = fp.add_run("Hito 1  ·  IA en Negocios Digitales")
    set_run_font(left, size=9, color=MUTED)
    mid = fp.add_run("          ")
    set_run_font(mid, size=9, color=MUTED)
    add_page_field(fp)

    # Portada sin encabezado ni pie.
    section.first_page_header.paragraphs[0].text = ""
    section.first_page_footer.paragraphs[0].text = ""

    core = doc.core_properties
    core.title = "Especificación de requerimientos — Motor NLU de Banco Andino"
    core.subject = "Identificador de solicitudes en lenguaje natural"
    core.category = "Especificación de requerimientos"
    core.language = "es-CO"
    core.comments = (
        "Consolidación de la Actividad 1 y la Actividad 2 del taller "
        "del identificador de solicitudes de Banco Andino."
    )


def h(doc, text, level=1):
    doc.add_heading(text, level=level)


def para(doc, text, size=11, bold=False, italic=False, color=INK, after=8, before=0, align="left"):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(after)
    p.paragraph_format.space_before = Pt(before)
    p.paragraph_format.line_spacing = 1.12
    if align == "center":
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    elif align == "justify":
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    run = p.add_run(text)
    set_run_font(run, size=size, bold=bold, italic=italic, color=color)
    return p


def labeled(doc, label, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(8)
    p.paragraph_format.line_spacing = 1.12
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    a = p.add_run(label)
    set_run_font(a, bold=True)
    b = p.add_run(text)
    set_run_font(b)
    return p


def bullets(doc, items):
    for item in items:
        p = doc.add_paragraph(style="List Bullet")
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.space_before = Pt(0)
        p.clear()
        run = p.add_run(item)
        set_run_font(run, size=11)


def numbered(doc, items):
    for index, item in enumerate(items, start=1):
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.left_indent = Cm(0.75)
        p.paragraph_format.first_line_indent = Cm(-0.75)
        run = p.add_run(f"{index}. {item}")
        set_run_font(run, size=11)


def callout(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(10)
    p.paragraph_format.line_spacing = 1.12
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    shade_paragraph(p, "F1F5F9")
    run = p.add_run(text)
    set_run_font(run, size=11, italic=False, color=INK)
    return p


def add_table(doc, headers, rows, widths):
    table = doc.add_table(rows=1 + len(rows), cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    table.allow_autofit = False
    tbl = table._tbl
    tbl_pr = tbl.tblPr
    tbl_w = OxmlElement("w:tblW")
    total = widths[0]
    for width in widths[1:]:
        total += width
    tbl_w.set(qn("w:w"), str(int(int(total) / 635)))
    tbl_w.set(qn("w:type"), "dxa")
    tbl_pr.append(tbl_w)

    borders = OxmlElement("w:tblBorders")
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        el = OxmlElement(f"w:{edge}")
        el.set(qn("w:val"), "single")
        el.set(qn("w:sz"), "4")
        el.set(qn("w:space"), "0")
        el.set(qn("w:color"), "CBD5E1")
        borders.append(el)
    tbl_pr.append(borders)

    for i, header in enumerate(headers):
        cell = table.rows[0].cells[i]
        cell.text = ""
        cell.width = widths[i]
        shade_cell(cell, "1B3A4B")
        set_cell_margins(cell)
        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.space_before = Pt(0)
        run = p.add_run(header)
        set_run_font(run, size=10, bold=True, color=RGBColor(255, 255, 255))
    prevent_row_split(table.rows[0])
    tr_pr = table.rows[0]._tr.get_or_add_trPr()
    tbl_header = OxmlElement("w:tblHeader")
    tbl_header.set(qn("w:val"), "true")
    tr_pr.append(tbl_header)

    for r, row in enumerate(rows):
        for c, value in enumerate(row):
            cell = table.rows[r + 1].cells[c]
            cell.text = ""
            cell.width = widths[c]
            if r % 2 == 1:
                shade_cell(cell, "F8FAFC")
            set_cell_margins(cell)
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.space_before = Pt(0)
            run = p.add_run(str(value))
            set_run_font(run, size=10)
        prevent_row_split(table.rows[r + 1])

    spacer = doc.add_paragraph()
    spacer.paragraph_format.space_after = Pt(6)
    spacer.paragraph_format.space_before = Pt(2)
    return table


def flatten(path):
    image = Image.open(path).convert("RGBA")
    background = Image.new("RGB", image.size, (255, 255, 255))
    background.paste(image, mask=image.split()[-1])
    target = BUILD / f"flat_{Path(path).stem}.png"
    background.save(target, "PNG")
    return target, background.size


def figure(doc, path, caption, max_w=Cm(17.4), max_h=Cm(22.2)):
    flat, (px_w, px_h) = flatten(path)
    width = max_w
    if px_h / px_w * width.cm > max_h.cm:
        width = Cm(max_h.cm * px_w / px_h)
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.keep_together = True
    run = p.add_run()
    run.add_picture(str(flat), width=width)
    cap = doc.add_paragraph()
    cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cap.paragraph_format.space_before = Pt(0)
    cap.paragraph_format.space_after = Pt(10)
    cap.paragraph_format.keep_together = True
    run = cap.add_run(caption)
    set_run_font(run, size=9, italic=True, color=MUTED)


def code_block(doc, text, label):
    para(doc, label, size=10, bold=True, color=TEAL, after=2, before=2)
    lines = text.replace("\r\n", "\n").strip("\n").split("\n")
    for line in lines:
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = 1.0
        run = p.add_run(line if line else " ")
        set_run_font(run, name="Consolas", size=8, color=INK)
    para(doc, "", after=6)


def cover(doc):
    banner = doc.add_table(rows=1, cols=1)
    banner.autofit = False
    cell = banner.cell(0, 0)
    cell.width = Cm(17.4)
    shade_cell(cell, "1B3A4B")
    set_cell_margins(cell, top=220, bottom=220, left=160, right=160)
    cell.text = ""
    lines = [
        ("BANCO ANDINO", 12, False),
        ("Especificación de requerimientos", 22, True),
        ("Motor de comprensión del lenguaje natural", 14, False),
        ("Identificador de solicitudes", 14, False),
    ]
    for index, (text, size, bold) in enumerate(lines):
        p = cell.paragraphs[0] if index == 0 else cell.add_paragraph()
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.space_before = Pt(0)
        run = p.add_run(text)
        set_run_font(run, size=size, bold=bold, color=RGBColor(255, 255, 255))

    para(doc, "", after=8)
    add_table(
        doc,
        ["Dato", "Valor"],
        [
            ["Documento", "Especificación de requerimientos del software (ERS)"],
            ["Sistema", "Motor NLU — identificador de solicitudes"],
            ["Asignatura", "IA en Negocios Digitales"],
            ["Entrega", "Hito 1 — taller, actividades 1 y 2"],
            ["Versión", "1.0"],
            ["Fecha", "12 de noviembre de 2026"],
            ["Estado", "Consolidación del trabajo realizado hasta esta fecha"],
        ],
        [Cm(4.2), Cm(13.2)],
    )
    para(
        doc,
        "Este documento reúne el requerimiento del identificador de solicitudes de Banco Andino: "
        "qué debe hacer el motor, qué recibe el cliente, cómo se recorre un caso, qué decisión "
        "sale de cada mensaje y con qué modelo, contratos y arquitectura se sostiene esa decisión.",
        align="justify",
    )
    callout(
        doc,
        "Ejemplo que recorre toda la especificación. «Llevo varios días esperando la devolución "
        "de mi dinero». Con solo ese texto, el motor reconoce una devolución pendiente, resume "
        "la espera y pide número de caso, monto y fecha. Si el mismo relato trae el caso 45821, "
        "$120.000 y la compra del 3 de noviembre, el caso se remite. Si además admite un cobro "
        "de tarjeta no reconocido, el caso pasa a un operador.",
    )
    para(doc, "Contenido", size=14, bold=True, color=NAVY, after=4)
    for item in [
        "1. Propósito y alcance",
        "2. Actores y fronteras del sistema",
        "3. Funcionalidades, beneficios y recorrido del cliente",
        "4. Casos de uso",
        "5. Requisitos funcionales y reglas de negocio",
        "6. Contratos de la respuesta",
        "7. Modelo de datos",
        "8. Interacción de identidades",
        "9. Secuencia de la identificación",
        "10. Arquitectura de despliegue",
        "11. Correspondencia con los artefactos del taller",
    ]:
        para(doc, item, size=11, after=1)
    doc.add_page_break()


def section_proposito(doc):
    h(doc, "1. Propósito y alcance")
    h(doc, "1.1 Propósito", 2)
    para(
        doc,
        "El motor NLU interpreta un mensaje escrito por el cliente, reconoce la intención "
        "principal, extrae la información relevante, resume el problema y señala ambigüedades "
        "o datos insuficientes. Con esa lectura elige una sola acción: remitir el caso al "
        "siguiente proceso, pedir una aclaración o derivarlo a un operador.",
        align="justify",
    )
    para(
        doc,
        "La especificación fija ese comportamiento para el MVP. También deja escritos los "
        "contratos que la implementación debe producir, el modelo que conserva la solicitud "
        "mientras el cliente aclara, y la forma de desplegar el mismo flujo en AWS. El ejercicio "
        "de diagramas sobre una aplicación de transporte pertenece a la práctica de la Actividad 1 "
        "y queda fuera de este sistema.",
        align="justify",
    )
    h(doc, "1.2 Qué termina el identificador", 2)
    para(
        doc,
        "El identificador termina cuando el mensaje ya tiene una decisión. La respuesta de esa "
        "decisión incluye la intención, la confianza, los datos encontrados, los datos que faltan, "
        "un resumen breve, la acción elegida y el motivo. La atención posterior del proceso de "
        "negocio y la conversación del operador con el cliente empiezan después de ese punto.",
        align="justify",
    )
    h(doc, "1.3 Qué queda dentro del diseño de soporte", 2)
    para(
        doc,
        "El canal, la persistencia y el alojamiento acompañan esa decisión y forman parte de lo "
        "ya definido en el taller. La interfaz captura el texto y muestra el resultado. La API "
        "correlaciona la petición y proyecta el estado. Cada aclaración del cliente vuelve a "
        "entrar por el mismo servicio y produce una interpretación nueva sobre la misma solicitud.",
        align="justify",
    )
    h(doc, "1.4 Fuera del alcance de esta entrega", 2)
    bullets(
        doc,
        [
            "El inicio de sesión. El diagrama distingue al visitante del usuario logueado, y el alta de la sesión queda fuera del identificador.",
            "La resolución del trámite una vez remitido: abonos, investigación del caso o tiempos de respuesta del área de negocio.",
            "La atención que el operador da después de tomar el caso. El motor le entrega el resumen y el motivo; ahí termina su trabajo.",
            "Umbrales numéricos de confianza. El taller fija que la confianza acompaña a la intención y que una lectura insegura deriva el caso. No fija un valor de corte.",
            "El catálogo completo de intenciones del banco. El caso elaborado es la devolución pendiente, y el diseño admite otras lecturas cuando el texto las pone en competencia.",
        ],
    )


def section_actores(doc):
    h(doc, "2. Actores y fronteras del sistema")
    para(
        doc,
        "Cliente es un actor abstracto. Usuario visitante y usuario logueado lo especializan. "
        "Los dos heredan el envío del mensaje y la obtención de una decisión. Solo el usuario "
        "logueado se asocia, además, a remitir el caso. Proceso de negocio y operador son "
        "actores secundarios: reciben la decisión y su trabajo posterior queda fuera.",
        align="justify",
    )
    add_table(
        doc,
        ["Actor", "Papel en el identificador"],
        [
            ["Cliente", "Actor abstracto. El visitante y el logueado heredan su asociación con el envío del mensaje."],
            ["Usuario visitante", "El mensaje llega sin identidad de cliente. Esa identidad cuenta como dato faltante, así que la salida de remisión no está disponible para él."],
            ["Usuario logueado", "La sesión ya aporta la identidad. Puede obtener la remisión cuando la intención es única, la confianza alcanza y están el caso, el monto y la fecha."],
            ["Proceso de negocio", "Recibe el caso cuando la acción es remitir. Continúa el trámite fuera del motor."],
            ["Operador", "Recibe el caso cuando la acción es derivar, con el resumen y el motivo ya armados."],
        ],
        [Cm(4.2), Cm(13.2)],
    )
    h(doc, "2.1 Cadena de entrada", 2)
    para(
        doc,
        "La cadena de entrada es lineal. El cliente solo conoce la interfaz, la interfaz solo "
        "conoce la API y la API solo conoce al coordinador. A partir de ahí el coordinador es "
        "la única identidad que alcanza a los agentes de comprensión, al validador y a los dos "
        "destinos. React envía el texto a POST /api/solicitudes. La API se lo entrega al "
        "coordinador. El coordinador dispara el resto del flujo y devuelve un único resultado.",
        align="justify",
    )
    add_table(
        doc,
        ["Identidad", "Capa", "Trabajo que conserva", "Habla solo con"],
        [
            ["Cliente", "Canal", "Redactar la solicitud y leer la respuesta", "Interfaz web"],
            ["Interfaz web (React)", "Canal", "Mostrar resumen, preguntas o aviso de derivación", "Cliente y API"],
            ["API de solicitudes (Node)", "Borde", "Correlacionar la petición y el estado HTTP", "Interfaz y coordinador"],
            ["Agente coordinador", "Orquestación", "Integrar las salidas y enrutar según el veredicto", "API, cuatro agentes y dos destinos"],
            ["Agente intérprete", "Comprensión", "Clasificar la intención y estimar la confianza", "Coordinador"],
            ["Agente extractor", "Comprensión", "Obtener entidades, identificadores y ausencias", "Coordinador"],
            ["Agente de análisis contextual", "Comprensión", "Resumir, detectar ambigüedades y juzgar suficiencia", "Coordinador"],
            ["Agente validador", "Control", "Contrastar la salida con las reglas y elegir la acción", "Coordinador"],
            ["Proceso de negocio", "Destino", "Continuar el caso ya válido", "Coordinador"],
            ["Operador humano", "Destino", "Atender lo que el NLU no cierra con el cliente", "Coordinador"],
        ],
        [Cm(4.4), Cm(2.8), Cm(5.6), Cm(4.6)],
    )


def section_valor(doc):
    h(doc, "3. Funcionalidades, beneficios y recorrido del cliente")
    h(doc, "3.1 Funcionalidades, de mayor a menor prioridad", 2)
    para(
        doc,
        "La prioridad la marca lo que permite actuar sobre la solicitud. Primero hay que "
        "entender qué pide el cliente y con qué datos. Después, si esa lectura es segura y "
        "completa. Al final, qué hacer con ella y cómo dejar constancia.",
        align="justify",
    )
    add_table(
        doc,
        ["Orden", "Funcionalidad", "Para qué existe"],
        [
            ["1", "Clasificar la intención principal", "Reconocer de qué se trata el mensaje y devolver un tipo de solicitud. Sin esa etiqueta el flujo no tiene destino."],
            ["2", "Extraer la información relevante", "Obtener entidades, identificadores y atributos, y señalar los que no aparecen. La intención sola no abre un trámite."],
            ["3", "Estimar la confianza", "Acompañar la intención con un grado de certeza. Una lectura poco segura no pasa al siguiente proceso."],
            ["4", "Juzgar suficiencia y ambigüedad", "Decidir si los datos bastan para un caso concreto y marcar lecturas dudosas o contradictorias."],
            ["5", "Resumir el problema", "Redactar en pocas líneas qué ocurre, para que el destino trabaje sobre la lectura y no sobre el mensaje crudo."],
            ["6", "Decidir el destino", "Elegir una sola acción —remitir, pedir aclaración o derivar— y dejar el motivo."],
            ["7", "Formular la aclaración", "Cuando faltan datos que el cliente puede aportar, devolver preguntas concretas."],
            ["8", "Conservar el contexto", "Tratar la respuesta del cliente como continuación de la misma solicitud y volver a interpretar, extraer y validar sobre el mensaje enriquecido."],
            ["9", "Dejar trazabilidad", "Registrar intención, datos, resumen, confianza y motivo. Sirve para auditar y corregir el motor."],
        ],
        [Cm(1.6), Cm(5.4), Cm(10.4)],
    )
    h(doc, "3.2 Beneficios para el cliente", 2)
    para(
        doc,
        "El cliente cuenta el problema con sus palabras y recibe una respuesta útil en el mismo "
        "momento: el trámite sigue, le piden solo lo que falta o una persona toma el caso ya entendido.",
        align="justify",
    )
    bullets(
        doc,
        [
            "Explica el caso como lo vive. Escribe la espera de una devolución y el banco reconoce esa intención. No necesita saber el nombre interno del trámite ni recorrer un menú.",
            "Llega al proceso correcto en el primer mensaje cuando la solicitud está clara y trae los datos necesarios. Evita repetir la historia en otro canal.",
            "Aporta menos datos de los que ya dijo. El motor toma del texto el producto, el monto, la fecha o el número de caso.",
            "Recibe preguntas concretas cuando algo falta: número de caso, monto o fecha. Puede responder en el mismo hilo.",
            "Cuando el mensaje admite más de una lectura o la certeza es baja, una persona recibe el caso con el resumen ya armado.",
            "La aclaración se suma al mensaje original. No abre un trámite nuevo ni pierde lo ya contado.",
            "La respuesta le dice si la solicitud fue remitida, si está incompleta o si pasó a un operador.",
        ],
    )
    h(doc, "3.3 Recorrido del cliente", 2)
    para(
        doc,
        "El recorrido normal es el de una solicitud cuyo primer mensaje todavía no cierra la "
        "identificación. El cliente cuenta el caso, ve qué entendió el banco, completa solo lo "
        "que falta y recibe el destino final en el mismo hilo.",
        align="justify",
    )
    numbered(
        doc,
        [
            "Entra al canal. Abre la web del banco, inicia sesión y llega a la pantalla para escribir una solicitud. Ve un campo de texto libre y el botón para enviarla. El inicio de sesión en sí queda fuera del identificador.",
            "Redacta con sus palabras. No elige un tipo de trámite ni llena un formulario previo.",
            "Envía la solicitud. La interfaz manda el texto y el cliente espera en la misma pantalla.",
            "Ve qué se entendió. La respuesta muestra el resumen y la lectura, para que compruebe si el banco interpretó el caso.",
            "Recibe las preguntas que faltan. En el ejemplo, la pantalla pide número de caso, monto y fecha. No le pide repetir el relato.",
            "Responde en el mismo hilo. El banco suma esos datos al mensaje original y vuelve a leer la solicitud completa.",
            "Recibe el cierre de la identificación. Si el caso queda claro, la pantalla muestra el resumen actualizado e indica que la solicitud fue remitida al proceso que la resuelve.",
        ],
    )
    para(doc, "En ese mismo punto de respuesta hay otras dos salidas posibles.", align="justify")
    bullets(
        doc,
        [
            "Sigue incompleta. Si aún falta algo que el cliente puede aclarar, la pantalla hace otra pregunta concreta y el paso 6 se repite.",
            "Pasa a una persona. Si el mensaje admite más de una lectura o la certeza es baja, la pantalla avisa que un operador continúa la atención. El cliente no vuelve a contar el caso.",
        ],
    )


def section_casos(doc):
    h(doc, "4. Casos de uso")
    para(
        doc,
        "El MVP se cubre con seis casos de uso de comprensión y tres extensiones de salida. "
        "Enviar el mensaje y obtener una decisión es la única entrada. Clasificar, extraer, "
        "estimar la confianza, resumir y elegir una acción ocurren siempre, como inclusiones. "
        "De las tres extensiones se ejecuta exactamente una, según la condición del caso: "
        "remitir, pedir una aclaración o derivar a un operador.",
        align="justify",
    )
    add_table(
        doc,
        ["Caso de uso", "Qué hace", "Relación"],
        [
            ["UC1 Enviar el mensaje y obtener una decisión", "El cliente envía un texto. El motor responde una sola vez con intención, confianza, datos encontrados, datos faltantes, resumen, acción y motivo.", "Caso base. Lo heredan visitante y logueado."],
            ["UC2 Clasificar la intención", "Asigna la etiqueta principal. Si el texto admite otra lectura igual de plausible, conserva esa duda para el veredicto.", "<<include>> de UC1"],
            ["UC3 Extraer datos encontrados y faltantes", "Obtiene lo que aparece y marca lo que el caso exige y no está.", "<<include>> de UC1"],
            ["UC4 Estimar la confianza", "Acompaña la intención con un grado de certeza. Un texto de una sola lectura la mantiene alta. Dos lecturas o un texto vago la bajan.", "<<include>> de UC1"],
            ["UC5 Resumir la solicitud", "Redacta en una o dos frases lo entendido, para que el destino trabaje sobre la lectura.", "<<include>> de UC1"],
            ["UC6 Elegir una sola acción", "Selecciona remitir, pedir aclaración o derivar, y deja el motivo.", "<<include>> de UC1"],
            ["UC7 Remitir el caso", "La intención es única, la confianza alcanza y están los datos mínimos. Solo el usuario logueado.", "<<extend>> de UC6. Lo recibe el proceso de negocio."],
            ["UC8 Pedir una aclaración", "La intención se sostiene y falta un dato que el cliente puede aportar. En el visitante, la identidad cuenta como dato faltante.", "<<extend>> de UC6"],
            ["UC9 Derivar a un operador", "Hay más de una lectura, o la confianza es baja. Vale para los dos actores.", "<<extend>> de UC6. Lo recibe el operador."],
        ],
        [Cm(5.2), Cm(7.4), Cm(4.8)],
    )
    para(
        doc,
        "La poscondición de UC1 es una respuesta con intención, confianza, datos encontrados, "
        "datos faltantes, resumen, acción y motivo. El sistema termina en ese punto.",
        align="justify",
    )
    h(doc, "4.1 Las tres salidas con el mismo relato", 2)
    add_table(
        doc,
        ["Salida", "Mensaje", "Lectura y motivo"],
        [
            [
                "Remitir",
                "«Llevo varios días esperando la devolución de mi dinero del caso 45821, por $120.000, de la compra del 3 de noviembre.»",
                "Intención única de devolución pendiente, confianza alta, datos mínimos completos. El usuario está logueado.",
            ],
            [
                "Pedir aclaración",
                "«Llevo varios días esperando la devolución de mi dinero.»",
                "La intención se sostiene. Faltan caso, monto y fecha. La respuesta nombra esas tres preguntas.",
            ],
            [
                "Derivar",
                "«Llevo varios días esperando la devolución de mi dinero, o quizá fue un cobro de la tarjeta que no reconozco.»",
                "Compiten una devolución pendiente y una transacción no reconocida. La confianza no alcanza para elegir una.",
            ],
        ],
        [Cm(3.2), Cm(7.2), Cm(7.0)],
    )
    h(doc, "4.2 Diagrama de casos de uso", 2)
    para(
        doc,
        "El diagrama separa al visitante del usuario logueado, marca Cliente como actor abstracto "
        "y deja a proceso de negocio y operador como actores secundarios. La gráfica proviene de "
        "la fuente PlantUML que sigue a la figura.",
        align="justify",
    )
    figure(
        doc,
        TALLER / "actividad_2" / "casos_de_uso.png",
        "Figura 1. Casos de uso del identificador de solicitudes, del mensaje escrito a una sola decisión.",
    )
    code_block(
        doc,
        (TALLER / "actividad_2" / "casos_de_uso.puml").read_text(encoding="utf-8"),
        "Fuente PlantUML — casos de uso",
    )


def section_requisitos(doc):
    h(doc, "5. Requisitos funcionales y reglas de negocio")
    h(doc, "5.1 Requisitos funcionales", 2)
    add_table(
        doc,
        ["ID", "Requisito", "Origen"],
        [
            ["RF-01", "Recibir un mensaje en lenguaje natural y devolver una sola decisión.", "UC1"],
            ["RF-02", "Clasificar la intención principal y conservar la duda cuando otra lectura es igual de plausible.", "UC2"],
            ["RF-03", "Extraer entidades, identificadores y atributos presentes, y marcar los atributos ausentes.", "UC3"],
            ["RF-04", "Estimar la confianza de la intención clasificada.", "UC4"],
            ["RF-05", "Redactar un resumen de una o dos frases con lo entendido.", "UC5"],
            ["RF-06", "Elegir exactamente una acción y registrar su motivo.", "UC6"],
            ["RF-07", "Remitir el caso al proceso de negocio cuando el cliente está logueado, la intención es única, la confianza es suficiente y están los datos mínimos del caso.", "UC7"],
            ["RF-08", "Pedir aclaración con preguntas concretas cuando la intención se sostiene y falta un dato que el cliente puede aportar.", "UC8"],
            ["RF-09", "Derivar a un operador cuando hay más de una lectura o la confianza es baja, para visitante y logueado.", "UC9"],
            ["RF-10", "Tratar la aclaración como continuación de la misma solicitud: el mensaje enriquecido vuelve a entrar por POST /api/solicitudes.", "Funcionalidad 8"],
            ["RF-11", "Registrar intención, datos, resumen, confianza y motivo del veredicto para auditoría.", "Funcionalidad 9"],
            ["RF-12", "Mostrar al cliente el resumen y el estado resultante: remitida, incompleta o derivada.", "Recorrido del cliente"],
            ["RF-13", "Correlacionar cada POST /api/solicitudes con la solicitud y responder HTTP 200 en las tres salidas. El destino se distingue en el cuerpo, no en el código de estado.", "Secuencia"],
        ],
        [Cm(1.8), Cm(12.2), Cm(3.4)],
    )
    h(doc, "5.2 Reglas de negocio y de diseño", 2)
    add_table(
        doc,
        ["ID", "Regla"],
        [
            ["RN-01", "De cada mensaje sale una sola acción: REMITIR_PROCESO, SOLICITAR_INFORMACION o DERIVAR_OPERADOR."],
            ["RN-02", "Para una devolución pendiente, los datos mínimos de remisión son número de caso, monto y fecha. El producto se extrae cuando aparece en el texto."],
            ["RN-03", "El usuario visitante no remite el caso. La ausencia de identidad cuenta como dato faltante y la salida correspondiente es pedir aclaración, salvo que el mensaje deba derivarse."],
            ["RN-04", "Intérprete y extractor trabajan a la vez sobre el texto crudo. El extractor no espera la intención, para poder detectar después un desajuste entre lo clasificado y lo extraído."],
            ["RN-05", "El análisis contextual ocurre después de las dos salidas anteriores. Resume, marca ambigüedades y juzga si la información alcanza."],
            ["RN-06", "El coordinador integra la salida. El validador decide la acción. Clasificar, extraer y resumir no autorizan por sí solos el paso al siguiente proceso."],
            ["RN-07", "SOLICITAR_INFORMACION no abre otro flujo ni otra identidad. La aclaración reutiliza la misma cadena de entrada."],
            ["RN-08", "REMITIR_PROCESO publica hacia el proceso de negocio. DERIVAR_OPERADOR deja el caso para el operador. Esas dos publicaciones salen del coordinador, que ya recibió el veredicto."],
            ["RN-09", "Los agentes de comprensión no se invocan entre sí. El validador no habla con el proceso de negocio ni con el operador. La interfaz no llama a los agentes."],
            ["RN-10", "Cada aclaración genera una interpretación nueva. La interpretación anterior se conserva; no se reescribe."],
            ["RN-11", "El estado visible de la solicitud es la proyección de la última decisión."],
        ],
        [Cm(2.0), Cm(15.4)],
    )
    h(doc, "5.3 Datos mínimos del ejemplo", 2)
    para(
        doc,
        "Sobre «Llevo varios días esperando la devolución de mi dinero», el análisis contextual "
        "deja esta lectura: intención de consulta por devolución pendiente, resumen de un dinero "
        "que no ha vuelto tras varios días, información insuficiente porque faltan caso, monto y "
        "fecha. La acción es pedir aclaración y el motivo es que la intención es clara y el "
        "cliente puede aportar esos tres datos.",
        align="justify",
    )


def section_contratos(doc):
    h(doc, "6. Contratos de la respuesta")
    para(
        doc,
        "Cada flecha de retorno del diagrama de secuencia nombra el objeto que la implementación "
        "debe producir. Esos nombres en español son el contrato del flujo. El modelo de datos "
        "del capítulo 7 usa los nombres en inglés de las entidades persistidas. La tabla de "
        "equivalencias cierra los dos vocabularios.",
        align="justify",
    )
    add_table(
        doc,
        ["Objeto", "Campos"],
        [
            ["Intencion", "tipo, confianza"],
            ["DatosRelevantes", "entidades, identificadores, atributosAusentes"],
            ["AnalisisContextual", "resumen, ambiguedades, datosFaltantes, suficiente"],
            ["SalidaIntegrada", "intencion, datos, analisis"],
            ["Veredicto", "cumpleRequisitos, accion, motivo"],
        ],
        [Cm(4.5), Cm(12.9)],
    )
    para(
        doc,
        "accion solo admite REMITIR_PROCESO, SOLICITAR_INFORMACION o DERIVAR_OPERADOR. "
        "Cuando la acción pide aclaración, la respuesta al cliente incluye además las preguntas.",
        align="justify",
    )
    h(doc, "6.1 Equivalencia de nombres", 2)
    add_table(
        doc,
        ["En el flujo y en la API", "En el modelo persistido", "Significado"],
        [
            ["RECIBIDA", "RECEIVED", "La solicitud existe y el mensaje acaba de entrar."],
            ["INCOMPLETA", "INCOMPLETE", "La última decisión pidió una aclaración."],
            ["REMITIDA", "FORWARDED", "La última decisión remitió el caso."],
            ["DERIVADA", "ESCALATED", "La última decisión dejó el caso al operador."],
            ["REMITIR_PROCESO", "FORWARD_TO_PROCESS", "Publicar el caso hacia el proceso de negocio."],
            ["SOLICITAR_INFORMACION", "REQUEST_INFORMATION", "Devolver preguntas al cliente por la misma llamada."],
            ["DERIVAR_OPERADOR", "ESCALATE_TO_OPERATOR", "Dejar el caso en la cola del operador."],
        ],
        [Cm(5.2), Cm(5.4), Cm(6.8)],
    )
    h(doc, "6.2 Cuerpo de la respuesta HTTP", 2)
    para(
        doc,
        "Las tres ramas responden 200. El cuerpo distingue el destino y transporta la decisión "
        "completa que exige el MVP.",
        align="justify",
    )
    add_table(
        doc,
        ["Campo de la respuesta", "Origen"],
        [
            ["estado", "REMITIDA, INCOMPLETA o DERIVADA"],
            ["intencion.tipo y confianza", "Intencion"],
            ["datos encontrados", "entidades e identificadores"],
            ["datos faltantes", "atributosAusentes y datosFaltantes"],
            ["resumen", "AnalisisContextual.resumen"],
            ["accion y motivo", "Veredicto"],
            ["preguntas", "Solo cuando la acción es SOLICITAR_INFORMACION"],
        ],
        [Cm(6.0), Cm(11.4)],
    )


def section_modelo(doc):
    h(doc, "7. Modelo de datos")
    para(
        doc,
        "Tres entidades sostienen el identificador. Request es la solicitud que el cliente va "
        "construyendo. Interpretation es lo que el motor entendió en un paso. Decision es la "
        "única acción que sale de esa interpretación. La solicitud es la raíz. Vive mientras el "
        "cliente aclara el caso y concentra el estado visible del trámite.",
        align="justify",
    )
    h(doc, "7.1 Request", 2)
    para(
        doc,
        "El texto no vive aquí como un único string definitivo. Cada envío del cliente es una "
        "vuelta sobre la misma solicitud.",
        align="justify",
    )
    add_table(
        doc,
        ["Campo", "Rol"],
        [
            ["id", "Identidad del caso."],
            ["status", "RECEIVED, INCOMPLETE, FORWARDED o ESCALATED."],
            ["correlationId", "Une el POST /api/solicitudes con la respuesta."],
            ["createdAt", "Orden y auditoría del hilo."],
        ],
        [Cm(4.2), Cm(13.2)],
    )
    h(doc, "7.2 Interpretation", 2)
    para(
        doc,
        "Es el resultado de un paso de comprensión sobre el mensaje ya enriquecido. No decide "
        "el destino. Intención, entidades y resumen son valores de esta interpretación: si el "
        "cliente aclara, se produce otra interpretación y la anterior permanece.",
        align="justify",
    )
    add_table(
        doc,
        ["Campo", "Rol"],
        [
            ["intentType", "Etiqueta principal, por ejemplo devolución pendiente."],
            ["confidence", "Certeza de esa etiqueta."],
            ["entities", "Lo que sí aparece: espera, dinero, devolución."],
            ["identifiers", "Caso, monto, fecha o producto cuando vienen en el texto."],
            ["missingFields", "Lo que el caso exige y no está."],
            ["summary", "Una o dos frases de lo entendido."],
            ["ambiguities", "Lecturas en pugna."],
            ["sufficient", "Si los datos alcanzan para un caso concreto."],
        ],
        [Cm(4.2), Cm(13.2)],
    )
    h(doc, "7.3 Decision", 2)
    para(doc, "Es el veredicto de una interpretación. El motor responde una sola vez con ella.", align="justify")
    add_table(
        doc,
        ["Campo", "Rol"],
        [
            ["action", "FORWARD_TO_PROCESS, REQUEST_INFORMATION o ESCALATE_TO_OPERATOR."],
            ["meetsRequirements", "Si la interpretación pasa las reglas del caso."],
            ["reason", "Por qué se eligió esa acción."],
            ["questions", "Solo cuando la acción pide aclaración. En el ejemplo: caso, monto y fecha."],
        ],
        [Cm(4.2), Cm(13.2)],
    )
    h(doc, "7.4 Relaciones", 2)
    bullets(
        doc,
        [
            "Una Request acumula cero o varias Interpretation. El primer mensaje y cada aclaración vuelven a entrar por el mismo POST y generan una interpretación nueva.",
            "Cada Interpretation produce una sola Decision.",
            "El status de Request es la proyección de la última decisión: remitir deja FORWARDED, pedir datos deja INCOMPLETE y derivar deja ESCALATED.",
        ],
    )
    para(
        doc,
        "Con el ejemplo, la solicitud nace en RECEIVED. La interpretación marca intención de "
        "devolución pendiente, confianza suficiente para esa etiqueta, faltantes de caso, monto "
        "y fecha, y sufficient en falso. La decisión pide aclaración y nombra esas tres preguntas. "
        "Si el cliente responde en el mismo hilo, nace otra interpretación sobre el mismo caso.",
        align="justify",
    )
    figure(
        doc,
        BUILD / "modelo_datos.png",
        "Figura 2. Request acumula interpretaciones y cada interpretación produce una decisión. "
        "La gráfica está en horizontal para la lectura impresa; la fuente del modelo es el Mermaid siguiente.",
        max_h=Cm(8),
    )
    code_block(doc, MERMAID_ER, "Fuente Mermaid — modelo de datos")


def section_identidades(doc):
    h(doc, "8. Interacción de identidades")
    para(
        doc,
        "Este diagrama fija quién puede hablar con quién. El de secuencia, en el capítulo siguiente, "
        "ordena los mismos mensajes en el tiempo. Cada caja es una identidad, escrita como "
        "instancia : tipo. Cada flecha es una interacción permitida. Si dos identidades no están "
        "unidas, no se hablan: el intérprete no llama al extractor, el análisis no llama al "
        "validador y el validador no remite el caso ni lo deriva.",
        align="justify",
    )
    para(
        doc,
        "La numeración de las flechas es la del diagrama de secuencia, para cruzar ambos sin "
        "cambiar de contrato. Los números que no aparecen en la tabla son trabajo interno de una "
        "identidad o la respuesta de una flecha que ya está listada.",
        align="justify",
    )
    add_table(
        doc,
        ["Flecha", "De", "Hacia", "Mensaje", "Vuelta"],
        [
            ["1", "Cliente", "Interfaz", "solicitud", "resultado"],
            ["2", "Interfaz", "API", "POST /api/solicitudes", "200"],
            ["4", "API", "Coordinador", "analizar(mensaje)", "Resultado"],
            ["5", "Coordinador", "Intérprete", "identificarIntencion", "Intencion"],
            ["8", "Coordinador", "Extractor", "extraerDatos", "DatosRelevantes"],
            ["11", "Coordinador", "Análisis", "analizarContexto", "AnalisisContextual"],
            ["15", "Coordinador", "Validador", "validar", "Veredicto"],
            ["18", "Coordinador", "Proceso", "remitir", "Acuse, solo si la acción es REMITIR_PROCESO"],
            ["26", "Coordinador", "Operador", "derivar", "Acuse, solo si la acción es DERIVAR_OPERADOR"],
        ],
        [Cm(1.8), Cm(3.0), Cm(3.0), Cm(4.2), Cm(5.4)],
    )
    callout(
        doc,
        "Intérprete y extractor solo se conectan al coordinador, así que pueden ejecutarse a la "
        "vez sobre el mismo mensaje. La flecha 15 devuelve el veredicto. Las flechas 18 y 26 "
        "salen del coordinador. Si la acción es SOLICITAR_INFORMACION, la vuelta al cliente usa "
        "las flechas 4, 2 y 1.",
    )
    figure(
        doc,
        TALLER / "actividad_1" / "proyecto_nlu" / "interaccion_identidades.png",
        "Figura 3. Interacción de identidades del motor NLU. La ausencia de flecha es una regla.",
    )
    code_block(
        doc,
        (TALLER / "actividad_1" / "proyecto_nlu" / "interaccion_identidades.puml").read_text(encoding="utf-8"),
        "Fuente PlantUML — interacción de identidades",
    )


def section_secuencia(doc):
    h(doc, "9. Secuencia de la identificación")
    para(
        doc,
        "El flujo empieza cuando el cliente escribe en lenguaje natural y termina en una de tres "
        "salidas. La interfaz no llama a los agentes. El paralelo existe solo entre intérprete y "
        "extractor. El análisis contextual es posterior porque necesita las dos salidas para "
        "resumir y para marcar huecos o contradicciones.",
        align="justify",
    )
    numbered(
        doc,
        [
            "Recepción. El cliente envía el mensaje. La API lo deja en estado RECIBIDA y llama a analizar(mensaje).",
            "Intención y datos, en paralelo. El intérprete devuelve Intencion. El extractor devuelve DatosRelevantes.",
            "Suficiencia y ambigüedad. El análisis contextual recibe el mensaje, la intención y los datos, y devuelve AnalisisContextual.",
            "Integración. El coordinador arma una sola SalidaIntegrada.",
            "Validación y destino. El validador devuelve un Veredicto. El coordinador ejecuta la acción y la API responde 200 con el estado correspondiente.",
        ],
    )
    add_table(
        doc,
        ["Acción", "Condición en el ejemplo", "Respuesta al cliente"],
        [
            ["REMITIR_PROCESO", "La salida cumple los requisitos del caso.", "200 con estado REMITIDA, resumen e intención. El proceso acusa recibo."],
            ["SOLICITAR_INFORMACION", "Faltan datos que el cliente puede aclarar.", "200 con estado INCOMPLETA, resumen y preguntas. En el ejemplo: caso, monto y fecha."],
            ["DERIVAR_OPERADOR", "La ambigüedad no se resuelve con otra pregunta, o la confianza no alcanza.", "200 con estado DERIVADA, resumen y motivo. El operador acusa la toma."],
        ],
        [Cm(4.6), Cm(6.2), Cm(6.6)],
    )
    para(
        doc,
        "La secuencia fija el recorrido de una solicitud ya recibida. La persistencia, la "
        "autenticación y el alojamiento del modelo están en la arquitectura del capítulo 10, "
        "sin cambiar el orden de los agentes ni las tres salidas.",
        align="justify",
    )
    figure(
        doc,
        TALLER / "actividad_1" / "proyecto_nlu" / "secuencia_identificacion_solicitudes.png",
        "Figura 4. Secuencia de la identificación de solicitudes, del mensaje del cliente a la decisión.",
        max_h=Cm(21.5),
    )
    code_block(
        doc,
        (TALLER / "actividad_1" / "proyecto_nlu" / "secuencia_identificacion_solicitudes.puml").read_text(encoding="utf-8"),
        "Fuente PlantUML — diagrama de secuencia",
    )


def section_arquitectura(doc):
    h(doc, "10. Arquitectura de despliegue")
    para(
        doc,
        "Hay dos vistas de despliegue y un invariante. El invariante es el de los capítulos 8 y 9: "
        "una sola puerta de entrada, el coordinador como único acceso a los agentes, y tres salidas "
        "distintas. La primera vista es el despliegue tentativo en AWS, con la API como único "
        "ingreso a la VPC. La segunda separa cada capacidad en un microservicio con su propia base, "
        "para cuando haya que escalar el modelo o aislar al validador. El primer código puede vivir "
        "en menos contenedores —React y un proceso Node— siempre que las llamadas respeten ese grafo.",
        align="justify",
    )
    h(doc, "10.1 Despliegue tentativo en AWS", 2)
    para(
        doc,
        "El cliente entra por Route 53, WAF y CloudFront. CloudFront entrega el React desde S3 "
        "y reenvía /api/* a API Gateway. Cognito autoriza al cliente antes de que la petición "
        "cruce a la VPC. API Gateway llega solo a la API Node, por VPC Link. Esa API es la única "
        "tarea con entrada desde el borde.",
        align="justify",
    )
    para(
        doc,
        "La API guarda el estado de la solicitud en Aurora y llama a analizar(mensaje) en el "
        "coordinador. El coordinador dispara intérprete y extractor en paralelo, después el "
        "análisis contextual y al final el validador. Intérprete, extractor y análisis llaman a "
        "Bedrock. El validador no llama al modelo: contrasta la salida con las reglas del caso. "
        "Aurora, Cognito, WAF y CloudWatch cubren estado, acceso, borde y trazas. No son "
        "identidades del flujo.",
        align="justify",
    )
    add_table(
        doc,
        ["Identidad", "Dónde queda en AWS"],
        [
            ["Cliente", "Persona frente a CloudFront."],
            ["Interfaz web", "React en S3, servido por CloudFront."],
            ["API de solicitudes", "API Gateway más la tarea Fargate de la API Node."],
            ["Coordinador", "Tarea Fargate. Solo la API la invoca."],
            ["Intérprete, extractor y análisis", "Tareas Fargate del grupo Comprensión. Solo ellas usan Bedrock."],
            ["Validador", "Tarea Fargate del grupo Control. No llama al modelo ni publica eventos."],
            ["Proceso de negocio", "Consumidor del evento en EventBridge."],
            ["Operador", "Persona que toma el mensaje dejado en SQS."],
        ],
        [Cm(5.6), Cm(11.8)],
    )
    add_table(
        doc,
        ["Acción", "Camino en AWS", "Qué ve el cliente"],
        [
            ["REMITIR_PROCESO", "El coordinador publica en EventBridge y espera el acuse del siguiente proceso.", "200 con estado REMITIDA."],
            ["SOLICITAR_INFORMACION", "No hay otro servicio. El resultado vuelve por la misma llamada analizar.", "200 con estado INCOMPLETA y las preguntas."],
            ["DERIVAR_OPERADOR", "El coordinador deja el caso en SQS. El acuse es el de haberlo encolado.", "200 con estado DERIVADA."],
        ],
        [Cm(4.8), Cm(7.6), Cm(5.0)],
    )
    bullets(
        doc,
        [
            "Una sola entrada a la VPC. El VPC Link termina en la API. Coordinador, agentes, validador y Aurora no se publican.",
            "Bedrock no lo llama la API, ni el coordinador, ni el validador.",
            "El paralelo es de red: intérprete y extractor son dos tareas porque el coordinador las llama a la vez. El análisis espera a que ambas respondan.",
            "El estado lo escribe la API. Aurora guarda la correlación y el paso de RECIBIDA a REMITIDA, INCOMPLETA o DERIVADA. Los agentes devuelven su objeto y no abren la base.",
            "Las tareas consumen Bedrock, SQS y EventBridge por endpoints de VPC. Esos endpoints no se dibujan para no tapar el recorrido de la solicitud.",
        ],
    )
    figure(
        doc,
        TALLER / "actividad_1" / "proyecto_nlu" / "arquitectura_nlu_aws.png",
        "Figura 5. Arquitectura AWS tentativa del motor NLU. Una sola entrada a la VPC y tres salidas.",
        max_h=Cm(21.5),
    )
    para(
        doc,
        "La gráfica se genera con el script arquitectura_aws.py de la librería Diagrams, desde "
        "la carpeta del proyecto NLU y con Graphviz instalado.",
        size=10,
        italic=True,
        color=MUTED,
    )
    h(doc, "10.2 Microservicios, cada uno con su base", 2)
    para(
        doc,
        "Cuando cada capacidad se separa, el frontend sigue hablando solo con la API, cada "
        "microservicio tiene su propia base y el borde usa los mismos servicios de AWS. En esta "
        "vista, API Gateway llega a Requests API a través de un Application Load Balancer, que "
        "reparte únicamente hacia esa API. Cognito autoriza la llamada y no es un salto hacia "
        "el balanceador. El coordinador sigue siendo el único que llama a los demás servicios.",
        align="justify",
    )
    add_table(
        doc,
        ["Microservicio", "Base propia", "Qué guarda"],
        [
            ["Requests API", "Aurora PostgreSQL", "Request"],
            ["Coordinator", "DynamoDB", "Interpretation ya integrada"],
            ["Interpreter", "DynamoDB", "intentType y confidence"],
            ["Extractor", "DynamoDB", "entities e identifiers"],
            ["Context analysis", "DynamoDB", "summary, ambiguities, missingFields y sufficient"],
            ["Validator", "DynamoDB", "Decision"],
        ],
        [Cm(4.4), Cm(4.4), Cm(8.6)],
    )
    para(
        doc,
        "Intérprete, extractor y análisis contextual llaman a Bedrock y no se llaman entre sí. "
        "El validador no usa el modelo. REQUEST_INFORMATION vuelve por la misma llamada. "
        "FORWARD_TO_PROCESS sale por EventBridge hacia el proceso de negocio. "
        "ESCALATE_TO_OPERATOR deja el caso en SQS para el operador. La API proyecta esa acción "
        "en Request.status.",
        align="justify",
    )
    figure(
        doc,
        BUILD / "microservicios.png",
        "Figura 6. Microservicios del motor NLU en AWS. Cada servicio tiene su base; el cliente entra por CloudFront y la API es la única tarea publicada.",
        max_h=Cm(18),
    )
    code_block(
        doc,
        (BUILD / "microservicios.mmd").read_text(encoding="utf-8"),
        "Fuente Mermaid — arquitectura de microservicios",
    )
    callout(
        doc,
        "Las dos vistas conviven así: el despliegue tentativo escribe el estado de la solicitud "
        "en Aurora y mantiene a los agentes detrás del coordinador. La vista de microservicios "
        "añade una base por servicio y sitúa el balanceador entre API Gateway y Requests API. "
        "En las dos, solo la API se publica, solo el coordinador llama a los agentes, solo la "
        "comprensión usa Bedrock y las tres acciones conservan su camino.",
    )


def section_trazabilidad(doc):
    h(doc, "11. Correspondencia con los artefactos del taller")
    para(
        doc,
        "Cada capítulo de esta especificación sale de un artefacto ya construido. La tabla "
        "permite volver del requisito a la fuente.",
        align="justify",
    )
    add_table(
        doc,
        ["Capítulo", "Artefacto"],
        [
            ["3. Funcionalidades, beneficios y recorrido", "taller_hito_1/actividad_2/respuestas_actividad_2.md, prompts 1 a 3"],
            ["4. Casos de uso", "respuestas_actividad_2.md, prompts 4 y 5; casos_de_uso.puml y casos_de_uso.png"],
            ["7. Modelo de datos", "respuestas_actividad_2.md, prompt 6, diagrama Mermaid"],
            ["8. Interacción de identidades", "diagrama_interaccion_identidades.md, interaccion_identidades.puml y su PNG"],
            ["9. Secuencia", "diagrama_secuencia.md, secuencia_identificacion_solicitudes.puml y su PNG"],
            ["10.1 Despliegue tentativo", "arquitectura_aws.md, arquitectura_aws.py y arquitectura_nlu_aws.png"],
            ["10.2 Microservicios", "respuestas_actividad_2.md, prompt 7, diagrama Mermaid"],
        ],
        [Cm(5.6), Cm(11.8)],
    )
    para(
        doc,
        "Los diagramas de casos de uso, de interacción y de secuencia quedan en el documento "
        "como gráfica y como fuente PlantUML. El modelo de datos y la arquitectura de "
        "microservicios quedan como gráfica y como fuente Mermaid. La arquitectura AWS "
        "tentativa queda como la gráfica generada por Diagrams.",
        align="justify",
    )
    para(
        doc,
        "Versión 1.0. Consolida el trabajo del motor NLU hasta el 12 de noviembre de 2026.",
        size=10,
        italic=True,
        color=MUTED,
    )


def main():
    BUILD.mkdir(parents=True, exist_ok=True)
    doc = Document()
    configure(doc)
    cover(doc)
    section_proposito(doc)
    section_actores(doc)
    section_valor(doc)
    section_casos(doc)
    section_requisitos(doc)
    section_contratos(doc)
    section_modelo(doc)
    section_identidades(doc)
    section_secuencia(doc)
    section_arquitectura(doc)
    section_trazabilidad(doc)
    doc.save(OUT)
    print(OUT)


if __name__ == "__main__":
    main()
