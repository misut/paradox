from pytest import raises

from paradox.domain.errors import UIAllocateError
from paradox.domain.posts import Post
from paradox.domain.uis.base import UI


class ThisPost(Post):
    ...


class ThatPost(Post):
    ...


def test_allocate() -> None:
    parent = UI(pos=(0, 0), size=(100, 100))

    child = UI(pos=(0, 0), size=(10, 10))
    parent.allocate(child)
    with raises(UIAllocateError):
        parent.allocate(child)
    assert parent.priority == child.priority

    bastard = UI(pos=(10, 10), size=(10, 10))
    parent.allocate(bastard)
    
    assert len(parent.childs) == 2
    assert parent.childs[0] == bastard
    assert parent.childs[1] == child


def test_at() -> None:
    ui = UI(pos=(0, 0), size=(100, 100))

    ui_one = UI(pos=(0, 0), size=(60, 60))
    ui.allocate(ui_one)
    assert ui.at((30, 30)) == ui_one
    
    ui_two = UI(pos=(40, 40), size=(60, 60))
    ui.allocate(ui_two)
    assert ui.at((70, 70)) == ui_two

    assert ui.at((50, 50)) == ui_two

    assert ui.at((30, 70)) == ui.at((70, 30)) == ui


def test_embracing() -> None:
    parent = UI(pos=(0, 0), size=(100, 100))

    small_child = UI(pos=(10, 10), size=(80, 80))
    assert parent.embracing(small_child)

    fit_child = UI(pos=(0, 0), size=(100, 100))
    assert parent.embracing(fit_child)

    big_child = UI(pos=(0, 0), size=(200, 200))
    assert not parent.embracing(big_child)


def test_including() -> None:
    ui = UI(pos=(0, 0), size=(100, 100))

    assert ui.including((50, 50))

    assert ui.including((99, 99))

    assert not ui.including((100, 100))


def test_overlapping() -> None:
    ui = UI(pos=(0, 0), size=(100, 100))

    overlapping_ui = UI(pos=(50, 50), size=(100, 100))
    assert ui.overlapping(overlapping_ui)

    tangent_ui = UI(pos=(100, 100), size=(100, 100))
    assert not ui.overlapping(tangent_ui)


def test_actor() -> None:
    ui = UI(pos=(0, 0), size=(100, 100))
    assert ui.click() == ui.hover() == None

    @ui.on_click()
    def click() -> ThisPost:
        return ThisPost()
    assert isinstance(ui.click(), ThisPost)

    @ui.on_hover()
    def hover() -> ThatPost:
        return ThatPost()
    assert isinstance(ui.hover(), ThatPost)
