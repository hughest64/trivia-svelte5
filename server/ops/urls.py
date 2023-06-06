from django.urls import path, re_path
from django.shortcuts import redirect

from .views import ops

app_name = "ops"

urlpatterns = [
    path("game-setup/", ops.GameSetupView.as_view(), name="game_setup"),
    path("game-delete/", ops.GameDeleteView.as_view(), name="game_delete"),
    path("rlock/<joincode>/", ops.HostControlsView.as_view(), name="round_lock"),
    path("run-game/", ops.RunGameView.as_view(), name="run_game"),
    path("validate/", ops.ValidateDataView.as_view(), name="validate"),
]
