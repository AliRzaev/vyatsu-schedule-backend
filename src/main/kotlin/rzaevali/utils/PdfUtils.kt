package rzaevali.utils

import org.apache.pdfbox.pdmodel.PDDocument
import rzaevali.exceptions.PdfFileFormatException
import rzaevali.exceptions.PdfFileProcessingException
import rzaevali.exceptions.VyatsuScheduleException
import rzaevali.exceptions.VyatsuServerException
import technology.tabula.ObjectExtractor
import technology.tabula.extractors.SpreadsheetExtractionAlgorithm
import java.io.IOException
import java.io.InputStream
import java.net.URL

typealias NestedList = List<List<List<String>>>

@Throws(PdfFileProcessingException::class)
private fun extractRows(stream: InputStream): List<String> {
    try {
        PDDocument.load(stream).use { pdfDocument ->
            val pageIterator = ObjectExtractor(pdfDocument).extract()
            val algorithm = SpreadsheetExtractionAlgorithm()

            return pageIterator.asSequence()
                    .flatMap { page -> algorithm.extract(page).asSequence() }
                    .flatMap({ table -> table.rows.asSequence() })
                    .map { row ->
                        row.asSequence()
                                .map { textContainer -> textContainer.text }
                                .filter { text -> text != "" }
                                .joinToString(" ")
                    }
                    .map { text -> text.replaceFirst(Regex("\\d{2}:\\d{2}-\\d{2}:\\d{2}\\s*"), "") }
                    .drop(2)
                    .toList()
        }
    } catch (ignore: Exception) {
        throw PdfFileProcessingException("Error while processing pdf file")
    }

}

@Throws(VyatsuScheduleException::class)
fun extractSchedule(stream: InputStream): NestedList {
    val daysCount = 14
    val lessonsPerDay = 7

    val rows = extractRows(stream)
    if (rows.size != daysCount * lessonsPerDay) {
        throw PdfFileFormatException("Invalid pdf file")
    }

    val days = (0..13).asSequence().map { day ->
        val fromIndex = day * 7
        val toIndex = fromIndex + 7
        rows.subList(fromIndex, toIndex)
    }.toList()

    return listOf(
            days.subList(0, 6),
            days.subList(7, 13)
    )
}

@Throws(VyatsuScheduleException::class)
fun extractSchedule(url: String): NestedList {
    try {
        return extractSchedule(URL(url).openStream())
    } catch (ignore: IOException) {
        throw VyatsuServerException("vyatsu.ru server error")
    }
}


