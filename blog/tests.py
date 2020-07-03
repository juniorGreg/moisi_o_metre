from django.test import SimpleTestCase
from .post_statistics import *
from .models import Post

# Create your tests here.
class PostTestCase(SimpleTestCase):
    def test_average_reading_time(self):
        text = "C’est-tu si bon que ça le bio ?"
        wc = word_count(text)
        self.assertEqual(wc, 7)
        art = average_reading_time(wc)
        self.assertEqual(art, 0)

    def test_average_reading_time_long_text(self):
        text = "C’est certain que ma mère ne va pas aimer ce post. Elle ne jure que sur le bio. Je dois avouer que j’ai été longtemps séduit par les promesses du l’agriculture biologique. Ça serait plus écologique car ça n’utiliserait pas des engrais et des pesticides chimiques. Les légumes bios seraient meilleurs pour la santé et ils auraient une meilleure valeur nutritive que leurs cousins conventionnels. Ça semble fantastique ! Alors pourquoi tout le monde n’a pas déjà abandonné l’agriculture conventionnelle. Ça serait idiot de continuer à manger des aliments chimiques si on a une alternative bien meilleure."

        wc = word_count(text)        
        self.assertEqual(wc, 96)
        art = average_reading_time(wc)
        self.assertEqual(art, 1)
