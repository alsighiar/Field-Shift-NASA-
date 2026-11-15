import streamlit as st
import pandas as pd
import requests
import folium
from folium.plugins import LocateControl
from datetime import datetime, timedelta
from streamlit_folium import st_folium

from core.controller import FieldShiftController
import ui_theme as theme

# --- 1. Page Configuration & High-Contrast Theme ---
st.set_page_config(
    page_title="Field Shift | Smart Agriculture",
    page_icon=str(theme.BRAND_ICON_PATH),
    layout="wide",
    initial_sidebar_state="expanded",
)
theme.apply_theme()

# --- 2. Bilingual Interface Labels ---
ui = {
    "title": {"en": "Field Shift: Agricultural Decision Support", "ar": "فيلد شيفت: نظام دعم القرار الزراعي"},
    "subtitle": {"en": "Assess field moisture and review crop recommendations informed by Earth observation data.", "ar": "قيّم رطوبة الحقل وراجع توصيات المحاصيل المستندة إلى بيانات رصد الأرض."},
    "sidebar": {"en": "Field Configuration", "ar": "إعدادات الحقل"},
    "sensor_p": {"en": "Set the current ground-sensor moisture reading:", "ar": "حدد قراءة رطوبة التربة الحالية من المستشعر الأرضي:"},
    "slider": {"en": "Ground Moisture", "ar": "رطوبة التربة"},
    "sys_ok": {"en": "SYSTEM READY", "ar": "النظام جاهز"},
    "step1": {"en": "1. Select Field Location", "ar": "1. تحديد موقع الحقل"},
    "step1_cap": {"en": "Use the location control or select a point on the map.", "ar": "استخدم أداة تحديد الموقع أو اختر نقطة على الخريطة."},
    "step2": {"en": "2. Analyze Field Conditions", "ar": "2. تحليل ظروف الحقل"},
    "btn": {"en": "Run Field Assessment", "ar": "بدء تقييم الحقل"},
    "loading1": {"en": "Retrieving weather and soil data...", "ar": "جارٍ استرجاع بيانات الطقس والتربة..."},
    "loading2": {"en": "Running the prediction and recommendation pipeline...", "ar": "جارٍ تشغيل مسار التنبؤ والتوصية..."},
    "diag": {"en": "Field Assessment", "ar": "تقييم الحقل"},
    "ai_base": {"en": "AI Target Moisture", "ar": "الرطوبة المستهدفة بالذكاء الاصطناعي"},
    "iot": {"en": "Ground Sensor Moisture", "ar": "رطوبة مستشعر التربة"},
    "def": {"en": "Moisture Gap", "ar": "فجوة الرطوبة"},
    "stress": {"en": "SEVERE WATER STRESS: Irrigation is recommended.", "ar": "إجهاد مائي شديد: يُوصى بالري."},
    "over": {"en": "OVER-IRRIGATION: Reduce or pause irrigation.", "ar": "ري مفرط: قلل الري أو أوقفه مؤقتًا."},
    "opt": {"en": "OPTIMAL: Moisture is within the target range.", "ar": "الحالة مثالية: الرطوبة ضمن النطاق المستهدف."},
    "rep_t": {"en": "Recommendation", "ar": "التوصية"},
    "act": {"en": "**Recommended crop:**", "ar": "**المحصول الموصى به:**"},
    "fao": {"en": "**Scientific context (FAO-56):**", "ar": "**السياق العلمي (FAO-56):**"},
    "wait": {"en": "Select a field location, then run an assessment.", "ar": "حدد موقع الحقل، ثم ابدأ التقييم."}
}

# --- 3. Sidebar & Language Selection ---
with st.sidebar:
    st.markdown(theme.render_brand_bar(), unsafe_allow_html=True)
    lang_choice = st.radio("Language / اللغة", ["العربية", "English"], horizontal=True)
    lang = "ar" if lang_choice == "العربية" else "en"
    
    # RTL Styling for Arabic
    if lang == "ar":
        st.markdown("<style>p, h1, h2, h3, h4, h5, h6, span, label, .stAlert, .stMarkdown { direction: rtl; text-align: right; } div[data-testid='stMetricValue'], div[data-testid='stMetricDelta'] { text-align: right; }</style>", unsafe_allow_html=True)

    st.markdown("---")
    st.subheader(ui["sidebar"][lang])
    st.write(ui["sensor_p"][lang])
    live_sensor_reading = st.slider(ui["slider"][lang], 0.0, 0.8, 0.20, 0.01)
    st.divider()
    st.success(ui["sys_ok"][lang])

# --- 4. System Initialization ---
if "controller" not in st.session_state:
    with st.spinner("Starting AI Engines..." if lang == "en" else "جاري تجهيز النظام..."):
        API_KEY = "AQ.Ab8RN6J6_X0_CimVL9O3xRCD06PhMjGtJhY0kCa0PffO5uCqig"
        st.session_state.controller = FieldShiftController(api_key=API_KEY)

if "lat" not in st.session_state:
    st.session_state.lat = 30.0444
if "lon" not in st.session_state:
    st.session_state.lon = 31.2357

# --- 5. Live Data Fetcher ---
def fetch_live_satellite_data(lat, lon):
    target_date = (datetime.now() - timedelta(days=5)).strftime('%Y%m%d')
    try:
        res = requests.get("https://power.larc.nasa.gov/api/temporal/daily/point", params={"parameters": "T2M,RH2M,PRECTOTCORR", "community": "AG", "longitude": lon, "latitude": lat, "start": target_date, "end": target_date, "format": "JSON"}, timeout=10).json()
        temp = list(res['properties']['parameter']['T2M'].values())[0]
        rh = list(res['properties']['parameter']['RH2M'].values())[0]
        precip = list(res['properties']['parameter']['PRECTOTCORR'].values())[0]
    except: temp, rh, precip = 32.0, 45.0, 0.0

    try:
        soil_res = requests.get(f"https://rest.isric.org/soilgrids/v2.0/properties/query?lon={lon}&lat={lat}&property=sand&property=clay&depth=0-5cm", timeout=10).json()
        sand_pct, clay_pct = 50.0, 20.0 
        for layer in soil_res.get('properties', {}).get('layers', []):
            val = layer['depths'][0]['values']['mean']
            if val:
                if layer['name'] == 'sand': sand_pct = val / 10
                elif layer['name'] == 'clay': clay_pct = val / 10
    except: sand_pct, clay_pct = 50.0, 20.0

    ndvi = 0.55 if clay_pct > 25 else 0.15 
    lst = temp + 3.5 
    now = datetime.now()
    return {
        'Temperature_Avg': temp, 'Relative_Humidity': rh, 'Precipitation': precip,
        'NDVI': ndvi, 'LST_Celsius': lst, 'Soil_Sand_pct': sand_pct, 'Soil_Clay_pct': clay_pct,
        'Crop_Kc': 1.15, 'Month': now.month, 'DayOfYear': now.timetuple().tm_yday, 
        'Rain_3d_sum': precip * 1.5, 'LST_5d_avg': lst - 1.0
    }

# --- 6. Main Dashboard ---
st.markdown(theme.render_brand_bar(), unsafe_allow_html=True)
st.markdown(theme.render_hero(ui["subtitle"][lang]), unsafe_allow_html=True)
st.markdown(theme.render_ticker(), unsafe_allow_html=True)
st.markdown(theme.render_data_pillars(), unsafe_allow_html=True)
st.markdown(theme.render_pipeline(), unsafe_allow_html=True)
st.markdown(theme.render_bridge(), unsafe_allow_html=True)
st.markdown(
    f'<div class="mission-tag telemetry-mono">FIELD FIX / LAT {st.session_state.lat:.4f}° / LON {st.session_state.lon:.4f}° / SENSOR {live_sensor_reading:.0%}</div>',
    unsafe_allow_html=True,
)

col1, col2 = st.columns([1, 1.2], gap="large")

with col1:
    st.subheader(ui["step1"][lang])
    st.caption(ui["step1_cap"][lang])
    
    m = folium.Map(location=[st.session_state.lat, st.session_state.lon], zoom_start=7, tiles=None)
    folium.TileLayer(tiles="CartoDB dark_matter", name="Tactical Night", overlay=False, control=True).add_to(m)
    LocateControl(auto_start=False, position='topleft').add_to(m)
    folium.CircleMarker(
        [st.session_state.lat, st.session_state.lon],
        radius=7,
        popup="Selected field",
        color="#00F0FF",
        weight=2,
        fill=True,
        fill_color="#10B981",
        fill_opacity=0.9,
    ).add_to(m)
    
    map_data = st_folium(m, height=400, width=700, returned_objects=["last_clicked"])
    
    if map_data and map_data.get("last_clicked"):
        c_lat, c_lon = map_data["last_clicked"]["lat"], map_data["last_clicked"]["lng"]
        if c_lat != st.session_state.lat or c_lon != st.session_state.lon:
            st.session_state.lat, st.session_state.lon = c_lat, c_lon
            st.rerun()

with col2:
    st.subheader(ui["step2"][lang])
    
    if st.button(ui["btn"][lang], type="primary", use_container_width=True):
        with st.spinner(ui["loading1"][lang]):
            real_live_data = fetch_live_satellite_data(st.session_state.lat, st.session_state.lon)
            
        with st.spinner(ui["loading2"][lang]):
            try:
                result = st.session_state.controller.run_pipeline(
                    raw_input_data=real_live_data, 
                    live_sensor_reading=live_sensor_reading,
                    lang=lang 
                )
                
                st.subheader(ui["diag"][lang])
                st.markdown(
                    theme.render_moisture_comparison(
                        result["ai_baseline"], result["sensor_reading"], result["deficit"]
                    ),
                    unsafe_allow_html=True,
                )
                
                st.markdown(
                    theme.render_status_alert(
                        result["status"], result["deficit"], ui[
                            "stress" if result["status"] == "SEVERE WATER STRESS"
                            else "over" if result["status"] == "OVER-IRRIGATION"
                            else "opt"
                        ][lang]
                    ),
                    unsafe_allow_html=True,
                )
                    
                st.subheader(ui["rep_t"][lang])
                st.info(f"{ui['act'][lang]} {result['recommended_crop']}")
                st.write(f"{ui['fao'][lang]}\n\n{result['fao_report']}")
                
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.write(ui["wait"][lang])