"""
Generador de informes PDF para diagnosticos preliminares.
"""

# pyright: reportMissingImports=false, reportMissingModuleSource=false

import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.graphics.shapes import Drawing, Rect, String
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak


PAGE_WIDTH, PAGE_HEIGHT = A4


def _safe_text(value, fallback="N/A"):
    text = str(value).strip() if value is not None else ""
    return text or fallback


def _build_styles():
    styles = getSampleStyleSheet()

    styles.add(
        ParagraphStyle(
            name="ReportTitle",
            parent=styles["Heading1"],
            fontSize=18,
            leading=22,
            textColor=colors.HexColor("#0B3C5D"),
            spaceAfter=8,
        )
    )
    styles.add(
        ParagraphStyle(
            name="SectionTitle",
            parent=styles["Heading2"],
            fontSize=12,
            leading=15,
            textColor=colors.HexColor("#1D5D8F"),
            spaceAfter=6,
            spaceBefore=8,
        )
    )
    styles.add(
        ParagraphStyle(
            name="SmallLabel",
            parent=styles["Normal"],
            fontSize=9,
            leading=11,
            textColor=colors.HexColor("#4A4A4A"),
        )
    )
    styles.add(
        ParagraphStyle(
            name="WarningText",
            parent=styles["Normal"],
            fontSize=9,
            leading=12,
            textColor=colors.HexColor("#7A1A0E"),
        )
    )

    return styles


def _build_stamp(styles, report_data):
    stamp_text = _safe_text(report_data.get("system_stamp"), "MediLogic")
    generated_at = _safe_text(report_data.get("generated_at"))
    report_id = _safe_text(report_data.get("report_id"))

    stamp_table = Table(
        [
            [Paragraph(f"<b>{stamp_text}</b>", styles["Normal"])],
            [Paragraph(f"Informe ID: {report_id} | Fecha: {generated_at}", styles["SmallLabel"])],
        ],
        colWidths=[180 * mm],
    )
    stamp_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#D6EAF8")),
                ("BACKGROUND", (0, 1), (-1, 1), colors.HexColor("#EBF5FB")),
                ("BOX", (0, 0), (-1, -1), 0.8, colors.HexColor("#2471A3")),
                ("INNERGRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#2471A3")),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    return stamp_table


def _build_profile_table(styles, report_data):
    profile = report_data.get("patient_profile", {})
    symptoms = profile.get("symptoms", [])
    symptom_items = [f"{s.get('name', 'N/A')} ({s.get('severity', 'Moderado')})" for s in symptoms]

    table_data = [
        ["Sintomas", ", ".join(symptom_items) or "No reportados"],
        ["Alergias", ", ".join(profile.get("allergies", [])) or "No reportadas"],
        ["Condiciones cronicas", ", ".join(profile.get("chronic_diseases", [])) or "No reportadas"],
    ]

    table = Table(table_data, colWidths=[42 * mm, 138 * mm])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#F4F6F7")),
                ("TEXTCOLOR", (0, 0), (0, -1), colors.HexColor("#2C3E50")),
                ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#D5DBDB")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    return table


def _build_summary_table(report_data):
    summary = report_data.get("summary", {})

    rows = [
        ["Total diagnosticos", str(summary.get("diagnosis_count", 0))],
        ["Diagnostico principal", _safe_text(summary.get("top_diagnosis"), "Sin coincidencias")],
        ["Afinidad principal", f"{summary.get('top_affinity_percent', 0.0)}%"],
        ["Urgencia global", _safe_text(summary.get("overall_urgency"), "leve").upper()],
        ["Accion recomendada", _safe_text(summary.get("overall_action"), "Observacion recomendada")],
    ]

    table = Table(rows, colWidths=[48 * mm, 132 * mm])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#EAF2F8")),
                ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#AEB6BF")),
                ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    return table


def _urgency_color(level):
    if level == "severo":
        return colors.HexColor("#C0392B")
    if level == "moderado":
        return colors.HexColor("#D68910")
    return colors.HexColor("#1E8449")


def _build_affinity_chart(diagnoses):
    if not diagnoses:
        drawing = Drawing(160 * mm, 12 * mm)
        drawing.add(String(0, 2 * mm, "Sin datos de afinidad", fontName="Helvetica", fontSize=9))
        return drawing

    width = 175 * mm
    row_height = 7 * mm
    gap = 2 * mm
    label_width = 52 * mm
    bar_width = 88 * mm
    value_offset = label_width + bar_width + 3 * mm

    height = 10 * mm + len(diagnoses) * (row_height + gap)
    drawing = Drawing(width, height)

    y = height - 10 * mm
    for diag in diagnoses:
        name = _safe_text(diag.get("name"))[:22]
        affinity = float(diag.get("affinity_percent", 0.0))
        urgency = _safe_text(diag.get("urgency", {}).get("level"), "leve").lower()
        fill_color = _urgency_color(urgency)

        drawing.add(String(0, y + 1.5 * mm, name, fontName="Helvetica", fontSize=8))
        drawing.add(Rect(label_width, y, bar_width, row_height, strokeColor=colors.HexColor("#B2BABB"), fillColor=colors.white))
        drawing.add(Rect(label_width, y, bar_width * (affinity / 100.0), row_height, strokeColor=None, fillColor=fill_color))
        drawing.add(String(value_offset, y + 1.5 * mm, f"{affinity:.1f}%", fontName="Helvetica", fontSize=8))

        y -= (row_height + gap)

    return drawing


def _build_diagnosis_table(diagnoses):
    headers = ["#", "Diagnostico", "Afinidad", "Urgencia", "Medicamento seguro sugerido"]
    rows = [headers]

    for index, diag in enumerate(diagnoses, start=1):
        med = diag.get("recommended_medication") or {}
        med_name = _safe_text(med.get("nombre"), "Sin alternativa segura")
        rows.append(
            [
                str(index),
                _safe_text(diag.get("name")),
                f"{float(diag.get('affinity_percent', 0.0)):.1f}%",
                _safe_text(diag.get("urgency", {}).get("level"), "leve").upper(),
                med_name,
            ]
        )

    table = Table(rows, colWidths=[10 * mm, 46 * mm, 22 * mm, 26 * mm, 76 * mm])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1D5D8F")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, 0), 8.5),
                ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
                ("FONTSIZE", (0, 1), (-1, -1), 8),
                ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#D5D8DC")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 4),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ]
        )
    )

    return table


def _build_warnings_box(styles, warnings):
    if not warnings:
        warnings = ["Sin advertencias adicionales."]

    warning_lines = "<br/>".join([f"- {_safe_text(w)}" for w in warnings])
    warning_content = Paragraph(f"<b>Advertencias importantes</b><br/>{warning_lines}", styles["WarningText"])

    box = Table([[warning_content]], colWidths=[180 * mm])
    box.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#FDEDEC")),
                ("BOX", (0, 0), (-1, -1), 0.8, colors.HexColor("#CB4335")),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    return box


def _build_rule_lines(diagnosis):
    rules = diagnosis.get("activated_rules", [])
    if not rules:
        return "- Sin reglas detalladas para esta condicion."

    lines = []
    for item in rules:
        rule_name = _safe_text(item.get("rule"), "regla")
        explanation = _safe_text(item.get("explanation"), "sin detalle")
        lines.append(f"- <b>{rule_name}</b>: {explanation}")
    return "<br/>".join(lines)


def _build_diagnosis_detail(styles, diagnosis, index):
    med = diagnosis.get("recommended_medication") or {}
    safe_med = _safe_text(med.get("nombre"), "Sin alternativa segura")
    safe_dose = _safe_text(med.get("dosis"), "No disponible")
    urgency = diagnosis.get("urgency", {})

    blocked_items = diagnosis.get("blocked_medications", [])
    if blocked_items:
        blocked_text = ", ".join(
            [f"{_safe_text(item.get('medicamento'))} ({_safe_text(item.get('motivo'), 'conflicto')})" for item in blocked_items[:5]]
        )
    else:
        blocked_text = "Sin bloqueos relevantes"

    matched = diagnosis.get("matched_symptoms", [])
    matched_text = ", ".join([f"{m.get('name', 'N/A')} ({m.get('severity', 'Moderado')})" for m in matched]) or "No especificado"

    classification = diagnosis.get("classification", {})
    rows = [
        ["Diagnostico", f"{index}. {_safe_text(diagnosis.get('name'))}"],
        ["Afinidad", f"{float(diagnosis.get('affinity_percent', 0.0)):.1f}%"],
        ["Urgencia", f"{_safe_text(urgency.get('level'), 'leve').upper()} | {_safe_text(urgency.get('action'))}"],
        ["Sistema/Tipo", f"{_safe_text(classification.get('sistema'))} / {_safe_text(classification.get('tipo'))}"],
        ["Sintomas vinculados", matched_text],
        ["Medicamento seguro", f"{safe_med} | Dosis: {safe_dose}"],
        ["Medicamentos bloqueados", blocked_text],
        ["Recomendacion", _safe_text(diagnosis.get('recommendation'))],
    ]

    table = Table(rows, colWidths=[42 * mm, 138 * mm])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#F8F9F9")),
                ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#D5DBDB")),
                ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
                ("FONTSIZE", (0, 0), (-1, -1), 8.5),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ]
        )
    )

    rule_title = Paragraph("<b>Reglas Prolog activadas</b>", styles["SmallLabel"])
    rule_body = Paragraph(_build_rule_lines(diagnosis), styles["SmallLabel"])
    return [table, Spacer(1, 2 * mm), rule_title, rule_body, Spacer(1, 4 * mm)]


def generar_pdf_diagnostico(report_data, output_path):
    """
    Genera un informe PDF en la ruta indicada y devuelve la ruta absoluta.
    """
    output_path = os.path.abspath(output_path)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    styles = _build_styles()
    diagnoses = report_data.get("diagnoses", [])

    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=14 * mm,
        rightMargin=14 * mm,
        topMargin=12 * mm,
        bottomMargin=12 * mm,
        title="Informe de Diagnostico MediLogic",
        author="MediLogic",
    )

    story = []

    story.append(_build_stamp(styles, report_data))
    story.append(Spacer(1, 4 * mm))
    story.append(Paragraph("Informe de diagnostico preliminar", styles["ReportTitle"]))
    story.append(Paragraph("Resumen clinico y trazabilidad de inferencia", styles["SmallLabel"]))
    story.append(Spacer(1, 4 * mm))

    story.append(Paragraph("Perfil del paciente", styles["SectionTitle"]))
    story.append(_build_profile_table(styles, report_data))
    story.append(Spacer(1, 3 * mm))

    story.append(Paragraph("Resumen del analisis", styles["SectionTitle"]))
    story.append(_build_summary_table(report_data))
    story.append(Spacer(1, 3 * mm))

    story.append(_build_warnings_box(styles, report_data.get("warnings", [])))
    story.append(Spacer(1, 4 * mm))

    story.append(Paragraph("Diagnosticos ordenados por afinidad", styles["SectionTitle"]))
    story.append(_build_diagnosis_table(diagnoses))
    story.append(Spacer(1, 4 * mm))

    story.append(Paragraph("Grafico de barras de afinidad", styles["SectionTitle"]))
    story.append(_build_affinity_chart(diagnoses))
    story.append(Spacer(1, 4 * mm))

    story.append(PageBreak())
    story.append(Paragraph("Detalle por diagnostico", styles["SectionTitle"]))

    if diagnoses:
        for index, diagnosis in enumerate(diagnoses, start=1):
            story.extend(_build_diagnosis_detail(styles, diagnosis, index))
    else:
        story.append(Paragraph("No se encontraron diagnosticos para detallar.", styles["Normal"]))

    story.append(Spacer(1, 4 * mm))
    story.append(
        Paragraph(
            "Sello visual del sistema: MediLogic | Uso academico y de apoyo clinico preliminar.",
            styles["SmallLabel"],
        )
    )

    doc.build(story)
    return output_path
