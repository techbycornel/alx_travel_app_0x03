from django.core.management.base import BaseCommand
from listings.models import Listing
from django.contrib.auth.models import User
import random


class Command(BaseCommand):
    help = "Seed the database with sample listings"

    def handle(self, *args, **kwargs):
        # Create a demo user if not exists
        user, created = User.objects.get_or_create(username="demo_user")
        if created:
            user.set_password("password123")
            user.save()

        # Sample data
        sample_listings = [
            {"title": "Beach House", "description": "Ocean view house", "price_per_night": 120.00, "location": "Lagos"},
            {"title": "Mountain Cabin", "description": "Cozy cabin in the hills", "price_per_night": 80.00, "location": "Jos"},
            {"title": "City Apartment", "description": "Modern flat downtown", "price_per_night": 150.00, "location": "Abuja"},
        ]

        for data in sample_listings:
            listing, created = Listing.objects.get_or_create(**data)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created listing: {listing.title}"))
            else:
                self.stdout.write(f"Listing already exists: {listing.title}")
