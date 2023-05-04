# Imports
import pandas as pd
import plotly.graph_objs as go
import plotly # To export chart to HTML

# CSV VERSION
df = pd.read_csv('Japan-1950.csv')

y = df['Age']
x1 = df['M']
x2 = df['F'] * -1


# Create instance of the figure
fig = go.Figure()

# Add Trace to Figure
fig.add_trace(go.Bar(
        y=y,
        x=x1,
        name='Male',
        orientation='h'
))

# Add Trace to figure
fig.add_trace(go.Bar(
        y=y,
        x=x2,
        name='Female',
        orientation='h'
))

# Update Figure Layout
fig.update_layout(
    template = 'plotly_white',
    title= 'Age Pyramid Japan 1950',
    title_font_size = 24,
    barmode='relative',
    bargap=0.0,
    bargroupgap=0,
    xaxis=dict(
        tickvals=[-4000000,-2000000,0,2000000,4000000],
        ticktext=['4M','2M','0','2M','4M'],
        title='Population in Mio',
        title_font_size=14
    )
)

# Plot figure
fig.show()

# Export Candlestick to HTML
#plotly.offline.plot(fig, filename='population_pyramid.html')
