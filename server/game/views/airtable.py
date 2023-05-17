import json

from django.contrib import messages
from django.core import management
from django.shortcuts import redirect
from django.urls import reverse


def airtable_import(request):
    query_params = request.GET
    start = query_params.get("start")
    end = query_params.get("end")
    superuser = request.user.is_superuser
    if not superuser:
        return redirect("/")

    try:
        msg = management.call_command("airtable_import", start=start, end=end)
        data = json.loads(msg)
        messages.success(
            request,
            data.get(
                "stats",
                "An Error Occured. Check the Airtable Log for More Information.",
            ),
        )

        # if there were any anomolies in the game data, report it to the user
        validation_data = data.get("validation")
        if validation_data:
            for game in validation_data:
                messages.warning(request, game)

    except Exception as e:
        messages.error(request, e)

    return redirect(reverse("admin:game_game_changelist"))
