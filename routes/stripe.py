from fastapi import APIRouter, HTTPException, Body, Header
from typing import Optional
import stripe
import os
from dotenv import load_dotenv
from utils.supabase_client import SupabaseClient

# Charger les variables d'environnement
load_dotenv()

stripe_router = APIRouter()

# Initialiser le client Supabase
def get_supabase_client():
    return SupabaseClient.get_client()

# Initialiser Stripe avec la clé secrète depuis les variables d'environnement
STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY')
if STRIPE_SECRET_KEY:
    stripe.api_key = STRIPE_SECRET_KEY
    print(f"✅ Stripe configuré avec la clé secrète: {STRIPE_SECRET_KEY[:20]}...")
else:
    print("⚠️ STRIPE_SECRET_KEY non configurée")

@stripe_router.post('/create-checkout-session')
async def create_checkout_session(request: dict):
    """Créer une session Stripe Checkout pour un pack de tokens"""
    if not STRIPE_SECRET_KEY:
        raise HTTPException(
            status_code=503,
            detail="Stripe n'est pas configuré sur le serveur"
        )
    
    try:
        user_id = request.get('user_id')
        product_name = request.get('product_name')
        amount = request.get('amount')  # Montant en euros
        token_amount = request.get('token_amount', 0)
        pack_id = request.get('pack_id')
        
        # Créer une session de paiement
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'eur',
                    'product_data': {
                        'name': product_name,
                    },
                    'unit_amount': int(amount * 100),  # Convertir en centimes
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=f"{request.get('success_url', 'http://localhost:5173')}?session_id={{CHECKOUT_SESSION_ID}}",
            cancel_url=f"{request.get('cancel_url', 'http://localhost:5173')}",
            metadata={
                'user_id': str(user_id),
                'pack_id': str(pack_id),
                'token_amount': str(token_amount),
                'type': 'token_pack'
            }
        )
        
        return {'sessionId': session.id, 'url': session.url}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@stripe_router.post('/create-subscription-session')
async def create_subscription_session(request: dict):
    """Créer une session Stripe Checkout pour un abonnement"""
    if not STRIPE_SECRET_KEY:
        raise HTTPException(
            status_code=503,
            detail="Stripe n'est pas configuré sur le serveur"
        )
    
    try:
        user_id = request.get('user_id')
        price_id = request.get('price_id')  # ID du prix Stripe
        subscription_id = request.get('subscription_id')
        
        if not price_id:
            # Si pas de price_id, créer un prix dynamique
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'eur',
                        'product_data': {
                            'name': request.get('product_name', 'Abonnement Premium'),
                        },
                        'unit_amount': int(request.get('amount', 9.99) * 100),
                        'recurring': {
                            'interval': 'month',
                        },
                    },
                    'quantity': 1,
                }],
                mode='subscription',
                success_url=f"{request.get('success_url', 'http://localhost:5173')}?session_id={{CHECKOUT_SESSION_ID}}",
                cancel_url=f"{request.get('cancel_url', 'http://localhost:5173')}",
                metadata={
                    'user_id': str(user_id),
                    'subscription_id': str(subscription_id),
                    'type': 'subscription'
                }
            )
        else:
            # Utiliser le prix existant
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price': price_id,
                    'quantity': 1,
                }],
                mode='subscription',
                success_url=f"{request.get('success_url', 'http://localhost:5173')}?session_id={{CHECKOUT_SESSION_ID}}",
                cancel_url=f"{request.get('cancel_url', 'http://localhost:5173')}",
                metadata={
                    'user_id': str(user_id),
                    'subscription_id': str(subscription_id),
                    'type': 'subscription'
                }
            )
        
        return {'sessionId': session.id, 'url': session.url}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@stripe_router.get('/verify-session/{session_id}')
async def verify_session(session_id: str):
    """Vérifier le statut d'une session Stripe"""
    if not STRIPE_SECRET_KEY:
        raise HTTPException(
            status_code=503,
            detail="Stripe n'est pas configuré"
        )
    
    try:
        session = stripe.checkout.Session.retrieve(session_id)
        
        # Si le paiement est réussi, activer l'abonnement ou ajouter les tokens
        if session.payment_status == 'paid' and session.metadata:
            user_id = session.metadata.get('user_id')
            payment_type = session.metadata.get('type')
            
            if payment_type == 'subscription' and user_id:
                # Activer l'abonnement Premium
                try:
                    supabase = get_supabase_client()
                    response = supabase.table('user_extend').update({
                        'has_subscription': True
                    }).eq('id', user_id).execute()
                    print(f"✅ Abonnement activé pour user {user_id}")
                    print(f"Response: {response}")
                except Exception as e:
                    print(f"❌ Erreur lors de l'activation de l'abonnement: {e}")
            
            elif payment_type == 'token_pack' and user_id:
                # Ajouter les tokens
                token_amount = int(session.metadata.get('token_amount', 0))
                if token_amount > 0:
                    try:
                        supabase = get_supabase_client()
                        # Récupérer le solde actuel
                        user_data = supabase.table('user_extend').select('token').eq('id', user_id).execute()
                        current_tokens = user_data.data[0].get('token', 0) if user_data.data and len(user_data.data) > 0 else 0
                        
                        # Mettre à jour avec le nouveau solde
                        supabase.table('user_extend').update({
                            'token': current_tokens + token_amount
                        }).eq('id', user_id).execute()
                        print(f"✅ {token_amount} tokens ajoutés pour user {user_id}")
                    except Exception as e:
                        print(f"❌ Erreur lors de l'ajout des tokens: {e}")
        
        return {
            'session_id': session.id,
            'status': session.payment_status,
            'paid': session.payment_status == 'paid',
            'metadata': session.metadata
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

