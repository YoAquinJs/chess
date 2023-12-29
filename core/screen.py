from game_object import GameObject

class Screen:

    def __init__(self) -> None:
        self.gameCbjects = []

    def register_obj(self, obj: GameObject):
        if obj in self.gameCbjects:
            raise Exception("Object already added to scene")
        
        self.gameCbjects.append(obj)
        for child in obj.children:
            self.register_obj(child)

    def update(self) -> None:
        for obj in self.gameCbjects:
            obj.update()

    def render(self) -> None:
        for obj in self.gameCbjects:
            obj.render()
