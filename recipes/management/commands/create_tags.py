from collections import namedtuple

from django.core.management.base import BaseCommand

from recipes.models import Tag

Tags_tuple = namedtuple('Tag', ['title', 'color', 'display_name'])

br = Tags_tuple(title='Завтрак', color='#E26C2D', display_name='Завтрак')
ln = Tags_tuple(title='Обед', color='#49B64E', display_name='Обед')
dn = Tags_tuple(title='Ужин', color='#8775D2', display_name='Ужин')

tags = [br, ln, dn]


class Command(BaseCommand):
    help = 'Creat 3 base tags: Breakfast, Lunch, Dinner'

    def handle(self, *args, **options):
        for tag in tags:
            if Tag.objects.filter(display_name=tag.display_name).exists():
                print(f'{tag.display_name} already exist')
            else:
                Tag.objects.create(title=tag.title,
                                   display_name=tag.display_name,
                                   color=tag.color)
                print(f'{tag.display_name} instance created')
