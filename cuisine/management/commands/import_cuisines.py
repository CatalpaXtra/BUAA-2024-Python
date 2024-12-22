import os
from django.core.management.base import BaseCommand
from cuisine.models import Cuisine

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('directory', type=str)

    def handle(self, *args, **kwargs):
        directory = kwargs['directory']
        self.import_cuisines(directory)

    def import_cuisines(self, directory):
        for root, _, files in os.walk(directory):
            for filename in files:
                if filename.lower().endswith('.jpg') or filename.lower().endswith('.png'):
                    folders = root.split('\\')
                    type = folders[2]
                    front = filename.rsplit('.', 1)[0].split('#')
                    name = front[0]
                    if type == 'meal':
                        cafeteria = folders[3]
                        floor = folders[4]
                        window = folders[5]
                        # 如果是 'name#price#tag1&tag2&tag3' 格式：
                        if len(front) == 3:
                            cost = float(front[1])
                            tags = front[2].split('&')
                            tag1 = tags[0]
                            # meal最少会有1个tag
                            if len(tags) <= 1:
                                tag2 = ''
                            else:
                                tag2 = tags[1]
                            if len(tags) == 3:
                                tag3 = tags[2]
                            else:
                                tag3 = ''
                        elif len(front) == 2:
                            imformation = front[1].split('&')
                            # 此处imformation相当于price + tag * 3
                            cost = float(imformation[0])
                            tag1 = imformation[1]
                            if len(imformation) <= 2:
                                tag2 = ''
                            else:
                                tag2 = imformation[2]
                            if len(imformation) == 4:
                                tag3 = imformation[3]
                            else:
                                tag3 = ''
                    elif type == 'drink':
                        cafeteria = folders[3]
                        floor = folders[4]
                        window = folders[5]
                        cost = float(front[1])
                        tag1 = tag2 = tag3 = ''
                    elif type == 'breakfast':
                        cafeteria = floor = window = ''
                        cost = float(front[1])
                        tags = front[2].split('&')
                        # breakfast 最少会有0个tag
                        if len(tags) == 0:
                            tag1 = ''
                        else:
                            tag1 = tags[0]
                        if len(tags) <= 1:
                            tag2 = ''
                        else:
                            tag2 = tags[1]
                        if len(tags) <= 2:
                            tag3 = ''
                        else:
                            tag3 = tags[2]
                    elif type == 'selfselect':
                        cafeteria = floor = ''
                        window = folders[3]
                        cost = -1
                        tag1 = front[1]
                        tag2 = tag3 = ''
                    cuisine = Cuisine(name=name, type=type, cafeteria=cafeteria, floor=floor, window=window, cost=cost,\
                                        image=os.path.join(root, filename), tag1 = tag1, tag2 = tag2, tag3 = tag3)
                    cuisine.save()