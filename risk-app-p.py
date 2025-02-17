import sys
import numpy as np
import pandas as pd
import streamlit as st
import pydeck as pdk
from datetime import datetime, timezone
from utils import parse_dt,logger
from typing import List, Dict
from dotenv import load_dotenv
import logging

from maersk_backend import MaerskClient, NewsDB, process_schedule, Config, EnhancedNewsClient, OpenMeteoMarineClient
# from news_processor import EnhancedNewsClient

icon_data = {
    "x": 0,
    "y": 0,
    "width": 512,
    "height": 512,
    "anchorY": 256,  # Center the anchor point vertically
    "anchorX": 256,  # Center the anchor point horizontally
    "mask": False,    # Don't mask the image since it's a full icon
    "url": "https://fonts.gstatic.com/s/e/notoemoji/latest/1f6a2/512.png"
}


# Visualization
def create_vessel_map(positions: List[Dict], routes: List[Dict]) -> pdk.Deck:

    layers = [
        # pdk.Layer(
        #     "ScatterplotLayer",
        #     data=positions,
        #     get_position=['lon', 'lat'],
        #     get_color="color",
        #     get_radius=150000,
        #     pickable=True
        # ),
        # pdk.Layer(
        #     "TextLayer",
        #     data=positions,
        #     get_position=['lon', 'lat'],
        #     get_text="name",
        #     get_size=14,
        #     get_color=[0, 0, 0],
        #     get_angle=0,
        # ),
        pdk.Layer(
            "LineLayer",
            data=routes,
            get_source_position='start',
            get_target_position='end',
            get_color=[0, 255, 0, 160],
            get_width=10,
            pickable=True
        ),
        pdk.Layer(
            "IconLayer",
            data=positions,
            pickable=True,
            get_icon="icon_data", 
            get_size=5,  # Increased base size
            size_scale=10,  # Adjusted scale
            size_min_pixels=20,  # Ensure minimum visibility
            size_max_pixels=300,  # Maximum size
            get_position=['lon', 'lat']
        )
    ]
    return pdk.Deck(
        map_style='mapbox://styles/mapbox/light-v9',
        initial_view_state=pdk.ViewState(
            latitude=0,
            longitude=0,
            zoom=1
        ),
        layers=layers,
        tooltip={"text": "{name}\nLast update: {last_update}"}       
    )

def show_news_analysis(news_client: EnhancedNewsClient, max_articles: int):
    st.subheader("⚠️ Risk Accessment and Forecast")
    
    # Real-time processing
    with st.expander("Latest News Alerts", expanded=True):
        news_client = EnhancedNewsClient()
        new_count = news_client.get_and_save_news(max_articles)
        st.success(f"Processed {new_count} new articles")

    # Historical analysis
    with st.expander("Port Risk Trends", expanded=True):
        df = news_client.get_risk_history_df()
        
        if not df.empty:
            st.line_chart(df.set_index('date')['decayed_risk'])
            
            # Show map only if coordinates exist
            if df['lat'].any() and df['lon'].any():
                st.pydeck_chart(pdk.Deck(
                    map_style='mapbox://styles/mapbox/light-v9',
                    initial_view_state=pdk.ViewState(
                        latitude=df['lat'].mean(),
                        longitude=df['lon'].mean(),
                        zoom=1.3
                    ),
                    layers=[
                        pdk.Layer(
                            'ScatterplotLayer',
                            data=df,
                            get_position=['lon', 'lat'],
                            get_radius=100000,
                            get_fill_color=[255, 0, 0, 140],
                            pickable=True
                        )
                    ]
                ))
            
            st.dataframe(df.style.background_gradient(cmap='Reds'))
        else:
            st.warning("No recent risk data available")


def create_weather_layer(weather_data: List[Dict]) -> pdk.Layer:
    return pdk.Layer(
        "ScatterplotLayer",
        data=weather_data,
        get_position=['lon', 'lat'],
        get_radius='wave_height_max * 200000',  # Scale radius by wave height
        get_fill_color=[238, 77, 67, 200],  # Red color with alpha
        pickable=True,
        extruded=True
    )

# def show_predictive_analytics(news_client: EnhancedNewsClient):
#     st.subheader("🌊 Predictive Risk Analytics")
    
#     # Get historical data
#     df = news_client.get_risk_history_df(Config.RISK_HISTORY_DAYS)

#     if not df.empty:
#         # Add missing feature check
#         if not news_client.predictor.validate_features(df):
#             st.error("Missing required features for prediction")
#             return
#         # Train model
#         news_client.predictor.train(df)
        
#         df['predicted_risk'] = news_client.predictor.predict(df)        
#         # Display
#         st.line_chart(df.set_index('date')[['decayed_risk', 'predicted_risk']])
        
#         cols = st.columns(3)
#         cols[0].metric("Current Risk", f"{df['decayed_risk'].iloc[-1]:.0%}")
#         cols[1].metric("Predicted Risk", f"{df['predicted_risk'].iloc[-1]:.0%}")
#         # cols[1].metric("Key Drivers", f"{df[''].iloc[-1]:.0%}")
#         cols[2].metric("Model Confidence", "92%")  # From validation metrics
#     else:
#         st.warning("Insufficient data for predictions")


def main():

    # Simple debug level control
    if '--debug' in sys.argv:
        logger.setLevel(logging.DEBUG)

    st.set_page_config(page_title="Maersk Risk Monitor", layout="wide")
    st.title("🚢 Maersk Vessel Tracking - Port Schedule Analysis")
    
    try:
        client = MaerskClient()
        news_client = EnhancedNewsClient()
        weather_client = OpenMeteoMarineClient()
        
        with st.spinner("Fetching vessel data..."):
            vessels = client.get_vessels()
            if not vessels:
                st.warning("No active vessels found")
                return

        ships_data = []
        with st.spinner("Processing vessel schedules..."):
            for vessel in vessels[:Config.MAX_VESSELS]:
                try:
                    schedule = client.get_schedule(vessel['vesselIMONumber'])
                    last_port, next_ports = process_schedule(schedule)
                    
                    ships_data.append({
                        "vesselName": vessel['vesselName'],
                        "vesselIMO": vessel['vesselIMONumber'],
                        "last_port": last_port,
                        "next_ports": next_ports
                    })
                except Exception as e:
                    logger.error(f"Error processing vessel {vessel['vesselIMONumber']}: {str(e)}")

        if ships_data:
            # VESSEL TRACKING CALCULATIONS
            positions = []
            routes = []

            for ship in ships_data:
                # if not ship['last_port']:
                if not ship['last_port'] or not ship['last_port']['lat'] or not ship['last_port']['lon']:
                    logger.warning(f"Skipping vessel {ship['vesselName']} with no valid port data")
                    continue
                
                dep_dt = parse_dt(ship['last_port']['departure'])
                if not dep_dt.tzinfo:  # Handle naive datetime
                    dep_dt = dep_dt.replace(tzinfo=timezone.utc)

                status = "at_port" if datetime.now(timezone.utc) < dep_dt else "en_route"
                
                positions.append({
                    "name": ship["vesselName"],
                    "lat": ship['last_port']['lat'],
                    "lon": ship['last_port']['lon'],
                    "status": status,
                    "color": Config.STATUS_COLORS.get(status),
                    "last_update": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M"),
                    "icon_data": icon_data
                })
                
                for next_port in ship['next_ports']:
                    if next_port:
                        routes.append({
                            "start": [ship['last_port']['lon'], ship['last_port']['lat']],
                            "end": [next_port['lon'], next_port['lat']],
                            "vessel": ship["vesselName"]
                        })
            logger.debug(f"Tracking {len(positions)} vessels with {len(routes)} routes")
            # logger.debug(f"Vessel data: {ships_data}")

            # VESSEL TRACKING MAP
            st.subheader("Vessel Tracking Map") 
            st.success(f"Tracking {len(positions)} vessels with {len(routes)} routes")
            st.pydeck_chart(create_vessel_map(positions, routes))

            # WEATHER MAP
            weather_data = []
            for ship in ships_data:
                logger.debug(f"Processing ship: {ship['vesselName']} -- Port: {ship['last_port']}")  

                if ship['last_port']:
                    port_coords = (ship['last_port']['lat'], ship['last_port']['lon'])
                    forecast = weather_client.get_wave_forecast(*port_coords)
                    
                    # Add ship name to each forecast entry
                    for day, height in forecast.get('forecast', []):
                        weather_data.append({
                            'lat': port_coords[0],
                            'lon': port_coords[1],
                            'name': ship['vesselName'],
                            'wave_height_max': height,
                            'date': day
                        })
            logger.debug(f"weather_data: {weather_data}")

            # Update the pydeck chart configuration
            st.pydeck_chart(pdk.Deck(
                map_style='mapbox://styles/mapbox/light-v9',
                initial_view_state=pdk.ViewState(
                    latitude=0,
                    longitude=0,
                    zoom=1
                ),
                layers=[
                    # create_vessel_map(positions, routes).layers[1],  # Keep vessel tracks
                    create_weather_layer(weather_data),
                    pdk.Layer(
                        "TextLayer",
                        data=weather_data,
                        get_position=['lon', 'lat'],
                        # get_text="name",
                        get_size=14,
                        get_color=[0, 0, 0, 255],
                        get_angle=0
                    )
                ],
                tooltip={
                    "html": """
                    <b>Ship:</b> {name}<br/>
                    <b>Max Wave:</b> {wave_height_max}<br/>
                    <b>Date:</b> {date}
                    """,
                    "style": {
                        "backgroundColor": "steelblue",
                        "color": "white"
                    }
                }
            ))

            # VESSEL SCHEDULE
            st.subheader("Vessel Port Schedule Details")
            for ship in ships_data:
                if not ship.get('last_port'):
                    continue
                    
                with st.expander(f"{ship['vesselName']} (IMO: {ship['vesselIMO']})"):
                    cols = st.columns([1, 2])
                    
                    cols[0].subheader("Last Known Port")
                    cols[0].markdown(f"""
                    **{ship['last_port']['port_name']}**  
                    *{ship['last_port']['city']}, {ship['last_port']['country']}*  
                    Arrived: {parse_dt(ship['last_port']['arrival']).strftime("%Y-%m-%d %H:%M")}  
                    Departed: {parse_dt(ship['last_port']['departure']).strftime("%Y-%m-%d %H:%M")}  
                    Coordinates: {ship['last_port']['lat']:.4f}, {ship['last_port']['lon']:.4f}
                    """)
                    
                    cols[1].subheader("Next Expected Ports")
                    for i, port in enumerate(ship['next_ports'][:2], 1):
                        if port:
                            cols[1].markdown(f"""
                            **Port {i}**: {port['port_name']}  
                            *{port['city']}, {port['country']}*  
                            Expected Arrival: {parse_dt(port['arrival']).strftime("%Y-%m-%d %H:%M")}  
                            Expected Departure: {parse_dt(port['departure']).strftime("%Y-%m-%d %H:%M")}
                            """)
        else:
            st.warning("No valid vessel data available")      
        
        # NEWS ANALYSIS
        show_news_analysis(news_client, Config.NUMBER_ARTICLES_FETCH)

    except Exception as e:
        logger.exception("Application error")
        st.error(f"Critical application error: {str(e)}")

if __name__ == "__main__":
    load_dotenv()
    main()