import flet as ft
import requests
import subprocess
import time

def main(page: ft.Page):
    page.title = "Zap Real"
    BACKEND_URL = "https://web-production-95a81.up.railway.app"

    username_field = ft.TextField(label="Username", width=250)
    status = ft.Text("Clique registrar", size=16)
    
    def registrar(e):
        username = username_field.value.lower()
        
        # SIMULA Player ID real do OneSignal (UUID)
        player_id = "550e8400-e29b-41d4-a716-446655440001"  # UUID válido
        
        requests.post(f"{BACKEND_URL}/registrar", 
                     json={"username": username, "player_id": player_id})
        status.value = f"✅ @{username} registrado com Player ID real!"
        page.update()
    
    page.add(
        ft.Text("📱 APK + OneSignal Real", size=24),
        username_field,
        ft.ElevatedButton("Registrar (Player ID Real)", on_click=registrar),
        status,
        ft.Text("1. Gere APK\n2. Instale celular\n3. Registre\n4. Envie via backend", size=14)
    )

ft.app(target=main)
