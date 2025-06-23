import pygame
import xml.etree.ElementTree as ET

class SpriteSheet:
    def __init__(self, image_path, plist_path, scale=0.4):
        self.sheet = pygame.image.load(image_path).convert_alpha()
        self.frames, self.frame_names = self._load_frames(plist_path)
        self.scale = scale

    def _load_frames(self, plist_path):
        tree = ET.parse(plist_path)
        root = tree.getroot()
        frames = []
        frame_names = []
        dicts = root.findall('.//dict')
        frames_dict = None
        for d in dicts:
            children = list(d)
            for i, elem in enumerate(children):
                if elem.tag == 'key' and elem.text == 'frames':
                    frames_dict = children[i+1]
                    break
            if frames_dict is not None:
                break
        if frames_dict is None:
            return frames, frame_names
        children = list(frames_dict)
        i = 0
        while i < len(children):
            key_elem = children[i]
            if key_elem.tag == 'key':
                frame_name = key_elem.text
                frame_data_dict = children[i+1]
                for j in range(len(frame_data_dict)):
                    if frame_data_dict[j].tag == 'key' and frame_data_dict[j].text == 'textureRect':
                        rect_str = frame_data_dict[j+1].text
                        rect = rect_str.replace('{','').replace('}','').replace(' ','').replace('},{',',').split(',')
                        x, y, w, h = map(int, rect)
                        frames.append(pygame.Rect(x, y, w, h))
                        frame_names.append(frame_name)
                        break
                i += 2
            else:
                i += 1
        return frames, frame_names

    def get_image(self, idx):
        rect = self.frames[idx % len(self.frames)]
        image = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        image.blit(self.sheet, (0, 0), rect)
        if self.scale != 1:
            new_size = (int(rect.width * self.scale), int(rect.height * self.scale))
            image = pygame.transform.smoothscale(image, new_size)
        return image

    def get_image_by_name(self, name):
        if name in self.frame_names:
            idx = self.frame_names.index(name)
            return self.get_image(idx)
        return self.get_image(0)

    def get_images_by_range(self, start, end):
        images = []
        for idx in range(start, end):
            images.append(self.get_image(idx))
        return images 