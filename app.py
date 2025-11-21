import pandas as pd  
import numpy as np
from shiny import App, ui, render, reactive
import matplotlib.pyplot as plt
import seaborn as sns 

df = pd.read_csv('../attendance_anonymised-1.csv')

df.rename(columns= {
    'Unit Instance Code':'Module Code',
    'Calocc Code':'Year',
    'Long Description':'Module Name',
    'Register Event ID':'Event ID',
    'Register Event Slot ID':'Event Slot ID',
    'Planned Start Date':'Date',
    'is Positive': 'Has Attended',
    'Negative Marks': 'NotAttended',
    'Usage Code': 'Attendance Code',
    'Postive Marks': 'Attended'
}, inplace=True)

# UI

app_ui = ui.page_fluid(
    ui.input_select(
        'select',
        'Select a Module:',
        choices= sorted(df['Module Name'].unique().tolist())
    ),
    ui.output_plot("attendance_plot"),
)

# SERVER 

def server(input, output, session):

    # reactive dataset based on dropdown selection
    @reactive.Calc
    def filtered_df():
        module = input.select()
        temp = df[df["Module Name"] == module].copy()
        temp = temp.set_index("Date")

        #grouping attendance over time
        att = (
            temp.groupby("Date")["Attended"]
            .sum()
            .reset_index()
        )
        return att

    @output
    @render.plot(alt="Average Attendance Over Time")
    def attendance_plot():

        data_to_plot = filtered_df()

        fig, ax = plt.subplots()
        ax.set_title(f"Attendance Over Time: {input.select()}")
        sns.lineplot(data=data_to_plot, x='Date', y='Attended', ax=ax)
        plt.xticks(rotation=45)

        return fig

app = App(app_ui, server, debug=True)

