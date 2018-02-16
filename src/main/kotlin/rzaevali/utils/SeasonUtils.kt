package rzaevali.utils

import rzaevali.exceptions.UnknownValueException

const val SEASON_AUTUMN = "autumn"

const val SEASON_SPRING = "spring"

/**
 * Check whether the season name is valid or not and return it
 * The valid names are [SEASON_AUTUMN] and [SEASON_SPRING]
 *
 * @param season season name
 * @return season name if it is valid
 * @throws UnknownValueException if season name doesn't equal to [SEASON_AUTUMN] or [SEASON_SPRING]
 */
@Throws(UnknownValueException::class)
fun checkSeason(season: String): String {
    return if (season != SEASON_AUTUMN && season != SEASON_SPRING) {
        throw UnknownValueException("Unknown season: $season")
    } else {
        season
    }
}

/**
 * Map season name to the season key
 *
 * @param season season name
 * @return season key
 * @throws UnknownValueException if season name isn't valid
 */
@Throws(UnknownValueException::class)
fun getSeasonKey(season: String): String {
    checkSeason(season)

    return if (season == SEASON_AUTUMN) "1" else "2"
}