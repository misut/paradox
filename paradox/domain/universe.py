from abc import ABC
from math import ceil, floor
from typing import Any

from loguru import logger
from pydantic import Field, validator

from paradox.domain.apparition import Apparition
from paradox.domain.base import Direction, Entity, Updatable, ValueObject
from paradox.domain.camera import Camera
from paradox.domain.constants import Z_LIMIT
from paradox.domain.sprite import SpriteTag

EMPTY_ARRAY = [0 for _ in range(128)]


class Tile(ValueObject):
    coo: tuple[int, int]
    roo: tuple[int, int]

    lwall: SpriteTag | None
    rwall: SpriteTag | None
    slate: SpriteTag | None

    @validator("roo")
    def validate_roo(
        cls, roo: tuple[int, int], values: dict[str, Any]
    ) -> tuple[int, int]:
        coo = values.get("coo")
        if roo[0] - coo[0] == roo[1] - coo[1]:
            return roo
        raise ValueError("roo should have same z-index with coo.")

    @property
    def zidx(self) -> int:
        return self.roo[0] - self.coo[0]


class Universe(Entity, Updatable):
    apparitions: list[Apparition] = Field(default=[])
    camera: Camera = Field(default=Camera(coo=(0.0, 0.0)))
    mapping: dict[tuple[int, int], Tile] = Field(default={})

    size: tuple[int, int] = Field(default=(0, 0))

    def at(self, coo: tuple[float, float]) -> Tile | None:
        x, y = map(floor, coo)
        return self.mapping.get((x, y), None)

    def along(self, src: tuple[float, float], dst: tuple[float, float]) -> list[Tile]:
        dx, dy = dst[0] - src[0], dst[1] - src[1]

        params = []
        if dx > 0.0:
            for sol in range(floor(src[0]), ceil(dst[0]) + 1):
                params.append((sol - floor(src[0])) / dx)

        if dy > 0.0:
            for sol in range(floor(src[1]), ceil(dst[1]) + 1):
                params.append((sol - floor(src[1])) / dy)

        params.sort()
        tiles = []
        for param in params:
            tile = self.at((src[0] + dx * param, src[1] + dy * param))
            if tile == None:
                continue
            if tile not in tiles:
                tiles.append(tile)

        return tiles

    def place(self, apprition: Apparition) -> None:
        self.apparitions.append(apprition)
        self.apparitions.sort(reverse=True)

    def simulate_collisions(self, secs: float) -> None:
        # UL, UR, UB, UF, DL, DR, DB, DF
        for apparition in self.apparitions:
            futures = apparition.simulate(secs)

            coo = futures.coo
            roo = futures.roo
            dim = futures.dim

            uc = (coo[0] - dim[1] - 1, coo[1] - dim[1] - 1)
            ul = (coo[0] - dim[0] - dim[1] - 1, coo[1] - dim[1] - 1)
            ur = (coo[0] + dim[0] - dim[1] - 1, coo[1] - dim[1] - 1)
            ub = (coo[0] - dim[1] - 1, coo[1] - dim[0] - dim[1] - 1)
            uf = (coo[0] - dim[1] - 1, coo[1] + dim[0] - dim[1] - 1)
            dc = coo
            dl = (coo[0] - dim[0], coo[1])
            dr = (coo[0] + dim[0], coo[1])
            db = (coo[0], coo[1] - dim[0])
            df = (coo[0], coo[1] + dim[0])

            roo_center = tuple(map(floor, (roo[0], roo[1])))
            roo_left = tuple(map(floor, (roo[0] - dim[0], roo[1])))
            roo_right = tuple(map(floor, (roo[0] + dim[0], roo[1])))
            roo_back = tuple(map(floor, (roo[0], roo[1] - dim[0])))
            roo_front = tuple(map(floor, (roo[0], roo[1] + dim[1])))

            coll_up = False
            coll_down = False
            coll_left = False
            coll_right = False
            coll_back = False
            coll_front = False

            tiles_up = [
                tile
                for tile in map(self.at, [uc, ul, ur, ub, uf])
                if tile != None and tile.zidx < apparition.zidx
            ]
            if tiles_up:
                # logger.info("Collide up!")
                coll_up = True

            tiles_down = [
                tile
                for tile in map(self.at, [dc, dl, dr, db, df])
                if tile != None and apparition.zidx <= tile.zidx < apparition.zidx + 0.1
            ]
            if len(tiles_down) > 2 and not apparition.jumping:
                # logger.info("Collide down!")
                coll_down = True

            tiles_left = (
                [
                    tile
                    for tile in self.along(ul, dl)
                    if tile.roo == roo_left and tile.zidx > apparition.zidx
                ]
                if roo_left != roo_center
                else []
            )
            left_directions = [Direction.NORTHWEST, Direction.NORTH, Direction.WEST]
            if tiles_left and apparition.direction in left_directions:
                # logger.info("Collide left!")
                coll_left = True

            tiles_right = (
                [
                    tile
                    for tile in self.along(ur, dr)
                    if tile.roo == roo_right and tile.zidx > apparition.zidx
                ]
                if roo_right != roo_center
                else []
            )
            right_directions = [Direction.SOUTHEAST, Direction.SOUTH, Direction.EAST]
            if tiles_right and apparition.direction in right_directions:
                # logger.info("Collide right!")
                coll_right = True

            tiles_back = (
                [
                    tile
                    for tile in self.along(ub, db)
                    if tile.roo == roo_back and tile.zidx > apparition.zidx
                ]
                if roo_back != roo_center
                else []
            )
            back_directions = [Direction.NORTHEAST, Direction.NORTH, Direction.EAST]
            if tiles_back and apparition.direction in back_directions:
                # logger.info("Collide back")
                coll_back = True

            tiles_front = (
                [
                    tile
                    for tile in self.along(uf, df)
                    if tile.roo == roo_front and tile.zidx > apparition.zidx
                ]
                if roo_front != roo_center
                else []
            )
            front_directions = [Direction.SOUTHWEST, Direction.SOUTH, Direction.WEST]
            if tiles_front and apparition.direction in front_directions:
                # logger.info("Collide front")
                coll_front = True

            can_fall = True
            can_move = True

            if coll_down:
                can_fall = False

            if any([coll_left, coll_right, coll_back, coll_front]):
                can_move = False

            if can_fall:
                if not apparition.falling:
                    apparition.jump_count += 1
                apparition.gravity = apparition.fall_power
                apparition.gravitate(secs)
                apparition.fall(secs)
                if apparition.zidx < -Z_LIMIT:
                    apparition.load()
                    continue
            else:
                if apparition.falling:
                    for tile in tiles_down:
                        if apparition.zidx + 1 > tile.zidx >= apparition.zidx:
                            break
                    apparition.roo = (
                        apparition.coo[0] + tile.zidx,
                        apparition.coo[1] + tile.zidx,
                    )
                    apparition.acceleration = 0.0
                    apparition.velocity = 0.0
                    apparition.gravity = 0.0
                    apparition.fall_velocity = 0.0
                    apparition.jump_count = 0
                for tile in tiles_down:
                    if apparition.zidx + 1 > tile.zidx >= apparition.zidx:
                        apparition.save(tile.coo, tile.zidx)
                        break

            if can_move:
                apparition.accelerate(secs)
                apparition.move(secs)
            else:
                apparition.acceleration = 0.0
                apparition.velocity = 0.0

    def update(self, ticks: int) -> None:
        secs = ticks / 1000
        self.simulate_collisions(secs)
        self.camera.update(ticks)


class UniverseRepository(ABC):
    def get(self, name: str) -> Universe | None:
        ...
