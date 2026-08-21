from django.shortcuts import render

import json
import threading
from django.http import JsonResponse
from django.db.models import Avg
from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import csrf_protect
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from .models import Avis, Contact

def home(request):
    return render(request, "index.html")

def vache(request):
    return render(request, "produits.html")

def contact(request):
    return render(request, "contact.html")

def mouton(request):
    return render(request, "mouton.html")

def tousproduits(request):
    return render(request, "tous-produits.html")


def _serialize_avis(a):
    return {
        'id': a.id,
        'name': a.name,
        'rating': a.rating,
        'message': a.message,
        'created_at': a.created_at.isoformat(),
    }


def _send_avis_thanks_email(avis):
    """Envoie l'email de remerciement. Ne doit jamais faire échouer la requête appelante."""
    try:
        context = {
            'name': avis.name,
            'rating': avis.rating,
            'message': avis.message,
            'stars_range': range(5),
        }
        html_content = render_to_string('avis_thanks.html', context)
        text_content = (
            f"Bonjour {avis.name},\n\n"
            f"Merci d'avoir laissé un avis ({avis.rating}/5) chez AL BASSATINE VIANDES.\n"
            f"Votre message : {avis.message}\n\n"
            f"L'équipe AL BASSATINE VIANDES"
        )
        email = EmailMultiAlternatives(
            subject="Merci pour votre avis — AL BASSATINE VIANDES",
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[avis.email],
        )
        email.attach_alternative(html_content, "text/html")
        email.send(fail_silently=True)
    except Exception:
        # on ne bloque jamais la réponse HTTP pour un problème d'email
        pass


@csrf_protect
@require_POST
def submit_avis(request):
    try:
        data = json.loads(request.body)
        name = (data.get('name') or '').strip()
        email = (data.get('email') or '').strip()
        rating = int(data.get('rating') or 0)
        message = (data.get('message') or '').strip()

        if not name or not email or not message:
            return JsonResponse({'ok': False, 'error': 'champs_manquants'}, status=400)
        if rating < 1 or rating > 5:
            return JsonResponse({'ok': False, 'error': 'note_invalide'}, status=400)

        avis = Avis.objects.create(name=name, email=email, rating=rating, message=message[:400])

        # envoi en arrière-plan pour ne pas ralentir la réponse au visiteur
        threading.Thread(target=_send_avis_thanks_email, args=(avis,), daemon=True).start()

        return JsonResponse({'ok': True, 'avis': _serialize_avis(avis)})
    except (json.JSONDecodeError, ValueError):
        return JsonResponse({'ok': False, 'error': 'donnees_invalides'}, status=400)


def _send_contact_emails(contact):
    """Envoie l'accusé de réception au visiteur + la notification interne.
    Ne doit jamais faire échouer la requête appelante (fail_silently)."""
    try:
        # Accusé de réception au visiteur
        text_content = (
            f"Bonjour {contact.name},\n\n"
            f"Merci de nous avoir contactés ! Nous avons bien reçu votre message "
            f"({contact.get_subject_display()}) et notre équipe vous répondra "
            f"dans les plus brefs délais, sous 24h ouvrées.\n\n"
            f"Voici un récapitulatif de votre message :\n{contact.message}\n\n"
            f"À très vite,\n"
            f"L'équipe AL BASSATINE VIANDES"
        )
        html_content = render_to_string('contact_thanks.html', {
            'name': contact.name,
            'subject_label': contact.get_subject_display(),
            'message': contact.message,
        })
        confirmation = EmailMultiAlternatives(
            subject="Merci pour votre message — AL BASSATINE VIANDES",
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[contact.email],
        )
        confirmation.attach_alternative(html_content, "text/html")
        confirmation.send(fail_silently=True)

        # Notification interne
        notify_to = getattr(settings, 'CONTACT_NOTIFY_EMAIL', None) or settings.DEFAULT_FROM_EMAIL
        internal_content = (
            f"Nouveau message de contact reçu :\n\n"
            f"Nom : {contact.name}\n"
            f"Email : {contact.email}\n"
            f"Téléphone : {contact.phone or '-'}\n"
            f"Société : {contact.company or '-'}\n"
            f"Objet : {contact.get_subject_display()}\n\n"
            f"Message :\n{contact.message}"
        )
        internal_html = render_to_string('contact_notification.html', {
            'name': contact.name,
            'email': contact.email,
            'phone': contact.phone,
            'company': contact.company,
            'subject_label': contact.get_subject_display(),
            'message': contact.message,
        })
        notification = EmailMultiAlternatives(
            subject=f"[Contact site] {contact.get_subject_display()} — {contact.name}",
            body=internal_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[notify_to],
        )
        notification.attach_alternative(internal_html, "text/html")
        notification.send(fail_silently=True)
    except Exception:
        pass


@csrf_protect
@require_POST
def submit_contact(request):
    try:
        data = json.loads(request.body)
        name = (data.get('name') or '').strip()
        email = (data.get('email') or '').strip()
        phone = (data.get('phone') or '').strip()
        company = (data.get('company') or '').strip()
        subject = (data.get('subject') or 'autre').strip()
        message = (data.get('message') or '').strip()

        if not name or not email or not message:
            return JsonResponse({'ok': False, 'error': 'champs_manquants'}, status=400)

        valid_subjects = dict(Contact.SUBJECT_CHOICES)
        if subject not in valid_subjects:
            subject = 'autre'

        contact = Contact.objects.create(
            name=name,
            email=email,
            phone=phone[:30],
            company=company[:150],
            subject=subject,
            message=message[:2000],
        )

        # envoi en arrière-plan pour ne pas ralentir la réponse au visiteur
        threading.Thread(target=_send_contact_emails, args=(contact,), daemon=True).start()

        return JsonResponse({'ok': True})
    except json.JSONDecodeError:
        return JsonResponse({'ok': False, 'error': 'donnees_invalides'}, status=400)


@require_GET
def list_avis(request):
    qs = Avis.objects.filter(is_approved=True)[:24]
    total = Avis.objects.filter(is_approved=True).count()
    avg = Avis.objects.filter(is_approved=True).aggregate(avg=Avg('rating'))['avg'] or 0
    return JsonResponse({
        'ok': True,
        'avis': [_serialize_avis(a) for a in qs],
        'total': total,
        'average': round(avg, 1),
    })