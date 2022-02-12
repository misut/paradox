from paradox.application.film_director import FilmDirector
from paradox.application.scenes.intro import intro_director
from paradox.application.scenes.playing import playing_director
from paradox.application.scenes.setting import setting_director

paradox_director = FilmDirector()
paradox_director.invite(
    intro_director,
    playing_director,
    setting_director,
)
