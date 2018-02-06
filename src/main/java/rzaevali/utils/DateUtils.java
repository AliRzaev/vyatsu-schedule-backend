package rzaevali.utils;

import java.time.LocalDate;
import java.time.Month;
import java.util.List;

import static com.google.common.base.Preconditions.checkArgument;
import static com.google.common.base.Preconditions.checkNotNull;

public class DateUtils {

    public static boolean isAutumn(LocalDate currentDate) {
        checkNotNull(currentDate, "Date must not be null");

        int monthValue = currentDate.getMonthValue();
        int augustValue = Month.AUGUST.getValue();
        int decemberValue = Month.DECEMBER.getValue();

        return monthValue <= decemberValue && monthValue >= augustValue;
    }

    public static boolean isSpring(LocalDate currentDate) {
        return !isAutumn(currentDate);
    }

    public static int compareDates(List<String> first, List<String> second) {
        checkArgument(first.size() == 2);
        checkArgument(second.size() == 2);

        LocalDate firstDate = parseDate(first.get(0));
        LocalDate secondDate = parseDate(second.get(0));

        return firstDate.compareTo(secondDate);
    }

    public static LocalDate parseDate(String date) {
        checkNotNull(date, "Date must not be null");

        int day = Integer.parseInt(date.substring(0, 2));
        int month = Integer.parseInt(date.substring(2, 4));
        int year = Integer.parseInt(date.substring(4));

        return LocalDate.of(year, month, day);
    }

}
