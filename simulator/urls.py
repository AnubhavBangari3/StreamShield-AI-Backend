from django.urls import path

from .views import (
    generate_simulation,
    scenario_list,
)

urlpatterns = [
    path(
        "scenarios/",
        scenario_list,
        name="simulation-scenarios",
    ),
    path(
        "generate/",
        generate_simulation,
        name="generate-simulation",
    ),
]