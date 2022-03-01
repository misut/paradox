import json
from abc import ABC, abstractmethod
from pathlib import Path

from pydantic import BaseModel, Field

from paradox.domain.apparition.base import Apparition, ApparitionSprite, ApparitionStatus, ApparitionTag
from paradox.domain.apparition.character import Character
from paradox.domain.base import Direction, ValueObject
from paradox.domain.sprite import SpriteTag, sprite_assets

ApparitionSpriteTags = dict[ApparitionStatus, dict[Direction, SpriteTag]]


def create_apparition_sprite(apparition_sprite_tags: ApparitionSpriteTags) -> ApparitionSprite:
    return {
        status: {
            direction: sprite_assets.copy(apparition_sprite_tags.get(status, {}).get(direction, SpriteTag.APPARITION_TEST)) 
            for direction in Direction
        } for status in ApparitionStatus
    }


class ApparitionStats(ValueObject):
    ...


class ApparitionAsset(ValueObject):
    tag: ApparitionTag
    sprites: ApparitionSpriteTags
    stats: ApparitionStats

    def apparition(self) -> Apparition | Character:
        if self.tag.type == "character":
            return Character(
                name="test_character",
                tag=self.tag,
                coo=(0.5, 0.5),
                roo=(0.5, 0.5),
                dim=(0.3, 1.0),
                sprites=create_apparition_sprite(self.sprites),
                velocity_limit=5.0,
                jump_limit=2,
            )

        return Apparition(
            name="test_apparition",
            tag=self.tag,
            coo=(0.5, 0.5),
            roo=(0.5, 0.5),
            dim=(0.3, 1.0),
            sprites=create_apparition_sprite(self.sprites),
        )


class ApparitionAssetManager(ABC, BaseModel):
    @abstractmethod
    def copy(self, tag: ApparitionTag) -> Apparition | None:
        ...


class ApparitionInfo(ValueObject):
    tag: ApparitionTag
    path: Path


class FileApparitionAssetManager(ApparitionAssetManager):
    apparition_assets: dict[ApparitionTag, ApparitionAsset] = Field(default={})
    apparitions_path: Path = Field(default=Path("assets/apparitions"))

    def initialize(self, apparitions_path: Path = Path("assets/apparitions")) -> None:
        self.apparition_assets.clear()
        self.apparitions_path = apparitions_path
        self.load_apparitions()

    def from_info(self, apparition_info: ApparitionInfo) -> ApparitionAsset:
        file_path = self.apparitions_path.joinpath(apparition_info.path)

        with file_path.open(mode="rt", encoding="utf-8") as stream:
            apparition_asset_dict = json.load(stream)
        
        apparition_asset_dict["sprites"]
        return ApparitionAsset.parse_obj(apparition_asset_dict)

    def load_apparitions(self) -> None:
        json_path = self.apparitions_path.joinpath("apparitions.json")
        with json_path.open(mode="rt", encoding="utf-8") as stream:
            apparition_info_dicts = json.load(stream)
        
        for apparition_info_dict in apparition_info_dicts:
            apparition_info = ApparitionInfo.parse_obj(apparition_info_dict)
            self.apparition_assets[apparition_info.tag] = self.from_info(apparition_info)

    def copy(self, tag: ApparitionTag) -> Apparition | Character | None:
        if tag not in self.apparition_assets:
            return None
        
        return self.apparition_assets[tag].apparition()


apparition_assets = FileApparitionAssetManager()
