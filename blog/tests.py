from django.test import TestCase
from .post_statistics import *
from .models import Post, RottenPoint

# Create your tests here.
class PostTestCase(TestCase):
    def setUp(self):
        post = Post.objects.create(title="test", content="C’est-tu si bon que ça le bio ?")
        text = "C’est certain que ma mère ne va pas aimer ce post. Elle ne jure que sur le bio. Je dois avouer que j’ai été longtemps séduit par les promesses du l’agriculture biologique. Ça serait plus écologique car ça n’utiliserait pas des engrais et des pesticides chimiques. Les légumes bios seraient meilleurs pour la santé et ils auraient une meilleure valeur nutritive que leurs cousins conventionnels. Ça semble fantastique ! Alors pourquoi tout le monde n’a pas déjà abandonné l’agriculture conventionnelle. Ça serait idiot de continuer à manger des aliments chimiques si on a une alternative bien meilleure."

        rp1 = RottenPoint.objects.create(post=post, title="test", description=text)
        rp2 = RottenPoint.objects.create(post=post, title="test2", description=text)



    def test_statistics(self):
        post = Post.objects.get(title="test")
        wc = post.statistics.word_count
        self.assertEqual(wc, 199)
        art = post.statistics.avg_reading_time
        self.assertEqual(art, 1)
