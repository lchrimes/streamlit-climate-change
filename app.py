import streamlit as st
from utils.base64_handler import file_to_base64
import pandas as pd
import numpy as np
from numpy.polynomial.polynomial import polyfit
import plotly.graph_objects as go
import plotly.express as px


# Changing title page and the favicon - set page call only be called once per app and only at the start
st.set_page_config(page_title='Climate Awareness', page_icon=file_to_base64("static/images/favicon_symbol.png"))

# Loading carbon data
@st.cache
def load_carbon_data():
  carbonSequesteredDf = pd.read_csv("static/data/TheGreatCarbonSinkInfo-Carbon-Rate.csv")
  return carbonSequesteredDf

# Max lifespan for each tree type
life_span = {
"Maple" : 300,
"Oak" : 1000,
"Sycamore" : 600,
"Pine" : 200,
"Fir" : 1000,
"Elm" : 150,
"Willow" : 75,
"Magnolia" : 120,
"Birch" : 50,
"Tulip" : 500,
"Butternut" : 75,
"Cedar" : 1000,
}

total_sequestered = {
  'Maple': 54,
 'Oak': 1450,
 'Sycamore': 348,
 'Pine': 19,
 'Fir': 1450,
 'Elm': 10,
 'Willow': 2,
 'Magnolia': 6,
 'Birch': 1,
 'Tulip': 211,
 'Butternut': 2,
  'Cedar': 1450}

# Adding sytle sheet
def remote_css(url):
  st.markdown(f'<link href="{url}" rel="stylesheet">', unsafe_allow_html=True)

def execute_markdown(markdown):
  st.markdown(markdown, unsafe_allow_html=True)

# font-awsome addition for icons
remote_css("https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css")

# Add some bootstrap css
execute_markdown('<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">')

# hiding the streamlit menu and footer
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

# Adding the company app logo
logo_image = file_to_base64("static/images/Databound_DATAdiscovery-01.png")

logo_add = f"""
<div class="logo-div">
<a href="https://databound.co.uk">
  <img src="data:image/png;base64, {logo_image}" alt="Red dot" width="450px" heigth="600px" style="padding:10px;"/>
</a>
</div>
"""

st.markdown(logo_add,unsafe_allow_html=True)

# Loading data in dataframe
carbon_sequestered_df = load_carbon_data()

# Header/Title
st.header("The Great Carbon Sink")

# Article Image
st.image("https://cdn.pixabay.com/photo/2015/12/01/20/28/green-1072828_1280.jpg", use_column_width=True)

# Intro
execute_markdown(open("static/html/intro.html","r").read())

# User input into columns
c1 , c2 = st.beta_columns((2,2))

with c1: # user input to col one
  age = st.number_input("What is the age of your tree?",  step=1, value=0)
with c2: # user input to col two
  tree = st.selectbox(
        "Tree Species", # Label
        [ # Tree type list
        "Maple",
        "Oak",
        "Sycamore",
        "Pine",
        "Fir",
        "Elm",
        "Willow",
        "Magnolia",
        "Birch",
        "Tulip",
        "Cedar"
        ]
                    )

# Tree icons and weigth icons 
def tree_icons(number):
  icons = '<i class="fa fa-tree" style="font-size:48px;"></i>' * number
  return icons

# If user input do graphs
if age != 0:

  # Sample data
  x = np.arange(60)
  y = carbon_sequestered_df[tree].values * 0.00045359237 # all values are being converted to tons

  # Fit with polyfit
  b, m= polyfit(x, y, 1)
  p = np.poly1d(np.polyfit(x, y, 2))
  
  # Get the total carbon sequestered based on the polynomial generated from the known data
  total_carbon_locked = []
  for i in range(0,age):
    total_carbon_locked.append(p(i))
  trees_needed = round(sum(total_carbon_locked)/y[0])

  # Total Cost of Sequestering Carbon
  tons_sequestered = sum(total_carbon_locked)
  cost_of_trees = trees_needed * 0.5
  cost_of_fill = tons_sequestered * 60

  # Carbon written stats displays
  execute_markdown("<p> Intertesing Facts with your data:</p>")
  co2_total = tons_sequestered * 3.6 # relative amount of co2
  if round(co2_total,3) < 0.001:
    execute_markdown(f"<li>Cutting down this tree would lead to < 0.001 tons of CO2 being released </li>")
  else: 
    execute_markdown(f"<li>Cutting down this tree would lead to {round(co2_total,3)} tons of CO2 being released </li>")
  execute_markdown(f"<li>To off-set this you would need to plant {trees_needed} tree, costing £{round(cost_of_trees,2)}</li>")
  execute_markdown(f"<li>Or to capture the carbon manually would cost approx £{round(cost_of_fill,2)}</li>")

  # Expander for the tree area
  tree_expander = st.beta_expander("Visualise the saplings")
  with tree_expander:
    st.markdown(tree_icons(trees_needed), unsafe_allow_html=True)

# Carbon Sequestered by all tree types
fig = go.Figure()

for tree in carbon_sequestered_df.columns[1:]:
    x = np.arange(60)
    y = carbon_sequestered_df[tree].values * 0.00045359237

    # Fit with polyfit
    p = np.poly1d(np.polyfit(x, y, 2))
    fig.add_trace(go.Scatter(
        x=x,
        y=y,
        name=tree
    ))

fig.update_layout(
  title=f"Average Carbon Sequestered Annually",
  xaxis_title="Tree Age (years)",
  yaxis_title="Carbon Sequestered (tonne)"
)

st.plotly_chart(fig, use_column_width=True)

# Total carbon sequestered over life time
total_sequestered_values = np.array(list(total_sequestered.values()))* 0.00045359237
sequestered_data = pd.DataFrame({"Tree" : total_sequestered.keys() , "Total Sequestered" : total_sequestered_values})

fig = px.bar(sequestered_data, x='Tree', y='Total Sequestered', log_y=True)
fig.update_layout(
  title="Maximal Carbon Sequestered Over Lifespan",
  xaxis_title="Tree Type",
  yaxis_title="Carbon Sequestered log(tonne)",
  plot_bgcolor='rgba(0,0,0,0)',
  )
fig.update_xaxes(showline=True, linewidth=2, linecolor='black', gridcolor='black')
fig.update_yaxes(showline=True, linewidth=2, linecolor='black', gridcolor='black')
st.plotly_chart(fig, use_column_width=True)

# Impact Paragraph
st.header("Our Impact Can Be Felt")
execute_markdown(open("static/html/impact.html","r").read())

# Oxford Graphics - Global CO2 emissions
execute_markdown('<iframe src="https://ourworldindata.org/grapher/co-emissions-per-capita?tab=chart&stackMode=absolute&region=World" loading="lazy" style="width: 100%; height: 600px; border: 0px none;"></iframe>')

# Oxford Graphic - Global 
execute_markdown('<iframe src="https://ourworldindata.org/grapher/annual-deforestation?stackMode=absolute&region=World" loading="lazy" style="width: 100%; height: 600px; border: 0px none;"></iframe>')

# Sponsor
execute_markdown(open("static/html/sponsorship.html","r").read())
st.image("https://thelandtrust.org.uk/wp-content/uploads/2015/09/Woodland-Trust.png", use_column_width=True)