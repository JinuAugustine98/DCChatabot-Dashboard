import random
import pandas as pd
from flask import Flask, render_template
import plotly
import plotly.graph_objs as go
import json

app = Flask(__name__, template_folder='template')

# Read the provided dataset and extract the relevant information
def read_dataset():
    data = pd.read_csv('data.csv', nrows=100)  # Read only the first 1000 rows
    data['timestamp'] = pd.to_datetime(data['timestamp'])  # Convert 'timestamp' to datetime
    data.sort_values(by='timestamp', inplace=True)  # Sort by 'timestamp'
    
    timestamps = data['timestamp']
    user_activity = [random.randint(50, 100) for _ in range(len(data))]
    top_user_messages = data['user_msg'].value_counts().index.tolist()[:5]
    user_locations = data['user_ip'].value_counts().index.tolist()[:3]
    user_engagement = [random.randint(10, 100) for _ in range(24)]
    return timestamps, user_activity, top_user_messages, user_locations, user_engagement

@app.route('/')
def index():
    timestamps, user_activity, top_user_messages, user_locations, user_engagement = read_dataset()

    # Visualization 1: User Activity Timeline (Line Chart)
    activity_chart = go.Scatter(x=timestamps, y=user_activity, mode='lines+markers', name='User Activity', line=dict(color='#ff0000'))

    # Visualization 2: Top User Messages (Bar Chart)
    top_messages_chart = go.Bar(x=top_user_messages, y=[random.randint(5, 20) for _ in range(5)], name='Top Messages', marker=dict(color='#097969'))

    # Visualization 3: User Locations Bar Chart (Bar Chart)
    location_chart = go.Bar(x=user_locations, y=[random.randint(10, 50) for _ in range(len(user_locations))], name='User Locations', marker=dict(color='#17229E'))

    # Visualization 4: User Engagement by Time of Day (Heatmap)
    engagement_chart = go.Heatmap(
        z=[user_engagement],
        x=[f"{i:02}:00" for i in range(24)],
        y=['User Engagement'],
        colorscale='Viridis',
    )

    # Serialize the data to JSON to pass to the template
    activity_chart_json = json.dumps(activity_chart, cls=plotly.utils.PlotlyJSONEncoder)
    top_messages_chart_json = json.dumps(top_messages_chart, cls=plotly.utils.PlotlyJSONEncoder)
    location_chart_json = json.dumps(location_chart, cls=plotly.utils.PlotlyJSONEncoder)
    engagement_chart_json = json.dumps(engagement_chart, cls=plotly.utils.PlotlyJSONEncoder)

    # Render the dashboard template and pass the visualizations to it
    return render_template(
        'dashboard.html',
        activity_chart=activity_chart_json,
        top_messages_chart=top_messages_chart_json,
        location_chart=location_chart_json,
        engagement_chart=engagement_chart_json,
    )

if __name__ == '__main__':
    app.run(debug=True)
