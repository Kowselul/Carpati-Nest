# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from CarpatiNest_app.models import Mountain, Refuge, Review
import random
from datetime import timedelta

class Command(BaseCommand):
    help = 'Create test users and reviews for refuges'

    def handle(self, *args, **options):
        # Lista de nume romanesti pentru generarea utilizatorilor
        romanian_first_names = [
            "Alexandru", "Andrei", "Mihai", "Stefan", "Gabriel", "Ionut", "Cristian", "Marian", "Florin", "Bogdan",
            "Maria", "Ana", "Elena", "Ioana", "Andreea", "Cristina", "Mihaela", "Gabriela", "Daniela", "Alexandra"
        ]
        
        romanian_last_names = [
            "Popescu", "Ionescu", "Popa", "Pop", "Dumitru", "Stan", "Stoica", "Gheorghe", "Rusu", "Munteanu",
            "Matei", "Constantin", "Moldovan", "Stanciu", "Vasile", "Oprea", "Dinu", "Tudor", "Dobre", "Barbu"
        ]
        
        # Comentarii pentru recenzii
        positive_comments = [
            "Priveliste spectaculoasa, personalul este foarte amabil.",
            "Unul dintre cele mai frumoase locuri din muntii nostri. Recomand cu caldura!",
            "Refugiul este bine intretinut si curat. Gazda este foarte primitoare.",
            "O experienta minunata, cu siguranta voi reveni!",
            "Peisaj de vis, atmosfera placuta si personal prietenos.",
            "Cel mai frumos loc in care am fost in ultimii ani.",
            "Locatia perfecta pentru a te bucura de natura salbatica.",
            "Refugiu curat si confortabil, exact ce aveam nevoie dupa o zi de drumetie.",
            "Personalul foarte de treaba, m-am simtit binevenit de la inceput.",
            "O bijuterie ascunsa in munti, recomand cu incredere!"
        ]
        
        neutral_comments = [
            "Refugiul este decent, dar ar putea beneficia de cateva imbunatatiri.",
            "Experienta ok, nimic spectaculos dar nici dezamagitor.",
            "Conditii bune pentru un refugiu montan, dar nimic iesit din comun.",
            "Peisaj frumos, dar refugiul necesita unele renovari.",
            "Personalul amabil, dar facilitati limitate."
        ]
        
        negative_comments = [
            "Din pacate, refugiul nu era prea curat.",
            "Putin dezamagit de conditiile gasite.",
            "Personalul nu a fost foarte amabil, nu m-am simtit binevenit.",
            "Prea aglomerat si galagios pentru o experienta montana autentica."
        ]
        
        # Crearea utilizatorilor de test (10 utilizatori)
        self.stdout.write("Crearea utilizatorilor de test...")
        users_created = 0
        test_users = []
        
        for i in range(10):
            first_name = random.choice(romanian_first_names)
            last_name = random.choice(romanian_last_names)
            username = f"{first_name.lower()}_{last_name.lower()}{random.randint(1, 99)}"
            email = f"{username}@example.com"
            
            # Verificare daca utilizatorul exista deja
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password="Parola123!",
                    first_name=first_name,
                    last_name=last_name
                )
                test_users.append(user)
                users_created += 1
                self.stdout.write(self.style.SUCCESS(f"Creat utilizator: {username}"))
            else:
                # Adaugam utilizatorul existent la lista noastra
                user = User.objects.get(username=username)
                test_users.append(user)
                self.stdout.write(f"Utilizatorul {username} exista deja")
        
        self.stdout.write(self.style.SUCCESS(f"{users_created} utilizatori noi creati"))
        
        # Adaugam recenzii pentru fiecare refugiu (5-10 recenzii per refugiu)
        self.stdout.write("Adaugarea recenziilor...")
        reviews_created = 0
        
        refuges = Refuge.objects.all()
        if not refuges:
            self.stdout.write(self.style.ERROR("Nu exista refugii in baza de date!"))
            return
        
        for refuge in refuges:
            # Generam intre 5 si 10 recenzii per refugiu
            num_reviews = random.randint(5, 10)
            
            for _ in range(num_reviews):
                user = random.choice(test_users)
                rating = random.choices([5, 4, 3, 2, 1], weights=[0.4, 0.3, 0.15, 0.1, 0.05])[0]
                
                # Selectam comentariul in functie de rating
                if rating >= 4:
                    comment = random.choice(positive_comments)
                elif rating == 3:
                    comment = random.choice(neutral_comments)
                else:
                    comment = random.choice(negative_comments)
                
                # Data crearii - intre 1 si 180 de zile in urma
                days_ago = random.randint(1, 180)
                created_at = timezone.now() - timedelta(days=days_ago)
                
                # Verificam daca utilizatorul are deja o recenzie pentru acest refugiu
                if not Review.objects.filter(user=user, refuge=refuge).exists():
                    review = Review.objects.create(
                        user=user,
                        refuge=refuge,
                        rating=rating,
                        comment=comment,
                        created_at=created_at
                    )
                    reviews_created += 1
                    self.stdout.write(f"Adaugat recenzie pentru {refuge.name} de la {user.username} (Rating: {rating}/5)")
        
        self.stdout.write(self.style.SUCCESS(f"{reviews_created} recenzii create cu succes!"))
