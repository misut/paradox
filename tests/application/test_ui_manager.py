from paradox.application import UIManager
from paradox.domain import LayoutUI, Post, TextUI


class ThisPost(Post):
    ...


class ThatPost(Post):
    ...


def test_click_on(ui_manager: UIManager) -> None:
    layout = LayoutUI(pos=(0, 0), size=(100, 100))

    text_topleft = TextUI(pos=(0, 0), size=(20, 20))

    @text_topleft.on_click()
    def click_text_topleft(self_ui: TextUI) -> list[Post]:
        return [ThisPost()]

    layout.allocate(text_topleft)

    text_bottomright = TextUI(pos=(80, 80), size=(20, 20))

    @text_bottomright.on_click()
    def click_text_bottomright(self_ui: TextUI) -> list[Post]:
        return [ThatPost()]

    layout.allocate(text_bottomright)

    text_overlapping = TextUI(pos=(10, 10), size=(80, 80))
    layout.allocate(text_overlapping)

    ui_manager.allocate(layout)

    assert ui_manager.click_on((90, 10)) == []
    assert isinstance(ui_manager.click_on((0, 0))[0], ThisPost)
    assert isinstance(ui_manager.click_on((99, 99))[0], ThatPost)
    assert ui_manager.click_on((10, 10)) == ui_manager.click_on((89, 89)) == []


def test_hover(ui_manager: UIManager) -> None:
    layout = LayoutUI(pos=(0, 0), size=(100, 100))

    text_topleft = TextUI(pos=(0, 0), size=(20, 20))

    @text_topleft.on_hover()
    def hover_text_topleft(self_ui: TextUI) -> list[Post]:
        return [ThisPost()]

    layout.allocate(text_topleft)

    text_bottomright = TextUI(pos=(80, 80), size=(20, 20))

    @text_bottomright.on_hover()
    def hover_text_bottomright(self_ui: TextUI) -> list[Post]:
        return [ThatPost()]

    layout.allocate(text_bottomright)

    text_overlapping = TextUI(pos=(10, 10), size=(80, 80))
    layout.allocate(text_overlapping)

    ui_manager.allocate(layout)

    assert ui_manager.hover((90, 10)) == []

    assert isinstance(ui_manager.hover((0, 0))[0], ThisPost)
    for idx in range(0, 10):
        assert ui_manager.hover((idx, idx)) == []

    assert isinstance(ui_manager.hover((99, 99))[0], ThatPost)
    for idx in range(90, 100):
        assert ui_manager.hover((idx, idx)) == []

    assert ui_manager.hover((10, 10)) == ui_manager.hover((89, 89)) == []
