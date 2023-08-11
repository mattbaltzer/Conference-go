from django.http import JsonResponse
from common.json import ModelEncoder
from .models import Presentation
from events.models import Conference
from events.api_views import ConferenceListEncoder
from django.views.decorators.http import require_http_methods
import json

class PrensentationListEncoder(ModelEncoder):
    model = Presentation
    properties = [
        "title",
        "status",
    ]

@require_http_methods(["GET", "POST"])
def api_list_presentations(request, conference_id):
    if request.method == "GET":
        presentations = Presentation.objects.filter(conference=conference_id)
        return JsonResponse(
            {"presentations": presentations},
            encoder=PrensentationListEncoder
            )
    else:
        content = json.loads(request.body)
        try:
            conference = Conference.objects.get(id=conference_id)
            content["conference"] = conference
        except Conference.DoesNotExist:
            return JsonResponse(
                {"message": "Invalid presentation id"},
                status=400,
            )
        presentation = Presentation.create(**content)
        return JsonResponse(
            presentation,
            encoder=PresentationDetailEncoder,
            safe=False,
        )


class PresentationDetailEncoder(ModelEncoder):
    model = Presentation
    properties = [
        "presenter_name",
        "company_name",
        "presenter_email",
        "title",
        "synopsis",
        "created",
    ]


@require_http_methods(["DELETE", "GET", "PUT"])
def api_show_presentation(request, id):
    if request.method == "GET":
        presentation = Presentation.objects.get(id=id)
        return JsonResponse(
            presentation,
            encoder=PresentationDetailEncoder,
            safe=False,
        )
    elif request.method == "DELETE":
        count, _ = Presentation.objects.filter(id=id).delete()
        return JsonResponse({"deleted": count > 0})
    else:
        content = json.loads(request.body)
        Presentation.objects.filter(id=id).update(**content)
        presentation = Presentation.objects.get(id=id)
        return JsonResponse(
            presentation,
            encoder=PresentationDetailEncoder,
            safe=False,
        )
