from django.dispatch import receiver
from django.utils.translation import get_language
from pretalx.mail.domain.placeholders import TrustedPlainMailTextPlaceholder
from pretalx.mail.signals import register_mail_placeholders
from pretalx.schedule.domain.notifications import get_current_notifications

TEXT = {
    "de": (
        "Barrierefreier Bühnenzugang kann in diesem Saal derzeit nicht garantiert werden. "
        "Falls du darauf angewiesen bist, antworte bitte kurzfristig per E-Mail.\n\n"
    ),
    "en": (
        "We cannot currently guarantee an accessible route to the stage in this room. "
        "If you need one, please reply promptly by email.\n\n"
    ),
}


def hint_text():
    return TEXT["de" if (get_language() or "").startswith("de") else "en"]


def saal45_spezial(user, event):
    changes = get_current_notifications(user, event)
    slots = list(changes["create"]) + [
        change["new_slot"] for change in changes["update"]
    ]
    if any(
        slot and slot.room and str(slot.room.name).casefold() in {"modify"}
        for slot in slots
    ):
        return hint_text()
    return ""


@receiver(register_mail_placeholders)
def register_placeholders(sender, **kwargs):
    return TrustedPlainMailTextPlaceholder(
        "saal45_spezial", ["user", "event"], saal45_spezial, lambda event: hint_text()
    )
