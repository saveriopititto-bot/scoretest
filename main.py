import flet as ft
import os
import logging
from config import Config
from services.strava_api import StravaService
from services.db import DatabaseService
from views.landing import LandingView
from views.dashboard import DashboardView
from views.demo import DemoView
from ui.state_manager import AppState

# Setup Logging
logger = Config.setup_logging()
logger.info("Starting sCore Flet App...")

def main(page: ft.Page):
    # Page Configuration
    page.title = Config.APP_TITLE
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 0
    page.spacing = 0
    page.bgcolor = "#0a0a0a"
    page.window.width = 1400
    page.window.height = 900
    
    # Check secrets
    missing_secrets = Config.check_secrets()
    if missing_secrets:
        page.add(
            ft.Container(
                content=ft.Text(
                    f"❌ Segreti mancanti: {', '.join(missing_secrets)}",
                    color=ft.colors.RED,
                    size=20,
                ),
                alignment=ft.alignment.center,
                expand=True,
            )
        )
        return
    
    # Initialize Services
    strava_creds = Config.get_strava_creds()
    supa_creds = Config.get_supabase_creds()
    auth_svc = StravaService(strava_creds["client_id"], strava_creds["client_secret"])
    db_svc = DatabaseService(supa_creds["url"], supa_creds["key"])
    
    # Initialize State
    state = AppState(page)
    
    # Navigation Function
    def navigate_to(view_name: str):
        """Navigate between views"""
        page.controls.clear()
        
        if view_name == "landing":
            view = LandingView(page, state, auth_svc, navigate_to)
        elif view_name == "dashboard":
            view = DashboardView(page, state, auth_svc, db_svc, navigate_to)
        elif view_name == "demo":
            view = DemoView(page, state, navigate_to)
        else:
            view = LandingView(page, state, auth_svc, navigate_to)
        
        page.add(view.build())
        page.update()
    
    # Handle OAuth callback
    def route_change(e: ft.RouteChangeEvent):
        """Handle route changes and OAuth callbacks"""
        route = page.route
        logger.info(f"Route changed to: {route}")
        
        # Check for OAuth code in route
        if "?code=" in route:
            code = route.split("?code=")[1].split("&")[0]
            token = auth_svc.exchange_token(code)
            if token:
                state.strava_token = token
                page.route = "/"
                navigate_to("dashboard")
        else:
            # Normal navigation
            if state.show_demo_page:
                navigate_to("demo")
            elif not state.strava_token:
                navigate_to("landing")
            else:
                navigate_to("dashboard")
    
    page.on_route_change = route_change
    
    # Initial navigation
    if state.show_demo_page:
        navigate_to("demo")
    elif state.strava_token:
        navigate_to("dashboard")
    else:
        navigate_to("landing")

if __name__ == "__main__":
    # Leggi porta da environment variable (Render)
    port = int(os.getenv("PORT", 8550))
    
    # Web mode per Render
    ft.app(
        target=main, 
        view=ft.AppView.WEB_BROWSER,
        port=port,
        host="0.0.0.0"  # Importante per Render!
    )
