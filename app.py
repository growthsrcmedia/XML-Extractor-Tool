"""
Streamlit Web UI for XML Sitemap -> HTML URL Extractor

A user-friendly web interface for extracting HTML URLs from XML sitemaps.
Powered by Botpresso
"""

import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urlparse
import time
from typing import Set, List
import io


# Page configuration
st.set_page_config(
    page_title="Sitemap URL Extractor | Botpresso",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded"
)

# Botpresso Design System Colors
PRIMARY_BLUE = "#5046E5"
PRIMARY_GREEN = "#71D997"
PRIMARY_RED = "#EF1E3B"
LIGHT_BLUE = "#EFF3FF"
LIGHT_GREEN = "#EEFCF3"
LIGHT_RED = "#FFEFEF"

# Inject custom CSS for Botpresso design
def inject_botpresso_css():
    """Inject custom CSS to match Botpresso design system."""
    st.markdown(f"""
    <style>
        /* Botpresso Color Variables */
        :root {{
            --primary-blue: {PRIMARY_BLUE};
            --primary-green: {PRIMARY_GREEN};
            --primary-red: {PRIMARY_RED};
            --light-blue: {LIGHT_BLUE};
            --light-green: {LIGHT_GREEN};
            --light-red: {LIGHT_RED};
        }}
        
        /* Botpresso Theme - Root Level */
        html, body {{
            background-color: #F7F8FC !important;
            color: #1F2937 !important;
            margin: 0 !important;
            padding: 0 !important;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Inter', 'Helvetica Neue', Arial, sans-serif !important;
        }}
        
        /* Streamlit App Containers - Light Blue-Grey Background */
        .appview-container,
        [data-testid="stAppViewContainer"],
        [data-testid="stApp"] {{
            background-color: #F7F8FC !important;
            color: #1F2937 !important;
            padding-top: 0 !important;
            margin-top: 0 !important;
        }}
        
        /* Main Content Area - Light Blue-Grey Background */
        .main {{
            background-color: #F7F8FC !important;
            color: #1F2937 !important;
        }}
        
        /* Main Block Container - White Cards with Rounded Corners and Shadows */
        .main .block-container {{
            background-color: #FFFFFF !important;
            color: #1F2937 !important;
            padding: 1.5rem !important;
            margin-top: 1rem !important;
            border-radius: 12px !important;
            box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06) !important;
        }}
        
        /* Sidebar Styling - Pure White with Sharp Corners and Blue Left Border */
        [data-testid="stSidebar"] {{
            background-color: #FFFFFF !important;
            color: #1F2937 !important;
            padding-top: 0 !important;
            margin-top: 0 !important;
            box-shadow: 2px 0 4px 0 rgba(0, 0, 0, 0.05) !important;
            border-radius: 0 !important;
            border-left: 4px solid #5046E5 !important;
        }}
        
        /* Hide black box or unwanted elements at top of sidebar */
        [data-testid="stSidebar"] > div:first-child > div:first-child,
        [data-testid="stSidebar"] > div:first-child > div:first-child > div,
        [data-testid="stSidebar"] > div:first-child > div:first-child > button,
        [data-testid="stSidebar"] > div:first-child > div:first-child > span,
        [data-testid="stSidebar"] > div:first-child > div:first-child > * {{
            background-color: transparent !important;
        }}
        
        /* Hide any black squares or boxes in sidebar */
        [data-testid="stSidebar"] div[style*="background-color: black"],
        [data-testid="stSidebar"] div[style*="background-color:#000000"],
        [data-testid="stSidebar"] div[style*="background-color: #000000"],
        [data-testid="stSidebar"] button[style*="background-color: black"],
        [data-testid="stSidebar"] button[style*="background-color:#000000"],
        [data-testid="stSidebar"] button[style*="background-color: #000000"],
        [data-testid="stSidebar"] span[style*="background-color: black"],
        [data-testid="stSidebar"] span[style*="background-color:#000000"],
        [data-testid="stSidebar"] span[style*="background-color: #000000"] {{
            display: none !important;
            visibility: hidden !important;
            width: 0 !important;
            height: 0 !important;
            opacity: 0 !important;
        }}
        
        /* Hide empty containers or placeholders at top of sidebar */
        [data-testid="stSidebar"] > div:first-child > div:first-child:empty,
        [data-testid="stSidebar"] > div:first-child > div:first-child:has(> div:empty) {{
            display: none !important;
            visibility: hidden !important;
            height: 0 !important;
            min-height: 0 !important;
            padding: 0 !important;
            margin: 0 !important;
        }}
        
        /* Remove rounded corners from sidebar elements */
        [data-testid="stSidebar"] * {{
            border-radius: 0 !important;
        }}
        
        /* Sidebar content container */
        [data-testid="stSidebar"] > div {{
            border-radius: 0 !important;
        }}
        
        /* Sidebar headers - hide default styling */
        [data-testid="stSidebar"] h1,
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3 {{
            color: #1F2937 !important;
            font-weight: 600 !important;
            margin-top: 1.5rem !important;
            margin-bottom: 0.75rem !important;
            font-size: 0.875rem !important;
            text-transform: uppercase !important;
            letter-spacing: 0.05em !important;
        }}
        
        /* Sidebar markdown content */
        [data-testid="stSidebar"] .stMarkdown {{
            color: #1F2937 !important;
        }}
        
        /* Sidebar divider */
        [data-testid="stSidebar"] hr {{
            border-color: #E5E7EB !important;
            margin: 1.5rem 0 !important;
        }}
        
        /* Sidebar checkbox */
        [data-testid="stSidebar"] .stCheckbox {{
            margin-top: 0.5rem !important;
        }}
        
        /* Sidebar Content */
        [data-testid="stSidebar"] > div {{
            background-color: #ffffff !important;
            padding-top: 0 !important;
            margin-top: 0 !important;
        }}
        
        /* Sidebar first element */
        [data-testid="stSidebar"] > div > div:first-child {{
            margin-top: 0 !important;
            padding-top: 0 !important;
        }}
        
        /* All divs and containers - Botpresso Theme */
        div {{
            color: #1F2937 !important;
        }}
        
        /* Override any dark theme */
        [data-theme="dark"],
        .dark {{
            background-color: #F7F8FC !important;
            color: #1F2937 !important;
        }}
        
        /* General Text Color on White Backgrounds - Botpresso Theme */
        .main p, .main div, .main span, .main label {{
            color: #1F2937 !important;
        }}
        
        [data-testid="stSidebar"] p, 
        [data-testid="stSidebar"] div, 
        [data-testid="stSidebar"] span, 
        [data-testid="stSidebar"] label {{
            color: #1F2937 !important;
        }}
        
        /* Markdown Text - Botpresso Theme */
        .main .stMarkdown, 
        .main .stMarkdown p,
        .main .stMarkdown li {{
            color: #1F2937 !important;
        }}
        
        [data-testid="stSidebar"] .stMarkdown,
        [data-testid="stSidebar"] .stMarkdown p,
        [data-testid="stSidebar"] .stMarkdown li {{
            color: #1F2937 !important;
        }}
        
        /* Text Input Labels - Botpresso Design Guide */
        .stTextInput label {{
            color: #1F2937 !important;
            font-weight: 500 !important;
            font-size: 0.875rem !important;
            margin-bottom: 0.375rem !important;
            display: block !important;
        }}
        
        /* Checkbox Labels - Botpresso Theme */
        .stCheckbox label {{
            color: #1F2937 !important;
            font-weight: 500 !important;
        }}
        
        /* Typography System - Botpresso Design Guide */
        /* 
         * Font Weights Available: Heavy (900), Bold (700), Medium (500), Regular (400), Thin (300)
         * Text Styles: Heading 1-6, Body, Caption, Small, Tiny
         * Usage: Add class like "heavy", "bold", "medium", "regular", or "thin" to any text element
         * Example: <h1 class="heavy">Title</h1> or <p class="medium">Text</p>
         */
        
        /* Base font family */
        * {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Inter', 'Helvetica Neue', Arial, sans-serif !important;
        }}
        
        /* Heading 1 - Multiple weights available */
        h1 {{
            color: {PRIMARY_BLUE} !important;
            margin-top: 0 !important;
            padding-top: 0 !important;
            font-size: 2.5rem !important; /* Largest size */
            line-height: 1.2 !important;
            font-weight: 700 !important; /* Bold by default, can be Heavy (900), Medium (500), Regular (400), Thin (300) */
            letter-spacing: -0.02em !important;
        }}
        
        h1.heavy {{ font-weight: 900 !important; }}
        h1.bold {{ font-weight: 700 !important; }}
        h1.medium {{ font-weight: 500 !important; }}
        h1.regular {{ font-weight: 400 !important; }}
        h1.thin {{ font-weight: 300 !important; }}
        
        /* Heading 2 */
        h2 {{
            color: #1F2937 !important;
            font-size: 2rem !important;
            line-height: 1.3 !important;
            font-weight: 600 !important; /* Bold by default */
            letter-spacing: -0.01em !important;
        }}
        
        h2.heavy {{ font-weight: 900 !important; }}
        h2.bold {{ font-weight: 700 !important; }}
        h2.medium {{ font-weight: 500 !important; }}
        h2.regular {{ font-weight: 400 !important; }}
        h2.thin {{ font-weight: 300 !important; }}
        
        /* Heading 3 */
        h3 {{
            color: #1F2937 !important;
            font-size: 1.75rem !important;
            line-height: 1.3 !important;
            font-weight: 600 !important; /* Bold by default */
        }}
        
        h3.heavy {{ font-weight: 900 !important; }}
        h3.bold {{ font-weight: 700 !important; }}
        h3.medium {{ font-weight: 500 !important; }}
        h3.regular {{ font-weight: 400 !important; }}
        h3.thin {{ font-weight: 300 !important; }}
        
        /* Heading 4 */
        h4 {{
            color: #1F2937 !important;
            font-size: 1.5rem !important;
            line-height: 1.4 !important;
            font-weight: 600 !important; /* Bold by default */
        }}
        
        h4.heavy {{ font-weight: 900 !important; }}
        h4.bold {{ font-weight: 700 !important; }}
        h4.medium {{ font-weight: 500 !important; }}
        h4.regular {{ font-weight: 400 !important; }}
        h4.thin {{ font-weight: 300 !important; }}
        
        /* Heading 5 */
        h5 {{
            color: #1F2937 !important;
            font-size: 1.25rem !important;
            line-height: 1.4 !important;
            font-weight: 600 !important; /* Bold by default */
        }}
        
        h5.heavy {{ font-weight: 900 !important; }}
        h5.bold {{ font-weight: 700 !important; }}
        h5.medium {{ font-weight: 500 !important; }}
        h5.regular {{ font-weight: 400 !important; }}
        h5.thin {{ font-weight: 300 !important; }}
        
        /* Heading 6 */
        h6 {{
            color: #1F2937 !important;
            font-size: 1.125rem !important;
            line-height: 1.4 !important;
            font-weight: 600 !important; /* Bold by default */
        }}
        
        h6.heavy {{ font-weight: 900 !important; }}
        h6.bold {{ font-weight: 700 !important; }}
        h6.medium {{ font-weight: 500 !important; }}
        h6.regular {{ font-weight: 400 !important; }}
        h6.thin {{ font-weight: 300 !important; }}
        
        /* Body Text */
        body, p, .body {{
            color: #1F2937 !important;
            font-size: 1rem !important;
            line-height: 1.5 !important;
            font-weight: 400 !important; /* Regular by default */
        }}
        
        body.heavy, p.heavy, .body.heavy {{ font-weight: 900 !important; }}
        body.bold, p.bold, .body.bold {{ font-weight: 700 !important; }}
        body.medium, p.medium, .body.medium {{ font-weight: 500 !important; }}
        body.regular, p.regular, .body.regular {{ font-weight: 400 !important; }}
        body.thin, p.thin, .body.thin {{ font-weight: 300 !important; }}
        
        /* Caption */
        .caption, .stCaption {{
            color: #6B7280 !important;
            font-size: 0.875rem !important; /* 14px */
            line-height: 1.4 !important;
            font-weight: 400 !important; /* Regular by default */
        }}
        
        .caption.heavy, .stCaption.heavy {{ font-weight: 900 !important; }}
        .caption.bold, .stCaption.bold {{ font-weight: 700 !important; }}
        .caption.medium, .stCaption.medium {{ font-weight: 500 !important; }}
        .caption.regular, .stCaption.regular {{ font-weight: 400 !important; }}
        .caption.thin, .stCaption.thin {{ font-weight: 300 !important; }}
        
        /* Small */
        .small {{
            color: #1F2937 !important;
            font-size: 0.8125rem !important; /* 13px */
            line-height: 1.4 !important;
            font-weight: 400 !important; /* Regular by default */
        }}
        
        .small.heavy {{ font-weight: 900 !important; }}
        .small.bold {{ font-weight: 700 !important; }}
        .small.medium {{ font-weight: 500 !important; }}
        .small.regular {{ font-weight: 400 !important; }}
        .small.thin {{ font-weight: 300 !important; }}
        
        /* Tiny */
        .tiny {{
            color: #6B7280 !important;
            font-size: 0.75rem !important; /* 12px */
            line-height: 1.4 !important;
            font-weight: 400 !important; /* Regular by default */
        }}
        
        .tiny.heavy {{ font-weight: 900 !important; }}
        .tiny.bold {{ font-weight: 700 !important; }}
        .tiny.medium {{ font-weight: 500 !important; }}
        .tiny.regular {{ font-weight: 400 !important; }}
        .tiny.thin {{ font-weight: 300 !important; }}
        
        /* Remove top spacing from first h1 */
        h1:first-child,
        .main h1:first-of-type {{
            margin-top: 0 !important;
            padding-top: 0 !important;
        }}
        
        /* Standardized Button System - Rounded Corners (8-12px) */
        .stButton > button,
        button,
        [role="button"],
        input[type="button"],
        input[type="submit"] {{
            border-radius: 10px !important; /* Moderately rounded corners */
            padding: 0.625rem 1.5rem !important; /* Medium height with comfortable padding */
            font-weight: 500 !important;
            transition: all 0.2s ease !important;
            display: inline-flex !important;
            align-items: center !important;
            justify-content: center !important;
            gap: 0.5rem !important;
            min-height: 40px !important;
            font-family: inherit !important;
        }}
        
        /* Ensure all buttons in modals, forms, and headers use standardized styling */
        .modal button,
        .dialog button,
        form button,
        header button,
        footer button,
        [data-testid*="modal"] button,
        [data-testid*="dialog"] button {{
            border-radius: 9999px !important;
            padding: 0.625rem 1.5rem !important;
            min-height: 40px !important;
        }}
        
        /* Primary Buttons - Solid #5046E5 */
        .stButton > button:not(:disabled),
        button.primary,
        button[type="primary"] {{
            background-color: #5046E5 !important;
            color: #FFFFFF !important;
            border: none !important;
        }}
        
        .stButton > button:not(:disabled):hover,
        button.primary:hover,
        button[type="primary"]:hover {{
            background-color: #4339d4 !important;
            color: #FFFFFF !important;
        }}
        
        .stButton > button:not(:disabled):focus,
        button.primary:focus,
        button[type="primary"]:focus {{
            background-color: #5046E5 !important;
            color: #FFFFFF !important;
            outline: 2px solid #5046E5 !important;
            outline-offset: 2px !important;
        }}
        
        .stButton > button:not(:disabled):active,
        button.primary:active,
        button[type="primary"]:active {{
            background-color: #3d32c2 !important;
            color: #FFFFFF !important;
        }}
        
        /* Primary button text and icons */
        .stButton > button:not(:disabled) *,
        .stButton > button:not(:disabled) span,
        .stButton > button:not(:disabled) p,
        .stButton > button:not(:disabled) div,
        button.primary *,
        button[type="primary"] * {{
            color: #FFFFFF !important;
        }}
        
        .stButton > button:not(:disabled) svg,
        .stButton > button:not(:disabled) svg *,
        .stButton > button:not(:disabled) svg path,
        button.primary svg,
        button.primary svg *,
        button.primary svg path,
        button[type="primary"] svg,
        button[type="primary"] svg *,
        button[type="primary"] svg path {{
            fill: #FFFFFF !important;
            stroke: #FFFFFF !important;
            color: #FFFFFF !important;
        }}
        
        /* Secondary Buttons - Outlined #5046E5 */
        button.secondary,
        button[type="secondary"],
        .secondary-button {{
            background-color: #FFFFFF !important;
            color: #5046E5 !important;
            border: 1.5px solid #5046E5 !important;
        }}
        
        button.secondary:hover,
        button[type="secondary"]:hover,
        .secondary-button:hover {{
            background-color: #EFF3FF !important;
            color: #5046E5 !important;
            border-color: #5046E5 !important;
        }}
        
        button.secondary:focus,
        button[type="secondary"]:focus,
        .secondary-button:focus {{
            background-color: #FFFFFF !important;
            color: #5046E5 !important;
            border-color: #5046E5 !important;
            outline: 2px solid #5046E5 !important;
            outline-offset: 2px !important;
        }}
        
        button.secondary:active,
        button[type="secondary"]:active,
        .secondary-button:active {{
            background-color: #EFF3FF !important;
            color: #5046E5 !important;
        }}
        
        /* Secondary button text and icons */
        button.secondary *,
        button.secondary span,
        button.secondary p,
        button.secondary div,
        button[type="secondary"] *,
        .secondary-button * {{
            color: #5046E5 !important;
        }}
        
        button.secondary svg,
        button.secondary svg *,
        button.secondary svg path,
        button[type="secondary"] svg,
        button[type="secondary"] svg *,
        button[type="secondary"] svg path,
        .secondary-button svg,
        .secondary-button svg *,
        .secondary-button svg path {{
            fill: #5046E5 !important;
            stroke: #5046E5 !important;
            color: #5046E5 !important;
        }}
        
        /* Destructive Buttons - Solid #EF1E3B */
        button.destructive,
        button[type="destructive"],
        button.delete {{
            background-color: #EF1E3B !important;
            color: #FFFFFF !important;
            border: none !important;
        }}
        
        button.destructive:hover,
        button[type="destructive"]:hover,
        button.delete:hover {{
            background-color: #dc1a2e !important;
            color: #FFFFFF !important;
        }}
        
        button.destructive:focus,
        button[type="destructive"]:focus,
        button.delete:focus {{
            background-color: #EF1E3B !important;
            color: #FFFFFF !important;
            outline: 2px solid #EF1E3B !important;
            outline-offset: 2px !important;
        }}
        
        button.destructive:active,
        button[type="destructive"]:active,
        button.delete:active {{
            background-color: #c91628 !important;
            color: #FFFFFF !important;
        }}
        
        /* Destructive button text and icons */
        button.destructive *,
        button.destructive span,
        button.destructive p,
        button.destructive div,
        button[type="destructive"] *,
        button.delete * {{
            color: #FFFFFF !important;
        }}
        
        button.destructive svg,
        button.destructive svg *,
        button.destructive svg path,
        button[type="destructive"] svg,
        button[type="destructive"] svg *,
        button[type="destructive"] svg path,
        button.delete svg,
        button.delete svg *,
        button.delete svg path {{
            fill: #FFFFFF !important;
            stroke: #FFFFFF !important;
            color: #FFFFFF !important;
        }}
        
        /* Outlined Destructive Buttons */
        button.destructive-outlined,
        button[type="destructive-outlined"],
        button.delete-outlined {{
            background-color: #FFFFFF !important;
            color: #EF1E3B !important;
            border: 1.5px solid #EF1E3B !important;
        }}
        
        button.destructive-outlined:hover,
        button[type="destructive-outlined"]:hover,
        button.delete-outlined:hover {{
            background-color: #FFEFEF !important;
            color: #EF1E3B !important;
            border-color: #EF1E3B !important;
        }}
        
        button.destructive-outlined:focus,
        button[type="destructive-outlined"]:focus,
        button.delete-outlined:focus {{
            background-color: #FFFFFF !important;
            color: #EF1E3B !important;
            border-color: #EF1E3B !important;
            outline: 2px solid #EF1E3B !important;
            outline-offset: 2px !important;
        }}
        
        button.destructive-outlined:active,
        button[type="destructive-outlined"]:active,
        button.delete-outlined:active {{
            background-color: #FFEFEF !important;
            color: #EF1E3B !important;
        }}
        
        /* Outlined destructive button text and icons */
        button.destructive-outlined *,
        button.destructive-outlined span,
        button.destructive-outlined p,
        button.destructive-outlined div,
        button[type="destructive-outlined"] *,
        button.delete-outlined * {{
            color: #EF1E3B !important;
        }}
        
        button.destructive-outlined svg,
        button.destructive-outlined svg *,
        button.destructive-outlined svg path,
        button[type="destructive-outlined"] svg,
        button[type="destructive-outlined"] svg *,
        button[type="destructive-outlined"] svg path,
        button.delete-outlined svg,
        button.delete-outlined svg *,
        button.delete-outlined svg path {{
            fill: #EF1E3B !important;
            stroke: #EF1E3B !important;
            color: #EF1E3B !important;
        }}
        
        /* Pagination Container - Flexbox Layout - Single Horizontal Line */
        .pagination-flex-container {{
            display: flex !important;
            align-items: center !important;
            gap: 0.75rem !important;
            flex-wrap: nowrap !important;
            white-space: nowrap !important;
            width: 100% !important;
            overflow-x: auto !important;
            overflow-y: hidden !important;
        }}
        
        /* Make the element container that follows pagination-flex-container use flexbox */
        .pagination-flex-container ~ div,
        .element-container:has(.pagination-flex-container),
        .element-container .pagination-flex-container,
        /* Target the element-container that wraps the pagination */
        .element-container:has(> .pagination-flex-container),
        div:has(> .pagination-flex-container) {{
            display: flex !important;
            align-items: center !important;
            gap: 0.75rem !important;
            flex-wrap: nowrap !important;
            white-space: nowrap !important;
            width: 100% !important;
            overflow-x: auto !important;
        }}
        
        /* Ensure columns container uses flexbox */
        .pagination-flex-container ~ div [data-testid="column"],
        .element-container:has(.pagination-flex-container) [data-testid="column"] {{
            display: flex !important;
            flex-direction: column !important;
            flex-shrink: 0 !important;
            min-width: fit-content !important;
        }}
        
        /* Ensure columns stay on one line */
        .pagination-flex-container [data-testid="column"],
        .pagination-flex-container ~ div [data-testid="column"],
        .element-container:has(.pagination-flex-container) [data-testid="column"],
        .element-container .pagination-flex-container [data-testid="column"],
        /* Target columns that are siblings of pagination container */
        .pagination-flex-container + div [data-testid="column"],
        div:has(> .pagination-flex-container) [data-testid="column"] {{
            flex-shrink: 0 !important;
            min-width: fit-content !important;
            display: flex !important;
            flex-direction: column !important;
            justify-content: center !important;
            white-space: nowrap !important;
            max-width: none !important;
        }}
        
        /* Prevent any wrapping in pagination columns */
        .pagination-flex-container [data-testid="column"] *,
        .pagination-flex-container ~ div [data-testid="column"] *,
        .pagination-flex-container + div [data-testid="column"] * {{
            white-space: nowrap !important;
            flex-shrink: 0 !important;
        }}
        
        /* Ensure the columns container itself uses flexbox */
        div:has(> .pagination-flex-container) > div[data-testid="column"],
        .element-container:has(> .pagination-flex-container) > div[data-testid="column"] {{
            display: flex !important;
            flex-wrap: nowrap !important;
            white-space: nowrap !important;
        }}
        
        /* Consistent height for pagination elements */
        .pagination-flex-container .stButton > button,
        .pagination-flex-container ~ div .stButton > button {{
            height: 40px !important;
            min-height: 40px !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            border-radius: 10px !important;
        }}
        
        .pagination-flex-container .stNumberInput,
        .pagination-flex-container ~ div .stNumberInput {{
            height: 40px !important;
        }}
        
        .pagination-flex-container .stNumberInput > div > div > input,
        .pagination-flex-container ~ div .stNumberInput > div > div > input {{
            height: 40px !important;
            min-height: 40px !important;
        }}
        
        .pagination-flex-container .stSelectbox,
        .pagination-flex-container ~ div .stSelectbox {{
            height: 40px !important;
            display: flex !important;
            align-items: center !important;
        }}
        
        .pagination-flex-container .stSelectbox > div > div > select,
        .pagination-flex-container ~ div .stSelectbox > div > div > select {{
            height: 40px !important;
            min-height: 40px !important;
        }}
        
        .pagination-flex-container .stCaption,
        .pagination-flex-container ~ div .stCaption {{
            height: 40px !important;
            display: flex !important;
            align-items: center !important;
            margin: 0 !important;
            white-space: nowrap !important;
        }}
        
        /* Prevent wrapping in pagination container */
        .pagination-flex-container *,
        .pagination-flex-container ~ div * {{
            white-space: nowrap !important;
        }}
        
        /* Pagination label styling */
        .pagination-label {{
            white-space: nowrap !important;
            margin: 0 !important;
            padding: 0 !important;
            display: inline-flex !important;
            align-items: center !important;
            height: 40px !important;
            color: #000000 !important;
            font-size: 0.875rem !important;
        }}
        
        /* Ensure number input controls (minus/plus buttons) stay inline */
        .pagination-flex-container .stNumberInput button,
        .pagination-flex-container ~ div .stNumberInput button {{
            flex-shrink: 0 !important;
            white-space: nowrap !important;
        }}
        
        /* Ensure selectbox label is inline if visible */
        .pagination-flex-container .stSelectbox label,
        .pagination-flex-container ~ div .stSelectbox label {{
            white-space: nowrap !important;
            display: inline-block !important;
            margin-right: 0.5rem !important;
        }}
        
        /* Force all pagination elements to stay on one line */
        .pagination-flex-container,
        .pagination-flex-container > *,
        .pagination-flex-container [data-testid="column"],
        .pagination-flex-container [data-testid="column"] > * {{
            flex-wrap: nowrap !important;
            white-space: nowrap !important;
        }}
        
        /* Target Streamlit columns row directly */
        .pagination-flex-container ~ div.row-widget,
        .pagination-flex-container ~ div[data-testid="column"],
        div:has(> .pagination-flex-container) > div.row-widget.stHorizontal {{
            display: flex !important;
            align-items: center !important;
            gap: 0.75rem !important;
            flex-wrap: nowrap !important;
            white-space: nowrap !important;
            width: 100% !important;
            overflow-x: auto !important;
        }}
        
        /* Ensure all pagination columns are flex and don't wrap */
        .pagination-flex-container ~ div.row-widget [data-testid="column"],
        div:has(> .pagination-flex-container) > div.row-widget.stHorizontal [data-testid="column"] {{
            flex-shrink: 0 !important;
            min-width: fit-content !important;
        }}
        
        /* Responsive: horizontal scroll on smaller screens */
        @media (max-width: 768px) {{
            .pagination-flex-container {{
                overflow-x: auto !important;
                overflow-y: hidden !important;
                -webkit-overflow-scrolling: touch !important;
            }}
            
            .pagination-flex-container [data-testid="column"],
            .pagination-flex-container ~ div [data-testid="column"] {{
                flex-shrink: 0 !important;
                min-width: fit-content !important;
            }}
        }}
        
        /* Text Input Styling - Botpresso Design Guide */
        .stTextInput > div > div > input {{
            background-color: #ffffff !important;
            color: #1F2937 !important;
            border-radius: 6px !important; /* Slightly rounded corners */
            border: 1px solid #CCCCCC !important; /* Light grey border - Default state */
            padding: 0.625rem 0.875rem !important;
            font-size: 0.875rem !important;
            transition: border-color 0.2s ease !important;
            outline: none !important;
        }}
        
        /* Hover state - slightly darker grey border */
        .stTextInput > div > div > input:hover {{
            background-color: #ffffff !important;
            border-color: #999999 !important;
        }}
        
        /* Focus/Active state - vibrant purple border */
        .stTextInput > div > div > input:focus {{
            background-color: #ffffff !important;
            color: #1F2937 !important;
            border-color: {PRIMARY_BLUE} !important; /* #5046E5 */
            outline: none !important;
            box-shadow: none !important;
        }}
        
        /* Error state - red border */
        .stTextInput > div > div > input.error,
        .stTextInput.error > div > div > input {{
            border-color: {PRIMARY_RED} !important; /* #EF1E3B */
            background-color: #ffffff !important;
        }}
        
        /* Success state - green border */
        .stTextInput > div > div > input.success,
        .stTextInput.success > div > div > input {{
            border-color: {PRIMARY_GREEN} !important; /* #71D997 */
            background-color: #ffffff !important;
        }}
        
        /* Disabled state - light grey background and border */
        .stTextInput > div > div > input:disabled {{
            background-color: #F5F5F5 !important;
            border-color: #CCCCCC !important;
            color: #999999 !important;
            cursor: not-allowed !important;
            opacity: 0.7 !important;
        }}
        
        /* Placeholder text - light grey */
        .stTextInput > div > div > input::placeholder {{
            color: #999999 !important;
        }}
        
        /* Disabled placeholder */
        .stTextInput > div > div > input:disabled::placeholder {{
            color: #CCCCCC !important;
        }}
        
        /* Text Input Container */
        .stTextInput > div {{
            background-color: #ffffff !important;
        }}
        
        /* Metric Cards - Botpresso Theme */
        [data-testid="stMetricValue"] {{
            color: {PRIMARY_BLUE} !important;
            font-weight: 700 !important;
            font-size: 1.875rem !important;
        }}
        
        /* Info Boxes - Botpresso Theme with Shadows */
        .stInfo {{
            background-color: #ffffff !important;
            border: 1px solid #E5E7EB !important;
            border-left: 4px solid {PRIMARY_BLUE} !important;
            border-radius: 12px !important;
            box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06) !important;
            padding: 1rem !important;
        }}
        
        .stInfo p, .stInfo div, .stInfo span {{
            color: #1F2937 !important;
        }}
        
        .stInfo * {{
            color: #1F2937 !important;
        }}
        
        /* Success Messages - Botpresso Theme */
        .stSuccess {{
            background-color: {LIGHT_GREEN} !important;
            border-left: 4px solid {PRIMARY_GREEN} !important;
            border-radius: 12px !important;
            box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06) !important;
            padding: 1rem !important;
        }}
        
        .stSuccess p, .stSuccess div, .stSuccess span {{
            color: #1F2937 !important;
        }}
        
        /* Error Messages - Botpresso Theme */
        .stError {{
            background-color: {LIGHT_RED} !important;
            border-left: 4px solid {PRIMARY_RED} !important;
            border-radius: 12px !important;
            box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06) !important;
            padding: 1rem !important;
        }}
        
        .stError p, .stError div, .stError span {{
            color: #1F2937 !important;
        }}
        
        /* Warning Messages - Botpresso Theme */
        .stWarning {{
            background-color: #FFF4E6 !important;
            border-left: 4px solid #FF9800 !important;
            border-radius: 12px !important;
            box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06) !important;
            padding: 1rem !important;
        }}
        
        .stWarning p, .stWarning div, .stWarning span {{
            color: #1F2937 !important;
        }}
        
        /* Dataframe Styling - Botpresso Theme */
        .dataframe {{
            background-color: #ffffff !important;
            border-radius: 12px !important;
            overflow: hidden !important;
            box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06) !important;
        }}
        
        .dataframe thead {{
            background-color: #F9FAFB !important;
        }}
        
        .dataframe thead th {{
            background-color: #F9FAFB !important;
            color: #1F2937 !important;
            border: 1px solid #E5E7EB !important;
            font-weight: 600 !important;
            padding: 0.75rem 1rem !important;
        }}
        
        .dataframe tbody {{
            background-color: #ffffff !important;
        }}
        
        .dataframe tbody tr {{
            background-color: #ffffff !important;
            transition: background-color 0.2s ease !important;
        }}
        
        .dataframe tbody td {{
            background-color: #ffffff !important;
            color: #1F2937 !important;
            border: 1px solid #E5E7EB !important;
            padding: 0.75rem 1rem !important;
        }}
        
        .dataframe tbody tr:nth-child(even) {{
            background-color: #ffffff !important;
        }}
        
        .dataframe tbody tr:nth-child(odd) {{
            background-color: #FAFAFA !important;
        }}
        
        .dataframe tbody tr:hover {{
            background-color: #F3F4F6 !important;
        }}
        
        /* Streamlit Dataframe Container */
        [data-testid="stDataFrame"] {{
            background-color: #ffffff !important;
        }}
        
        [data-testid="stDataFrame"] table {{
            background-color: #ffffff !important;
        }}
        
        [data-testid="stDataFrame"] th,
        [data-testid="stDataFrame"] td {{
            background-color: #ffffff !important;
            color: #000000 !important;
        }}
        
        /* Selectbox Styling - Botpresso Design Guide */
        .stSelectbox > div > div > select {{
            background-color: #ffffff !important;
            color: #1F2937 !important;
            border-radius: 6px !important; /* Slightly rounded corners */
            border: 1px solid #CCCCCC !important; /* Light grey border - Default state */
            padding: 0.625rem 0.875rem !important;
            font-size: 0.875rem !important;
            transition: border-color 0.2s ease !important;
            outline: none !important;
        }}
        
        /* Hover state */
        .stSelectbox > div > div > select:hover {{
            border-color: #999999 !important;
        }}
        
        /* Focus/Active state */
        .stSelectbox > div > div > select:focus {{
            border-color: {PRIMARY_BLUE} !important; /* #5046E5 */
            outline: none !important;
            box-shadow: none !important;
        }}
        
        /* Disabled state */
        .stSelectbox > div > div > select:disabled {{
            background-color: #F5F5F5 !important;
            border-color: #CCCCCC !important;
            color: #999999 !important;
            cursor: not-allowed !important;
            opacity: 0.7 !important;
        }}
        
        .stSelectbox > div {{
            background-color: #ffffff !important;
        }}
        
        /* Selectbox Dropdown Options */
        .stSelectbox select option {{
            background-color: #ffffff !important;
            color: #1F2937 !important;
        }}
        
        /* Selectbox Label */
        .stSelectbox label {{
            color: #1F2937 !important;
            font-weight: 500 !important;
        }}
        
        /* Number Input Styling - Botpresso Design Guide */
        .stNumberInput > div > div > input {{
            background-color: #ffffff !important;
            color: #1F2937 !important;
            border-radius: 6px !important; /* Slightly rounded corners */
            border: 1px solid #CCCCCC !important; /* Light grey border - Default state */
            padding: 0.625rem 0.875rem !important;
            font-size: 0.875rem !important;
            transition: border-color 0.2s ease !important;
            outline: none !important;
        }}
        
        /* Hover state */
        .stNumberInput > div > div > input:hover {{
            border-color: #999999 !important;
        }}
        
        /* Focus/Active state */
        .stNumberInput > div > div > input:focus {{
            border-color: {PRIMARY_BLUE} !important; /* #5046E5 */
            outline: none !important;
            box-shadow: none !important;
        }}
        
        /* Disabled state */
        .stNumberInput > div > div > input:disabled {{
            background-color: #F5F5F5 !important;
            border-color: #CCCCCC !important;
            color: #999999 !important;
            cursor: not-allowed !important;
            opacity: 0.7 !important;
        }}
        
        .stNumberInput > div {{
            background-color: #ffffff !important;
        }}
        
        /* Number Input Container */
        .stNumberInput > div > div {{
            background-color: #ffffff !important;
        }}
        
        /* Number Input Label */
        .stNumberInput label {{
            color: #1F2937 !important;
            font-weight: 500 !important;
        }}
        
        /* Number Input Increment/Decrement Buttons - Botpresso Theme */
        .stNumberInput button {{
            background-color: #F9FAFB !important;
            color: #1F2937 !important;
            border: 1px solid #E5E7EB !important;
            border-radius: 8px !important;
            transition: all 0.2s ease !important;
        }}
        
        .stNumberInput button:hover {{
            background-color: #E5E7EB !important;
            border-color: {PRIMARY_BLUE} !important;
        }}
        
        /* Ensure all selectbox and number input containers are white */
        [data-baseweb="select"],
        [data-baseweb="input"] {{
            background-color: #ffffff !important;
        }}
        
        [data-baseweb="select"] > div,
        [data-baseweb="input"] > div {{
            background-color: #ffffff !important;
        }}
        
        /* BaseWeb Select Component */
        [data-baseweb="select"] input,
        [data-baseweb="select"] div {{
            background-color: #ffffff !important;
            color: #000000 !important;
        }}
        
        /* BaseWeb Select Dropdown */
        [data-baseweb="popover"] {{
            background-color: #ffffff !important;
        }}
        
        [data-baseweb="popover"] ul,
        [data-baseweb="popover"] li {{
            background-color: #ffffff !important;
            color: #000000 !important;
        }}
        
        /* BaseWeb Number Input */
        [data-baseweb="input"] input {{
            background-color: #ffffff !important;
            color: #000000 !important;
        }}
        
        /* Override any dark backgrounds in form elements */
        form .stSelectbox,
        form .stNumberInput {{
            background-color: #ffffff !important;
        }}
        
        form .stSelectbox *,
        form .stNumberInput * {{
            color: #000000 !important;
        }}
        
        /* Progress Bar */
        .stProgress > div > div > div > div {{
            background-color: {PRIMARY_BLUE};
        }}
        
        /* Download Button - Primary Style */
        .stDownloadButton > button {{
            background-color: #5046E5 !important;
            color: #FFFFFF !important;
            border: none !important;
            border-radius: 9999px !important;
            padding: 0.625rem 1.5rem !important;
            font-weight: 500 !important;
            transition: all 0.2s ease !important;
            min-height: 40px !important;
        }}
        
        .stDownloadButton > button:hover {{
            background-color: #4339d4 !important;
            color: #FFFFFF !important;
        }}
        
        .stDownloadButton > button:focus {{
            background-color: #5046E5 !important;
            color: #FFFFFF !important;
            outline: 2px solid #5046E5 !important;
            outline-offset: 2px !important;
        }}
        
        .stDownloadButton > button:active {{
            background-color: #3d32c2 !important;
            color: #FFFFFF !important;
        }}
        
        .stDownloadButton > button * {{
            color: #FFFFFF !important;
        }}
        
        .stDownloadButton > button svg,
        .stDownloadButton > button svg *,
        .stDownloadButton > button svg path {{
            fill: #FFFFFF !important;
            stroke: #FFFFFF !important;
            color: #FFFFFF !important;
        }}
        
        /* Hide Dataframe Action Icon Buttons */
        [data-testid="stDataFrame"] button,
        .stDataFrame button,
        button[title*="Download"],
        button[title*="Search"],
        button[title*="Fullscreen"],
        button[title*="Expand"],
        button[title*="Collapse"],
        button[aria-label*="Download"],
        button[aria-label*="Search"],
        button[aria-label*="Fullscreen"],
        button[aria-label*="Expand"],
        button[aria-label*="Collapse"] {{
            display: none !important;
            visibility: hidden !important;
            width: 0 !important;
            height: 0 !important;
            opacity: 0 !important;
        }}
        
        /* Hide dataframe toolbar button container if it only contains buttons */
        [data-testid="stDataFrame"] > div:first-child:has(button:only-child),
        [data-testid="stDataFrame"] > div:first-child > div:has(button:only-child),
        .stDataFrame > div:first-child:has(button:only-child) {{
            display: none !important;
            visibility: hidden !important;
        }}
        
        /* Hide empty button containers */
        [data-testid="stDataFrame"] > div:first-child:empty,
        .stDataFrame > div:first-child:empty {{
            display: none !important;
        }}
        
        /* Generic button icons styling */
        button svg,
        button svg *,
        button svg path {{
            color: #000000 !important;
            fill: #000000 !important;
            stroke: #000000 !important;
        }}
        
        /* Override white icons in buttons */
        button[style*="color: white"],
        button[style*="color:white"],
        button *[style*="color: white"],
        button *[style*="color:white"] {{
            color: #000000 !important;
        }}
        
        /* Hide Dataframe container buttons */
        div[data-testid="stDataFrame"] button,
        div[data-testid="stDataFrame"] button svg,
        div[data-testid="stDataFrame"] button path {{
            display: none !important;
            visibility: hidden !important;
        }}
        
        /* Hide Streamlit dataframe action bar buttons */
        [data-testid="stDataFrame"] > div > div button,
        [data-testid="stDataFrame"] > div > div button svg,
        [data-testid="stDataFrame"] > div > div button path {{
            display: none !important;
            visibility: hidden !important;
        }}
        
        /* Force all SVG icons to be black */
        svg,
        svg *,
        svg path,
        svg circle,
        svg rect,
        svg line {{
            color: #000000 !important;
            fill: #000000 !important;
            stroke: #000000 !important;
        }}
        
        /* Override white fills and strokes */
        svg[fill="white"],
        svg[fill="#ffffff"],
        svg[fill="#FFFFFF"],
        path[fill="white"],
        path[fill="#ffffff"],
        path[fill="#FFFFFF"] {{
            fill: #000000 !important;
        }}
        
        svg[stroke="white"],
        svg[stroke="#ffffff"],
        svg[stroke="#FFFFFF"],
        path[stroke="white"],
        path[stroke="#ffffff"],
        path[stroke="#FFFFFF"] {{
            stroke: #000000 !important;
        }}
        
        /* Hide Dataframe action buttons completely */
        [data-testid="stDataFrame"] button,
        [data-testid="stDataFrame"] button span,
        [data-testid="stDataFrame"] button p,
        [data-testid="stDataFrame"] button div,
        .stDataFrame button,
        .stDataFrame button span,
        .stDataFrame button p,
        .stDataFrame button div {{
            display: none !important;
            visibility: hidden !important;
        }}
        
        /* Hide dataframe toolbar container if it only contains buttons */
        [data-testid="stDataFrame"] > div:first-child:has(> button),
        [data-testid="stDataFrame"] > div:first-child > div:has(> button),
        .stDataFrame > div:first-child:has(> button),
        /* Alternative selectors for better browser support */
        [data-testid="stDataFrame"] > div:first-child,
        [data-testid="stDataFrame"] > div:first-child > div {{
            /* Hide if contains only buttons */
        }}
        
        /* Hide all buttons in dataframe toolbar area */
        [data-testid="stDataFrame"] > div:first-child button,
        [data-testid="stDataFrame"] > div:first-child > div button,
        [data-testid="stDataFrame"] > div:first-child > div > button,
        .stDataFrame > div:first-child button,
        .stDataFrame > div:first-child > div button {{
            display: none !important;
            visibility: hidden !important;
            width: 0 !important;
            height: 0 !important;
            padding: 0 !important;
            margin: 0 !important;
            opacity: 0 !important;
        }}
        
        /* Disabled Buttons - Reduced Opacity */
        .stButton > button:disabled,
        button:disabled {{
            background-color: #e5e7eb !important;
            color: #9ca3af !important;
            border: none !important;
            cursor: not-allowed !important;
            opacity: 0.6 !important;
            border-radius: 9999px !important;
        }}
        
        .stButton > button:disabled *,
        button:disabled * {{
            color: #9ca3af !important;
            opacity: 0.6 !important;
        }}
        
        .stButton > button:disabled svg,
        .stButton > button:disabled svg *,
        .stButton > button:disabled svg path,
        button:disabled svg,
        button:disabled svg *,
        button:disabled svg path {{
            fill: #9ca3af !important;
            stroke: #9ca3af !important;
            color: #9ca3af !important;
            opacity: 0.6 !important;
        }}
        
        /* Divider Styling */
        hr {{
            border: none;
            border-top: 1px solid #e5e7eb;
            margin: 2rem 0;
        }}
        
        /* Sidebar Branding - Botpresso Theme with Sharp Corners */
        .sidebar-brand {{
            padding: 1.5rem 1.25rem 1.5rem 1.25rem;
            border-bottom: 1px solid #E5E7EB;
            margin-bottom: 0;
            margin-top: 0 !important;
            border-radius: 0 !important;
        }}
        
        .sidebar-logo {{
            display: flex;
            align-items: center;
            gap: 0.5rem;
            margin-bottom: 0.5rem;
        }}
        
        .sidebar-logo-icon {{
            width: 32px;
            height: 32px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: {PRIMARY_BLUE} !important;
            font-size: 1.25rem;
            font-weight: 700;
            position: relative;
            line-height: 1;
            background-color: transparent !important;
            border: none !important;
        }}
        
        /* Logo icon styling - arrow with eyes */
        .sidebar-logo-icon {{
            font-family: monospace;
        }}
        
        /* Ensure logo icon content is visible and not black */
        .sidebar-logo-icon * {{
            color: {PRIMARY_BLUE} !important;
            background-color: transparent !important;
        }}
        
        .botpresso-brand {{
            color: {PRIMARY_BLUE} !important;
            font-size: 1.5rem !important;
            font-weight: 700 !important;
            margin: 0 !important;
            display: inline-block !important;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Inter', 'Helvetica Neue', Arial, sans-serif !important;
        }}
        
        .sidebar-brand h2 {{
            color: #1F2937 !important;
            margin: 0 !important;
            font-size: 1rem !important;
            font-weight: 600 !important;
            display: none !important;
        }}
        
        .sidebar-brand p {{
            color: #6B7280 !important;
            margin: 0.25rem 0 0 0 !important;
            font-size: 0.875rem !important;
            font-weight: 400 !important;
        }}
        
        /* Sidebar Navigation Items */
        .sidebar-nav {{
            padding: 0.5rem 0;
            border-radius: 0 !important;
        }}
        
        .sidebar-nav-item {{
            display: flex;
            align-items: center;
            gap: 0.75rem;
            padding: 0.75rem 1.25rem;
            color: #333333 !important;
            font-weight: 600 !important;
            font-size: 0.9375rem !important;
            text-decoration: none !important;
            border-radius: 0 !important;
            transition: background-color 0.2s ease;
            cursor: pointer;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Inter', 'Helvetica Neue', Arial, sans-serif !important;
        }}
        
        .sidebar-nav-item:hover {{
            background-color: #F9FAFB !important;
        }}
        
        .sidebar-nav-item.active {{
            background-color: {LIGHT_BLUE} !important;
            color: {PRIMARY_BLUE} !important;
        }}
        
        .sidebar-nav-icon {{
            width: 20px;
            height: 20px;
            color: #AEC4FF !important;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.125rem;
            flex-shrink: 0;
        }}
        
        .sidebar-nav-item.active .sidebar-nav-icon {{
            color: {PRIMARY_BLUE} !important;
        }}
        
        /* Navigation icons use CSS-based line icons (defined earlier) */
        
        .sidebar-nav-text {{
            color: inherit !important;
            font-weight: 600 !important;
        }}
        
        /* Status Indicators */
        .status-indicator {{
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.5rem 1rem;
            border-radius: 6px;
            background-color: #f9fafb;
        }}
        
        .status-dot {{
            width: 8px;
            height: 8px;
            border-radius: 50%;
            display: inline-block;
        }}
        
        .status-critical {{
            background-color: {LIGHT_RED};
        }}
        
        .status-warning {{
            background-color: #fff4e6;
        }}
        
        .status-normal {{
            background-color: {LIGHT_GREEN};
        }}
        
        /* Card Styling */
        .metric-card {{
            background: white;
            padding: 1.5rem;
            border-radius: 12px;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
            border: 1px solid #e5e7eb;
        }}
        
        /* Metric Containers - Botpresso Theme */
        [data-testid="stMetricContainer"] {{
            background: #FFFFFF !important;
            padding: 1.25rem !important;
            border-radius: 12px !important;
            border: 1px solid #E5E7EB !important;
            box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06) !important;
        }}
        
        /* Metric Labels - Botpresso Theme */
        [data-testid="stMetricLabel"] {{
            color: #6B7280 !important;
            font-weight: 500 !important;
            font-size: 0.875rem !important;
        }}
        
        /* Caption uses the typography system defined above */
        
        /* Table/Dataframe Text - Enhanced */
        .dataframe,
        .dataframe th,
        .dataframe td {{
            color: #000000 !important;
            background-color: #ffffff !important;
        }}
        
        /* All table elements */
        table {{
            background-color: #ffffff !important;
        }}
        
        table th {{
            background-color: #ffffff !important;
            color: #000000 !important;
        }}
        
        table td {{
            background-color: #ffffff !important;
            color: #000000 !important;
        }}
        
        table tr {{
            background-color: #ffffff !important;
        }}
        
        /* Streamlit dataframe wrapper */
        .stDataFrame {{
            background-color: #ffffff !important;
        }}
        
        .stDataFrame > div {{
            background-color: #ffffff !important;
        }}
        
        /* Index column styling */
        .dataframe .index_name,
        .dataframe .row_heading {{
            background-color: #ffffff !important;
            color: #000000 !important;
        }}
        
        /* Ensure all table borders are visible */
        .dataframe th,
        .dataframe td {{
            border-color: #e5e7eb !important;
        }}
        
        /* Override any dark theme for tables */
        [data-theme="dark"] .dataframe,
        [data-theme="dark"] table {{
            background-color: #ffffff !important;
        }}
        
        [data-theme="dark"] .dataframe th,
        [data-theme="dark"] .dataframe td,
        [data-theme="dark"] table th,
        [data-theme="dark"] table td {{
            background-color: #ffffff !important;
            color: #000000 !important;
        }}
        
        /* Selectbox Options - Enhanced */
        .stSelectbox select,
        .stSelectbox option {{
            background-color: #ffffff !important;
            color: #000000 !important;
        }}
        
        /* Dropdown Menu Styling */
        [role="listbox"],
        [role="option"] {{
            background-color: #ffffff !important;
            color: #000000 !important;
        }}
        
        [role="listbox"] [role="option"]:hover {{
            background-color: #f9fafb !important;
            color: #000000 !important;
        }}
        
        /* Number Input Text */
        .stNumberInput input {{
            color: #000000 !important;
        }}
        
        /* Text Input Text */
        .stTextInput input {{
            color: #000000 !important;
        }}
        
        /* Info/Success/Error/Warning Text */
        .stInfo p,
        .stSuccess p,
        .stError p,
        .stWarning p {{
            color: #000000 !important;
        }}
        
        /* Subheader Styling */
        h3 {{
            color: #1f2937;
            margin-top: 2rem;
        }}
        
        /* Hide Streamlit Menu, Footer, and Header */
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        header {{visibility: hidden; display: none !important; height: 0 !important;}}
        [data-testid="stHeader"] {{visibility: hidden; display: none !important; height: 0 !important;}}
        .stApp > header {{visibility: hidden; display: none !important; height: 0 !important;}}
        header[data-testid="stHeader"] {{visibility: hidden; display: none !important; height: 0 !important;}}
        
        /* Remove all top spacing */
        .main .block-container {{
            padding-top: 0 !important;
            margin-top: 0 !important;
        }}
        
        /* Remove top spacing from block-container's first child */
        .block-container > div:first-child,
        .block-container > *:first-child {{
            margin-top: 0 !important;
            padding-top: 0 !important;
        }}
        
        /* Remove any default Streamlit spacing */
        [class*="block-container"],
        [class*="element-container"] {{
            margin-top: 0 !important;
            padding-top: 0 !important;
        }}
        
        /* Ensure no spacing on the very first element */
        .main > .block-container > *:first-child,
        .main > .block-container > div:first-child > *:first-child {{
            margin-top: 0 !important;
            padding-top: 0 !important;
        }}
        
        /* Hide sidebar toggle button area */
        [data-testid="stSidebarToggle"] {{
            display: none !important;
            visibility: hidden !important;
            height: 0 !important;
            width: 0 !important;
        }}
        
        /* Hide any black box or placeholder at the very top of sidebar */
        [data-testid="stSidebar"] > div:first-child,
        [data-testid="stSidebar"] > div:first-child > div:first-child,
        [data-testid="stSidebar"] > div:first-child > div:first-child > div:first-child {{
            background-color: transparent !important;
        }}
        
        /* Target specific black box elements */
        [data-testid="stSidebar"] div[style*="background"],
        [data-testid="stSidebar"] > div > div > div[style*="background"] {{
            background-color: transparent !important;
        }}
        
        /* Hide any element with black background in sidebar top area */
        [data-testid="stSidebar"] > div:first-child div[style*="black"],
        [data-testid="stSidebar"] > div:first-child div[style*="#000"],
        [data-testid="stSidebar"] > div:first-child div[style*="rgb(0, 0, 0)"] {{
            display: none !important;
            visibility: hidden !important;
        }}
        
        /* Hide any small black squares or boxes (common placeholder size) */
        [data-testid="stSidebar"] div[style*="width"][style*="height"][style*="black"],
        [data-testid="stSidebar"] div[style*="width: 8px"][style*="height: 8px"],
        [data-testid="stSidebar"] div[style*="width: 16px"][style*="height: 16px"],
        [data-testid="stSidebar"] div[style*="width: 24px"][style*="height: 24px"] {{
            background-color: transparent !important;
        }}
        
        /* Hide Streamlit sidebar header if it exists */
        [data-testid="stSidebar"] [class*="header"],
        [data-testid="stSidebar"] [class*="Header"],
        [data-testid="stSidebar"] [id*="header"],
        [data-testid="stSidebar"] [id*="Header"] {{
            display: none !important;
            visibility: hidden !important;
            height: 0 !important;
        }}
        
        /* Remove top spacing from app containers */
        .appview-container {{
            padding-top: 0 !important;
            margin-top: 0 !important;
        }}
        
        [data-testid="stAppViewContainer"] {{
            padding-top: 0 !important;
            margin-top: 0 !important;
        }}
        
        /* Remove top spacing from main content */
        .main {{
            padding-top: 0 !important;
            margin-top: 0 !important;
        }}
        
        /* Remove top spacing from first elements */
        .main .block-container > div:first-child,
        .main h1:first-child,
        .main .element-container:first-child,
        .main .stMarkdown:first-child,
        .main > div:first-child {{
            margin-top: 0 !important;
            padding-top: 0 !important;
        }}
        
        /* Remove top spacing from all element containers */
        .element-container {{
            margin-top: 0 !important;
            padding-top: 0 !important;
        }}
        
        .element-container:first-child {{
            margin-top: 0 !important;
            padding-top: 0 !important;
        }}
        
        /* Remove top spacing from markdown containers */
        .stMarkdown:first-child,
        .stMarkdownContainer:first-child {{
            margin-top: 0 !important;
            padding-top: 0 !important;
        }}
        
        /* Remove top spacing from Streamlit columns */
        .stColumn:first-child {{
            margin-top: 0 !important;
            padding-top: 0 !important;
        }}
        
        /* Ensure all text on white backgrounds is black */
        body {{
            background-color: #ffffff !important;
            color: #000000 !important;
        }}
        
        /* Streamlit app container */
        .appview-container {{
            background-color: #ffffff !important;
            color: #000000 !important;
        }}
        
        /* Block containers */
        .block-container {{
            background-color: #ffffff !important;
            color: #000000 !important;
        }}
        
        /* List items - Botpresso Theme */
        ul li, ol li {{
            color: #1F2937 !important;
        }}
        
        /* Strong and emphasis text - Botpresso Theme */
        strong, b {{
            color: #1F2937 !important;
            font-weight: 600 !important;
        }}
        
        /* Code blocks - Botpresso Theme */
        code {{
            color: #1F2937 !important;
            background-color: #F3F4F6 !important;
            padding: 0.125rem 0.375rem !important;
            border-radius: 6px !important;
            font-size: 0.875rem !important;
        }}
        
        pre code {{
            background-color: #F3F4F6 !important;
            padding: 1rem !important;
            border-radius: 10px !important;
            display: block !important;
        }}
        
        /* All paragraphs and text elements - Botpresso Theme */
        p, span, label, li, td, th {{
            color: #1F2937 !important;
        }}
        
        /* Override any Streamlit default dark backgrounds - Botpresso Theme */
        section[data-testid="stSidebar"],
        section[data-testid="stSidebar"] > div,
        .element-container,
        .stMarkdown,
        .stMarkdownContainer {{
            background-color: transparent !important;
            color: #1F2937 !important;
        }}
        
        /* Checkbox container - Botpresso Theme */
        .stCheckbox > label {{
            color: #1F2937 !important;
            font-weight: 500 !important;
        }}
        
        .stCheckbox > div {{
            background-color: #ffffff !important;
        }}
        
        /* Checkbox input styling */
        .stCheckbox input[type="checkbox"] {{
            border-radius: 4px !important;
            border: 1px solid #E5E7EB !important;
        }}
        
        .stCheckbox input[type="checkbox"]:checked {{
            background-color: {PRIMARY_BLUE} !important;
            border-color: {PRIMARY_BLUE} !important;
        }}
    </style>
    """, unsafe_allow_html=True)

# Configuration
REQUEST_TIMEOUT = 10  # seconds
REQUEST_DELAY = 0.5   # seconds between requests to be respectful
MAX_RETRIES = 3


def is_html_url(url: str) -> bool:
    """
    Check if a URL points to an HTML page.
    Filters out images, PDFs, videos, XML, and other non-HTML resources.
    """
    parsed = urlparse(url)
    path = parsed.path.lower()
    
    non_html_extensions = {
        '.jpg', '.jpeg', '.png', '.gif', '.svg', '.webp', '.ico',
        '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx',
        '.mp4', '.avi', '.mov', '.wmv', '.flv', '.webm',
        '.mp3', '.wav', '.ogg', '.flac',
        '.xml', '.rss', '.atom',
        '.zip', '.rar', '.tar', '.gz',
        '.css', '.js', '.json',
        '.txt', '.csv',
    }
    
    for ext in non_html_extensions:
        if path.endswith(ext):
            return False
    
    if not path or path.endswith('/') or path.endswith('.html') or path.endswith('.htm'):
        return True
    
    if '.' not in path.split('/')[-1]:
        return True
    
    return True


def fetch_sitemap(url: str) -> BeautifulSoup:
    """Fetch and parse an XML sitemap from a URL."""
    for attempt in range(MAX_RETRIES):
        try:
            response = requests.get(url, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'xml')
            return soup
        except requests.exceptions.RequestException as e:
            if attempt < MAX_RETRIES - 1:
                time.sleep(REQUEST_DELAY * (attempt + 1))
            else:
                raise Exception(f"Failed to fetch {url} after {MAX_RETRIES} attempts: {str(e)}")
    
    raise Exception(f"Failed to fetch sitemap: {url}")


def is_sitemap_index(soup: BeautifulSoup) -> bool:
    """Check if the parsed XML is a sitemap index or a URL set."""
    if soup.find('sitemap'):
        return True
    if soup.find('url'):
        return False
    return False


def extract_sitemap_urls(soup: BeautifulSoup) -> List[str]:
    """Extract sitemap URLs from a sitemap index."""
    sitemap_urls = []
    sitemap_tags = soup.find_all('sitemap')
    
    for sitemap_tag in sitemap_tags:
        loc_tag = sitemap_tag.find('loc')
        if loc_tag and loc_tag.text:
            sitemap_urls.append(loc_tag.text.strip())
    
    return sitemap_urls


def extract_page_urls(soup: BeautifulSoup) -> List[str]:
    """Extract page URLs from a URL set sitemap."""
    page_urls = []
    url_tags = soup.find_all('url')
    
    for url_tag in url_tags:
        loc_tag = url_tag.find('loc')
        if loc_tag and loc_tag.text:
            url = loc_tag.text.strip()
            if is_html_url(url):
                page_urls.append(url)
    
    return page_urls


def process_sitemap(url: str, visited: Set[str], all_urls: Set[str], status_container, progress_bar) -> None:
    """Recursively process a sitemap URL with UI updates."""
    if url in visited:
        return
    
    visited.add(url)
    
    try:
        soup = fetch_sitemap(url)
        time.sleep(REQUEST_DELAY)
        
        if is_sitemap_index(soup):
            child_sitemaps = extract_sitemap_urls(soup)
            status_container.text(f"Processing sitemap index: {url} ({len(child_sitemaps)} child sitemaps)")
            
            for i, child_url in enumerate(child_sitemaps):
                if progress_bar:
                    progress_bar.progress((i + 1) / len(child_sitemaps))
                process_sitemap(child_url, visited, all_urls, status_container, None)
        else:
            page_urls = extract_page_urls(soup)
            status_container.text(f"Extracting URLs from: {url} ({len(page_urls)} HTML URLs found)")
            all_urls.update(page_urls)
            
    except Exception as e:
        status_container.warning(f"Error processing {url}: {str(e)}")


def main():
    """Main Streamlit app."""
    # Inject Botpresso CSS
    inject_botpresso_css()
    
    # Sidebar with Botpresso branding and navigation
    with st.sidebar:
        # Logo and Branding
        st.markdown("""
        <div class="sidebar-brand">
            <div class="sidebar-logo">
                <div class="sidebar-logo-icon">▲</div>
                <span class="botpresso-brand">SEOvigil</span>
            </div>
            <p>Powered by Botpresso</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Navigation Items
        st.markdown("""
        <div class="sidebar-nav">
            <div class="sidebar-nav-item active">
                <div class="sidebar-nav-icon nav-icon-projects"></div>
                <span class="sidebar-nav-text">Projects</span>
            </div>
            <div class="sidebar-nav-item">
                <div class="sidebar-nav-icon nav-icon-reports"></div>
                <span class="sidebar-nav-text">Reports</span>
            </div>
            <div class="sidebar-nav-item">
                <div class="sidebar-nav-icon nav-icon-monitor"></div>
                <span class="sidebar-nav-text">Monitor Links</span>
            </div>
            <div class="sidebar-nav-item">
                <div class="sidebar-nav-icon nav-icon-vitals"></div>
                <span class="sidebar-nav-text">Web Vitals</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Settings Section
        st.markdown("---")
        st.markdown("### Settings")
        show_progress = st.checkbox("Show detailed progress", value=True)
    
    # Main content area
    st.title("XML Sitemap URL Extractor")
    st.markdown("Extract HTML page URLs from XML sitemaps with support for nested sitemap indexes.")
    
    # Main content area
    col1, col2 = st.columns([3, 1])
    
    with col1:
        sitemap_url = st.text_input(
            "Sitemap URL",
            placeholder="https://example.com/sitemap.xml"
        )
    
    with col2:
        st.write("")  # Spacing
        extract_button = st.button("Extract URLs", type="primary", use_container_width=True)
    
    # Processing area
    if extract_button:
        # Strip whitespace from the URL
        sitemap_url = sitemap_url.strip() if sitemap_url else ""
        
        if not sitemap_url:
            st.error("Please enter a sitemap URL")
            return
        
        if not sitemap_url.startswith(('http://', 'https://')):
            st.error("Please enter a valid sitemap URL starting with http:// or https://")
            return
        
        # Initialize session state
        if 'extraction_complete' not in st.session_state:
            st.session_state.extraction_complete = False
        
        # Create containers for status updates
        status_container = st.empty()
        progress_container = st.empty()
        results_container = st.container()
        
        # Initialize progress
        status_container.info("Starting extraction...")
        progress_bar = progress_container.progress(0) if show_progress else None
        
        # Track visited sitemaps and collected URLs
        visited_sitemaps: Set[str] = set()
        html_urls: Set[str] = set()
        
        try:
            # Process the sitemap
            start_time = time.time()
            process_sitemap(sitemap_url, visited_sitemaps, html_urls, status_container, progress_bar)
            
            # Update progress bar
            if progress_bar:
                progress_bar.progress(1.0)
            
            # Convert to sorted list
            sorted_urls = sorted(html_urls)
            elapsed_time = time.time() - start_time
            
            # Store URLs in session state for pagination
            st.session_state.extraction_complete = True
            st.session_state.urls = sorted_urls
            st.session_state.visited_sitemaps_count = len(visited_sitemaps)
            
            # Display results
            status_container.success(f"Extraction complete! Found {len(html_urls)} HTML URLs in {elapsed_time:.2f} seconds")
            
            with results_container:
                st.header("Results")
                
                # Statistics
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total HTML URLs", len(html_urls))
                with col2:
                    st.metric("Sitemaps Processed", len(visited_sitemaps))
                with col3:
                    st.metric("Processing Time", f"{elapsed_time:.2f}s")
                
                # Display URLs with pagination
                if sorted_urls:
                    # Pagination controls
                    st.subheader("All URLs")
                    
                    # Items per page selector
                    items_per_page_options = [25, 50, 100, 200, 500]
                    if 'items_per_page' not in st.session_state:
                        st.session_state.items_per_page = 50
                    
                    if 'current_page' not in st.session_state:
                        st.session_state.current_page = 1
                    
                    # Get current items_per_page for initial calculation
                    items_per_page = st.session_state.items_per_page
                    total_urls = len(sorted_urls)
                    total_pages = (total_urls + items_per_page - 1) // items_per_page if items_per_page > 0 else 1
                    
                    # All pagination controls in one line using flexbox
                    st.markdown('''
                    <div class="pagination-flex-container" style="display: flex; align-items: center; gap: 0.75rem; flex-wrap: nowrap; white-space: nowrap; width: 100%; overflow-x: auto;">
                    ''', unsafe_allow_html=True)
                    
                    nav_col1, nav_col2, nav_col3, nav_col4, nav_col5 = st.columns([0.8, 0.8, 1.2, 0.6, 1.5], gap="small")
                    
                    with nav_col1:
                        if st.button("Previous", disabled=st.session_state.current_page == 1, key="prev_btn_main", use_container_width=True):
                            if st.session_state.current_page > 1:
                                st.session_state.current_page -= 1
                                st.rerun()
                    
                    with nav_col2:
                        if st.button("Next", disabled=st.session_state.current_page >= total_pages, key="next_btn_main", use_container_width=True):
                            if st.session_state.current_page < total_pages:
                                st.session_state.current_page += 1
                                st.rerun()
                    
                    with nav_col3:
                        # Page number input (includes minus and plus buttons)
                        page_input = st.number_input(
                            "Page",
                            min_value=1,
                            max_value=total_pages,
                            value=st.session_state.current_page,
                            key="page_input",
                            label_visibility="collapsed"
                        )
                        if page_input != st.session_state.current_page:
                            st.session_state.current_page = int(page_input)
                            st.rerun()
                    
                    with nav_col4:
                        st.caption(f"of {total_pages}")
                    
                    with nav_col5:
                        items_per_page = st.selectbox(
                            "",
                            options=items_per_page_options,
                            index=items_per_page_options.index(st.session_state.items_per_page) if st.session_state.items_per_page in items_per_page_options else 1,
                            key="items_per_page_selector",
                            label_visibility="collapsed"
                        )
                        if items_per_page != st.session_state.items_per_page:
                            st.session_state.items_per_page = items_per_page
                            st.rerun()
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Recalculate pagination after items per page change
                    items_per_page = st.session_state.items_per_page
                    total_pages = (total_urls + items_per_page - 1) // items_per_page if items_per_page > 0 else 1
                    if st.session_state.current_page > total_pages:
                        st.session_state.current_page = total_pages
                    
                    # Calculate start and end indices
                    current_page = st.session_state.current_page
                    start_idx = (current_page - 1) * items_per_page
                    end_idx = min(start_idx + items_per_page, total_urls)
                    
                    # Display page info
                    st.info(f"Showing page {current_page} of {total_pages} | URLs {start_idx + 1} to {end_idx} of {total_urls}")
                    
                    # Display URLs for current page
                    page_urls = sorted_urls[start_idx:end_idx]
                    urls_df = pd.DataFrame({'URL': page_urls})
                    urls_df.index = range(start_idx + 1, end_idx + 1)  # Start index from 1
                    
                    st.dataframe(urls_df, use_container_width=True, height=400)
                    
                    # Download button
                    st.divider()
                    csv_data = pd.DataFrame({'URL': sorted_urls}).to_csv(index=False)
                    st.download_button(
                        label="📥 Download Report",
                        data=csv_data,
                        file_name="sitemap_urls.csv",
                        mime="text/csv",
                        type="primary",
                        use_container_width=True
                    )
                else:
                    st.warning("No HTML URLs found in the sitemap(s).")
            
        except Exception as e:
            status_container.error(f"❌ Error: {str(e)}")
            st.exception(e)
    
    # Show previous results if available
    elif 'extraction_complete' in st.session_state and st.session_state.extraction_complete:
        if 'urls' in st.session_state and st.session_state.urls:
            sorted_urls = st.session_state.urls
            
            st.header("Previous Results")
            
            # Statistics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total HTML URLs", len(sorted_urls))
            with col2:
                st.metric("Sitemaps Processed", st.session_state.get('visited_sitemaps_count', 0))
            with col3:
                st.metric("Status", "Complete")
            
            # Pagination controls
            st.subheader("All URLs")
            
            # Items per page selector
            items_per_page_options = [25, 50, 100, 200, 500]
            if 'items_per_page' not in st.session_state:
                st.session_state.items_per_page = 50
            
            if 'current_page' not in st.session_state:
                st.session_state.current_page = 1
            
            # Get current items_per_page for initial calculation
            items_per_page = st.session_state.items_per_page
            total_urls = len(sorted_urls)
            total_pages = (total_urls + items_per_page - 1) // items_per_page if items_per_page > 0 else 1
            
            # All pagination controls in one line using flexbox
            st.markdown('''
            <div class="pagination-flex-container" style="display: flex; align-items: center; gap: 0.75rem; flex-wrap: nowrap; white-space: nowrap; width: 100%; overflow-x: auto;">
            ''', unsafe_allow_html=True)
            
            nav_col1, nav_col2, nav_col3, nav_col4, nav_col5 = st.columns([0.8, 0.8, 1.2, 0.6, 1.5], gap="small")
            
            with nav_col1:
                if st.button("Previous", disabled=st.session_state.current_page == 1, key="prev_btn_prev", use_container_width=True):
                    if st.session_state.current_page > 1:
                        st.session_state.current_page -= 1
                        st.rerun()
            
            with nav_col2:
                if st.button("Next", disabled=st.session_state.current_page >= total_pages, key="next_btn_prev", use_container_width=True):
                    if st.session_state.current_page < total_pages:
                        st.session_state.current_page += 1
                        st.rerun()
            
            with nav_col3:
                # Page number input (includes minus and plus buttons)
                page_input = st.number_input(
                    "Page",
                    min_value=1,
                    max_value=total_pages,
                    value=st.session_state.current_page,
                    key="page_input_prev",
                    label_visibility="collapsed"
                )
                if page_input != st.session_state.current_page:
                    st.session_state.current_page = int(page_input)
                    st.rerun()
            
            with nav_col4:
                st.caption(f"of {total_pages}")
            
            with nav_col5:
                items_per_page = st.selectbox(
                    "",
                    options=items_per_page_options,
                    index=items_per_page_options.index(st.session_state.items_per_page) if st.session_state.items_per_page in items_per_page_options else 1,
                    key="items_per_page_selector_prev",
                    label_visibility="collapsed"
                )
                if items_per_page != st.session_state.items_per_page:
                    st.session_state.items_per_page = items_per_page
                    st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Recalculate pagination after items per page change
            items_per_page = st.session_state.items_per_page
            total_pages = (total_urls + items_per_page - 1) // items_per_page if items_per_page > 0 else 1
            if st.session_state.current_page > total_pages:
                st.session_state.current_page = total_pages
            
            # Calculate start and end indices
            current_page = st.session_state.current_page
            start_idx = (current_page - 1) * items_per_page
            end_idx = min(start_idx + items_per_page, total_urls)
            
            # Display page info
            st.info(f"Showing page {current_page} of {total_pages} | URLs {start_idx + 1} to {end_idx} of {total_urls}")
            
            # Display URLs for current page
            page_urls = sorted_urls[start_idx:end_idx]
            urls_df = pd.DataFrame({'URL': page_urls})
            urls_df.index = range(start_idx + 1, end_idx + 1)
            
            st.dataframe(urls_df, use_container_width=True, height=400)
            
            # Download button
            st.divider()
            csv_data = pd.DataFrame({'URL': sorted_urls}).to_csv(index=False)
            st.download_button(
                label="📥 Download Report",
                data=csv_data,
                file_name="sitemap_urls.csv",
                mime="text/csv",
                type="primary",
                use_container_width=True
            )
            
            st.info("💡 Enter a new sitemap URL above and click 'Extract URLs' to process another sitemap.")


if __name__ == '__main__':
    main()
