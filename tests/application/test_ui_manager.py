from paradox.application import UIManager
from paradox.domain import LayoutUI, Post, TextUI


class ThisPost(Post):
    ...


class ThatPost(Post):
    ...


def test_click(ui_manager: UIManager) -> None:
    layout = LayoutUI(pos=(0, 0), size=(100, 100))

    text_topleft = TextUI(pos=(0, 0), size=(20, 20))

    @text_topleft.on_click()
    def click_text_topleft() -> ThisPost:
        return ThisPost()

    layout.allocate(text_topleft)

    text_bottomright = TextUI(pos=(80, 80), size=(20, 20))

    @text_bottomright.on_click()
    def click_text_bottomright() -> ThatPost:
        return ThatPost()

    layout.allocate(text_bottomright)

    text_overlapping = TextUI(pos=(10, 10), size=(80, 80))
    layout.allocate(text_overlapping)

    ui_manager.allocate(layout)

    assert ui_manager.click((90, 10)) == None
    assert isinstance(ui_manager.click((0, 0)), ThisPost)
    assert isinstance(ui_manager.click((99, 99)), ThatPost)
    assert ui_manager.click((10, 10)) == ui_manager.click((89, 89)) == None


def test_hover(ui_manager: UIManager) -> None:
    layout = LayoutUI(pos=(0, 0), size=(100, 100))

    text_topleft = TextUI(pos=(0, 0), size=(20, 20))

    @text_topleft.on_hover()
    def hover_text_topleft() -> ThisPost:
        return ThisPost()

    layout.allocate(text_topleft)

    text_bottomright = TextUI(pos=(80, 80), size=(20, 20))

    @text_bottomright.on_hover()
    def hover_text_bottomright() -> ThatPost:
        return ThatPost()

    layout.allocate(text_bottomright)

    text_overlapping = TextUI(pos=(10, 10), size=(80, 80))
    layout.allocate(text_overlapping)

    ui_manager.allocate(layout)

    assert ui_manager.hover((90, 10)) == None

    assert isinstance(ui_manager.hover((0, 0)), ThisPost)
    for idx in range(0, 10):
        assert ui_manager.hover((idx, idx)) == None

    assert isinstance(ui_manager.hover((99, 99)), ThatPost)
    for idx in range(90, 100):
        assert ui_manager.hover((idx, idx)) == None

    assert ui_manager.hover((10, 10)) == ui_manager.hover((89, 89)) == None
