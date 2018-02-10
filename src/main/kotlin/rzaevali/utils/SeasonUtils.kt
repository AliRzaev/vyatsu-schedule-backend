package rzaevali.utils

import rzaevali.exceptions.UnknownValueException

const val SEASON_AUTUMN = "autumn"

const val SEASON_SPRING = "spring"

@Throws(UnknownValueException::class)
fun checkSeason(season: String): String {
    return if (season != SEASON_AUTUMN && season != SEASON_SPRING) {
        throw UnknownValueException("Unknown season: $season")
    } else {
        season
    }
}

@Throws(UnknownValueException::class)
fun getSeasonKey(season: String): String {
    checkSeason(season)

    return if (season == SEASON_AUTUMN) "1" else "2"
}