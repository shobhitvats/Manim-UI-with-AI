class SceneManager:
    def __init__(self):
        self.scenes = []
        self.current_scene_index = -1

    def create_scene(self, scene_name):
        scene = {
            'name': scene_name,
            'objects': [],
            'animations': []
        }
        self.scenes.append(scene)
        self.current_scene_index = len(self.scenes) - 1
        return scene

    def add_object_to_scene(self, obj):
        if self.current_scene_index >= 0:
            self.scenes[self.current_scene_index]['objects'].append(obj)

    def add_animation_to_scene(self, animation):
        if self.current_scene_index >= 0:
            self.scenes[self.current_scene_index]['animations'].append(animation)

    def get_current_scene(self):
        if self.current_scene_index >= 0:
            return self.scenes[self.current_scene_index]
        return None

    def switch_scene(self, index):
        if 0 <= index < len(self.scenes):
            self.current_scene_index = index

    def get_all_scenes(self):
        return self.scenes

    def clear_current_scene(self):
        if self.current_scene_index >= 0:
            self.scenes[self.current_scene_index]['objects'] = []
            self.scenes[self.current_scene_index]['animations'] = []