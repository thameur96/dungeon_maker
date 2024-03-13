import Dungeon3_0

dungeon=Dungeon3_0.Dungeon(100,(700,700))
dungeon.load('dungeon2')
dungeon.draw()
# dungeon.part_draw()
dungeon.fps=60
dungeon.game_mode()