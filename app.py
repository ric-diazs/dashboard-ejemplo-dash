from dash import Dash, dcc, html, dash_table
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


# ---------------------------------------------------------------------
# Datos de ejemplo
# Sustituye estos valores por los datos exportados desde Microsoft Project
# y por la información de costos y riesgos de tu proyecto.
# ---------------------------------------------------------------------

presupuesto_aprobado = 250.0  # Miles de unidades monetarias

# PV: Planned Value; EV: Earned Value; AC: Actual Cost.
# Los tres valores deben corresponder al mismo corte de reporte.
fases = pd.DataFrame(
    [
        {
            "Fase": "Inicio y planificación",
            "PV": 25.0,
            "EV": 25.0,
            "AC": 28.0,
            "Alcance total": 8,
            "Entregables aceptados": 8,
        },
        {
            "Fase": "Análisis de requisitos",
            "PV": 45.0,
            "EV": 40.0,
            "AC": 43.0,
            "Alcance total": 12,
            "Entregables aceptados": 10,
        },
        {
            "Fase": "Diseño",
            "PV": 35.0,
            "EV": 30.0,
            "AC": 32.0,
            "Alcance total": 10,
            "Entregables aceptados": 8,
        },
        {
            "Fase": "Desarrollo",
            "PV": 20.0,
            "EV": 15.0,
            "AC": 18.0,
            "Alcance total": 20,
            "Entregables aceptados": 5,
        },
        {
            "Fase": "Pruebas",
            "PV": 0.0,
            "EV": 0.0,
            "AC": 0.0,
            "Alcance total": 12,
            "Entregables aceptados": 0,
        },
        {
            "Fase": "Implementación",
            "PV": 0.0,
            "EV": 0.0,
            "AC": 0.0,
            "Alcance total": 6,
            "Entregables aceptados": 0,
        },
    ]
)

riesgos = pd.DataFrame(
    [
        {
            "ID": "R-01",
            "Riesgo": "Retraso en la aprobación de requisitos",
            "Probabilidad": 4,
            "Impacto": 5,
            "Responsable": "Jefe de proyecto",
            "Respuesta": "Escalar pendientes y fijar fecha límite de aprobación",
            "Estado": "Abierto",
        },
        {
            "ID": "R-02",
            "Riesgo": "Disponibilidad limitada de expertos del cliente",
            "Probabilidad": 3,
            "Impacto": 4,
            "Responsable": "Líder funcional",
            "Respuesta": "Reservar sesiones de validación con anticipación",
            "Estado": "En tratamiento",
        },
        {
            "ID": "R-03",
            "Riesgo": "Cambios de alcance durante el desarrollo",
            "Probabilidad": 4,
            "Impacto": 4,
            "Responsable": "Comité de cambios",
            "Respuesta": "Evaluar solicitudes mediante control formal de cambios",
            "Estado": "Abierto",
        },
        {
            "ID": "R-04",
            "Riesgo": "Defectos críticos en pruebas de aceptación",
            "Probabilidad": 2,
            "Impacto": 5,
            "Responsable": "Líder de QA",
            "Respuesta": "Revisiones tempranas y criterios de aceptación trazables",
            "Estado": "En seguimiento",
        },
    ]
)

# ---------------------------------------------------------------------
# Cálculos de KPIs
# ---------------------------------------------------------------------

pv = fases["PV"].sum()
ev = fases["EV"].sum()
ac = fases["AC"].sum()

cpi = ev / ac if ac else 0
spi = ev / pv if pv else 0

avance_planificado = (pv / presupuesto_aprobado) * 100
avance_real = (ev / presupuesto_aprobado) * 100
presupuesto_consumido = (ac / presupuesto_aprobado) * 100

entregables_totales = fases["Alcance total"].sum()
entregables_aceptados = fases["Entregables aceptados"].sum()
avance_alcance = (
    entregables_aceptados / entregables_totales * 100
    if entregables_totales
    else 0
)

riesgos["Exposición"] = riesgos["Probabilidad"] * riesgos["Impacto"]
riesgos["Nivel"] = riesgos["Exposición"].apply(
    lambda valor: "Alto" if valor >= 16 else "Medio" if valor >= 9 else "Bajo"
)

# ---------------------------------------------------------------------
# Gráficos
# ---------------------------------------------------------------------

fig_avance = go.Figure()

fig_avance.add_trace(
    go.Bar(
        name="Planificado (PV)",
        x=fases["Fase"],
        y=fases["PV"],
        marker_color="#9db7d5",
    )
)
fig_avance.add_trace(
    go.Bar(
        name="Valor ganado (EV)",
        x=fases["Fase"],
        y=fases["EV"],
        marker_color="#2878b5",
    )
)
fig_avance.add_trace(
    go.Bar(
        name="Costo real (AC)",
        x=fases["Fase"],
        y=fases["AC"],
        marker_color="#e29d45",
    )
)

fig_avance.update_layout(
    title="Valor planificado, valor ganado y costo real por fase",
    barmode="group",
    xaxis_title="Fase",
    yaxis_title="Miles de unidades monetarias",
    legend_title="Métrica",
    margin=dict(l=30, r=20, t=60, b=100),
)

fig_alcance = px.bar(
    fases,
    x="Fase",
    y=["Entregables aceptados", "Alcance total"],
    barmode="group",
    title="Entregables aceptados frente al alcance total",
    labels={"value": "Número de entregables", "variable": "Métrica"},
    color_discrete_map={
        "Entregables aceptados": "#2878b5",
        "Alcance total": "#d7e1ec",
    },
)
fig_alcance.update_layout(margin=dict(l=30, r=20, t=60, b=100))

fig_riesgos = px.scatter(
    riesgos,
    x="Probabilidad",
    y="Impacto",
    size="Exposición",
    color="Nivel",
    text="ID",
    hover_name="Riesgo",
    color_discrete_map={
        "Bajo": "#4c9f70",
        "Medio": "#e4aa36",
        "Alto": "#d9534f",
    },
    title="Matriz de probabilidad e impacto de riesgos",
    range_x=[0.5, 5.5],
    range_y=[0.5, 5.5],
)
fig_riesgos.update_traces(textposition="top center")
fig_riesgos.update_layout(
    xaxis=dict(dtick=1, title="Probabilidad (1–5)"),
    yaxis=dict(dtick=1, title="Impacto (1–5)"),
    margin=dict(l=30, r=20, t=60, b=40),
)

# ---------------------------------------------------------------------
# Componentes reutilizables
# ---------------------------------------------------------------------


def tarjeta(titulo, valor, detalle, color="#2878b5"):
    return html.Div(
        [
            html.Div(titulo, className="kpi-title"),
            html.Div(valor, className="kpi-value", style={"color": color}),
            html.Div(detalle, className="kpi-detail"),
        ],
        className="kpi-card",
    )



def color_indice(valor):
    if valor >= 1:
        return "#26834a"
    if valor >= 0.9:
        return "#c58a00"
    return "#c0392b"


# ---------------------------------------------------------------------
# Aplicación Dash
# ---------------------------------------------------------------------

app = Dash(__name__)
app.title = "Dashboard de proyecto"

app.layout = html.Div(
    [
        html.H1("Dashboard de seguimiento del proyecto", className="page-title"),
        html.P(
            "Proyecto de software · Enfoque cascada · "
            "Corte de reporte: sustituir por la fecha correspondiente",
            className="page-subtitle",
        ),

        html.Div(
            [
                tarjeta(
                    "Presupuesto aprobado",
                    f"{presupuesto_aprobado:,.1f}",
                    "Miles de unidades monetarias",
                ),
                tarjeta(
                    "Costo real acumulado",
                    f"{ac:,.1f}",
                    f"{presupuesto_consumido:.1f}% del presupuesto consumido",
                    "#e29d45",
                ),
                tarjeta(
                    "CPI · eficiencia de costos",
                    f"{cpi:.2f}",
                    "EV / AC · mayor que 1 es favorable",
                    color_indice(cpi),
                ),
                tarjeta(
                    "SPI · desempeño del cronograma",
                    f"{spi:.2f}",
                    "EV / PV · mayor que 1 es favorable",
                    color_indice(spi),
                ),
                tarjeta(
                    "Avance del alcance",
                    f"{avance_alcance:.1f}%",
                    f"{entregables_aceptados} de {entregables_totales} entregables aceptados",
                ),
            ],
            className="kpi-grid",
        ),

        html.Div(
            [
                dcc.Graph(figure=fig_avance, style={"flex": "2", "minWidth": "500px"}),
                dcc.Graph(figure=fig_alcance, style={"flex": "1", "minWidth": "380px"}),
            ],
            className="chart-grid",
        ),

        html.Div(
            [
                html.H2("Riesgos", className="section-title"),

                dcc.Graph(figure=fig_riesgos, className="chart", config={"displayModeBar": False}),

                dash_table.DataTable(
                    data=riesgos.to_dict("records"),
                    columns=[
                        {"name": "ID", "id": "ID"},
                        {"name": "Riesgo", "id": "Riesgo"},
                        {"name": "Probabilidad", "id": "Probabilidad"},
                        {"name": "Impacto", "id": "Impacto"},
                        {"name": "Exposición", "id": "Exposición"},
                        {"name": "Nivel", "id": "Nivel"},
                        {"name": "Responsable", "id": "Responsable"},
                        {"name": "Respuesta", "id": "Respuesta"},
                        {"name": "Estado", "id": "Estado"},
                    ],
                    style_table={"overflowX": "auto"},
                    style_cell={
                        "textAlign": "left",
                        "padding": "8px",
                        "whiteSpace": "normal",
                        "height": "auto",
                        "minWidth": "100px",
                    },
                    style_header={
                        "backgroundColor": "#edf2f7",
                        "fontWeight": "bold",
                    },
                    style_data_conditional=[
                        {
                            "if": {"filter_query": '{Nivel} = "Alto"'},
                            "backgroundColor": "#fde2e2",
                        },
                        {
                            "if": {"filter_query": '{Nivel} = "Medio"'},
                            "backgroundColor": "#fff3cd",
                        },
                    ],
                ),
            ],
            className="panel",
        ),

        html.P(
            [
                "Avance planificado del presupuesto: ",
                html.B(f"{avance_planificado:.1f}%"),
                " · Avance ganado: ",
                html.B(f"{avance_real:.1f}%"),
            ],
            className="summary-line",
        ),
    ],
    className="page",
)

if __name__ == "__main__":
    app.run(debug=True)
